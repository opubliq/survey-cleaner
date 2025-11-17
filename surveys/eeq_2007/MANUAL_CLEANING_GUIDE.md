# Guide de nettoyage manuel - eeq_2007

**Sondage**: Quebec Election Study 2007 / Enquête électorale québécoise 2007
**Dataset**: 2175 observations × 93 variables
**Source**: Élection générale provinciale du Québec 2007

## Structure des fichiers

```
surveys/eeq_2007/
├── raw/
│   ├── data.csv              ← Données brutes (2175 lignes, 93 vars)
│   ├── Quebec Election Study 2007 (SPSS).sav  ← Original SPSS
│   └── Quebec Election Study 2007 FR.doc      ← Codebook original
├── processed/                ← Vide, à remplir après nettoyage
├── clean.py                  ← Script de nettoyage (TOI!)
├── analyze_all_variables.py  ← Script d'analyse
├── VARIABLES_ANALYSIS_REPORT.txt  ← Généré par analyze_all_variables.py
└── MANUAL_CLEANING_GUIDE.md  ← Ce fichier
```

## Workflow de nettoyage manuel

### 1. Analyser les variables

**IMPORTANT**: Commencer par exécuter le script d'analyse pour obtenir le rapport complet

```bash
# Activer venv
source venv/bin/activate

# Exécuter l'analyse
python surveys/eeq_2007/analyze_all_variables.py
```

Cela génère `VARIABLES_ANALYSIS_REPORT.txt` avec pour chaque variable:
- Type détecté (binaire, catégorielle, continue, texte)
- Distribution des valeurs
- Valeurs manquantes (%)
- Suggestions de transformation

### 2. Éditer `clean.py`

Ouvre `surveys/eeq_2007/clean.py` et ajoute ton code dans la fonction `clean_data(df)` autour de la ligne 113 (après le TODO).

**Workflow recommandé**:
1. Consulter `VARIABLES_ANALYSIS_REPORT.txt` pour voir les suggestions
2. Consulter le codebook (`raw/Quebec Election Study 2007 FR.doc`) pour la signification
3. Écrire le code de mapping dans `clean.py`
4. Tester périodiquement avec `python surveys/eeq_2007/clean.py`

### 3. Nomenclature (règles importantes)

Consulte `surveys/cleaning_rules.json` pour les règles complètes. Résumé:

**Préfixes de variables:**
- `id_` : Identifiants (caseid, respondent_id)
- `ses_` : Socio-économiques (age, gender, education, income, province, region)
- `op_` : Opinions et attitudes
- `behav_` : Comportements (vote, participation)
- `tech_` : Techniques (weights, filters)
- `weight_` : Pondérations

**Valeurs catégorielles:**
- Simples et concises (PAS de répétition du nom de variable)
- Exemples:
  - `ses_gender`: "male", "female", "other" (PAS "gender_male")
  - `ses_province`: "quebec", "ontario" (PAS "province_quebec")
  - `behav_vote_choice`: "plq", "pq", "adq", "qs" (abréviations OK)

**Valeurs ordinales:**
- Normaliser à [0, 1] avec .map()
- Exemple: Likert 1-4 → {1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0}

**Variables continues (age, income):**
- Créer DEUX variables:
  - Continuous: `ses_age` (numeric)
  - Categorical: `ses_age_category` (character avec bins)

### 4. Patterns de code sécurisés

**Catégorielle (TOUJOURS utiliser .map()):**
```python
df_clean['ses_gender'] = df['sexe'].map({
    1.0: 'male',
    2.0: 'female'
    # Unmapped → NaN automatiquement
})
```

**Ordinale normalisée:**
```python
df_clean['op_satisfaction_democracy'] = df['q9'].map({
    1.0: 1.0,    # Très satisfait
    2.0: 0.67,   # Plutôt satisfait
    3.0: 0.33,   # Plutôt insatisfait
    4.0: 0.0,    # Très insatisfait
    9.0: np.nan  # Ne sait pas
})
```

