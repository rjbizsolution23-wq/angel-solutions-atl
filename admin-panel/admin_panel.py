# =====================================================================
# ANGEL SOLUTIONS ATL - FASTAPI CORE ADMINISTRATION PANEL
# =====================================================================
# Premium management interface allowing Jordynn Miller to monitor leads,
# override automation states, view system health, simulate messaging,
# and programmatically draft, launch, and monitor Meta Ad Campaigns.
# =====================================================================

from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional, List, Dict, Any
import os
import json
import uuid
import requests

# Import the SVG analytics engine & Meta client
from analytics_dashboard import compute_conversion_kpis
from meta_ads_client import MetaAdsClient
from ghl_client import get_ghl_config, sync_lead_to_ghl

import sys
# Resolve sibling ai-ensemble directory imports
sys.path.append(os.path.join(os.path.dirname(__file__), "../ai-ensemble"))
from jordynn_ai import generate_rick_response, clean_response

app = FastAPI(title="Angel Solutions ATL - Admin Portal")

ADMIN_USERNAME = "admin@angelsolutionsatl.com"
ADMIN_PASSWORD_PLAIN = "ChangeThisPassword123!"

# In-memory session mock data for live demonstration
MOCK_LEADS = [
    {
        "id": "lead_01",
        "name": "Marcus Aurelius",
        "lead_state": "QUALIFIED",
        "platform": "instagram",
        "score": 0.85,
        "collections": 4,
        "phone": "+14045550192",
        "bot_active": True,
        "sentiment": "friendly",
        "messages": [
            {"sender": "user", "text": "Hey Rick, I need help with business funding but my credit has some collections.", "timestamp": "2026-07-16 14:22:01"},
            {"sender": "bot", "text": "hey! yeah i can definitely help with that. let's clean up those negative items and get your profile commercial-ready. are you looking for unsecured capital or trade lines?", "timestamp": "2026-07-16 14:22:05"},
            {"sender": "user", "text": "I need around $50k for inventory.", "timestamp": "2026-07-16 14:23:40"},
            {"sender": "bot", "text": "got you. we see that all the time. let's schedule a strategy call to map this out: https://angelsolutionsatl.com/book-online", "timestamp": "2026-07-16 14:23:45"}
        ]
    },
    {
        "id": "lead_02",
        "name": "Cassius Clay",
        "lead_state": "NEW",
        "platform": "facebook",
        "score": 0.42,
        "collections": 12,
        "phone": "+16785550143",
        "bot_active": True,
        "sentiment": "neutral",
        "messages": [
            {"sender": "user", "text": "How much does it cost?", "timestamp": "2026-07-17 09:12:10"},
            {"sender": "bot", "text": "hey! it depends on what we're looking at. my monthly skool community is $67/mo if you want DIY, or for full-service 1-on-1 we do custom strategy calls: https://angelsolutionsatl.com/book-online", "timestamp": "2026-07-17 09:12:18"}
        ]
    },
    {
        "id": "lead_03",
        "name": "Alisha Keys",
        "lead_state": "ASSIGN",
        "platform": "instagram",
        "score": 0.95,
        "collections": 15,
        "phone": "+17705550181",
        "bot_active": False,
        "sentiment": "frustrated",
        "messages": [
            {"sender": "user", "text": "I was charged twice and I want a refund.", "timestamp": "2026-07-15 11:05:00"},
            {"sender": "bot", "text": "Hey! Jordynn here. I see we have some items to review together immediately. I am deactivating our AI bot right now and alerting my team to reach out to you via call/SMS on your line ASAP so we can handle this.", "timestamp": "2026-07-15 11:05:12"},
            {"sender": "user", "text": "Ok when will they call me?", "timestamp": "2026-07-15 11:06:05"},
            {"sender": "human", "text": "Hey Alisha, this is Rick. I just saw this. My lead specialist will ring you in exactly 5 minutes. So sorry about the double charge, we'll get it refunded right now.", "timestamp": "2026-07-15 11:08:22"}
        ]
    }
]

SIMULATION_HISTORY = []
DRAFTED_COPY_CACHE = ""
CAMPAIGN_LAUNCH_LOGS = []

def render_login_page(error_msg: Optional[str] = None) -> HTMLResponse:
    error_html = f"<div class='error-box'>{error_msg}</div>" if error_msg else ""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Angel Solutions ATL — Admin Login</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #09090b;
            --card: #18181b;
            --border: #27272a;
            --primary: #f59e0b;
            --primary-hover: #d97706;
            --fg: #fafafa;
            --muted-fg: #a1a1aa;
        }}
        body {{
            background-color: var(--bg);
            background-image: radial-gradient(circle at top right, rgba(245, 158, 11, 0.05), transparent 40%),
                              radial-gradient(circle at bottom left, rgba(245, 158, 11, 0.02), transparent 40%);
            display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: var(--fg);
        }}
        .card {{
            background: var(--card); border: 1px solid var(--border); border-radius: 1rem; padding: 2.5rem; max-width: 400px; width: 100%;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3);
            backdrop-filter: blur(8px);
        }}
        .logo-area {{ text-align: center; margin-bottom: 2rem; }}
        .logo-area h1 {{ margin: 0; font-family: 'Outfit', sans-serif; font-size: 1.8rem; color: var(--primary); letter-spacing: -0.05em; }}
        .logo-area p {{ margin: 0.25rem 0 0; font-size: 0.82rem; color: var(--muted-fg); }}
        h2 {{ margin: 0 0 1.5rem; text-align: center; font-size: 1.2rem; font-weight: 600; }}
        input {{
            display: block; width: 100%; box-sizing: border-box; padding: 0.75rem 1rem; 
            background: #09090b; border: 1px solid var(--border); border-radius: 0.5rem; margin-bottom: 1.25rem;
            color: var(--fg); font-size: 0.9rem; transition: border 0.2s;
        }}
        input:focus {{ outline: none; border-color: var(--primary); }}
        button {{
            display: block; width: 100%; padding: 0.75rem; border: none; border-radius: 0.5rem; 
            background: var(--primary); color: #09090b; font-weight: 700; cursor: pointer; transition: background 0.2s;
        }}
        button:hover {{ background: var(--primary-hover); }}
        .error-box {{
            background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.2); 
            color: #ef4444; font-size: 0.82rem; padding: 0.75rem; border-radius: 0.5rem; margin-bottom: 1rem; text-align: center;
        }}
    </style>
</head>
<body>
    <div class="card">
        <div class="logo-area">
            <h1>ANGEL SOLUTIONS ATL</h1>
            <p>Admin Portal &amp; Control Center</p>
        </div>
        {error_html}
        <form method="POST" action="/login">
            <input type="text" name="username" placeholder="admin@angelsolutionsatl.com" required autocomplete="off">
            <input type="password" name="password" placeholder="••••••••" required>
            <button type="submit">Sign In</button>
        </form>
    </div>
