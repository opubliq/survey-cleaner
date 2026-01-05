# Stratégie de nettoyage hybride pour données de sondages

**Date**: 2025-01-05  
**Contexte**: Amélioration du workflow de nettoyage de données de sondages  
**Objectif**: Réduire temps et coûts tout en maintenant qualité et scalabilité

---

## Résumé exécutif

Le workflow manuel variable-par-variable avec agents "micro" Claude Code s'est révélé **non viable** (46,200 tokens/variable, 6h+ par sondage de 84 variables). 

La solution proposée dépend de votre contexte :

### Pour sondages hétérogènes (tous différents) :
**Agents "macro" Claude Code + Pattern Library évolutive**
- Agents orchestrateurs par phase (pas par variable)
- Pattern library qui s'enrichit avec chaque sondage
- Gains : 98% réduction tokens (2.9M vs 184M pour 40 sondages), 79% réduction temps (50h vs 240h)

### Pour familles de sondages similaires :
**Agents (setup) + API (exécution)**
- Setup famille avec agents (1 fois)
- Exécution automatique via API (répétable)
- Gains : 99% réduction tokens, 85% réduction temps

### Pour répétitions exactes (panels, baromètres) :
**Agents (setup 1×) + API automatisée**
- Setup initial avec agents
- Pipeline automatique ensuite
- Gains : Automatisation complète possible

---

## 1. Le rôle central du codebook

### 1.1 Pourquoi le codebook est critique

Le codebook n'est pas qu'une documentation - c'est **la source de vérité sémantique** :

**Sans codebook** : Une variable `age=[1,2,3,4,5,6]` pourrait signifier :
- Des groupes d'âge : `1="18-24", 2="25-34"...`
- Une échelle de Likert : `1="Très jeune", 2="Jeune"...`
- Des codes arbitraires d'un autre système

**Avec codebook** : On sait exactement ce que représente chaque valeur.

### 1.2 Anatomie d'une entrée de codebook

Un bon codebook contient **6 types d'information essentielles** :

```
Variable: Q5_participation_locale
Question: "À quelle fréquence participez-vous à des assemblées citoyennes?"
Type: Catégoriel ordinal
Valeurs:
  1 = Jamais
  2 = Rarement (1-2 fois par année)
  3 = Occasionnellement (3-5 fois par année)
  4 = Régulièrement (6+ fois par année)
  98 = Ne sait pas
  99 = Refuse de répondre
Notes: Question posée seulement aux répondants ayant répondu "Oui" à Q4
```

| Information | Utilité | Exemple |
|-------------|---------|---------|
| **1. Sémantique** | Comprendre le sens | Texte de la question posée |
| **2. Mapping valeurs** | Transformer correctement | `1 = "Jamais"` (pas juste "1") |
| **3. Type de variable** | Choisir traitement approprié | Catégoriel ordinal vs nominal |
| **4. Valeurs spéciales** | Gérer données manquantes | `98=NSP`, `99=Refus` → NaN |
| **5. Contraintes** | Valider résultats | Skip logic, plages valides |
| **6. Métadonnées** | Nommer intelligemment | "participation_locale" vs "Q5" |

### 1.3 Trois approches pour intégrer le codebook

#### Approche 1 : Pattern matching enrichi par codebook

Combiner détection structurelle (pattern des données) + validation sémantique (codebook) :

```
Niveau 1: DÉTECTION STRUCTURELLE (rapide)
  → Variable a 5 valeurs entières [1-5]
  → Candidat : likert_5

Niveau 2: ENRICHISSEMENT SÉMANTIQUE (codebook)
  → Question contient "d'accord" / "désaccord"
  → Labels contiennent "fortement", "plutôt"
  → Type = "ordinal"

Niveau 3: VALIDATION CROISÉE
  → Structure + Sémantique concordent
  → Confiance : 95%
  → Pattern confirmé : likert_5_accord
```

#### Approche 2 : Codebook comme "schema" de transformation

Le codebook devient une spécification formelle :

```json
{
  "variable": "Q5_participation_locale",
  "question_text": "À quelle fréquence participez-vous...",
  "value_labels": {
    "1": "Jamais",
    "2": "Rarement (1-2 fois par année)",
    "3": "Occasionnellement (3-5 fois par année)",
    "4": "Régulièrement (6+ fois par année)"
  },
  "missing_codes": {"98": "NSP", "99": "Refus"},
  "variable_type": "categorical_ordinal",
  "clean_name": "participation_assemblees_freq"
}
```

