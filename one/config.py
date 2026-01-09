# one/config.py - MODO SNHU (Online Friendly)

PROGRAM_ID = '67c8c14f5f17a83b745e3f82'
SHEERID_BASE_URL = 'https://services.sheerid.com'

# Southern New Hampshire University (SNHU)
# ID: 3578 (Suele funcionar bien para online)
SCHOOLS = {
    '3578': {
        'id': 3578,
        'name': 'Southern New Hampshire University',
        'city': 'Manchester',
        'state': 'NH',
        'country': 'US',
        'type': 'UNIVERSITY'
    }
}

DEFAULT_SCHOOL_ID = '3578'

METADATA = {
    "marketConsentValue": False,
    "submissionOptIn": "By submitting the personal information above, I acknowledge that my personal information is being collected under the privacy policy."
}
