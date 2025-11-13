# CODEBOOK - [NOM_SONDAGE]

## Instructions

Ce fichier sert de référence humaine pour le nettoyage des données. Pour chaque variable:

1. **Lisez** la question et les choix de réponse dans ce fichier
2. **Nettoyez** la variable dans `clean.py` (mappings, normalisation)
3. **Transcrivez** les labels dans le dictionnaire `VARIABLE_METADATA` de `clean.py`

Le script `clean.py` générera automatiquement `processed/codebook.json` enrichi avec ces labels pour les LLMs downstream.

---

## Métadonnées du sondage

- **Titre**: [Titre complet du sondage]
- **Année**: [YYYY]
- **Source**: [Organisation/URL]
- **Fichier brut**: [data.csv/data.sav/data.xlsx]
- **Notes**: [Informations importantes sur le sondage]

---

## Variables démographiques

### ses_age

**Question**: Quel âge avez-vous?

**Type**: Numérique continu

**Variable brute**: `age` ou `Q1_age`

**Valeurs**:
- 18-100: Âge en années
- -99 / 999: Valeur manquante

**Notes**: Créer deux variables - `ses_age` (continu) et `ses_age_category` (catégorisé)

---

### ses_gender

**Question**: Quel est votre genre?

**Type**: Catégoriel

**Variable brute**: `gender` ou `Q2_sexe`

**Choix de réponse**:
- 1 = Homme
- 2 = Femme
- 3 = Non-binaire
- 4 = Autre
- 99 = Préfère ne pas répondre

**Mapping recommandé**:
```python
1.0: 'male',
2.0: 'female',
3.0: 'non_binary',
4.0: 'other',
99.0: np.nan
```

---

### ses_province

**Question**: Dans quelle province habitez-vous?

**Type**: Catégoriel

**Variable brute**: `province` ou `Q3_province`

**Choix de réponse**:
- 1 = Québec
- 2 = Ontario
- 3 = Colombie-Britannique
- 4 = Alberta
- 5 = Manitoba
- 6 = Saskatchewan
- 7 = Nouvelle-Écosse
- 8 = Nouveau-Brunswick
- 9 = Île-du-Prince-Édouard
- 10 = Terre-Neuve-et-Labrador
- 11 = Yukon
- 12 = Territoires du Nord-Ouest
- 13 = Nunavut

**Mapping recommandé**:
```python
1.0: 'quebec',
2.0: 'ontario',
3.0: 'british_columbia',
# ... etc
```

---

## Variables d'opinion

### op_satisfaction_gov

**Question**: Dans quelle mesure êtes-vous satisfait du gouvernement actuel?

**Type**: Échelle Likert (5 points)

**Variable brute**: `satisfaction_gouv` ou `Q10_satisfaction`

**Choix de réponse**:
- 1 = Très insatisfait
- 2 = Plutôt insatisfait
- 3 = Neutre
- 4 = Plutôt satisfait
- 5 = Très satisfait
- 99 = Ne sait pas / Refuse

**Transformation**: Normaliser sur échelle 0-1 (1→0.0, 2→0.25, 3→0.5, 4→0.75, 5→1.0)

**Mapping recommandé**:
```python
1.0: 0.0,    # Très insatisfait
2.0: 0.25,   # Plutôt insatisfait
3.0: 0.5,    # Neutre
4.0: 0.75,   # Plutôt satisfait
5.0: 1.0,    # Très satisfait
99.0: np.nan
```

**Entrée VARIABLE_METADATA**:
```python
'op_satisfaction_gov': {
    'question_label': "Dans quelle mesure êtes-vous satisfait du gouvernement actuel?",
    'value_labels': {
        0.0: "Très insatisfait",
        0.25: "Plutôt insatisfait",
        0.5: "Neutre",
        0.75: "Plutôt satisfait",
        1.0: "Très satisfait"
    }
}
```

---

### op_environment_importance

**Question**: Quelle importance accordez-vous aux enjeux environnementaux?

**Type**: Échelle Likert (4 points)

**Variable brute**: `env_importance` ou `Q15_environnement`

**Choix de réponse**:
- 1 = Pas important du tout
- 2 = Peu important
- 3 = Assez important
- 4 = Très important
- 99 = Ne sait pas

**Transformation**: Normaliser sur échelle 0-1

---

## Variables politiques

### behav_vote_choice

**Question**: Pour quel parti avez-vous voté aux dernières élections?

**Type**: Catégoriel

**Variable brute**: `vote_intention` ou `Q20_vote`

**Choix de réponse**:
- 1 = Parti Libéral du Québec (PLQ)
- 2 = Coalition Avenir Québec (CAQ)
- 3 = Parti Québécois (PQ)
- 4 = Québec Solidaire (QS)
- 5 = Parti Conservateur du Québec (PCQ)
- 6 = Autre parti
- 7 = N'a pas voté
- 99 = Refuse de répondre

**Mapping recommandé**:
```python
1.0: 'liberal',
2.0: 'coalition_avenir_quebec',
3.0: 'parti_quebecois',
4.0: 'quebec_solidaire',
5.0: 'conservative',
6.0: 'other',
7.0: 'did_not_vote',
99.0: np.nan
```

---

## Variables techniques (à ignorer ou transformer)

### tech_response_date

**Variable brute**: `ResponseDate` ou `date_reponse`

**Type**: Date/timestamp

**Notes**: Convertir en ISO 8601 ou garder tel quel si pertinent

---

### tech_response_id

**Variable brute**: `ResponseID` ou `id_reponse`

**Type**: Identifiant unique

**Notes**: Renommer en `id_respondent` pour standardisation

---

## Variables PII (à EXCLURE)

Les variables suivantes contiennent des informations personnelles identifiables et ne doivent PAS être incluses dans les données nettoyées:

- `nom` / `name` - Nom complet
- `email` - Adresse courriel
- `telephone` / `phone` - Numéro de téléphone
- `adresse` / `address` - Adresse postale
- `code_postal` - Code postal (si 6 caractères)
- `ip_address` - Adresse IP

**Action**: Marquer comme SKIPPED dans `variables_todo.md`

---

## Conventions de nommage Opubliq

**Préfixes des variables nettoyées**:
- `ses_` - Socio-démographique (age, gender, education, income, province, region)
- `op_` - Opinion (satisfaction, trust, importance)
- `behav_` - Comportement (vote choice, turnout, participation)
- `tech_` - Technique (dates, IDs, survey metadata)

**Valeurs catégorielles**:
- Toujours en minuscules
- Mots séparés par underscore: `coalition_avenir_quebec`
- Simple et concis: `'quebec'` pas `'province_quebec'`
- Abréviations anglaises OK pour partis: `'liberal'`, `'ndp'`, `'bloc'`

**Échelles normalisées**:
- Toujours 0-1 pour variables ordinales
- 0 = minimum de l'échelle (ex: très insatisfait, pas du tout d'accord)
- 1 = maximum de l'échelle (ex: très satisfait, tout à fait d'accord)
- Valeurs intermédiaires espacées uniformément (0, 0.25, 0.5, 0.75, 1.0)

**Valeurs manquantes**:
- Convertir tous les codes manquants (99, -99, -98, etc.) en `np.nan`
- Ne jamais laisser de codes numériques arbitraires dans les données nettoyées
