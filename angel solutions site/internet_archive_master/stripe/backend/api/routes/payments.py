"""
Payment handling endpoints.
"""
from fastapi import APIRouter, HTTPException, Body
from core.stripe_client import get_stripe_client
from core.config import get_settings
from typing import Optional
import logging

from core.constants import PACKAGES

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/create-checkout-session")
async def create_checkout_session(
    package_id: str = Body(..., embed=True),
    success_url: str = Body(..., embed=True),
    cancel_url: str = Body(..., embed=True),
    customer_email: Optional[str] = Body(None, embed=True),
):
    """
    Create a Stripe Checkout Session for a package.
    """
    try:
        if package_id not in PACKAGES:
            raise HTTPException(status_code=400, detail="Invalid package ID")
            
        package = PACKAGES[package_id]
        client = get_stripe_client()
        settings = get_settings()
        
        session = client.create_checkout_session(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": package["name"],
                        "metadata": {"package_id": package_id}
                    },
                    "unit_amount": package["amount"],
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
            customer_email=customer_email,
            metadata={
                "package_id": package_id,
                "expected_amount": package["amount"]
            }
        )
        
        return {"url": session.url, "id": session.id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating checkout session: {e}")
        raise HTTPException(status_code=500, detail=str(e))
