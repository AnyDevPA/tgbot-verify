# one/config.py - MODO PRO (School Email)

PROGRAM_ID = '67c8c14f5f17a83b745e3f82'
SHEERID_BASE_URL = 'https://services.sheerid.com'

# Western Governors University (Salt Lake City, UT)
# ID: 3919 (Confirmado)
SCHOOLS = {
    '3919': {
        'id': 3919,
        'name': 'Western Governors University (Salt Lake City, UT)',
        'city': 'Salt Lake City',
        'state': 'UT',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'wgu.edu'  # <--- EL DOMINIO MÁGICO
    }
}

DEFAULT_SCHOOL_ID = '3919'

METADATA = {
    "marketConsentValue": False,
    "submissionOptIn": "By submitting the personal information above, I acknowledge that my personal information is being collected under the privacy policy."
}
