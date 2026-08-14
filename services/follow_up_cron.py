# =====================================================================
# ANGEL SOLUTIONS ATL - AUTOMATED FOLLOW-UP NURTURE CRON
# =====================================================================
# Executes daily at 8 AM. Evaluates elapsed days since last contact,
# triggers targeted 7-step nurture copy, and delivers compliant DMs.
# =====================================================================

import os
import requests
from datetime import datetime, timedelta

CADENCE_DAYS = [1, 3, 5, 8, 12, 16, 18]

# Standard static follow-up copy templates (Steps 1, 2, 7)
STATIC_TEMPLATES = {
    1: "hey! just wanted to check in on you. were you able to check out the link i sent over yesterday? let me know if you have any questions or if you're ready to get those items cleaned up! 😊",
    2: "hey, i know life gets super busy! just wanted to see if you had any questions on how we actually get those collections off your report. my team and i are ready to jump on it whenever you are.",
    7: "happy friday! my dispute team has a few open slots for next week. if you're ready to clear those credit roadblocks and get things moving towards that funding, just let me know! 🚀"
}

def check_meta_24h_window(last_message_time_str: str) -> bool:
    """
    Checks if we are still within Meta's strict 24-hour messaging window.
    """
    if not last_message_time_str:
        return False
    try:
        last_msg_time = datetime.fromisoformat(last_message_time_str.replace("Z", "+00:00"))
        time_diff = datetime.now(last_msg_time.tzinfo) - last_msg_time
        return time_diff.total_seconds() < 24 * 60 * 60
    except Exception as e:
        print(f"Error parsing date: {e}")
        return False

def generate_ai_followup(step: int, service_needed: str, env) -> str:
    """
    Leverages Claude to craft dynamically tailored, high-converting follow-up variants.
    """
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return f"hey! just wanted to check in on your {service_needed or 'credit'} goals. let me know when you're free to chat so we can get things moving! ✨"

    prompt_angle = ""
    if step == 3:
        prompt_angle = "Focus on the specific collection accounts holding them back from funding."
    elif step == 4:
        prompt_angle = "Provide a mini motivational insight regarding legal credit restoral benefits."
    elif step == 5:
        prompt_angle = "Offer to introduce them directly to Jordynn Miller on a 15-minute strategy call."
    else: # Step 6
        prompt_angle = "Highlight an success story or client testimonial case study."

    system_prompt = f"""
    You are Jordynn Miller sending a quick, extremely natural, warm follow-up text. Write a very brief message (1-2 sentences max). Talk like a real human sending a casual text message.
    Focus: {prompt_angle}
    Context: They expressed interest in {service_needed or 'credit repair/business funding'}.
    Constraints: 
    - Never use AI buzzwords (delve, additionally, furthermore, tailored, leverage, embark).
    - NEVER use bullet points, bolding, lists, or colons.
    - Never use 'credit sweep', 'guarantee', 'guaranteed', 'best', 'yo', 'bet'.
    - Keep it short, casual, and warm.
    - Always include booking link: https://angelsolutionsatl.com/book-online.
    """

    payload = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 256,
        "messages": [{"role": "user", "content": system_prompt}],
        "temperature": 0.7
    }

    try:
        url = os.getenv("AI_ENSEMBLE_URL") or "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        res = requests.post(url, json=payload, headers=headers, timeout=10)
        return res.json()["content"][0]["text"].strip()
    except Exception as e:
        print(f"Failed to generate AI follow-up: {e}")
        return f"hey! let's clear those credit roadblocks and get you capital-ready. book your strategy call here: https://angelsolutionsatl.com/book-online"

