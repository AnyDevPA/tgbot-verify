import random
try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

def generate_asu_html(first_name, last_name):
    """Credencial Arizona State University"""
    # ID de ASU suele ser 10 dígitos o 9
    asu_id = f"{random.randint(1000000000, 1299999999)}"
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<style>
    body {{ font-family: sans-serif; background: #fff; margin: 0; padding: 20px; }}
    .card {{
        width: 350px; height: 220px;
        border-radius: 12px;
        background: #8C1D40; /* ASU Maroon */
        position: relative;
        color: white;
        overflow: hidden;
        border: 1px solid #666;
    }}
    .header {{
        position: absolute; top: 15px; left: 15px;
        font-weight: bold; font-size: 14px; text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .gold-bar {{
        position: absolute; top: 45px; left: 0; width: 100%; height: 20px;
        background: #FFC627; /* ASU Gold */
    }}
    .photo {{
        position: absolute; top: 75px; left: 15px;
        width: 90px; height: 110px; background: #ddd; border: 2px solid white;
        display: flex; align-items: center; justify-content: center; color: #555; font-size: 10px;
    }}
    .info {{
        position: absolute; top: 80px; left: 120px;
    }}
    .name {{ font-size: 18px; font-weight: bold; text-transform: uppercase; margin-bottom: 5px; }}
    .role {{ font-size: 12px; font-weight: normal; margin-bottom: 15px; }}
    .id-num {{ font-family: monospace; font-size: 14px; letter-spacing: 1px; }}
    .footer {{
        position: absolute; bottom: 10px; right: 15px;
        font-size: 10px; font-weight: bold;
    }}
</style>
</head>
<body>
    <div class="card">
        <div class="header">Arizona State University</div>
        <div class="gold-bar"></div>
        <div class="photo">PHOTO</div>
        <div class="info">
            <div class="name">{first_name}<br>{last_name}</div>
            <div class="role">STUDENT</div>
            <div class="id-num">{asu_id}</div>
        </div>
        <div class="footer">SUN CARD</div>
    </div>
</body>
</html>"""
    return html

def generate_image(first_name, last_name, school_id='999'):
    if not HAS_PLAYWRIGHT: return b""
    try:
        html = generate_asu_html(first_name, last_name)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 400, 'height': 300})
            page.set_content(html)
            img = page.screenshot(type='jpeg', quality=90)
            browser.close()
        return img
    except Exception:
        return b""
