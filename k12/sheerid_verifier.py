import logging
import httpx
import random
import unicodedata
import re  # <--- IMPORTANTE
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

    # --- AGREGADO: EL BOT NECESITA ESTO ---
    @staticmethod
    def parse_verification_id(url: str):
        match = re.search(r"verificationId=([a-f0-9]+)", url)
        return match.group(1) if match else None
    # --------------------------------------

    def sanitize_email(self, email: str) -> str:
        if not email: return ""
        nfkd = unicodedata.normalize('NFKD', email)
        return "".join([c for c in nfkd if not unicodedata.combining(c)]).encode('ascii', 'ignore').decode('ascii')

    def verify(self):
        try:
            name_data = NameGenerator.generate() 
            first = name_data['first_name']
            last = name_data['last_name']
            
            email = self.sanitize_email(f"{first}.{last}@austinisd.org").lower()
            dob = f"19{random.randint(75,95)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
            school = config.SCHOOLS[config.DEFAULT_SCHOOL_ID]

            logger.info(f"👨‍🏫 TEACHER: {first} {last} | {school['name']}")

            # PASO 1
            logger.info(">> Enviando Datos K-12...")
            payload = {
                "firstName": first,
                "lastName": last,
                "birthDate": dob,
                "email": email,
                "organization": {"id": school['id'], "name": school['name']},
                "deviceFingerprintHash": self.device_fingerprint,
                "metadata": {**config.METADATA, "verificationId": self.verification_id, "refererUrl": f"{config.SHEERID_BASE_URL}/verify/{config.PROGRAM_ID}/"}
            }
            
            url_step1 = f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/collectTeacherPersonalInfo"
            resp1 = self.client.post(url_step1, json=payload)
            if resp1.status_code != 200:
                url_step1 = f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/collectFacultyPersonalInfo"
                resp1 = self.client.post(url_step1, json=payload)
                if resp1.status_code != 200: raise Exception(f"Error Datos: {resp1.text}")

            # PASO 2
            logger.info(">> Subiendo Credencial...")
            img_bytes = generate_image(first, last)
            
            url_upload = f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/docUpload"
            resp2 = self.client.post(url_upload, json={"files": [{"fileName": "teacher_id.jpg", "mimeType": "image/jpeg", "fileSize": len(img_bytes)}]})
            
            upload_link = resp2.json()["documents"][0]["uploadUrl"]
            self.client.put(upload_link, content=img_bytes, headers={"Content-Type": "image/jpeg"})
            
            # Confirmar
            url_finish = f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/completeDocUpload"
            final = self.client.post(url_finish).json()
            
            # --- RETORNO FORMATO BOT ---
            return {
                "success": True, 
                "pending": True, 
                "redirect_url": final.get("redirectUrl"), # IMPORTANTE
                "status": final
            }

        except Exception as e:
            return {"success": False, "message": str(e)}