La transformation est alors **dérivée directement** du schema (0 tokens).

#### Approche 3 : LLM comme "interprète" du codebook

Pour les cas complexes, le LLM lit et interprète le codebook :

```python
prompt = f"""
VARIABLE: {var_name}
DONNÉES: {échantillon_valeurs}
CODEBOOK: {entrée_codebook_complète}

Analyse cette variable en utilisant UNIQUEMENT le codebook.

Retourne JSON avec:
- semantic_name: Vrai nom conceptuel
- variable_type: Type précis
- value_mapping: Mapping valeurs → labels (du codebook!)
- missing_values: Codes pour NA/NSP/Refus
- transformation_code: Code Python pour appliquer mapping

IMPORTANT: Ne jamais inventer de labels.
"""
```

---

## 2. Architecture conceptuelle du système hybride

**Note importante** : Cette architecture décrit le **concept général** du système hybride. L'implémentation concrète (Agents Claude Code vs API Python) dépend de votre contexte spécifique (voir section 11).

### 2.1 Vue d'ensemble des phases

```
┌─────────────────────────────────────────────────────────────┐
│ PHASE 0: Parse Codebook (1 fois)                           │
│ ─────────────────────────────────────────────────────────── │
│ Input:  codebook (Excel/CSV/Word/etc.)                      │
│ Output: codebook_schema.json (standardisé)                  │
│                                                              │
│ Pour chaque variable:                                        │
│   → Extraire question_text                                   │
│   → Extraire value_labels                                    │
│   → Inférer semantic_name                                    │
│   → Détecter missing_codes                                   │
│   → Suggérer pattern si évident                              │
│                                                              │
│ Implémentation: @codebook-analyzer agent (Claude Code)      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ PHASE 1: Classification (instantané)                        │
│ ─────────────────────────────────────────────────────────── │
│                                                              │
│ TYPE A: Codebook complet + pattern standard (60-70%)        │
│   → Route: RULE-BASED                                        │
│   → Exemple: age = {1:"18-24", 2:"25-34", ...}              │
│                                                              │
│ TYPE B: Codebook complet + pattern non-standard (15-25%)    │
│   → Route: LLM-INTERPRET (batch)                            │
│   → Exemple: Q12 = {1:"Oui, beaucoup", 2:"Oui, un peu"}    │
│                                                              │
│ TYPE C: Codebook incomplet/absent (5-15%)                   │
│   → Route: LLM-INFER ou MANUAL                              │
│   → Exemple: var_mysterious sans documentation              │
│                                                              │
│ Implémentation: @pattern-matcher agent (Claude Code)        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ PHASE 2: Transformation                                      │
│ ─────────────────────────────────────────────────────────── │
│                                                              │
│ TYPE A → Rule-based (0 tokens supplémentaires)              │
│   Apply .map() avec value_labels du codebook                │
│                                                              │
│ TYPE B → LLM batch (tokens minimisés par batching)          │
│   Batch de 10 vars = 1 appel LLM                            │
│                                                              │
│ TYPE C → LLM individuel ou manuel                            │
│   Cas complexes traités séparément                          │
│                                                              │
│ Implémentation: @batch-cleaner agent (Claude Code)          │
│              ou script Python + API (selon contexte)        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ PHASE 3: Validation & QA                                    │
│ ─────────────────────────────────────────────────────────── │
│ → Vérifier distributions                                     │
│ → Détecter anomalies                                         │
│ → Flaguer variables nécessitant review humaine              │
│                                                              │
│ Implémentation: @quality-validator agent (Claude Code)      │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Estimation des coûts selon implémentation

#### Scénario 1 : Sondages hétérogènes (Agents Claude Code uniquement)

**Sondage type (84 variables)** :

| Phase | Description | Tokens | Temps |
|-------|-------------|--------|-------|
| Phase 0 | Parse codebook (agent) | ~5-10k | 2 min |
| Phase 1 | Classification (agent) | ~2k | 30 sec |
| Phase 2A | Rule-based (59 vars) | 0 | 2 sec |
| Phase 2B | LLM batch (21 vars, 3 batches) | ~45k | 3 min |
| Phase 2C | LLM individuel (4 vars) | ~5k | 1 min |
| Phase 3 | Validation (agent) | ~3k | 30 sec |
| **TOTAL** | **Premier sondage** | **~60-70k** | **~8-10 min** |

**Note** : Tokens diminuent avec maturité de pattern library (40-50k après 20 sondages)

**Pour 40 sondages hétérogènes** : ~2.9M tokens, ~40-60h humain total

---

#### Scénario 2 : Familles de sondages (Agents setup + API exécution)

**Setup famille (1 fois, avec agents)** :
- Analyse de 2-3 sondages exemples : ~80-100k tokens
- Création template réutilisable : ~10k tokens
- **Total setup** : ~90-110k tokens, 2-3h humain

**Exécution membre famille (API automatique)** :
- Parse data + apply rules : 0 tokens
- LLM pour edge cases : ~20-30k tokens
- **Total exécution** : ~20-30k tokens, automatique

**Pour 12 sondages d'une famille** : 100k (setup) + 12×25k (exécution) = ~400k tokens

---

#### Scénario 3 : Répétitions exactes (Agents setup + API automatisée)

**Setup (1 fois, avec agents)** : ~50k tokens, 1h humain

**Exécutions mensuelles (API automatique)** : ~5k tokens, 0 temps humain

**Pour 12 mois** : 50k + 12×5k = ~110k tokens total

---

## 3. Les 10 patterns standards prioritaires

Ces patterns couvrent ~70% des variables typiques de sondages québécois :

### 🔴 Priorité 1 (couvre 30-40% des variables)

#### Pattern 1 : Likert 5 points (accord/désaccord)

**Détection** :
- Valeurs : [1, 2, 3, 4, 5]
- Keywords codebook : "accord", "d'accord", "fortement", "plutôt"
- Distribution : symétrique autour de 3

**Transformation** :
```python
{
  1: "Fortement en désaccord",
  2: "Plutôt en désaccord",
  3: "Ni en accord ni en désaccord",
  4: "Plutôt en accord",
  5: "Fortement en accord"
}
```

**Exemples de variables** : Q12_economie, Q15_immigration, attitude_gouvernement

---

#### Pattern 2 : Likert 4 points (fréquence)

**Détection** :
- Valeurs : [1, 2, 3, 4]
- Keywords : "jamais", "rarement", "parfois", "souvent", "toujours"

**Transformation** :
```python
{
  1: "Jamais",
  2: "Rarement",
  3: "Parfois",
  4: "Souvent/Toujours"
}
```

**Exemples** : participation_evenements, lecture_nouvelles, Q8_frequence

---

### 🟠 Priorité 2 (couvre 15-20% des variables)

#### Pattern 3 : Binaire Oui/Non

**Détection** :
- Valeurs : [0, 1] ou [1, 2]
- Keywords : "oui", "non"

**Transformation** :
```python
lambda val: "Oui" if val in [1, "Oui"] else "Non"
```

**Exemples** : vote_derniere_election, membre_parti, Q3_participation

---

#### Pattern 4 : Groupes d'âge Québec standard

**Détection** :
- Nom variable : "age", "age_group", "ses_age"
- Valeurs : [1, 2, 3, 4, 5, 6]
- Keywords : "18-24", "25-34", "35-44"

**Transformation** :
```python
{
  1: "18-24",
  2: "25-34",
  3: "35-44",
  4: "45-54",
  5: "55-64",
  6: "65+"
}
```

---

#### Pattern 5 : Sexe/Genre

**Détection** :
- Nom variable : "sexe", "sex", "gender", "genre"
- Valeurs uniques : 2 ou 3
- Keywords : "homme", "femme", "masculin", "féminin"

**Transformation** :
```python
{
  1: "Homme",
  2: "Femme",
  3: "Autre/Non-binaire"  # si applicable
}
```

---

### 🟡 Priorité 3 (couvre 10-15% des variables)

#### Pattern 6 : Échelle 0-10

**Détection** :
- Valeurs : 0 à 10
- Keywords : "échelle", "0 à 10", "satisfaction", "probabilité"

**Transformation** : Garder numérique, optionnel binning en catégories

---

#### Pattern 7 : Éducation (niveaux)

**Détection** :
- Nom : "educ", "education", "scolarite"
- Keywords : "primaire", "secondaire", "collégial", "universitaire"

**Transformation** :
```python
{
  1: "Primaire ou moins",
  2: "Secondaire",
  3: "Collégial/DEP",
  4: "Universitaire 1er cycle",
  5: "Universitaire 2e/3e cycle"
}
```

---

#### Pattern 8 : Revenu (tranches)

**Détection** :
- Nom : "revenu", "income", "salaire"
- Keywords : "moins de", "$", "k$"

**Transformation** :
```python
{
  1: "Moins de 20k$",
  2: "20k$ - 39k$",
  3: "40k$ - 59k$",
  4: "60k$ - 79k$",
  5: "80k$ - 99k$",
  6: "100k$ et plus"
}
```

---

#### Pattern 9 : Choix multiples (checkbox)

**Détection** :
- Valeurs : [0, 1] pour plusieurs variables avec même préfixe
- Keywords : "sélectionner", "cocher", "plusieurs choix"
- Pattern nom : "Q5_option_A", "Q5_option_B", etc.

**Transformation** : One-hot encoding (déjà fait), renommer clairement

---

#### Pattern 10 : Valeurs manquantes spéciales

**Détection** :
- Valeurs : 98, 99, -99, -9, "NSP", "Refus"
- Keywords : "ne sait pas", "refus", "sans réponse"

**Transformation** : Convertir en NaN avec métadata sur la raison

```python
missing_map = {
  98: np.nan,  # metadata: "Ne sait pas"
  99: np.nan   # metadata: "Refuse de répondre"
}
```

---

## 4. Nettoyage manuel pour cas complexes

### 4.1 Quand escalader vers manuel ?

**Critères pour escalade** :
- Variable absente du codebook ET distribution ambiguë
- Logique métier complexe (calculs multi-variables)
- Texte libre nécessitant catégorisation qualitative
- Données corrompues/incohérentes nécessitant investigation
- Skip logic complexe avec multiples dépendances

**Proportion attendue** : ~5-10% des variables

### 4.2 Workflow de review manuelle

```
1. FLAGGING AUTOMATIQUE
   Le système identifie variables problématiques :
   → Confiance détection < 30%
   → Codebook manquant + distribution non-standard
   → Échec validation (ex: 95% de valeurs manquantes)

