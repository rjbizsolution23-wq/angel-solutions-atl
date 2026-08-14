"""
Webhook handling endpoints.
"""
from fastapi import APIRouter, Request, HTTPException, Header
from core.config import get_settings
from services.supabase_service import get_supabase_service
from services.provisioning_service import trigger_post_purchase_workflow
import stripe
import logging
from core.constants import PACKAGES

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/stripe")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None)
):
    """
    Handle Stripe webhook events.
    
    Verifies webhook signature and stores events in Supabase.
    """
    try:
        settings = get_settings()
        payload = await request.body()
        
        # Verify webhook signature
        try:
            event = stripe.Webhook.construct_event(
                payload,
                stripe_signature,
                settings.stripe_webhook_secret
            )
        except ValueError as e:
            logger.error(f"Invalid payload: {e}")
            raise HTTPException(status_code=400, detail="Invalid payload")
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid signature: {e}")
            raise HTTPException(status_code=400, detail="Invalid signature")
        
        # Store event in Supabase
        supabase = get_supabase_service()
        supabase.store_webhook_event(
            event_id=event.id,
            event_type=event.type,
            event_data=event.data.to_dict()
        )
        
        logger.info(f"Webhook event received: {event.type} (ID: {event.id})")
        
        # Handle specific event types
        if event.type == "payment_intent.succeeded":
            logger.info(f"Payment succeeded: {event.data.object.id}")
        elif event.type == "checkout.session.completed":
            session = event.data.object
            logger.info(f"Checkout session completed: {session.id}")
            
            # Verify amount and package
            metadata = session.metadata
            package_id = metadata.get("package_id")
            expected_amount = metadata.get("expected_amount")
            
            if package_id and package_id in PACKAGES:
                package = PACKAGES[package_id]
                if int(session.amount_total) == package["amount"]:
                    logger.info(f"PAYMENT VERIFIED: Package {package_id} bought for correct amount {session.amount_total}")
                    # Trigger post-purchase workflow
                    customer_email = session.customer_details.email if session.customer_details else "unknown@example.com"
                    await trigger_post_purchase_workflow(
                        session_id=session.id,
                        package_id=package_id,
                        customer_email=customer_email
                    )
                else:
                    logger.warning(f"PAYMENT MISMATCH: Expected {package['amount']}, got {session.amount_total}")
            else:
                 logger.warning(f"Unknown package in session: {package_id}")

        elif event.type == "customer.subscription.created":
            logger.info(f"Subscription created: {event.data.object.id}")
        elif event.type == "invoice.payment_failed":
            logger.info(f"Invoice payment failed: {event.data.object.id}")
        
        # Mark as processed
        supabase.mark_webhook_processed(event.id)
        
        return {"status": "success", "event_id": event.id}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/events")
async def get_webhook_events(limit: int = 50):
    """Get recent webhook events."""
    try:
        supabase = get_supabase_service()
        events = supabase.get_recent_webhook_events(limit=limit)
        return {"events": events}
    except Exception as e:
        logger.error(f"Error retrieving webhook events: {e}")
        raise HTTPException(status_code=500, detail=str(e))
