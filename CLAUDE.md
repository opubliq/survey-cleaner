# CLAUDE.md

## ⚠️ IMPORTANT: Setup de l'environnement AVANT de commencer

**Tout code Python dans ce projet doit s'exécuter dans le virtual environment.**

### Setup initial (une seule fois)

```bash
./setup.sh
```

OU manuellement:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Activation (à chaque session)

```bash
source venv/bin/activate
```

Vérifier que le venv est actif:

```bash
which python  # Devrait pointer vers venv/bin/python
```

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

**IMPORTANT**: Toujours lire le plan détaillé dans `schemas/plan.md` avant de commencer tout travail sur le projet pour comprendre l'architecture complète du workflow n8n.

## Architecture n8n actuelle

### Workflow principal: survey-cleaner-mvp
- **Workflow ID**: EuQL3RwAz5ULPxjP 
- **Type**: Form Trigger (upload intégré n8n)
- **WebhookId**: 17f8e709-76d0-49c6-b4af-6d5f7a2201b8
- **Status**: Actif
- **Fonction**: Orchestrateur principal du nettoyage de sondages

### Workflow spécialisé: codebook-reader
- **Fonction**: Lecture et structuration des codebooks en JSON
- **Input**: Fichiers codebook (TXT, PDF, CSV, XLSX)
- **Output**: JSON structuré standardisé
- **Intégration**: Appelé par survey-cleaner-mvp

Pour gérer les workflows :
```bash
# Via MCP n8n
mcp__n8n-mcp__get_workflow --workflowId EuQL3RwAz5ULPxjP
mcp__n8n-mcp__update_workflow --workflowId EuQL3RwAz5ULPxjP
```

## Prérequis

- Python 3.9+
- R 4.0+
- API key Anthropic (Claude)

## Dépendances

Python (voir `requirements.txt`):
```
pandas>=2.3.2
numpy>=2.3.3
pyreadstat>=1.3.1
openpyxl>=3.1.5
fuzzywuzzy>=0.18.0
python-Levenshtein>=0.27.1
matplotlib>=3.10.6
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

1. Cloner le dépôt
```bash
git clone [URL] survey-cleaner
cd survey-cleaner
```

2. Setup automatique (recommandé)
```bash
./setup.sh
```

Ou installation manuelle:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Configurer l'API key Claude
```bash
echo "ANTHROPIC_API_KEY=your_key_here" > .env
```

4. Activer l'environnement pour chaque session
```bash
source venv/bin/activate
```

## Utilisation de l'agent survey-cleaner

### Commande rapide

Pour nettoyer un sondage automatiquement:
```
/clean-survey [nom_du_sondage]
```

OU utiliser la phrase naturelle:
```
utilise survey-cleaner-agent pour surveys/test
```

### Ce que l'agent fait automatiquement

Quand tu lances l'agent (via `/clean-survey` ou "utilise survey-cleaner-agent pour surveys/X"):

1. **Setup**: Vérifie l'environnement Python (venv)
2. **Discovery**: Trouve les fichiers dans `surveys/{nom}/raw/`
3. **Variables**: Liste toutes les variables du dataset
4. **Todo**: Crée `variables_todo.md` pour tracking
5. **Processing**: Pour CHAQUE variable:
   - Cherche dans le codebook (fuzzy matching)
   - Explore les données (frequencies, distributions)
   - Génère le code de nettoyage
   - Execute et valide
   - Ajoute au script `clean.py`
6. **Output**: Génère `clean.py`, `data_cleaned.csv`, `codebook.json`

### Structure des fichiers attendue

```
surveys/
  {nom_du_sondage}/
    raw/
      data.csv         # ou .sav, .xlsx
      codebook.md      # ou .txt (sera converti)
    metadata.json      # optionnel
    clean.py           # généré par l'agent
    variables_todo.md  # généré par l'agent
    processed/
      data_cleaned.csv # généré par l'agent
      codebook.json    # généré par l'agent
```

### Invocation programmatique

Si tu veux lancer l'agent depuis Claude (pas via commande slash):

```python
# Utilise Task tool avec:
subagent_type = "survey-cleaner-agent"
description = "Clean survey {nom}"
prompt = "Process survey in surveys/{nom}/ following your complete workflow. Report summary when done."
```

**IMPORTANT**: L'agent a toutes les instructions dans `.claude/agents/survey-cleaner-agent.md`. Pas besoin de répéter les instructions dans le prompt.

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
├── tests/            # Tests et scripts utilitaires
│   ├── test_codebook.txt  # Fichier de test codebook TXT
│   ├── test_codebook.csv  # Fichier de test codebook CSV
│   ├── test_survey.csv    # Fichier de test données
│   ├── start_mvp.sh       # Script de démarrage MVP
│   └── quick_test.sh      # Tests rapides
├── templates/        # Templates de prompts
│   ├── analysis.txt
│   └── cleaning.txt
├── utils/
│   ├── parsers.py    # Parsers CSV/SAV/PDF
│   └── validators.py # Validation des outputs
├── schemas/          # Schémas et documentation
│   ├── plan.md       # Plan détaillé du projet
│   └── n8n/          # Schémas des workflows n8n
│       ├── survey-cleaner-mvp.json  # Workflow principal
│       └── codebook-reader.json     # Workflow codebook reader
└── CLAUDE.md         # Instructions du projet
```

## Tests et développement

Tous les scripts de test et utilitaires sont dans le dossier `tests/`:
- `start_mvp.sh`: Script de vérification n8n et instructions d'utilisation
- `test_codebook.txt`: Fichier de test pour le codebook (format markdown)
- `test_survey.csv`: Fichier de test pour les données de sondage
- `quick_test.sh`: Tests rapides du workflow

## Utilisation

### Mode n8n form upload

1. Démarrer n8n : `npm run start` ou `docker-compose up`
2. Vérifier le setup : `./tests/start_mvp.sh`
3. Aller sur http://localhost:5678
4. Ouvrir le workflow `survey-cleaner-mvp`
5. Utiliser le form trigger intégré pour uploader:
   - **Codebook**: fichier TXT/PDF/CSV/XLSX (requis)
   - **Données**: fichier CSV/SAV/XLSX (optionnel)

### Workflow actuel

Le workflow traite actuellement les codebooks TXT en les convertissant en markdown.
Les autres formats (PDF, CSV, XLSX) ont des placeholders à implémenter.

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

- **MVP 1**: ✅ Form upload n8n + traitement codebook TXT
- **MVP 2**: Implémentation parseurs PDF, CSV, XLSX pour codebooks
- **MVP 3**: Traitement des données de sondage + génération script R  
- **MVP 4**: Intégration avec API Claude pour génération automatique

## Intégration avec le projet parent

Ce composant s'intègre dans le projet Opubliq comme outil d'alimentation pour le moteur de recherche de sondages.