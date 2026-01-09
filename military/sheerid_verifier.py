# military/sheerid_verifier.py
import logging
import httpx
import random
import time
from . import config
from .utils import get_military_dates
from utils.name_generator import NameGenerator  # Usamos el generador global
from .img_generator import generate_image # Necesitas crear este archivo tmb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SheerIDVerifier:
    def __init__(self, verification_id):
        self.verification_id = verification_id
        self.client = httpx.Client(timeout=30.0)
        # Fingerprint aleatorio
        self.device_fingerprint = ''.join(random.choices('0123456789abcdef', k=32))

    def verify(self):
        try:
            # --- 0. PREPARAR DATOS ---
            name_data = NameGenerator.generate()
            first_name = name_data['first_name']
            last_name = name_data['last_name']
            # Email militar suele ser personal (gmail/yahoo), no .edu
            email = f"{first_name}.{last_name}{random.randint(10,99)}@gmail.com".lower()
            
            birth_date, discharge_date = get_military_dates()
            branch = random.choice(config.MILITARY_BRANCHES)

            logger.info(f"🪖 INICIANDO MILITARY: {first_name} {last_name} | {branch['name']}")
            logger.info(f"📅 Nacimiento: {birth_date} | Retiro: {discharge_date}")

            # --- PASO 1: collectMilitaryStatus (SEGÚN README) ---
            logger.info(">> Paso 1: Enviando estatus VETERAN...")
            step1_url = f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/collectMilitaryStatus"
            
            resp1 = self.client.post(
                step1_url, 
                json={"status": "VETERAN"}, # Obligatorio según README
                headers={"Content-Type": "application/json"}
            )
            
            if resp1.status_code != 200:
                raise Exception(f"Fallo Paso 1: {resp1.text}")
            
            data1 = resp1.json()
            submission_url = data1.get("submissionUrl")
            if not submission_url:
                raise Exception("No se recibió submissionUrl del Paso 1")

            # --- PASO 2: collectInactiveMilitaryPersonalInfo ---
            logger.info(">> Paso 2: Enviando Datos Personales...")
            
            payload_step2 = {
                "firstName": first_name,
                "lastName": last_name,
                "birthDate": birth_date,
                "email": email,
                "phoneNumber": "",
                "organization": {
                    "id": branch["id"],
                    "name": branch["name"]
                },
                "dischargeDate": discharge_date, # CAMPO CLAVE
                "locale": "en-US",
                "country": "US",
                "deviceFingerprintHash": self.device_fingerprint,
                "metadata": {
                    "marketConsentValue": False,
                    "refererUrl": "",
                    "verificationId": "",
                    "flags": config.METADATA_FLAGS,
                    "submissionOptIn": config.SUBMISSION_OPT_IN
                }
            }

            resp2 = self.client.post(
                submission_url,
                json=payload_step2,
                headers={"Content-Type": "application/json"}
            )

            if resp2.status_code != 200:
                raise Exception(f"Fallo Paso 2: {resp2.text}")

            data2 = resp2.json()
            logger.info("✅ Datos aceptados. Preparando documento...")

            # --- PASO 3: Subir Documento (DD-214) ---
            # OJO: Aquí necesitas un generador de DD-214, no de estudiante.
            # Por ahora usaremos generate_image genérico, pero te lo van a rechazar si no parece militar.
            img_bytes = generate_image(first_name, last_name)
            
            # Obtener URL de subida
            step3_url = f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/docUpload"
            resp3 = self.client.post(
                step3_url,
                json={"files": [{"fileName": "DD214_Scan.jpg", "mimeType": "image/jpeg", "fileSize": len(img_bytes)}]}
            )
            upload_data = resp3.json()
            upload_url = upload_data["documents"][0]["uploadUrl"]

            # Subir archivo
            self.client.put(upload_url, content=img_bytes, headers={"Content-Type": "image/jpeg"})

            # Completar
            confirm_url = f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/completeDocUpload"
            final_resp = self.client.post(confirm_url)
            
            return {
                "success": True, 
                "message": "Verificación Militar Enviada", 
                "details": final_resp.json()
            }

        except Exception as e:
            logger.error(f"Error Militar: {e}")
            return {"success": False, "message": str(e)}
