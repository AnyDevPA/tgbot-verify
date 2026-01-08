# SheerID 验证配置文件

# SheerID API 配置
PROGRAM_ID = '695f63e8f44326081137a4e8'
SHEERID_BASE_URL = 'https://services.sheerid.com'
MY_SHEERID_URL = 'https://my.sheerid.com'

# 文件大小限制
MAX_FILE_SIZE = 1 * 1024 * 1024  # 1MB

# ID REAL QUE ENCONTRASTE EN LA CAPTURA
UNAM_ID = 415489  # <--- ESTE ES EL BUENO

SCHOOLS = {
    str(UNAM_ID): {
        'id': UNAM_ID,
        'idExtended': str(UNAM_ID),
        # El nombre exacto que sale en tu captura
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

# Configurar este ID como el default
DEFAULT_SCHOOL_ID = str(UNAM_ID)
