"""
Prometheus Archive Engine - Stripe Checkout API Router
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.db import get_db
from ...core.auth import get_current_user
from ...core.payments import (
    PRICE_TIER_MAPPING,
    generate_stripe_checkout_session,
    generate_stripe_billing_portal_session,
    create_stripe_customer
)
from ...models.database import User

router = APIRouter()

class CheckoutRequest(BaseModel):
    tier: str # pro, enterprise
    success_url: str
    cancel_url: str

class PortalRequest(BaseModel):
    return_url: str

@router.post("/create-session")
async def create_checkout_session_endpoint(
    payload: CheckoutRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Generates redirect Stripe Checkout URL for subscription purchases"""
    tier_lower = payload.payload_tier if hasattr(payload, "payload_tier") else payload.tier.lower()
    
    if tier_lower not in PRICE_TIER_MAPPING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid pricing tier target: {payload.tier}"
        )

    price_id = PRICE_TIER_MAPPING[tier_lower]

    # Dynamically generate customer ID if missing from user record
    if not current_user.stripe_customer_id:
        customer_id = create_stripe_customer(current_user.email, current_user.id)
        current_user.stripe_customer_id = customer_id
        db.add(current_user)
        await db.commit()
    else:
        customer_id = current_user.stripe_customer_id

    try:
        redirect_url = generate_stripe_checkout_session(
            customer_id=customer_id,
            price_id=price_id,
            success_url=payload.success_url,
            cancel_url=payload.cancel_url
        )
        return {"checkout_url": redirect_url}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate stripe checkout session: {str(exc)}"
        ) from exc

@router.post("/portal")
async def create_billing_portal_endpoint(
    payload: PortalRequest,
    current_user: User = Depends(get_current_user)
):
    """Retrieve URL for customer self-service billing management portal"""
    if not current_user.stripe_customer_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not have an active Stripe customer identity. Purchase subscription first."
        )

    try:
        portal_url = generate_stripe_billing_portal_session(
            customer_id=current_user.stripe_customer_id,
            return_url=payload.return_url
        )
        return {"portal_url": portal_url}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate customer billing portal: {str(exc)}"
        ) from exc
