# Question: Architecture du Pattern Engine (Tier 1) pour un pipeline de nettoyage de sondages

## Contexte du projet

Pipeline de nettoyage de sondages québécois (CSV/SAV) qui génère un script Python (`clean.py`)
standardisant les variables brutes (ex: `Q2 = 1,2,3` → `ses_province = "qc","on","bc"`).

Architecture 3-tiers décidée :
- **Tier 1** (~50% vars) : pattern reconnu → règle déterministe générée automatiquement
- **Tier 2** (~40% vars) : batch LLM léger (GLM-5 gratuit)
- **Tier 3** (~10% vars) : LLM Haiku individuel (cas complexes)

## Ce qui existe déjà

- `pattern_engine/schemas/pattern_schema.py` : Pydantic `Pattern`, `DetectionCriteria`,
  `PatternLibrary` (sérialisable JSON)
- `codebook_parser/schemas/` : `VariableSchema` avec `value_labels`, `range_min/max`,
  `missing_codes`, `scale_type`
- `pattern_engine/patterns/` : répertoire vide — à implémenter
- `pattern_engine/pattern_library.json` : schema JSON défini, zéro patterns dedans

## Ce qu'on construit maintenant (2 issues)

### Issue zy4.1 : Core patterns (likert, demographics, binary, scales)

Créer `surveys/pattern_engine/patterns/` avec :
- `base_pattern.py` : classe de base
- `likert_scales.py` : Likert 3/4/5/7 pts, fréquence
- `demographics.py` : province QC, sexe, groupe d'âge, revenu, région admin QC
- `binary.py` : Oui/Non (1/2 ou 0/1), vrai/faux
- `scales.py` : thermomètre 0-10, pourcentages

### Issue zy4.2 : Pattern classifier

Créer `surveys/pattern_engine/pattern_classifier.py` qui :
- Prend les stats d'une colonne (min, max, n_unique, distribution, NaN) + optionnellement un `VariableSchema`
- Retourne : tier recommandé (1/2/3) + pattern_id candidat + confidence score

## Question 1 : Modélisation des patterns (zy4.1)

**Option A — Classes Python OOP** avec logique de détection encapsulée :
```python
class Likert5AgreePattern(BasePattern):
    pattern_id = "likert_5_agree"

    def matches(self, var: VariableSchema, series: pd.Series) -> float:
        # retourne confidence 0.0-1.0
        ...

    def generate_code(self, var_name: str, codebook_entry: VariableSchema) -> str:
        ...
```

**Option B — Instances Pydantic pures** (constantes) :
```python
LIKERT_5_AGREE = Pattern(
    pattern_id="likert_5_agree",
    detection_criteria=DetectionCriteria(unique_values=[1,2,3,4,5], n_unique=5),
    transformation_template="df['{var}'].map({mapping})"
)
```
La logique de détection vit dans le matcher (issue zy4.3 suivante).

**Option C — Hybride** : classes Python avec méthode `to_pattern() -> Pattern` pour la sérialisation JSON.

Laquelle est la plus maintenable pour une petite équipe? La logique de détection doit-elle vivre dans le pattern ou dans le matcher?

## Question 2 : Input du PatternClassifier (zy4.2)

Le classifier doit décider Tier 1/2/3. Quelles données utiliser ?

**Option A — Stats pandas seulement** (analyse de la Series CSV) :
```python
classify(series: pd.Series) -> ClassificationResult
```
Avantage : indépendant du codebook (peut tourner même si le codebook est partiel).
Risque : perd l'info sémantique du codebook (ex: `scale_type="likert"` déjà parsé).

**Option B — VariableSchema seulement** (info du codebook) :
```python
classify(var: VariableSchema) -> ClassificationResult
```
Avantage : sémantique riche, cohérent avec le pipeline.
Risque : dépend d'un codebook bien parsé — si le codebook est mauvais, le classifier se trompe.

**Option C — Les deux en entrée** :
```python
classify(series: pd.Series, var: VariableSchema | None = None) -> ClassificationResult
```
Plus robuste (peut croiser les deux sources), mais interface plus complexe.

Quelle option est la plus robuste dans la pratique pour des codebooks de qualité variable ?

## Question 3 : Gestion des codes manquants dans le tiering

Les critères Tier 1 dans l'issue sont : `n_unique ≤ 7, valeurs dans plage connue, correspond à un pattern`.

Mais en pratique, les données de sondages ont souvent des **codes manquants** (98=NSP, 99=NR, -9=Refus)
qui augmentent `n_unique`. Faut-il :

**A)** Filtrer les codes manquants **avant** de calculer `n_unique` (donc Likert 5pts + 2 codes manquants = n_unique effectif=5, pas 7)

**B)** Inclure les codes manquants dans n_unique et ajuster le seuil Tier 1 à ≤ 10

**C)** Avoir une détection explicite des codes manquants comme étape préalable au classifier, qui les extrait et les documente avant toute classification

## Ce qu'on attend

Une recommandation concrète et opiniée sur chacune des 3 questions, avec les trade-offs honnêtes.