def execute_daily_nurture_campaign(db_env):
    """
    Main loop querying eligible leads and executing nurture step dispatches.
    """
    # SQLite/D1 select queries representation
    # Select leads that are qualified, not paused, and have follow-up step < 7
    query = """
        SELECT l.*, c.last_message_at, c.bot_active 
        FROM leads l
        JOIN conversations c ON l.id = c.lead_id
        WHERE l.lead_state = 'QUALIFIED' 
          AND (l.paused_until IS NULL OR l.paused_until < datetime('now'))
          AND l.follow_up_step < 7
          AND c.bot_active = 1
    """
    
    if not hasattr(db_env, "DB"):
        print("[MOCK NURTURE CRON] DB not initialized. Skipping automated batch run.")
        return

    leads_to_process = db_env.DB.prepare(query).all()
    print(f"Found {len(leads_to_process.results)} leads eligible for nurture calculation.")

    for lead in leads_to_process.results:
        # Calculate days elapsed since last contact
        try:
            last_contact = datetime.fromisoformat(lead["last_contact_at"].replace("Z", "+00:00"))
            days_elapsed = (datetime.now(last_contact.tzinfo) - last_contact).days
        except Exception:
            days_elapsed = 0

        current_step = lead["follow_up_step"]
        target_step = current_step + 1
        required_days = CADENCE_DAYS[current_step]

        if days_elapsed >= required_days:
            print(f"Lead {lead['id']} ready for Step {target_step} (Days elapsed: {days_elapsed}, required: {required_days})")

            # Check strict Meta 24h message window
            within_24h = check_meta_24h_window(lead["last_message_at"])

            # 1. Determine or generate the message
            if target_step in STATIC_TEMPLATES:
                message_text = STATIC_TEMPLATES[target_step]
            else:
                message_text = generate_ai_followup(target_step, lead["service_needed"], db_env)

            now_str = datetime.utcnow().isoformat()

            # If outside 24h window, log skip state (no Tag-based template configured yet)
            if not within_24h:
                print(f"Skipping live send for Lead {lead['id']} due to expired 24h Meta window.")
                db_env.DB.prepare(
                    `INSERT INTO follow_ups (id, lead_id, step_number, message_text, scheduled_for, sent, sent_at, skipped_reason, created_at)
                     VALUES (?, ?, ?, ?, ?, 0, NULL, 'meta_24h_expired', ?)`
                ).bind(crypto.randomUUID(), lead["id"], target_step, message_text, now_str, now_str).run()
                continue

            # 2. Log nurture record to D1
            db_env.DB.prepare(
                `INSERT INTO follow_ups (id, lead_id, step_number, message_text, scheduled_for, sent, sent_at, skipped_reason, created_at)
                 VALUES (?, ?, ?, ?, ?, 1, ?, NULL, ?)`
            ).bind(crypto.randomUUID(), lead["id"], target_step, message_text, now_str, now_str, now_str).run()

            # 3. Log interaction
            db_env.DB.prepare(
                `INSERT INTO interactions (id, conversation_id, sender_type, platform_message_id, message_text, compliance_flag, compliance_reason, created_at)
                 VALUES (?, ?, 'bot', NULL, ?, 0, NULL, ?)`
            ).bind(crypto.randomUUID(), lead["conversation_id"] if "conversation_id" in lead else "mock_conv_id", message_text, now_str).run()

            # 4. Update lead model state
            db_env.DB.prepare(
                `UPDATE leads SET follow_up_step = ?, last_contact_at = ?, updated_at = ? WHERE id = ?`
            ).bind(target_step, now_str, now_str, lead["id"]).run()

            # 5. Live deliver DM if launch approved
            is_shadow = os.getenv("ENVIRONMENT") != "production"
            if not is_shadow:
                # Dispatch live Meta Send API
                recipient_id = lead["platform_user_id"]
                url = f"https://graph.facebook.com/v19.0/me/messages?access_token={os.getenv('META_PAGE_ACCESS_TOKEN')}"
                requests.post(url, json={
                    "recipient": {"id": recipient_id},
                    "message": {"text": message_text}
                }, timeout=10)
                print(f"Live DM delivered to {recipient_id}.")
            else:
                print(f"[SHADOW MODE] Logged draft follow-up to {lead['platform_user_id']}.")
