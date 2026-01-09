# one/config.py - MODO ASU (Arizona State)

# ID del Programa Google One
PROGRAM_ID = '67c8c14f5f17a83b745e3f82'
SHEERID_BASE_URL = 'https://services.sheerid.com'

# Arizona State University (ASU)
# ID común en SheerID: 1496
SCHOOLS = {
    '1496': {
        'id': 1496,
        'name': 'Arizona State University',
        'city': 'Tempe',
        'state': 'AZ',
        'country': 'US',
        'type': 'UNIVERSITY'
    }
}

DEFAULT_SCHOOL_ID = '1496'

METADATA = {
    "marketConsentValue": False,
    "submissionOptIn": "By submitting the personal information above, I acknowledge that my personal information is being collected under the privacy policy."
}
