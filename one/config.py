# one/config.py - MODO WESTERN TECH (Fake Edu Email)

PROGRAM_ID = '67c8c14f5f17a83b745e3f82'
SHEERID_BASE_URL = 'https://services.sheerid.com'

# Western Technical College (El Paso, TX)
# ID: 4078874
SCHOOLS = {
    '4078874': {
        'id': 4078874,
        'name': 'Western Technical College (El Paso, TX)',
        'city': 'El Paso',
        'state': 'TX',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'westerntech.edu' # <--- DOMINIO CLAVE
    }
}

DEFAULT_SCHOOL_ID = '4078874'

METADATA = {
    "marketConsentValue": False,
    "submissionOptIn": "By submitting the personal information above, I acknowledge that my personal information is being collected under the privacy policy."
}
