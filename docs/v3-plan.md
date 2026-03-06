# Survey Cleaner v3 — Plan d'architecture

**Date**: 2026-02-22  
**Contexte**: Abandon de la v2 3-tiers déterministe suite à un test run décevant. On repart sur une architecture agent-based simple.

---

## Diagnostic v2

La v2 avait trop de complexité déterministe (pattern engine OOP, pattern_library.json, scoring de confiance à 4 dimensions, orchestrateur 1094 lignes) pour éviter des calls LLM. Sauf que les LLMs gratuits (GLM-5, Kimi, big-pickle) peuvent faire ces tâches triviales pour $0. On a programmé ce qu'on n'avait pas besoin de programmer.

Les tâches réelles sont simples et décomposables:
1. Lire le codebook brut → comprendre la structure d'une variable
2. Regarder la variable dans les données (value counts, dtype)
3. Écrire le code Python de nettoyage
4. Valider que le code tourne

---

## Principe fondateur v3

> Un orchestrateur Python minimal (~100 lignes) qui appelle `opencode prompt --model` en subprocess pour chaque tâche. Chaque agent = un fichier `.claude/agents/*.md`. Les LLMs gratuits font le vrai travail. Parallelisation via un fichier `.py` par variable.

---

## Architecture

```
surveys/pipeline.py                 ← orchestrateur (~100 lignes)
│
├── 1. parse_codebook(survey_id)
│       opencode prompt --model <model> → codebook.json
│
├── 2. [PARALLEL] pour chaque variable:
│       clean_variable(survey_id, var)
│         opencode prompt --model <model> → vars/{var_name}.py
│         [fallback → kimi → big-pickle si échec/timeout]
│
├── 3. assemble(survey_id)
│       concat vars/*.py → clean.py  ← script Python déterministe
│
├── 4. [PARALLEL, OPTIONAL] pour chaque variable:
│       validate_variable(survey_id, var)
│         opencode prompt --model <model> → verdict ok/needs_fix
│         [--skip-validation pour bypasser]
│
└── 5. finalize(survey_id)
        met à jour status.json
```

### Structure de fichiers par sondage

```
surveys/{survey_id}/
├── vars/
│   ├── Q2_province.py      ← généré en parallèle (1 variable = 1 fichier)
│   ├── Q3_age.py
│   ├── Q10_vote.py
│   └── ...
├── codebook.json           ← produit par parse-codebook, source de vérité
├── clean.py                ← assemblé depuis vars/*.py (format final lambda)
└── status.json             ← état du sondage
```

#### Format d'un `vars/{var}.py`

```python
# ses_province — Province de résidence
# Source: Q2_province
df_clean['ses_province'] = df['Q2_province'].map({
    1.0: 'quebec',
    2.0: 'ontario',
    3.0: 'alberta',
    99.0: np.nan
})
CODEBOOK_VARIABLES['ses_province'] = {
    'original_variable': 'Q2_province',
    'question_label': "Dans quelle province habitez-vous?",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario", 'alberta': "Alberta"}
}
```

**Pourquoi un fichier par variable?**
- Parallelisation réelle (N subprocessus simultanés)
- Isolation totale (un agent plante pas les autres)
- Retry facile sur une seule variable
- Débogage trivial
- Le `clean.py` final reste intact (format lambda inchangé)

---

## Les agents

### 1. `transform-codebook` (refactorer)
**Tâche**: Codebook brut (PDF/XLSX/DOCX/MD) → `codebook.json` structuré  
**Modèle**: GLM-5 free → fallback Kimi  
**Input**: `survey_id`, chemin codebook, chemin données  
**Output**: `surveys/{survey_id}/codebook.json`

Format `codebook.json`:
```json
{
  "survey_id": "...",
  "variables": [
    {
      "raw_name": "Q2_province",
      "label": "Province de résidence",
      "type": "categorical",
      "values": {"1": "Québec", "2": "Ontario"},
      "missing_codes": [99]
    }
  ]
}
```

