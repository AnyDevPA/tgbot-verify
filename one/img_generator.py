import random
try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

def generate_snhu_html(first_name, last_name):
    """Credencial SNHU (Southern New Hampshire University)"""
    # ID de 7 dígitos
    snhu_id = f"{random.randint(1000000, 9999999)}"
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<style>
    body {{ font-family: 'Arial', sans-serif; background: #fff; margin: 0; padding: 20px; }}
    .card {{
        width: 360px; height: 230px;
        border-radius: 8px;
        background: white;
        border: 2px solid #00205B;
        position: relative;
        overflow: hidden;
    }}
    .header {{
        background-color: #00205B; /* SNHU Blue */
        height: 60px;
        color: #FFC72C; /* SNHU Yellow */
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; font-size: 20px;
    }}
    .content {{ padding: 20px; display: flex; }}
    .photo {{
        width: 80px; height: 100px; background: #ddd;
        border: 1px solid #aaa;
        display: flex; align-items: center; justify-content: center;
        font-size: 9px; color: #555;
    }}
    .text-info {{ margin-left: 20px; font-size: 14px; color: #333; }}
    .name {{ font-size: 18px; font-weight: bold; margin-bottom: 5px; text-transform: uppercase; color: #00205B; }}
    .role {{ font-weight: bold; color: #555; margin-bottom: 15px; font-size: 12px; }}
    .id-text {{ font-family: monospace; font-size: 16px; letter-spacing: 1px; }}
    .footer {{
        position: absolute; bottom: 0; width: 100%; height: 25px;
        background: #F2F2F2; color: #00205B;
        text-align: center; line-height: 25px; font-size: 10px; font-weight: bold;
    }}
</style>
</head>
<body>
    <div class="card">
        <div class="header">SNHU</div>
        <div class="content">
            <div class="photo">STUDENT<br>IMAGE</div>
            <div class="text-info">
                <div class="name">{first_name}<br>{last_name}</div>
                <div class="role">Active Student</div>
                <div>ID Number:</div>
                <div class="id-text">{snhu_id}</div>
            </div>
        </div>
        <div class="footer">Southern New Hampshire University</div>
    </div>
</body>
</html>"""
    return html

def generate_image(first_name, last_name, school_id='999'):
    if not HAS_PLAYWRIGHT: return b""
    try:
        html = generate_snhu_html(first_name, last_name)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 400, 'height': 300})
            page.set_content(html)
            img = page.screenshot(type='jpeg', quality=90)
            browser.close()
        return img
    except Exception:
        return b""
