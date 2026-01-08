# SheerID 验证配置文件 (Google One / Gemini)

# SheerID API 配置 - ESTE ID ES EL DE GOOGLE, NO LO CAMBIES
PROGRAM_ID = '67c8c14f5f17a83b745e3f82'
SHEERID_BASE_URL = 'https://services.sheerid.com'
MY_SHEERID_URL = 'https://my.sheerid.com'

# 文件大小限制
MAX_FILE_SIZE = 1 * 1024 * 1024  # 1MB

# USAMOS EL MISMO ID DE LA UNAM QUE YA FUNCIONÓ
UNAM_ID = 415489

SCHOOLS = {
    str(UNAM_ID): {
        'id': UNAM_ID,
        'idExtended': str(UNAM_ID),
        'name': 'Universidad Nacional Autónoma De México (UNAM)',
        'city': 'Coyoacán',
        'state': 'CDMX',
        'country': 'MX',
        'type': 'UNIVERSITY',
        'domain': 'UNAM.MX',
        'latitude': 19.332,
        'longitude': -99.186
    }
}

# Default
DEFAULT_SCHOOL_ID = str(UNAM_ID)