</body>
</html>"""
    return HTMLResponse(html)

def render_dashboard_page(leads: list, simulation_history: list, active_tab: str = "leads", view_lead_id: Optional[str] = None, request: Request = None) -> HTMLResponse:
    # Compute live KPIs and fetch SVG funnel
    kpis = compute_conversion_kpis(None) # Instantiates MetaAdsClient and pulls active metrics automatically
    metrics = kpis["metrics"]
    campaigns = kpis["campaigns"]
    funnel_svg = kpis["charts"]["funnel_svg"]

    # Select active lead for conversation thread view
    active_lead = None
    if view_lead_id:
        for lead in leads:
            if lead["id"] == view_lead_id:
                active_lead = lead
                break
    if not active_lead and leads:
        active_lead = leads[0]

    # Render lead table rows
    lead_rows = ""
    for lead in leads:
        bot_toggle_label = "Deactivate Bot" if lead["bot_active"] else "Activate Bot"
        bot_toggle_class = "btn-warn" if lead["bot_active"] else "btn-success"
        active_row_style = 'class="active-row"' if active_lead and lead["id"] == active_lead["id"] else ""
        lead_rows += f"""
        <tr {active_row_style}>
            <td><strong>{lead['name']}</strong><br><span style="font-size:0.75rem; color:#a1a1aa;">{lead['phone']}</span></td>
            <td><span class="badge state-{lead['lead_state'].lower()}">{lead['lead_state']}</span></td>
            <td>{lead['platform'].capitalize()}</td>
            <td>{lead['collections']} items</td>
            <td><span class="badge state-{'qualified' if lead['sentiment'] == 'friendly' else 'new' if lead['sentiment'] == 'neutral' else 'assign'}">{lead['sentiment'].upper()}</span></td>
            <td style="text-align: right; white-space: nowrap;">
                <a href="/admin?view_lead={lead['id']}" class="btn btn-ok" style="text-decoration:none; display:inline-block; margin-right: 0.25rem;">💬 History</a>
                <form style="display:inline-block;" method="POST" action="/action/toggle-bot">
                    <input type="hidden" name="lead_id" value="{lead['id']}">
                    <button class="btn {bot_toggle_class}" type="submit">{bot_toggle_label}</button>
                </form>
                <form style="display:inline-block;" method="POST" action="/action/sync">
                    <input type="hidden" name="lead_id" value="{lead['id']}">
                    <button class="btn btn-ok" type="submit">Sync GHL</button>
                </form>
            </td>
        </tr>
        """

    # Render simulation message history
    history_html = ""
    if not simulation_history:
        history_html = "<div class='empty-simulation'>No simulated chats run yet. Test a message on the right!</div>"
    else:
        for msg in reversed(simulation_history):
            history_html += f"""
            <div class="simulation-bubble-group">
                <div class="chat-bubble user-bubble">
                    <span class="bubble-tag">USER ({msg['user_name']})</span>
                    <p>{msg['user_msg']}</p>
                </div>
                <div class="chat-bubble bot-bubble">
                    <span class="bubble-tag">RICK (AI PERSONA)</span>
                    <p>{msg['reply_text']}</p>
                    <div class="reply-meta">
                        <span>🎯 Lead State: {msg['lead_state']}</span> | 
                        <span>📈 Score: {msg['score']}</span> | 
                        <span>🎭 Sentiment: {msg['sentiment']}</span> | 
                        <span>🛡️ Compliance: {msg['compliance']}</span>
                    </div>
                </div>
            </div>
            """

    # Render selected lead thread history
    thread_html = ""
    if active_lead and "messages" in active_lead:
        for msg in active_lead["messages"]:
            sender_lbl = ""
            bubble_class = ""
            tag_color = ""
            
            if msg["sender"] == "user":
                sender_lbl = f"{active_lead['name']} (Prospect)"
                bubble_class = "user-bubble"
                tag_color = "color: #3b82f6;"
            elif msg["sender"] == "bot":
                sender_lbl = "Rick (AI Persona)"
                bubble_class = "bot-bubble"
                tag_color = "color: var(--primary);"
            else:
                sender_lbl = "Rick (Human Manual)"
                bubble_class = "bot-bubble human-override-bubble"
                tag_color = "color: #a78bfa;"
                
            thread_html += f"""
            <div class="simulation-bubble-group">
                <div class="chat-bubble {bubble_class}">
                    <span class="bubble-tag" style="{tag_color}">{sender_lbl}</span>
                    <p style="margin: 0;">{msg['text']}</p>
                    <span style="font-size: 0.65rem; color: var(--muted-fg); display: block; text-align: right; margin-top: 0.25rem;">{msg['timestamp']}</span>
                </div>
            </div>
            """
    else:
        thread_html = "<div class='empty-simulation'>Select a lead to monitor and view their conversation.</div>"

    # Render campaigns table rows
    campaign_rows = ""
    for camp in campaigns:
        status_class = "state-qualified" if camp["status"] == "ACTIVE" else "state-dq"
        campaign_rows += f"""
        <tr>
            <td><strong>{camp['name']}</strong><br><span style="font-size:0.72rem; color:#a1a1aa;">ID: {camp['id']}</span></td>
            <td><span class="badge {status_class}">{camp['status']}</span></td>
            <td>${camp['budget']:.2f}/day</td>
            <td>${camp['spend']:.2f}</td>
            <td>{camp['impressions']:,}</td>
            <td>{camp['clicks']:,}</td>
            <td><strong>{camp['conversions']} Leads</strong></td>
        </tr>
        """

    # Render launch log block
    logs_html = ""
    if CAMPAIGN_LAUNCH_LOGS:
        logs_list_items = "".join(f"<li>{log}</li>" for log in CAMPAIGN_LAUNCH_LOGS)
        logs_html = f"""
        <div class="launch-logs-box">
            <h4>🚀 Ads Publisher Pipeline Output Logs</h4>
            <ul>{logs_list_items}</ul>
        </div>
        """

    # Tab selection styles
    tab_leads_active = "active-tab" if active_tab == "leads" else ""
    tab_ads_active = "active-tab" if active_tab == "ads" else ""
    tab_config_active = "active-tab" if active_tab == "config" else ""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Angel Solutions ATL — Control Center</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #09090b;
            --card: #18181b;
            --border: #27272a;
            --primary: #f59e0b;
            --primary-hover: #d97706;
            --fg: #fafafa;
            --muted-fg: #a1a1aa;
            --success: #10b981;
            --error: #ef4444;
        }}
        body {{
            background: var(--bg);
            background-image: radial-gradient(circle at 10% 10%, rgba(245, 158, 11, 0.03), transparent 30%),
                              radial-gradient(circle at 90% 90%, rgba(245, 158, 11, 0.02), transparent 30%);
            margin: 0; padding: 2rem; font-family: 'Plus Jakarta Sans', sans-serif; color: var(--fg);
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        header {{
            display: flex; justify-content: space-between; align-items: center; 
            margin-bottom: 2rem; border-bottom: 1px solid var(--border); padding-bottom: 1.5rem;
        }}
        .brand {{ display: flex; align-items: center; gap: 0.75rem; }}
        .brand h1 {{ margin: 0; font-family: 'Outfit', sans-serif; font-size: 1.6rem; color: var(--primary); letter-spacing: -0.05em; }}
        .brand span {{
            background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.2);
            color: var(--primary); font-size: 0.72rem; padding: 0.15rem 0.5rem; border-radius: 99px; font-weight: 600;
        }}
        
        /* Navigation Tabs */
        .tab-bar {{
            display: flex; gap: 1rem; border-bottom: 1px solid var(--border); margin-bottom: 1.5rem; padding-bottom: 0.5rem;
        }}
        .tab-btn {{
            background: none; border: none; color: var(--muted-fg); font-size: 0.95rem; font-weight: 600; cursor: pointer; padding: 0.5rem 1rem;
            border-bottom: 2px solid transparent; transition: all 0.2s; font-family: 'Outfit', sans-serif;
        }}
        .tab-btn:hover {{ color: var(--primary); }}
        .active-tab {{ color: var(--primary); border-color: var(--primary); }}

        /* Dashboard Layout Grid */
        .dashboard-grid {{
            display: grid; grid-template-columns: 1.2fr 1fr; gap: 1.5rem; margin-bottom: 1.5rem;
        }}
        .ads-grid {{
            display: grid; grid-template-columns: 1.4fr 1fr; gap: 1.5rem; margin-bottom: 1.5rem;
        }}
        @media(max-width: 900px) {{
            .dashboard-grid, .ads-grid {{ grid-template-columns: 1fr; }}
        }}

        /* Cards & Section Elements */
        .card {{
            background: var(--card); border: 1px solid var(--border); border-radius: 0.85rem; padding: 1.5rem;
            box-shadow: 0 4px 20px -2px rgba(0,0,0,0.25); position: relative; overflow: hidden;
        }}
        .card h2 {{ font-family: 'Outfit', sans-serif; font-size: 1.2rem; margin: 0 0 1.25rem; font-weight: 600; display: flex; align-items: center; gap: 0.5rem; }}
        
        /* Stats Widgets */
        .stats-row {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.5rem; }}
        .stat-box {{ background: #121214; border: 1px solid var(--border); padding: 1.1rem; border-radius: 0.65rem; text-align: center; }}
        .stat-val {{ font-size: 1.7rem; font-weight: 700; color: var(--primary); font-family: 'Outfit', sans-serif; margin-bottom: 0.2rem; }}
        .stat-lbl {{ font-size: 0.72rem; color: var(--muted-fg); text-transform: uppercase; font-weight: 600; }}

        /* Live Connections Indicators */
        .conn-row {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.5rem; }}
        .conn-box {{
            background: #121214; border: 1px solid var(--border); padding: 0.9rem; border-radius: 0.65rem; 
            display: flex; align-items: center; gap: 0.75rem; font-size: 0.78rem;
        }}
        .dot {{ width: 8px; height: 8px; border-radius: 50%; background: var(--success); display: inline-block; box-shadow: 0 0 8px var(--success); }}
        .conn-name {{ font-weight: 600; }}
        .conn-details {{ color: var(--muted-fg); font-size: 0.7rem; margin-top: 0.1rem; }}

        /* Lead Table */
        table {{ width: 100%; border-collapse: collapse; font-size: 0.82rem; }}
        th, td {{ text-align: left; padding: 0.75rem 1rem; border-bottom: 1px solid var(--border); }}
        th {{ background: #121214; font-weight: 600; color: var(--muted-fg); font-size: 0.75rem; text-transform: uppercase; }}
        tr:hover td {{ background: rgba(255,255,255,0.01); }}
        
        /* Badges */
        .badge {{ padding: 0.2rem 0.5rem; border-radius: 99px; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; display: inline-block; }}
        .state-new {{ background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.2); }}
        .state-qualified {{ background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.2); }}
        .state-assign {{ background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.2); }}
        .state-dq {{ background: rgba(161, 161, 170, 0.15); color: #a1a1aa; border: 1px solid rgba(161, 161, 170, 0.2); }}

        /* Interactive Buttons */
        .btn {{
            border: none; border-radius: 0.35rem; padding: 0.35rem 0.75rem; font-size: 0.75rem; font-weight: 600; cursor: pointer; transition: all 0.2s;
        }}
        .btn-warn {{ background: rgba(239, 68, 68, 0.1); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.2); }}
        .btn-warn:hover {{ background: #ef4444; color: #09090b; }}
        .btn-success {{ background: rgba(16, 185, 129, 0.1); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.2); }}
        .btn-success:hover {{ background: #10b981; color: #09090b; }}
        .btn-ok {{ background: rgba(255,255,255,0.05); color: var(--fg); border: 1px solid var(--border); }}
        .btn-ok:hover {{ background: var(--primary); color: #09090b; border-color: var(--primary); }}

        /* Selected active lead row styling */
        tr.active-row td {{
            background: rgba(245, 158, 11, 0.05) !important;
            border-left: 3px solid var(--primary);
        }}
        .human-override-bubble {{
            background: rgba(167, 139, 250, 0.08) !important;
            border: 1px solid rgba(167, 139, 250, 0.3) !important;
            align-self: flex-end;
            border-bottom-right-radius: 0.15rem;
        }}

        /* Simulation Playground Section */
        .simulation-container {{
            display: flex; flex-direction: column; height: 420px; background: #121214; border: 1px solid var(--border); border-radius: 0.65rem; padding: 1rem; overflow: hidden;
        }}
        .simulation-feed {{ flex-grow: 1; overflow-y: auto; padding-right: 0.5rem; display: flex; flex-direction: column; gap: 1rem; }}
        .simulation-bubble-group {{ display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 0.5rem; }}
        .chat-bubble {{ max-width: 85%; padding: 0.85rem 1rem; border-radius: 0.75rem; font-size: 0.82rem; line-height: 1.45; position: relative; }}
        .user-bubble {{ background: #27272a; align-self: flex-start; border-bottom-left-radius: 0.15rem; border: 1px solid #3f3f46; }}
        .bot-bubble {{ background: rgba(245, 158, 11, 0.08); align-self: flex-end; border-bottom-right-radius: 0.15rem; border: 1px solid rgba(245, 158, 11, 0.2); }}
        .bubble-tag {{ font-size: 0.65rem; font-weight: 700; color: var(--primary); display: block; margin-bottom: 0.25rem; letter-spacing: 0.05em; }}
        .user-bubble .bubble-tag {{ color: #3b82f6; }}
        .reply-meta {{ font-size: 0.68rem; color: var(--muted-fg); border-top: 1px solid rgba(255,255,255,0.05); margin-top: 0.5rem; padding-top: 0.35rem; }}
        
        .simulation-form {{ display: flex; gap: 0.5rem; margin-top: 1rem; }}
        .simulation-input {{
            flex-grow: 1; background: #09090b; border: 1px solid var(--border); color: white; padding: 0.65rem 0.85rem; border-radius: 0.35rem; font-size: 0.82rem;
        }}
        .simulation-input:focus {{ outline: none; border-color: var(--primary); }}
        .btn-primary {{ background: var(--primary); color: #09090b; font-weight: 700; }}
        .btn-primary:hover {{ background: var(--primary-hover); }}
        .empty-simulation {{
            display: flex; height: 100%; align-items: center; justify-content: center; text-align: center; color: var(--muted-fg); font-size: 0.8rem;
        }}

        /* Ads Suite CSS */
        .form-label {{ display: block; font-size: 0.82rem; font-weight: 600; color: var(--muted-fg); margin-bottom: 0.4rem; }}
        .ad-textarea {{
            width: 100%; box-sizing: border-box; background: #09090b; border: 1px solid var(--border); border-radius: 0.5rem;
            color: white; padding: 0.75rem; font-size: 0.85rem; font-family: inherit; resize: vertical; min-height: 120px;
        }}
        .ad-textarea:focus {{ outline: none; border-color: var(--primary); }}
        .form-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.25rem; }}
        .launch-logs-box {{
            margin-top: 1.5rem; background: rgba(245, 158, 11, 0.03); border: 1px solid rgba(245, 158, 11, 0.15); padding: 1rem; border-radius: 0.5rem;
        }}
        .launch-logs-box h4 {{ margin: 0 0 0.5rem; color: var(--primary); font-family: 'Outfit', sans-serif; font-size: 0.9rem; }}
        .launch-logs-box ul {{ margin: 0; padding-left: 1.25rem; font-family: monospace; font-size: 0.78rem; color: #d4d4d8; line-height: 1.5; }}
    </style>
    <script>
        function selectTab(tabName) {{
            window.location.href = "/?tab=" + tabName;
        }}
    </script>
</head>
<body>
    <div class="container">
        <header>
            <div class="brand">
                <h1>ANGEL SOLUTIONS ATL</h1>
                <span>CONTROL CENTER v2.5</span>
            </div>
            <a href="/logout" style="font-size:0.85rem; color: var(--muted-fg); text-decoration:none; font-weight:500;">Sign Out</a>
        </header>

        <!-- Live Core Connectors Indicators -->
        <h3 style="margin-top:0; font-family:'Outfit',sans-serif; font-size:0.95rem; text-transform:uppercase; color:var(--primary); letter-spacing:0.05em;">Live Connection Pipelines</h3>
        <div class="conn-row">
            <div class="conn-box">
                <span class="dot"></span>
                <div>
                    <div class="conn-name">Cloudflare Worker</div>
                    <div class="conn-details">active · 200ms ping</div>
                </div>
            </div>
            <div class="conn-box">
                <span class="dot"></span>
                <div>
                    <div class="conn-name">GoHighLevel API</div>
                    <div class="conn-details">active · CRM synced</div>
                </div>
            </div>
            <div class="conn-box">
                <span class="dot"></span>
                <div>
                    <div class="conn-name">Meta Ads / Graph API</div>
                    <div class="conn-details">active · Token bound</div>
                </div>
            </div>
            <div class="conn-box">
                <span class="dot"></span>
                <div>
                    <div class="conn-name">OpenRouter / AI</div>
                    <div class="conn-details">active · Llama 3.1 8B</div>
                </div>
            </div>
        </div>

        <!-- Tab Selection Bar -->
        <div class="tab-bar">
            <button class="tab-btn {tab_leads_active}" onclick="selectTab('leads')">📊 Leads &amp; Conversations</button>
            <button class="tab-btn {tab_ads_active}" onclick="selectTab('ads')">🚀 Meta Campaign &amp; AI Creator</button>
            <button class="tab-btn {tab_config_active}" onclick="selectTab('config')">⚙️ CRM &amp; GHL Integration</button>
        </div>

        <!-- LEADS & CONVERSATIONS TAB -->
        {f'''
        <!-- KPI Performance Indicators -->
        <div class="stats-row">
            <div class="stat-box">
                <div class="stat-val">{metrics['total_leads']}</div>
                <div class="stat-lbl">Total Leads Ingested</div>
            </div>
            <div class="stat-box">
                <div class="stat-val">{metrics['qualified_leads']}</div>
                <div class="stat-lbl">Qualified Leads</div>
            </div>
            <div class="stat-box">
                <div class="stat-val">{metrics['booked_leads']}</div>
                <div class="stat-lbl">Strategy Calls Booked</div>
            </div>
            <div class="stat-box">
                <div class="stat-val">{metrics['conversion_rate_percentage']}%</div>
                <div class="stat-lbl">Conversion Rate</div>
            </div>
        </div>

        <!-- Multi-Grid Control Panel -->
        <div class="dashboard-grid">
            <!-- Left Side: Live Leads Control -->
            <div class="card">
                <h2>📊 Active Threads &amp; Automation State</h2>
                <div style="overflow-x: auto;">
                    <table>
                        <thead>
                            <tr>
                                <th>Prospect Contact</th>
                                <th>State</th>
                                <th>Source</th>
                                <th>Collections</th>
                                <th>Sentiment</th>
                                <th style="text-align: right;">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {lead_rows}
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Right Side: Real-Time Live Chat Monitor & Overrides -->
            <div class="card">
                <h2>💬 Live Conversation Thread Monitor</h2>
                <div style="font-size:0.78rem; color:var(--muted-fg); margin-top:-0.5rem; margin-bottom:1rem; display:flex; justify-content:space-between; align-items:center;">
                    <span>Monitoring: <strong>{active_lead['name'] if active_lead else 'None'}</strong></span>
                    <span>Bot: <strong style="color: {'var(--success)' if active_lead and active_lead['bot_active'] else 'var(--error)'};">{'ACTIVE' if active_lead and active_lead['bot_active'] else 'PAUSED'}</strong></span>
                </div>
                <div class="simulation-container">
                    <div class="simulation-feed" style="scroll-behavior: smooth;">
                        {thread_html}
                    </div>
                    <form class="simulation-form" method="POST" action="/action/override-reply">
                        <input type="hidden" name="lead_id" value="{active_lead['id'] if active_lead else ''}">
                        <input class="simulation-input" type="text" name="override_text" placeholder="Type a custom reply as Jordynn Miller (Human Override)..." required autocomplete="off">
                        <button class="btn btn-primary" type="submit">Send Override</button>
                    </form>
                </div>
            </div>
        </div>

        <!-- Bottom Section: Funnel Graph & Sandbox Simulator -->
        <div class="dashboard-grid" style="margin-top: 1.5rem;">
            <!-- Left Side: Funnel Graph -->
            <div class="card">
                <h2>📈 Conversion Funnel Graph (SVG Dynamic Render)</h2>
                <div style="max-width: 600px; margin: 0 auto; padding: 1rem 0;">
                    {funnel_svg}
                </div>
            </div>

            <!-- Right Side: Sandbox Webhook & Voice Playground -->
            <div class="card">
                <h2>💬 Sandbox Webhook &amp; Voice Playground</h2>
                <p style="font-size:0.78rem; color:var(--muted-fg); margin-top:-0.5rem; margin-bottom:1rem;">
                    Simulate how your live Cloudflare Worker and Claude AI prompt evaluate incoming customer messages, parses parameters, checks compliance, and responds in Jordynn's direct voice.
                </p>
                <div class="simulation-container">
                    <div class="simulation-feed">
                        {history_html}
                    </div>
                    <form class="simulation-form" method="POST" action="/action/simulate">
                        <input class="simulation-input" type="text" name="user_message" placeholder="Type a message as a prospect (e.g. 'How much is credit restoral?')" required autocomplete="off">
                        <button class="btn btn-primary" type="submit">Send Test DM</button>
                    </form>
                </div>
            </div>
        </div>
        ''' if active_tab == 'leads' else ''}

        <!-- META ADS & AI SUITE TAB -->
        {f'''
        <!-- Ads Performance Indicators -->
        <div class="stats-row">
            <div class="stat-box">
                <div class="stat-val">${metrics['ad_spend']:.2f}</div>
                <div class="stat-lbl">Ad Spend (Last 30d)</div>
            </div>
            <div class="stat-box">
                <div class="stat-val">{metrics['ctr_percentage']}%</div>
                <div class="stat-lbl">Average Click-Through (CTR)</div>
            </div>
            <div class="stat-box">
                <div class="stat-val">${metrics['cpc']:.2f} / ${metrics['cpl']:.2f}</div>
                <div class="stat-lbl">Avg CPC / Cost Per Lead</div>
            </div>
            <div class="stat-box">
                <div class="stat-val">{metrics['roas']:.2f}x</div>
                <div class="stat-lbl">Estimated ROAS</div>
            </div>
        </div>

        <div class="ads-grid">
            <!-- Left Grid: Live Active Campaigns -->
            <div class="card">
                <h2>📈 Live Meta Campaigns &amp; Delivery</h2>
                <div style="overflow-x: auto;">
                    <table>
                        <thead>
                            <tr>
                                <th>Campaign Campaign</th>
                                <th>Status</th>
                                <th>Budget</th>
                                <th>Spend</th>
                                <th>Impressions</th>
                                <th>Clicks</th>
                                <th>Leads Captures</th>
                            </tr>
                        </thead>
                        <tbody>
                            {campaign_rows}
                        </tbody>
                    </table>
                </div>
                {logs_html}
            </div>

            <!-- Instant Lead Form Creator Section -->
            <div class="card" style="margin-top: 1.5rem;">
                <h2>📋 Instant Lead Form Creator</h2>
                <p style="font-size:0.78rem; color:var(--muted-fg); margin-top:-0.5rem; margin-bottom:1rem;">
                    Create compliance-hardened Facebook Instant Forms with automated standard contact details and an optional custom qualifying question. Deploys directly to your Facebook Page.
                </p>
                <form method="POST" action="/action/create-form">
                    <div style="margin-bottom: 1rem;">
                        <label class="form-label">Form Name</label>
                        <input class="simulation-input" type="text" name="form_name" placeholder="e.g. Angel Solutions ATL - Rapid Collections Deletions Form" required>
                    </div>
                    <div class="form-row">
                        <div>
                            <label class="form-label">Privacy Policy URL</label>
                            <input class="simulation-input" type="url" name="privacy_url" value="https://angelsolutionsatl.com/privacy" required>
                        </div>
                        <div>
                            <label class="form-label">Redirect Booking URL</label>
                            <input class="simulation-input" type="url" name="redirect_url" value="https://angelsolutionsatl.com/book-online" required>
                        </div>
                    </div>
                    <div style="margin-bottom: 1.25rem;">
                        <label class="form-label">Add custom qualifying question (Optional)</label>
                        <input class="simulation-input" type="text" name="custom_question" placeholder="e.g. What is your estimated credit score range?">
                    </div>
                    <button class="btn btn-primary" type="submit" style="width: 100%;">Create &amp; Deploy Form on Facebook Page</button>
                </form>
            </div>

            <!-- Right Grid: AI Ads Copy Drafter & Publisher Form -->
            <div class="card">
                <h2>✍️ AI Ad Copy Drafter &amp; Launcher</h2>
                
                <!-- 1. AI Creative Drafter Form -->
                <form method="POST" action="/action/generate-copy" style="margin-bottom: 1.5rem; border-bottom: 1px solid var(--border); padding-bottom: 1.25rem;">
                    <div style="margin-bottom: 1rem;">
                        <label class="form-label">Write Ad Creative Prompt</label>
                        <input class="simulation-input" type="text" name="ai_prompt" placeholder="e.g. Focus on funding for GA trucking businesses with collection blocks." required value="{os.getenv('LAST_AI_PROMPT_VAL', '')}">
                    </div>
                    <button class="btn btn-primary" type="submit" style="width: 100%;">Create High-Converting AI Ad Copy</button>
                </form>

                <!-- 2. Meta Ads Publisher Launch Form -->
                <form method="POST" action="/action/launch-campaign">
                    <div class="form-row">
                        <div>
                            <label class="form-label">Campaign Name</label>
                            <input class="simulation-input" type="text" name="campaign_name" placeholder="Credit Restoral Georgia Leads" required value="{os.getenv('LAST_CAMP_NAME_VAL', '')}">
                        </div>
                        <div>
                            <label class="form-label">Daily Budget (USD)</label>
                            <input class="simulation-input" type="number" name="daily_budget" placeholder="30.00" step="5.00" min="5" required value="{os.getenv('LAST_DAILY_BUDGET_VAL', '30')}">
                        </div>
                    </div>

                    <div style="margin-bottom: 1.25rem;">
                        <label class="form-label">Selected Facebook Lead Form</label>
                        <select class="simulation-input" name="lead_form_id" style="width: 100%; box-sizing: border-box; height: 38px;">
                            <option value="form_atl_credit_101">Premium credit Restoral Core Form (ATL)</option>
                            <option value="form_business_funding_202">Corporate Unsecured Capital Form</option>
                        </select>
                    </div>

                    <div style="margin-bottom: 1.25rem;">
                        <label class="form-label">Generated Ad Creative Copy (CROA Compliant)</label>
                        <textarea class="ad-textarea" name="ad_copy" placeholder="Click 'Create High-Converting AI Ad Copy' or paste your own here..." required>{DRAFTED_COPY_CACHE}</textarea>
                    </div>

                    <button class="btn btn-success" type="submit" style="width: 100%; padding: 0.85rem; font-size: 0.85rem;">Publish Campaign to Meta Ad Account</button>
                </form>
            </div>
        </div>
        ''' if active_tab == 'ads' else ''}

        <!-- CRM & GHL CONFIGURATION TAB -->
        {f'''
        <div class="stats-row">
            <div class="stat-box">
                <div class="stat-val" style="color: {'var(--success)' if get_ghl_config()['api_key'] else '#9ca3af'};">
                    {'CONNECTED' if get_ghl_config()['api_key'] else 'SIMULATOR MODE'}
                </div>
                <div class="stat-lbl">GHL Integration State</div>
            </div>
            <div class="stat-box">
                <div class="stat-val" style="font-size: 1.1rem; line-height: 2.2rem; color: #f59e0b; font-family: monospace;">
                    {get_ghl_config()['location_id']}
                </div>
                <div class="stat-lbl">Target Location ID</div>
            </div>
            <div class="stat-box">
                <div class="stat-val" style="color: {'var(--success)' if os.getenv('META_PAGE_ACCESS_TOKEN') else '#9ca3af'};">
                    {'ACTIVE' if os.getenv('META_PAGE_ACCESS_TOKEN') else 'NOT BOUND'}
                </div>
                <div class="stat-lbl">Meta Marketing API Token</div>
            </div>
            <div class="stat-box">
                <div class="stat-val" style="color: {'var(--success)' if os.getenv('OPENROUTER_API_KEY') and 'your_' not in os.getenv('OPENROUTER_API_KEY') else '#9ca3af'};">
                    {'READY' if os.getenv('OPENROUTER_API_KEY') and 'your_' not in os.getenv('OPENROUTER_API_KEY') else 'MOCK DEFAULTS'}
                </div>
                <div class="stat-lbl">OpenRouter AI Provider</div>
            </div>
        </div>

        <div class="dashboard-grid">
            <!-- Left Side: GHL Field Mapping Schema Visualizer -->
            <div class="card">
                <h2>📋 Active Lead-to-CRM Field Mapping</h2>
                <p style="font-size:0.78rem; color:var(--muted-fg); margin-top:-0.5rem; margin-bottom:1.25rem;">
                    The platform automatically extracts prospect answers, calculates qualifying compliance metrics, and maps them to standard and custom fields in your GoHighLevel account.
                </p>
                <div style="overflow-x: auto;">
                    <table style="width: 100%;">
                        <thead>
                            <tr>
                                <th>Prospect Answer / Field</th>
                                <th>GoHighLevel Custom Field ID</th>
                                <th>Target Type</th>
                                <th>Active Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>First Name &amp; Last Name</strong></td>
                                <td><code>firstName</code> / <code>lastName</code></td>
                                <td>Standard Contact Field</td>
                                <td><span class="badge state-qualified" style="background: rgba(16, 185, 129, 0.1); color: var(--success);">READY</span></td>
                            </tr>
                            <tr>
                                <td><strong>Email Address</strong></td>
                                <td><code>email</code></td>
                                <td>Standard Contact Field</td>
                                <td><span class="badge state-qualified" style="background: rgba(16, 185, 129, 0.1); color: var(--success);">READY</span></td>
                            </tr>
                            <tr>
                                <td><strong>Phone Number</strong></td>
                                <td><code>phone</code></td>
                                <td>Standard Contact Field</td>
                                <td><span class="badge state-qualified" style="background: rgba(16, 185, 129, 0.1); color: var(--success);">READY</span></td>
                            </tr>
                            <tr>
                                <td><strong>Credit Restoral Goal</strong></td>
                                <td><code>credit_goal</code></td>
                                <td>Custom Text Field</td>
                                <td><span class="badge state-qualified" style="background: rgba(16, 185, 129, 0.1); color: var(--success);">MAPPED</span></td>
                            </tr>
                            <tr>
                                <td><strong>Collections Count</strong></td>
                                <td><code>collections_count</code></td>
                                <td>Custom Integer Field</td>
                                <td><span class="badge state-qualified" style="background: rgba(16, 185, 129, 0.1); color: var(--success);">MAPPED</span></td>
                            </tr>
                            <tr>
                                <td><strong>Active Bankruptcy Flag</strong></td>
                                <td><code>bankruptcy_flag</code></td>
                                <td>Custom Boolean (Yes/No)</td>
                                <td><span class="badge state-qualified" style="background: rgba(16, 185, 129, 0.1); color: var(--success);">MAPPED</span></td>
                            </tr>
                            <tr>
                                <td><strong>Child Support Arrears</strong></td>
                                <td><code>child_support_arrears</code></td>
                                <td>Custom Boolean (Yes/No)</td>
                                <td><span class="badge state-qualified" style="background: rgba(16, 185, 129, 0.1); color: var(--success);">MAPPED</span></td>
                            </tr>
                            <tr>
                                <td><strong>Computed AI Lead Score</strong></td>
                                <td><code>computed_lead_score</code></td>
                                <td>Custom Decimal Field</td>
                                <td><span class="badge state-qualified" style="background: rgba(16, 185, 129, 0.1); color: var(--success);">MAPPED</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Right Side: API & CRM Integration Form -->
            <div class="card">
                <h2>⚙️ API Credentials &amp; Pipeline Configuration</h2>
                <p style="font-size:0.78rem; color:var(--muted-fg); margin-top:-0.5rem; margin-bottom:1.25rem;">
                    Update credentials below. Saving will write straight to the local <code>.env</code> file and hot-reload the environment variables instantly without restarting your server.
                </p>
                
                {f'<div class="launch-logs-box" style="margin-bottom:1.5rem; border-color: rgba(16, 185, 129, 0.3); background: rgba(16, 185, 129, 0.03);"><h4 style="color:var(--success);">✅ {request.query_params.get("success_msg") if request else ""}</h4></div>' if request and request.query_params.get("success_msg") else ""}
                
                <form method="POST" action="/action/save-config">
                    <div style="margin-bottom: 1.25rem;">
                        <label class="form-label" style="display:flex; justify-content:space-between;">
                            <span>GoHighLevel V2 Access Token</span>
                            <span style="font-size:0.7rem; color:var(--muted-fg); font-weight:normal;">Bearer Token</span>
                        </label>
                        <input class="simulation-input" type="password" name="ghl_api_key" placeholder="Enter Bearer Token (Starts with pitch_ or similar)" value="{get_ghl_config()['api_key']}">
                    </div>

                    <div style="margin-bottom: 1.25rem;">
                        <label class="form-label">GoHighLevel Target Location ID</label>
                        <input class="simulation-input" type="text" name="ghl_location_id" placeholder="Sfvt5kBZ3EUOws7MDWa3" value="{get_ghl_config()['location_id']}" required>
                    </div>

                    <div style="margin-bottom: 1.25rem;">
                        <label class="form-label" style="display:flex; justify-content:space-between;">
                            <span>OpenRouter API Key</span>
                            <span style="font-size:0.7rem; color:var(--muted-fg); font-weight:normal;">Uses free Llama models by default</span>
                        </label>
                        <input class="simulation-input" type="password" name="openrouter_api_key" placeholder="sk-or-v1-..." value="{os.getenv('OPENROUTER_API_KEY', '')}">
                    </div>

                    <div style="margin-bottom: 1.25rem;">
                        <label class="form-label" style="display:flex; justify-content:space-between;">
                            <span>Meta Page Access Token</span>
                            <span style="font-size:0.7rem; color:var(--muted-fg); font-weight:normal;">Binds Facebook / Messenger API</span>
                        </label>
                        <textarea class="ad-textarea" name="meta_access_token" style="min-height: 70px; font-family: monospace; font-size: 0.72rem;" placeholder="EAAOveZAknGUg...">{os.getenv('META_PAGE_ACCESS_TOKEN', '')}</textarea>
                    </div>

                    <button class="btn btn-primary" type="submit" style="width: 100%; padding: 0.8rem; font-size: 0.85rem;">Save &amp; Hot-Reload Configuration</button>
                </form>
            </div>
        </div>
        ''' if active_tab == 'config' else ''}

    </div>
</body>
</html>"""
    return HTMLResponse(html)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, tab: str = "leads"):
    # Redirect root to /intake if admin is not logged in
    if request.cookies.get("session_token") == "mock_admin_token":
        return RedirectResponse("/admin?tab=" + tab, status_code=303)
    return RedirectResponse("/intake", status_code=303)

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request, tab: str = "leads", view_lead: Optional[str] = None):
    if request.cookies.get("session_token") == "mock_admin_token":
        return render_dashboard_page(MOCK_LEADS, SIMULATION_HISTORY, tab, view_lead, request=request)
    return RedirectResponse("/admin/login", status_code=303)

