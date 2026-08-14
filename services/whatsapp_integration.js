/**
 * =====================================================================
 * ANGEL SOLUTIONS ATL - WHATSAPP BUSINESS ADAPTER
 * =====================================================================
 * Integrates WhatsApp Cloud API to enable premium text, template matching,
 * and automated interactive replies.
 * =====================================================================
 */

/**
 * Sends a pre-approved WhatsApp message template
 * @param {string} toPhoneNumber 
 * @param {string} templateName 
 * @param {Array<string>} parameters Template variable parameters
 * @param {object} env 
 * @returns {Promise<object>} response status results
 */
export async function sendWhatsAppTemplate(toPhoneNumber, templateName, parameters, env) {
  const apiKey = env.WHATSAPP_API_TOKEN;
  const phoneNumberId = env.WHATSAPP_PHONE_NUMBER_ID || "1234567890";

  if (!apiKey) {
    console.log(`[MOCK WHATSAPP] Outbound template '${templateName}' sent to ${toPhoneNumber}. Variables: [${parameters.join(", ")}]`);
    return {
      success: true,
      whatsappMessageId: `wamid.HBgL${crypto.randomUUID().slice(0, 15)}`,
      status: "mock_queued"
    };
  }

  const url = `https://graph.facebook.com/v19.0/${phoneNumberId}/messages`;

  const components = [{
    type: "body",
    parameters: parameters.map(p => ({ type: "text", text: p }))
  }];

  const payload = {
    messaging_product: "whatsapp",
    to: toPhoneNumber,
    type: "template",
    template: {
      name: templateName,
      language: { code: "en_US" },
      components: components
    }
  };

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (response.ok && data.messages && data.messages[0]) {
      console.log(`WhatsApp template dispatched successfully! Message ID: ${data.messages[0].id}`);
      return {
        success: true,
        whatsappMessageId: data.messages[0].id,
        status: "sent"
      };
    } else {
      throw new Error(data.error ? data.error.message : "WhatsApp Cloud API template delivery failure");
    }

  } catch (error) {
    console.error("WhatsApp delivery failed:", error);
    return {
      success: false,
      error: error.message
    };
  }
}
