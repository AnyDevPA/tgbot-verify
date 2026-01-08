import random
from datetime import datetime
import io
import sys

# Importación segura de librerías de imagen
try:
    import numpy as np
    from PIL import Image, ImageFilter, ImageEnhance
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

def generate_html(first_name, last_name):
    """
    Genera un Comprobante de Inscripción de la UNAM (Estilo DGAE-SIAE)
    """
    # Fecha actual en formato español
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    now = datetime.now()
    fecha_impresion = f"{now.day} de {meses[now.month-1]} de {now.year}"
    hora_impresion = now.strftime("%H:%M:%S")
    
    # Generar número de cuenta UNAM (9 dígitos típicos: 3 o 4 al inicio + random)
    cuenta = f"32{random.randint(1000000, 9999999)}"
    
    # Materias típicas de tronco común
    materias = [
        {"clave": "1123", "asignatura": "ÁLGEBRA", "grupo": "1105", "creditos": "8"},
        {"clave": "1124", "asignatura": "CÁLCULO Y GEOMETRÍA ANALÍTICA", "grupo": "1105", "creditos": "12"},
        {"clave": "1128", "asignatura": "QUÍMICA", "grupo": "1112", "creditos": "10"},
        {"clave": "1130", "asignatura": "REDACCIÓN Y EXPOSICIÓN DE TEMAS", "grupo": "1101", "creditos": "6"},
        {"clave": "0052", "asignatura": "INGLES I", "grupo": "1101", "creditos": "0"}
    ]

    filas_html = ""
    for m in materias:
        filas_html += f"""
        <tr>
            <td style="text-align: center;">{m['clave']}</td>
            <td>{m['asignatura']}</td>
            <td style="text-align: center;">{m['grupo']}</td>
            <td style="text-align: center;">{m['creditos']}</td>
            <td style="text-align: center;">ORDINARIO</td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; background-color: white; margin: 40px; color: #333; font-size: 12px; }}
        
        /* Cabecera UNAM */
        .header {{ display: flex; align-items: center; border-bottom: 2px solid #D59F0F; padding-bottom: 10px; margin-bottom: 20px; }}
        .unam-logo {{ font-size: 30px; font-weight: bold; color: #002B7A; margin-right: 20px; border: 2px solid #002B7A; padding: 5px 10px; border-radius: 5px; }}
        .header-text {{ color: #002B7A; }}
        .header-title {{ font-size: 16px; font-weight: bold; }}
        .header-sub {{ font-size: 12px; }}
        
        /* Título del Documento */
        .doc-title {{ text-align: center; font-size: 18px; font-weight: bold; margin: 20px 0; color: #000; text-transform: uppercase; }}
        
        /* Datos del Alumno */
        .student-box {{ border: 1px solid #ccc; padding: 10px; margin-bottom: 20px; background-color: #fcfcfc; }}
        .data-row {{ display: flex; margin-bottom: 5px; }}
        .label {{ font-weight: bold; width: 150px; color: #002B7A; }}
        .value {{ font-weight: bold; color: #000; }}
        
        /* Tabla de Materias */
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 11px; }}
        th {{ background-color: #002B7A; color: white; padding: 8px; border: 1px solid #002B7A; }}
        td {{ border: 1px solid #ccc; padding: 6px; }}
        
        /* Pie de página */
        .footer {{ font-size: 10px; color: #666; margin-top: 40px; border-top: 1px solid #ccc; padding-top: 10px; display: flex; justify-content: space-between; }}
        
        /* Marca de agua simulada */
        .watermark {{ position: fixed; top: 40%; left: 20%; transform: rotate(-45deg); font-size: 100px; color: rgba(0,0,0,0.03); font-weight: bold; z-index: -1; }}
    </style>
</head>
<body>
    <div class="watermark">UNAM DGAE</div>

    <div class="header">
        <div class="unam-logo">UNAM</div>
        <div class="header-text">
            <div class="header-title">UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO</div>
            <div class="header-sub">DIRECCIÓN GENERAL DE ADMINISTRACIÓN ESCOLAR</div>
            <div class="header-sub">SISTEMA INTEGRAL DE ADMINISTRACIÓN ESCOLAR</div>
        </div>
    </div>

    <div class="doc-title">COMPROBANTE DE INSCRIPCIÓN<br><span style="font-size:14px">CICLO ESCOLAR 2025-2026 / 1</span></div>

    <div class="student-box">
        <div class="data-row"><span class="label">NÚMERO DE CUENTA:</span> <span class="value">{cuenta}</span></div>
        <div class="data-row"><span class="label">NOMBRE DEL ALUMNO:</span> <span class="value">{last_name.upper()} {first_name.upper()}</span></div>
        <div class="data-row"><span class="label">PLANTEL:</span> <span class="value">FACULTAD DE INGENIERÍA</span></div>
        <div class="data-row"><span class="label">CARRERA:</span> <span class="value">INGENIERÍA EN COMPUTACIÓN</span></div>
        <div class="data-row"><span class="label">SITUACIÓN:</span> <span class="value" style="color:green">INSCRITO</span></div>
    </div>

    <table>
        <thead>
            <tr>
                <th>CLAVE</th>
                <th>ASIGNATURA</th>
                <th>GRUPO</th>
                <th>CRÉDITOS</th>
                <th>TIPO INSCRIPCIÓN</th>
            </tr>
        </thead>
        <tbody>
            {filas_html}
        </tbody>
    </table>

    <div style="font-size: 11px; margin-top: 10px;">
        <strong>TOTAL DE CRÉDITOS INSCRITOS:</strong> 36
    </div>

    <div class="footer">
        <div>
            La información contenida en este documento es de carácter informativo.<br>
            Fuente: DGAE-SIAE WEB
        </div>
        <div style="text-align: right;">
            Fecha de impresión: {fecha_impresion}<br>
            Hora: {hora_impresion}
        </div>
    </div>
</body>
</html>
"""
    return html

