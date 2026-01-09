# Configuración K-12 (Maestros)

# ID del Programa (Sacado de tu captura de pantalla)
PROGRAM_ID = '68d47554aa292d20b9bec8f7'
SHEERID_BASE_URL = 'https://services.sheerid.com'

# Configuración de Escuela (Usaremos una High School de Texas real)
# ID obtenido de la base de datos de SheerID
SCHOOLS = {
    '152865': {
        'id': 152865,
        'name': 'Austin High School',
        'city': 'Austin',
        'state': 'TX',
        'country': 'US',
        'type': 'K12_SCHOOL'
    }
}

DEFAULT_SCHOOL_ID = '152865'

# Metadata estándar
METADATA = {
    "marketConsentValue": False,
    "submissionOptIn": "By submitting the personal information above, I acknowledge that my personal information is being collected under the privacy policy."
}
