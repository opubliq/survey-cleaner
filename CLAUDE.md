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

## Installation et Quick Start

### Setup (une fois)

```bash
# 1. Setup automatique
./setup.sh

# 2. Configurer API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# 3. Tester
./surveys/run_cleaner.sh test --limit 3
```

### Utilisation quotidienne

```bash
# Nettoyer un sondage complet
./surveys/run_cleaner.sh mon_sondage

# Limiter à N variables pour tests
./surveys/run_cleaner.sh mon_sondage --limit 10
```

**Structure minimale requise:**
```
surveys/mon_sondage/
  raw/
    data.csv        # ou .sav, .xlsx
    codebook.md     # ou .txt
```

Le système génère automatiquement tout le reste.

## Architecture du système de nettoyage

### Système agentic via API Anthropic (mode principal)

Le système utilise des **appels API directs** à Claude avec tool use pour automatiser le nettoyage de sondages. Contrairement aux commandes slash interactives, ce mode permet l'exécution en batch, background, et dans des pipelines CI/CD.

**Composants:**
1. **`surveys/run_cleaner.sh`** - Wrapper qui active venv et lance l'orchestrateur
2. **`surveys/process_survey.py`** - Orchestrateur Python principal
3. **`surveys/agent_tools.py`** - Définitions et exécutions des tools
4. **`.claude/agents/*.md`** - Instructions pour chaque agent spécialisé

**Agents spécialisés:**
- **`survey-init-agent`**: Initialise structure et crée `variables_todo.md`
- **`survey-variable-cleaner-agent`**: Nettoie UNE variable à la fois

**Flow agentic:**
```
User lance run_cleaner.sh
  ↓
process_survey.py charge instructions agent depuis .md
  ↓
Appelle API Anthropic avec tools (bash, read_file, write_file, edit_file)
  ↓
LOOP jusqu'à end_turn:
  - Agent demande tools (stop_reason=tool_use)
  - Exécution locale des tools
  - Résultats renvoyés à l'agent
  ↓
Agent termine (stop_reason=end_turn)
```

### Utilisation (mode API - recommandé)

**Commande simple:**
```bash
./surveys/run_cleaner.sh test              # Nettoie tout le sondage
./surveys/run_cleaner.sh ces19 --limit 10  # Limite à 10 variables
```

**Ce que le script fait automatiquement:**

1. **Initialisation** (via `survey-init-agent`):
   - Crée `raw/` et `processed/`
   - Liste toutes les variables du dataset
   - Crée `variables_todo.md` (tracking)
   - Crée `pending_vars.txt` (liste pour loop)
   - Copie template `clean.py`

2. **Processing variable par variable** (via `survey-variable-cleaner-agent`):
   - Explore la variable (frequencies, distributions)
   - Fuzzy matching dans codebook
   - Génère code de nettoyage sécurisé
   - Valide transformation
   - Ajoute au `clean.py`
   - Met à jour `codebook.json`
   - Commit git
   - Marque comme complété dans `variables_todo.md`

3. **Finalisation**:
   - Exécute `clean.py`
   - Génère `data_cleaned.csv` et `codebook.json`
   - Rapport final

**Logs:**
- Console: progression en temps réel
- `surveys/{nom}/process.log`: log détaillé

### Commandes slash (mode interactif)

Pour usage interactif depuis Claude Code (moins courant):
```bash
/init-survey [nom]       # Initialise structure
/clean-var [nom] [var]   # Nettoie 1 variable
/finalize-survey [nom]   # Validation finale
```

Ces commandes utilisent le même système agentic mais via Task tool de Claude Code.

### Structure des fichiers

```
surveys/
  {nom_du_sondage}/
    raw/
      data.csv           # ou .sav, .xlsx
      codebook.md        # ou .txt
    clean.py             # Script dual-mode (AWS + local)
    variables_todo.md    # Tracking: [x] done, [~] in progress, [ ] pending
    pending_vars.txt     # Liste pour loop shell
    process.log          # Log du processing
    processed/
      data_cleaned.csv   # Output nettoyé
      codebook.json      # Codebook standardisé
```

## Script clean.py (dual-mode)

Chaque sondage génère un script `clean.py` qui fonctionne en deux modes:

