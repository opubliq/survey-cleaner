# Plan de Refactoring: Survey Cleaner v2

## Résumé Exécutif

Construire un système hybride (règles + LLM 3-Tier) qui réduit le coût de **38$/sondage** à **$0.50-$2.50/sondage** tout en maintenant l'autonomie et la qualité.

## Stratégie de Branche

**Approche choisie**: Évolution itérative depuis `manual-survey-cleaning`

**Pourquoi**: `orchestrator.py` fonctionne et est testé → rollback facile si problème, cohabitation possible pendant transition

---

## Séquence d'Actions

### 1. Créer la branche

```bash
git checkout manual-survey-cleaning
git checkout -b feature/survey-cleaner-v2-evolve
```

### 2. Cleanup des fichiers obsolètes (racine)

À faire AVANT de créer les issues BD pour avoir un repo propre:

```bash
rm tracker.py generate_codebook.py extract_excel_sheets.py explore_q12_m2.py temp_explore_q12_m7.py
```

**Pourquoi ces fichiers?**
- `tracker.py`: Logic de tracking intégrée dans `surveys/status.json`
- `generate_codebook.py`: Remplacé par `surveys/codebook_parser/parser.py`
- `extract_excel_sheets.py`: Fonction utilitaire intégrée dans parser
- `explore_q12_*.py`: Scripts d'exploration ad-hoc

### 3. Créer les issues BD (dans l'ordre logique)

Une fois le cleanup fait, créer 6 issues BD pour les 6 phases:

#### Issue 1: Pattern Library Structure

```bash
bd ready
bd create --description "Créer structure pattern_engine avec Pydantic schemas" --design "○ P0"
```

**Contenu à inclure dans `--description`**:

Créer `surveys/pattern_engine/` avec:
```
surveys/pattern_engine/
├── pattern_library.json        # Schéma Pydantic pour validation
├── patterns/
│   ├── __init__.py
│   ├── likert_scales.py      # Classes Likert 3/4/5/7 points
│   ├── demographics.py        # Classes age, sexe, province, region
│   ├── binary.py             # Classes oui/non, 0/1
│   └── scales.py             # Échelles 0-10, thermomètres
├── rule_generator.py          # Génère code Python depuis pattern + codebook
├── rule_validator.py         # LLM valide les règles (Tier 1)
├── pattern_classifier.py     # Classification data-driven (min/max/unique/dist)
└── pattern_matcher.py        # Matching signature-based
```

#### Issue 2: Codebook Parser Foundation

```bash
bd create --description "Parser codebook structuré en JSON (PDF/Excel/MD → JSON)" --design "○ P0"
```

**Contenu**:

Créer `surveys/codebook_parser/` avec:
```
surveys/codebook_parser/
├── schemas/
│   ├── codebook_schema.py   # Schéma Pydantic pour validation
│   └── variable_schema.py    # Schéma pour une variable
├── parser.py                # Parse codebook → JSON (GLM-5/Kimi)
├── templates/               # Templates prompts LLM (avec caching)
└── validators/
    └── codebook_validator.py  # Validation des outputs LLM
```

#### Issue 3: Core Patterns Implementation

```bash
bd create --description "Implémenter patterns Likert, demo, binary" --design "● P1"
```

**Contenu**:

Créer `surveys/pattern_engine/patterns/` avec:
- `likert_scales.py` - Likert 3, 4, 5, 7 points (accord/désaccord, fréquence, etc.)
- `demographics.py` - Province Québec, age, sexe, revenu
- `binary.py` - Oui/Non, 0/1, vrai/faux

#### Issue 4: Rule Generator & Validator

```bash
bd create --description "Générateur de règles + validateur LLM (Tier 1)" --design "● P1"
```

**Contenu**:

Créer `surveys/pattern_engine/` avec:
- `rule_generator.py` - Génère code Python depuis pattern + codebook JSON
- `rule_validator.py` - LLM valide les règles générées (Kimi/GLM-5, validation obligatoire)

#### Issue 5: Tier 2 & 3 LLM Processors

```bash
bd create --description "Processors LLM 3-Tier (batch pour semi-standards, individuel pour complexes)" --design "● P1"
```

**Contenu**:

Créer `surveys/llm_processors/` avec:
- `tier1_validator.py` - LLM validation pour règles (Kimi/GLM-5)
- `tier2_batch.py` - Batch LLM semi-standard (GLM-5/GLM-4.7, 10-20 vars/batch)
- `tier3_individual.py` - LLM individuel complexe (Claude Haiku)
- `batcher.py` - Utilitaire pour grouper variables par batch
- `prompt_cache.py` - Cache système prompts (codebook, patterns)

