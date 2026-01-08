import random
from datetime import datetime
import io

# Importación segura de librerías
try:
    import numpy as np
    from PIL import Image, ImageFilter, ImageEnhance
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

def generate_html(first_name, last_name):
    """
    Genera una Tira de Materias (Horario) de la UNAM - Estilo SIAE Clásico
    """
    # Semestre actual UNAM (2026-2 es el próximo semestre típico para estas fechas)
    semestre = "2026-2"
    
    # Generar número de cuenta (9 dígitos)
    cuenta = f"31{random.randint(1000000, 9999999)}"
    
    # Lista de materias con horarios realistas
    materias = [
        {"clave": "1123", "gpo": "1105", "asignatura": "ÁLGEBRA SUPERIOR", "profesor": "DR. JORGE ALBERTO", "horario": "Lu Mi Vi 07:00-09:00", "salon": "A-101"},
        {"clave": "1124", "gpo": "1105", "asignatura": "CÁLCULO DIFERENCIAL", "profesor": "M.I. ROBERTO GÓMEZ", "horario": "Lu Mi Vi 09:00-11:00", "salon": "A-102"},
        {"clave": "1130", "gpo": "1101", "asignatura": "PROGRAMACIÓN AVANZADA", "profesor": "ING. LAURA MÉNDEZ", "horario": "Ma Ju 07:00-09:00", "salon": "L-201"},
        {"clave": "1208", "gpo": "1112", "asignatura": "MECÁNICA CLÁSICA", "profesor": "FIS. PEDRO RAMÍREZ", "horario": "Ma Ju 09:00-11:00", "salon": "B-004"},
        {"clave": "0052", "gpo": "1101", "asignatura": "INGLÉS IV", "profesor": "LIC. SARAH JONES", "horario": "Lu Mi Vi 11:00-13:00", "salon": "I-305"}
    ]

    filas_html = ""
    for m in materias:
        filas_html += f"""
        <tr class="data-row">
            <td class="center">{m['clave']}</td>
            <td class="center">{m['gpo']}</td>
            <td>
                <div class="asignatura">{m['asignatura']}</div>
                <div class="profesor">{m['profesor']}</div>
            </td>
            <td class="center">{m['horario']}</td>
            <td class="center">{m['salon']}</td>
            <td class="center">Ordinario</td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Verdana, Arial, sans-serif; background-color: white; margin: 20px; font-size: 11px; color: #333; }}
        
        /* Encabezado */
        .header {{ display: flex; justify-content: space-between; border-bottom: 3px solid #D59F0F; padding-bottom: 10px; margin-bottom: 15px; }}
        .unam-title {{ font-weight: bold; font-size: 16px; color: #002B7A; }}
        .sub-title {{ font-size: 12px; color: #555; margin-top: 4px; }}
        
        /* Caja de Datos del Alumno */
        .info-box {{ background-color: #E6EEF8; border: 1px solid #B0C4DE; padding: 10px; margin-bottom: 15px; border-radius: 4px; }}
        .info-grid {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; }}
        .label {{ font-weight: bold; color: #002B7A; font-size: 10px; }}
        .value {{ font-weight: bold; color: #000; font-size: 11px; }}
        
        /* Tabla */
        table {{ width: 100%; border-collapse: collapse; border: 1px solid #ccc; }}
        th {{ background-color: #002B7A; color: white; padding: 8px; font-size: 10px; text-align: left; border: 1px solid #001A4A; }}
        td {{ padding: 6px; border: 1px solid #ddd; vertical-align: top; }}
        
        .data-row:nth-child(even) {{ background-color: #f9f9f9; }}
        .center {{ text-align: center; }}
        .asignatura {{ font-weight: bold; color: #000; }}
        .profesor {{ font-size: 9px; color: #555; font-style: italic; margin-top: 2px; }}
        
        /* Pie de página */
        .footer {{ margin-top: 20px; font-size: 9px; color: #777; text-align: center; border-top: 1px solid #ccc; padding-top: 10px; }}
        
        /* Sello Digital Simulado */
        .sello {{ font-family: "Courier New", monospace; font-size: 8px; color: #999; word-break: break-all; margin-top: 10px; border: 1px dashed #ccc; padding: 5px; }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <div class="unam-title">UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO</div>
            <div class="sub-title">SISTEMA INTEGRAL DE ADMINISTRACIÓN ESCOLAR (SIAE)</div>
        </div>
        <div style="text-align: right;">
            <div class="unam-title" style="color:#D59F0F">DGAE</div>
            <div class="sub-title">Tira de Asignaturas</div>
        </div>
    </div>

    <div class="info-box">
        <div class="info-grid">
            <div><span class="label">NÚMERO DE CUENTA:</span><br><span class="value">{cuenta}</span></div>
            <div><span class="label">NOMBRE:</span><br><span class="value">{last_name.upper()}, {first_name.upper()}</span></div>
            <div><span class="label">PLANTEL:</span><br><span class="value">FACULTAD DE INGENIERÍA</span></div>
            <div><span class="label">CARRERA:</span><br><span class="value">INGENIERÍA EN COMPUTACIÓN</span></div>
            <div><span class="label">SEMESTRE:</span><br><span class="value">{semestre}</span></div>
            <div><span class="label">ESTATUS:</span><br><span class="value" style="color:green">REINSCRITO</span></div>
        </div>
    </div>

    <table>
        <thead>
            <tr>
                <th width="5%" class="center">CLAVE</th>
                <th width="5%" class="center">GRUPO</th>
                <th width="40%">ASIGNATURA / PROFESOR</th>
                <th width="20%" class="center">HORARIO</th>
                <th width="10%" class="center">SALÓN</th>
                <th width="10%" class="center">MOVIMIENTO</th>
            </tr>
        </thead>
        <tbody>
            {filas_html}
        </tbody>
    </table>

    <div class="sello">
        SELLO DIGITAL DE INSCRIPCIÓN: 
        {random.randint(1000,9999)}-X{random.randint(1000,9999)}-ABC{random.randint(10,99)}-UNAM-{random.randint(100000,999999)}
        <br>Este documento es válido para trámites escolares internos.
    </div>

    <div class="footer">
        Fecha de consulta: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} | DGAE-SIAE
    </div>
</body>
</html>
"""
    return html

