"""
LangChain tools for Stripe payment operations.
"""
from langchain.tools import tool
from core.stripe_client import get_stripe_client
from services.supabase_service import get_supabase_service
from typing import Optional
import logging

logger = logging.getLogger(__name__)


@tool
def create_payment_intent_tool(
    amount: int,
    currency: str = "usd",
    description: Optional[str] = None,
    customer_id: Optional[str] = None
) -> str:
    """
    Create a Stripe Payment Intent for processing a payment.
    
    Args:
        amount: Amount in cents (e.g., 5000 for $50.00)
        currency: Three-letter currency code (default: usd)
        description: Optional description of the payment
        customer_id: Optional customer ID to associate with payment
    
    Returns:
        JSON string with payment intent details including client_secret
    """
    try:
        client = get_stripe_client()
        params = {}
        if description:
            params["description"] = description
        if customer_id:
            params["customer"] = customer_id
        
        payment_intent = client.create_payment_intent(
            amount=amount,
            currency=currency,
            **params
        )
        
        return f"Payment Intent created successfully! ID: {payment_intent.id}, Amount: ${amount/100:.2f}, Status: {payment_intent.status}, Client Secret: {payment_intent.client_secret}"
    except Exception as e:
        logger.error(f"Error creating payment intent: {e}")
        return f"Error creating payment intent: {str(e)}"


@tool
def create_refund_tool(payment_intent_id: str, amount: Optional[int] = None) -> str:
    """
    Create a refund for a payment.
    
    Args:
        payment_intent_id: The ID of the payment intent to refund
        amount: Optional partial refund amount in cents. If not provided, full refund.
    
    Returns:
        Refund confirmation details
    """
    try:
        client = get_stripe_client()
        refund = client.create_refund(payment_intent_id, amount)
        
        refund_amount = amount or refund.amount
        return f"Refund created successfully! ID: {refund.id}, Amount: ${refund_amount/100:.2f}, Status: {refund.status}"
    except Exception as e:
        logger.error(f"Error creating refund: {e}")
        return f"Error creating refund: {str(e)}"


@tool
def create_checkout_session_tool(
    price_id: str,
    quantity: int = 1,
    mode: str = "payment",
    success_url: Optional[str] = None,
    cancel_url: Optional[str] = None
) -> str:
    """
    Create a Stripe Checkout Session for a hosted payment page.
    
    Args:
        price_id: The ID of the price to purchase
        quantity: Quantity of items (default: 1)
        mode: "payment" for one-time, "subscription" for recurring
        success_url: URL to redirect after successful payment
        cancel_url: URL to redirect if payment is cancelled
    
    Returns:
        Checkout session URL
    """
    try:
        client = get_stripe_client()
        line_items = [{"price": price_id, "quantity": quantity}]
        
        session = client.create_checkout_session(
            line_items=line_items,
            mode=mode,
            success_url=success_url,
            cancel_url=cancel_url
        )
        
        return f"Checkout session created! URL: {session.url}"
    except Exception as e:
        logger.error(f"Error creating checkout session: {e}")
        return f"Error creating checkout session: {str(e)}"


@tool
def create_payment_link_tool(price_id: str, quantity: int = 1) -> str:
    """
    Create a shareable Payment Link.
    
    Args:
        price_id: The ID of the price to sell
        quantity: Default quantity (default: 1)
    
    Returns:
        Payment link URL
    """
    try:
        client = get_stripe_client()
        line_items = [{"price": price_id, "quantity": quantity}]
        
        payment_link = client.create_payment_link(line_items=line_items)
        
        return f"Payment link created! URL: {payment_link.url}"
    except Exception as e:
        logger.error(f"Error creating payment link: {e}")
        return f"Error creating payment link: {str(e)}"
