# Upload vers pipeline_sondages AWS

Documentation pour l'intégration entre survey-cleaner et pipeline_sondages AWS.

## Architecture

```
survey-cleaner                    pipeline_sondages (AWS)
├── surveys/                      ├── S3 lac (trigger)
│   ├── survey_001/              │   └── survey_001/
│   │   ├── clean.py     ────────┼──────→ clean.py
│   │   └── data.csv     ────────┼──────→ data.csv
│   └── survey_002/              │             ↓
│                                 ├── Lambda chargeur
                                  │             ↓
upload_to_pipeline.py             ├── S3 entrepot
                                  │   └── data_structured.parquet
                                  │             ↓
                                  ├── Lambda raffineur
                                  │             ↓
                                  └── S3 comptoirs
                                      ├── data_cleaned.parquet
                                      ├── metadata.json
                                      └── codebook.json
```

## Script : upload_to_pipeline.py

### Objectif
Upload automatique de `clean.py` + données vers S3 AWS pour déclencher le pipeline de traitement.

### Usage de base

```bash
# Upload un sondage vers sandbox
python upload_to_pipeline.py trois_rivieres_2024

# Upload vers production
python upload_to_pipeline.py trois_rivieres_2024 --stage prod

# Upload tous les sondages
python upload_to_pipeline.py --all --stage sandbox
```

### Options recommandées

```python
# upload_to_pipeline.py
parser.add_argument('survey_id', nargs='?', help='Survey ID to upload')
parser.add_argument('--stage', default='sandbox', choices=['sandbox', 'dev', 'prod'])
parser.add_argument('--all', action='store_true', help='Upload all surveys')
parser.add_argument('--script-only', action='store_true', help='Upload clean.py only (no trigger)')
parser.add_argument('--data-only', action='store_true', help='Upload data only (re-trigger)')
parser.add_argument('--reprocess', action='store_true', help='Force reprocess with trigger file')
parser.add_argument('--delay', type=int, default=0, help='Delay between uploads (seconds)')
parser.add_argument('--dry-run', action='store_true', help='Show what would be uploaded')
```

## Fonctionnement du pipeline

### Déclencheurs
- **Upload de data.*** dans S3 lac → Lambda chargeur se déclenche
- **clean.py seul** → Aucun déclenchement (attend data)

### Comportement sur re-upload
Si un sondage existe déjà dans l'infrastructure et que tu re-upload :

1. Upload clean.py (nouvelle version) → S3 lac
2. Upload data.csv → S3 lac → **Pipeline se déclenche**
3. Lambda chargeur utilise le **nouveau clean.py**
4. Lambda raffineur utilise le **nouveau clean.py**
5. Fichiers dans comptoirs sont **écrasés** avec nouveaux résultats

**Le pipeline est idempotent** : Re-traiter écrase les anciens résultats.

## Cas d'usage

### 1. Premier upload d'un sondage
```bash
python upload_to_pipeline.py survey_001 --stage sandbox
# → Upload clean.py + data.csv
# → Pipeline se déclenche
# → Vérifie résultats dans S3 comptoirs
```

### 2. Modifier le nettoyage (itération)
```bash
# 1. Modifie clean.py localement
vim surveys/survey_001/clean.py

# 2. Re-upload
python upload_to_pipeline.py survey_001

# → Upload nouveau clean.py + data
# → Pipeline re-traite avec nouveau script
# → Résultats écrasés dans comptoirs
```

### 3. Upload initial de tous les sondages historiques
```bash
python upload_to_pipeline.py --all --stage sandbox --delay 30
# → Upload tous les sondages
# → Délai de 30s entre chaque (évite overload)
# → Confirmation demandée avant execution
```

### 4. Upload script seulement (test sans trigger)
```bash
python upload_to_pipeline.py survey_001 --script-only
# → Upload clean.py seulement
# → Pipeline NOT triggered
# → Utile pour tester/préparer sans déclencher traitement
```

### 5. Forcer re-traitement sans re-upload data
```bash
python upload_to_pipeline.py survey_001 --reprocess
# → Upload fichier _trigger.txt
# → Pipeline se déclenche avec clean.py actuel
```

