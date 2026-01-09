import random

class NameGenerator:
    """Generador de Nombres Reales para USA (Optimizado para Texas)"""
    
    # Lista de nombres comunes (Censo USA + Latinos comunes en TX)
    FIRST_NAMES = [
        'James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda',
        'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica',
        'Thomas', 'Sarah', 'Charles', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa',
        'Matthew', 'Betty', 'Anthony', 'Margaret', 'Mark', 'Sandra', 'Donald', 'Ashley',
        'Steven', 'Kimberly', 'Paul', 'Emily', 'Andrew', 'Donna', 'Joshua', 'Michelle',
        'Kenneth', 'Dorothy', 'Kevin', 'Carol', 'Brian', 'Amanda', 'George', 'Melissa',
        'Edward', 'Deborah', 'Ronald', 'Stephanie', 'Timothy', 'Rebecca', 'Jason', 'Sharon',
        'Jeffrey', 'Laura', 'Ryan', 'Cynthia', 'Jacob', 'Kathleen', 'Gary', 'Amy',
        'Nicholas', 'Shirley', 'Eric', 'Angela', 'Jonathan', 'Helen', 'Stephen', 'Anna',
        'Larry', 'Brenda', 'Justin', 'Pamela', 'Scott', 'Nicole', 'Brandon', 'Emma',
        # Nombres latinos comunes en Texas
        'Jose', 'Maria', 'Juan', 'Ana', 'Luis', 'Sofia', 'Carlos', 'Isabella', 'Jesus', 'Camila'
    ]
    
    LAST_NAMES = [
        'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
        'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas',
        'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson', 'White',
        'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker', 'Young',
        'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores',
        'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell',
        'Carter', 'Roberts', 'Gomez', 'Phillips', 'Evans', 'Turner', 'Diaz', 'Parker',
        'Cruz', 'Edwards', 'Collins', 'Reyes', 'Stewart', 'Morris', 'Morales', 'Murphy',
        'Cook', 'Rogers', 'Gutierrez', 'Ortiz', 'Morgan', 'Cooper', 'Peterson', 'Bailey',
        'Reed', 'Kelly', 'Howard', 'Ramos', 'Kim', 'Cox', 'Ward', 'Richardson'
    ]
    
    @classmethod
    def generate(cls):
        """Genera un nombre completo realista"""
        first = random.choice(cls.FIRST_NAMES)
        last = random.choice(cls.LAST_NAMES)
        
        return {
            'first_name': first,
            'last_name': last,
            'full_name': f"{first} {last}"
        }

def generate_email():
    """
    Genera un email personal genérico (Gmail/Outlook)
    Nota: El verificador principal usará el email escolar (@austinisd.org)
    """
    name = NameGenerator.generate()
    first = name['first_name'].lower()
    last = name['last_name'].lower()
    num = random.randint(100, 9999)
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
    return f"{first}.{last}{num}@{random.choice(domains)}"

def generate_birth_date():
    """
    Genera fecha de nacimiento para un MAESTRO (Edad 28 - 55 años aprox)
    Rango: 1970 - 1995
    """
    year = random.randint(1970, 1995)
    month = str(random.randint(1, 12)).zfill(2)
    day = str(random.randint(1, 28)).zfill(2)
    return f"{year}-{month}-{day}"
