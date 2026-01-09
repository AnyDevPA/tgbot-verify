import logging
import httpx
import random
import unicodedata
import re
from . import config
from .img_generator import generate_image
from .name_generator import NameGenerator 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SheerIDVerifier:
    def __init__(self, verification_id):
        self.verification_id = verification_id
        self.client = httpx.Client(timeout=30.0)
        self.device_fingerprint = ''.join(random.choices('0123456789abcdef', k=32))

    @staticmethod
    def parse_verification_id(url: str):
        match = re.search(r"verificationId=([a-f0-9]+)", url)
        return match.group(1) if match else None

    def sanitize_email(self, email: str) -> str:
        if not email: return ""
        nfkd = unicodedata.normalize('NFKD', email)
        return "".join([c for c in nfkd if not unicodedata.combining(c)]).encode('ascii', 'ignore').decode('ascii')

    def verify(self):
        try:
            # --- DATOS ---
            name_data = NameGenerator.generate() 
            first = name_data['first_name']
            last = name_data['last_name']
            
            # --- CAMBIO CLAVE: USAR GMAIL PARA FORZAR DOCUMENTO ---
            # Si usamos @austinisd.org, pide código de verificación (emailLoop).
            # Si usamos @gmail.com, pide subir foto (docUpload).
            email_domains = ["gmail.com", "yahoo.com", "hotmail.com"]
            email = self.sanitize_email(f"{first}.{last}{random.randint(11,99)}@{random.choice(email_domains)}").lower()
            
            dob = f"19{random.randint(75,95)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
            school = config.SCHOOLS[config.DEFAULT_SCHOOL_ID]

            logger.info(f"👨‍🏫 TEACHER: {first} {last} | {email}")

            # --- PASO 1: Enviar Datos ---
            logger.info(">> Enviando Datos K-12...")
            
            payload = {
                "firstName": first,
                "lastName": last,
                "birthDate": dob,
                "email": email,
                "organization": {
                    "id": school['id'],
                    "name": school['name']
                },
                "deviceFingerprintHash": self.device_fingerprint,
                "metadata": {
                    **config.METADATA,
                    "verificationId": self.verification_id,
                    "refererUrl": f"{config.SHEERID_BASE_URL}/verify/{config.PROGRAM_ID}/"
                }
            }
            
            # Intentar primero como Teacher
            url_step1 = f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/collectTeacherPersonalInfo"
            resp1 = self.client.post(url_step1, json=payload)
            
            # Si falla el endpoint de Teacher, probar Faculty
            if resp1.status_code != 200:
                url_step1 = f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/collectFacultyPersonalInfo"
                resp1 = self.client.post(url_step1, json=payload)
                if resp1.status_code != 200:
                     raise Exception(f"Error Datos (Status {resp1.status_code}): {resp1.text}")

            data1 = resp1.json()
            current_step = data1.get("currentStep")
            logger.info(f"Paso 1 completado. Siguiente paso: {current_step}")

            # --- LÓGICA INTELIGENTE ---
            if current_step == "success":
                return {
                    "success": True, 
                    "pending": False, 
                    "redirect_url": data1.get("redirectUrl"),
                    "status": data1
                }
            
            elif current_step != "docUpload":
                # Si sigue saliendo emailLoop u otra cosa, es que SheerID se puso estricto
                raise Exception(f"Flujo inesperado: {current_step}. Error: {data1.get('errorIds')}")

            # --- PASO 2: Subir Credencial (Solo si pide docUpload) ---
            logger.info(">> Generando y Subiendo Credencial...")
            img_bytes = generate_image(first, last)
            
            url_upload = f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/docUpload"
            resp2 = self.client.post(url_upload, json={"files": [{"fileName": "teacher_id.jpg", "mimeType": "image/jpeg", "fileSize": len(img_bytes)}]})
            
            if resp2.status_code != 200:
                raise Exception(f"Error al iniciar subida: {resp2.text}")

            upload_data = resp2.json()
            if "documents" not in upload_data:
                raise Exception(f"Error crítico: API no devolvió URL de subida. Resp: {upload_data}")

            upload_link = upload_data["documents"][0]["uploadUrl"]
            
            # Subir archivo real a S3
            put_resp = self.client.put(upload_link, content=img_bytes, headers={"Content-Type": "image/jpeg"})
            if put_resp.status_code not in [200, 201]:
                 raise Exception(f"Error subiendo imagen a S3: {put_resp.status_code}")
            
            # Confirmar subida
            url_finish = f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/completeDocUpload"
            final_resp = self.client.post(url_finish)
            final_data = final_resp.json()
            
            return {
                "success": True, 
                "pending": True,
                "redirect_url": final_data.get("redirectUrl"),
                "status": final_data
            }

        except Exception as e:
            logger.error(f"K12 Error: {e}")
            return {"success": False, "message": str(e)}
