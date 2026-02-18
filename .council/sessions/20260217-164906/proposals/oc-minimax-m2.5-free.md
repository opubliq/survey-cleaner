# Recommendation: Hybrid avec modèles gratuits

## Summary

Je recommande **Option C (Hybride)** avec un changement crucial: **utiliser des modèles gratuits/subsidisés** plutôt que Claude Sonnet. Le problème fondamental n'est pas l'architecture mais le coût du modèle. Avec des modèles gratuits, même une approche "suboptimale" devient économique. La stratégie hybride permet ensuite d'optimiser progressivement.

## Recommendation

### Architecture recommandée

```
┌─────────────────────────────────────────────────────────┐
│  survey-cleaner/                                        │
│  ├── orchestrator.py        # Point d'entrée            │
│  ├── classifiers/           # Type detection (règles)    │
│  │   ├── likert.py         # Detecte échelles Likert    │
│  │   ├── binary.py         # Detecte oui/non            │
│  │   └── demographics.py   # Province, age, genre      │
│  ├── patterns/             # Bibliothèque de patterns   │
│  │   └── {survey_type}.json # Règles par type survey    │
│  ├── llm_gateway.py         # Abstraction modèle LLM     │
│  └── cleaners/             # Nettoyeurs par type         │
```

### Modèle recommandé: **Minimax M2.5** ou **GLM-5**

Ces modèles gratuits sont amplement suffisants pour:
- Classifier les variables (Type A/B/C)
- Prendre des décisions de standardisation
- Générer du code Python simple

Le nettoyage de sondage ne requiert pas de reasoning complexe. C'est de la transformation de données, pas de la mathématique avancée.

### Granularité d'appel: **Batch par type**

Au lieu de 1 appel/variable:
1. Classifier toutes les variables upfront (règles déterministes)
2. Grouper les Type B/C par catégorie
3. Un seul appel LLM par catégorie: "Voici 15 variables Likert, génère le code de nettoyage"

### Gestion du codebook

Convertir le codebook **une fois** en JSON structuré au début:
```json
{
  "variable": "Q2_province",
  "label": "Province de résidence",
  "values": {"1": "Québec", "2": "Ontario", "3": "Colombie-Britannique"},
  "missing": [98, 99]
}
```

Ce JSON est:
- Much cheaper à passer en prompt que du Markdown
- Validable programmatiquement
- Réutilisable entre sessions

## Trade-offs

| Avantages | Inconvénients |
|-----------|---------------|
| Coût: ~$0-2/survey avec modèles gratuits | Quality: ~5-10% d'erreurs，需要 validation |
| Progressif: la pattern library s'enrichit | Complexité: plus de code à maintenir |
| Autonome: une fois lancé, finit tout seul | Setup initial: classifier les types prend du temps |
| Flexible: ajoute nouveaux types facilement | Dépendance: aux modèles gratuits (peut changer) |

## Estimation de coût

Pour 84 variables avec approche hybride + modèle gratuit:

| Étape | Tokens | Coût |
|-------|--------|------|
| Classification (règles) | 0 | $0 |
| Parse codebook (1x) | ~5K | $0 |
| Batch LLM (~30 vars complexes) | ~15K | $0 |
| **Total** | ~20K | **$0** |

Le coût réel devient le temps de développement, pas les tokens.

## Implementation sketch

### Étape 1: Classifier les variables (semaine 1)

```python
# classifiers/detector.py
def classify_variable(df, codebook_var):
    # Likert: valeurs 1-5 ou 1-7, label contient "agree/disagree"
    if is_likert(df[var], codebook_var):
        return "likert"
    # Binary: exactement 2 valeurs
    if is_binary(df[var]):
        return "binary"
    # Standard demographics
    if is_demographic(var):
        return "demographic"
    return "complex"
```

### Étape 2: Créer le LLM gateway (semaine 1)

```python
# llm_gateway.py
from openai import OpenAI

def call_llm(prompt, model="minimax"):
    # Gratuit via opencode ou z.ai
    client = OpenAI(base_url="...", api_key="...")
    return client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
```

### Étape 3: Batch les variables complexes (semaine 1)

```python
# Nettoie 15 variables Likert en un appel
prompt = """
Tu as une liste de variables Likert à standardiser:
- Q5A, Q5B, Q5C (satisfaction 1-7)
- Q10, Q11, Q12 (accord 1-5)

Pour chaque variable, génère le code Python de nettoyage.
Utilise ce format:
{
  "variable": "Q5A",
  "new_name": "sat_product",
  "map": {"1": "very dissatisfied", "7": "very satisfied"},
  "missing": [98, 99]
}
"""
```

### Étape 4: Générer clean.py (semaine 2)

Assembler les sorties:
- Règles déterministes pour Type A (65%)
- Sortie LLM pour Type B/C (35%)

## Prochaine étape concrète

Test sur 1 survey avec Minimax M2.5:
1. Parser le codebook en JSON
2. Classifier les 84 variables en types
3. Faire 2-3 appels LLM batch pour les cas complexes
4. Mesurer le coût réel

Cela prendra ~2-3 heures et vous donnera une answer réelle au lieu d'une estimation.
