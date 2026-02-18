**Summary**

Option C (hybride) pour la modélisation des patterns - sérialisation JSON pour l'interopérabilité, classes Python pour la logique métier. Option C (les deux entrées) pour le classifier - robustesse prime sur la simplicité. Option C (détection explicite des codes manquants) - évite les erreurs de classification et documente les conventions du sondage.

---

## Question 1 : Modélisation des patterns

**Recommandation : Option C — Hybride**

Les patterns comme classes Python avec méthode `to_pattern()`. La logique de détection vit **dans le pattern**, pas dans le matcher.

```python
# pattern_engine/patterns/base_pattern.py
from abc import ABC, abstractmethod
from typing import Optional
import pandas as pd

class BasePattern(ABC):
    pattern_id: str
    description: str
    
    @abstractmethod
    def matches(self, series: pd.Series, var_schema: Optional[VariableSchema] = None) -> float:
        """Retourne confidence score 0.0-1.0"""
        pass
    
    @abstractmethod
    def to_pattern(self) -> Pattern:
        """Sérialise vers Pydantic Pattern pour JSON"""
        pass
```

Pourquoi dans le pattern ? Parce que chaque pattern a sa propre heuristique (Likert vérifie la distribution, binaire vérifie exactement 2 valeurs, etc.). Un matcher générique deviendrait un switch-case ingérable.

```python
# pattern_engine/patterns/likert_scales.py
class Likert5AgreePattern(BasePattern):
    pattern_id = "likert_5_agree"
    description = "Likert 5 points: Fortement en désaccord (1) à Fortement d'accord (5)"
    expected_values = {1, 2, 3, 4, 5}
    
    def matches(self, series, var_schema=None) -> float:
        unique_vals = set(series.dropna().unique())
        
        # Bonus si codebook confirme
        codebook_bonus = 0.1 if var_schema and var_schema.scale_type == "likert" else 0.0
        
        if unique_vals == self.expected_values:
            return 0.9 + codebook_bonus
        elif unique_vals.issubset(self.expected_values):
            return 0.6 + codebook_bonus
        return 0.0
    
    def to_pattern(self) -> Pattern:
        return Pattern(
            pattern_id=self.pattern_id,
            detection_criteria=DetectionCriteria(
                unique_values=list(self.expected_values),
                n_unique=5
            ),
            transformation_template="df['{var}'].map({1:'Fortement en désaccord', ...})"
        )
```

**Trade-offs :**
- ✅ Logique co-localisée avec le pattern (SRP)
- ✅ Testable unitairement (mock pd.Series)
- ✅ Sérialisable pour audit/debug
- ❌ Double maintenance (classe + to_pattern)
- ❌ Risque de divergence classe ↔ JSON

**Mitigation :** Générer automatiquement `pattern_library.json` via un script qui appelle `to_pattern()` sur toutes les instances.

---

## Question 2 : Input du PatternClassifier

**Recommandation : Option C — Les deux en entrée**

Avec ordre de priorité : `series` (vérité terrain) > `var_schema` (métadonnées).

```python
# pattern_engine/pattern_classifier.py
from dataclasses import dataclass
from typing import Optional
import pandas as pd

@dataclass
class ClassificationResult:
    tier: int  # 1, 2, ou 3
    pattern_id: Optional[str]
    confidence: float
    reasoning: str  # Pour le debugging

class PatternClassifier:
    def __init__(self, patterns: list[BasePattern]):
        self.patterns = patterns
    
    def classify(
        self, 
        series: pd.Series, 
        var_schema: Optional[VariableSchema] = None
    ) -> ClassificationResult:
        # Tier 1: Essayer tous les patterns
        matches = []
        for pattern in self.patterns:
            confidence = pattern.matches(series, var_schema)
            if confidence > 0.5:
                matches.append((pattern.pattern_id, confidence))
        
        if matches:
            best = max(matches, key=lambda x: x[1])
            if best[1] > 0.8:
                return ClassificationResult(
                    tier=1, 
                    pattern_id=best[0], 
                    confidence=best[1],
                    reasoning=f"Pattern reconnu: {best[0]}"
                )
        
        # Tier 2/3: Heuristiques sur la complexité
        n_unique = series.nunique(dropna=True)
        if n_unique <= 20:
            return ClassificationResult(
                tier=2, 
                pattern_id=None, 
                confidence=0.7,
                reasoning=f"Batch GLM-5: {n_unique} valeurs uniques"
            )
        
        return ClassificationResult(
            tier=3, 
            pattern_id=None, 
            confidence=0.5,
            reasoning="Cas complexe: Haiku individuel"
        )
```

