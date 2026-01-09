# military/config.py

# ID del Programa (OJO: Tienes que buscar el ID de "ChatGPT Military" en tu navegador con F12)
# Si no lo tienes, este es uno común de OpenAI Military, pero VERIFÍCALO:
PROGRAM_ID = '6465476a6937517937397063' 
SHEERID_BASE_URL = 'https://services.sheerid.com'

# Ramas Militares (Copiadas tal cual del README)
MILITARY_BRANCHES = [
    {"id": 4070, "name": "Army", "type": "MILITARY"},
    {"id": 4073, "name": "Air Force", "type": "MILITARY"},
    {"id": 4072, "name": "Navy", "type": "MILITARY"},
    {"id": 4071, "name": "Marine Corps", "type": "MILITARY"},
    {"id": 4074, "name": "Coast Guard", "type": "MILITARY"},
    {"id": 4544268, "name": "Space Force", "type": "MILITARY"}
]

# Metadata obligatoria (Texto legal)
METADATA_FLAGS = '{"doc-upload-considerations":"default","doc-upload-may24":"default","doc-upload-redesign-use-legacy-message-keys":false,"docUpload-assertion-checklist":"default","include-cvec-field-france-student":"not-labeled-optional","org-search-overlay":"default","org-selected-display":"default"}'

SUBMISSION_OPT_IN = 'By submitting the personal information above, I acknowledge that my personal information is being collected under the <a target="_blank" rel="noopener noreferrer" class="sid-privacy-policy sid-link" href="https://openai.com/policies/privacy-policy/">privacy policy</a> of the business from which I am seeking a discount.'
