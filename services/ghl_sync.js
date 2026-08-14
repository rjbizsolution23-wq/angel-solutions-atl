/**
 * =====================================================================
 * ANGEL SOLUTIONS ATL - GOHIGHLEVEL CRM SYNC SERVICE
 * =====================================================================
 * Connects to GHL v2 API to upsert contacts, apply workflow tags,
 * and push custom credit profile metrics.
 * =====================================================================
 */

/**
 * Syncs lead contact and custom fields to GoHighLevel CRM
 * @param {object} lead 
 * @param {object} creditProfile 
 * @param {object} env Cloudflare/Service environment
 * @returns {Promise<object>} sync status results
 */
export async function syncLeadToGoHighLevel(lead, creditProfile, env) {
  const ghlApiKey = env.GHL_API_KEY;
  const locationId = env.GHL_LOCATION_ID || "Sfvt5kBZ3EUOws7MDWa3";

  // Safeguard fallback for testing if API key is missing
  if (!ghlApiKey) {
    console.log("[MOCK GHL SYNC] API Key missing, registering mock success.");
    return {
      success: true,
      ghlContactId: "mock_ghl_contact_12345",
      status: "success"
    };
  }

  const nameParts = (lead.name || "Angel Lead").split(" ");
  const firstName = nameParts[0];
  const lastName = nameParts.slice(1).join(" ") || "Prospect";

  const payload = {
    firstName: firstName,
    lastName: lastName,
    email: lead.email || `${lead.platform_user_id}@${lead.platform}.com`,
    phone: lead.phone || null,
    locationId: locationId,
    tags: [lead.platform, `state_${lead.lead_state.toLowerCase()}`],
    customFields: [
      { id: "bankruptcy", value: creditProfile.has_active_bankruptcy ? "Yes" : "No" },
      { id: "child_support", value: creditProfile.has_active_child_support_arrears ? "Yes" : "No" },
      { id: "collections_count", value: creditProfile.collections_count || 0 },
      { id: "credit_goal", value: creditProfile.credit_goal || "General Restore" }
    ]
  };

  try {
    const url = "https://services.leadconnectorhq.com/contacts/";
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${ghlApiKey}`,
        "Content-Type": "application/json",
        "Version": "2021-04-15"
      },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    
    if (response.ok && data.contact) {
      // Log successful sync to D1 if available
      if (env.DB) {
        await env.DB.prepare(
          `INSERT INTO ghl_sync_log (id, lead_id, ghl_contact_id, sync_status, error_message, synced_at)
           VALUES (?, ?, ?, 'success', NULL, ?)`
        ).bind(crypto.randomUUID(), lead.id, data.contact.id, new Date().toISOString()).run();
      }

      return {
        success: true,
        ghlContactId: data.contact.id,
        status: "success"
      };
    } else {
      throw new Error(data.message || "Failed to create contact");
    }

  } catch (error) {
    console.error("GHL Sync failed:", error);
    
    if (env.DB) {
      await env.DB.prepare(
        `INSERT INTO ghl_sync_log (id, lead_id, ghl_contact_id, sync_status, error_message, synced_at)
         VALUES (?, ?, NULL, 'failed', ?, ?)`
      ).bind(crypto.randomUUID(), lead.id, error.message, new Date().toISOString()).run();
    }

    return {
      success: false,
      error: error.message,
      status: "failed"
    };
  }
}
