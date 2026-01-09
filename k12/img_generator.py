import random
from datetime import datetime
import io

try:
    import numpy as np
    from PIL import Image, ImageFilter, ImageEnhance
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

def generate_teacher_id_html(first_name, last_name):
    """Genera un Gafete de Maestro (Teacher ID)"""
    school_name = "AUSTIN HIGH SCHOOL"
    school_year = "2025 - 2026"
    staff_id = f"T-{random.randint(10000, 99999)}"
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<style>
    body {{ font-family: sans-serif; background: #fff; margin: 0; padding: 20px; }}
    .badge {{
        width: 350px; height: 550px;
        border: 2px solid #000;
        border-radius: 15px;
        position: relative;
        text-align: center;
        background: linear-gradient(180deg, #800000 0%, #800000 15%, #ffffff 15%, #ffffff 100%);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }}
    .header {{ color: white; font-weight: bold; font-size: 22px; padding-top: 20px; letter-spacing: 1px; }}
    .photo-box {{
        width: 180px; height: 220px;
        background-color: #ddd;
        margin: 40px auto 20px;
        border: 3px solid #333;
        display: flex; align-items: center; justify-content: center;
        color: #666; font-size: 10px;
    }}
    .name {{ font-size: 26px; font-weight: 900; color: #000; text-transform: uppercase; margin-bottom: 5px; }}
    .title {{ font-size: 18px; color: #800000; font-weight: bold; text-transform: uppercase; letter-spacing: 2px; }}
    .meta {{ margin-top: 20px; font-size: 14px; color: #333; }}
    .barcode {{
        margin-top: 30px; height: 40px; background: #000; width: 80%; margin-left: 10%;
        mask: repeating-linear-gradient(90deg, transparent, transparent 2px, #000 2px, #000 4px);
    }}
    .footer {{ position: absolute; bottom: 15px; width: 100%; font-size: 10px; color: #666; }}
    .year-badge {{
        position: absolute; top: 100px; right: 20px;
        background: #D4AF37; color: black; padding: 5px 10px;
        font-weight: bold; border-radius: 50%; transform: rotate(15deg);
        border: 2px solid white; box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    }}
</style>
</head>
<body>
    <div class="badge">
        <div class="header">AUSTIN MAROONS</div>
        
        <div class="year-badge">STAFF<br>25-26</div>
        
        <div class="photo-box">
            [ PHOTO ]
        </div>
        
        <div class="name">{first_name}<br>{last_name}</div>
        <div class="title">FACULTY / TEACHER</div>
        
        <div class="meta">
            ID: {staff_id}<br>
            DEPT: SCIENCE
        </div>
        
        <div class="barcode"></div>
        
        <div class="footer">
            {school_name}<br>
            1715 W Cesar Chavez St, Austin, TX
        </div>
    </div>
</body>
</html>"""
    return html

def make_it_look_scanned(image_bytes):
    """Filtro de foto de gafete real"""
    if not HAS_PIL: return image_bytes
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        # Ruido y desenfoque ligero
        arr = np.array(img)
        noise = np.random.normal(0, 5, arr.shape)
        img = Image.fromarray(np.clip(arr + noise, 0, 255).astype(np.uint8))
        img = img.filter(ImageFilter.GaussianBlur(radius=0.3))
        # Guardar
        out = io.BytesIO()
        img.save(out, format='JPEG', quality=85)
        return out.getvalue()
    except:
        return image_bytes

def generate_image(first_name, last_name, school_id='999'):
    try:
        from playwright.sync_api import sync_playwright
        html = generate_teacher_id_html(first_name, last_name)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 400, 'height': 600})
            page.set_content(html, wait_until='load')
            page.wait_for_timeout(200)
            ss = page.screenshot(type='png', full_page=True)
            browser.close()
        return make_it_look_scanned(ss)
    except Exception as e:
        raise Exception(f"Error generando Teacher ID: {e}")

# Compatibilidad
def generate_psu_id(): return "000"
def generate_psu_email(f, l): return f"{f[0]}{l}@austinisd.org"
