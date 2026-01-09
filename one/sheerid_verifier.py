import logging
import httpx
import random
import unicodedata
import re
import json
from . import config
from .img_generator import generate_image
from .name_generator import NameGenerator 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SheerIDVerifier:
    def __init__(self, verification_id):
        self.verification_id = verification_id
        # Headers de Chrome REAL
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Referer": f"https://services.sheerid.com/verify/{config.PROGRAM_ID}/",
            "Origin": "https://services.sheerid.com",
            "Sec-Ch-Ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty"
        }
        
        # SI TIENES UN PROXY, PONLO AQUÍ:
        # proxies = "http://user:pass@ip:port"
        # self.client = httpx.Client(headers=self.headers, proxies=proxies, timeout=30.0)
        
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
            
            # Edad joven para escuela técnica (18-24)
            dob = f"200{random.randint(0,5)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
            school = config.SCHOOLS[config.DEFAULT_SCHOOL_ID]
            
            # Email ULTRA NORMAL (Nada de palabras raras)
            # Solo nombre.apellido + numeros random @ gmail/yahoo
            domains = ["gmail.com", "yahoo.com", "outlook.com"]
            email = self.sanitize_email(f"{first}.{last}{random.randint(10,9999)}@{random.choice(domains)}").lower()

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
            
            url_step1 = f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/collectStudentPersonalInfo"
            resp1 = self.client.post(url_step1, json=payload)
            data1 = resp1.json()
            current_step = data1.get("currentStep")

            # REINTENTO INTELIGENTE
            if current_step == "collectStudentPersonalInfo":
                logger.info("⚠️ Reintentando con otro email...")
                payload["email"] = self.sanitize_email(f"{last}{first}{random.randint(1,99)}@gmail.com").lower()
                resp1 = self.client.post(url_step1, json=payload)
                data1 = resp1.json()
                current_step = data1.get("currentStep")

            if current_step == "emailLoop":
                self.client.delete(f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/emailLoop")
                status = self.client.get(f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}").json()
                current_step = status.get("currentStep")

            if current_step == "error":
                return {"success": False, "message": f"❌ BLOQUEADO: {data1.get('errorIds')}"}

            if current_step == "success":
                 return {"success": True, "pending": False, "redirect_url": data1.get("redirectUrl"), "status": data1}

            # PASO 2: Doc Upload
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
            
            return {"success": False, "message": f"Estado desconocido: {current_step}"}

        except Exception as e:
            return {"success": False, "message": str(e)}