2. GÉNÉRATION DE RAPPORT
   Pour chaque variable flaggée :
   → Résumé de la tentative automatique
   → Raison de l'échec
   → Suggestions d'investigation

3. REVIEW HUMAINE
   Analyste examine :
   → Données brutes
   → Documentation disponible
   → Contexte du sondage
   
4. DÉCISION
   → Nettoyage manuel + documentation
   → Exclusion de la variable (justifiée)
   → Ajout d'un nouveau pattern pour futur
```

### 4.3 Feedback loop

Les cas manuels enrichissent le système :

```python
# Après nettoyage manuel réussi d'une variable
def add_pattern_from_manual_cleaning(var_name, transformation_applied):
    """
    Analyser le nettoyage manuel pour créer un nouveau pattern
    """
    
    # Extraire les caractéristiques de la variable
    pattern_signature = extract_signature(var_name)
    
    # Généraliser la transformation
    generalized_pattern = generalize_transformation(transformation_applied)
    
    # Ajouter à la bibliothèque de patterns
    PATTERNS_LIBRARY.append({
        'pattern_id': f'custom_{var_name}',
        'detection': pattern_signature,
        'transformation': generalized_pattern,
        'source': 'manual_cleaning',
        'validated': True
    })
    
    # Cette variable similaire sera automatique la prochaine fois
