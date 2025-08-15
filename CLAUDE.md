# CLAUDE.md

## Objectif

Permettre l'importation rapide et standardisée de fichiers de sondages (CSV/SAV) dans notre moteur de recherche en automatisant:
- L'analyse de structure
- Le nettoyage des données
- La standardisation des variables
- La détection d'erreurs

## Rôle dans le projet

Claude servira de moteur d'intelligence pour notre bot de nettoyage de sondages, avec les fonctions principales:

- Analyser la structure des fichiers de sondage (CSV/SAV)
- Générer des scripts R de nettoyage adaptés
- Détecter et corriger les problèmes courants
- Standardiser les variables selon notre schéma

## Prérequis

- Python 3.9+
- R 4.0+
- API key Anthropic (Claude)

## Dépendances

Python:
```
streamlit
flask
anthropic
pandas
pyreadstat
```

R:
```
tidyverse
haven
lubridate
httr
jsonlite
```

## Configuration API

### Python
```python
from anthropic import Anthropic

# Configuration
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
anthropic = Anthropic(api_key=api_key)
```

### R
```r
# Installation
install.packages("httr")
install.packages("jsonlite")

# Configuration
api_key <- Sys.getenv("ANTHROPIC_API_KEY")
model <- "claude-3-opus-20240229" # Ou autre version appropriée
```

## Installation

1. Cloner le dépôt dans l'arborescence existante
```bash
git clone [URL] bot_nettoyage
```

2. Installer les dépendances
```bash
pip install -r bot_nettoyage/requirements.txt
```

3. Configurer l'API key Claude
```bash
echo "ANTHROPIC_API_KEY=your_key_here" > .env
```

## Exemples de prompts

### Analyse de structure

```
Analyse ce fichier de sondage. Identifie:
1. Variables démographiques
2. Variables d'opinion
3. Variables techniques/métadonnées
4. Problèmes potentiels (valeurs manquantes, encodage)

Format des données:
{données_exemple}

Format du codebook (si disponible):
{codebook_exemple}
```

### Génération de script R

```
Génère un script R pour nettoyer ce sondage selon notre format standard.
Le script doit:
1. Importer les données correctement
2. Renommer les variables selon notre convention
3. Recoder les valeurs manquantes
4. Harmoniser les échelles des variables d'opinion
5. Exporter en format .rds

Voici nos conventions:
- Préfixe démographique: demo_
- Préfixe opinion: op_
- Encodage NA: NA pour toutes les valeurs manquantes
- Échelles standardisées: 0-1 pour toutes les variables d'opinion

Données originales:
{données_exemple}
```

## Pipeline de traitement

1. Envoi du fichier → Claude analyse
2. Claude génère script R initial
3. Exécution test du script → feedback erreurs
4. Claude corrige et optimise
5. Validation utilisateur → finalisation

## Structure du projet

```
survey-cleaner/
├── web/              # Interface web d'upload
│   └── index.html    # Page de upload MVP
├── tests/            # Tests et scripts utilitaires
│   ├── test_webhook.sh    # Test du webhook n8n
│   └── start_mvp.sh       # Script de démarrage MVP
├── templates/        # Templates de prompts
│   ├── analysis.txt
│   └── cleaning.txt
├── utils/
│   ├── parsers.py    # Parsers CSV/SAV/PDF
│   └── validators.py # Validation des outputs
├── schema.json       # Configuration du workflow n8n
└── CLAUDE.md         # Instructions du projet
```

## Tests et développement

Tous les scripts de test et utilitaires sont dans le dossier `tests/`:
- `test_webhook.sh`: Test du webhook n8n avec fichier CSV d'exemple
- `start_mvp.sh`: Script de démarrage complet (active webhook + lance serveur web + ouvre navigateur)

## Utilisation

### Mode local

```bash
cd bot_nettoyage
streamlit run app.py
```

### Intégration avec pipeline actuel

```bash
python bot_nettoyage/process.py --input data.csv --codebook codebook.pdf --output create_survey_bd/new_survey/
```

## Limitations

- Sensible à la qualité du prompt
- Peut nécessiter plusieurs itérations pour les datasets complexes
- Connaissance limitée aux formats courants (CSV, SAV, mais pas SPSS avancé)
- Prévoir validation humaine des transformations

## Performance monitoring

Mesurer et stocker:
- Taux de réussite du premier script généré
- Points d'échec communs
- Temps de traitement
- Feedback utilisateur

Utiliser ces métriques pour améliorer les prompts.

## Tips pour développement

- Les prompts de Claude sont dans `/templates/`
- Logs d'exécution dans `/logs/`
- Pour débugger, activer le mode verbose: `python process.py --verbose`
- Structure du pipeline existant dans `create_survey_bd`

## Roadmap

- **MVP 1**: Upload CSV + génération script simple
- **MVP 2**: Exécution et debug automatique
- **MVP 3**: Support complet formats + optimisation

## Intégration avec le projet parent

Ce composant s'intègre dans le projet Opubliq comme outil d'alimentation pour le moteur de recherche de sondages.