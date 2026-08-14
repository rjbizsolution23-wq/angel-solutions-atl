# =====================================================================
# ANGEL SOLUTIONS ATL - CONVERSATION HANDOFF ENGINE
# =====================================================================
# Suspension and escalation coordinator. Automatically disables bot
# responses, logs the trigger state, and constructs notify payloads.
# =====================================================================

from datetime import datetime, timedelta, timezone

def initiate_human_handoff(lead_id: str, conversation_id: str, trigger_msg: str, reason: str, db_env) -> dict:
    """
    Deactivates bot replies, changes lead state, logs an escalation record,
    and returns SMS payload parameters.
    """
    now = datetime.now(timezone.utc).isoformat()
    # Pause bot replies for 24h by default unless manually cleared earlier
    paused_until = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()

    try:
        # 1. Update Lead State to ASSIGN and set paused_until
        update_lead_query = """
            UPDATE leads 
            SET lead_state = 'ASSIGN', paused_until = ?, updated_at = ? 
            WHERE id = ?
        """
        # Execute query against D1 (represented via env mock or actual driver)
        if hasattr(db_env, "DB"):
            db_env.DB.prepare(update_lead_query).bind(paused_until, now, lead_id).run()

        # 2. Set bot_active = 0 in Conversations
        update_conv_query = """
            UPDATE conversations 
            SET bot_active = 0, last_message_at = ? 
            WHERE id = ?
        """
        if hasattr(db_env, "DB"):
            db_env.DB.prepare(update_conv_query).bind(now, conversation_id).run()

        # 3. Create Escalation Log
        escalation_id = f"esc_{int(datetime.now(timezone.utc).timestamp())}"
        insert_esc_query = """
            INSERT INTO escalations (id, lead_id, trigger_message, sms_sent, sms_status, human_resolved, created_at)
            VALUES (?, ?, ?, 0, 'pending', 0, ?)
        """
        if hasattr(db_env, "DB"):
            db_env.DB.prepare(insert_esc_query).bind(escalation_id, lead_id, f"Reason: {reason}. Text: {trigger_msg}", now).run()

        # Build notification text payload for Twilio/GHL SMS
        sms_text = f"⚠️ Angel Solutions ATL Alert: Lead handoff triggered! Reason: {reason}. Immediate response needed at: https://angelsolutionsatl.com/dashboard"

        return {
            "success": True,
            "escalation_id": escalation_id,
            "bot_active": False,
            "paused_until": paused_until,
            "sms_payload": {
                "to": "+14703386689", # Jordynn Miller's Phone
                "body": sms_text
            }
        }

    except Exception as e:
        print(f"Error executing handoff database updates: {e}")
        return {
            "success": False,
            "error": str(e)
        }
