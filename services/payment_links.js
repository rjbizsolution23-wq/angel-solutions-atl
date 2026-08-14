/**
 * =====================================================================
 * ANGEL SOLUTIONS ATL - STRIPE CHECKOUT GATEWAY INTERFACE
 * =====================================================================
 * Dynamically constructs verified checkout links for our two target pricing
 * programs, supporting custom redirect success targets.
 * =====================================================================
 */

/**
 * Creates a Stripe Checkout Session URL
 * @param {string} planType "monthly" or "advanced"
 * @param {string} customerEmail 
 * @param {object} env 
 * @returns {Promise<object>} session details with checkout URL
 */
export async function createStripePaymentLink(planType, customerEmail, env) {
  const stripeSecretKey = env.STRIPE_SECRET_KEY;
  const successUrl = `${env.CLOUDFLARE_WORKER_URL || "https://angelsolutionsatl.com"}/payment/success?session_id={CHECKOUT_SESSION_ID}`;
  const cancelUrl = `${env.CLOUDFLARE_WORKER_URL || "https://angelsolutionsatl.com"}/payment/cancel`;

  // Sandbox fallback for local test execution
  if (!stripeSecretKey) {
    const mockSessionId = `cs_test_${crypto.randomUUID().slice(0, 10)}`;
    console.log(`[MOCK STRIPE] Created mock checkout link for ${planType} (${customerEmail})`);
    return {
      success: true,
      sessionId: mockSessionId,
      url: `https://checkout.stripe.com/c/pay/${mockSessionId}`
    };
  }

  // Determine pricing structures
  const priceId = planType === "monthly" 
    ? (env.STRIPE_PRICE_67_PLAN || "price_mock_monthly_67")
    : (env.STRIPE_PRICE_ADVANCED_795 || "price_mock_advanced_795");

  const mode = planType === "monthly" ? "subscription" : "payment";

  try {
    const endpoint = "https://api.stripe.com/v1/checkout/sessions";
    const bodyParams = new URLSearchParams();
    bodyParams.append("success_url", successUrl);
    bodyParams.append("cancel_url", cancelUrl);
    bodyParams.append("payment_method_types[0]", "card");
    bodyParams.append("line_items[0][price]", priceId);
    bodyParams.append("line_items[0][quantity]", "1");
    bodyParams.append("mode", mode);
    
    if (customerEmail) {
      bodyParams.append("customer_email", customerEmail);
    }

    const authHeader = "Basic " + btoa(`${stripeSecretKey}:`);

    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Authorization": authHeader,
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: bodyParams.toString()
    });

    const session = await response.json();

    if (response.ok && session.url) {
      console.log(`Stripe Checkout Session initialized successfully! ID: ${session.id}`);
      return {
        success: true,
        sessionId: session.id,
        url: session.url
      };
    } else {
      throw new Error(session.error ? session.error.message : "Failed to initialize Stripe payment session");
    }

  } catch (error) {
    console.error("Stripe Checkout Link generation failed:", error);
    return {
      success: false,
      error: error.message
    };
  }
}
