# Survey Cleaner - Documentation Système

## Vue d'ensemble

Système automatisé de nettoyage de sondages utilisant l'API Claude avec prompt caching pour un traitement efficace et scalable.

**Architecture:** Un seul point d'entrée (`orchestrator.py`) qui orchestre des agents spécialisés via appels API directs.

**Principe clé:** Les données restent dans `_SharedFolder_data_produit/` et ne sont jamais copiées. Seul le script `clean.py` est généré dans `surveys/`.

## Installation rapide

```bash
# 1. Setup venv
python3 -m venv venv
source venv/bin/activate

# 2. Installer dépendances
pip install -r requirements.txt

# 3. Configurer API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# 4. Tester (nécessite un survey dans _SharedFolder_data_produit/)
python surveys/orchestrator.py test --limit 3
```

## Utilisation

### Commande principale

```bash
python surveys/orchestrator.py <survey_id> [OPTIONS]

# Exemples:
python surveys/orchestrator.py mon_sondage              # Nettoie tout
python surveys/orchestrator.py mon_sondage --limit 10   # Limite à 10 vars
python surveys/orchestrator.py mon_sondage --only-var age  # Nettoie 1 var
```

### Prérequis

Le survey doit exister dans `_SharedFolder_data_produit/{survey_id}/` avec:
- **Fichier de données:** `*.csv`, `*.xlsx`, `*.sav`, ou `*.dta`
- **Codebook (optionnel):** `*.pdf`, `*.pptx`, `*.txt`, ou `*.md`

**Note:** L'orchestrateur initialise automatiquement le survey s'il n'existe pas dans `status.json`.

## Workflow complet

L'orchestrateur exécute 4 étapes automatiquement:

### Step 0: Initialisation (auto si nécessaire)

**Agent:** `survey-init`
**Tokens:** ~2-3K (Haiku)

**Actions:**
- Vérifie que `_SharedFolder_data_produit/{survey_id}/` existe
- Identifie le fichier data et compte les variables
- Crée entrée dans `surveys/status.json`
- Crée répertoire `surveys/{survey_id}/`
- Copie template `clean.py` vers `surveys/{survey_id}/clean.py`

**Important:** Les données ne sont **jamais copiées**. Elles restent dans `_SharedFolder_data_produit/` et sont accédées directement.

### Step 1: Transformation du codebook

**Agent:** `transform-codebook`
**Tokens:** ~20K (Sonnet, création cache)

**Actions:**
- Parse le codebook source (PDF/TXT/PPTX → Markdown)
- Génère `_SharedFolder_data_produit/{survey_id}/codebook.md` standardisé
- Cache le codebook pour réutilisation dans les étapes suivantes

### Step 2: Nettoyage variable par variable

**Agent:** `clean-variable`
**Tokens:**
- Première variable: ~25K (création cache instructions + codebook)
- Variables suivantes: ~500 tokens (cache hit 95%)

**Pour chaque variable:**

1. **Explore** la variable (frequencies, type, distribution)
   - Accède aux données dans `_SharedFolder_data_produit/` (path fourni par orchestrator)

2. **Match** dans le codebook (fuzzy matching)
   - Cherche la documentation de la variable

3. **Génère** le code de transformation
   - Détermine le type (catégorielle, Likert, numérique)
   - Crée mapping approprié

4. **Ajoute** au `clean.py` et `VARIABLE_METADATA`
   - Insère transformation dans `surveys/{survey_id}/clean.py`
   - Ajoute labels pour LLMs downstream

5. **Valide** immédiatement (compare raw vs cleaned)
   - L'agent retourne le code de transformation en JSON
   - Orchestrator exécute **seulement ce code** (pas tout clean.py)
   - Affiche fréquences raw vs cleaned côte-à-côte
   - Marque comme nettoyée **seulement si validation OK**

6. **Met à jour** `status.json`

**Validation automatique optimisée:** Après chaque variable, l'orchestrateur:
- Parse la réponse JSON de l'agent pour extraire `transformation_code`
- Charge les données depuis `_SharedFolder_data_produit/`
- Exécute **uniquement** le code de transformation de cette variable (économie de tokens)
- Affiche comparaison visuelle des fréquences
- Vérifie que la transformation a fonctionné

**Avantage:** Au lieu d'exécuter tout `clean.py` (qui peut contenir 50+ variables déjà nettoyées), on exécute seulement la ligne de code de la variable courante. Beaucoup plus rapide et économique.