def make_it_look_real(image_bytes):
    """
    Filtro 'Foto de Celular' para evitar detección de bot.
    """
    if not HAS_PIL:
        return image_bytes # Devuelve original si falla librería
    
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img_array = np.array(img)
        
        # 1. Ruido (Granulado)
        noise = np.random.normal(0, 10, img_array.shape) 
        noisy_img = np.clip(img_array + noise, 0, 255).astype(np.uint8)
        img = Image.fromarray(noisy_img)

        # 2. Desenfoque leve
        img = img.filter(ImageFilter.GaussianBlur(radius=0.5))

        # 3. Rotación sutil
        angle = random.uniform(-0.8, 0.8)
        img = img.rotate(angle, resample=Image.BICUBIC, expand=True, fillcolor='white')

        # 4. Ajustes finales
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.96) # Un poco grisáceo (papel)
        
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=85)
        return output.getvalue()
        
    except Exception as e:
        print(f"Error filtro: {e}")
        return image_bytes

def generate_image(first_name, last_name, school_id='999'):
    try:
        from playwright.sync_api import sync_playwright
        html_content = generate_html(first_name, last_name)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            # Tamaño A4 vertical aproximado
            page = browser.new_page(viewport={'width': 850, 'height': 1100})
            page.set_content(html_content, wait_until='load')
            page.wait_for_timeout(500)
            
            screenshot_bytes = page.screenshot(type='png', full_page=True)
            browser.close()

        return make_it_look_real(screenshot_bytes)

    except Exception as e:
        raise Exception(f"Error generando: {e}")

# Funciones Dummy para que el bot no se queje (Importante no borrarlas)
def generate_psu_id(): return "320000000"
def generate_psu_email(f, l): return f"{f}.{l}@comunidad.unam.mx"
