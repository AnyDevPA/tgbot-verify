# military/utils.py
import random
from datetime import datetime, timedelta

def get_military_dates():
    """
    Genera fecha de nacimiento (birthDate) y fecha de retiro (dischargeDate)
    Formato: YYYY-MM-DD
    Lógica: Entró a los 18-20 años, sirvió 4 años, se retiró.
    """
    # Edad actual simulada: 28 a 45 años
    age = random.randint(28, 45)
    current_year = datetime.now().year
    birth_year = current_year - age
    
    # Generar cumpleaños
    birth_date = f"{birth_year}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
    
    # Calculamos retiro: (Año nacimiento + 18 años para enlistarse + 4 de servicio)
    discharge_year = birth_year + 18 + 4 + random.randint(0, 5) # +0 a 5 años extra
    
    # Fecha de retiro (dischargeDate)
    discharge_date = f"{discharge_year}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
    
    return birth_date, discharge_date
