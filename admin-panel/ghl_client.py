# =====================================================================
# ANGEL SOLUTIONS ATL - GOHIGHLEVEL CRM INTEGRATION CLIENT
# =====================================================================
# Enterprise-grade integration connecting the Control Center with the
# GoHighLevel V2 API. Supports dynamic custom-field mapping, strict
# error bounds, and high-fidelity local simulation fallbacks.
# =====================================================================

import os
import requests
import json
import uuid
from typing import Dict, Any

# Helper to load .env variables manually for absolute safety
def load_env_manually():
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    val = val.strip().strip('"').strip("'")
                    if key not in os.environ:
                        os.environ[key] = val

load_env_manually()

def get_ghl_config() -> Dict[str, str]:
    """Retrieves current GoHighLevel credentials from environment"""
    # Reload from .env first to ensure latest edits are caught
    load_env_manually()
    return {
        "api_key": os.getenv("GHL_API_KEY", "").strip(),
        "location_id": os.getenv("GHL_LOCATION_ID", "Sfvt5kBZ3EUOws7MDWa3").strip()
    }

def sync_lead_to_ghl(lead: Dict[str, Any]) -> Dict[str, Any]:
    """
    Syncs a lead dictionary directly to GoHighLevel CRM using standard/custom fields.
    If no GHL_API_KEY is active, operates in a high-fidelity simulator mode.
    """
    config = get_ghl_config()
    api_key = config["api_key"]
    location_id = config["location_id"]

    # 1. Parse Name Elements Safely
    full_name = lead.get("name", "Valued Client").strip()
    name_parts = full_name.split(" ", 1)
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ""

    # 2. Extract Lead Attributes
    email = lead.get("email", "").strip()
    phone = lead.get("phone", "").strip()
    collections = lead.get("collections", 0)
    bankruptcy = lead.get("bankruptcy", 0)
    child_support = lead.get("child_support", 0)
    goal = lead.get("goal", "credit_repair")
    score = lead.get("score", 0.5)
    platform = lead.get("platform", "website")

    # 3. Formulate Tags & Grouping Segmentations
    lead_tags = ["credit_restoral_system", f"platform_{platform}"]
    if score >= 0.7:
        lead_tags.push("qualified_high_priority") if hasattr(lead_tags, "push") else lead_tags.append("qualified_high_priority")
    else:
        lead_tags.push("new_prospect") if hasattr(lead_tags, "push") else lead_tags.append("new_prospect")

    if collections > 5:
        lead_tags.append("high_collections")
    if bankruptcy == 1:
        lead_tags.append("active_bankruptcy")

    # 4. Compile High-Fidelity Custom GHL Fields Mapping
    custom_fields = [
        {"id": "credit_goal", "value": goal},
        {"id": "collections_count", "value": str(collections)},
        {"id": "bankruptcy_flag", "value": "Yes" if bankruptcy == 1 else "No"},
        {"id": "child_support_arrears", "value": "Yes" if child_support == 1 else "No"},
        {"id": "computed_lead_score", "value": str(score)}
    ]

    # 5. Build GHL contacts Payload
    ghl_payload = {
        "firstName": first_name,
        "lastName": last_name,
        "name": full_name,
        "email": email if email else f"{first_name.lower()}@angelsolutionsatl.local",
        "phone": phone if phone else None,
        "locationId": location_id,
        "tags": lead_tags,
        "customFields": custom_fields
    }

    # 6. Check if API Key exists - Else route to Mock/Simulation Mode
    if not api_key or api_key.startswith("your_") or api_key == "placeholder":
        sim_contact_id = f"ghl_sim_{uuid.uuid4().hex[:8]}"
        print(f"[MOCK GHL SYNC] Simulated sync payload for Lead {full_name}:")
        print(json.dumps(ghl_payload, indent=2))
        return {
            "success": True,
            "mode": "simulation",
            "contact_id": sim_contact_id,
            "payload": ghl_payload,
            "message": f"Simulated GHL Sync Complete! Contact ID generated: {sim_contact_id}"
        }

    # 7. Make Real REST Request to GoHighLevel CRM
    print(f"[GHL CRM ACTIVE] Posting Lead {full_name} to GoHighLevel location {location_id}...")
    try:
        response = requests.post(
            "https://services.gohighlevel.com/v2/contacts/",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Version": "2021-04-15"
            },
            json=ghl_payload,
            timeout=10
        )

        if response.status_code in [200, 201]:
            resp_data = response.json()
            contact_id = resp_data.get("contact", {}).get("id", f"ghl_live_{uuid.uuid4().hex[:8]}")
            print(f"[GHL CRM ACTIVE] CRM Sync Success! Registered GHL Contact ID: {contact_id}")
            return {
                "success": True,
                "mode": "live",
                "contact_id": contact_id,
                "payload": ghl_payload,
                "message": f"Successfully Synced with GoHighLevel CRM! Contact ID: {contact_id}"
            }
        else:
            err_msg = response.text
            print(f"[GHL CRM ERROR] API sync failed with status {response.status_code}: {err_msg}")
            return {
                "success": False,
                "mode": "live",
                "error": f"GoHighLevel API returned {response.status_code}: {err_msg}",
                "message": "Failed to sync with GoHighLevel CRM. Check credentials."
            }

    except Exception as e:
        print(f"[GHL CRM EXCEPTION] Connection exception during GHL API post: {str(e)}")
        return {
            "success": False,
            "mode": "live",
            "error": str(e),
            "message": f"Network error during GHL Sync: {str(e)}"
        }
