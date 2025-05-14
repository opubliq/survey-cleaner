# survey-cleaner
Bot automatisé pour nettoyer des fichiers de sondages (.csv, .sav) à partir d’un codebook, générer un script R de traitement, valider son exécution et insérer les données nettoyées à l'endroit voulu (bucket S3, BD SQL, path, etc.). Optimisé pour les règles de nettoyage spécifiques à Opubliq.

## Objectif

Permettre l'importation rapide et standardisée de fichiers de sondages (CSV/SAV) dans notre moteur de recherche en automatisant:
- L'analyse de structure
- Le nettoyage des données
- La standardisation des variables
- La détection d'erreurs

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

## Structure

```
bot_nettoyage/
├── app.py            # Interface Streamlit
├── api.py            # Communication avec Claude
├── executor.py       # Exécution des scripts R
├── templates/        # Templates de prompts
│   ├── analysis.txt
│   └── cleaning.txt
├── utils/
│   ├── parsers.py    # Parsers CSV/SAV/PDF
│   └── validators.py # Validation des outputs
└── tests/            # Tests unitaires
```

## Roadmap

- **MVP 1**: Upload CSV + génération script simple
- **MVP 2**: Exécution et debug automatique
- **MVP 3**: Support complet formats + optimisation

## Tips pour développement

- Les prompts de Claude sont dans `/templates/`
- Logs d'exécution dans `/logs/`
- Pour débugger, activer le mode verbose: `python process.py --verbose`
- Structure du pipeline existant dans `create_survey_bd`

## Intégration avec le projet parent

Ce composant s'intègre dans le projet Opubliq comme outil d'alimentation pour le moteur de recherche de sondages.