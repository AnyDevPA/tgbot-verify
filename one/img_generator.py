import random
try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

def generate_psu_html(first_name, last_name):
    """Credencial Penn State University"""
    id_num = f"9{random.randint(10000000, 99999999)}"
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<style>
    body {{ font-family: Arial, sans-serif; background: #fff; margin: 0; padding: 20px; }}
    .card {{
        width: 350px; height: 220px;
        border: 1px solid #ddd;
        border-radius: 10px;
        position: relative;
        background: white;
        overflow: hidden;
    }}
    .header {{
        background-color: #001E44; /* PSU Blue */
        height: 50px;
        display: flex; align-items: center; justify-content: center;
    }}
    .header-text {{ color: white; font-weight: bold; font-size: 18px; letter-spacing: 1px; }}
    .content {{ display: flex; padding: 15px; }}
    .photo {{
        width: 90px; height: 110px; background: #eee; border: 2px solid #001E44;
        display: flex; align-items: center; justify-content: center; font-size: 10px; color: #888;
    }}
    .details {{ margin-left: 15px; font-size: 12px; color: #333; }}
    .name {{ font-size: 16px; font-weight: bold; text-transform: uppercase; color: #000; margin-bottom: 5px; }}
    .id-row {{ margin-top: 10px; font-weight: bold; font-size: 14px; color: #001E44; }}
    .footer {{
        position: absolute; bottom: 0; width: 100%; height: 30px;
        background: #001E44; color: white; text-align: center; line-height: 30px; font-size: 10px;
    }}
    .logo-placeholder {{
        position: absolute; top: 60px; right: 20px;
        width: 50px; height: 50px; border-radius: 50%;
        background: #ddd; opacity: 0.5;
    }}
</style>
</head>
<body>
    <div class="card">
        <div class="header">
            <div class="header-text">PENN STATE</div>
        </div>
        <div class="logo-placeholder"></div>
        <div class="content">
            <div class="photo">STUDENT<br>PHOTO</div>
            <div class="details">
                <div class="name">{first_name}<br>{last_name}</div>
                <div>Undergraduate Student</div>
                <div>University Park</div>
                <div class="id-row">ID: {id_num}</div>
                <div style="margin-top:5px;">Exp: 05/2026</div>
            </div>
        </div>
        <div class="footer">PennState id+ Card</div>
    </div>
</body>
</html>"""
    return html

def generate_image(first_name, last_name, school_id='999'):
    if not HAS_PLAYWRIGHT: return b""
    try:
        html = generate_psu_html(first_name, last_name)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 400, 'height': 300})
            page.set_content(html)
            img = page.screenshot(type='jpeg', quality=90)
            browser.close()
        return img
    except Exception:
        return b""
