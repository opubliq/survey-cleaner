# Guide de nettoyage manuel - elxnqc_particip_egp_2018

## Vue d'ensemble

**Sondage**: Élection québécoise - Participation ÉGP 2018
**Observations**: 2175
**Variables brutes**: 208

## Ressources disponibles

1. **VARIABLES_ANALYSIS_REPORT.txt** - Rapport complet d'analyse de toutes les variables
2. **raw/codebook.md** - Codebook extrait de l'Excel
3. **raw/data.csv** - Données brutes (encodage: latin-1, séparateur: `;`)
4. **clean.py** - Script à remplir avec le code de nettoyage

## Nomenclature des variables nettoyées

Utiliser les préfixes suivants pour standardiser les noms:

- **`id_`** - Identifiants (caseid, respondent_id, etc.)
- **`ses_`** - Variables socioéconomiques et démographiques
  - `ses_age`, `ses_gender`, `ses_education`, `ses_income`, etc.
- **`behav_`** - Comportements politiques
  - `behav_vote_turnout`, `behav_campaign_activity`, etc.
- **`op_`** - Opinions et attitudes
  - `op_party_preference`, `op_leader_rating`, etc.
- **`weight_`** - Pondérations
  - `weight_standard`, `weight_alternative`, etc.

## Variables identifiées (aperçu du rapport)

### Variables techniques/ID
- **QUESTIONNAIRE** - ID unique du questionnaire (2175 valeurs uniques) → `id_respondent`

### Variables géographiques/démographiques
- **REGIO** - Région administrative (17 catégories) → `ses_region_administrative`
- **REGIX** - Regroupement régional (3 catégories) → `ses_region_grouped`
- **ZONE** - Zone urbaine/rurale (3 catégories) → `ses_zone_type`

### Variables de comportement électoral
- **VOT1** - A voté ou non (binaire) → `behav_vote_turnout_provincial_2018`
- **Q4** - Raison de ne pas voter (4 catégories, si VOT1=2)
- **Q5** - Intention de vote future

### Variables d'opinion
- **Q2** - Opinion générale (6 catégories)
- **Q6A-Q6P** - Séries de raisons (binaires, beaucoup de NA)
- **Q7M1-Q7M8** - Variables multiples avec texte ouvert (_O suffix)
- **Q8A-Q8I** - Opinions sur différents sujets
- **Q9A-Q9C** - Autres opinions
- **Q10A-Q10D** - Évaluations
- **Q16A-Q16O** - Séries d'évaluations (15 items)
- **Q17A-Q17C** - Évaluations
- **Q23A-Q23H** - Opinions (8 items)
- **Q24A-Q24E** - Opinions (5 items)
- **Q25A-Q25I** - Opinions (9 items)
- **Q26A-Q26B** - 2 items
- **Q27A-Q27C** - 3 items

### Variables démographiques (fin du questionnaire)
- **Q28-Q39** - Variables socioéconomiques standards
- **Pondération** - Poids pour analyse

### Variables à SKIP (selon rapport)
- **Q2B** - Constante, 92.9% missing
- **Q3** - Constante (valeur unique)
- Variables ouvertes (texte libre) avec suffix `_O` - PII ou non structuré

## Patterns de code recommandés

### 1. Identifiant unique
```python
# ID respondent
df_clean['id_respondent'] = df['QUESTIONNAIRE'].copy()
```

### 2. Binaire (1/2 → 1/0 ou yes/no)
```python
df_clean['behav_vote_turnout_provincial_2018'] = df['VOT1'].map({
    1: 1.0,  # Voted
    2: 0.0   # Did not vote
})
```

### 3. Catégorielle ordinale (normaliser 0-1)
```python
df_clean['op_example'] = df['Q_EXAMPLE'].map({
    1: 1.0,    # Strongly agree
    2: 0.67,   # Agree
    3: 0.33,   # Disagree
    4: 0.0     # Strongly disagree
})
```

### 4. Catégorielle nominale (labels texte)
```python
df_clean['ses_region_administrative'] = df['REGIO'].map({
    1: 'bas_saint_laurent',
    2: 'saguenay_lac_saint_jean',
    3: 'capitale_nationale',
    # ... (consulter codebook pour les 17 régions)
})
```

### 5. Pondération (copie directe)
```python
df_clean['weight_standard'] = df['Pondération'].copy()
```

## Workflow de nettoyage

1. **Consulter VARIABLES_ANALYSIS_REPORT.txt** pour voir la distribution de chaque variable
2. **Consulter raw/codebook.md** pour les labels et descriptions
3. **Ajouter le code dans clean.py** section par section
4. **Tester régulièrement** avec `python surveys/elxnqc_particip_egp_2018/clean.py`
5. **Vérifier les outputs** dans `processed/data_cleaned.csv` et `processed/codebook.json`

## Groupes suggérés pour le nettoyage

### Groupe 1: ID et géographie
- QUESTIONNAIRE → id_respondent
- REGIO → ses_region_administrative
- REGIX → ses_region_grouped
- ZONE → ses_zone_type

### Groupe 2: Comportement électoral principal
- VOT1 → behav_vote_turnout_provincial_2018
- Q4 → behav_vote_abstention_reason
- Q5 → behav_vote_intention_future

### Groupe 3: Variables d'opinion (ordinal scales)
- Q8A-Q8I
- Q9A-Q9C
- Q16A-Q16O
- Q17A-Q17C
- Q23A-Q23H
- Q24A-Q24E
- Q25A-Q25I
- Q26A-Q26B
- Q27A-Q27C

### Groupe 4: Démographiques (Q28-Q39)
- Q28 → ses_gender
- Q29 → ses_language_home
- Q30 → ses_education
- Q31 → ses_occupation
- Q32 → ses_income
- etc.

### Groupe 5: Pondération
- Pondération → weight_standard

## Notes importantes

- **Encodage**: Fichier en `latin-1` avec séparateur `;`
- **Valeurs manquantes**: Beaucoup de variables conditionnelles (ex: Q6A-Q6P seulement si VOT1=2)
- **Valeurs 9, 98, 99**: Souvent "Ne sais pas" ou "Refus" → mapper à `np.nan`
- **Variables ouvertes**: Suffix `_O` contient texte libre → SKIP ou conserver tel quel
- **Variables multi-mention**: Séries `_M1`, `_M2`, etc. → binaires pour chaque mention

## Statut du nettoyage

- [ ] Groupe 1: ID et géographie
- [ ] Groupe 2: Comportement électoral
- [ ] Groupe 3: Opinions ordinales
- [ ] Groupe 4: Démographiques
- [ ] Groupe 5: Pondération
- [ ] Test final et validation

---

**Prêt à commencer le nettoyage manuel !**

Consulte `VARIABLES_ANALYSIS_REPORT.txt` pour les distributions complètes.
