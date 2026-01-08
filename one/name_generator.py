"""Generador de Nombres Latinos para Bypass"""
import random

class NameGenerator:
    """Generador de nombres comunes en México/Latam"""
    
    # Listas de nombres reales y comunes
    FIRST_NAMES = [
        'Juan', 'José', 'Luis', 'Carlos', 'Francisco', 'Pedro', 'Jesús', 'Manuel', 'Miguel', 'Antonio',
        'Alejandro', 'David', 'Daniel', 'Jorge', 'Ricardo', 'Eduardo', 'Roberto', 'Gabriel', 'Fernando',
        'María', 'Ana', 'Sofía', 'Fernanda', 'Valeria', 'Daniela', 'Guadalupe', 'Andrea', 'Juana',
        'Gabriela', 'Patricia', 'Adriana', 'Verónica', 'Alejandra', 'Elizabeth', 'Mariana', 'Ximena'
    ]
    
    LAST_NAMES = [
        'Hernández', 'García', 'Martínez', 'López', 'González', 'Pérez', 'Rodríguez', 'Sánchez',
        'Ramírez', 'Cruz', 'Flores', 'Gómez', 'Morales', 'Vázquez', 'Jiménez', 'Reyes', 'Díaz',
        'Torres', 'Gutiérrez', 'Ruiz', 'Mendoza', 'Aguilar', 'Ortiz', 'Castillo', 'Moreno',
        'Romero', 'Álvarez', 'Rivera', 'Chávez', 'Ramos', 'De la Cruz', 'Domínguez', 'Vargas'
    ]
    
    @classmethod
    def generate(cls):
        """
        Genera un nombre latino aleatorio
        """
        first = random.choice(cls.FIRST_NAMES)
        last = random.choice(cls.LAST_NAMES)
        
        # A veces agregamos un segundo apellido para más realismo (50% de probabilidad)
        if random.random() > 0.5:
            last2 = random.choice(cls.LAST_NAMES)
            # Evitamos apellidos repetidos (ej. Lopez Lopez)
            while last2 == last:
                last2 = random.choice(cls.LAST_NAMES)
            full_last = f"{last} {last2}"
        else:
            full_last = last

        return {
            'first_name': first,
            'last_name': full_last,
            'full_name': f"{first} {full_last}"
        }

def generate_email(school_domain='comunidad.unam.mx'):
    """
    Genera un correo con formato de alumno real
    """
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    username = ''.join(random.choice(chars) for _ in range(random.randint(6, 10)))
    return f"{username}@{school_domain}"

def generate_birth_date():
    """
    Genera cumpleaños para alguien de 18-24 años
    """
    year = random.randint(2001, 2006)
    month = str(random.randint(1, 12)).zfill(2)
    day = str(random.randint(1, 28)).zfill(2)
    return f"{year}-{month}-{day}"
