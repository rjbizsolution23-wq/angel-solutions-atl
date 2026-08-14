"""
LangChain tools for Stripe customer and subscription operations.
"""
from langchain.tools import tool
from core.stripe_client import get_stripe_client
from typing import Optional
import logging

logger = logging.getLogger(__name__)


@tool
def create_customer_tool(
    email: Optional[str] = None,
    name: Optional[str] = None,
    description: Optional[str] = None
) -> str:
    """
    Create a new customer in Stripe.
    
    Args:
        email: Customer email address
        name: Customer name
        description: Optional description
    
    Returns:
        Customer details including ID
    """
    try:
        client = get_stripe_client()
        kwargs = {}
        if description:
            kwargs["description"] = description
        
        customer = client.create_customer(email=email, name=name, **kwargs)
        
        return f"Customer created! ID: {customer.id}, Email: {customer.email}, Name: {customer.name}"
    except Exception as e:
        logger.error(f"Error creating customer: {e}")
        return f"Error creating customer: {str(e)}"


@tool
def list_customers_tool(limit: int = 10) -> str:
    """
    List customers.
    
    Args:
        limit: Maximum number of customers to return (default: 10)
    
    Returns:
        List of customers
    """
    try:
        client = get_stripe_client()
        customers = client.list_customers(limit=limit)
        
        if not customers.data:
            return "No customers found."
        
        result = "Customers:\n"
        for customer in customers.data:
            result += f"- {customer.name or customer.email or 'No name'} (ID: {customer.id})\n"
        
        return result
    except Exception as e:
        logger.error(f"Error listing customers: {e}")
        return f"Error listing customers: {str(e)}"


@tool
def create_subscription_tool(
    customer_id: str,
    price_id: str,
    trial_period_days: Optional[int] = None
) -> str:
    """
    Create a subscription for a customer.
    
    Args:
        customer_id: The customer ID
        price_id: The price ID to subscribe to
        trial_period_days: Optional trial period in days
    
    Returns:
        Subscription details
    """
    try:
        client = get_stripe_client()
        subscription = client.create_subscription(
            customer_id=customer_id,
            price_id=price_id,
            trial_period_days=trial_period_days
        )
        
        trial_info = f", Trial: {trial_period_days} days" if trial_period_days else ""
        return f"Subscription created! ID: {subscription.id}, Status: {subscription.status}{trial_info}"
    except Exception as e:
        logger.error(f"Error creating subscription: {e}")
        return f"Error creating subscription: {str(e)}"


@tool
def cancel_subscription_tool(subscription_id: str) -> str:
    """
    Cancel a subscription.
    
    Args:
        subscription_id: The subscription ID to cancel
    
    Returns:
        Cancellation confirmation
    """
    try:
        client = get_stripe_client()
        subscription = client.cancel_subscription(subscription_id)
        
        return f"Subscription cancelled! ID: {subscription.id}, Status: {subscription.status}"
    except Exception as e:
        logger.error(f"Error cancelling subscription: {e}")
        return f"Error cancelling subscription: {str(e)}"


@tool
def list_subscriptions_tool(limit: int = 10) -> str:
    """
    List all subscriptions.
    
    Args:
        limit: Maximum number of subscriptions to return (default: 10)
    
    Returns:
        List of subscriptions
    """
    try:
        client = get_stripe_client()
        subscriptions = client.list_subscriptions(limit=limit)
        
        if not subscriptions.data:
            return "No subscriptions found."
        
        result = "Subscriptions:\n"
        for sub in subscriptions.data:
            result += f"- ID: {sub.id}, Status: {sub.status}, Customer: {sub.customer}\n"
        
        return result
    except Exception as e:
        logger.error(f"Error listing subscriptions: {e}")
        return f"Error listing subscriptions: {str(e)}"
