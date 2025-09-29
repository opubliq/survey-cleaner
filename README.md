# Survey Cleaner

Outil pour automatiser le nettoyage manuel de fichiers de sondages (CSV/SAV/XLSX) à partir d'un codebook, avec Claude comme assistant interactif.

## Branch: manual-survey-cleaning

Cette branch est dédiée au **nettoyage manuel interactif** de sondages avec l'aide de Claude. Le workflow consiste à:

1. Placer les fichiers bruts dans `surveys/{survey-id}/raw/`
2. Utiliser l'agent `survey-cleaner-agent` de Claude pour analyser et nettoyer variable par variable
3. Générer un script Python `clean.py` qui peut être déployé sur AWS
4. Obtenir les données nettoyées dans `surveys/{survey-id}/processed/`

## ⚠️ IMPORTANT: Setup de l'environnement Python

**Avant de commencer à coder ou utiliser l'agent, vous DEVEZ créer et activer le virtual environment Python:**

### Setup automatique (recommandé)

```bash
./setup.sh
source venv/bin/activate
```

### Setup manuel

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Activation pour chaque session

À chaque fois que vous ouvrez un nouveau terminal:

```bash
source venv/bin/activate
```

## Prérequis

- Python 3.9+
- API key Anthropic (Claude Code)

## Structure du projet

```
survey-cleaner/
├── surveys/              # Répertoire des sondages
│   ├── _template/        # Template avec exemple de clean.py
│   └── {survey-id}/      # Un dossier par sondage
│       ├── raw/          # Fichiers bruts (data.csv/sav + codebook.md)
│       ├── processed/    # Données nettoyées (data_cleaned.csv + codebook.json)
│       ├── clean.py      # Script Python généré (pour AWS)
│       └── variables_todo.md  # Suivi des variables traitées
├── tests/                # Scripts de test
├── requirements.txt      # Dépendances Python
├── setup.sh              # Script de setup automatique
├── CLAUDE.md             # Instructions détaillées pour Claude
└── README.md             # Ce fichier
```

## Utilisation

### 1. Préparer les fichiers

Créer un dossier pour votre sondage:

```bash
mkdir -p surveys/{survey-id}/raw
```

Placer dans `surveys/{survey-id}/raw/`:
- **data.csv** (ou .sav, .xlsx) - fichier de données du sondage
- **codebook.md** - codebook déjà converti en Markdown

### 2. Lancer le nettoyage avec Claude

Dans Claude Code, invoquer l'agent:

```
utilise survey-cleaner-agent pour cleaner surveys/{survey-id}
```

L'agent va:
1. Créer le venv s'il n'existe pas déjà
2. Analyser les fichiers bruts
3. Créer `variables_todo.md` pour tracker la progression
4. Traiter chaque variable de façon itérative:
   - Chercher dans le codebook (fuzzy matching)
   - Explorer la variable dans les données
   - Générer le code de nettoyage
   - Valider la transformation
5. Construire le script `clean.py` final
6. Exporter les données nettoyées et le codebook JSON

### 3. Résultats

À la fin du processus, vous aurez:
- `surveys/{survey-id}/clean.py` - script Python pour AWS
- `surveys/{survey-id}/processed/data_cleaned.csv` - données nettoyées
- `surveys/{survey-id}/processed/codebook.json` - métadonnées structurées

## Conventions de nommage

- **Variables démographiques**: préfixe `demo_` (ex: `demo_age`, `demo_gender`)
- **Variables d'opinion**: préfixe `op_` (ex: `op_satisfaction`, `op_trust`)
- **Échelles d'opinion**: normalisées sur 0-1
- **Valeurs manquantes**: `NaN` (pandas convention)

## Documentation complète

Voir [CLAUDE.md](CLAUDE.md) pour:
- Architecture détaillée du projet
- Workflow complet variable-by-variable
- Standards techniques et formats
- Intégration n8n (workflows automatisés)

## Support

Cette branch fait partie du projet Opubliq pour l'alimentation du moteur de recherche de sondages.