import random
from datetime import datetime
import io
import base64
import sys

# Intentamos importar librerías de imagen, si no están, no crashea
try:
    import numpy as np
    from PIL import Image, ImageFilter, ImageEnhance
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

def generate_html(first_name, last_name):
    """
    Genera un Dashboard de Canvas LMS (Muy común en USA)
    """
    date_str = datetime.now().strftime('%b %d at %I:%M %p')
    
    # Colores típicos de tarjetas de Canvas
    colors = ['#E03E3E', '#008450', '#EF6C00', '#B30021', '#2D3B45', '#69208F']
    random.shuffle(colors)
    
    courses = [
        {"code": "CS 101", "name": "Intro to Computer Science", "term": "Spring 2026"},
        {"code": "HIST 202", "name": "World History Since 1500", "term": "Spring 2026"},
        {"code": "MATH 141", "name": "Calculus I", "term": "Spring 2026"},
        {"code": "ENG 102", "name": "Composition II", "term": "Spring 2026"}
    ]

    # Construimos las tarjetas HTML
    cards_html = ""
    for i, course in enumerate(courses):
        color = colors[i % len(colors)]
        cards_html += f"""
        <div class="card">
            <div class="card-header" style="background-color: {color};">
                <div class="card-dots">...</div>
            </div>
            <div class="card-body">
                <div class="course-title"><span style="color:{color}">{course['code']}</span><br>{course['name']}</div>
                <div class="course-term">{course['term']}</div>
                <div class="card-icons">
                    <span>📣</span> <span>📝</span> <span>💬</span> <span>📂</span>
                </div>
            </div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body {{ margin: 0; font-family: "Lato", "Helvetica Neue", Arial, sans-serif; background-color: #F5F5F5; display: flex; height: 100vh; overflow: hidden; }}
        /* Sidebar Azul Oscuro (Estilo Canvas) */
        .sidebar {{ width: 84px; background-color: #2D3B45; display: flex; flex-direction: column; align-items: center; padding-top: 20px; flex-shrink: 0; }}
        .logo {{ width: 50px; height: 50px; background-color: white; border-radius: 50%; margin-bottom: 20px; display: flex; align-items: center; justify-content: center; font-weight: bold; color: #2D3B45; font-size: 10px; text-align: center; }}
        .menu-item {{ color: white; font-size: 11px; margin-bottom: 20px; text-align: center; opacity: 0.8; }}
        .menu-icon {{ display: block; font-size: 24px; margin-bottom: 5px; }}
        .menu-item.active {{ color: white; opacity: 1; border-left: 4px solid white; width: 100%; }}
        
        /* Contenido Principal */
        .main {{ flex: 1; padding: 24px; overflow-y: auto; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; border-bottom: 1px solid #ddd; padding-bottom: 15px; }}
        .page-title {{ font-size: 24px; color: #2D3B45; margin: 0; font-weight: 300; }}
        .page-title strong {{ font-weight: 700; }}
        
        /* Grid de Cursos */
        .dashboard-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 24px; }}
        .card {{ background: white; border-radius: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); overflow: hidden; height: 260px; display: flex; flex-direction: column; }}
        .card-header {{ height: 140px; position: relative; }}
        .card-dots {{ position: absolute; top: 10px; right: 10px; color: white; font-weight: bold; cursor: pointer; }}
        .card-body {{ padding: 12px; flex: 1; display: flex; flex-direction: column; justify-content: space-between; }}
        .course-title {{ font-weight: bold; color: #2D3B45; font-size: 15px; line-height: 1.4; }}
        .course-term {{ color: #666; font-size: 12px; margin-top: 4px; text-transform: uppercase; }}
        .card-icons {{ display: flex; gap: 15px; color: #666; font-size: 16px; margin-top: 10px; }}
        
        /* Sidebar Derecha (To Do) */
        .right-sidebar {{ width: 250px; padding: 24px; background: #F5F5F5; border-left: 1px solid #ddd; display: none; }}
        @media (min-width: 1000px) {{ .right-sidebar {{ display: block; }} }}
        .todo-item {{ margin-bottom: 15px; font-size: 13px; color: #444; }}
        .todo-title {{ font-weight: bold; display: block; }}
        .todo-meta {{ color: #777; font-size: 11px; }}
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="logo">STATE<br>UNIV</div>
        <div class="menu-item">
            <span class="menu-icon">👤</span>Account
        </div>
        <div class="menu-item active">
            <span class="menu-icon">dashboard</span>Dashboard
        </div>
        <div class="menu-item">
            <span class="menu-icon">📖</span>Courses
        </div>
        <div class="menu-item">
            <span class="menu-icon">📅</span>Calendar
        </div>
        <div class="menu-item">
            <span class="menu-icon">📥</span>Inbox
        </div>
    </div>

    <div class="main">
        <div class="header">
            <h1 class="page-title">Dashboard</h1>
            <div style="font-size: 14px; color: #555;">Welcome, <strong>{first_name} {last_name}</strong></div>
        </div>

        <div class="dashboard-grid">
            {cards_html}
        </div>
    </div>

    <div class="right-sidebar">
        <h3 style="margin-top: 0; color: #2D3B45; font-size: 14px; border-bottom: 1px solid #ccc; padding-bottom: 10px;">To Do</h3>
        <div class="todo-item">
            <span class="todo-title">Grade Assignment: Intro to Python</span>
            <span class="todo-meta">10 points • Due Jan 20 at 11:59pm</span>
        </div>
        <div class="todo-item">
            <span class="todo-title">Read: Chapter 4 History</span>
            <span class="todo-meta">Due Jan 22 at 11:59pm</span>
        </div>
        <h3 style="margin-top: 20px; color: #2D3B45; font-size: 14px; border-bottom: 1px solid #ccc; padding-bottom: 10px;">Coming Up</h3>
        <div class="todo-item">
            <span class="todo-title">Midterm Exam (Calculus)</span>
            <span class="todo-meta">Feb 15 at 1:00pm</span>
        </div>
    </div>
</body>
</html>
"""
    return html

