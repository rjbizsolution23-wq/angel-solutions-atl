"""
ADVANCED STRIPE INTEGRATION - All 2026 Features
Embedded Checkout, Payment Links, Customer Portal, Tax, Radar, Billing

Author: RJ PROMETHEUS APEX
Date: 2026-07-11
Version: 3.1.0
"""

import stripe
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from loguru import logger

# Initialize Stripe
stripe.api_key = "sk_test_YOUR_STRIPE_SECRET_KEY"

# ═══════════════════════════════════════════════════════════════════
# DATA MODELS
# ═══════════════════════════════════════════════════════════════════

class ProductType(Enum):
    DIGITAL_DOWNLOAD = "digital_download"
    COLLECTION = "collection"
    COURSE = "course"
    CUSTOM_BUILD = "custom_build"
    SUBSCRIPTION = "subscription"


class PriceType(Enum):
    ONE_TIME = "one_time"
    RECURRING = "recurring"


class SubscriptionInterval(Enum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


@dataclass
class ProductConfig:
    name: str
    description: str
    price_amount: int  # in cents
    currency: str = "usd"
    product_type: ProductType = ProductType.DIGITAL_DOWNLOAD
    price_type: PriceType = PriceType.ONE_TIME
    interval: Optional[SubscriptionInterval] = None
    images: List[str] = None
    metadata: Dict[str, Any] = None
    tax_code: Optional[str] = None  # For automatic tax calculation
    features: List[str] = None


# ═══════════════════════════════════════════════════════════════════
# ADVANCED STRIPE CLIENT
# ═══════════════════════════════════════════════════════════════════

class AdvancedStripeClient:
    """
    Complete Stripe integration with ALL 2026 features:
    - Embedded Checkout (inline payment form)
    - Payment Links (shareable checkout URLs)
    - Customer Portal (self-service billing)
    - Stripe Tax (automatic tax calculation)
    - Stripe Radar (fraud detection)
    - Billing Portal
    - Invoice management
    - Usage-based billing
    - Metered subscriptions
    """
    
    def __init__(self, api_key: str, webhook_secret: str):
        stripe.api_key = api_key
        self.webhook_secret = webhook_secret
        logger.info("💳 AdvancedStripeClient initialized")
    
    # ═══════════════════════════════════════════════════════════════
    # PRODUCT MANAGEMENT
    # ═══════════════════════════════════════════════════════════════
    
    async def create_product(self, config: ProductConfig) -> Dict[str, Any]:
        """
        Create product with price in one call.
        Returns product_id and price_id.
        """
        try:
            # Create product
            product = stripe.Product.create(
                name=config.name,
                description=config.description,
                images=config.images or [],
                metadata={
                    "type": config.product_type.value,
                    **(config.metadata or {})
                },
                tax_code=config.tax_code,  # For automatic tax
                features=[{"name": f} for f in (config.features or [])]
            )
            
            # Create price
            price_params = {
                "product": product.id,
                "unit_amount": config.price_amount,
                "currency": config.currency,
                "metadata": config.metadata or {}
            }
            
            if config.price_type == PriceType.RECURRING:
                price_params["recurring"] = {
                    "interval": config.interval.value if config.interval else "month"
                }
            
            price = stripe.Price.create(**price_params)
            
            logger.info(f"✅ Product created: {product.id} with price {price.id}")
            
            return {
                "product_id": product.id,
                "price_id": price.id,
                "product": product,
                "price": price
            }
        except stripe.error.StripeError as e:
            logger.error(f"❌ Stripe product creation failed: {e}")
            raise
    
    async def update_product(
        self,
        product_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        images: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> stripe.Product:
        """Update product."""
        update_params = {}
        if name:
            update_params["name"] = name
        if description:
            update_params["description"] = description
        if images:
            update_params["images"] = images
        if metadata:
            update_params["metadata"] = metadata
        
        return stripe.Product.modify(product_id, **update_params)
    
    async def archive_product(self, product_id: str) -> stripe.Product:
        """Archive (soft delete) product."""
        return stripe.Product.modify(product_id, active=False)
    
    # ═══════════════════════════════════════════════════════════════
    # EMBEDDED CHECKOUT (NEW 2026 FEATURE)
    # ═══════════════════════════════════════════════════════════════
    
    async def create_embedded_checkout_session(
        self,
        customer_id: str,
        price_id: str,
        quantity: int = 1,
        success_url: str = None,
        cancel_url: str = None,
        metadata: Dict[str, Any] = None,
        allow_promotion_codes: bool = True,
        collect_tax: bool = True
    ) -> Dict[str, Any]:
        """
        Create Embedded Checkout Session (renders inline in your app).
        
        Frontend integration:
        ```html
        <div id="checkout"></div>
        <script src="https://js.stripe.com/v3/"></script>
        <script>
          const stripe = Stripe('pk_test_...');
          const checkout = await stripe.initEmbeddedCheckout({
            clientSecret: '{{client_secret}}'
          });
          checkout.mount('#checkout');
        </script>
        ```
        """
        try:
            session = stripe.checkout.Session.create(
                ui_mode='embedded',  # 🔥 NEW: Embedded mode
                customer=customer_id,
                line_items=[{
                    "price": price_id,
                    "quantity": quantity
                }],
                mode="payment",
                return_url=success_url,  # For embedded, use return_url instead of success_url
                automatic_tax={"enabled": collect_tax},  # 🔥 Automatic tax calculation
                allow_promotion_codes=allow_promotion_codes,
                metadata=metadata or {},
                payment_intent_data={
                    "metadata": metadata or {}
                }
            )
            
            return {
                "session_id": session.id,
                "client_secret": session.client_secret,  # 🔥 Use this in frontend
                "url": session.url
            }
        except stripe.error.StripeError as e:
            logger.error(f"❌ Embedded checkout creation failed: {e}")
            raise
    
    # ═══════════════════════════════════════════════════════════════
    # PAYMENT LINKS (2026 FEATURE)
    # ═══════════════════════════════════════════════════════════════
    
    async def create_payment_link(
        self,
        price_id: str,
        quantity: int = 1,
        metadata: Dict[str, Any] = None,
        after_completion_redirect_url: Optional[str] = None,
        allow_promotion_codes: bool = True,
        collect_tax: bool = True,
        collect_phone: bool = False,
        collect_shipping: bool = False
    ) -> stripe.PaymentLink:
        """
        Create Payment Link - shareable URL for checkout.
        
        Example:
        https://buy.stripe.com/test_xyz123abc
        
        Perfect for:
        - Email marketing
        - Social media posts
        - QR codes
        - No-code selling
        """
        try:
            payment_link = stripe.PaymentLink.create(
                line_items=[{
                    "price": price_id,
                    "quantity": quantity
                }],
                metadata=metadata or {},
                after_completion={
                    "type": "redirect",
                    "redirect": {"url": after_completion_redirect_url}
                } if after_completion_redirect_url else {"type": "hosted_confirmation"},
                allow_promotion_codes=allow_promotion_codes,
                automatic_tax={"enabled": collect_tax},
                phone_number_collection={"enabled": collect_phone},
                shipping_address_collection={
                    "allowed_countries": ["US", "CA", "GB", "AU"]
                } if collect_shipping else None
            )
            
            logger.info(f"✅ Payment Link created: {payment_link.url}")
            
            return payment_link
        except stripe.error.StripeError as e:
            logger.error(f"❌ Payment Link creation failed: {e}")
            raise
    
    async def list_payment_links(self, limit: int = 10) -> List[stripe.PaymentLink]:
        """List all payment links."""
        return stripe.PaymentLink.list(limit=limit).data
    
    async def deactivate_payment_link(self, payment_link_id: str) -> stripe.PaymentLink:
        """Deactivate payment link."""
        return stripe.PaymentLink.modify(payment_link_id, active=False)
    
    # ═══════════════════════════════════════════════════════════════
    # CUSTOMER PORTAL (2026 FEATURE)
    # ═══════════════════════════════════════════════════════════════
    
    async def create_customer_portal_session(
        self,
        customer_id: str,
        return_url: str
    ) -> Dict[str, Any]:
        """
        Create Customer Portal session - self-service billing.
        
        Customers can:
        - Update payment methods
        - View invoices
        - Manage subscriptions
        - Update billing details
        - Download receipts
        """
        try:
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=return_url
            )
            
            return {
                "url": session.url,  # Redirect customer here
                "session_id": session.id
            }
        except stripe.error.StripeError as e:
            logger.error(f"❌ Customer Portal creation failed: {e}")
            raise
    
    async def configure_customer_portal(
        self,
        business_name: str,
        support_email: str,
        terms_of_service_url: str,
        privacy_policy_url: str
    ) -> stripe.billing_portal.Configuration:
        """
        Configure Customer Portal settings.
        """
        return stripe.billing_portal.Configuration.create(
            business_profile={
                "headline": business_name,
            },
            features={
                "payment_method_update": {"enabled": True},
                "invoice_history": {"enabled": True},
                "customer_update": {
                    "enabled": True,
                    "allowed_updates": ["email", "address", "phone", "tax_id"]
                },
                "subscription_cancel": {"enabled": True},
                "subscription_pause": {"enabled": True},
                "subscription_update": {
                    "enabled": True,
                    "default_allowed_updates": ["price", "quantity"],
                    "proration_behavior": "create_prorations"
                }
            },
            default_return_url=support_email,
            metadata={
                "tos_url": terms_of_service_url,
                "privacy_url": privacy_policy_url
            }
        )
    
    # ═══════════════════════════════════════════════════════════════
    # STRIPE TAX (2026 FEATURE)
    # ═══════════════════════════════════════════════════════════════
    
    async def calculate_tax(
        self,
        amount: int,
        currency: str,
        customer_address: Dict[str, str],
        line_items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculate tax automatically using Stripe Tax.
        
        Stripe Tax handles:
        - US sales tax (all states)
        - EU VAT
        - Canadian GST/PST
        - UK VAT
        - Australian GST
        - And more...
        """
        try:
            calculation = stripe.tax.Calculation.create(
                currency=currency,
                line_items=line_items,
                customer_details={
                    "address": customer_address,
                    "address_source": "shipping"
                },
                expand=["line_items.data.tax_breakdown"]
            )
            
            return {
                "amount_total": calculation.amount_total,
                "tax_amount_exclusive": calculation.tax_amount_exclusive,
                "tax_amount_inclusive": calculation.tax_amount_inclusive,
                "tax_breakdown": calculation.line_items.data[0].tax_breakdown if calculation.line_items.data else []
            }
        except stripe.error.StripeError as e:
            logger.error(f"❌ Tax calculation failed: {e}")
            raise
    
    # ═══════════════════════════════════════════════════════════════
    # STRIPE RADAR (FRAUD DETECTION)
    # ═══════════════════════════════════════════════════════════════
    
    async def create_radar_rule(
        self,
        name: str,
        condition: str,
        action: str = "block"
    ) -> stripe.radar.Rule:
        """
        Create Radar rule for fraud prevention.
        
        Examples:
        - Block if card is from high-risk country
        - Require 3D Secure if amount > $100
        - Block if IP country != card country
        """
        return stripe.radar.Rule.create(
            name=name,
            expression=condition,
            action=action
        )
    
    async def review_payment(self, payment_intent_id: str) -> Dict[str, Any]:
        """
        Get Radar assessment for a payment.
        """
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        return {
            "risk_level": payment_intent.charges.data[0].outcome.risk_level if payment_intent.charges.data else None,
            "risk_score": payment_intent.charges.data[0].outcome.risk_score if payment_intent.charges.data else None,
            "seller_message": payment_intent.charges.data[0].outcome.seller_message if payment_intent.charges.data else None,
            "radar_rules": payment_intent.charges.data[0].outcome.rule if payment_intent.charges.data else None
        }
    
    # ═══════════════════════════════════════════════════════════════
    # SUBSCRIPTIONS & BILLING
    # ═══════════════════════════════════════════════════════════════
    
    async def create_subscription(
        self,
        customer_id: str,
        price_id: str,
        trial_period_days: Optional[int] = None,
        metadata: Dict[str, Any] = None,
        proration_behavior: str = "create_prorations"
    ) -> stripe.Subscription:
        """Create subscription."""
        return stripe.Subscription.create(
            customer=customer_id,
            items=[{"price": price_id}],
            trial_period_days=trial_period_days,
            metadata=metadata or {},
            proration_behavior=proration_behavior,
            payment_behavior="default_incomplete",
            payment_settings={
                "save_default_payment_method": "on_subscription"
            }
        )
    
    async def create_metered_subscription(
        self,
        customer_id: str,
        price_id: str,
        metadata: Dict[str, Any] = None
    ) -> stripe.Subscription:
        """
        Create usage-based subscription (pay-per-use).
        
        Example: API calls, storage GB, bandwidth
        """
        return stripe.Subscription.create(
            customer=customer_id,
            items=[{
                "price": price_id,
                # Don't set quantity - it's metered
            }],
            metadata=metadata or {}
        )
    
    async def report_usage(
        self,
        subscription_item_id: str,
        quantity: int,
        timestamp: Optional[int] = None,
        action: str = "increment"
    ) -> stripe.UsageRecord:
        """
        Report usage for metered billing.
        
        Example:
        - User downloads 50 files → report 50
        - User uses 10 GB storage → report 10
        """
        return stripe.SubscriptionItem.create_usage_record(
            subscription_item_id,
            quantity=quantity,
            timestamp=timestamp or int(datetime.utcnow().timestamp()),
            action=action  # increment or set
        )
    
    # ═══════════════════════════════════════════════════════════════
    # INVOICES
    # ═══════════════════════════════════════════════════════════════
    
    async def create_invoice(
        self,
        customer_id: str,
        items: List[Dict[str, Any]],
        auto_advance: bool = True
    ) -> stripe.Invoice:
        """
        Create and send invoice.
        """
        # Add invoice items
        for item in items:
            stripe.InvoiceItem.create(
                customer=customer_id,
                amount=item["amount"],
                currency=item.get("currency", "usd"),
                description=item.get("description", "")
            )
        
        # Create invoice
        invoice = stripe.Invoice.create(
            customer=customer_id,
            auto_advance=auto_advance,  # Auto-finalize and send
            collection_method="send_invoice",
            days_until_due=30
        )
        
        if auto_advance:
            invoice = stripe.Invoice.finalize_invoice(invoice.id)
        
        return invoice
    
    # ═══════════════════════════════════════════════════════════════
    # WEBHOOKS
    # ═══════════════════════════════════════════════════════════════
    
    async def verify_webhook(
        self,
        payload: bytes,
        sig_header: str
    ) -> stripe.Event:
        """Verify webhook signature."""
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, self.webhook_secret
            )
            return event
        except ValueError:
            raise Exception("Invalid payload")
        except stripe.error.SignatureVerificationError:
            raise Exception("Invalid signature")
    
    async def handle_webhook_event(self, event: stripe.Event) -> Dict[str, Any]:
        """
        Handle webhook events.
        
        Common events:
        - checkout.session.completed
        - payment_intent.succeeded
        - payment_intent.payment_failed
        - customer.subscription.created
        - customer.subscription.updated
        - customer.subscription.deleted
        - invoice.paid
        - invoice.payment_failed
        """
        event_type = event.type
        data = event.data.object
        
        handlers = {
            "checkout.session.completed": self._handle_checkout_completed,
            "payment_intent.succeeded": self._handle_payment_succeeded,
            "payment_intent.payment_failed": self._handle_payment_failed,
            "customer.subscription.created": self._handle_subscription_created,
            "customer.subscription.updated": self._handle_subscription_updated,
            "customer.subscription.deleted": self._handle_subscription_deleted,
            "invoice.paid": self._handle_invoice_paid,
            "invoice.payment_failed": self._handle_invoice_failed
        }
        
        handler = handlers.get(event_type)
        if handler:
            return await handler(data)
        else:
            logger.warning(f"Unhandled event type: {event_type}")
            return {"status": "ignored"}
    
    # Event handlers (implement in your application)
    async def _handle_checkout_completed(self, session): pass
    async def _handle_payment_succeeded(self, payment_intent): pass
    async def _handle_payment_failed(self, payment_intent): pass
    async def _handle_subscription_created(self, subscription): pass
    async def _handle_subscription_updated(self, subscription): pass
    async def _handle_subscription_deleted(self, subscription): pass
    async def _handle_invoice_paid(self, invoice): pass
    async def _handle_invoice_failed(self, invoice): pass


# ═══════════════════════════════════════════════════════════════════
# PRODUCT BUILDER HELPER
# ═══════════════════════════════════════════════════════════════════

class ProductBuilder:
    """
    Helper class for building products with UI.
    """
    
    def __init__(self, stripe_client: AdvancedStripeClient):
        self.stripe = stripe_client
    
    async def build_digital_product(
        self,
        name: str,
        description: str,
        price: float,
        files: List[str],
        thumbnail_url: str,
        features: List[str]
    ) -> Dict[str, Any]:
        """
        Build complete digital product with Stripe integration.
        """
        config = ProductConfig(
            name=name,
            description=description,
            price_amount=int(price * 100),  # Convert to cents
            product_type=ProductType.DIGITAL_DOWNLOAD,
            images=[thumbnail_url],
            features=features,
            metadata={
                "files": ",".join(files),
                "type": "digital"
            }
        )
        
        result = await self.stripe.create_product(config)
        
        # Create payment link
        payment_link = await self.stripe.create_payment_link(
            price_id=result["price_id"],
            metadata={"product_name": name}
        )
        
        return {
            **result,
            "payment_link": payment_link.url,
            "payment_link_id": payment_link.id
        }
