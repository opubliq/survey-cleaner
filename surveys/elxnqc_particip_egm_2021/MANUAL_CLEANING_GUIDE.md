# Guide de nettoyage manuel - elxnqc_particip_egm_2021

**Sondage**: Participation aux élections générales municipales 2021
**Dataset**: 3222 observations × 84 variables
**Source**: Directeur général des élections du Québec (DGEQ)

## Structure des fichiers

```
surveys/elxnqc_particip_egm_2021/
├── raw/
│   ├── data.csv              ← Données brutes (3222 lignes)
│   └── codebook.md           ← Codebook original (85 entrées)
├── processed/                ← Vide, à remplir après nettoyage
├── clean.py                  ← Script de nettoyage (TOI!)
└── MANUAL_CLEANING_GUIDE.md  ← Ce fichier
```

## Workflow de nettoyage manuel

### 1. Éditer `clean.py`

Ouvre `surveys/elxnqc_particip_egm_2021/clean.py` et ajoute ton code dans la fonction `clean_data(df)` autour de la ligne 113 (après le TODO).

### 2. Nomenclature (règles importantes)

Consulte `surveys/cleaning_rules.json` pour les règles complètes. Résumé:

**Préfixes de variables:**
- `id_` : Identifiants (caseid, respondent_id)
- `ses_` : Socio-économiques (age, gender, education, income, province)
- `op_` : Opinions
- `behav_` : Comportements (vote, participation)
- `tech_` : Techniques (weights, filters)
- `weight_` : Pondérations

**Valeurs catégorielles:**
- Simples et concises (PAS de répétition du nom de variable)
- Exemples:
  - `ses_gender`: "male", "female", "other" (PAS "gender_male")
  - `ses_province`: "quebec", "ontario" (PAS "province_quebec")
  - `behav_vote_turnout`: "voted", "did_not_vote", "not_eligible"

**Valeurs ordinales:**
- Normaliser à [0, 1] avec .map()
- Exemple: Likert 1-5 → {1: 1.0, 2: 0.75, 3: 0.5, 4: 0.25, 5: 0.0}

**Variables continues (age, income):**
- Créer DEUX variables:
  - Continuous: `ses_age` (numeric)
  - Categorical: `ses_age_category` (character avec bins)

### 3. Patterns de code sécurisés

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

### 4. Tester le script

```bash
# Activer venv
source venv/bin/activate

# Exécuter le script
python surveys/elxnqc_particip_egm_2021/clean.py
```

Si succès, tu obtiendras:
- `processed/data_cleaned.csv`
- `processed/codebook.json`

### 5. Variables à nettoyer (84 total)

#### Identifiants et techniques
- `caseid` → `id_respondent`
- `pond17`, `pondalt` → `weight_main`, `weight_alternative`

#### Démographiques (ses_)
- `age` → `ses_age` + `ses_age_category`
- `sexe`, `sexep` → `ses_gender`
- `langm` → `ses_language_home`
- `orig` → `ses_born_canada`
- `scol` → `ses_education`
- `occup` → `ses_occupation`
- `reven` → `ses_income_household` + `ses_income_household_category`
- `menag` → `ses_household_type`
- `regio` → `ses_region_administrative`

#### Comportements électoraux (behav_)
- `q1`, `q1x` → `behav_vote_turnout_2021`
- `q2` → `behav_vote_method` (en personne, par correspondance, etc.)
- `q13` → `behav_contacted_by_campaign`
- `q15` → `behav_vote_frequency_history`
- `q16` → `behav_vote_duty_vs_choice`
- `q19` → `behav_volunteering_past_year`
- `q20` → `behav_civic_participation_past_year`
- `q24` → `behav_considered_running_for_office`

#### Opinions et attitudes (op_)
- `q3a`, `q3b` → `op_covid_measures_*` (compréhension, rassurance)
- `q4` → `op_voting_ease`
- `q5a-q5i` → `op_reason_not_vote_*` (série de raisons)
- `q6a` → `op_knowledge_candidates_names`
- `q6b` → `op_knowledge_candidates_platforms`
- `q7` → `op_closeness_to_party`
- `q8`, `q8x` → `op_campaign_finance_rules_adequate`
- `q9` → `op_satisfaction_democracy_municipal`
- `q10a-q10e` → `op_trust_council_*` (série d'énoncés)
- `q11` → `op_council_decisions_impact`
- `q14` → `op_interest_municipal_politics`
- `q17a-q17c` → `op_voting_perception_*` (fierté, importance, etc.)
- `q18` → `op_frequency_discuss_politics`
- `q21` → `op_sense_of_belonging_municipality`
- `q22` → `op_years_living_municipality`
- `q23` → `op_homeownership`
- `q25a-q25e` → `op_barrier_running_office_*` (série de barrières)

#### Sources d'information (tech_ ou op_)
- `q12_m1` à `q12_m8` → Variables multi-réponses sources d'information

#### Variables à potentiellement EXCLURE (PII ou non pertinentes)
- `cp` : Code postal (PII - non dans le dataset extrait)
- `popnum`, `qpop`, `qregiz` : Quotas techniques
- `excl` : Filtre technique
- `muncp` : Municipalité (PII potentiel si trop granulaire)
- `q5j_o`, `q5j_o_m1`, `q5j_o_m2` : Réponses ouvertes (texte libre)
- `q5t_m1` à `q5t_m9` : Variables techniques non documentées

## Références

- **Codebook complet**: `raw/codebook.md`
- **Règles de nettoyage**: `../../cleaning_rules.json`
- **Template de référence**: `../../_template/clean.py`

## Prochaines étapes après nettoyage

1. Valider les outputs (`processed/data_cleaned.csv`)
2. Vérifier le codebook généré (`processed/codebook.json`)
3. Créer un commit git avec tes changements
4. Intégrer dans le pipeline AWS si nécessaire

---

**Bon nettoyage! 🧹**
