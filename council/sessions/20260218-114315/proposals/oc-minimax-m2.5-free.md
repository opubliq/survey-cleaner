# Recommendation: Pattern Engine Architecture

## Summary

Je recommande une architecture hybride pour les patterns (Q1), un classifier acceptant les deux entrées avec fallback intelligent (Q2), et une détection explicite des codes manquants预处理 (Q3). Cette combo maximise la robustesse tout en gardant la maintenance simple pour une petite équipe.

---

## Question 1: Modélisation des Patterns

**Recommandation: Option C — Hybride**

La logique de détection vit dans le **matcher**, pas dans le pattern. Le pattern est un objet de données (Pydantic) sérialisable ; le matcher contient la logique.

```python
# pattern_engine/patterns/likert_scales.py
class Likert5AgreePattern:
    pattern_id = "likert_5_agree"
    
    @staticmethod
    def detect(series: pd.Series, var: VariableSchema | None) -> float:
        # Logique de détection centralisée ici
        if var and var.scale_type == "likert" and var.value_labels:
            unique = set(var.value_labels.keys())
            if unique == {1,2,3,4,5}:
                return 1.0
        # Fallback stats-only
        unique_vals = series.dropna().unique()
        if set(unique_vals) <= {1,2,3,4,5} and len(unique_vals) >= 3:
            return 0.8
        return 0.0
    
    @staticmethod
    def generate_code(var_name: str, var: VariableSchema) -> str:
        mapping = var.value_labels or {1:"1",2:"2",3:"3",4:"4",5:"5"}
        return f"df['{var_name}'].map({mapping})"
```

**Pourquoi:**
- Le `Pattern` Pydantic reste sérialisable pour `pattern_library.json` (export/import)
- La logique `detect()` est testable unitairement
- Ajout d'un nouveau pattern = 1 fichier, easy onboarding

**Contre de B:** Constants Pydantic seules → la détection doit vivre ailleurs, pollution du namespace
**Contre de A:** Héritage + méthodes = plus de boilerplate, harder à serializer

---

## Question 2: Input du PatternClassifier

**Recommandation: Option C avec prioritization intelligente**

```python
@dataclass
class ClassificationResult:
    tier: Literal[1, 2, 3]
    pattern_id: str | None
    confidence: float
    
def classify(series: pd.Series, var: VariableSchema | None = None) -> ClassificationResult:
    # Step 1: Si codebook disponible et fiable, l'utiliser en priorité
    if var and var.scale_type and var.value_labels:
        tier = fast_path_classify(series, var)
        if tier == 1:
            return tier1_result
            
    # Step 2: Fallback stats-only
    return stats_based_classify(series)
```

**Logique de fallback:**
- Si `var.scale_type` est présent et crédible → Tier 1 direct
- Si `var` est partial (labels mais pas type) →Tier 2
- Si pas de `var` → stats-only classifier

**Pourquoi:**
- En pratique, les codebooks sont souvent partis/mal parsés
- Le classifier doit être ** résilient**: si une source est bonne, l'utiliser ; sinon, fallback
- L'interface reste simple: `classify(series, var=None)` fonctionne seul

---

## Question 3: Codes Manquants

**Recommandation: Option C — Détection explicite en preprocessing**

Créer un `MissingValueDetector` qui:
1. Reconnaît les patterns standards (98, 99, -9, -1, NSP, NR, etc.)
2. Les-extrait de la Series AVANT classification
3. Les documente dans `var.missing_codes` pour le générateur de code

```python
# missing_value_detector.py
STANDARD_MISSING = {
    97: "NSP", 98: "NSP", 99: "NR",
    -9: "Refus", -1: "N/A",
    "NSP", "NR", "NA", "Ne sait pas"
}

def extract_missing(series: pd.Series) -> tuple[pd.Series, dict]:
    missing_mask = series.isin(STANDARD_MISSING.keys()) | series.isin(STANDARD_MISSING.values())
    clean_series = series[~missing_mask]
    missing_codes = series[missing_mask].value_counts().to_dict()
    return clean_series, missing_codes
```

**Intégration dans le classifier:**
```python
def classify(series: pd.Series, var: VariableSchema | None):
    clean_series, missing = extract_missing(series)
    n_unique = clean_series.nunique()
    
    # Maintenant n_unique reflète la vraie cardinality
    if n_unique <= 7 and matches_known_pattern(clean_series):
        return Tier1(...)
```

**Pourquoi C:**
- **A (filter before)** : Risque de faux positifs si les codes manquants ne sont pas standards
- **B (adjust threshold)** : Seuil 10 est trop permissif, perd la granularité Likert 5/7
- **C** : Traite le problème à la source, puis le classifier reste clean

---

## Implementation Sketch

1. **Créer `pattern_engine/patterns/base.py`** avec `BasePattern` ABC
2. **Implémenter les 5 patterns** (likert, demographics, binary, scales, numeric) avec méthode `detect()`
3. **Créer `pattern_engine/missing_value_detector.py`** avec les standards QC
4. **Créer `pattern_engine/pattern_classifier.py`** intégrant detector + fallback logic
5. **Loader les patterns** dans `PatternLibrary` au startup

**Fichier à créer en priorité:**
```
pattern_engine/
├── patterns/
│   ├── __init__.py
│   ├── base.py
│   ├── likert_scales.py
│   ├── demographics.py
│   ├── binary.py
│   └── scales.py
├── missing_value_detector.py
└── pattern_classifier.py
```

---

## Trade-offs Summary

| Aspect | Choix | Trade-off |
|--------|-------|-----------|
| Modélisation | Hybride (classe + to_pattern()) | Plus de code que B, mais plus testable |
| Input classifier | Both + fallback | Interface plus large, mais robuste |
| Missing values | Détection explicite | Étape supplémentaire, mais Tier 1 plus précis |