```

---

## 5. Pour plus de détails : voir section 11

Les sections détaillées sur les métriques, l'implémentation et les choix technologiques se trouvent dans la **section 11 : Choix technologique : Claude Code vs API vs Hybride**.

Cette section couvre :
- Comparaison détaillée des trois contextes (sondages hétérogènes, familles, répétitions)
- Architecture complète des agents "macro"
- Métriques de succès selon votre contexte
- Guide de décision pour choisir l'approche optimale

---

## 11. Choix technologique : Claude Code vs API vs Hybride

### 11.1 Le rôle des agents dans le workflow

#### Agents "micro" actuels (❌ Non viable)

Le workflow testé utilisait des agents spécialisés par opération :
```
.claude/agents/
├── survey-init.md        # Initialise structure
├── transform-codebook.md # Parse codebook
├── clean-variable.md     # Nettoie 1 variable
└── validate-survey.md    # Valide
```

**Problème** : 46,200 tokens/variable car :
- Instructions complètes rechargées à chaque appel
- Contexte conversationnel maintenu
- 24-28 tool uses par opération

#### Agents "macro" proposés (✅ Optimal)

Agents par **phase du workflow** plutôt que par variable :

```
.claude/agents/
├── master-cleaner.md         # Orchestrateur principal
├── codebook-analyzer.md      # Parse codebook (tous formats)
├── pattern-matcher.md        # Match avec bibliothèque globale
├── pattern-learner.md        # Découvre nouveaux patterns
├── batch-cleaner.md          # Nettoie efficacement
└── quality-validator.md      # Valide outputs
```

**Avantage** : Un agent traite toute une phase, pas une variable à la fois.

---

### 11.2 Comparaison des approches selon le contexte

#### Contexte A : Sondages **très hétérogènes** (chacun unique)

**Caractéristiques** :
- 40 sondages de sources variées (universités, ministères provinciaux/fédéraux)
- Codebooks dans formats différents (Excel, CSV, Word, absent)
- Questions et structures très variables
- Peu de patterns réutilisables entre sondages (30-40% overlap)

**Solution recommandée : Claude Code + Agents macro uniquement**

| Aspect | Détail |
|--------|--------|
| **Approche** | Agents adaptatifs pour chaque sondage |
| **Réutilisation** | Pattern library globale qui s'enrichit |
| **Coût/sondage** | 40-150k tokens (diminue avec maturité library) |
| **Temps/sondage** | 30 min - 2h selon complexité |
| **Scalabilité** | 40 sondages = ~50h temps humain total |
| **Automatisation** | Limitée (présence humaine pour supervision) |

**Workflow type** :
```bash
# Nouveau sondage unique
> @master-cleaner nettoie [nom_sondage] --learn

