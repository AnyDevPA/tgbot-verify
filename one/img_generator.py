import random
try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

def generate_wtc_html(first_name, last_name):
    """Credencial Western Tech"""
    wtc_id = f"WT-{random.randint(10000, 99999)}"
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<style>
    body {{ font-family: Arial, sans-serif; background: #fff; margin: 0; padding: 20px; }}
    .card {{
        width: 360px; height: 230px;
        background: #fff;
        border: 2px solid #E35205; /* Tech Orange */
        border-radius: 8px;
        position: relative;
    }}
    .header {{
        background: #E35205;
        height: 40px;
        display: flex; align-items: center; justify-content: center;
        color: white; font-weight: bold; font-size: 16px;
    }}
    .photo {{
        position: absolute; top: 60px; left: 20px;
        width: 100px; height: 120px;
        background: #333;
        display: flex; align-items: center; justify-content: center;
        color: white; font-size: 10px;
    }}
    .info {{ position: absolute; top: 60px; left: 140px; width: 200px; }}
    .name {{ font-size: 18px; font-weight: bold; text-transform: uppercase; margin-bottom: 5px; }}
    .program {{ font-size: 12px; color: #666; margin-bottom: 20px; }}
    .footer {{
        position: absolute; bottom: 10px; width: 100%;
        text-align: center; font-size: 10px; font-weight: bold; color: #333;
    }}
</style>
</head>
<body>
    <div class="card">
        <div class="header">Western Technical College</div>
        <div class="photo">STUDENT</div>
        <div class="info">
            <div class="name">{first_name}<br>{last_name}</div>
            <div class="program">Occupational Studies</div>
            <div>ID: {wtc_id}</div>
        </div>
        <div class="footer">EL PASO, TEXAS</div>
    </div>
</body>
</html>"""
    return html

def generate_image(first_name, last_name, school_id='999'):
    if not HAS_PLAYWRIGHT: return b""
    try:
        html = generate_wtc_html(first_name, last_name)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 400, 'height': 300})
            page.set_content(html)
            img = page.screenshot(type='jpeg', quality=90)
            browser.close()
        return img
    except Exception:
        return b""