**Trade-offs :**
- ✅ Robuste aux codebooks incomplets (séries seules suffisent)
- ✅ Exploite la sémantique quand disponible (meilleure précision)
- ✅ Peut détecter incohérences (codebook dit "likert" mais données = texte → alerte)
- ❌ Interface plus complexe (deux paramètres)
- ❌ Nécessite gestion des cas `var_schema=None`

**Dans la pratique :** Les codebooks de sondages québécois sont souvent des PDFs parsés imparfaitement. Option C permet de "dégrader élégamment" vers l'analyse des données brutes quand le codebook est boiteux.

---

## Question 3 : Gestion des codes manquants

**Recommandation : Option C — Détection explicite préalable**

Créer un `MissingCodeDetector` qui s'exécute **avant** le classifier.

```python
# pattern_engine/missing_code_detector.py
import pandas as pd
from typing import Set, Dict

class MissingCodeDetector:
    """Détecte et standardise les codes manquants avant classification."""
    
    COMMON_MISSING_CODES = {98, 99, -9, -99, 999, "NSP", "NR", "Refus", " ", ""}
    
    def detect(self, series: pd.Series) -> Dict:
        unique_vals = set(series.dropna().unique())
        missing_codes = unique_vals & self.COMMON_MISSING_CODES
        
        # Heuristique: codes > 90 ou < 0 souvent des missing
        numeric_vals = {v for v in unique_vals if isinstance(v, (int, float))}
        heuristic_missing = {v for v in numeric_vals if v > 90 or v < 0}
        
        all_missing = missing_codes | heuristic_missing
        
        return {
            "missing_codes": list(all_missing),
            "effective_unique": len(unique_vals - all_missing),
            "cleaned_series": series.replace(list(all_missing), pd.NA)
        }
```

**Pourquoi pas A ?** Filtrer silencieusement masque les conventions du sondage (est-ce que 98=NSP ou 98=une vraie réponse ?).

**Pourquoi pas B ?** Augmenter le seuil à 10 cache le problème sans le résoudre.

**Avec C :**

```python
# Dans pattern_classifier.py
def classify(self, series: pd.Series, var_schema=None) -> ClassificationResult:
    # Étape 1: Détecter codes manquants
    detection = self.missing_detector.detect(series)
    clean_series = detection["cleaned_series"]
    n_unique_effective = detection["effective_unique"]
    
    # Étape 2: Classifier sur données nettoyées
    # ... logique avec n_unique_effective ...
    
    # Étape 3: Documenter dans le résultat
    return ClassificationResult(
        tier=1,
        pattern_id="likert_5_agree",
        confidence=0.95,
        missing_codes_detected=detection["missing_codes"],  # Pour le rapport
        reasoning=f"Likert 5pts + codes manquants: {detection['missing_codes']}"
    )
```

**Trade-offs :**
- ✅ Transparent (on sait quels codes sont considérés manquants)
- ✅ Réutilisable (même détecteur pour tout le pipeline)
- ✅ Documente les conventions du sondage (98 vs 99 vs -9)
- ❌ Étape supplémentaire
- ❌ Faux positifs possibles (si 98 est une vraie valeur)

**Mitigation :** Logger un warning si un "code manquant" détecté apparaît >5% des réponses (probablement pas un vrai missing).

---

## Implementation sketch (Prochaines étapes)

1. **Créer l'infrastructure (30 min)**
   ```bash
   mkdir -p surveys/pattern_engine/patterns
   touch surveys/pattern_engine/__init__.py
   touch surveys/pattern_engine/patterns/__init__.py
   touch surveys/pattern_engine/patterns/base_pattern.py
   ```

2. **Implémenter base_pattern.py et missing_code_detector.py**

3. **Créer 3 patterns MVP** (likert_5, binary_yn, province_qc) pour valider l'architecture

4. **Implémenter PatternClassifier avec les 3 tiers**

5. **Générer pattern_library.json** via script d'introspection

6. **Tests :** `pytest tests/test_pattern_engine/`

La clé : commencer petit avec 3-4 patterns, valider que le tiering fonctionne sur un vrai sondage, puis étendre.