[master] Analyzing codebook... (format: Excel, 3 sheets)
[master] Matching against pattern library...
[master] ✓ 68/94 vars (72%) matched existing patterns
[master] ⚠️ 22 vars need LLM (batching)
[master] ⚠️ 4 vars complex (flagged for review)
[master] Cleaning... 
[master] Learning 2 new patterns from edge cases
[master] ✓ Complete! 90/94 vars (96%)

Total: ~60k tokens, 45 min
```

**Pattern library évolutive** :
```
patterns_library/
├── core_patterns.json          # 10 patterns universels
├── domain_electoral.json       # Appris des sondages ELXN
├── domain_health.json          # Appris des sondages santé
├── domain_participation.json   # Appris des sondages participation
└── edge_cases.json            # Cas rares accumulés

Taux de couverture:
- Après 10 sondages: ~50%
- Après 20 sondages: ~70%
- Après 40 sondages: ~80%
```

**Estimation coûts pour 40 sondages hétérogènes** :

| Phase | Sondages | Tokens/sondage | Total | Temps humain |
|-------|----------|----------------|-------|--------------|
| Phase 1 (bootstrap) | 1-10 | 100-150k | 1.2M | 20-30h |
| Phase 2 (maturation) | 11-20 | 60-80k | 700k | 10-15h |
| Phase 3 (maturité) | 21-40 | 40-60k | 1M | 8-12h |
| **TOTAL** | **40** | **~72k moy** | **~2.9M** | **~40-60h** |

**vs approche manuelle actuelle** : 
- Tokens : 2.9M vs 184M (98.4% réduction)
- Temps : 50h vs 240h (79% réduction)
- Coût : $0 (quota Claude Code) vs prohibitif

---

#### Contexte B : Sondages **moyennement similaires** (familles identifiables)

**Caractéristiques** :
- 40 sondages groupables en 3-5 familles
- Exemple : 12 ELXN similaires, 8 santé similaires, 8 participation, 12 uniques
- Codebooks partiellement standardisés
- 50-70% de patterns communs dans chaque famille

**Solution recommandée : Claude Code + Agents (setup) → API (exécution)**

**Workflow pour nouvelle famille** :
```bash
# PHASE 1: Setup famille avec agents (1 fois)
> @master-cleaner analyse famille ELXN et crée template

