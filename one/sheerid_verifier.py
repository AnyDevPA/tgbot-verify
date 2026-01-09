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
        # Intentamos un fingerprint más complejo
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
            name_data = NameGenerator.generate() 
            first = name_data['first_name']
            last = name_data['last_name']
            
            # ESTRATEGIA ANTI-FRAUDE:
            # 1. Evitar Gmail (muy quemado). Usar Outlook/Yahoo.
            # 2. Formato más limpio: nombre.apellido@... en lugar de nombre.apellido9999
            domains = ["outlook.com", "yahoo.com", "icloud.com"]
            clean_email = f"{first}.{last}@{random.choice(domains)}".lower()
            email = self.sanitize_email(clean_email)
            
            # Fechas realistas para estudiante online (pueden ser mayores)
            dob = f"19{random.randint(90,99)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
            school = config.SCHOOLS[config.DEFAULT_SCHOOL_ID]

            logger.info(f"🎓 STUDENT (SNHU): {first} {last} | {email}")

            # PASO 1
            payload = {
                "firstName": first,
                "lastName": last,
                "birthDate": dob,
                "email": email,
                "organization": {"id": school['id'], "name": school['name']},
                "deviceFingerprintHash": self.device_fingerprint,
                "metadata": {**config.METADATA, "verificationId": self.verification_id, "refererUrl": f"{config.SHEERID_BASE_URL}/verify/{config.PROGRAM_ID}/"}
            }
            
            url_step1 = f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/collectStudentPersonalInfo"
            resp1 = self.client.post(url_step1, json=payload)
            data1 = resp1.json()
            current_step = data1.get("currentStep")

            # --- DIAGNÓSTICO DE FRAUDE ---
            if current_step == "error":
                error_ids = data1.get("errorIds", [])
                logger.error(f"❌ RECHAZADO: {error_ids}")
                return {"success": False, "message": f"SheerID bloqueó la solicitud: {error_ids}"}

            if current_step == "emailLoop":
                self.client.delete(f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/emailLoop")
                status = self.client.get(f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}").json()
                current_step = status.get("currentStep")

            if current_step == "success":
                 return {"success": True, "pending": False, "redirect_url": data1.get("redirectUrl"), "status": data1}

            # PASO 2: Subir Credencial SNHU
            if current_step == "docUpload":
                logger.info(">> Subiendo Credencial SNHU...")
                img_bytes = generate_image(first, last)
                
                url_upload = f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/docUpload"
                resp2 = self.client.post(url_upload, json={"files": [{"fileName": "student_id.jpg", "mimeType": "image/jpeg", "fileSize": len(img_bytes)}]})
                
                if "documents" in resp2.json():
                    upload_link = resp2.json()["documents"][0]["uploadUrl"]
                    self.client.put(upload_link, content=img_bytes, headers={"Content-Type": "image/jpeg"})
                    
                    final = self.client.post(f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/completeDocUpload").json()
                    return {"success": True, "pending": True, "redirect_url": final.get("redirectUrl"), "status": final}
            
            return {"success": False, "message": f"Estado desconocido: {current_step}"}

        except Exception as e:
            return {"success": False, "message": str(e)}
