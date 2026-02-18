# Survey Cleaner

Pipeline automatisé de nettoyage de sondages québécois (CSV/SAV/XLSX) générant des scripts Python standardisés.

## Architecture

Système 3-tiers pour le nettoyage de variables:

- **Tier 1** (~50% vars): Pattern Engine - règles déterministes générées automatiquement
- **Tier 2** (~40% vars): LLM batch (GLM-5 gratuit)
- **Tier 3** (~10% vars): LLM individuel (cas complexes)

### Composants principaux

```
surveys/
├── orchestrator.py          # Point d'entrée unique
├── pattern_engine/          # Détection et génération de règles
│   ├── pattern_classifier.py
│   ├── pattern_matcher.py
│   ├── rule_generator.py
│   └── patterns/            # Patterns prédéfinis (Likert, demographics, etc.)
├── codebook_parser/         # Parsing des codebooks (PDF/TXT/Markdown)
│   ├── parser.py
│   ├── schemas/
│   └── strategies/
└── llm_processors/          # Traitement LLM (Tier 2/3)
    ├── tier2_batch.py
    └── tier3_individual.py
```

## Setup

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Utilisation

```bash
python surveys/orchestrator.py <survey_id> [--limit N] [--only-var VAR_NAME]
```

Le survey doit exister dans `_SharedFolder_data_produit/{survey_id}/` avec:
- **Fichier de données:** `*.csv`, `*.xlsx`, `*.sav`, ou `*.dta`
- **Codebook (optionnel):** `*.pdf`, `*.pptx`, `*.txt`, ou `*.md`

## Structure du projet

```
survey-cleaner/
├── surveys/                 # Scripts générés + orchestrateur
│   ├── orchestrator.py
│   ├── status.json
│   ├── pattern_engine/
│   ├── codebook_parser/
│   ├── llm_processors/
│   └── {survey_id}/         # Un dossier par sondage
│       └── clean.py         # Script généré
├── .council/                # Multi-LLM decision council (llm-council)
├── tests/
├── _SharedFolder_data_produit/  # Données sources (jamais modifiées)
├── CLAUDE.md               # Documentation complète
└── AGENTS.md               # Instructions pour agents AI
```

## Documentation

- [CLAUDE.md](CLAUDE.md) - Documentation complète du système
- [AGENTS.md](AGENTS.md) - Instructions pour agents AI (tracking, workflow)

## Tests

```bash
venv/bin/python -m pytest tests/
```

## Issue Tracking

Ce projet utilise **bd** (beads). Voir `AGENTS.md` pour les commandes.
