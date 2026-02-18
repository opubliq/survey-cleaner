# Recommendation: Pattern Engine Architecture

## Summary

Je recommande une architecture **hybride (Option C)** pour les patterns avec logique de détection intégrée, un classifier acceptant **les deux entrées (Option C)** pour robustesse, et une **détection explicite des codes manquants (Option C)** comme étape de preprocessing. Cette combinaison offre la meilleure maintenabilité pour une petite équipe tout en étant robuste aux codebooks de qualité variable.

---

## Question 1 : Modélisation des Patterns

### Recommandation : **Option C — Hybride**

Les classes Python avec méthode `to_pattern()` pour la sérialisation.

```python
# pattern_engine/patterns/likert_scales.py
class Likert5AgreePattern(BasePattern):
    pattern_id = "likert_5_agree"
    
    def matches(self, var: VariableSchema | None, series: pd.Series) -> float:
        # Logique de détection encapsulée ici
        ...
    
    def to_pattern(self) -> Pattern:
        return Pattern(
            pattern_id=self.pattern_id,
            detection_criteria=...,  # metadata pour debug/UI
            transformation_template=...
        )
```

**La détection vit dans le pattern lui-même**, pas dans un matcher séparé.

### Trade-offs

| Aspect | Option A (OOP) | Option B (Pydantic) | Option C (Hybride) |
|--------|---------------|---------------------|-------------------|
| Testabilité | ★★★★★ | ★★☆☆☆ | ★★★★★ |
| Sérialisation JSON | ★★☆☆☆ | ★★★★★ | ★★★★☆ |
| Complexité ajout pattern | Faible | Faible | Faible |
| Détection complexe | ★★★★★ | ★☆☆☆☆ | ★★★★★ |

### Pourquoi Option C pour petite équipe :
- Les patterns Likert/démographiques ont des cas edge subtils (ex: "1=Très satisfait" vs "1=Pas du tout satisfait")
- Chaque pattern peut avoir sa propre logique de détection sans polluer un matcher générique
- `to_pattern()` permet la sérialisation quand même
- Plus facile à débugger en inspectant `pattern.matches()` directement

---

## Question 2 : Input du PatternClassifier

### Recommandation : **Option C — Les deux (series + var optionnel)**

```python
@dataclass
class ClassificationResult:
    tier: Literal[1, 2, 3]
    pattern_id: str | None
    confidence: float
    reasoning: str

def classify(series: pd.Series, var: VariableSchema | None = None) -> ClassificationResult:
    # 1. Détection missing codes d'abord (voir Q3)
    effective_stats = compute_effective_stats(series)
    
    # 2. Si var fourni, valider contre stats
    if var:
        if var.scale_type == "likert" and not looks_like_likert(effective_stats):
            return tier_2_or_3(var, effective_stats, reason="scale_type mismatch")
    
    # 3. Appliquer règles Tier 1
    if looks_like_known_pattern(effective_stats, var):
        return tier_1_result(...)
    
    return tier_2_default(...)
```

### Pourquoi les deux :

1. **Défensif** : Si le codebook dit "likert" mais les stats montrent 500 valeurs uniques → flag pour review
2. **Fonctionne sans codebook** : Peut classifier même si le PDF est mal parsé
3. **Sémantique+statistique** : Croiser les deux sources est plus robuste

### Trade-offs

- Option A (stats only) : Bon fallback, mais perd `scale_type`, `value_labels`
- Option B (var only) : Dépend du parser — si le codebook est un PDF malformaté, le classifier reçoit n'importe quoi
- **Option C** : Le parser échoue → on utilise stats seulement. Le codebook est bon → on valide. Robustesse maximale.

---

## Question 3 : Codes Manquants

### Recommandance : **Option C — Étape explicite de preprocessing**

```python
# pattern_engine/preprocessing/detect_missing_codes.py
@dataclass
class MissingCodeInfo:
    codes: set[int | float]
    meanings: dict[int, str]  # {98: "NSP", 99: "NR", -9: "Refus"}
    has_legitimate_range: bool

def detect_missing_codes(series: pd.Series, var: VariableSchema | None = None) -> MissingCodeInfo:
    # 1. Si var a missing_codes définis → les utiliser
    if var?.missing_codes:
        return MissingCodeInfo(codes=var.missing_codes, ...)
    
    # 2. Sinon, heuristiques classiques
    standard_missing = {97, 98, 99, -7, -8, -9, 996, 997, 998, 999}
    found = set(series.dropna().unique()) & standard_missing
    return MissingCodeInfo(codes=found, ...)
```

### Intégration dans le classifier :

```python
def classify(series: pd.Series, var: VariableSchema | None = None):
    missing = detect_missing_codes(series, var)
    effective_series = series[~series.isin(missing.codes)]
    effective_stats = compute_stats(effective_series)  # n_unique, min, max, etc.
    
    # Maintenant effective_stats est propre pour la détection Tier 1
    if effective_stats.n_unique <= 7 and matches_known_pattern(effective_stats, var):
        return tier_1(..., missing_codes=missing)
```

### Pourquoi Option C :

- **A (filter)** : Simple mais perd l'info des codes manquants — important pour `clean.py` qui doit les Documenter
- **B (ajuster seuil)** : Fragile — un questionnaire avec 8 questions Likert et 2 NSP passe en Tier 2 artificiellement
- **C** : Les codes manquants sont **conservés et documentés** — critical pour la qualité du nettoyage et pour que `clean.py` génère du code qui gère lesNA correctement

---

## Implementation Sketch

### Priorité 1 : Préprocessing codes manquants
```python
# surveys/pattern_engine/preprocessing/missing_detector.py
def detect_and_classify_missing_codes(series, var_schema) -> tuple[pd.Series, MissingCodeInfo]
```
Sortie : series "effective" + metadata sur ce qui a été filtré.

### Priorité 2 : Pattern base + 2-3 patterns core
```python
# surveys/pattern_engine/patterns/base.py
class BasePattern(ABC):
    pattern_id: str
    @abstractmethod
    def matches(self, stats, var) -> float: ...
    def to_pattern(self) -> Pattern: ...

# surveys/pattern_engine/patterns/demographics.py  
class ProvinceQCPattern(BasePattern):
    pattern_id = "province_qc"
    def matches(self, stats, var) -> float:
        # valeurs typiques QC: ["QC", "Québec", 24] etc.
```

### Priorité 3 : Classifier
```python
# surveys/pattern_engine/pattern_classifier.py
def classify(series: pd.Series, var: VariableSchema | None = None) -> ClassificationResult:
    # 1. Missing detection
    # 2. Effective stats
    # 3. Règles Tier 1 → fallback Tier 2/3
```

### Note finale
La logique de détection vit **dans le pattern** (`matches()`), pas dans le classifier. Le classifier est juste un router qui decide Tier et appelle le bon pattern. Cela sépare les responsabilités proprement.
