"""
LangChain tools for Stripe product and pricing operations.
"""
from langchain.tools import tool
from core.stripe_client import get_stripe_client
from typing import Optional
import logging

logger = logging.getLogger(__name__)


@tool
def create_product_tool(name: str, description: Optional[str] = None) -> str:
    """
    Create a new product in Stripe.
    
    Args:
        name: Product name
        description: Optional product description
    
    Returns:
        Product details including ID
    """
    try:
        client = get_stripe_client()
        product = client.create_product(name=name, description=description)
        
        return f"Product created! ID: {product.id}, Name: {product.name}"
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        return f"Error creating product: {str(e)}"


@tool
def create_price_tool(
    product_id: str,
    amount: int,
    currency: str = "usd",
    recurring_interval: Optional[str] = None,
    recurring_interval_count: int = 1
) -> str:
    """
    Create a price for a product.
    
    Args:
        product_id: The product ID to create a price for
        amount: Price in cents (e.g., 9900 for $99.00)
        currency: Three-letter currency code (default: usd)
        recurring_interval: For subscriptions: "day", "week", "month", or "year"
        recurring_interval_count: Billing frequency (e.g., 2 for every 2 months)
    
    Returns:
        Price details including ID
    """
    try:
        client = get_stripe_client()
        
        recurring = None
        if recurring_interval:
            recurring = {
                "interval": recurring_interval,
                "interval_count": recurring_interval_count
            }
        
        price = client.create_price(
            product_id=product_id,
            unit_amount=amount,
            currency=currency,
            recurring=recurring
        )
        
        price_type = "recurring" if recurring else "one-time"
        return f"Price created! ID: {price.id}, Amount: ${amount/100:.2f}, Type: {price_type}"
    except Exception as e:
        logger.error(f"Error creating price: {e}")
        return f"Error creating price: {str(e)}"


@tool
def list_products_tool(limit: int = 10) -> str:
    """
    List all products.
    
    Args:
        limit: Maximum number of products to return (default: 10)
    
    Returns:
        List of products with IDs and names
    """
    try:
        client = get_stripe_client()
        products = client.list_products(limit=limit)
        
        if not products.data:
            return "No products found."
        
        result = "Products:\n"
        for product in products.data:
            result += f"- {product.name} (ID: {product.id})\n"
        
        return result
    except Exception as e:
        logger.error(f"Error listing products: {e}")
        return f"Error listing products: {str(e)}"


@tool
def create_coupon_tool(
    duration: str,
    percent_off: Optional[float] = None,
    amount_off: Optional[int] = None,
    currency: str = "usd",
    duration_in_months: Optional[int] = None
) -> str:
    """
    Create a coupon for discounts.
    
    Args:
        duration: "forever", "once", or "repeating"
        percent_off: Percentage discount (e.g., 25 for 25% off)
        amount_off: Fixed amount discount in cents (e.g., 1000 for $10 off)
        currency: Currency for amount_off (default: usd)
        duration_in_months: Required if duration is "repeating"
    
    Returns:
        Coupon details including ID
    """
    try:
        client = get_stripe_client()
        
        kwargs = {}
        if duration == "repeating" and duration_in_months:
            kwargs["duration_in_months"] = duration_in_months
        
        coupon = client.create_coupon(
            duration=duration,
            percent_off=percent_off,
            amount_off=amount_off,
            currency=currency if amount_off else None,
            **kwargs
        )
        
        discount_desc = f"{percent_off}% off" if percent_off else f"${amount_off/100:.2f} off"
        return f"Coupon created! ID: {coupon.id}, Discount: {discount_desc}, Duration: {duration}"
    except Exception as e:
        logger.error(f"Error creating coupon: {e}")
        return f"Error creating coupon: {str(e)}"
