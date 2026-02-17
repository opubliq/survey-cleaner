# Survey Cleaner v2: Architecture Organisation

## Structure Proposée

```
surveys/                              # Core system (existant + extensions)
├── orchestrator.py                  # Existant: point d'entrée, à améliorer
├── pattern_engine/                 # NOUVEAU: Cœur du système hybride
│   ├── pattern_library.json        # Pattern library partagée et persistente
│   ├── patterns/
│   │   ├── __init__.py
│   │   ├── likert_scales.py      # Patterns Likert 3/4/5/7 points
│   │   ├── demographics.py        # Patterns age, sexe, province, region
│   │   ├── binary.py             # Patterns oui/non, 0/1
│   │   └── scales.py             # Échelles 0-10, thermomètres
│   ├── rule_generator.py          # Génère code Python depuis pattern + codebook
│   ├── rule_validator.py         # LLM valide les règles (Tier 1)
│   ├── pattern_classifier.py     # Classification data-driven (min/max/unique/dist)
│   └── pattern_matcher.py        # Matching signature-based
├── codebook_parser/               # NOUVEAU: Parsing structuré
│   ├── parser.py                # Parse codebook → JSON (PDF/Excel/MD)
│   ├── schemas/
│   │   ├── codebook_schema.py   # Schéma Pydantic pour validation
│   │   └── variable_schema.py    # Schéma pour une variable
│   └── templates/               # Templates prompts LLM (avec caching)
├── llm_processors/               # NOUVEAU: 3-Tier LLM strategy
│   ├── tier1_validator.py        # LLM validation pour règles (Kimi/GLM-5)
│   ├── tier2_batch.py           # Batch LLM semi-standard (GLM-5/GLM-4.7)
│   ├── tier3_individual.py      # LLM individuel complexe (Claude Haiku)
│   ├── batcher.py              # Utilitaire: grouper variables par batch
│   └── prompt_cache.py         # Cache système prompts (codebook, patterns)
├── validation/                    # NOUVEAU: Validation layer
│   ├── validator.py             # Validation automatique (syntaxe, range, types)
│   ├── quality_reporter.py     # Rapport de qualité par sondage
│   └── conflict_resolver.py     # Résolution conflits de mapping
├── cli/                          # NOUVEAU: Interface utilisateur
│   ├── __init__.py
│   ├── main.py                 # CLI entry point (`survey-cleaner` command)
│   ├── commands/
│   │   ├── clean.py          # `survey-cleaner clean <survey_id>`
│   │   ├── watch.py          # `survey-cleaner watch`
│   │   ├── pattern.py         # `survey-cleaner pattern add/list`
│   │   └── config.py         # `survey-cleaner config`
│   └── output/                # Formatters (progress bars, tableaux)
├── config/                        # NOUVEAU: Configuration
│   ├── models.json              # Définition des modèles (tier1/2/3)
│   ├── config_schema.py        # Validation Pydantic de la config
│   └── defaults.yaml            # Valeurs par défaut
├── _template/
│   └── clean.py                 # Template pour clean.py (existant)
├── status.json                   # Tracking (existant)
├── INSTRUCTIONS.MD               # Instructions utilisateur (existant)
└── WORKFLOW.md                  # Workflow documentation (existant)

survey_cleaner_cli/                # NOUVEAU: Package CLI portable
├── package.json                 # npm package
├── bin/
│   └── survey-cleaner           # Entrée CLI
├── src/
│   ├── cli.py                    # Interface CLI
│   └── lib/                     # Logique partagée avec surveys/
└── README.md

~/.survey-cleaner/                # NOUVEAU: Config utilisateur locale
├── config.json                 # Config utilisateur
├── pattern_library.json        # Copy locale (optionnel, override global)
└── logs/
```

## Organisation des issues BD (Proposée)

### Phase 1: Foundation (Weeks 1-2)

```
1. Pattern Library Structure
   - surveys/pattern_engine/pattern_library.json schema
   - surveys/pattern_engine/patterns/ modules
   → Issue: "Setup pattern library structure"

2. Codebook Parser Foundation
   - surveys/codebook_parser/schemas/ Pydantic models
   - surveys/codebook_parser/parser.py shell
   → Issue: "Create codebook parser foundation"

3. Configuration System
   - surveys/config/models.json schema
   - surveys/config/config_schema.py validation
   - surveys/config/defaults.yaml defaults
   → Issue: "Implement configuration system"

4. CLI Skeleton
   - surveys/cli/main.py entry point
   - surveys/cli/commands/ stubs
   → Issue: "Create CLI skeleton"
```

