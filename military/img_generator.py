import random
from datetime import datetime
import io

# Importación segura de librerías de imagen
try:
    import numpy as np
    from PIL import Image, ImageFilter, ImageEnhance, ImageOps
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

def generate_dd214_html(first_name, last_name):
    """
    Genera una réplica del Formulario DD-214 (Certificate of Release or Discharge from Active Duty)
    """
    # --- DATOS SIMULADOS ---
    # Generar fechas lógicas (Retiro hace unos años)
    year_retire = random.randint(2018, 2024)
    discharge_date = f"{year_retire}-05-{random.randint(10,28)}"
    entry_date = f"{year_retire-4}-02-{random.randint(10,28)}" # 4 años de servicio
    
    # Datos personales
    middle_init = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    ssn = f"{random.randint(100,999)}-{random.randint(10,99)}-{random.randint(1000,9999)}"
    dob = f"19{random.randint(85,99)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
    
    # Ramas y Rangos
    branches = ["ARMY", "NAVY", "AIR FORCE", "MARINE CORPS"]
    branch = random.choice(branches)
    
    pay_grades = ["E-4", "E-5", "E-6"]
    grade = random.choice(pay_grades)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body {{ 
            font-family: Arial, Helvetica, sans-serif; 
            background-color: #fcfcfc; 
            margin: 0; padding: 40px; 
            font-size: 10px;
            color: #000;
        }}
        
        /* Contenedor principal que simula la hoja */
        .page {{
            width: 800px;
            border: 2px solid black;
            padding: 2px;
            margin: auto;
        }}

        /* Título del documento */
        .header {{
            text-align: center;
            font-weight: bold;
            font-size: 14px;
            border-bottom: 2px solid black;
            padding: 5px;
            text-transform: uppercase;
        }}

        /* La grilla del formulario */
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        td {{
            border: 1px solid black;
            padding: 2px 4px;
            vertical-align: top;
            height: 25px;
        }}

        /* Estilos de texto */
        .label {{
            font-size: 8px;
            font-weight: bold;
            display: block;
            margin-bottom: 2px;
        }}

        .typewriter {{
            font-family: 'Courier New', Courier, monospace;
            font-size: 12px;
            font-weight: bold;
            color: #111;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .section-title {{
            background-color: #ddd;
            font-weight: bold;
            text-align: center;
            border-top: 2px solid black;
            border-bottom: 2px solid black;
            padding: 2px;
            font-size: 11px;
        }}

        /* Marca de agua de copia */
        .watermark {{
            position: absolute;
            top: 40%;
            left: 30%;
            font-size: 100px;
            color: rgba(0,0,0,0.05);
            transform: rotate(-45deg);
            z-index: 0;
            pointer-events: none;
        }}
    </style>