## Structure attendue dans survey-cleaner

```
surveys/
├── survey_001/
│   ├── clean.py          ← REQUIS - Script avec get_metadata()
│   ├── data.csv          ← REQUIS - Données brutes (ou .xlsx, .sav, .json)
│   └── config.json       ← OPTIONNEL - Metadata du survey (pour référence)
└── survey_002/
    ├── clean.py
    └── data.xlsx
```

## Ce que clean.py doit exposer

```python
# clean.py généré par survey-cleaner

def get_metadata():
    """Intelligence métier fournie par survey-cleaner"""
    return {
        "survey_info": {
            "survey_id": "survey_001",
            "title": "Titre du sondage",
            "description": "Description détaillée",
            "year": 2024,
            "source_url": "https://...",
            "tags": ["infrastructure", "municipal"],
            "n_respondents": 1200
        },
        "codebook": {
            "variable_name": {
                "question_label": "Question en français",
                "value_labels": {
                    "value1": "Label 1",
                    "value2": "Label 2"
                },
                "category": "socio_demographic",
                "type": "categorical"
            }
        }
    }

def clean_data(df):
    """Nettoyage des données"""
    # ... transformations ...
    return df
```

## Configuration AWS

### Credentials
Le script nécessite credentials AWS configurés :

```bash
# Option 1: AWS CLI configuré
aws configure

# Option 2: Variables d'environnement
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_DEFAULT_REGION=ca-central-1

# Option 3: Fichier config/aws_config.json (à créer)
{
  "aws_access_key_id": "...",
  "aws_secret_access_key": "...",
  "region": "ca-central-1"
}
```

### Buckets cibles par stage
- **sandbox**: `pipeline-sondages-lac-sandbox`
- **dev**: `pipeline-sondages-lac-dev`
- **prod**: `pipeline-sondages-lac-prod`

## Monitoring

### Vérifier si upload a réussi
```bash
aws s3 ls s3://pipeline-sondages-lac-sandbox/survey_001/
# → Devrait lister clean.py et data.csv
```

### Vérifier si pipeline a traité
```bash
aws s3 ls s3://pipeline-sondages-comptoirs-sandbox/survey_001/
# → Devrait lister data_cleaned.parquet, metadata.json, codebook.json
```

### Logs des lambdas
```bash
aws logs tail /aws/lambda/pipeline-sondages-chargeur --follow
aws logs tail /aws/lambda/pipeline-sondages-raffineur --follow
```

## Bonnes pratiques

1. **Toujours tester en sandbox d'abord**
   ```bash
   python upload_to_pipeline.py survey_001 --stage sandbox
   # Vérifie résultats
   python upload_to_pipeline.py survey_001 --stage prod
   ```

2. **Utiliser --dry-run pour vérifier avant upload**
   ```bash
   python upload_to_pipeline.py --all --dry-run
   # → Affiche ce qui serait uploadé sans exécuter
   ```

3. **Batch upload avec delay pour éviter overload**
   ```bash
   python upload_to_pipeline.py --all --delay 30
   # → 30s entre chaque upload
   ```

4. **Itérer rapidement sur un sondage**
   ```bash
   # Cycle rapide:
   vim surveys/survey_001/clean.py
   python upload_to_pipeline.py survey_001
   # Vérifie résultats dans comptoirs
   # Répète jusqu'à satisfaction
   ```

## Prochaines étapes (futures améliorations)

1. **Intégration n8n** : Automatiser upload après génération de clean.py
2. **Notifications** : Email/Slack quand pipeline termine (succès/erreur)
3. **Dashboard** : Interface web pour voir status des sondages
4. **Validation** : Vérifier clean.py avant upload (lint, structure)
5. **Versioning** : Garder historique des versions dans S3

## Troubleshooting

### "No data file found"
→ Vérifie que tu as un fichier `data.*` dans le dossier du survey

### "Pipeline not triggered"
→ Seul l'upload de data.* déclenche le pipeline, pas clean.py seul

### "Permission denied"
→ Vérifie tes credentials AWS

### "Lambda timeout"
→ Vérifie les logs CloudWatch, peut-être erreur dans clean.py
