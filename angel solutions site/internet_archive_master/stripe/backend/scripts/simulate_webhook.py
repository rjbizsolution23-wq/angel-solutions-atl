import time
import json
import httpx
import stripe

stripe_webhook_secret = "whsec_ZMbXlKgi9lWCTfhMGAuYb65u6PO7fh5h"

# Create a mock Stripe checkout.session.completed event
payload_dict = {
    "id": "evt_test_123",
    "object": "event",
    "api_version": "2023-10-16",
    "created": int(time.time()),
    "type": "checkout.session.completed",
    "data": {
        "object": {
            "id": "cs_test_abc123",
            "object": "checkout.session",
            "amount_total": 9700,  # $97.00
            "currency": "usd",
            "customer_details": {
                "email": "test_purchaser@example.com",
                "name": "Test Purchaser"
            },
            "payment_status": "paid",
            "status": "complete",
            "metadata": {
                "package_id": "lead_engine",
                "expected_amount": "9700"
            }
        }
    }
}

payload = json.dumps(payload_dict)
timestamp = int(time.time())
scheme = "v1"

# Generate Stripe signature
# Stripe signature format is t=timestamp,v1=signature
signature = stripe.WebhookSignature._compute_signature(f"{timestamp}.{payload}", stripe_webhook_secret)
stripe_signature_header = f"t={timestamp},v1={signature}"

# Send POST request to local webhook endpoint
url = "http://localhost:8000/api/webhooks/stripe"
headers = {
    "Stripe-Signature": stripe_signature_header,
    "Content-Type": "application/json"
}

print("Sending simulated webhook to:", url)
try:
    response = httpx.post(url, content=payload, headers=headers, timeout=10)
    print("Response Status Code:", response.status_code)
    print("Response JSON:", response.json())
except Exception as e:
    print("Error:", e)