</head>
<body>
    <div class="page">
        <div class="header">
            CERTIFICATE OF RELEASE OR DISCHARGE FROM ACTIVE DUTY
        </div>

        <div class="watermark">MEMBER - 4</div>

        <table>
            <tr>
                <td width="50%">
                    <span class="label">1. NAME (Last, First, Middle)</span>
                    <span class="typewriter">{last_name.upper()}, {first_name.upper()} {middle_init}.</span>
                </td>
                <td width="15%">
                    <span class="label">2. DEPARTMENT</span>
                    <span class="typewriter">{branch}</span>
                </td>
                <td width="35%">
                    <span class="label">3. SOCIAL SECURITY NUMBER</span>
                    <span class="typewriter">{ssn}</span>
                </td>
            </tr>
            <tr>
                <td>
                    <span class="label">4. GRADE, RATE OR RANK</span>
                    <span class="typewriter">{grade}</span>
                </td>
                <td colspan="2">
                    <span class="label">5. PAY GRADE</span>
                    <span class="typewriter">{grade}</span>
                </td>
            </tr>
             <tr>
                <td>
                    <span class="label">5. DATE OF BIRTH (YYYY-MM-DD)</span>
                    <span class="typewriter">{dob}</span>
                </td>
                <td colspan="2">
                    <span class="label">6. RESERVE OBLIG. TERM. DATE</span>
                    <span class="typewriter">N/A</span>
                </td>
            </tr>
            <tr>
                <td colspan="3">
                    <span class="label">7. PLACE OF ENTRY INTO ACTIVE DUTY</span>
                    <span class="typewriter">MEPS LOS ANGELES, CA</span>
                </td>
            </tr>
            <tr>
                <td colspan="3">
                    <span class="label">8. LAST DUTY ASSIGNMENT AND MAJOR COMMAND</span>
                    <span class="typewriter">1ST BATTALION, 5TH INFANTRY REGIMENT</span>
                </td>
            </tr>
        </table>

        <div class="section-title">RECORD OF SERVICE</div>

        <table>
            <tr>
                <td width="60%"><span class="label">9. COMMAND TO WHICH TRANSFERRED</span><br><span class="typewriter">US ARMY RESERVE CONTROL GROUP</span></td>
                <td width="40%"><span class="label">10. SGLI COVERAGE AMOUNT</span><br><span class="typewriter">$400,000</span></td>
            </tr>
        </table>

        <table>
            <tr>
                <td width="50%" style="background:#eee; font-weight:bold; text-align:center;">12. RECORD OF SERVICE</td>
                <td width="16%" style="text-align:center;">YEAR(S)</td>
                <td width="16%" style="text-align:center;">MONTH(S)</td>
                <td width="16%" style="text-align:center;">DAY(S)</td>
            </tr>
            <tr>
                <td><span class="label">a. DATE ENTERED AD THIS PERIOD</span></td>
                <td class="typewriter" style="text-align:center">{entry_date.split('-')[0]}</td>
                <td class="typewriter" style="text-align:center">{entry_date.split('-')[1]}</td>
                <td class="typewriter" style="text-align:center">{entry_date.split('-')[2]}</td>
            </tr>
            <tr>
                <td><span class="label">b. SEPARATION DATE THIS PERIOD</span></td>
                <td class="typewriter" style="text-align:center">{discharge_date.split('-')[0]}</td>
                <td class="typewriter" style="text-align:center">{discharge_date.split('-')[1]}</td>
                <td class="typewriter" style="text-align:center">{discharge_date.split('-')[2]}</td>
            </tr>
            <tr>
                <td><span class="label">c. NET ACTIVE SERVICE THIS PERIOD</span></td>
                <td class="typewriter" style="text-align:center">04</td>
                <td class="typewriter" style="text-align:center">00</td>
                <td class="typewriter" style="text-align:center">00</td>
            </tr>
        </table>

        <br>
        <table>
            <tr>
                <td height="60">
                     <span class="label">13. DECORATIONS, MEDALS, BADGES, CITATIONS AND CAMPAIGN RIBBONS AWARDED OR AUTHORIZED</span>
                     <span class="typewriter">NATIONAL DEFENSE SERVICE MEDAL // GLOBAL WAR ON TERRORISM SERVICE MEDAL // ARMY SERVICE RIBBON // MARKSMANSHIP QUAL BADGE WITH RIFLE BAR //</span>
                </td>
            </tr>
        </table>

        <br>
        <div style="border: 2px solid black; padding: 5px;">
            <div style="display:flex; justify-content:space-between;">
                <div style="width:45%">
                    <span class="label">23. TYPE OF SEPARATION</span>
                    <span class="typewriter" style="font-size:14px; font-weight:900;">DISCHARGE</span>
                </div>
                <div style="width:45%">
                    <span class="label">24. CHARACTER OF SERVICE (Includes upgrades)</span>
                    <span class="typewriter" style="font-size:14px; font-weight:900;">HONORABLE</span>
                </div>
            </div>
            <div style="border-top:1px solid black; margin-top:5px; padding-top:5px;">
                 <span class="label">28. NARRATIVE REASON FOR SEPARATION</span>
                 <span class="typewriter">COMPLETION OF REQUIRED ACTIVE SERVICE</span>
            </div>
        </div>

        <div style="text-align:center; font-size:9px; margin-top:10px;">
            <strong>DD FORM 214, AUG 2009</strong> &nbsp;&nbsp;&nbsp; PREVIOUS EDITIONS ARE OBSOLETE.
        </div>
    </div>
</body>
</html>
"""
    return html

def make_it_look_scanned(image_bytes):
    """
    Convierte la imagen digital perfecta en un 'Scan' de gobierno (Blanco y Negro, Ruido)
    """
    if not HAS_PIL: return image_bytes
    
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        # 1. Convertir a Escala de Grises (Documento de gobierno)
        img = img.convert("L")
        
        img_array = np.array(img)

        # 2. Agregar Ruido de Escáner (Granulado)
        noise = np.random.normal(0, 8, img_array.shape)
        noisy_img = np.clip(img_array + noise, 0, 255).astype(np.uint8)
        img = Image.fromarray(noisy_img)

        # 3. Rotación muy leve (Mal alineado en el escáner)
        angle = random.uniform(-0.6, 0.6)
        img = img.rotate(angle, resample=Image.BICUBIC, expand=True, fillcolor=255) # Fill con blanco

        # 4. Desenfoque ligero (Scanner viejo)
        img = img.filter(ImageFilter.GaussianBlur(radius=0.4))
        
        # 5. Aumentar contraste (Efecto fotocopia)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5)

        # Guardar como JPEG comprimido
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=75)
        return output.getvalue()
        
    except Exception as e:
        print(f"Error filtro scan: {e}")
        return image_bytes

def generate_image(first_name, last_name, school_id='999'):
    # Nota: school_id se ignora aquí, se usa branch en el HTML generator
    try:
        from playwright.sync_api import sync_playwright
        html_content = generate_dd214_html(first_name, last_name)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 850, 'height': 1100})
            page.set_content(html_content, wait_until='load')
            page.wait_for_timeout(500)
            
            screenshot_bytes = page.screenshot(type='png', full_page=True)
            browser.close()

        return make_it_look_scanned(screenshot_bytes)

    except Exception as e:
        raise Exception(f"Error generando DD-214: {e}")

# Funciones Dummy
def generate_psu_id(): return "000000000"
def generate_psu_email(f, l): return f"{f}.{l}@gmail.com"
