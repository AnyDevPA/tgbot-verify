import random
try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

def generate_phoenix_html(first_name, last_name):
    """Credencial University of Phoenix"""
    # ID numérico largo
    phx_id = f"900{random.randint(100000, 999999)}"
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<style>
    body {{ font-family: 'Arial', sans-serif; background: #fff; margin: 0; padding: 20px; }}
    .card {{
        width: 360px; height: 230px;
        background: #C8102E; /* Phoenix Red */
        border-radius: 10px;
        position: relative;
        color: white;
        overflow: hidden;
    }}
    .white-section {{
        position: absolute; bottom: 0; width: 100%; height: 160px;
        background: white;
    }}
    .header {{
        position: absolute; top: 20px; left: 20px;
        font-size: 16px; font-weight: bold; text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .photo {{
        position: absolute; top: 50px; left: 20px;
        width: 100px; height: 125px;
        background: #eee; border: 3px solid white;
        display: flex; align-items: center; justify-content: center;
        color: #555; font-size: 10px;
        z-index: 10;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }}
    .info {{
        position: absolute; top: 80px; left: 140px;
        color: #333; z-index: 5;
    }}
    .name {{ font-size: 20px; font-weight: bold; text-transform: uppercase; color: #C8102E; margin-bottom: 5px; }}
    .role {{ font-size: 14px; font-weight: bold; margin-bottom: 20px; color: #555; }}
    .id-row {{ font-family: monospace; font-size: 14px; color: #000; }}
    .footer {{
        position: absolute; bottom: 10px; right: 15px;
        font-size: 10px; color: #999; font-weight: bold;
    }}
</style>
</head>
<body>
    <div class="card">
        <div class="header">University of Phoenix</div>
        <div class="white-section"></div>
        <div class="photo">STUDENT</div>
        <div class="info">
            <div class="name">{first_name}<br>{last_name}</div>
            <div class="role">Student Body</div>
            <div class="id-row">ID: {phx_id}</div>
        </div>
        <div class="footer">VALID 2025-2026</div>
    </div>
</body>
</html>"""
    return html

def generate_image(first_name, last_name, school_id='999'):
    if not HAS_PLAYWRIGHT: return b""
    try:
        html = generate_phoenix_html(first_name, last_name)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 400, 'height': 300})
            page.set_content(html)
            img = page.screenshot(type='jpeg', quality=90)
            browser.close()
        return img
    except Exception:
        return b""
