import random
try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

def generate_gcu_html(first_name, last_name):
    """Credencial Grand Canyon University"""
    gcu_id = f"{random.randint(10000000, 99999999)}"
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<style>
    body {{ font-family: Arial, sans-serif; background: #fff; margin: 0; padding: 20px; }}
    .card {{
        width: 350px; height: 220px;
        background: white;
        border-radius: 10px;
        border: 2px solid #522398; /* GCU Purple */
        position: relative;
        overflow: hidden;
    }}
    .header {{
        background: #522398;
        height: 50px;
        display: flex; align-items: center; justify-content: center;
        color: white; font-weight: bold; font-size: 18px; letter-spacing: 1px;
    }}
    .content {{ display: flex; padding: 15px; }}
    .photo {{
        width: 90px; height: 110px; background: #eee;
        border: 2px solid #522398;
        display: flex; align-items: center; justify-content: center;
        font-size: 10px; color: #555;
    }}
    .info {{ margin-left: 15px; width: 200px; }}
    .name {{ font-size: 18px; font-weight: bold; text-transform: uppercase; color: #000; margin-bottom: 5px; }}
    .role {{ color: #555; font-size: 14px; margin-bottom: 15px; font-weight: bold; }}
    .id-block {{ font-size: 12px; color: #333; }}
    .footer {{
        position: absolute; bottom: 0; width: 100%; height: 20px;
        background: #000; color: white; text-align: center;
        font-size: 9px; line-height: 20px;
    }}
</style>
</head>
<body>
    <div class="card">
        <div class="header">GRAND CANYON UNIVERSITY</div>
        <div class="content">
            <div class="photo">GCU<br>STUDENT</div>
            <div class="info">
                <div class="name">{first_name}<br>{last_name}</div>
                <div class="role">UNDERGRADUATE</div>
                <div class="id-block">
                    CAMPUS ID: {gcu_id}<br>
                    VALID THRU: 05/2026
                </div>
            </div>
        </div>
        <div class="footer">Lopes Up!</div>
    </div>
</body>
</html>"""
    return html

def generate_image(first_name, last_name, school_id='999'):
    if not HAS_PLAYWRIGHT: return b""
    try:
        html = generate_gcu_html(first_name, last_name)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 400, 'height': 300})
            page.set_content(html)
            img = page.screenshot(type='jpeg', quality=90)
            browser.close()
        return img
    except Exception:
        return b""
