## Summary

Recommandation : **Option A** (classes OOP) pour modélisation, **Option C** (double input) pour classifier, **Option C** (détection explicite) pour codes manquants. Architecture orientée vers la maintenabilité d'une petite équipe avec séparation claire des responsabilités.

---

## Question 1 : Modélisation des patterns → **Option A (Classes OOP)**

**Recommandation** : Utiliser des classes Python avec méthodes `matches()` et `generate_code()` encapsulées.

**Trade-offs** :
- ✅ Logique de détection co-localisée avec le pattern (testable, lisible)
- ✅ Extensibilité naturelle (héritage pour variantes de Likert, démographie)
- ❌ Plus verbeux que des constantes Pydantic
- ❌ Sérialisation JSON nécessite méthode `to_model()` (Option C serait mieux ici)

**Pourquoi pas B** : Mettre toute la logique dans le matcher crée une classe "Dieu" difficile à maintenir. Chaque pattern a des critères de détection spécifiques (ex: Likert 5 vs fréquence) qui justifient leur encapsulation.

---

## Question 2 : Input du PatternClassifier → **Option C (double input)**

**Recommandation** : Classifier accepte `series: pd.Series` ET `var: VariableSchema | None`, avec heuristique de fallback.

**Trade-offs** :
- ✅ Robustesse : utilise VariableSchema si disponible (confiance haute), fallback sur stats pandas si absent
- ✅ Validation croisée : si codebook dit "likert" mais stats montrent n_unique=100 → downgrade automatique à Tier 2
- ❌ Interface plus complexe
- ❌ Nécessite doc claire sur priorité des sources

**Implémentation sketch** :
```python
if var and var.scale_type == "likert" and matches(series, var):
    return Tier1, "likert_5", 0.95
elif var and var.scale_type == "demographic":
    return Tier2, None, 0.7  # Demographie souvent nuancée
else:
    return Tier2, None, 0.5  # Fallback stats only
```

---

## Question 3 : Codes manquants → **Option C (détection explicite préalable)**

**Recommandation** : Ajouter une étape `detect_missing_codes()` AVANT le classifier qui extrait et documente les codes manquants dans VariableSchema.

**Trade-offs** :
- ✅ Séparation claire des responsabilités (détecter vs classifier)
- ✅ Documentation explicite dans VariableSchema (traceabilité)
- ✅ Classifier utilise toujours `n_unique_effectif` (sans codes manquants)
- ❌ Étape supplémentaire dans le pipeline
- ❌ Nécessite heuristique de détection (valeurs typiques 98/99/-9)

**Pourquoi pas A/B** : A masque la complexité dans le classifier, B est fragile (seuil arbitraire). C transforme un problème d'impédance en une étape documentée et réutilisable.

---

## Implementation sketch (priorité)

1. **Option C (Q3)** d'abord : `codebook_parser/detect_missing.py` → extrait 98/99/-9, enrichit VariableSchema
2. **Option A (Q1)** ensuite : `pattern_engine/patterns/*.py` avec classes héritant de BasePattern
3. **Option C (Q2)** enfin : `pattern_engine/pattern_classifier.py` avec heuristique de priorité VariableSchema → stats

**Règle d'or** : Si VariableSchema est de bonne qualité → privilégier. Sinon, le classifier doit être robuste aux données brutes (Tier 2/3 par défaut).
