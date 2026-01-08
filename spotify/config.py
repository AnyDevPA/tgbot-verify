# SheerID 验证配置文件

# SheerID API 配置
PROGRAM_ID = '695f63e8f44326081137a4e8' 
SHEERID_BASE_URL = 'https://services.sheerid.com'
MY_SHEERID_URL = 'https://my.sheerid.com'

# 文件大小限制
MAX_FILE_SIZE = 1 * 1024 * 1024  # 1MB

# 学校配置
SCHOOLS = {
    # --- AGREGADO: UNAM (MEXICO) ---
    '5032': {  # <--- ESTE ES EL ID, CONFIRMA SI ES 5032 EN TU NAVEGADOR
        'id': 5032,
        'idExtended': '5032',
        'name': 'Universidad Nacional Autónoma De México (UNAM)',
        'city': 'Coyoacán',
        'state': 'CDMX',
        'country': 'MX',
        'type': 'UNIVERSITY',
        'domain': 'UNAM.MX',
        'latitude': 19.332,
        'longitude': -99.186
    },
    # -------------------------------
    '2565': {
        'id': 2565,
        'idExtended': '2565',
        'name': 'Pennsylvania State University-Main Campus',
        'city': 'University Park',
        'state': 'PA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'PSU.EDU',
        'latitude': 40.798214,
        'longitude': -77.85991
    }
}

# 默认学校 (CAMBIADO A UNAM)
DEFAULT_SCHOOL_ID = '5032'
