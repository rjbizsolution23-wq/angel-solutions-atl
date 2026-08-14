"""
Prometheus Archive Engine - Stripe Webhooks Processor
Syncs Stripe account events back into database user subscription states
"""
import os
import json
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import stripe

from ...core.db import get_db
from ...models.database import User, SubscriptionPlan

router = APIRouter()

STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")

async def update_user_subscription(
    db: AsyncSession,
    customer_id: str,
    subscription_id: str,
    status_str: str,
    price_id: str
):
    """Update active user subscription values inside local relational tables"""
    result = await db.execute(select(User).filter(User.stripe_customer_id == customer_id))
    user = result.scalars().first()
    if not user:
        return

    # Map stripe price ids to subscription tier name
    tier_name = "free"
    from ...core.payments import PRICE_TIER_MAPPING
    for name, mapped_price in PRICE_TIER_MAPPING.items():
        if mapped_price == price_id:
            tier_name = name

    # Handle subscription cancellations or billing lapses
    if status_str not in ["active", "trialing"]:
        tier_name = "free"

    # Update User object
    user.subscription_tier = tier_name
    user.stripe_subscription_id = subscription_id
    db.add(user)

    # Sync matching SubscriptionPlan resource limit metrics
    plan_result = await db.execute(select(SubscriptionPlan).filter(SubscriptionPlan.user_id == user.id))
    plan = plan_result.scalars().first()
    if not plan:
        # Create a new subscription plan record
        from uuid import uuid4
        plan = SubscriptionPlan(
            id=str(uuid4()),
            user_id=user.id,
            plan_name=tier_name,
            is_active=(tier_name != "free")
        )
    
    plan.plan_name = tier_name
    plan.is_active = (tier_name != "free")
    
    # Reset limits dynamically based on target tier
    if tier_name == "pro":
        plan.archives_limit = 200
        plan.ai_queries_limit = 100
        plan.storage_limit_mb = 10000.0 # 10GB
    elif tier_name == "enterprise":
        plan.archives_limit = 5000
        plan.ai_queries_limit = 10000
        plan.storage_limit_mb = 100000.0 # 100GB
    else:
        plan.archives_limit = 50
        plan.ai_queries_limit = 10
        plan.storage_limit_mb = 500.0 # 500MB

    db.add(plan)
    await db.commit()

    # Synchronize subscription updates to Base44 Cloud Entities NoSQL
    from ...core.base44_sync import sync_to_base44
    await sync_to_base44("SubscriptionPlan", {
        "user_id": str(user.id),
        "plan_name": tier_name,
        "is_active": (tier_name != "free"),
        "archives_limit": plan.archives_limit,
        "ai_queries_limit": plan.ai_queries_limit,
        "storage_limit_mb": plan.storage_limit_mb,
        "stripe_subscription_id": subscription_id
    })

@router.post("/stripe")
async def stripe_webhook_endpoint(request: Request, db: AsyncSession = Depends(get_db)):
    """Receives and processes active events dispatched from the Stripe webhook broker"""
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")
    
    event = None

    if STRIPE_WEBHOOK_SECRET and sig_header:
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, STRIPE_WEBHOOK_SECRET
            )
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid payload signature") from exc
        except stripe.error.SignatureVerificationError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Signature verification failed") from exc
    else:
        # Fallback for unauthenticated local simulated webhooks
        try:
            event_json = json.loads(payload.decode("utf-8"))
            event = stripe.Event.construct_from(event_json, stripe.api_key)
        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to parse custom event payload") from exc

    event_type = event["type"]
    data_object = event["data"]["object"]

    # Handle completion checkout sessions
    if event_type == "checkout.session.completed":
        customer_id = data_object.get("customer")
        subscription_id = data_object.get("subscription")
        
        # Retrieve active subscription details to extract exact pricing ID
        if subscription_id:
            try:
                sub_detail = stripe.Subscription.retrieve(subscription_id)
                price_id = sub_detail["items"]["data"][0]["price"]["id"]
                sub_status = sub_detail["status"]
                await update_user_subscription(db, customer_id, subscription_id, sub_status, price_id)
            except Exception:
                pass

    # Handle subscription updates or cancellations
    elif event_type in ["customer.subscription.created", "customer.subscription.updated", "customer.subscription.deleted"]:
        customer_id = data_object.get("customer")
        subscription_id = data_object.get("id")
        sub_status = data_object.get("status")
        price_id = data_object["items"]["data"][0]["price"]["id"]
        
        await update_user_subscription(db, customer_id, subscription_id, sub_status, price_id)

    return Response(status_code=status.HTTP_200_OK)