def make_it_look_real(image_bytes):
    """ Filtro de suciedad para parecer foto de celular """
    if not HAS_PIL:
        return image_bytes # Si no hay librería, devuelve original
    
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img_array = np.array(img)
        
        # Ruido
        noise = np.random.normal(0, 12, img_array.shape) 
        noisy_img = np.clip(img_array + noise, 0, 255).astype(np.uint8)
        img = Image.fromarray(noisy_img)

        # Desenfoque y rotación
        img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
        angle = random.uniform(-1.0, 1.0)
        img = img.rotate(angle, resample=Image.BICUBIC, expand=True, fillcolor='#F5F5F5')

        # Ajustes finales
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.97)
        
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=85)
        return output.getvalue()
    except Exception as e:
        print(f"Error filtro: {e}")
        return image_bytes

def generate_image(first_name, last_name, school_id='9999'):
    try:
        from playwright.sync_api import sync_playwright
        
        html_content = generate_html(first_name, last_name)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            # Tamaño típico de laptop 13 pulgadas
            page = browser.new_page(viewport={'width': 1366, 'height': 768})
            page.set_content(html_content, wait_until='networkidle')
            page.wait_for_timeout(1000) # Esperamos renderizado
            
            screenshot_bytes = page.screenshot(type='png', full_page=True)
            browser.close()

        # Aplicar filtro
        final_image = make_it_look_real(screenshot_bytes)
        return final_image

    except ImportError:
        raise Exception("Falta Playwright")
    except Exception as e:
        raise Exception(f"Error: {e}")

# Esto es solo para que el código viejo no rompa si llama a estas funciones
def generate_psu_id(): return "912345678"
def generate_psu_email(f, l): return f"{f}.{l}@edu.com"

if __name__ == '__main__':
    # Test local
    d = generate_image("Brian", "Test")
    with open("test_canvas.jpg", "wb") as f:
        f.write(d)
    print("Generado test_canvas.jpg")
