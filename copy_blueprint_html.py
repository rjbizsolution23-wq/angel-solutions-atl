import re
import os

html_path = "8f4ed056a_angel_solutions_atl_master_blueprint (1).html"
js_output_path = "cloudflare-worker/src/blueprint-html.js"

if not os.path.exists(html_path):
    print(f"Error: {html_path} does not exist.")
    exit(1)

with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# Define the Live Telemetry Card HTML
telemetry_card = """
  <div class="telemetry-card" style="background: var(--card); border: 1px solid var(--border); border-radius: 0.85rem; padding: 1.25rem 1.4rem; margin-top: 1.5rem; box-shadow: 0 4px 20px -2px rgba(0,0,0,0.05);">
    <h3 style="margin-top:0; font-size:1rem; font-family:-apple-system, sans-serif; display:flex; align-items:center; gap:0.5rem; color:var(--primary);">
      <span style="width:8px; height:8px; border-radius:50%; background:#10b981; display:inline-block; box-shadow:0 0 8px #10b981;"></span>
      Live Cloudflare D1 Telemetry
    </h3>
    <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:1rem; text-align:center; margin-top:1rem;">
      <div style="background:var(--background); padding:0.75rem; border-radius:0.5rem; border:1px solid var(--border);">
        <div style="font-size:1.5rem; font-weight:700; color:var(--primary);">{{LEAD_COUNT}}</div>
        <div style="font-size:0.7rem; color:var(--muted-foreground); text-transform:uppercase; font-weight:600;">Total Leads</div>
      </div>
      <div style="background:var(--background); padding:0.75rem; border-radius:0.5rem; border:1px solid var(--border);">
        <div style="font-size:1.5rem; font-weight:700; color:var(--primary);">{{QUALIFIED_COUNT}}</div>
        <div style="font-size:0.7rem; color:var(--muted-foreground); text-transform:uppercase; font-weight:600;">Qualified</div>
      </div>
      <div style="background:var(--background); padding:0.75rem; border-radius:0.5rem; border:1px solid var(--border);">
        <div style="font-size:1.5rem; font-weight:700; color:var(--primary);">{{BOOKED_COUNT}}</div>
        <div style="font-size:0.7rem; color:var(--muted-foreground); text-transform:uppercase; font-weight:600;">Booked</div>
      </div>
      <div style="background:var(--background); padding:0.75rem; border-radius:0.5rem; border:1px solid var(--border);">
        <div style="font-size:1.5rem; font-weight:700; color:var(--primary);">{{CONVERSION_RATE}}%</div>
        <div style="font-size:0.7rem; color:var(--muted-foreground); text-transform:uppercase; font-weight:600;">Conv. Rate</div>
      </div>
    </div>
  </div>
"""

# Inject the card below the header paragraph
header_pattern = r'(<div class="header">.*?<p>.*?</p>)'
if re.search(header_pattern, html_content, re.DOTALL):
    html_content = re.sub(header_pattern, r'\1' + telemetry_card, html_content, flags=re.DOTALL)
else:
    print("Warning: Could not locate header paragraph structure in HTML.")

# Escape backticks in HTML to make it a safe JavaScript template literal
escaped_html = html_content.replace("`", "\\`").replace("${", "\\${")

# Write to blueprint-html.js
js_content = f"""// =====================================================================
// ANGEL SOLUTIONS ATL - MASTER SYSTEM BLUEPRINT HTML TEMPLATE
// =====================================================================
// Auto-generated from {html_path}.
// =====================================================================

export const BLUEPRINT_HTML = `{escaped_html}`;
"""

with open(js_output_path, "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"Successfully compiled {html_path} to {js_output_path}")
