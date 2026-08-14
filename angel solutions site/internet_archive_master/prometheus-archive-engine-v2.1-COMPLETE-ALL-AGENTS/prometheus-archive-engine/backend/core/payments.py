"""
Prometheus Archive Engine - Stripe Billing Handler
Manages subscription product price mappings and SDK actions
"""
import os
from typing import Dict
import stripe

# Retrieve Stripe api key
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY", "")
stripe.api_key = STRIPE_API_KEY

# Pricing Price IDs mapped from stripe dashboard
# Using environmental variable placeholders, falling back to local simulation keys
PRICE_TIER_MAPPING: Dict[str, str] = {
    "pro": os.getenv("STRIPE_PRO_PRICE_ID", "price_PRO_mock_key_2026"),
    "enterprise": os.getenv("STRIPE_ENTERPRISE_PRICE_ID", "price_ENT_mock_key_2026")
}

def get_stripe_client():
    """Initializes and returns configured stripe client"""
    return stripe

def create_stripe_customer(email: str, user_id: str) -> str:
    """Register customer profile inside Stripe CRM database"""
    if not STRIPE_API_KEY:
        # Simulate local key generation if Stripe credentials are blank
        return f"cus_mock_{user_id[:8]}"
        
    customer = stripe.Customer.create(
        email=email,
        metadata={"user_id": user_id}
    )
    return customer.id

def generate_stripe_checkout_session(
    customer_id: str,
    price_id: str,
    success_url: str,
    cancel_url: str
) -> str:
    """Generate session payload for Stripe Checkout redirect"""
    if not STRIPE_API_KEY:
        # Simulate redirection local URL
        return f"https://checkout.stripe.com/pay/mock_session_cus_{customer_id}"

    session = stripe.checkout.Session.create(
        customer=customer_id,
        payment_method_types=["card"],
        line_items=[{
            "price": price_id,
            "quantity": 1
        }],
        mode="subscription",
        success_url=success_url,
        cancel_url=cancel_url,
        subscription_data={
            "metadata": {
                "price_id": price_id
            }
        }
    )
    return session.url

def generate_stripe_billing_portal_session(customer_id: str, return_url: str) -> str:
    """Create self-service customer portal session redirect URL"""
    if not STRIPE_API_KEY:
        return f"https://billing.stripe.com/p/mock_portal_cus_{customer_id}"

    session = stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url=return_url
    )
    return session.url