#### Issue 6: Orchestrator & CLI

```bash
bd create --description "Refactor orchestrator.py + interface CLI portable" --design "● P2"
```

**Contenu**:

Créer/Modifier `surveys/orchestrator.py` avec:
- Intégration de pattern_engine, codebook_parser, llm_processors
- Logique de routing Tier 1→2→3 (data-driven)
- Gestion de state avec `status.json`

Créer `surveys/cli/` avec:
- `main.py` - Entry point CLI (`survey-cleaner` command)
- `commands/` - `clean.py`, `watch.py`, `pattern.py`, `config.py`
- `output/` - Formatters (progress bars, tableaux)

Créer `surveys/config/` avec:
- `models.json` - Définition des modèles par tier
- `config_schema.py` - Validation Pydantic
- `defaults.yaml` - Valeurs par défaut

---

## Nouvelle Architecture

```
surveys/                              # Core system
├── pattern_engine/                 # NOUVEAU: Cœur du système hybride
│   ├── pattern_library.json        # Pattern library partagée et persistente
│   ├── patterns/                     # Définitions de patterns
│   ├── rule_generator.py          # Génère code depuis pattern + codebook
│   ├── rule_validator.py         # LLM valide les règles (Tier 1)
│   └── pattern_classifier.py     # Classification data-driven
├── codebook_parser/               # NOUVEAU: Parsing structuré
│   ├── parser.py                # Parse codebook → JSON (GLM-5/Kimi)
│   ├── schemas/                   # Pydantic models
│   └── templates/               # Templates prompts LLM
├── llm_processors/               # NOUVEAU: 3-Tier LLM strategy
│   ├── tier1_validator.py        # LLM validation règles (Kimi)
│   ├── tier2_batch.py           # Batch LLM semi-standard (GLM-5)
│   ├── tier3_individual.py      # LLM individuel complexe (Haiku)
│   ├── batcher.py                # Utilitaire batching
│   └── prompt_cache.py         # Cache prompts
├── validation/                    # NOUVEAU: Validation layer
│   ├── validator.py             # Validation automatique
│   ├── quality_reporter.py     # Rapport qualité par sondage
│   └── conflict_resolver.py     # Résolution conflits
├── cli/                          # NOUVEAU: Interface utilisateur
│   ├── main.py                 # CLI entry point
│   ├── commands/               # `clean`, `watch`, `pattern`, `config`
│   └── output/                # Formatters
├── config/                        # NOUVEAU: Configuration
│   ├── models.json              # Modèles par tier
│   ├── config_schema.py        # Validation
│   └── defaults.yaml            # Defaults
├── _template/clean.py             # Template (existant)
├── status.json                   # Tracking (existant)
├── INSTRUCTIONS.MD               # Instructions (existant)
└── WORKFLOW.md                  # Workflow (existant)

survey_cleaner_cli/                # NOUVEAU: Package CLI portable
├── package.json                 # npm package
├── bin/survey-cleaner           # Entrée CLI
├── src/cli.py                   # Interface
└── README.md

~/.survey-cleaner/                # NOUVEAU: Config utilisateur locale
├── config.json                 # Config utilisateur
├── pattern_library.json        # Copy locale (optionnel, override global)
└── logs/
```

## Architecture du Système Hybride

```
[BOOTSTRAP - une fois par sondage]
└─ Parse raw codebook → JSON structuré (GLM-5/Kimi)
   (Templates prompts avec caching)

[VARIABLE PROCESSING LOOP - orchestré par Python]
├─ Variable → Classifier (data-driven: min/max/unique/dist)
│
│   ├─ Tier 1 (Règles + Validation LLM) - 40-50% vars
│   │   ├─ Pattern match (signature-based)
│   │   ├─ Rule génère code Python (pattern + codebook JSON)
│   │   └─ LLM valide (Kimi/GLM-5): per-survey variations (missing codes, échelles inversées)
│   │   └─ Coût: 1 quick validation LLM (pas full generation)
│   │
│   ├─ Tier 2 (Batch LLM Semi-Standard) - 40-50% vars
│   │   └─ Process 10-20 vars/batch (GLM-5/GLM-4.7 gratuits)
│   │   └─ Coût: partagé entre 10-20 variables
│   │
│   └─ Tier 3 (LLM Individuel Complexe) - 5-10% vars
│       ├─ Single variable (Haiku)
│       ├─ Codebook JSON snippet en contexte
│       ├─ Prompt focalisé
│       └─ Coût: ~500-700 tokens/variable
│
└─ Généérer clean.py (Python code assemblé)

[CLEANUP & VALIDATION]
├─ Valider syntaxe Python
├─ Checks types, ranges, valeurs non mappées
├─ Flag variables problèmes pour review humain
└─ Sauver data_cleaned.csv + codebook.json final
```

