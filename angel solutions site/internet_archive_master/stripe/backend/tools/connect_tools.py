"""
LangChain tools for Stripe Connect operations.
"""
from langchain.tools import tool
from core.stripe_client import get_stripe_client
from core.config import get_settings
from typing import Optional
import logging

logger = logging.getLogger(__name__)


@tool
def create_connect_account_tool(
    account_type: str = "express",
    email: Optional[str] = None,
    country: str = "US"
) -> str:
    """
    Create a Stripe Connect account for a seller/service provider.
    
    Args:
        account_type: "express" (recommended), "standard", or "custom"
        email: Account holder's email
        country: Two-letter country code (default: US)
    
    Returns:
        Account details including ID
    """
    try:
        client = get_stripe_client()
        kwargs = {"country": country}
        
        account = client.create_account(
            account_type=account_type,
            email=email,
            **kwargs
        )
        
        return f"Connect account created! ID: {account.id}, Type: {account_type}, Email: {email}"
    except Exception as e:
        logger.error(f"Error creating Connect account: {e}")
        return f"Error creating Connect account: {str(e)}"


@tool
def create_account_onboarding_link_tool(account_id: str) -> str:
    """
    Create an onboarding link for a Connect account.
    
    Args:
        account_id: The Connect account ID
    
    Returns:
        Onboarding URL
    """
    try:
        client = get_stripe_client()
        settings = get_settings()
        
        account_link = client.create_account_link(
            account_id=account_id,
            refresh_url=f"{settings.frontend_url}/connect/refresh",
            return_url=f"{settings.frontend_url}/connect/return",
            link_type="account_onboarding"
        )
        
        return f"Onboarding link created! URL: {account_link.url} (expires in 5 minutes)"
    except Exception as e:
        logger.error(f"Error creating onboarding link: {e}")
        return f"Error creating onboarding link: {str(e)}"


@tool
def create_transfer_tool(
    amount: int,
    destination_account_id: str,
    currency: str = "usd",
    description: Optional[str] = None
) -> str:
    """
    Transfer funds to a connected account.
    
    Args:
        amount: Amount in cents to transfer
        destination_account_id: The Connect account ID to transfer to
        currency: Three-letter currency code (default: usd)
        description: Optional transfer description
    
    Returns:
        Transfer confirmation
    """
    try:
        client = get_stripe_client()
        kwargs = {}
        if description:
            kwargs["description"] = description
        
        transfer = client.create_transfer(
            amount=amount,
            currency=currency,
            destination=destination_account_id,
            **kwargs
        )
        
        return f"Transfer created! ID: {transfer.id}, Amount: ${amount/100:.2f}, Destination: {destination_account_id}"
    except Exception as e:
        logger.error(f"Error creating transfer: {e}")
        return f"Error creating transfer: {str(e)}"
