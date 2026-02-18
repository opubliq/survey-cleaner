Je vais d'abord explorer le codebase existant pour comprendre l'architecture actuelle avant de formuler ma recommandation.
## Summary

Je recommande une approche **hybride batch + modè1e gratuit** : traiter toutes les variables en un seul appel API avec un modèle gratuit (GLM-5), plutôt que 1 appel/variable avec Claude Sonnet. Cela réduit le coût de ~$38 à ~$0.50-2$/survey.

## Recommendation

### Architecture recommandée: Batch Hybrid avec Modèle Gratuit

```
┌─────────────────────────────────────────────────────────┐
│  Survey Cleaner Pipeline (nouveau orchestrateur)        │
├─────────────────────────────────────────────────────────┤
│  1. parse_codebook.py    → codebook.json (one-time)    │
│  2. batch_clean.py       → GLM-5 (gratuit) pour ~80   │
│                           variables en 1 appel         │
│  3. human_validate.py    → review interactif            │
│  4. retry_failing.py     → 2e passe si needed          │
└─────────────────────────────────────────────────────────┘
```

### Pourquoi cette approche?

**Le problème fondamental** de l'approche actuelle:
- 186,900 tokens pour 1 variable = 2200 tokens/variable en overhead seul
- Claude Sonnet = $3-15/M tokens input
- 84 variables × (overhead 2200 + data ~500) = trop cher

**La solution**: 
1. **Un seul appel API** pour 80 variables au lieu de 80 appels
2. **Modèle gratuit** (GLM-5 ou Kimi K2.5) via LiteLLM
3. **Codebook structuré** (JSON) plutôt que Markdown à chaque fois

### Modèle recommandé

| Modèle | Cout | Capacité | Verdict |
|--------|------|----------|---------|
| **GLM-5 (free)** | $0 | Bon | ✅ Recommandé - tester d'abord |
| Kimi K2.5 (free) | $0 | Bon | ✅ Alternative |
| Claude Sonnet | $3-15/M | Excellent | ⚠️ Fallback seulement |

**Pourquoi GLM-5?**
- Gratuit via LiteLLM (`glm-5-flash`)
- Context window 1M tokens = assez pour 80 variables + codebook
- Suffisant pour du cleaning structuré (patterns reconnaissables)

### Granularité d'appel

| Option | Tokens | Coût | Qualité |
|--------|--------|------|---------|
| 1/variable (actuel) | ~2,500/v | $7.50/v | Haute |
| **Batch 80** | ~50,000 total | ~$0.50 | OK |
| Batch 20 × 4 | ~25,000/batch | ~$0.30/batch | OK |

**Recommandé**: Batch complet (80 variables) = 1 appel. Si ça échoue → retry sur batch de 20.

### Gestion du codebook

```python
# Schema codebook.json
{
  "variables": {
    "Q2_province": {
      "label": "Province de résidence",
      "values": {"1": "Québec", "2": "Ontario", "3": "BC"},
      "missing": [98, 99]
    }
  }
}
```

**Avantages**:
- Parsed une fois, réutilisé pour toutes les variables
- Plus besoin de grep ~30 lignes par variable
- 80× moins de tokens devoted au codebook

### Prompt pour le batch (exemple)

```
Tu es un expert en nettoyage de données de sondages.

Tu as:
- Un dataset CSV avec 84 variables
- Un codebook.json avec les définitions

Génère un script Python clean.py qui:
1. Charge les données
2. Pour chaque variable, crée une version standardisée
3. Retourne df_clean

Règles:
- Variables ses_* pour démographiques
- Variables op_* pour opinions
- Variables behav_* pour comportements
- Likert → normaliser 0-1
- Catégorielles → strings simples ("quebec", "liberal")
- Codes manquants (98,99,-9) → NaN

Sortie: Code Python complet dans un bloc ```python
```

## Trade-offs

### Avantages
- **Cost**: $0.50-2/survey vs $38 (95% réduction)
- **Speed**: 1 appel API vs 80 appels
- **Simplicité**: Un seul script, pas d'orchestration complexe

### Inconvénients
- **Qualité**: GLM-5 < Claude pour les cas edge
- **Retry**: Si le batch échoue, il faut retry sur sous-batches
- **Validation**: Plus difficile de valider 80 transformations d'un coup
- **Debug**: Une erreur dans le batch = toute la variable list à retry

### Mitigations
1. **Fallback gracieux**: Si GLM-5 échoue → Claude Sonnet en batch
2. **Validation humaine**: Review interactive des transformations
3. **Pattern library**: Stocker les transformations réussies pour reuse

## Implementation sketch

```python
# Step 1: parse_codebook.py (run once per survey)
import json
# Convert PDF/TXT codebook → codebook.json
# Use GLM-4 ou Claude avec 1 call

# Step 2: batch_clean.py (le cœur)
import litellm

response = litellm.completion(
    model="glm-5-flash",  # gratuit
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Dataset: {df_summary}\nCodebook: {json.dumps(codebook)}"}
    ],
    max_tokens=32000
)

# Parse et génère clean.py
clean_code = extract_python_block(response)

# Step 3: Validation humaine
# Afficher les 80 transformations, user accepte/skip/retry

# Step 4: Si needed, retry individuelles
```

### Estimation de coût réelle

| Étape | Model | Tokens | Coût |
|-------|-------|--------|------|
| Parse codebook | GLM-5 | 5,000 | $0 |
| Batch clean | GLM-5 | 50,000 | $0 |
| Retry (si besoin) | GLM-5 | 20,000 | $0 |
| **Total** | | **75,000** | **~$0.50** |

### Prochaines étapes concrètes

1. **Tester GLM-5** sur 1 survey complet: `python orchestrator.py survey_id --model glm-5-flash`
2. **Implementer batch**: Créer `batch_clean.py` qui envoie toutes variables + codebook.json
3. **Ajouter fallback**: Si GLM-5 fail → Claude Sonnet en mode batch
4. **Valider**: Afficher les transformations à l'utilisateur avant acceptation

## Conclusion

**Va directement avec l'approche C (hybride) + modèle gratuit**. Laisse tomber le per-variable avec Claude - c'est architecturalement trop coûteux. Le modèle gratuit (GLM-5) est largement suffisant pour du cleaning de surveys avec patterns reconnaissables.

Le point clé: **1 appel API pour tout le survey, pas 80**.