### Step 3: Finalisation

**Agent:** `finalize-survey`
**Tokens:** ~2-3K (Haiku)

**Actions:**
- Vérifie complétude (toutes variables nettoyées)
- Exécute `clean.py` final
- Génère `processed/data_cleaned.csv` et `codebook.json`
- Marque survey comme "completed" dans `status.json`

## Architecture technique

### Structure des fichiers

```
survey-cleaner/
├── _SharedFolder_data_produit/      # ⭐ Données sources (57 surveys, jamais modifiées)
│   ├── _archives/
│   └── {survey_id}/                 # Ex: eeq_2022/, govcan_2023/, etc.
│       ├── data.csv|xlsx|sav|dta    # Données brutes
│       └── codebook.md|pdf|pptx     # Codebook (source ou généré)
│
├── surveys/                         # ⭐ Scripts générés + orchestrateur
│   ├── orchestrator.py              # Point d'entrée unique
│   ├── status.json                  # Tracking centralisé
│   ├── INSTRUCTIONS.MD              # Instructions de workflow
│   ├── WORKFLOW.md                  # Workflow détaillé
│   ├── _template/
│   │   └── clean.py                 # Template script
│   └── {survey_id}/
│       └── clean.py                 # Script généré progressivement
│
├── council/                         # 🗳️ Multi-LLM decision council
│   ├── council.sh                   # Script d'orchestration (propose→critique→vote→verdict)
│   ├── config.sh                    # Modèles et paramètres
│   ├── templates/                   # Templates de prompts par phase
│   └── sessions/                    # Sessions de délibération
│
├── refactoring/                     # 📋 Docs stratégie et rapports
│   ├── strategie_finale.md          # Stratégie adoptée
│   ├── strategie_cleaning_hybride.md
│   └── rapport_experience_cleaning_manuel.md
│
├── tests/                           # Données de test et codebooks sample
│
├── .claude/agents/                  # Agents Claude (voir ci-dessous)
├── .beads/                          # Issue tracking (bd)
├── requirements.txt
├── setup.sh
└── CLAUDE.md                        # Ce fichier
```

### Agents (instructions)

```
.claude/agents/
├── survey-init.md               # Initialisation (crée clean.py, status.json)
├── transform-codebook.md        # Parse codebook → Markdown
├── clean-variable.md            # Nettoie 1 variable
├── validate-cleaning.md         # Valide transformation (compare raw vs cleaned)
└── finalize-survey.md           # Finalisation
```

### Format de réponse des agents

L'agent `clean-variable` retourne un JSON structuré pour permettre la validation optimisée:

```json
{
  "success": true,
  "variable_name": "Q2_province",
  "standard_name": "ses_province",
  "type": "categorical",
  "transformation_code": "df_clean['ses_province'] = df['Q2_province'].map({1.0: 'qc', 2.0: 'on', 3.0: 'bc', 99.0: np.nan})",
  "metadata": {
    "original_variable": "Q2_province",
    "question_label": "Province de résidence",
    "type": "categorical",
    "value_labels": {"qc": "Québec", "on": "Ontario", "bc": "Colombie-Britannique"}
  },
  "summary": "✓ Variable cleaned: Q2_province → ses_province\nType: categorical"
}
```

Le champ `transformation_code` contient la ligne de code Python exacte qui sera:
1. Exécutée par l'orchestrator pour validation immédiate
2. Déjà insérée dans `clean.py` par l'agent

### Prompt Caching

L'orchestrateur utilise le prompt caching d'Anthropic pour réduire drastiquement les coûts:

```python
# Premier appel (variable 1)
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    system=[
        {
            "text": agent_instructions,        # ~5K tokens
            "cache_control": {"type": "ephemeral"}
        },
        {
            "text": codebook_md,               # ~15K tokens (si disponible)
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": context}]
)
# Total: ~25K tokens (création cache)

# Appels suivants (variables 2-84)
# Total: ~500 tokens (95% cache hit!)
```

**Résultat:** 92K tokens pour un sondage de 84 variables vs 3.9M avec l'ancien système Claude Code Task tool (98% réduction).

## Performance

### Coûts estimés (par sondage de 84 variables)