[master] Analyzing 3 sample ELXN surveys...
[master] Identifying common patterns... 15 found
[master] Generating elxn_patterns.json
[master] Generating elxn_cleaner.py (paramétrable)
[master] ✓ Template ready for reuse

Coût: ~80-100k tokens, 2-3h humain
```

```python
# PHASE 2: Exécution avec API (répétable)
$ python elxn_cleaner.py --survey ELXN_federal_2025

# Le script:
# - Charge elxn_patterns.json
# - Apply rules (80% des variables, 0 tokens)
# - Call API for edge cases (20% variables, batch)

Coût: ~20k tokens ($0.06), automatique
```

**Coûts pour 40 sondages en familles** :

| Famille | Sondages | Setup (1×) | Exécution (n×) | Total |
|---------|----------|------------|----------------|-------|
| ELXN | 12 | 80k | 12 × 20k = 240k | 320k |
| Santé | 8 | 80k | 8 × 25k = 200k | 280k |
| Participation | 8 | 80k | 8 × 20k = 160k | 240k |
| Uniques | 12 | - | 12 × 70k = 840k | 840k |
| **TOTAL** | **40** | **240k** | **1,440k** | **~1.7M** |

**Temps humain** : ~30-35h (vs 50h contexte A, vs 240h manuel)

---

#### Contexte C : Sondages **très similaires** (répétitions exactes)

**Caractéristiques** :
- Même sondage avec mises à jour régulières
- Exemples : Baromètre mensuel, panel électoral par vagues
- Structure identique, nouveaux répondants ajoutés
- 90%+ de patterns identiques

**Solution recommandée : Agents (setup 1×) → API pure (exécution automatique)**

**Setup initial** :
```bash
> @master-cleaner crée pipeline pour Barometre_Satisfaction

[master] Generating barometre_cleaner.py
[master] All 84 variables mapped to patterns
[master] ✓ Ready for automated execution

Coût: ~50k tokens, 1h humain
```

**Exécutions mensuelles** :
```python
# Automatique via AWS Lambda ou cron
$ python barometre_cleaner.py --data janvier_2025.csv

Coût: ~5k tokens ($0.02), 0 temps humain
```

**Cas d'usage API pure** :
- Rapports automatisés mensuels/trimestriels
- Panels suivis dans le temps (vagues T0, T1, T2...)
- Intégration dans pipeline AWS (S3 trigger → Lambda → nettoyage)

---

### 11.3 Architecture des agents "macro"

#### Agent 1 : `master-cleaner.md`

```markdown
# Master Cleaner Agent

Orchestrateur principal du nettoyage de sondages.

## Responsabilités
- Analyser nouveau sondage
- Router vers agents spécialisés
- Optimiser utilisation des tokens
- Apprendre de chaque sondage

## Workflow décisionnel

1. **Évaluation initiale**
   - Codebook existe ? Format ?
   - Pattern library existe ?
   - Famille de sondage détectée ?

2. **Stratégie de nettoyage**
   - Classifier variables (standard/edge/complex)
   - Optimiser ordre de traitement
   - Décider batch size pour LLM

3. **Orchestration**
   - Déléguer à agents spécialisés
   - Monitorer progression
   - Consolider résultats

4. **Apprentissage**
   - Identifier nouveaux patterns
   - Enrichir pattern library
   - Documenter edge cases

## Commandes
- `@master-cleaner nettoie [survey] --learn`
- `@master-cleaner analyse famille [family_name]`
- `@master-cleaner status` (progression, stats)
```

#### Agent 2 : `codebook-analyzer.md`

```markdown
# Codebook Analyzer Agent

Expert en parsing de codebooks tous formats.

## Capacités
- Excel (multi-onglets, formats variables)
- CSV/TSV (avec ou sans headers)
- Word/PDF (extraction texte)
- Codebook absent (inférence depuis données)

## Output
- codebook_schema.json standardisé :
  {
    "variable": {
      "question_text": "...",
      "value_labels": {...},
      "variable_type": "categorical_ordinal",
      "missing_codes": [98, 99],
      "suggested_pattern": "likert_5_accord"
    }
  }

