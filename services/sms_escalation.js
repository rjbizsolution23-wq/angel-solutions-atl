/**
 * =====================================================================
 * ANGEL SOLUTIONS ATL - TWILIO SMS ESCALATION SERVICE
 * =====================================================================
 * Dispatches real-time, compliance-hardened SMS alerts to Jordynn Miller
 * for critical user activities (scam allegations, refund requests, etc.).
 * =====================================================================
 */

/**
 * Sends emergency notification SMS via Twilio API
 * @param {string} toPhoneNumber 
 * @param {string} bodyText 
 * @param {object} env 
 * @returns {Promise<object>} dispatch status results
 */
export async function sendEscalationSMS(toPhoneNumber, bodyText, env) {
  const accountSid = env.TWILIO_ACCOUNT_SID;
  const authToken = env.TWILIO_AUTH_TOKEN;
  const fromNumber = env.TWILIO_PHONE_NUMBER;

  // Sandbox fallback for local test suites
  if (!accountSid || !authToken || !fromNumber) {
    console.log(`[MOCK TWILIO SMS] Dispatched alert to ${toPhoneNumber}: "${bodyText}"`);
    return {
      success: true,
      messageSid: "mock_twilio_sid_998877",
      status: "mock_queued"
    };
  }

  const endpoint = `https://api.twilio.com/2010-04-01/Accounts/${accountSid}/Messages.json`;

  try {
    const formData = new URLSearchParams();
    formData.append("To", toPhoneNumber);
    formData.append("From", fromNumber);
    formData.append("Body", bodyText);

    const authHeader = "Basic " + btoa(`${accountSid}:${authToken}`);

    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Authorization": authHeader,
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: formData.toString()
    });

    const data = await response.json();

    if (response.ok && data.sid) {
      console.log(`Live Twilio SMS dispatched successfully! SID: ${data.sid}`);
      return {
        success: true,
        messageSid: data.sid,
        status: data.status
      };
    } else {
      throw new Error(data.message || "Unknown Twilio API dispatch failure");
    }

  } catch (error) {
    console.error("Twilio SMS dispatch failed:", error);
    return {
      success: false,
      error: error.message,
      status: "failed"
    };
  }
}
