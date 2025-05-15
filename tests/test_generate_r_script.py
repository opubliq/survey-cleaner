import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.llm_interface import generate_r_script

prompt = """
Génère un script R pour nettoyer un sondage.
Le script doit :
1. Charger un fichier CSV
2. Nettoyer les noms de colonnes
3. Recoder les valeurs manquantes comme NA
4. Exporter au format .rds
"""

script = generate_r_script(prompt)
print(script)
