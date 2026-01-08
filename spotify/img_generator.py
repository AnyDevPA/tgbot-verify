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
    Genera Tira de Materias UNAM corregida para pasar el filtro de nombre exacto.
    """
    semestre = "2026-2"
    cuenta = f"31{random.randint(1000000, 9999999)}"
    
    # Materias
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
        body {{ font-family: Arial, Helvetica, sans-serif; background-color: white; margin: 30px; font-size: 11px; color: #333; }}
        
        /* HEADER MODIFICADO PARA MATCH EXACTO */
        .header {{ border-bottom: 3px solid #D59F0F; padding-bottom: 15px; margin-bottom: 20px; }}
        .unam-title {{ font-weight: 900; font-size: 18px; color: #002B7A; letter-spacing: 0.5px; }}
        .sub-title {{ font-size: 13px; color: #555; margin-top: 5px; font-weight: bold; }}
        
        .info-box {{ background-color: #F0F4F8; border: 1px solid #B0C4DE; padding: 15px; margin-bottom: 20px; border-radius: 4px; }}
        .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
        .label {{ font-weight: bold; color: #002B7A; font-size: 10px; text-transform: uppercase; }}
        .value {{ font-weight: bold; color: #000; font-size: 12px; }}
        
        table {{ width: 100%; border-collapse: collapse; border: 1px solid #ccc; }}
        th {{ background-color: #002B7A; color: white; padding: 10px; font-size: 10px; text-align: left; }}
        td {{ padding: 8px; border: 1px solid #ddd; vertical-align: top; }}
        
        .data-row:nth-child(even) {{ background-color: #f9f9f9; }}
        .center {{ text-align: center; }}
        .asignatura {{ font-weight: bold; font-size: 11px; }}
        .profesor {{ font-size: 9px; color: #666; margin-top: 2px; }}
        
        .footer {{ margin-top: 30px; font-size: 9px; color: #777; text-align: center; border-top: 1px solid #eee; padding-top: 10px; }}
    </style>
</head>
<body>
    <div class="header">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div class="unam-title">UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO (UNAM)</div>
                <div class="sub-title">DIRECCIÓN GENERAL DE ADMINISTRACIÓN ESCOLAR (DGAE)</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:24px; font-weight:bold; color:#D59F0F; border:2px solid #D59F0F; padding:2px 8px; border-radius:4px;">SIAE</div>
            </div>
        </div>
    </div>

    <div class="info-box">
        <div class="info-grid">
            <div><span class="label">Alumno:</span><br><span class="value">{last_name.upper()} {first_name.upper()}</span></div>
            <div><span class="label">N° Cuenta:</span><br><span class="value">{cuenta}</span></div>
            <div><span class="label">Plantel / Campus:</span><br><span class="value">CIUDAD UNIVERSITARIA</span></div>
            <div><span class="label">Carrera:</span><br><span class="value">LICENCIATURA EN INFORMÁTICA</span></div>
            <div><span class="label">Ciclo Escolar:</span><br><span class="value">{semestre}</span></div>
            <div><span class="label">Situación:</span><br><span class="value" style="color:#008000">✔ REINSCRITO</span></div>
        </div>
    </div>

    <div style="margin-bottom:10px; font-weight:bold; font-size:12px; color:#002B7A;">TIRA DE ASIGNATURAS INSCRITAS</div>

    <table>
        <thead>
            <tr>
                <th width="8%" class="center">Cve</th>
                <th width="8%" class="center">Gpo</th>
                <th>Asignatura</th>
                <th width="20%" class="center">Horario</th>
                <th width="10%" class="center">Salón</th>
                <th width="10%" class="center">Estatus</th>
            </tr>
        </thead>
        <tbody>
            {filas_html}
        </tbody>
    </table>

    <div class="footer">
        Este documento es una representación impresa de la información escolar del alumno.<br>
        SIAE - Sistema Integral de Administración Escolar | UNAM
        <br>Fecha de emisión: {datetime.now().strftime('%d/%m/%Y')}
    </div>
</body>
</html>
"""
    return html

def make_it_look_real(image_bytes):
    """ Filtro de Realismo (Esencial) """
    if not HAS_PIL: return image_bytes
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        arr = np.array(img)
        
        # 1. Ruido
        noise = np.random.normal(0, 12, arr.shape)
        img = Image.fromarray(np.clip(arr + noise, 0, 255).astype(np.uint8))
        
        # 2. Desenfoque y Rotación muy leves
        img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
        img = img.rotate(random.uniform(-0.5, 0.5), resample=Image.BICUBIC, expand=True, fillcolor='white')
        
        # 3. Compresión
        out = io.BytesIO()
        img.save(out, format='JPEG', quality=82)
        return out.getvalue()
    except:
        return image_bytes

def generate_image(first_name, last_name, school_id='999'):
    try:
        from playwright.sync_api import sync_playwright
        html = generate_html(first_name, last_name)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 900, 'height': 1000})
            page.set_content(html, wait_until='load')
            page.wait_for_timeout(500)
            ss = page.screenshot(type='png', full_page=True)
            browser.close()
        return make_it_look_real(ss)
    except Exception as e:
        raise Exception(f"Error: {e}")

# Compatibilidad
def generate_psu_id(): return "310000000"
def generate_psu_email(f, l): return f"{f}.{l}@comunidad.unam.mx"
