# =====================================================================
# ANGEL SOLUTIONS ATL - STRATEGY CALL APPOINTMENT REMINDERS
# =====================================================================
# Automatically polls booking states and schedules multi-touch reminders
# at the 24-hour and 1-hour marks to maximize strategy call show rates.
# =====================================================================

import os
from datetime import datetime, timedelta

def process_upcoming_appointment_reminders(db_env):
    """
    Selects leads scheduled for strategy calls, calculates remaining time,
    and dispatches high-touch reminder messages.
    """
    # SQLite/D1 representation: Find leads booked with GHL appointment times
    # Target: appointment_time is set and reminder state needs update
    query = """
        SELECT l.*, c.id as conversation_id
        FROM leads l
        JOIN conversations c ON l.id = c.lead_id
        WHERE l.lead_state = 'BOOKED'
          AND l.paused_until IS NULL
    """

    if not hasattr(db_env, "DB"):
        print("[MOCK REMINDERS] Database not initialized. Simulating poller execution.")
        return

    appointments = db_env.DB.prepare(query).all()
    print(f"Polling appointment calendar. Found {len(appointments.results)} booked consults.")

    for lead in appointments.results:
        # Mock appointment time if column missing (usually saved in GHL and synced)
        # We will parse custom fields or appointment_time columns
        app_time_str = lead.get("appointment_time") or (datetime.utcnow() + timedelta(hours=12)).isoformat()
        
        try:
            appointment_time = datetime.fromisoformat(app_time_str.replace("Z", "+00:00"))
            time_to_app = appointment_time - datetime.now(appointment_time.tzinfo)
            hours_remaining = time_to_app.total_seconds() / 3600.0
        except Exception:
            hours_remaining = 12.0

        now_str = datetime.utcnow().isoformat()

        # 24-Hour Reminder touchpoint
        if 23.0 <= hours_remaining <= 24.5:
            msg_text = f"hey {lead.get('name', 'there')}! rick here. just a heads-up that our strategy call is scheduled for tomorrow. super excited to connect and help you get things moving towards that funding! 📊"
            
            # Send SMS/DM log
            db_env.DB.prepare(
                `INSERT INTO interactions (id, conversation_id, sender_type, platform_message_id, message_text, compliance_flag, compliance_reason, created_at)
                 VALUES (?, ?, 'bot', NULL, ?, 0, NULL, ?)`
            ).bind(crypto.randomUUID(), lead["conversation_id"], msg_text, now_str).run()
            print(f"24h reminder dispatched to Lead {lead['id']}.")

        # 1-Hour Reminder touchpoint
        elif 0.8 <= hours_remaining <= 1.2:
            msg_text = f"hey! just 1 hour until our call. if you can, grab a notebook and have your credit report ready so we can dive straight in. join the lobby link here when you're ready: https://angelsolutionsatl.com/lobby 🚀"
            
            db_env.DB.prepare(
                `INSERT INTO interactions (id, conversation_id, sender_type, platform_message_id, message_text, compliance_flag, compliance_reason, created_at)
                 VALUES (?, ?, 'bot', NULL, ?, 0, NULL, ?)`
            ).bind(crypto.randomUUID(), lead["conversation_id"], msg_text, now_str).run()
            print(f"1h reminder dispatched to Lead {lead['id']}.")