def make_it_look_real(image_bytes):
    """
    Filtro de 'Foto de Pantalla' (Esencial para engañar a la IA)
    """
    if not HAS_PIL: return image_bytes
    
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        arr = np.array(img)
        
        # 1. Ruido (Simular mala calidad de cámara)
        noise = np.random.normal(0, 15, arr.shape)
        img = Image.fromarray(np.clip(arr + noise, 0, 255).astype(np.uint8))
        
        # 2. Desenfoque y Rotación (Efecto "Foto chueca")
        img = img.filter(ImageFilter.GaussianBlur(radius=0.6))
        img = img.rotate(random.uniform(-1.0, 1.0), resample=Image.BICUBIC, expand=True, fillcolor='white')
        
        # 3. Compresión JPEG agresiva
        out = io.BytesIO()
        img.save(out, format='JPEG', quality=75)
        return out.getvalue()
    except:
        return image_bytes

def generate_image(first_name, last_name, school_id='999'):
    try:
        from playwright.sync_api import sync_playwright
        html = generate_html(first_name, last_name)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            # Viewport ancho para que quepa la tabla bien
            page = browser.new_page(viewport={'width': 1024, 'height': 800})
            page.set_content(html, wait_until='load')
            page.wait_for_timeout(500)
            ss = page.screenshot(type='png', full_page=True)
            browser.close()
        return make_it_look_real(ss)
    except Exception as e:
        raise Exception(f"Error: {e}")

# Funciones de compatibilidad para evitar crash
def generate_psu_id(): return "310000000"
def generate_psu_email(f, l): return f"{f}.{l}@comunidad.unam.mx"