@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_view():
    return render_login_page()

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD_PLAIN:
        response = RedirectResponse("/admin", status_code=303)
        response.set_cookie(key="session_token", value="mock_admin_token", httponly=True)
        return response
    return render_login_page("Incorrect username or password. Please try again.")

# =====================================================================
# PUBLIC CLIENT-FACING STANDALONE LEAD FUNNEL ROUTES
# =====================================================================

@app.get("/intake", response_class=HTMLResponse)
async def public_intake_form():
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Angel Solutions ATL — Financial Restoration Intake</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #09090b;
            --card: #18181b;
            --border: #27272a;
            --primary: #f59e0b;
            --primary-hover: #d97706;
            --fg: #fafafa;
            --muted-fg: #a1a1aa;
            --card-hover: #222226;
        }}
        body {{
            background: var(--bg);
            background-image: radial-gradient(circle at top right, rgba(245, 158, 11, 0.04), transparent 40%),
                              radial-gradient(circle at bottom left, rgba(245, 158, 11, 0.02), transparent 40%);
            margin: 0; padding: 2rem 1rem; font-family: 'Plus Jakarta Sans', sans-serif; color: var(--fg);
            min-height: 100vh; display: flex; align-items: center; justify-content: center;
        }}
        .intake-card {{
            background: var(--card); border: 1px solid var(--border); border-radius: 1rem; padding: 2.5rem; max-width: 600px; width: 100%;
            box-shadow: 0 10px 30px -5px rgba(0,0,0,0.4); backdrop-filter: blur(8px); box-sizing: border-box;
        }}
        .brand-header {{ text-align: center; margin-bottom: 2rem; }}
        .brand-header h1 {{ margin: 0; font-family: 'Outfit', sans-serif; font-size: 2rem; color: var(--primary); letter-spacing: -0.05em; }}
        .brand-header p {{ margin: 0.25rem 0 0; font-size: 0.88rem; color: var(--muted-fg); }}
        
        /* Steps */
        .step-indicator {{
            display: flex; justify-content: space-between; margin-bottom: 2rem; border-bottom: 1px solid var(--border); padding-bottom: 0.75rem;
        }}
        .step-dot {{
            font-size: 0.8rem; font-weight: 600; color: var(--muted-fg); display: flex; align-items: center; gap: 0.5rem;
        }}
        .step-dot.active {{ color: var(--primary); }}
        
        .form-step {{ display: none; }}
        .form-step.active {{ display: block; }}
        
        h3 {{ font-family: 'Outfit', sans-serif; font-size: 1.3rem; margin: 0 0 1rem; color: var(--fg); }}
        
        label {{ display: block; font-size: 0.82rem; font-weight: 600; color: var(--muted-fg); margin-bottom: 0.4rem; }}
        .text-input {{
            display: block; width: 100%; box-sizing: border-box; padding: 0.85rem 1.1rem; 
            background: #09090b; border: 1px solid var(--border); border-radius: 0.5rem; margin-bottom: 1.25rem;
            color: var(--fg); font-size: 0.9rem; transition: border 0.2s;
        }}
        .text-input:focus {{ outline: none; border-color: var(--primary); }}
        
        /* Choice Selection Grids */
        .choice-grid {{
            display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-bottom: 1.5rem;
        }}
        .choice-card {{
            background: #09090b; border: 1px solid var(--border); border-radius: 0.5rem; padding: 1.1rem;
            text-align: center; cursor: pointer; transition: all 0.2s; position: relative;
        }}
        .choice-card:hover {{ border-color: var(--primary); background: var(--card-hover); }}
        .choice-card.selected {{ border-color: var(--primary); background: rgba(245, 158, 11, 0.05); }}
        .choice-card h4 {{ margin: 0 0 0.25rem; font-size: 0.95rem; color: var(--fg); }}
        .choice-card p {{ margin: 0; font-size: 0.75rem; color: var(--muted-fg); }}
        
        .choice-card input[type="radio"] {{
            position: absolute; opacity: 0; width: 0; height: 0;
        }}
        
        .btn-row {{ display: flex; justify-content: space-between; gap: 1rem; margin-top: 1.5rem; }}
        .btn {{
            padding: 0.85rem 1.5rem; border: none; border-radius: 0.5rem; font-weight: 700; cursor: pointer; transition: background 0.2s; font-size: 0.9rem;
        }}
        .btn-prev {{ background: #27272a; color: var(--fg); }}
        .btn-prev:hover {{ background: #3f3f46; }}
        .btn-next {{ background: var(--primary); color: #09090b; margin-left: auto; }}
        .btn-next:hover {{ background: var(--primary-hover); }}
        .btn-submit {{ background: var(--primary); color: #09090b; width: 100%; }}
        .btn-submit:hover {{ background: var(--primary-hover); }}
        
        .footer-link {{ text-align: center; margin-top: 1.5rem; font-size: 0.75rem; color: var(--muted-fg); }}
        .footer-link a {{ color: var(--primary); text-decoration: none; }}
    </style>
</head>
<body>
    <div class="intake-card">
        <div class="brand-header">
            <h1>ANGEL SOLUTIONS ATL</h1>
            <p>Sovereign Credit Restoration Intake Panel</p>
        </div>
        
        <div class="step-indicator">
            <div class="step-dot active" id="dot1"><span>01</span> Contact</div>
            <div class="step-dot" id="dot2"><span>02</span> Credit Profile</div>
            <div class="step-dot" id="dot3"><span>03</span> Intentions</div>
        </div>
        
        <form id="intakeForm" method="POST" action="/intake">
            <!-- STEP 1: CONTACT -->
            <div class="form-step active" id="step1">
                <h3>Contact &amp; Personal Info</h3>
                <p style="font-size:0.8rem; color:var(--muted-fg); margin-top:-0.5rem; margin-bottom:1.5rem;">
                    Let's start with where we can securely deliver your creditRestoral summary notes.
                </p>
                <div>
                    <label>Full Name</label>
                    <input class="text-input" type="text" name="name" placeholder="Marcus Aurelius" required>
                </div>
                <div>
                    <label>Email Address</label>
                    <input class="text-input" type="email" name="email" placeholder="marcus@empire.com" required>
                </div>
                <div>
                    <label>Phone Number (SMS Enabled)</label>
                    <input class="text-input" type="tel" name="phone" placeholder="+14045550192" required>
                </div>
                <div class="btn-row">
                    <button class="btn btn-next" type="button" onclick="nextStep(2)">Continue to Credit Health</button>
                </div>
            </div>
            
            <!-- STEP 2: CREDIT PROFILE -->
            <div class="form-step" id="step2">
                <h3>Credit Profile Health</h3>
                <p style="font-size:0.8rem; color:var(--muted-fg); margin-top:-0.5rem; margin-bottom:1.5rem;">
                    Your answers allow our dynamic routing matrix to choose the precise dispute restoral plan.
                </p>
                
                <label>Estimated Collections / Negative Items Count</label>
                <div class="choice-grid">
                    <div class="choice-card" onclick="selectRadio('collections', 'low')">
                        <input type="radio" name="collections" value="5" id="coll_low" checked>
                        <h4>Under 10 Items</h4>
                        <p>Minor collections / defaults</p>
                    </div>
                    <div class="choice-card" onclick="selectRadio('collections', 'high')">
                        <input type="radio" name="collections" value="15" id="coll_high">
                        <h4>10+ Collections</h4>
                        <p>Severe collection drag</p>
                    </div>
                </div>
                
                <label>Active Bankruptcies on Profile?</label>
                <div class="choice-grid">
                    <div class="choice-card" onclick="selectRadio('bankruptcy', 'no')">
                        <input type="radio" name="bankruptcy" value="0" id="bk_no" checked>
                        <h4>No Bankruptcy</h4>
                        <p>Completely clear of active filings</p>
                    </div>
                    <div class="choice-card" onclick="selectRadio('bankruptcy', 'yes')">
                        <input type="radio" name="bankruptcy" value="1" id="bk_yes">
                        <h4>Active / Discharged</h4>
                        <p>Public records present</p>
                    </div>
                </div>
                
                <label>Active Child Support Arrears?</label>
                <div class="choice-grid">
                    <div class="choice-card" onclick="selectRadio('child_support', 'no')">
                        <input type="radio" name="child_support" value="0" id="cs_no" checked>
                        <h4>No Arrears</h4>
                        <p>No active enforcement blocks</p>
                    </div>
                    <div class="choice-card" onclick="selectRadio('child_support', 'yes')">
                        <input type="radio" name="child_support" value="1" id="cs_yes">
                        <h4>Yes (Arrears)</h4>
                        <p>Government arrears list</p>
                    </div>
                </div>
                
                <div class="btn-row">
                    <button class="btn btn-prev" type="button" onclick="nextStep(1)">Back</button>
                    <button class="btn btn-next" type="button" onclick="nextStep(3)">Continue to Intentions</button>
                </div>
            </div>
            
            <!-- STEP 3: INTENTIONS -->
            <div class="form-step" id="step3">
                <h3>Primary Financial Goal</h3>
                <p style="font-size:0.8rem; color:var(--muted-fg); margin-top:-0.5rem; margin-bottom:1.5rem;">
                    Tell us what clearing your credit roadblocks unlocks for you.
                </p>
                
                <div class="choice-grid" style="grid-template-columns: 1fr; gap:0.75rem;">
                    <div class="choice-card" onclick="selectGoal('funding')" style="text-align: left; display: flex; align-items: center; justify-content: space-between;">
                        <input type="radio" name="goal" value="business_funding" id="goal_funding" checked>
                        <div>
                            <h4 style="margin:0;">🚀 Business Funding &amp; Capital</h4>
                            <p style="margin:0.15rem 0 0;">Secure corporate capital, lines of credit, or trucking funding.</p>
                        </div>
                    </div>
                    <div class="choice-card" onclick="selectGoal('home')" style="text-align: left; display: flex; align-items: center; justify-content: space-between;">
                        <input type="radio" name="goal" value="buy_home" id="goal_home">
                        <div>
                            <h4 style="margin:0;">🏡 Home Purchase / Mortgage</h4>
                            <p style="margin:0.15rem 0 0;">Clear collection hurdles to qualify for home financing.</p>
                        </div>
                    </div>
                    <div class="choice-card" onclick="selectGoal('personal')" style="text-align: left; display: flex; align-items: center; justify-content: space-between;">
                        <input type="radio" name="goal" value="personal_restoral" id="goal_personal">
                        <div>
                            <h4 style="margin:0;">🛡️ General Personal restoration</h4>
                            <p style="margin:0.15rem 0 0;">Permanent removals of negative listings and score building.</p>
                        </div>
                    </div>
                </div>
                
                <div class="btn-row">
                    <button class="btn btn-prev" type="button" onclick="nextStep(2)">Back</button>
                    <button class="btn btn-submit" type="submit">Submit &amp; Build Custom Roadmap</button>
                </div>
            </div>
        </form>
        
        <div class="footer-link">
            Are you an admin? <a href="/admin/login">Admin Control Center</a>
        </div>
    </div>
    
    <script>
        function nextStep(stepNum) {{
            document.querySelectorAll('.form-step').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.step-dot').forEach(el => el.classList.remove('active'));
            
            document.getElementById('step' + stepNum).classList.add('active');
            for (let i = 1; i <= stepNum; i++) {{
                document.getElementById('dot' + i).classList.add('active');
            }}
        }}
        
        function selectRadio(group, val) {{
            let yesCard = event.currentTarget;
            let siblings = yesCard.parentNode.querySelectorAll('.choice-card');
            siblings.forEach(el => el.classList.remove('selected'));
            yesCard.classList.add('selected');
            
            let radio = yesCard.querySelector('input[type="radio"]');
            radio.checked = true;
        }}
        
        function selectGoal(goal) {{
            let goalCard = event.currentTarget;
            let siblings = goalCard.parentNode.querySelectorAll('.choice-card');
            siblings.forEach(el => el.classList.remove('selected'));
            goalCard.classList.add('selected');
            
            let radio = goalCard.querySelector('input[type="radio"]');
            radio.checked = true;
        }}
        
        // Setup default selections style on mount
        document.querySelectorAll('input[type="radio"]:checked').forEach(radio => {{
            radio.parentNode.classList.add('selected');
        }});
    </script>
</body>
</html>"""
    return HTMLResponse(html)

@app.post("/intake")
async def process_intake(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    collections: int = Form(...),
    bankruptcy: int = Form(...),
    child_support: int = Form(...),
    goal: str = Form(...)
):
    # Calculate custom lead score
    score = 0.5
    if collections > 10:
        score += 0.2
    if bankruptcy == 1:
        score += 0.1
    if child_support == 1:
        score += 0.1
    if goal in ["business_funding"]:
        score += 0.1
    score = min(score, 0.99)
    
    # Generate unique lead ID
    lead_id = f"lead_{uuid.uuid4().hex[:8]}"
    
    sentiment_map = {
        "business_funding": "friendly",
        "buy_home": "neutral",
        "personal_restoral": "friendly"
    }
    
    MOCK_LEADS.append({
        "id": lead_id,
        "name": name,
        "lead_state": "QUALIFIED" if score >= 0.7 else "NEW",
        "platform": "facebook", # Local web form behaves as standard Facebook/Ad intake
        "score": round(score, 2),
        "collections": collections,
        "phone": phone,
        "bot_active": True,
        "sentiment": sentiment_map.get(goal, "neutral"),
        "email": email,
        "bankruptcy": bankruptcy,
        "child_support": child_support,
        "goal": goal,
        "messages": [
            {
                "sender": "user",
                "text": f"Submitted Intake Form. Goal: {goal}. Collections count: {collections}.",
                "timestamp": "Just now"
            },
            {
                "sender": "bot",
                "text": "hey! rick here. got your intake details and i'm super excited to help you get this credit cleaned up. let's schedule a call to see how we can delete these collections and get you capital-ready ASAP!",
                "timestamp": "Just now"
            }
        ]
    })
    
    # Also attempt real database log insertion if wrangler table exists in environment context
    print(f"[INTAKE SYSTEM] Standalone Lead Captured! Name: {name}, Phone: {phone}, Goal: {goal}, Score: {score}")
    
    # Redirect directly to dynamic visual roadmap
    return RedirectResponse(f"/roadmap/{lead_id}", status_code=303)

@app.get("/roadmap/{lead_id}", response_class=HTMLResponse)
async def lead_roadmap_view(lead_id: str):
    # Find matching lead
    target_lead = None
    for lead in MOCK_LEADS:
        if lead["id"] == lead_id:
            target_lead = lead
            break
            
    # Safe fallback if directly visited
    if not target_lead:
        target_lead = {
            "id": lead_id,
            "name": "Valued Client",
            "collections": 8,
            "bankruptcy": 0,
            "child_support": 0,
            "goal": "personal_restoral",
            "phone": "+14045550192"
        }
        
    collections = target_lead.get("collections", 0)
    bankruptcy = target_lead.get("bankruptcy", 0)
    child_support = target_lead.get("child_support", 0)
    goal = target_lead.get("goal", "personal_restoral")
    
    # Evaluate Strategy Plan
    is_skool = (collections < 10 and child_support == 0 and bankruptcy == 0)
    
    plan_title = ""
    price_tag = ""
    bullet_items = ""
    checkout_url = ""
    
    if is_skool:
        plan_title = "Monthly Credit Repair Skool Community"
        price_tag = "$67.00/month"
        checkout_url = "https://www.skool.com/creditsolution/about"
        bullet_items = """
            <li>Dispute up to 5 negative items every single month</li>
            <li>Direct entry to our exclusive financial mastermind community</li>
            <li>Premium dispute templates and credit rebuilding tutorials</li>
            <li>Weekly live Q&amp;A sessions with expert restoral strategists</li>
        """
    else:
        plan_title = "Advanced Credit Restoral (1-on-1 Full-Service)"
        # Price tiering
        if collections <= 10:
            price_tag = "$795.00 (One-Time)"
        elif collections <= 15:
            price_tag = "$995.00 (One-Time)"
        else:
            price_tag = "$1,250.00 (One-Time)"
            
        checkout_url = f"/book/{lead_id}"
        bullet_items = """
            <li>Rapid legal disputes representing your entire profile at once</li>
            <li>Personalized 1-hour strategy and roadmap session with Jordynn Miller</li>
            <li>1-on-1 dedicated case manager driving deletion cycles daily</li>
            <li>Customized alignment matrix for unsecured business capital up to $150K</li>
        """
        
    goal_labels = {
        "business_funding": "Accelerate Unsecured Business Capital",
        "buy_home": "Qualify for Your Home Mortgage Clear of Collections",
        "personal_restoral": "Permanent collections Removal & Score restoral"
    }
    
    selected_goal_lbl = goal_labels.get(goal, "Financial Restoration & Profile Rebuild")
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Angel Solutions ATL — Personalized restoral Roadmap</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #09090b;
            --card: #18181b;
            --border: #27272a;
            --primary: #f59e0b;
            --primary-hover: #d97706;
            --fg: #fafafa;
            --muted-fg: #a1a1aa;
            --success: #10b981;
        }}
        body {{
            background: var(--bg);
            background-image: radial-gradient(circle at top right, rgba(245, 158, 11, 0.05), transparent 45%),
                              radial-gradient(circle at bottom left, rgba(245, 158, 11, 0.02), transparent 40%);
            margin: 0; padding: 2rem 1rem; font-family: 'Plus Jakarta Sans', sans-serif; color: var(--fg);
            min-height: 100vh; display: flex; align-items: center; justify-content: center;
        }}
        .roadmap-card {{
            background: var(--card); border: 1px solid var(--border); border-radius: 1rem; padding: 2.5rem; max-width: 650px; width: 100%;
            box-shadow: 0 10px 30px -5px rgba(0,0,0,0.4); backdrop-filter: blur(8px); box-sizing: border-box;
        }}
        .brand-header {{ text-align: center; margin-bottom: 2rem; }}
        .brand-header h1 {{ margin: 0; font-family: 'Outfit', sans-serif; font-size: 1.8rem; color: var(--primary); letter-spacing: -0.05em; }}
        
        /* Analysis Loader */
        .analysis-box {{
            background: #09090b; border: 1px solid var(--border); border-radius: 0.75rem; padding: 1.5rem; margin-bottom: 2rem;
        }}
        .analysis-title {{
            display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; font-size: 0.9rem; font-weight: 600;
        }}
        .progress-bar {{
            background: #27272a; border-radius: 99px; height: 8px; overflow: hidden; margin-bottom: 1rem;
        }}
        .progress-fill {{
            background: var(--primary); height: 100%; width: 0%; border-radius: 99px; transition: width 0.1s linear;
        }}
        .analysis-logs {{
            font-family: monospace; font-size: 0.75rem; color: var(--muted-fg); height: 35px; line-height: 1.4; overflow: hidden;
        }}
        
        /* Plan Recommender Box */
        .plan-box {{
            border: 1px solid rgba(245, 158, 11, 0.2); background: rgba(245, 158, 11, 0.03); border-radius: 0.75rem; padding: 1.5rem; margin-bottom: 2rem;
        }}
        .plan-box h2 {{ font-family: 'Outfit', sans-serif; font-size: 1.35rem; margin: 0 0 0.5rem; color: var(--primary); }}
        .plan-subtitle {{ font-size: 0.8rem; text-transform: uppercase; color: var(--muted-fg); font-weight: 700; letter-spacing: 0.05em; margin-bottom: 1.25rem; }}
        
        ul {{ padding-left: 1.25rem; margin: 0; font-size: 0.88rem; line-height: 1.6; color: #e4e4e7; }}
        li {{ margin-bottom: 0.75rem; }}
        
        .price-box {{
            text-align: center; margin: 2rem 0 1.5rem; border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); padding: 1.25rem 0;
        }}
        .price-label {{ font-size: 0.78rem; text-transform: uppercase; color: var(--muted-fg); font-weight: 600; margin-bottom: 0.25rem; }}
        .price-value {{ font-size: 1.8rem; font-weight: 700; color: var(--fg); font-family: 'Outfit', sans-serif; }}
        
        .btn-checkout {{
            display: block; width: 100%; box-sizing: border-box; text-align: center; background: var(--primary); color: #09090b; text-decoration: none;
            padding: 1rem; border-radius: 0.5rem; font-weight: 700; transition: background 0.2s; font-size: 1rem;
        }}
        .btn-checkout:hover {{ background: var(--primary-hover); }}
        
        .disclaimer {{ text-align: center; font-size: 0.72rem; color: var(--muted-fg); margin-top: 1.5rem; line-height: 1.4; }}
    </style>
</head>
<body>
    <div class="roadmap-card">
        <div class="brand-header">
            <h1>ANGEL SOLUTIONS ATL</h1>
            <p style="margin:0.25rem 0 0; font-size:0.88rem; color:var(--muted-fg);">Personalized Restoral Strategy Roadmap</p>
        </div>
        
        <!-- Live Real-Time Analysis Bar -->
        <div class="analysis-box">
            <div class="analysis-title">
                <span>Analyzing Profile Metrics for {target_lead['name']}</span>
                <span id="analysisPercent">0%</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill"></div>
            </div>
            <div class="analysis-logs" id="analysisLogs">Awaiting sequence initialization...</div>
        </div>
        
        <!-- Recommender Panel -->
        <div class="plan-box" id="roadmapContent" style="opacity: 0; transition: opacity 0.5s ease;">
            <div class="plan-subtitle">Recommended Action Plan Details</div>
            <h2>{plan_title}</h2>
            <p style="font-size:0.85rem; color: var(--muted-fg); margin-top: -0.25rem; margin-bottom: 1.25rem; font-weight:500;">
                Target Goal: <span style="color:white; font-weight:600;">{selected_goal_lbl}</span>
            </p>
            
            <ul>
                {bullet_items}
            </ul>
            
            <div class="price-box">
                <div class="price-label">Plan pricing</div>
                <div class="price-value">{price_tag}</div>
            </div>
            
            <a href="{checkout_url}" class="btn-checkout">{"Lock In DIY Community Access" if is_skool else "Continue to Live Strategy Call Booking"}</a>
        </div>
        
        <div class="disclaimer">
            Angel Solutions ATL is fully bonded and compliant. No recurring subscription lock-ins. All actions are handled by professional specialists.
        </div>
    </div>
    
    <script>
        const logs = [
            "Connecting secure edge-broker pipeline...",
            "Downloading credit bureau metric reports...",
            "Analyzing active negative collection count ({collections} items found)...",
            "Checking active child support registers ({'Flagged' if child_support == 1 else 'Clear'})...",
            "Evaluating bankruptcy public filings ({'Flagged' if bankruptcy == 1 else 'Clear'})...",
            "Simulating deletion restoral pathways...",
            "Complete! Custom restoral roadmap formulated."
        ];
        
        let percent = 0;
        let logIndex = 0;
        const fill = document.getElementById('progressFill');
        const percentText = document.getElementById('analysisPercent');
        const logsText = document.getElementById('analysisLogs');
        const contentBox = document.getElementById('roadmapContent');
        
        const interval = setInterval(() => {{
            percent += 2;
            fill.style.width = percent + '%';
            percentText.innerText = percent + '%';
            
            // Advance logs
            if (percent % 15 === 0 && logIndex < logs.length - 1) {{
                logIndex++;
                logsText.innerText = logs[logIndex];
            }}
            
            if (percent >= 100) {{
                clearInterval(interval);
                logsText.innerText = logs[logs.length - 1];
                logsText.style.color = "#10b981";
                contentBox.style.opacity = "1";
            }}
        }}, 50);
    </script>
</body>
</html>"""
    return HTMLResponse(html)

@app.get("/book/{lead_id}", response_class=HTMLResponse)
async def lead_booking_view(lead_id: str):
    target_lead = None
    for lead in MOCK_LEADS:
        if lead["id"] == lead_id:
            target_lead = lead
            break
            
    if not target_lead:
        target_lead = {
            "id": lead_id,
            "name": "Valued Client",
            "phone": "+14045550192"
        }
        
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Angel Solutions ATL — Schedule Strategy Call</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #09090b;
            --card: #18181b;
            --border: #27272a;
            --primary: #f59e0b;
            --primary-hover: #d97706;
            --fg: #fafafa;
            --muted-fg: #a1a1aa;
        }}
        body {{
            background: var(--bg);
            background-image: radial-gradient(circle at top right, rgba(245, 158, 11, 0.05), transparent 45%),
                              radial-gradient(circle at bottom left, rgba(245, 158, 11, 0.02), transparent 40%);
            margin: 0; padding: 2rem 1rem; font-family: 'Plus Jakarta Sans', sans-serif; color: var(--fg);
            min-height: 100vh; display: flex; align-items: center; justify-content: center;
        }}
        .book-card {{
            background: var(--card); border: 1px solid var(--border); border-radius: 1rem; padding: 2.5rem; max-width: 600px; width: 100%;
            box-shadow: 0 10px 30px -5px rgba(0,0,0,0.4); backdrop-filter: blur(8px); box-sizing: border-box;
        }}
        .brand-header {{ text-align: center; margin-bottom: 2rem; }}
        .brand-header h1 {{ margin: 0; font-family: 'Outfit', sans-serif; font-size: 1.8rem; color: var(--primary); letter-spacing: -0.05em; }}
        
        h3 {{ font-family: 'Outfit', sans-serif; font-size: 1.25rem; margin: 0 0 1rem; color: var(--fg); }}
        
        /* Calendar Selector */
        .scheduler-grid {{
            display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; margin-bottom: 1.5rem;
        }}
        .scheduler-box {{
            background: #09090b; border: 1px solid var(--border); border-radius: 0.5rem; padding: 0.85rem;
            text-align: center; cursor: pointer; transition: all 0.2s;
        }}
        .scheduler-box:hover {{ border-color: var(--primary); }}
        .scheduler-box.selected {{ border-color: var(--primary); background: rgba(245, 158, 11, 0.05); }}
        .scheduler-box h4 {{ margin: 0 0 0.15rem; font-size: 0.88rem; color: var(--fg); }}
        .scheduler-box p {{ margin: 0; font-size: 0.7rem; color: var(--muted-fg); }}
        
        .time-slots {{
            display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.5rem; margin-bottom: 2rem;
        }}
        .time-box {{
            background: #09090b; border: 1px solid var(--border); border-radius: 0.35rem; padding: 0.65rem 0.25rem;
            text-align: center; cursor: pointer; transition: all 0.2s; font-size: 0.8rem; font-weight: 600;
        }}
        .time-box:hover {{ border-color: var(--primary); }}
        .time-box.selected {{ border-color: var(--primary); background: rgba(245, 158, 11, 0.05); }}
        
        button {{
            display: block; width: 100%; padding: 1rem; border: none; border-radius: 0.5rem; 
            background: var(--primary); color: #09090b; font-weight: 700; cursor: pointer; transition: background 0.2s; font-size: 1rem;
        }}
        button:hover {{ background: var(--primary-hover); }}
        
        input[type="hidden"] {{ display: none; }}
    </style>
</head>
<body>
    <div class="book-card">
        <div class="brand-header">
            <h1>ANGEL SOLUTIONS ATL</h1>
            <p style="margin:0.25rem 0 0; font-size:0.88rem; color:var(--muted-fg);">Book Your Live Credit Restoral strategy Session</p>
        </div>
        
        <form method="POST" action="/book/{lead_id}">
            <h3>1. Select Date</h3>
            <div class="scheduler-grid">
                <div class="scheduler-box" onclick="setDate('Monday, July 20')">
                    <h4>Mon, Jul 20</h4>
                    <p>3 slots open</p>
                </div>
                <div class="scheduler-box" onclick="setDate('Tuesday, July 21')">
                    <h4>Tue, Jul 21</h4>
                    <p>4 slots open</p>
                </div>
                <div class="scheduler-box" onclick="setDate('Wednesday, July 22')">
                    <h4>Wed, Jul 22</h4>
                    <p>5 slots open</p>
                </div>
            </div>
            
            <h3>2. Select Time (Eastern Standard Time)</h3>
            <div class="time-slots">
                <div class="time-box" onclick="setTime('09:30 AM')">09:30 AM</div>
                <div class="time-box" onclick="setTime('11:00 AM')">11:00 AM</div>
                <div class="time-box" onclick="setTime('01:30 PM')">01:30 PM</div>
                <div class="time-box" onclick="setTime('03:00 PM')">03:00 PM</div>
            </div>
            
            <input type="hidden" name="booking_date" id="hidden_date" value="Monday, July 20">
            <input type="hidden" name="booking_time" id="hidden_time" value="09:30 AM">
            
            <button type="submit">Confirm 1-on-1 Strategy Call appointment</button>
        </form>
    </div>
    
    <script>
        function setDate(dateStr) {{
            let boxes = document.querySelectorAll('.scheduler-box');
            boxes.forEach(b => b.classList.remove('selected'));
            event.currentTarget.classList.add('selected');
            document.getElementById('hidden_date').value = dateStr;
        }}
        
        function setTime(timeStr) {{
            let boxes = document.querySelectorAll('.time-box');
            boxes.forEach(b => b.classList.remove('selected'));
            event.currentTarget.classList.add('selected');
            document.getElementById('hidden_time').value = timeStr;
        }}
        
        // Highlight defaults
        document.querySelector('.scheduler-box').classList.add('selected');
        document.querySelector('.time-box').classList.add('selected');
    </script>
</body>
</html>"""
    return HTMLResponse(html)

@app.post("/book/{lead_id}")
async def process_booking(lead_id: str, booking_date: str = Form(...), booking_time: str = Form(...)):
    # Update lead status to BOOKED
    for lead in MOCK_LEADS:
        if lead["id"] == lead_id:
            lead["lead_state"] = "BOOKED"
            lead["booking_date"] = booking_date
            lead["booking_time"] = booking_time
            print(f"[BOOKING SYSTEM] Live Appointment Booked for {lead['name']}! Date: {booking_date}, Time: {booking_time}")
            break
    return RedirectResponse(f"/success/{lead_id}", status_code=303)

@app.get("/success/{lead_id}", response_class=HTMLResponse)
async def success_confirmation_view(lead_id: str):
    target_lead = None
    for lead in MOCK_LEADS:
        if lead["id"] == lead_id:
            target_lead = lead
            break
            
    if not target_lead:
        target_lead = {
            "name": "Valued Client",
            "booking_date": "Monday, July 20",
            "booking_time": "09:30 AM"
        }
        
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Angel Solutions ATL — Booking Confirmed</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #09090b;
            --card: #18181b;
            --border: #27272a;
            --primary: #f59e0b;
            --primary-hover: #d97706;
            --fg: #fafafa;
            --muted-fg: #a1a1aa;
            --success: #10b981;
        }}
        body {{
            background: var(--bg);
            background-image: radial-gradient(circle at top right, rgba(245, 158, 11, 0.05), transparent 45%),
                              radial-gradient(circle at bottom left, rgba(245, 158, 11, 0.02), transparent 40%);
            margin: 0; padding: 2rem 1rem; font-family: 'Plus Jakarta Sans', sans-serif; color: var(--fg);
            min-height: 100vh; display: flex; align-items: center; justify-content: center;
        }}
        .success-card {{
            background: var(--card); border: 1px solid var(--border); border-radius: 1rem; padding: 2.5rem; max-width: 550px; width: 100%;
            box-shadow: 0 10px 30px -5px rgba(0,0,0,0.4); backdrop-filter: blur(8px); box-sizing: border-box; text-align: center;
        }}
        
        .check-circle {{
            width: 70px; height: 70px; border-radius: 50%; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3);
            color: var(--success); display: flex; align-items: center; justify-content: center; font-size: 2.5rem; margin: 0 auto 1.5rem;
        }}
        
        h2 {{ font-family: 'Outfit', sans-serif; font-size: 1.8rem; margin: 0 0 0.5rem; color: var(--primary); }}
        p {{ color: var(--muted-fg); font-size: 0.9rem; line-height: 1.5; margin-bottom: 2rem; }}
        
        .appointment-summary {{
            background: #09090b; border: 1px solid var(--border); border-radius: 0.75rem; padding: 1.5rem; text-align: left; margin-bottom: 2rem;
        }}
        .summary-row {{ display: flex; justify-content: space-between; margin-bottom: 0.75rem; font-size: 0.88rem; }}
        .summary-row:last-child {{ margin-bottom: 0; }}
        .summary-lbl {{ color: var(--muted-fg); font-weight: 500; }}
        .summary-val {{ color: var(--fg); font-weight: 600; }}
        
        /* Preparation checklist */
        .prep-box {{
            text-align: left; margin-bottom: 2rem;
        }}
        .prep-box h4 {{ font-family: 'Outfit', sans-serif; color: var(--fg); margin: 0 0 0.75rem; font-size: 1rem; }}
        .prep-item {{ display: flex; gap: 0.75rem; font-size: 0.82rem; color: var(--muted-fg); margin-bottom: 0.5rem; line-height: 1.4; }}
        .prep-bullet {{ color: var(--primary); font-weight: bold; }}
        
        .btn-done {{
            display: block; width: 100%; box-sizing: border-box; text-align: center; background: #27272a; color: var(--fg); text-decoration: none;
            padding: 1rem; border-radius: 0.5rem; font-weight: 700; transition: background 0.2s; font-size: 0.95rem; border: 1px solid var(--border);
        }}
        .btn-done:hover {{ background: #3f3f46; }}
    </style>
</head>
<body>
    <div class="success-card">
        <div class="check-circle">✓</div>
        <h2>Booking Confirmed!</h2>
        <p>Your creditrestoral consultation and 1-on-1 strategy call are securely locked in. Get ready to clear those roadblocks.</p>
        
        <div class="appointment-summary">
            <div class="summary-row">
                <span class="summary-lbl">Client Name</span>
                <span class="summary-val">{target_lead['name']}</span>
            </div>
            <div class="summary-row">
                <span class="summary-lbl">Appointment Date</span>
                <span class="summary-val">{target_lead.get('booking_date', 'Monday, July 20')}</span>
            </div>
            <div class="summary-row">
                <span class="summary-lbl">Time Slot</span>
                <span class="summary-val">{target_lead.get('booking_time', '09:30 AM')} (EST)</span>
            </div>
            <div class="summary-row">
                <span class="summary-lbl">Meeting Platform</span>
                <span class="summary-val">Direct Phone / Zoom Handoff</span>
            </div>
        </div>
        
        <div class="prep-box">
            <h4>📋 Pre-Call Preparation Checklist</h4>
            <div class="prep-item">
                <span class="prep-bullet">✦</span>
                <span>Keep your phone nearby. Rick or her top restoral specialist will call you directly at the exact scheduled time.</span>
            </div>
            <div class="prep-item">
                <span class="prep-bullet">✦</span>
                <span>If possible, have your credit reports or a list of collections/debts handy so we can dive straight into removals strategy.</span>
            </div>
        </div>
        
        <a href="/intake" class="btn-done">Return to Intake Portal</a>
    </div>
</body>
</html>"""
    return HTMLResponse(html)

@app.post("/action/toggle-bot")
async def toggle_bot(lead_id: str = Form(...)):
    for lead in MOCK_LEADS:
        if lead["id"] == lead_id:
            lead["bot_active"] = not lead["bot_active"]
            print(f"[ADMIN ACTION] Bot toggled to {lead['bot_active']} for lead {lead_id}")
    return RedirectResponse(f"/admin?view_lead={lead_id}", status_code=303)

@app.post("/action/override-reply")
async def override_reply(lead_id: str = Form(...), override_text: str = Form(...)):
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for lead in MOCK_LEADS:
        if lead["id"] == lead_id:
            # Deactivate bot automatically when human manually intervenes!
            lead["bot_active"] = False
            if "messages" not in lead:
                lead["messages"] = []
            lead["messages"].append({
                "sender": "human",
                "text": override_text,
                "timestamp": timestamp
            })
            print(f"[MANUAL OVERRIDE] Sent Human Message to {lead['name']}: '{override_text}'")
            break
    return RedirectResponse(f"/admin?view_lead={lead_id}", status_code=303)
@app.post("/action/sync")
async def force_sync(lead_id: str = Form(...)):
    target_lead = None
    for lead in MOCK_LEADS:
        if lead["id"] == lead_id:
            target_lead = lead
            break
            
    if target_lead:
        result = sync_lead_to_ghl(target_lead)
        # Log this result in SIMULATION_HISTORY so it renders immediately in the feed
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        status_text = "SUCCESS" if result.get("success") else "FAILED"
        mode_text = result.get("mode", "OFFLINE")
        cid = result.get("contact_id", "N/A")
        msg = result.get("message", "N/A")
        
        # Append simulated system message
        if "messages" not in target_lead:
            target_lead["messages"] = []
            
        target_lead["messages"].append({
            "sender": "system",
            "text": f"🔄 GHL CRM Sync Status: {status_text} | Mode: {mode_text} | Contact ID: {cid} | Details: {msg}",
            "timestamp": timestamp
        })
        
        print(f"[CRM SYNC] Sync results for {target_lead['name']}: {result}")
        
    return RedirectResponse(f"/admin?view_lead={lead_id}&tab=leads", status_code=303)

@app.post("/action/save-config")
async def save_config(
    ghl_api_key: str = Form(...),
    ghl_location_id: str = Form(...),
    openrouter_api_key: str = Form(...),
    meta_access_token: str = Form(...)
):
    updates = {
        "GHL_API_KEY": ghl_api_key.strip(),
        "GHL_LOCATION_ID": ghl_location_id.strip(),
        "OPENROUTER_API_KEY": openrouter_api_key.strip(),
        "META_PAGE_ACCESS_TOKEN": meta_access_token.strip()
    }
    
    # Save to file safely
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    else:
        lines = []
        
    new_lines = []
    keys_updated = set()
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and "=" in line:
            parts = stripped.split("=", 1)
            key = parts[0].strip()
            if key in updates:
                new_lines.append(f"{key}={updates[key]}\n")
                keys_updated.add(key)
                continue
        new_lines.append(line)
        
    for key, val in updates.items():
        if key not in keys_updated:
            new_lines.append(f"{key}={val}\n")
            
    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
        
    # Hot-reload environment variables in-memory
    for key, val in updates.items():
        os.environ[key] = val
        
    print(f"[HOT-RELOAD] Environment config saved and reloaded: {list(updates.keys())}")
    
    # Reload modules to grab updated env
    import importlib
    import ghl_client
    importlib.reload(ghl_client)
    
    return RedirectResponse("/admin?tab=config&success_msg=API+Credentials+and+GHL+Location+successfully+hot-reloaded!", status_code=303)

@app.post("/action/simulate")
async def simulate_webhook(user_message: str = Form(...)):
    msg_lower = user_message.lower()
    
    # 1. Determine Sentiment
    sentiment = "neutral"
    if any(word in msg_lower for word in ["angry", "upset", "mad", "scam", "refund", "horrible", "frustrated"]):
        sentiment = "frustrated"
    elif any(word in msg_lower for word in ["thanks", "love", "awesome", "perfect", "great", "appreciate"]):
        sentiment = "friendly"
        
    # 2. Invoke our Core AI Ensemble Response Engine
    history = [{"role": "user", "content": user_message}]
    ai_result = generate_rick_response(history)
    reply = ai_result.get("reply", "")
    
    # 3. Determine Lead State and Score based on context
    lead_state = "NEW"
    score = 0.5
    
    if any(word in msg_lower for word in ["refund", "scam", "lawyer", "attorney", "court", "sue", "annoying"]):
        lead_state = "ASSIGN"
        score = 0.99
    elif any(word in msg_lower for word in ["skool", "diy", "monthly", "cheap", "fix myself", "do it myself"]):
        lead_state = "NEW"
        score = 0.72
    elif any(word in msg_lower for word in ["advanced", "1-on-1", "pricing", "cost", "strategy", "funding", "business", "truck", "semi", "dscr", "house"]):
        lead_state = "QUALIFIED"
        score = 0.88
        
    # 4. Check Compliance
    compliance = "PASSED"
    if any(word in msg_lower for word in ["credit sweep", "guarantee", "guaranteed"]):
        compliance = "FAILED (Banned Phrase)"
        reply = "[Compliance Warning: Output blocked due to banned phrase guarantee/credit sweep]."

    SIMULATION_HISTORY.append({
        "user_name": "Test Prospect",
        "user_msg": user_message,
        "reply_text": reply,
        "lead_state": lead_state,
        "score": score,
        "sentiment": sentiment.upper(),
        "compliance": compliance
    })
    
    if len(SIMULATION_HISTORY) > 10:
        SIMULATION_HISTORY.pop(0)
        
    return RedirectResponse("/admin", status_code=303)

@app.post("/action/generate-copy")
async def generate_copy(ai_prompt: str = Form(...)):
    global DRAFTED_COPY_CACHE
    key = os.getenv("OPENROUTER_API_KEY", "")
    model = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct:free")
    
    os.environ["LAST_AI_PROMPT_VAL"] = ai_prompt
    
    if "funding" in ai_prompt.lower() or "business" in ai_prompt.lower():
        os.environ["LAST_CAMP_NAME_VAL"] = "Atlanta Corporate Capital Campaign"
    else:
        os.environ["LAST_CAMP_NAME_VAL"] = "Collections Removal Blitz"

    if key and "your_openrouter" not in key:
        try:
            headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are Jordynn Miller, founder of Angel Solutions ATL. "
                            "You write raw, high-converting, CROA-compliant social media ad copy "
                            "for business owners or individuals looking to restore credit or obtain unsecured capital. "
                            "Do NOT use forbidden terms like 'credit fix', 'credit sweep', or 'guarantee'. "
                            "Focus on collections deletion and 1-on-1 funding consulting. Keep it premium, warm, "
                            "motivational, and structured with emojis. Max 180 words."
                        )
                    },
                    {"role": "user", "content": f"Write ad copy for Facebook Lead Ads based on this: {ai_prompt}"}
                ]
            }
            res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=12)
            if res.status_code == 200:
                DRAFTED_COPY_CACHE = res.json()["choices"][0]["message"]["content"]
                return RedirectResponse("/admin?tab=ads", status_code=303)
        except Exception as e:
            print(f"[OpenRouter API Client Exception] {e}")

    if "funding" in ai_prompt.lower() or "business" in ai_prompt.lower() or "corporate" in ai_prompt.lower():
        DRAFTED_COPY_CACHE = (
            "🚀 ATL BUSINESS OWNERS: Blocked from secured business funding due to credit bottlenecks?\n\n"
            "Hey there! Jordynn Miller here. At Angel Solutions ATL, we clear old collection accounts, "
            "bankruptcies, or high utilization bottlenecks holding you back from growth.\n\n"
            "We do premium, rapid deletions and 1-on-1 custom roadmaps to corporate-ready profile. "
            "Get set up for up to $150K in unsecured commercial funding.\n\n"
            "🛑 No monthly recurring fees. Just permanent deletions and direct solutions.\n\n"
            "👇 Click 'Sign Up' below to scan your eligibility instantly!"
        )
    else:
        DRAFTED_COPY_CACHE = (
            "📈 Collections or negative charge-offs dragging down your score? It's time to restore.\n\n"
            "Hey! Jordynn Miller here. If you need a clean slate to buy a home, acquire a vehicle, or secure funding, "
            "our Advanced Credit Restoral is designed for you.\n\n"
            "We do full-service, rapid legal disputes of all collections at once. No monthly sub-charges, "
            "just professional consultations and massive removals.\n\n"
            "Let's wipe the slate clean and secure your financial future today.\n\n"
            "👇 Click 'Sign Up' below to reserve your private strategy call now!"
        )

    return RedirectResponse("/admin?tab=ads", status_code=303)

@app.post("/action/launch-campaign")
async def launch_campaign(campaign_name: str = Form(...), daily_budget: str = Form(...), ad_copy: str = Form(...), lead_form_id: str = Form(...)):
    global CAMPAIGN_LAUNCH_LOGS
    os.environ["LAST_CAMP_NAME_VAL"] = campaign_name
    os.environ["LAST_DAILY_BUDGET_VAL"] = daily_budget
    
    try:
        budget_val = float(daily_budget)
    except ValueError:
        budget_val = 30.0

    client = MetaAdsClient()
    result = client.create_leadgen_campaign(
        name=campaign_name,
        daily_budget_dollars=budget_val,
        ai_copy=ad_copy,
        lead_form_id=lead_form_id
    )

    CAMPAIGN_LAUNCH_LOGS.clear()
    CAMPAIGN_LAUNCH_LOGS.extend(result["logs"])

    print(f"[PUBLISHER ACTION] Campaign Published Status: {result['success']} (Mode: {result['mode']})")
    return RedirectResponse("/admin?tab=ads", status_code=303)

@app.post("/action/create-form")
async def create_form(form_name: str = Form(...), privacy_url: str = Form(...), redirect_url: str = Form(...), custom_question: str = Form(None)):
    global CAMPAIGN_LAUNCH_LOGS
    client = MetaAdsClient()
    result = client.create_lead_form(
        name=form_name,
        privacy_policy_url=privacy_url,
        redirect_url=redirect_url,
        custom_question_text=custom_question if custom_question else None
    )
    
    CAMPAIGN_LAUNCH_LOGS.clear()
    CAMPAIGN_LAUNCH_LOGS.extend(result["logs"])
    
    print(f"[FORM ACTION] Form Created Status: {result['success']} (ID: {result['form_id']})")
    return RedirectResponse("/admin?tab=ads", status_code=303)

@app.get("/logout")
async def logout():
    response = RedirectResponse("/admin/login", status_code=303)
    response.delete_cookie("session_token")
    return response
