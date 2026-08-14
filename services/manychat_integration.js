/**
 * =====================================================================
 * ANGEL SOLUTIONS ATL - MANYCHAT API INTEGRATION SERVICE
 * =====================================================================
 * Natively integrates with the ManyChat API to set Custom User Fields,
 * apply/remove tags, and trigger automation flows programmatically.
 * =====================================================================
 */

const MANYCHAT_TOKEN = "4762116:ebcba757acecde41bbacaae8a41a2387";

// Mappings compiled from live account audit
const CUSTOM_FIELDS = {
  "messages": 14509568,
  "human_message": 14509569
};

const TAGS = {
  "IG_BOT_INBOUND_FB": 85918996,
  "CUSTOMFU": 85917842,
  "ASSIGN": 85917683,
  "BOT_OFF": 85917684,
  "VAFOLLOWUP": 85917680,
  "COLLAB": 85917679,
  "BOOKED": 85917678,
  "DQ": 85917677,
  "LINK_SENT": 85917676,
  "IG_BOT_GENERAL_OFF": 85917675,
  "IG_BOT_GENERAL": 85917674,
  "IG_BOT_FOLLOW": 85917673,
  "IG_BOT_FLOW": 85917672,
  "IG_BOT_INBOUND": 85917671,
  "SETY": 85917670
};

/**
 * Sets a custom user field value on ManyChat
 * @param {string|number} subscriberId 
 * @param {string} fieldName 
 * @param {any} fieldValue 
 * @param {object} env 
 * @returns {Promise<object>} status
 */
export async function setManyChatCustomField(subscriberId, fieldName, fieldValue, env = {}) {
  const token = env.MANYCHAT_API_KEY || MANYCHAT_TOKEN;
  const fieldId = CUSTOM_FIELDS[fieldName];

  if (!fieldId) {
    console.error(`[ManyChat Error] Field '${fieldName}' is not defined in custom fields mapping.`);
    return { success: false, error: `Unknown field '${fieldName}'` };
  }

  const payload = {
    subscriber_id: Number(subscriberId),
    field_id: fieldId,
    field_value: fieldValue
  };

  try {
    const response = await fetch("https://api.manychat.com/fb/subscriber/setCustomField", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    if (response.ok && data.status === "success") {
      console.log(`[ManyChat Success] Custom field '${fieldName}' set to '${fieldValue}' for subscriber ${subscriberId}`);
      return { success: true, data };
    } else {
      throw new Error(data.message || "Failed to set custom field");
    }
  } catch (error) {
    console.error(`[ManyChat Error] setCustomField failed:`, error.message);
    return { success: false, error: error.message };
  }
}

/**
 * Adds a tag to a ManyChat subscriber
 * @param {string|number} subscriberId 
 * @param {string} tagName 
 * @param {object} env 
 * @returns {Promise<object>} status
 */
export async function addManyChatTag(subscriberId, tagName, env = {}) {
  const token = env.MANYCHAT_API_KEY || MANYCHAT_TOKEN;
  const tagId = TAGS[tagName];

  if (!tagId) {
    console.error(`[ManyChat Error] Tag '${tagName}' is not defined in system tags mapping.`);
    return { success: false, error: `Unknown tag '${tagName}'` };
  }

  const payload = {
    subscriber_id: Number(subscriberId),
    tag_id: tagId
  };

  try {
    const response = await fetch("https://api.manychat.com/fb/subscriber/addTag", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    if (response.ok && data.status === "success") {
      console.log(`[ManyChat Success] Added tag '${tagName}' for subscriber ${subscriberId}`);
      return { success: true, data };
    } else {
      throw new Error(data.message || "Failed to add tag");
    }
  } catch (error) {
    console.error(`[ManyChat Error] addTag failed:`, error.message);
    return { success: false, error: error.message };
  }
}

/**
 * Removes a tag from a ManyChat subscriber
 * @param {string|number} subscriberId 
 * @param {string} tagName 
 * @param {object} env 
 * @returns {Promise<object>} status
 */
export async function removeManyChatTag(subscriberId, tagName, env = {}) {
  const token = env.MANYCHAT_API_KEY || MANYCHAT_TOKEN;
  const tagId = TAGS[tagName];

  if (!tagId) {
    console.error(`[ManyChat Error] Tag '${tagName}' is not defined in system tags mapping.`);
    return { success: false, error: `Unknown tag '${tagName}'` };
  }

  const payload = {
    subscriber_id: Number(subscriberId),
    tag_id: tagId
  };

  try {
    const response = await fetch("https://api.manychat.com/fb/subscriber/removeTag", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    if (response.ok && data.status === "success") {
      console.log(`[ManyChat Success] Removed tag '${tagName}' for subscriber ${subscriberId}`);
      return { success: true, data };
    } else {
      throw new Error(data.message || "Failed to remove tag");
    }
  } catch (error) {
    console.error(`[ManyChat Error] removeTag failed:`, error.message);
    return { success: false, error: error.message };
  }
}

/**
 * Triggers a ManyChat flow for a subscriber
 * @param {string|number} subscriberId 
 * @param {string} flowNs 
 * @param {object} env 
 * @returns {Promise<object>} status
 */
export async function triggerManyChatFlow(subscriberId, flowNs, env = {}) {
  const token = env.MANYCHAT_API_KEY || MANYCHAT_TOKEN;

  const payload = {
    subscriber_id: Number(subscriberId),
    flow_ns: flowNs
  };

  try {
    const response = await fetch("https://api.manychat.com/fb/sending/sendFlow", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    if (response.ok && data.status === "success") {
      console.log(`[ManyChat Success] Triggered flow '${flowNs}' for subscriber ${subscriberId}`);
      return { success: true, data };
    } else {
      throw new Error(data.message || "Failed to trigger flow");
    }
  } catch (error) {
    console.error(`[ManyChat Error] triggerManyChatFlow failed:`, error.message);
    return { success: false, error: error.message };
  }
}