## Gestion cas difficiles
- Codebook incomplet → flag variables sans doc
- Format bizarre → adaptation interactive
- Multi-langues → détection langue principale
```

#### Agent 3 : `pattern-matcher.md`

```markdown
# Pattern Matcher Agent

Match variables avec pattern library globale.

## Input
- codebook_schema.json
- patterns_library/*.json

## Workflow
1. Pour chaque variable:
   - Calculer score de match avec chaque pattern
   - Seuil confiance > 85% → standard
   - Seuil 50-85% → edge case (vérifier avec LLM)
   - Seuil < 50% → complex (analyse approfondie)

2. Grouper edge cases par type (batch LLM optimal)

3. Output classification complète

## Scoring sophistiqué
- Nom variable (30%)
- Valeurs uniques (30%)
- Keywords codebook (25%)
- Distribution statistique (15%)
```

#### Agent 4 : `pattern-learner.md`

```markdown
# Pattern Learner Agent

Découvre et formalise nouveaux patterns.

## Déclenchement
- Variables non matchées récurrentes
- Edge cases similaires dans plusieurs sondages
- Demande explicite utilisateur

## Workflow
1. Analyser 3-5 exemples du pattern
2. Extraire caractéristiques communes
3. Générer règle de détection
4. Tester sur autres variables
5. Valider avec utilisateur
6. Ajouter à pattern library

## Output
- Nouveau pattern formalisé
- Tests de validation
- Documentation
```

#### Agent 5 : `batch-cleaner.md`

```markdown
# Batch Cleaner Agent

Nettoie efficacement en optimisant tokens.

## Stratégies d'optimisation

### Pour variables standard (rule-based)
- Apply patterns directement
- 0 tokens consommés
- Validation automatique inline

### Pour edge cases (LLM batch)
- Grouper 10 variables similaires
- 1 appel LLM = 15k tokens
- Contexte minimal par variable

### Pour variables complexes
- Traitement individuel si nécessaire
- Flag pour review manuelle si trop complexe

## Logging détaillé
- Tokens par variable
- Temps par opération
- Taux de succès par pattern
```

#### Agent 6 : `quality-validator.md`

```markdown
# Quality Validator Agent

Valide et flag anomalies.

## Vérifications
- Distributions cohérentes
- Pas de valeurs hors range
- Missing values raisonnables (<30%)
- Skip logic respectée

## Output
- Rapport de validation
- Variables flaggées pour review
- Statistiques descriptives
- Recommandations
```

---

### 11.4 Comparaison finale : Quand utiliser quoi ?

| Critère | Claude Code + Agents | API (après setup) | Hybride |
|---------|---------------------|-------------------|---------|
| **Sondages hétérogènes** | ✅✅✅ Optimal | ❌ Pas adapté | ⚠️ Possible |
| **Familles similaires** | ✅ Setup | ✅✅ Exécution | ✅✅✅ Optimal |
| **Répétitions exactes** | ⚠️ Setup seulement | ✅✅✅ Optimal | ✅✅ Très bon |
| **Codebooks variables** | ✅✅✅ Adaptatif | ❌ Rigide | ✅✅ Bon |
| **Learning continu** | ✅✅✅ Excellent | ❌ Aucun | ✅✅ Bon |
| **Automatisation** | ❌ Supervision requise | ✅✅✅ Complète | ✅✅ Partielle |
| **Coût 40 sondages** | ~2.9M tokens ($0) | ~300k tokens ($1) | ~1.7M tokens ($0.50) |
| **Temps humain** | 40-60h | 5-10h | 30-35h |

---

### 11.5 Recommandation selon votre contexte

#### Si vous avez 40 sondages vraiment différents :

**→ Claude Code + Agents macro uniquement**

**Justification** :
- Chaque sondage nécessite analyse contextuelle
- Pattern library s'enrichit progressivement
- Flexibilité maximale pour formats variables
- Coût inclus dans quota Claude Code

**Workflow** :
```bash
# Pour chaque nouveau sondage
> @master-cleaner nettoie [nom_sondage] --learn

# 40-150k tokens selon maturité de la library
# 30 min - 2h selon complexité
# Résultat : 90-95% variables nettoyées automatiquement
```

---

#### Si vous avez des familles identifiables :

**→ Agents (setup familles) + API (exécution membre famille)**

**Justification** :
- Investissement initial rentabilisé sur membres de la famille
- Automatisation des sondages similaires
- Réduction maximale du temps humain

**Workflow** :
```bash
# 1× par famille : Setup avec agents
> @master-cleaner analyse famille ELXN

# n× : Exécution automatique API
$ python elxn_cleaner.py --survey ELXN_2025
```

---

#### Si vous avez des mises à jour régulières :

**→ Agents (setup 1×) + API pure (exécutions automatiques)**

**Justification** :
- Structure identique
- Automatisation complète possible
- Coût marginal très faible

**Setup AWS Lambda** :
```python
# Déclenché automatiquement par upload S3
def lambda_handler(event, context):
    survey_file = event['s3']['object']['key']
    cleaner = SurveyCleaner(survey_file)
    df_clean = cleaner.clean()
    save_to_s3(df_clean)
```

---

## 12. Questions à clarifier pour finaliser l'approche

Avant d'implémenter, il est crucial de clarifier :

### 12.1 Sur la similarité des sondages

**Question 1** : Parmi vos 40 sondages, combien se regroupent en familles similaires ?

Exemples de réponse :
- "12 sondages ELXN quasi-identiques, 8 santé similaires, 20 vraiment uniques"
- "Tous les 40 sont différents"
- "10 familles de ~4 sondages chacune"

**Impact** : Détermine si approche "Agents seuls" ou "Agents + API"

---

**Question 2** : Certains sondages sont-ils répétés/mis à jour régulièrement ?

Exemples :
- "Baromètre mensuel de satisfaction (12× par an)"
- "Panel électoral suivi sur 6 vagues"
- "Tous one-shot, aucune répétition"

**Impact** : Justifie ou non l'investissement dans automatisation API

---

### 12.2 Sur les codebooks

**Question 3** : Quel est le niveau de standardisation de vos codebooks ?

Options :
- A) Tous Excel, même format (colonnes standardisées)
- B) Même format général mais variations mineures
- C) Formats très variés (Excel/CSV/Word/PDF/absent)

**Impact** : Si C → Agents adaptatifs essentiels. Si A → API plus facile.

---

**Question 4** : Quel % de vos variables sont documentées dans les codebooks ?

- "95%+ ont value labels complets"
- "~70% documentées, 30% à inférer"
- "Très variable selon sondage"

**Impact** : Détermine ratio rule-based vs LLM

---

### 12.3 Sur les objectifs

**Question 5** : Quel est votre objectif de temps par sondage ?

- "< 30 minutes acceptable"
- "< 2h nécessaire"
- "Peu importe si qualité garantie"

**Impact** : Ajuste niveau d'automatisation requis

---

**Question 6** : Prévoyez-vous d'augmenter le volume de sondages ?

- "Oui, passer de 10/an à 50/an"
- "Non, 10-15/an stable"
- "Incertain"

**Impact** : Justifie investissement dans infrastructure automatisée

---

## Conclusion

Le système de nettoyage hybride proposé offre :

✅ **98% réduction tokens** : 184M → 2.9M pour 40 sondages hétérogènes  
✅ **79% réduction temps** : 240h → 50h temps humain total  
✅ **Scalabilité** : De "impossible" à 50+ sondages/an  
✅ **Qualité maintenue** : >95% précision avec validation  
✅ **Amélioration continue** : Pattern library qui apprend  
✅ **Adaptabilité** : Agents gèrent formats variables  

**L'approche optimale dépend de votre contexte spécifique** :

| Votre contexte | Solution recommandée |
|----------------|---------------------|
| 40 sondages hétérogènes | **Agents Claude Code uniquement** |
| 3-5 familles de sondages | **Agents (setup) + API (exécution)** |
| Mises à jour régulières | **Agents (1×) + API automatisée** |

La clé du succès : **Pattern library évolutive** qui s'enrichit avec chaque sondage, réduisant progressivement les tokens et le temps requis.

---

**Auteurs** : Discussion Claude + Analyste  
**Date** : 2025-01-05  
**Version** : 2.0  
**Statut** : Proposition pour validation  
**Prochaine étape** : Clarifier questions section 12 pour finaliser architecture