**Changements vs v1**: Modèle assigné, output JSON (pas MD), prompt simplifié pour LLMs cheap.

---

### 2. `clean-variable` (refactorer)
**Tâche**: 1 entrée `codebook.json` + stats variable → `vars/{var}.py`  
**Modèle**: GLM-5 free → Kimi → big-pickle  
**Input**: `survey_id`, `variable_name`, `codebook_entry` (JSON), `value_counts` (JSON)  
**Output**: `surveys/{survey_id}/vars/{variable_name}.py`

**Changements vs v1**:
- Écrit dans `vars/{var}.py` (pas dans `clean.py` directement)
- Input contexte pré-packagé en JSON (pas de lecture fichier par l'agent)
- Modèles cheap assignés, prompt resserré
- Pas de `status.json` update (c'est le rôle du pipeline)

---

### 3. `validate-cleaning` (refactorer)
**Tâche**: Valider `vars/{var}.py` variable par variable  
**Modèle**: GLM-5 free  
**Input**: `survey_id`, `variable_name`, chemin `vars/{var}.py`, chemin données  
**Output**: verdict par variable (`ok` / `needs_fix`) + corrections suggérées  
**Optionnel**: le pipeline peut tourner sans cette étape (`--skip-validation`)

**Changements vs v1**: Variable par variable (pas le `clean.py` assemblé). Pour chaque variable : exécute le code dans un contexte isolé, vérifie les distributions contre les données brutes, détecte NaN excessifs / mappings incorrects / types inattendus. Ne se fie pas aux commentaires dans le code — valide contre les données.

---

### 4. `finalize-survey` (ajustements mineurs)
**Tâche**: Vérifier complétude, mettre `status.json` à `completed`  
**Modèle**: Pas LLM, logique déterministe  
**Changements**: Référencer `vars/*.py` et `codebook.json` au lieu de `codebook.md`

---

### 5. `survey-init` (garder tel quel)
**Tâche**: Copier fichiers, créer structure  
Pas de changements nécessaires.

---

## Orchestrateur `surveys/pipeline.py`

```python
#!/usr/bin/env python3
"""Pipeline v3 — appelle les agents opencode en subprocess"""

import subprocess, json, sys, concurrent.futures
from pathlib import Path

MODELS = {
    "primary": "opencode/glm-5-free",
    "fallback1": "opencode/kimi-k2.5-free",
    "fallback2": "opencode/big-pickle",
}

def run_agent(agent_md, context, models=None):
    """Lance opencode prompt --model avec fallback dynamique."""
    models = models or [MODELS["primary"], MODELS["fallback1"], MODELS["fallback2"]]
    for model in models:
        result = subprocess.run(
            ["opencode", "prompt", "--model", model, "--context", json.dumps(context)],
            input=open(agent_md).read(),
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            return result.stdout
    raise RuntimeError(f"All models failed for {agent_md}")

def clean_survey(survey_id):
    data_dir = Path(f"_SharedFolder_data_produit/{survey_id}")
    survey_dir = Path(f"surveys/{survey_id}")
    survey_dir.mkdir(exist_ok=True)
    (survey_dir / "vars").mkdir(exist_ok=True)

    # 1. Parse codebook
    run_agent(".claude/agents/transform-codebook.md", {"survey_id": survey_id, ...})

    # 2. Load codebook + variable list
    codebook = json.loads((survey_dir / "codebook.json").read_text())

    # 3. Clean variables en parallèle
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        futures = {
            ex.submit(run_agent, ".claude/agents/clean-variable.md", {"var": v, ...}): v
            for v in codebook["variables"]
        }
        for f in concurrent.futures.as_completed(futures):
            var = futures[f]
            # handle result / errors

    # 4. Assemble clean.py depuis vars/*.py
    assemble(survey_dir)

    # 5. Validate
    run_agent(".claude/agents/validate-cleaning.md", {"survey_id": survey_id, ...})

    # 6. Finalize
    update_status(survey_id, "completed")

if __name__ == "__main__":
    clean_survey(sys.argv[1])
```

**Usage**: `python surveys/pipeline.py elxnqc_particip_egm_2021`

---

## Routing modèles

Fallback dynamique: si le modèle primaire échoue (returncode != 0 ou timeout), passe au suivant.

| Tâche | Primaire | Fallback 1 | Fallback 2 |
|-------|----------|------------|------------|
| parse-codebook | GLM-5 free | Kimi free | big-pickle |
| clean-variable | GLM-5 free | Kimi free | big-pickle |
| validate-cleaning | GLM-5 free | Kimi free | — |
| Ollama local | À tester plus tard | — | — |

Config dans `surveys/config.json` (user-editable).

---

## Ce qu'on garde de la v2

| Composant | Décision | Raison |
|-----------|----------|--------|
| `surveys/io.py` | Garder | Lecture robuste CSV/SAV/XLSX/DTA, bien testé |
| `.claude/agents/` | Refactorer | Base solide, prompt à réécrire |
| Template `clean.py` | Garder | Format lambda inchangé |
| `data/battue_100vars.json` | Garder | Insights empiriques sur les patterns réels |
| Conventions nommage (`ses_*`, `op_*`, `behav_*`) | Garder | Standard établi |
| `surveys/status.json` | Garder | Tracking per-survey |

## Ce qu'on archive (branche `v2-archive`)

- `surveys/pattern_engine/` — logique déterministe complexe, inutile
- `surveys/llm_processors/` — tier2/tier3 processors, remplacés par agents
- `surveys/orchestrator.py` — 1094 lignes, remplacé par ~100 lignes
- `surveys/codebook_parser/` — remplacé par agent transform-codebook
- `surveys/validation/` — remplacé par agent validate-cleaning
- `surveys/cli/` — remplacé par script simple
- `docs/refactoring-plan.md`, `docs/v2-architecture*.md` — archivé avec le code

---

## Plan d'implémentation

### Phase 0 : Nettoyage (avant tout)
1. Créer branche `v2-archive`, y pousser le code actuel
2. Supprimer les dossiers v2 du main (`pattern_engine/`, `llm_processors/`, etc.)
3. Fermer / archiver les issues beads liées à la v2
4. Créer les nouvelles issues beads pour v3

### Phase 1 : Agents (fondation)
5. Refactorer `transform-codebook.md` → output JSON, modèles cheap
6. Refactorer `clean-variable.md` → output `vars/{var}.py`, fallback modèles
7. Refactorer `validate-cleaning.md` → valide `clean.py` assemblé

### Phase 2 : Pipeline
8. Écrire `surveys/pipeline.py` — orchestrateur ~100 lignes
9. Écrire la fonction `assemble()` — concat `vars/*.py` → `clean.py`
10. Configurer le routing modèles (`surveys/config.json`)

### Phase 3 : Tests
11. Tester `transform-codebook` sur 3 formats réels (PDF, XLSX, MD)
12. Tester `clean-variable` sur ~10 variables de types différents
13. Test end-to-end sur 1 sondage complet
14. Benchmarker GLM-5 vs Kimi vs big-pickle (qualité + vitesse)

### Phase 4 : Optionnel
15. Tester Ollama local comme modèle fallback gratuit
16. Parallélisation tuning (max_workers optimal)
17. Monitoring et rapport qualité

---

## Contraintes inchangées

- Output final = `surveys/{survey_id}/clean.py` compatible lambda AWS
- Interface `clean_data(df)` + `get_metadata()` obligatoire
- Données brutes dans `_SharedFolder_data_produit/` (pas copiées)
- Variables nettoyées: `ses_*`, `op_*`, `behav_*`, `know_*`
- Likert normalisé 0-1, missing codes → `np.nan`
