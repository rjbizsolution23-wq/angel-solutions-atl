"""
Unified Stripe client wrapper with error handling, retries, and logging.
"""
import stripe
from typing import Any, Optional
from core.config import get_settings
import logging

logger = logging.getLogger(__name__)


class StripeClient:
    """Wrapper around Stripe SDK with enhanced error handling."""
    
    def __init__(self, mode: Optional[str] = None):
        """
        Initialize Stripe client.
        
        Args:
            mode: Override mode ("test" or "live"). If None, uses settings default.
        """
        settings = get_settings()
        self.mode = mode or settings.stripe_mode
        
        # Set the appropriate API key
        if self.mode == "live":
            stripe.api_key = settings.stripe_secret_key_live
        else:
            stripe.api_key = settings.stripe_secret_key_test
        
        logger.info(f"Stripe client initialized in {self.mode} mode")
    
    # ========== PAYMENT METHODS ==========
    
    def create_payment_intent(
        self,
        amount: int,
        currency: str = "usd",
        **kwargs
    ) -> stripe.PaymentIntent:
        """Create a payment intent."""
        try:
            return stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                **kwargs
            )
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create payment intent: {e}")
            raise
    
    def retrieve_payment_intent(self, payment_intent_id: str) -> stripe.PaymentIntent:
        """Retrieve a payment intent."""
        return stripe.PaymentIntent.retrieve(payment_intent_id)
    
    def create_refund(self, payment_intent_id: str, amount: Optional[int] = None) -> stripe.Refund:
        """Create a refund."""
        params = {"payment_intent": payment_intent_id}
        if amount:
            params["amount"] = amount
        return stripe.Refund.create(**params)
    
    # ========== CUSTOMERS ==========
    
    def create_customer(
        self,
        email: Optional[str] = None,
        name: Optional[str] = None,
        **kwargs
    ) -> stripe.Customer:
        """Create a customer."""
        params = {**kwargs}
        if email:
            params["email"] = email
        if name:
            params["name"] = name
        return stripe.Customer.create(**params)
    
    def retrieve_customer(self, customer_id: str) -> stripe.Customer:
        """Retrieve a customer."""
        return stripe.Customer.retrieve(customer_id)
    
    def list_customers(self, limit: int = 10, **kwargs) -> stripe.ListObject:
        """List customers."""
        return stripe.Customer.list(limit=limit, **kwargs)
    
    def update_customer(self, customer_id: str, **kwargs) -> stripe.Customer:
        """Update a customer."""
        return stripe.Customer.modify(customer_id, **kwargs)
    
    # ========== PRODUCTS & PRICES ==========
    
    def create_product(
        self,
        name: str,
        description: Optional[str] = None,
        **kwargs
    ) -> stripe.Product:
        """Create a product."""
        params = {"name": name, **kwargs}
        if description:
            params["description"] = description
        return stripe.Product.create(**params)
    
    def list_products(self, limit: int = 10, **kwargs) -> stripe.ListObject:
        """List products."""
        return stripe.Product.list(limit=limit, **kwargs)
    
    def create_price(
        self,
        product_id: str,
        unit_amount: int,
        currency: str = "usd",
        recurring: Optional[dict] = None,
        **kwargs
    ) -> stripe.Price:
        """Create a price."""
        params = {
            "product": product_id,
            "unit_amount": unit_amount,
            "currency": currency,
            **kwargs
        }
        if recurring:
            params["recurring"] = recurring
        return stripe.Price.create(**params)
    
    def list_prices(self, limit: int = 10, **kwargs) -> stripe.ListObject:
        """List prices."""
        return stripe.Price.list(limit=limit, **kwargs)
    
    # ========== SUBSCRIPTIONS ==========
    
    def create_subscription(
        self,
        customer_id: str,
        price_id: str,
        trial_period_days: Optional[int] = None,
        **kwargs
    ) -> stripe.Subscription:
        """Create a subscription."""
        params = {
            "customer": customer_id,
            "items": [{"price": price_id}],
            **kwargs
        }
        if trial_period_days:
            params["trial_period_days"] = trial_period_days
        return stripe.Subscription.create(**params)
    
    def retrieve_subscription(self, subscription_id: str) -> stripe.Subscription:
        """Retrieve a subscription."""
        return stripe.Subscription.retrieve(subscription_id)
    
    def cancel_subscription(self, subscription_id: str) -> stripe.Subscription:
        """Cancel a subscription."""
        return stripe.Subscription.delete(subscription_id)
    
    def list_subscriptions(self, limit: int = 10, **kwargs) -> stripe.ListObject:
        """List subscriptions."""
        return stripe.Subscription.list(limit=limit, **kwargs)
    
    # ========== CHECKOUT ==========
    
    def create_checkout_session(
        self,
        line_items: list,
        mode: str = "payment",
        success_url: Optional[str] = None,
        cancel_url: Optional[str] = None,
        **kwargs
    ) -> stripe.checkout.Session:
        """Create a checkout session."""
        settings = get_settings()
        params = {
            "line_items": line_items,
            "mode": mode,
            "success_url": success_url or f"{settings.frontend_url}/success",
            "cancel_url": cancel_url or f"{settings.frontend_url}/cancel",
            **kwargs
        }
        return stripe.checkout.Session.create(**params)
    
    # ========== PAYMENT LINKS ==========
    
    def create_payment_link(
        self,
        line_items: list,
        **kwargs
    ) -> stripe.PaymentLink:
        """Create a payment link."""
        return stripe.PaymentLink.create(
            line_items=line_items,
            **kwargs
        )
    
    # ========== INVOICES ==========
    
    def create_invoice(
        self,
        customer_id: str,
        **kwargs
    ) -> stripe.Invoice:
        """Create an invoice."""
        return stripe.Invoice.create(
            customer=customer_id,
            **kwargs
        )
    
    def finalize_invoice(self, invoice_id: str) -> stripe.Invoice:
        """Finalize an invoice."""
        return stripe.Invoice.finalize_invoice(invoice_id)
    
    def pay_invoice(self, invoice_id: str) -> stripe.Invoice:
        """Pay an invoice."""
        return stripe.Invoice.pay(invoice_id)
    
    # ========== CONNECT ==========
    
    def create_account(
        self,
        account_type: str = "express",
        email: Optional[str] = None,
        **kwargs
    ) -> stripe.Account:
        """Create a Connect account."""
        params = {"type": account_type, **kwargs}
        if email:
            params["email"] = email
        return stripe.Account.create(**params)
    
    def create_account_link(
        self,
        account_id: str,
        refresh_url: str,
        return_url: str,
        link_type: str = "account_onboarding"
    ) -> stripe.AccountLink:
        """Create an account link for onboarding."""
        return stripe.AccountLink.create(
            account=account_id,
            refresh_url=refresh_url,
            return_url=return_url,
            type=link_type
        )
    
    def create_transfer(
        self,
        amount: int,
        currency: str,
        destination: str,
        **kwargs
    ) -> stripe.Transfer:
        """Create a transfer to a connected account."""
        return stripe.Transfer.create(
            amount=amount,
            currency=currency,
            destination=destination,
            **kwargs
        )
    
    # ========== BALANCE & TRANSACTIONS ==========
    
    def retrieve_balance(self) -> stripe.Balance:
        """Retrieve account balance."""
        return stripe.Balance.retrieve()
    
    def list_balance_transactions(self, limit: int = 10, **kwargs) -> stripe.ListObject:
        """List balance transactions."""
        return stripe.BalanceTransaction.list(limit=limit, **kwargs)
    
    # ========== COUPONS & PROMOTIONS ==========
    
    def create_coupon(
        self,
        duration: str,
        percent_off: Optional[float] = None,
        amount_off: Optional[int] = None,
        currency: Optional[str] = None,
        **kwargs
    ) -> stripe.Coupon:
        """Create a coupon."""
        params = {"duration": duration, **kwargs}
        if percent_off:
            params["percent_off"] = percent_off
        if amount_off:
            params["amount_off"] = amount_off
            params["currency"] = currency or "usd"
        return stripe.Coupon.create(**params)
    
    def create_promotion_code(
        self,
        coupon_id: str,
        code: Optional[str] = None,
        **kwargs
    ) -> stripe.PromotionCode:
        """Create a promotion code."""
        params = {"coupon": coupon_id, **kwargs}
        if code:
            params["code"] = code
        return stripe.PromotionCode.create(**params)


# Singleton instance
_stripe_client: Optional[StripeClient] = None


def get_stripe_client(mode: Optional[str] = None) -> StripeClient:
    """Get or create Stripe client instance."""
    global _stripe_client
    if _stripe_client is None or (mode and _stripe_client.mode != mode):
        _stripe_client = StripeClient(mode=mode)
    return _stripe_client