**Mode AWS (fonction exportée):**
```python
from surveys.test.clean import clean_data

df_clean = clean_data(df_raw)  # Appelé par lambda_raffineur_nettoyage
```

**Mode local (exécution standalone):**
```bash
python surveys/test/clean.py  # Génère processed/data_cleaned.csv
```

Le script s'enrichit variable par variable pendant le processing. Chaque bloc suit un pattern sécurisé validé par l'agent.

## Documentation des labels de questions et choix de réponse

**IMPORTANT**: Les labels de questions et choix de réponse sont essentiels pour l'interprétation sémantique des données par les LLMs dans les marts downstream (pipeline_sondages → OpenSearch).

### Pourquoi documenter les labels?

Sans labels, le `codebook.json` contient seulement:
```json
"op_satisfaction_gov": {
  "values": {
    "0.0": {"count": 2, "percent": 10.0}  // ❌ Pas de label - LLM ne sait pas ce que 0.0 signifie
  }
}
```

Avec labels:
```json
"op_satisfaction_gov": {
  "question_label": "Dans quelle mesure êtes-vous satisfait du gouvernement actuel?",
  "values": {
    "0.0": {"count": 2, "percent": 10.0, "label": "Très insatisfait"}  // ✅ LLM comprend
  }
}
```

### Workflow manuel en 2 étapes

#### Étape 1: Standardisation du codebook source (une fois par sondage)

Convertir le codebook original (PPTX, PDF, TXT) en format Markdown standardisé:

```
raw/codebook.pptx (source hétérogène)
    ↓
[Lecture humaine + copier-coller]
    ↓
raw/codebook.md (format standardisé)
```

**Template disponible**: `surveys/_template/codebook.md`

**Format recommandé pour chaque variable**:
```markdown
### op_satisfaction_gov

**Question**: Dans quelle mesure êtes-vous satisfait du gouvernement actuel?

**Type**: Échelle Likert (5 points)

**Variable brute**: `satisfaction_gouv` ou `Q10_satisfaction`

**Choix de réponse**:
- 1 = Très insatisfait
- 2 = Plutôt insatisfait
- 3 = Neutre
- 4 = Plutôt satisfait
- 5 = Très satisfait
- 99 = Ne sait pas / Refuse

**Mapping recommandé**:
```python
1.0: 0.0,    # Très insatisfait
2.0: 0.25,   # Plutôt insatisfait
3.0: 0.5,    # Neutre
4.0: 0.75,   # Plutôt satisfait
5.0: 1.0,    # Très satisfait
99.0: np.nan
```

**Entrée VARIABLE_METADATA**:
```python
'op_satisfaction_gov': {
    'question_label': "Dans quelle mesure êtes-vous satisfait du gouvernement actuel?",
    'value_labels': {
        0.0: "Très insatisfait",
        0.25: "Plutôt insatisfait",
        0.5: "Neutre",
        0.75: "Plutôt satisfait",
        1.0: "Très satisfait"
    }
}
```

#### Étape 2: Transcription pendant le cleaning (variable par variable)

Pendant que vous nettoyez chaque variable dans `clean.py`:

**1. Ajoutez le code de transformation dans `clean_data()`**:
```python
def clean_data(df):
    df_clean = pd.DataFrame(index=df.index)

    # Nettoyage de la variable
    df_clean['op_satisfaction_gov'] = df['satisfaction_gouv'].map({
        1.0: 0.0,
        2.0: 0.25,
        3.0: 0.5,
        4.0: 0.75,
        5.0: 1.0,
        99.0: np.nan
    })

    return df_clean