| Étape | Tokens | Modèle | Coût |
|-------|--------|--------|------|
| Init | 3K | Haiku | $0.0001 |
| Transform codebook | 20K | Sonnet | $0.006 |
| Variable 1 | 25K | Sonnet | $0.0075 |
| Variables 2-84 (83x) | 41K | Sonnet | $0.012 |
| Finalize | 3K | Haiku | $0.0001 |
| **TOTAL** | **92K** | - | **$0.026** |

**Temps estimé:** 8-12 minutes par sondage (84 variables)

### Batch de 40 sondages

- Tokens: 92K × 40 = 3.68M tokens
- Coût: $0.026 × 40 = **$1.04**
- Temps: 10 min × 40 = 6-7 heures (parallélisable à 2-3h avec threading)

## Tracking et monitoring

### status.json

Structure par survey:

```json
{
  "surveys": {
    "mon_sondage": {
      "status": "in_progress",           // not_started | in_progress | completed
      "created_date": "2025-12-05",
      "data_file": "data.csv",
      "n_observations": 2000,
      "n_variables": 84,
      "variables": {
        "total": 84,
        "cleaned": 15,
        "pending": 69
      },
      "last_updated": "2025-12-05T16:46:52"
    }
  }
}
```

### Logs

- **Console:** Progression en temps réel + validation visuelle des fréquences
- **Usage tokens:** Affiché après chaque appel agent (input, output, cache read, cache creation)

## Script clean.py (dual-mode)

Chaque survey génère un `clean.py` qui fonctionne en deux modes:

### Mode AWS (fonction exportée)
```python
from surveys.mon_sondage.clean import clean_data
df_clean = clean_data(df_raw)  # Appelé par pipeline_sondages
```

### Mode local (standalone)
```bash
python surveys/mon_sondage/clean.py  # Génère processed/data_cleaned.csv
```

### Structure du script

```python
import pandas as pd
import numpy as np

# Metadata (labels pour LLMs downstream)
VARIABLE_METADATA = {
    'ses_province': {
        'original_variable': 'Q2_province',
        'question_label': "Province de résidence",
        'type': 'categorical',
        'value_labels': {'qc': "Québec", 'on': "Ontario", ...}
    },
    # ... autres variables
}

def clean_data(df):
    """Transforme raw data → cleaned data"""
    df_clean = pd.DataFrame(index=df.index)

    # Variable 1 - Province de résidence
    # Source: Q2_province
    df_clean['ses_province'] = df['Q2_province'].map({
        1.0: 'qc',
        2.0: 'on',
        # ...
    })

    # Variable 2 - Satisfaction gouvernement
    # Source: satisfaction_gov
    df_clean['op_satisfaction'] = df['satisfaction_gov'].map({
        1.0: 0.0,   # Très insatisfait
        2.0: 0.25,  # Plutôt insatisfait
        3.0: 0.5,   # Neutre
        4.0: 0.75,  # Plutôt satisfait
        5.0: 1.0,   # Très satisfait
        99.0: np.nan
    })

    # ... autres variables

    return df_clean

if __name__ == "__main__":
    # Standalone mode: charge depuis _SharedFolder_data_produit
    import sys
    from pathlib import Path

    survey_id = Path(__file__).parent.name
    data_dir = Path(__file__).parents[1] / "_SharedFolder_data_produit" / survey_id

    # Trouve le fichier data
    data_files = list(data_dir.glob("*.csv")) + list(data_dir.glob("*.xlsx"))
    if not data_files:
        print("ERROR: No data file found")
        sys.exit(1)

    data_file = data_files[0]

    if data_file.suffix == ".csv":
        df = pd.read_csv(data_file)
    elif data_file.suffix in [".xlsx", ".xls"]:
        df = pd.read_excel(data_file)

    df_clean = clean_data(df)

    # Sauvegarde dans processed/
    output_dir = Path(__file__).parent / "processed"
    output_dir.mkdir(exist_ok=True)
    df_clean.to_csv(output_dir / "data_cleaned.csv", index=False)

    print(f"✓ Cleaned data saved to {output_dir / 'data_cleaned.csv'}")
```

## Conventions de nommage des variables

Le système suit des conventions strictes pour les noms de variables standardisées:

- **`ses_*`** - Socio-démographiques (age, gender, income, education, region)
- **`op_*`** - Opinions/attitudes (satisfaction, trust, ideology)
- **`behav_*`** - Comportements (vote choice, participation, media consumption)
- **`know_*`** - Questions de connaissance