**Continue avec bins:**
```python
# Continuous
df_clean['ses_age'] = df['age'].copy()
df_clean.loc[df['age'] < 0, 'ses_age'] = np.nan

# Categorical
df_clean['ses_age_category'] = pd.cut(
    df['age'],
    bins=[0, 25, 35, 45, 55, 65, 150],
    labels=['18_24', '25_34', '35_44', '45_54', '55_64', '65_plus']
).astype(str)
df_clean.loc[df_clean['ses_age_category'] == 'nan', 'ses_age_category'] = np.nan
```

**Choix de parti (Quebec Election Study):**
```python
df_clean['behav_vote_choice_provincial'] = df['q_vote'].map({
    1.0: 'plq',    # Parti libéral du Québec
    2.0: 'pq',     # Parti Québécois
    3.0: 'adq',    # Action démocratique du Québec
    4.0: 'qs',     # Québec solidaire
    5.0: 'pvq',    # Parti vert du Québec
    6.0: 'other',
    9.0: np.nan    # Ne sait pas / Refus
})
```

### 5. Tester le script

```bash
# Activer venv
source venv/bin/activate

# Exécuter le script
python surveys/eeq_2007/clean.py
```

Si succès, tu obtiendras:
- `processed/data_cleaned.csv`
- `processed/codebook.json`

### 6. Variables typiques à nettoyer (93 total)

**Note**: Consulter le codebook FR et le rapport d'analyse pour les détails exacts.

#### Identifiants et techniques
- ID respondent → `id_respondent`
- Poids / pondérations → `weight_*`

#### Démographiques (ses_)
- Âge → `ses_age` + `ses_age_category`
- Sexe → `ses_gender`
- Langue maternelle → `ses_language_mother`
- Langue à la maison → `ses_language_home`
- Lieu de naissance → `ses_born_canada`
- Scolarité → `ses_education`
- Occupation → `ses_occupation`
- Revenu → `ses_income_household` + `ses_income_household_category`
- Province → `ses_province` (si applicable)
- Région (Québec) → `ses_region_administrative`

#### Comportements électoraux (behav_)
- Participation électorale 2007 → `behav_vote_turnout_2007`
- Choix de vote provincial → `behav_vote_choice_provincial`
- Choix de vote fédéral → `behav_vote_choice_federal` (si applicable)
- Moment de décision → `behav_vote_decision_timing`
- Certitude du vote → `behav_vote_certainty`
- Participation campagne → `behav_campaign_participation`
- Fréquence de vote → `behav_vote_frequency_history`

#### Opinions et attitudes (op_)
- Satisfaction démocratie → `op_satisfaction_democracy`
- Intérêt politique → `op_interest_politics`
- Efficacité politique → `op_political_efficacy`
- Confiance institutions → `op_trust_*`
- Proximité partisane → `op_party_identification`
- Force de l'identification → `op_party_identification_strength`
- Évaluations de chefs → `op_leader_rating_*` (thermomètres 0-100 → normaliser à 0-1)
- Évaluations de partis → `op_party_rating_*`
- Positions sur enjeux → `op_issue_*`
- Souveraineté/fédéralisme → `op_sovereignty_*`

#### Variables à potentiellement EXCLURE
- Codes postaux (PII)
- Identifiants géographiques trop granulaires
- Réponses ouvertes (texte libre)
- Variables techniques de quotas

## Références

- **Codebook complet**: `raw/Quebec Election Study 2007 FR.doc`
- **Règles de nettoyage**: `../../cleaning_rules.json`
- **Template de référence**: `../../_template/clean.py`
- **Rapport d'analyse**: `VARIABLES_ANALYSIS_REPORT.txt` (généré)

## Contexte - Élection 2007

**Date**: 26 mars 2007
**Partis principaux**:
- PLQ (Parti libéral du Québec) - Jean Charest (élu)
- PQ (Parti Québécois) - André Boisclair
- ADQ (Action démocratique du Québec) - Mario Dumont

**Enjeux**: Identité québécoise, accommodements raisonnables, économie

## Prochaines étapes après nettoyage

1. Valider les outputs (`processed/data_cleaned.csv`)
2. Vérifier le codebook généré (`processed/codebook.json`)
3. Créer un commit git avec tes changements
4. Intégrer dans le pipeline AWS si nécessaire

---

**Bon nettoyage! 🧹**