## 3-Tier Model Strategy

| Tier | Rôle | Modèle | Granularité | Coût estimatif |
|-------|--------|---------|-------------|----------------|
| **Tier 1** | Validation LLM de règles | Kimi K2.5 ou GLM-5 (gratuits) | 1 appel/variable rapide (validation) |
| **Tier 2** | Batch LLM semi-standard | GLM-5 ou GLM-4.7 (gratuits) | 10-20 vars/batch partagé |
| **Tier 3** | LLM individuel complexe | Claude Haiku ($0.0003/1K) | Cas complexes individuels |

**Pourquoi Haiku pour Tier 3?** - Moins cher que Sonnet, suffisant pour cas bien définis (codebook structuré disponible)

## Estimation de Coût Réaliste

### Par sondage de 84 variables

| Tier | Variables | Appels LLM | Coût LLM | Coût Total |
|-------|-----------|-------------|-----------|------------|
| Tier 1 | ~42 vars (50%) | ~42 validations | ~$0 (gratuits) | ~$0 |
| Tier 2 | ~33 vars (40%) | ~2-3 batches | ~$0.20 (gratuits) | ~$0.20 |
| Tier 3 | ~9 vars (10%) | ~9 appels | 5K tokens/variable × 9 = ~45K | ~$0.01 (Haiku) |
| **TOTAL** | 84 vars | - | - | **~$0.21/sondage** |

**Réduction**: 99.4% vs $38 actuel

---

## Workflow Utilisateur Final

### Usage Basique

```bash
# Nettoyer un sondage (après setup)
python surveys/orchestrator.py clean <survey_id>

# Ou avec la nouvelle CLI (après implémentation)
survey-cleaner clean <survey_id>
```

### Watch Mode (Automatique)

```bash
# Surveiller le dossier pour nouveaux sondages
survey-cleaner watch --dir _SharedFolder_data_produit
```

**Comportement**:
- Poll toutes les 5 minutes
- Déclenche `survey-cleaner clean` automatiquement pour nouveaux sondages
- Log avec timestamps dans `~/.survey-cleaner/logs/`

### Configuration

```bash
# Éditer la config utilisateur
survey-cleaner config

# Format JSON
{
  "models": {
    "tier1_validator": "opencode/kimi-k2.5-free",
    "tier2_batch": "opencode/glm-5-free",
    "tier3_individual": "anthropic/claude-3-5-haiku-20241022"
  },
  "paths": {
    "data_root": "/path/to/_SharedFolder_data_produit",
    "pattern_library": "~/.survey-cleaner/pattern_library.json"
  },
  "api_keys": {
    "anthropic": "sk-ant-..."
    "opencode": "auto"
  }
}
```

---

## Métriques de Succès

| Métrique | Actuel | Cible | Commentaire |
|-----------|---------|--------|------------|
| Coût/sondage (84 vars) | $38 | <$2.50 | Réduction 99.4% |
| Temps/sondage | N/A | <2h | Autonome |
| Intervention humaine | 100% | <20% | Validation échantillonnée |
| Couverture pattern library | 0% | 80%+ | Après 10-15 sondages |
| Qualité des transformations | ~90% | >95% | Validation automatique |
| Scalabilité | N/A (57 sondages = impraticable) | 50+ sondages/an | Autonome |

---

## Risques & Atténuations

| Risque | Probabilité | Mitigation |
|---------|-------------|------------|
| Complexité pattern matching | Moyenne | Validation LLM Tier 1 ajuste |
| Coût modèles payants si limit dépassée | Faible | Haiku pour Tier 3, fallback gratuit |
| Qualité modèles gratuits < payants | Faible | Validation humaine initiale, puis confiance |
| Compatibilité backward | N/A (nouveau système) | Orchestrator v2 peut cohabiter |
| Bug parsing codebook | Moyenne | Templates robustes + fallback LLM |

---

## Notes

- **Pattern library persistente**: Partagée entre tous les sondages, apprend progressivement
- **Codebook structuré**: JSON schema → plus robuste que Markdown
- **3-Tier routing**: Classifie automatiquement variables → adapte à complexité
- **CLI portable**: Peut être installé via npm, fonctionne en dehors du repo
- **Cohabitation**: Ancien `orchestrator.py` reste fonctionnel pendant transition

---

**Date**: 2025-02-17
**Contexte**: Conseil multi-LLM (session 20260217-164906)
**Verdict**: `council/sessions/20260217-164906/verdict.md`
