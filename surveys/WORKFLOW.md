# Survey Cleaning Workflow

Système agentic pour générer des scripts `clean.py` qui seront exécutés dans pipeline_sondages.

## Architecture

```
_SharedFolder_data_produit/{survey_id}/  Fichiers sources (data.csv, codebook.pdf)
         ↓
Agents Claude Code                   Génèrent clean.py variable par variable
         ↓
surveys/{survey_id}/clean.py        Script de nettoyage prêt
         ↓
upload_to_pipeline.py               Upload vers AWS S3
         ↓
pipeline_sondages (AWS)             Exécute clean.py, génère codebook.json
```

## Tracking: status.json

Fichier central `surveys/status.json` qui track l'état de tous les sondages.

**Structure**:
```json
{
  "surveys": {
    "survey_id": {
      "status": "not_started|in_progress|completed",
      "variables": {"total": 150, "cleaned": 45, "pending": 105},
      "pipeline": {"uploaded": false}
    }
  }
}
```

## Agents Claude Code

### 1. survey-init-agent
**Rôle**: Initialise le sondage
- Copie template clean.py → `surveys/{survey_id}/clean.py`
- Remplit `SURVEY_METADATA` (survey_id, title, year, etc.)
- **CRÉE** entrée dans status.json avec status=`not_started`

### 2. transform-codebook-agent
**Rôle**: Transforme codebook original en format lisible
- Lit `sharedfolder/{survey_id}/codebook.*` (PDF/PPTX/TXT)
- Génère `sharedfolder/{survey_id}/codebook.md` (format standardisé)
- Pas de mise à jour status.json

### 3. clean-variable-agent
**Rôle**: Nettoie UNE variable (appelé N fois)
- Lit codebook.md
- Explore la variable raw dans data.*
- Génère code de nettoyage dans `clean.py` (fonction clean_data)
- Génère entrée CODEBOOK_VARIABLES (question_label, type, value_labels)
- **UPDATE** status.json: `variables.cleaned += 1`, `status = in_progress`

### 4. validate-cleaning-agent
**Rôle**: Valide le nettoyage d'une variable
- Exécute le code de cleaning pour cette variable
- Compare distribution raw vs cleanée
- Vérifie cohérence
- Pas de mise à jour status.json (validation inline)

### 5. finalize-survey-agent (nouveau)
**Rôle**: Finalise le sondage quand toutes les variables sont cleanées
- Vérifie que SURVEY_METADATA est complet
- Vérifie que toutes les variables ont entrée CODEBOOK_VARIABLES
- **UPDATE** status.json: `status = completed`

## Scripts Python

### upload_to_pipeline.py
**Rôle**: Upload vers AWS pour exécution
- Lit `surveys/{survey_id}/clean.py`
- Upload vers S3 `pipeline-sondages-lac-{stage}/{survey_id}/clean.py`
- Upload data.* depuis sharedfolder vers S3 (trigger pipeline)
- **UPDATE** status.json: `pipeline.uploaded = true`, `pipeline.uploaded_date`, `pipeline.stage`

### status.py (utilitaire)
**Rôle**: Gestion de status.json
- `python status.py list` - Liste tous les sondages avec leur statut
- `python status.py sync` - Synchronise avec filesystem + AWS
- `python status.py show <survey_id>` - Détails d'un sondage
- Pas de modification par agents (juste lecture/sync manuel)

## Workflow typique

```bash
# 1. Initialiser le sondage
/init-survey ces2019
# → Crée surveys/ces2019/clean.py
# → status.json: {"ces2019": {"status": "not_started"}}

# 2. Transformer le codebook
/transform-codebook ces2019
# → Crée sharedfolder/ces2019/codebook.md

# 3. Nettoyer chaque variable (repeat N fois)
/clean-var ces2019 ses_province
# → Ajoute code dans clean.py
# → status.json: variables.cleaned += 1

/validate-cleaning ces2019 ses_province
# → Valide la transformation

# 4. Finaliser
/finalize-survey ces2019
# → status.json: status = "completed"

# 5. Upload vers pipeline
python upload_to_pipeline.py ces2019 --stage sandbox
# → Upload vers AWS S3
# → status.json: pipeline.uploaded = true
```

## Fichiers générés

```
surveys/
├── status.json                  ← Tracking central (créé au premier init)
├── ces2019/
│   └── clean.py                 ← Script généré par agents
└── ces2021/
    └── clean.py

_SharedFolder_data_produit/
├── ces2019/
│   ├── data.csv                 ← Source (déjà présent)
│   ├── codebook.pdf             ← Source (déjà présent)
│   └── codebook.md              ← Généré par transform-codebook
└── ces2021/
    └── ...
```
