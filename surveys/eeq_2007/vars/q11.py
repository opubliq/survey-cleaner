import numpy as np

CODEBOOK_VARIABLES = {}

# q11 variable definition as per context provided for validation
CODEBOOK_VARIABLES['q11'] = {
    "question": "Rôle de l'économie comme enjeu électoral",
    "type": "likert",
    "values": {
        "1": "très important",
        "2": "assez important",
        "3": "peu important",
        "4": "pas du tout important"
    },
    "missing_codes": [8, 9]
}