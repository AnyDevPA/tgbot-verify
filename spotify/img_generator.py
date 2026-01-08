import random
from datetime import datetime
import io
import sys

# Intentamos importar librerías de imagen
try:
    import numpy as np
    from PIL import Image, ImageFilter, ImageEnhance
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

def generate_html(first_name, last_name):
    """
    Genera un 'Unofficial Transcript' de Arizona State University (ASU)
    Estilo clásico web (MyASU)
    """
    current_date = datetime.now().strftime('%m/%d/%Y')
    
    # Generamos calificaciones creíbles (No todo A, para que parezca real)
    grades = [
        {"code": "CSE 110", "title": "Principles of Programming", "credit": "3.0", "grade": "A", "term": "Fall 2025"},
        {"code": "MAT 265", "title": "Calculus for Engineers I", "credit": "3.0", "grade": "B+", "term": "Fall 2025"},
        {"code": "ENG 101", "title": "First-Year Composition", "credit": "3.0", "grade": "A-", "term": "Fall 2025"},
        {"code": "ASU 101", "title": "The ASU Experience", "credit": "1.0", "grade": "A", "term": "Fall 2025"},
        # Cursos actuales (En progreso)
        {"code": "CSE 205", "title": "Obj-Oriented Prog & Data Struc", "credit": "3.0", "grade": "IP", "term": "Spring 2026"},
        {"code": "MAT 266", "title": "Calculus for Engineers II", "credit": "3.0", "grade": "IP", "term": "Spring 2026"},
        {"code": "PHY 121", "title": "University Physics I", "credit": "4.0", "grade": "IP", "term": "Spring 2026"}
    ]
    
    student_id = f"12{random.randint(1000000, 9999999)}"

    rows_html = ""
    for g in grades:
        status = "Completed" if g['grade'] != "IP" else "In Progress"
        rows_html += f"""
        <tr class="{'current' if g['grade'] == 'IP' else ''}">
            <td>{g['term']}</td>
            <td>{g['code']}</td>
            <td>{g['title']}</td>
            <td>{g['credit']}</td>
            <td>{g['grade']}</td>
            <td>{status}</td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, Helvetica, sans-serif; background-color: #ffffff; margin: 40px; color: #333; }}
        .header {{ border-bottom: 2px solid #8C1D40; padding-bottom: 20px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: flex-end; }}
        .logo-text {{ font-family: "Impact", "Arial Black", sans-serif; font-size: 32px; color: #000; text-transform: uppercase; }}
        .logo-sub {{ color: #8C1D40; font-size: 14px; font-weight: bold; }}
        .doc-title {{ font-size: 24px; font-weight: bold; color: #333; text-align: center; margin: 20px 0; text-transform: uppercase; }}
        
        .student-info {{ background-color: #f9f9f9; padding: 15px; border: 1px solid #ddd; margin-bottom: 30px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 14px; }}
        .info-label {{ font-weight: bold; color: #555; }}
        
        table {{ width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 20px; }}
        th {{ background-color: #8C1D40; color: white; text-align: left; padding: 10px; font-weight: bold; }}
        td {{ border-bottom: 1px solid #eee; padding: 10px; }}
        tr.current {{ background-color: #fff8e1; }} /* Highlight current classes */
        
        .summary {{ float: right; width: 300px; margin-top: 10px; border: 1px solid #ccc; padding: 10px; font-size: 13px; }}
        .sum-row {{ display: flex; justify-content: space-between; margin-bottom: 5px; }}
        .status-verified {{ color: green; font-weight: bold; }}
        
        .footer {{ clear: both; margin-top: 50px; font-size: 11px; color: #777; border-top: 1px solid #ccc; padding-top: 10px; text-align: center; }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <div class="logo-text">Arizona State University</div>
            <div class="logo-sub">UNIVERSITY REGISTRAR SERVICES</div>
        </div>
        <div style="text-align: right; font-size: 12px;">
            Date Issued: {current_date}<br>
            Campus: Tempe
        </div>
    </div>

    <div class="doc-title">Unofficial Academic Transcript</div>

    <div class="student-info">
        <div><span class="info-label">Student Name:</span> {last_name.upper()}, {first_name.upper()}</div>
        <div><span class="info-label">Student ID:</span> {student_id}</div>
        <div><span class="info-label">Date of Birth:</span> **/**/****</div>
        <div><span class="info-label">Residency:</span> Resident</div>
        <div><span class="info-label">College:</span> Ira A. Fulton Schools of Engineering</div>
        <div><span class="info-label">Major:</span> Computer Science (BS)</div>
    </div>

    <table>
        <thead>
            <tr>
                <th>Term</th>
                <th>Course</th>
                <th>Title</th>
                <th>Credits</th>
                <th>Grade</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>

    <div class="summary">
        <div class="sum-row"><strong>Cumulative GPA:</strong> <span>3.67</span></div>
        <div class="sum-row"><strong>Credits Attempted:</strong> <span>20.00</span></div>
        <div class="sum-row"><strong>Academic Standing:</strong> <span class="status-verified">Good Standing</span></div>
        <div class="sum-row"><strong>Enrollment Status:</strong> <span class="status-verified">Enrolled (Spring 2026)</span></div>
    </div>

    <div class="footer">
        This is an unofficial transcript generated from MyASU. For official records, please request an Official Transcript.<br>
        Arizona State University | Tempe, AZ 85287
    </div>
</body>
</html>
"""
    return html

def make_it_look_real(image_bytes):
    """ Filtro para simular foto de celular (Esencial para bypass) """
    if not HAS_PIL: return image_bytes
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        arr = np.array(img)
        
        # Ruido y desenfoque
        noise = np.random.normal(0, 8, arr.shape) # Menos ruido para texto
        img = Image.fromarray(np.clip(arr + noise, 0, 255).astype(np.uint8))
        img = img.filter(ImageFilter.GaussianBlur(radius=0.4)) # Desenfoque leve para que el texto siga legible
        
        # Rotación muy leve
        img = img.rotate(random.uniform(-0.8, 0.8), resample=Image.BICUBIC, expand=True, fillcolor='white')
        
        # Guardar
        out = io.BytesIO()
        img.save(out, format='JPEG', quality=88)
        return out.getvalue()
    except:
        return image_bytes

def generate_image(first_name, last_name, school_id='999'):
    try:
        from playwright.sync_api import sync_playwright
        html = generate_html(first_name, last_name)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 1000, 'height': 1100}) # Formato carta vertical
            page.set_content(html, wait_until='load')
            page.wait_for_timeout(500)
            ss = page.screenshot(type='png', full_page=True)
            browser.close()
        return make_it_look_real(ss)
    except Exception as e:
        raise Exception(f"Error: {e}")

if __name__ == '__main__':
    # Test
    with open("test_asu_transcript.jpg", "wb") as f:
        f.write(generate_image("Brian", "Test"))