**Exemples:**
- `Q2_province` → `ses_province`
- `satisfaction_gov` → `op_satisfaction_gov`
- `vote_choice` → `behav_vote_choice`
- `media_consumption_tv` → `behav_media_tv`

## Types de transformations

### Variables catégorielles
```python
df_clean['ses_province'] = df['Q2_province'].map({
    1.0: 'qc',
    2.0: 'on',
    3.0: 'bc',
    # ...
})
```

### Échelles Likert (normalisées 0-1)
```python
df_clean['op_satisfaction'] = df['satisfaction'].map({
    1.0: 0.0,    # Très insatisfait
    2.0: 0.25,
    3.0: 0.5,
    4.0: 0.75,
    5.0: 1.0,    # Très satisfait
    99.0: np.nan
})
```

### Variables binaires
```python
df_clean['behav_voted'] = df['Q10_vote'].map({
    1.0: 1.0,    # Oui
    2.0: 0.0,    # Non
    99.0: np.nan
})
```

### Variables numériques
```python
# Normalisation 0-100 → 0-1
df_clean['op_thermometer_trudeau'] = df['therm_trudeau'] / 100
df_clean['op_thermometer_trudeau'] = df_clean['op_thermometer_trudeau'].where(
    (df['therm_trudeau'] >= 0) & (df['therm_trudeau'] <= 100),
    np.nan
)
```

## Développement et debugging

### Tester sur petit dataset

```bash
python surveys/orchestrator.py test --limit 3
```

### Modifier un agent

1. Éditer `.claude/agents/{agent_name}.md`
2. Relancer `orchestrator.py` (reload automatique des instructions)

### Ajouter logging détaillé

Modifier `orchestrator.py` ligne ~275 pour ajouter:

```python
print(f"📤 Request: {user_prompt}")
print(f"📥 Response: {result_text}")
```

### Tester clean.py manuellement

```bash
cd surveys/mon_sondage
python clean.py  # Génère processed/data_cleaned.csv
```

## Déploiement AWS

Le script `clean.py` est conçu pour être importé par le Lambda `lambda_raffineur_nettoyage`:

```python
# Dans lambda_raffineur_nettoyage
from surveys.{survey_id}.clean import clean_data

# Applique le nettoyage
df_clean = clean_data(df_raw)
```

Le Lambda upload ensuite `df_clean` vers le bucket S3 pour ingestion par `pipeline_sondages`.

## Limitations

- **Codebook très volumineux (>200 pages):** Peut dépasser limite de cache prompt (20K tokens)
- **Variables extrêmement complexes:** Nécessitent intervention manuelle
- **Formats de données exotiques:** Support limité pour anciens formats `.dta` Stata

## Dépannage

### Survey non trouvé
```
ValueError: Survey mon_sondage not found in status.json
```
**Solution:** L'orchestrateur initialise automatiquement le survey. Vérifier que `_SharedFolder_data_produit/mon_sondage/` existe avec un fichier data.

### Variable pas dans les données
```
ERROR: Variable 'Q99' not found in data
```
**Solution:** L'agent clean-variable liste les colonnes disponibles. Vérifier le nom exact dans le fichier data.

### Validation échoue
```
⚠️ Variable age validation failed
```
**Solution:** Regarder l'output de validation (fréquences raw vs cleaned) pour identifier le problème. Corriger manuellement `clean.py` si nécessaire.

### Erreur d'exécution clean.py
```
⚠️ Failed to execute clean.py: NameError: name 'np' is not defined
```
**Solution:** Vérifier que `import numpy as np` est présent en haut de `clean.py`.

## Roadmap

- ✅ **MVP 1:** Système orchestrator.py avec API + caching
- ✅ **MVP 2:** Auto-init + validation variable par variable
- ✅ **MVP 3:** Data reste dans _SharedFolder_data_produit (pas de copie)
- ✅ **MVP 3.5:** Multi-LLM council pour décisions techniques (`council/council.sh`)
- 🔄 **MVP 4:** Threading pour paralléliser cleaning de 2-3 surveys simultanés
- 📋 **MVP 5:** Dashboard web pour monitoring (status, logs, coûts)
- 📋 **MVP 6:** Auto-detection de variables similaires entre surveys (cross-survey matching)

## Références

- **Stratégie complète:** Voir `refactoring/strategie_finale.md`
- **Métriques performance:** Voir `refactoring/rapport_experience_cleaning_manuel.md`
