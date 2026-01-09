import logging
import httpx
import random
import unicodedata
import re
import json
import asyncio
from . import config
from .img_generator import generate_image
from .name_generator import NameGenerator 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SheerIDVerifier:
    def __init__(self, verification_id):
        self.verification_id = verification_id
        # Headers Chrome Windows
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Referer": f"https://services.sheerid.com/verify/{config.PROGRAM_ID}/",
            "Origin": "https://services.sheerid.com"
        }
        self.client = httpx.Client(headers=self.headers, timeout=30.0)
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
            
            # --- CAMBIO IMPORTANTE: USAR EMAIL INSTITUCIONAL FALSO ---
            # Esto evita el bloqueo inmediato de "fraudRulesReject".
            school = config.SCHOOLS[config.DEFAULT_SCHOOL_ID]
            domain = school.get('domain', 'westerntech.edu')
            
            # Generamos algo como: juan.perez22@westerntech.edu
            email = self.sanitize_email(f"{first}.{last}{random.randint(10,99)}@{domain}").lower()
            
            dob = f"200{random.randint(0,5)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"

            logger.info(f"🔧 TECH STUDENT: {first} {last} | {email}")

            payload = {
                "firstName": first,
                "lastName": last,
                "birthDate": dob,
                "email": email,
                "organization": {"id": school['id'], "name": school['name']},
                "deviceFingerprintHash": self.device_fingerprint,
                "metadata": {**config.METADATA, "verificationId": self.verification_id, "refererUrl": f"{config.SHEERID_BASE_URL}/verify/{config.PROGRAM_ID}/"}
            }
            
            # PASO 1: ENVIAR DATOS
            url_step1 = f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/collectStudentPersonalInfo"
            resp1 = self.client.post(url_step1, json=payload)
            data1 = resp1.json()
            current_step = data1.get("currentStep")

            # --- HACK PARA ROMPER EL LOOP ---
            if current_step == "emailLoop":
                logger.info("⚠️ Entramos al Loop (Código enviado). Intentando saltar a Documentos...")
                
                # Intentamos dos métodos para romper el loop:
                
                # Método A: DELETE al endpoint del loop (Simula clic en "Verificar de otra forma")
                del_resp = self.client.delete(f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/emailLoop")
                
                # Actualizamos estado
                status = self.client.get(f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}").json()
                current_step = status.get("currentStep")
                logger.info(f"Estado post-salto: {current_step}")

            # Si nos manda a error, es que nos detectaron
            if current_step == "error":
                return {"success": False, "message": f"❌ Error: {data1.get('errorIds')}"}

            if current_step == "success":
                 return {"success": True, "pending": False, "redirect_url": data1.get("redirectUrl"), "status": data1}

            # PASO 2: SUBIR DOCUMENTO
            # Si logramos romper el loop, deberíamos estar aquí
            if current_step == "docUpload":
                logger.info(">> Subiendo Credencial WTC...")
                img_bytes = generate_image(first, last)
                
                url_upload = f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/docUpload"
                resp2 = self.client.post(url_upload, json={"files": [{"fileName": "student_id.jpg", "mimeType": "image/jpeg", "fileSize": len(img_bytes)}]})
                
                if "documents" in resp2.json():
                    upload_link = resp2.json()["documents"][0]["uploadUrl"]
                    self.client.put(upload_link, content=img_bytes, headers={"Content-Type": "image/jpeg"})
                    final = self.client.post(f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/completeDocUpload").json()
                    return {"success": True, "pending": True, "redirect_url": final.get("redirectUrl"), "status": final}
            
            # Si seguimos en emailLoop después de intentar borrarlo, estamos jodidos
            if current_step == "emailLoop":
                 return {"success": False, "message": "❌ No se pudo salir del Email Loop. Google exige el código."}

            return {"success": False, "message": f"Estado desconocido: {current_step}"}

        except Exception as e:
            return {"success": False, "message": str(e)}