### Phase 2: Core Components (Weeks 2-3)

```
5. Pattern Definitions (Likert, demographics, binary)
   - surveys/pattern_engine/patterns/likert_scales.py
   - surveys/pattern_engine/patterns/demographics.py
   - surveys/pattern_engine/patterns/binary.py
   → Issue: "Implement core patterns (Likert, demo, binary)"

6. Rule Generator
   - surveys/pattern_engine/rule_generator.py
   → Issue: "Build rule generator from patterns + codebook"

7. Pattern Classifier
   - surveys/pattern_engine/pattern_classifier.py (data-driven)
   → Issue: "Build pattern classifier (stats-based)"

8. Codebook Parser
   - surveys/codebook_parser/parser.py (GLM-5/Kimi)
   → Issue: "Complete codebook parser (PDF/Excel → JSON)"

9. Rule Validator (Tier 1 LLM)
   - surveys/llm_processors/tier1_validator.py
   → Issue: "Build Tier 1 LLM validator"

10. Validation Layer
    - surveys/validation/validator.py
    → Issue: "Implement validation layer"
```

### Phase 3: Tier 2 & 3 Processing (Weeks 3-4)

```
11. Tier 2 Batch Processor
    - surveys/llm_processors/tier2_batch.py
    - surveys/llm_processors/batcher.py
    → Issue: "Build Tier 2 batch LLM processor"

12. Tier 3 Individual Handler
    - surveys/llm_processors/tier3_individual.py
    → Issue: "Build Tier 3 individual LLM handler"

13. Prompt Caching System
    - surveys/llm_processors/prompt_cache.py
    → Issue: "Implement prompt caching for codebook"
```

### Phase 4: Orchestrator & CLI (Weeks 4-5)

```
14. Enhanced Orchestrator
    - surveys/orchestrator.py refactor
    - Integrate pattern_engine, codebook_parser, llm_processors
    - Tier routing logic (1→2→3)
    → Issue: "Refactor orchestrator with 3-tier architecture"

15. CLI Commands Implementation
    - surveys/cli/commands/clean.py
    - surveys/cli/commands/watch.py
    - surveys/cli/commands/pattern.py
    - surveys/cli/commands/config.py
    → Issue: "Implement CLI commands (clean, watch, pattern, config)"

16. Output Formatters
    - surveys/cli/output/ (progress bars, tables)
    → Issue: "Add CLI output formatting"

17. Quality Reporter
    - surveys/validation/quality_reporter.py
    → Issue: "Build quality reporter"
```

### Phase 5: Testing & Refinement (Weeks 5-6)

```
18. End-to-End Testing
    - Test sur 3-5 sondages existants
    → Issue: "E2E testing on existing surveys"

19. Pattern Library Bootstrap
    - Analyser 3-5 sondages
    - Extraire 5-10 patterns récurrents
    → Issue: "Bootstrap pattern library from existing surveys"

20. Cost Validation
    - Mesurer coût réel vs estimation
    → Issue: "Validate cost estimates vs reality"
```

### Phase 6: Documentation & Polish (Weeks 6-7)

```
21. Documentation
    - README.md (quick start)
    - PATTERN_LIBRARY.md (contribution guide)
    - TROUBLESHOOTING.md
    → Issue: "Write comprehensive documentation"
```

## Migration Path

L'existant `surveys/orchestrator.py` peut être **progressivement refactoré** plutôt que remplacé:

**Sprint 1**: Créer les nouveaux modules parallèles à orchestrator.py
**Sprint 2**: Intégrer pattern_engine dans orchestrator.py (mode hybride)
**Sprint 3**: Remacer orchestrator.py avec nouvelle architecture
**Sprint 4**: CLI interface, déprécier usage direct de orchestrator.py

## Notes

- **Pattern Library Persistence**: Centralisée dans `surveys/pattern_engine/pattern_library.json` (shared across all surveys)
- **Config Priorité**: `~/.survey-cleaner/config.json` > `surveys/config/defaults.yaml` > code
- **CLI Portabilité**: `survey-cleaner` package peut être utilisé en dehors du repo (installation npm)
- **Orchestrateur Réutilisable**: Keep `surveys/orchestrator.py` fonctionnel en cas de rollback
