/**
 * Prometheus Cloudflare-Native Advanced Stripe billing wrapper
 * Direct edge fetches to the Stripe REST APIs for performance.
 */

export interface StripeProductConfig {
  name: string;
  description?: string;
  priceAmount: number; // in cents
  currency?: string;
  productType: "digital" | "collection" | "course" | "custom" | "subscription";
  interval?: "day" | "week" | "month" | "year"; // for subscription recurring
}

export class CloudflareStripeAdvanced {
  private stripeApiKey: string;

  constructor(stripeApiKey: string) {
    this.stripeApiKey = stripeApiKey;
  }

  /**
   * Universal header builder for Stripe REST API
   */
  private getHeaders(): HeadersInit {
    return {
      Authorization: `Bearer ${this.stripeApiKey}`,
      "Content-Type": "application/x-www-form-urlencoded"
    };
  }

  /**
   * Create a new product and price tier inside Stripe
   */
  async createProduct(config: StripeProductConfig): Promise<any> {
    const currency = config.currency || "usd";

    // 1. Create Product
    const productParams = new URLSearchParams();
    productParams.append("name", config.name);
    if (config.description) productParams.append("description", config.description);
    productParams.append("metadata[product_type]", config.productType);

    const productRes = await fetch("https://api.stripe.com/v1/products", {
      method: "POST",
      headers: this.getHeaders(),
      body: productParams
    });
    const productData: any = await productRes.json();
    if (productData.error) throw new Error(productData.error.message);

    // 2. Create Price for Product
    const priceParams = new URLSearchParams();
    priceParams.append("product", productData.id);
    priceParams.append("unit_amount", config.priceAmount.toString());
    priceParams.append("currency", currency);

    if (config.productType === "subscription" && config.interval) {
      priceParams.append("recurring[interval]", config.interval);
    }

    const priceRes = await fetch("https://api.stripe.com/v1/prices", {
      method: "POST",
      headers: this.getHeaders(),
      body: priceParams
    });
    const priceData: any = await priceRes.json();
    if (priceData.error) throw new Error(priceData.error.message);

    return {
      productId: productData.id,
      priceId: priceData.id,
      name: productData.name,
      priceAmount: config.priceAmount
    };
  }

  /**
   * Initiate dynamic Stripe Embedded Checkout sessions (inline frames)
   */
  async createEmbeddedCheckoutSession(priceId: string, returnUrl: string, collectTax: boolean = true): Promise<any> {
    const params = new URLSearchParams();
    params.append("ui_mode", "embedded");
    params.append("return_url", returnUrl || "https://prometheus.rickjeffersonsolutions.com/checkout/return?session_id={CHECKOUT_SESSION_ID}");
    params.append("line_items[0][price]", priceId);
    params.append("line_items[0][quantity]", "1");
    
    // Enable automated tax collection
    if (collectTax) {
      params.append("automatic_tax[enabled]", "true");
    }

    const res = await fetch("https://api.stripe.com/v1/checkout/sessions", {
      method: "POST",
      headers: this.getHeaders(),
      body: params
    });
    
    const data: any = await res.json();
    if (data.error) throw new Error(data.error.message);

    return {
      sessionId: data.id,
      clientSecret: data.client_secret
    };
  }

  /**
   * Generate direct Payment Links for email campaigns, chats, and QR codes
   */
  async createPaymentLink(priceId: string, redirectUrl: string, collectTax: boolean = true): Promise<any> {
    const params = new URLSearchParams();
    params.append("line_items[0][price]", priceId);
    params.append("line_items[0][quantity]", "1");
    if (redirectUrl) {
      params.append("after_completion[type]", "redirect");
      params.append("after_completion[redirect][url]", redirectUrl);
    }
    if (collectTax) {
      params.append("automatic_tax[enabled]", "true");
    }

    const res = await fetch("https://api.stripe.com/v1/payment_links", {
      method: "POST",
      headers: this.getHeaders(),
      body: params
    });

    const data: any = await res.json();
    if (data.error) throw new Error(data.error.message);

    return {
      paymentLinkId: data.id,
      url: data.url
    };
  }

  /**
   * Initiate customer self-service billing Portal sessions
   */
  async createCustomerPortalSession(customerId: string, returnUrl: string): Promise<any> {
    const params = new URLSearchParams();
    params.append("customer", customerId);
    params.append("return_url", returnUrl || "https://prometheus.rickjeffersonsolutions.com/dashboard");

    const res = await fetch("https://api.stripe.com/v1/billing_portal/sessions", {
      method: "POST",
      headers: this.getHeaders(),
      body: params
    });

    const data: any = await res.json();
    if (data.error) throw new Error(data.error.message);

    return {
      portalSessionId: data.id,
      url: data.url
    };
  }
}