```

**2. Ajoutez l'entrée correspondante dans `VARIABLE_METADATA`** (en haut du fichier):
```python
VARIABLE_METADATA = {
    'op_satisfaction_gov': {
        'question_label': "Dans quelle mesure êtes-vous satisfait du gouvernement actuel?",
        'value_labels': {
            0.0: "Très insatisfait",
            0.25: "Plutôt insatisfait",
            0.5: "Neutre",
            0.75: "Plutôt satisfait",
            1.0: "Très satisfait"
        }
    },
    # Ajoutez d'autres variables au fur et à mesure...
}
```

**3. Exécutez `python clean.py`**:
- Génère automatiquement `processed/codebook.json` enrichi avec les labels
- Les labels seront utilisés par pipeline_sondages pour l'indexation sémantique

### Notes importantes

- **Optionnel mais recommandé**: Si vous n'ajoutez pas les labels, le `codebook.json` sera quand même généré avec les stats de base
- **Progressif**: Enrichissez au fur et à mesure, pas besoin de tout faire d'un coup
- **Un seul endroit**: Tout dans `clean.py`, pas de fichier séparé à maintenir
- **Format final**: Le `codebook.json` enrichi est le format utilisé par les marts et les LLMs downstream

## Structure du projet

```
survey-cleaner/
├── .claude/
│   ├── agents/                        # Instructions agents agentic
│   │   ├── survey-init-agent.md       # Agent d'initialisation
│   │   └── survey-variable-cleaner-agent.md  # Agent de nettoyage variable
│   └── commands/                      # Commandes slash (mode interactif)
│       ├── init-survey.md
│       ├── clean-var.md
│       └── finalize-survey.md
├── surveys/
│   ├── run_cleaner.sh                 # ⭐ Script principal (wrapper)
│   ├── process_survey.py              # ⭐ Orchestrateur agentic API
│   ├── agent_tools.py                 # ⭐ Tools pour agents (bash, read, write, edit)
│   ├── cleaning_rules.json            # Règles de nettoyage
│   ├── _template/                     # Template pour nouveaux sondages
│   │   ├── clean.py                   # Template script dual-mode
│   │   └── codebook.md                # Template codebook standardisé
│   ├── test/                          # Sondage de test
│   │   ├── raw/
│   │   ├── clean.py
│   │   ├── variables_todo.md
│   │   └── process.log
│   └── ces19/                         # Canadian Election Study 2019
│       └── ...
├── tests/                             # Tests et scripts utilitaires
│   ├── test_codebook.txt
│   ├── test_survey.csv
│   └── start_mvp.sh
├── schemas/                           # Schémas et documentation
│   ├── plan.md                        # Plan détaillé du projet
│   └── n8n/                           # Workflows n8n (legacy/complémentaire)
│       ├── survey-cleaner-mvp.json
│       └── codebook-reader.json
├── setup.sh                           # Setup venv et dépendances
├── requirements.txt                   # Dépendances Python
└── CLAUDE.md                          # ⭐ Instructions du projet
```

## Tests et développement

**Tester le système rapidement:**
```bash
./surveys/run_cleaner.sh test --limit 3  # Nettoie 3 variables du sondage test
```

**Fichiers de test:**
- `surveys/test/`: Sondage minimal pour tests
- `tests/test_codebook.txt`: Codebook de test
- `tests/test_survey.csv`: Données de test

**Modes d'intégration:**

1. **Mode standalone** (actuel): `./surveys/run_cleaner.sh {nom}`
2. **Mode n8n** (complémentaire): Workflow `survey-cleaner-mvp` pour upload via UI
3. **Mode AWS Lambda**: Script `clean.py` exposé via `clean_data(df)` pour pipeline_sondages

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

- **Logs**: `surveys/{nom}/process.log` contient tous les appels API et résultats
- **Debug agent**: Modifier `.claude/agents/{agent}.md` puis relancer `run_cleaner.sh`
- **Tools**: Tous les tools sont dans `agent_tools.py` (bash, read, write, edit)
- **Limiter variables**: `--limit N` pour tester sur N variables seulement
- **Règles de nettoyage**: `surveys/cleaning_rules.json` contient patterns communs

**Développer un nouvel agent:**
1. Créer `.claude/agents/mon-agent.md` avec instructions
2. Ajouter fonction dans `process_survey.py` qui appelle `call_agent("mon-agent", prompt)`
3. L'agent aura accès aux 4 tools définis dans `agent_tools.py`

## Roadmap

- **MVP 1**: ✅ Form upload n8n + traitement codebook TXT
- **MVP 2**: ✅ Système agentic via API avec tool use
- **MVP 3**: ✅ Processing variable-par-variable avec validation
- **MVP 4**: ✅ Script dual-mode (AWS + local)
- **Next**:
  - Améliorer fuzzy matching cross-survey
  - Détection automatique de variables similaires entre sondages
  - Dashboard de monitoring (taux de succès, temps par variable)

## Intégration avec le projet parent

Ce composant s'intègre dans le projet Opubliq comme outil d'alimentation pour le moteur de recherche de sondages.