# Questions : Architecture opérationnelle du pipeline de nettoyage

## Contexte du projet

Pipeline de nettoyage de sondages québécois (CSV/SAV) qui génère un script Python (`clean.py`)
standardisant les variables brutes (ex: `Q2 = 1,2,3` → `ses_province = "qc","on","bc"`).

Architecture 3-tiers **implémentée** :
- **Tier 1** : pattern reconnu (confiance ≥ 0.8) → règle déterministe générée automatiquement (gratuit)
- **Tier 2** : LLM léger en batch (GLM-5 gratuit via ZhipuAI)
- **Tier 3** : Claude Haiku individuel (cas complexes)

Ce qui est **implémenté** :
- `orchestrator.py` : coordonne tout le pipeline, sérialise l'état dans `status.json`
- `pattern_engine/pattern_classifier.py` : 8 étapes de classification (detect missing codes → cross-validate codebook → matcher tous les patterns → confidence threshold)
- `pattern_engine/patterns/` : 12 patterns (likert x5, demographics x4, binary x3, scales x3)
- `pattern_engine/missing_code_detector.py` : détection en 4 couches (codebook > value labels > heuristique > outlier)
- `llm_processors/tier2_batch.py` : GLM-5, prompt JSON, retry individuel
- `llm_processors/tier3_individual.py` : Claude Haiku, prompt très ciblé
- `validation/validator.py` : validation statique (AST) + validation dynamique (types, ranges) — mais **non connecté à l'orchestrateur**

Ce qui est **stub/incomplet** :
- Le `Batcher` (groupement par lot) est implémenté mais non utilisé — l'orchestrateur envoie 1 variable à la fois en Tier 2
- Le `CleanValidator` est implémenté mais non appelé par l'orchestrateur
- Les coûts LLM réels ne sont pas collectés (estimés seulement)
- Le `clean.py` généré n'inclut pas `CODEBOOK_VARIABLES` ni `get_metadata()` (contrairement au template cible)

---

## Question 1 : Rôle exact de l'orchestrateur — est-ce la bonne structure ?

L'orchestrateur actuel fait tout en séquence :

```
1. Charger le DataFrame (.csv/.sav/.dta)
2. Parser le codebook (codebook.json > codebook.md > xlsx/pdf/docx)
3. Classifier TOUTES les variables (pattern_classifier) → stocker tier/pattern_id/confidence
4. Boucler sur les variables pending, une par une :
   a. Tier 1 → pattern.generate_code() directement
   b. Tier 2 → tier2_batch.process() avec 1 variable à la fois (pas un vrai batch)
   c. Tier 3 → tier3_individual.process()
5. Assembler clean.py
```

**Problème identifié :** le Tier 2 envoie 1 variable à la fois alors qu'il est censé envoyer des batches de 10-20 variables pour réduire les coûts et les appels API.

**Question :** L'orchestrateur devrait-il :

**Option A — Séparer classification et traitement en deux passes**
```
Passe 1 : classifier toutes les variables → regrouper par tier
Passe 2 : traiter tous les Tier 1 (instantané), envoyer Tier 2 en vrais batches de 10-20, Tier 3 individuellement
```

**Option B — Garder la boucle séquentielle mais activer le vrai batching**
Accumuler les variables Tier 2 dans une file, flush par lot quand on atteint N=15 ou fin du pipeline.

**Option C — Pipeline event-driven (queue par tier)**
Chaque tier a sa propre file de traitement, les résultats alimentent la validation.

Quelle structure est la plus simple à maintenir pour une petite équipe, tout en activant le vrai batching Tier 2 ?

---

## Question 2 : La classification stat-only est-elle suffisante, ou faut-il un LLM dans la classification ?

Le classifier actuel est **100% déterministe** : stats pandas + heuristiques sur les value labels du codebook. Aucun LLM n'est impliqué dans la décision de tier.

**Exemple de limite :** une variable avec 5 valeurs {1,2,3,4,5} et un label ambigu comme "Q15_eval" sera classée Tier 1 Likert5 si le codebook dit `scale_type=likert`, mais Tier 2 sinon — même si un humain verrait immédiatement que c'est une échelle de satisfaction.

**Actuellement**, le classifier peut faire de faux Tier 1 (code incorrect généré sans validation) ou envoyer en Tier 2 des variables triviales que Tier 1 aurait pu gérer.

**Option A — Garder la classification 100% déterministe (statu quo)**
Avantage : zéro coût supplémentaire, déterministe, reproductible.
Risque : faux Tier 1 non détectés avant validation (qui n'est pas branchée).

**Option B — Ajouter un LLM ultra-léger (GLM-5 gratuit) pour les variables à confiance 0.5–0.79**
Ces variables iraient actuellement en Tier 2 anyway. On pourrait demander au LLM de confirmer/infirmer la classification du pattern_engine avant de décider.

**Option C — Post-classification review par LLM sur un échantillon aléatoire**
Pas dans le pipeline critique, mais auditer périodiquement 5-10% des décisions Tier 1 pour détecter des patterns défaillants.

Faut-il introduire un LLM dans la classification, ou est-ce une sur-ingénierie ?

---

## Question 3 : Vaut-il la peine d'optimiser les patterns sur 500 variables réelles ?

**Situation actuelle :** les 12 patterns ont été développés de façon raisonnée mais sans validation empirique sur un corpus de variables réelles. On ne sait pas si :
- Le taux de Tier 1 réel est proche de l'objectif ~50% ou bien en dessous
- Les seuils de confiance (0.8 pour Tier 1) sont bien calibrés
- Il y a des patterns manquants qui couvriraient une grande portion des variables

**Proposition de "battue" :** passer 500 variables aléatoires de vrais sondages (issus des 57 sondages existants) dans le classifier, comparer la classification automatique à une classification manuelle, et identifier les patterns manquants ou mal calibrés.

**Sous-question A :** vaut-il la peine d'investir ce temps (estimé : 2-4 jours), sachant que les variables Tier 2 coûtent quasi 0$ (GLM-5 gratuit) ?

**Sous-question B :** si oui, comment structurer cette battue ?
- Stratégie d'échantillonnage : aléatoire vs stratifié par type de variable ?
- Quel outil pour annoter rapidement (CSV + colonne manuelle, ou interface légère) ?
- Comment mesurer le gain : comparer le taux Tier 1 avant/après ?

**Sous-question C :** y a-t-il un seuil de taux Tier 1 (ex: ≥60%) en dessous duquel ça ne vaut pas la peine d'optimiser davantage les patterns ?

---

## Question 4 : Comment les variables nettoyées sont-elles nommées — la stratégie actuelle est-elle robuste ?

**Situation actuelle :** le nommage est un mélange de deux logiques :

- **Tier 1 et Tier 3** : l'orchestrateur utilise une fonction `_generate_clean_var_name()` basée sur le `pattern_type` et des mots-clés dans le nom brut :
  ```python
  # Exemple : demographic + "province" dans le nom → ses_province
  # Tout autre demographic → ses_<nom[:20]>
  # likert ou binary → op_<nom[:20]>
  # Tout autre → op_<nom[:20]>
  ```
  Le préfixe `behav_*` (comportement) n'est jamais généré par cette logique.

- **Tier 2** : le LLM (GLM-5) choisit lui-même le nom en respectant la convention `ses_*/op_*/behav_*` apprise dans le prompt.

**Problème :** les variables Tier 1 `op_<nom_brut[:20]>` peuvent être des noms peu lisibles (ex: `op_q15_m2_eval_gvt` au lieu de `op_satisfaction_gouvernement`). Incohérence entre tiers.

**Option A — Garder le nommage déterministe pour Tier 1 (statu quo)**
Simple, reproductible, pas de LLM supplémentaire. Les noms seront moches mais cohérents.

**Option B — Passer tous les noms par un LLM léger (GLM-5) après la classification**
Appel unique avec toutes les variables pour générer des noms propres en une passe. Coût marginal.

**Option C — Nommage basé sur le label du codebook plutôt que le nom brut**
Pour Tier 1, utiliser `var_label` (ex: "Satisfaction envers le gouvernement") comme base du nom standardisé → snake_case → préfixe selon pattern_type.

Quelle stratégie de nommage est la plus cohérente et maintenable ?

---

## Question 5 : Faut-il un LLM dans la phase de validation, et comment connecter la validation au pipeline ?

**Situation actuelle :** le `CleanValidator` existe mais n'est **pas appelé par l'orchestrateur**. Il fait :
- Validation **statique** : syntaxe Python (AST), assignations dupliquées, imports
- Validation **dynamique** : types de colonnes, ranges de valeurs, colonnes vides

**Ce qu'il ne fait pas :**
- Vérifier la cohérence sémantique du code (ex: est-ce que le mapping `{1: "Pas du tout d'accord", 5: "Tout à fait d'accord"}` est dans le bon sens ?)
- Détecter si un Tier 1 a généré du code incorrect (ex: un thermomètre 0-10 traité comme Likert)
- S'assurer que les noms générés respectent la convention (`ses_*/op_*/behav_*`)

**Sous-question A :** comment intégrer la validation dans l'orchestrateur ?
- Après chaque variable individuellement → retry immédiat si échec
- Après l'assemblage final du clean.py → une seule passe de validation en fin de pipeline

**Sous-question B :** faut-il un LLM dans la validation ?
- **Option Non-LLM :** validation statique/dynamique uniquement. Simple, gratuit, pas de faux positifs LLM.
- **Option LLM-light :** pour les variables Tier 1 seulement, faire vérifier la cohérence sémantique du code généré par GLM-5 (gratuit). Détecte les inversions de mapping, les mauvaises étiquettes.
- **Option LLM-lourd :** review complète du clean.py par Claude Haiku. Plus coûteux mais détecte plus d'erreurs.

---

## Question 6 : Que faire si la validation échoue — stratégie d'escalade de tier ?

**Situation actuelle :** aucune stratégie de fallback n'existe. Si le code généré est invalide, l'orchestrateur stocke le code d'erreur (`# ERROR: LLM call failed`) et continue.

**Proposition : escalade automatique de tier en cas d'échec de validation**

```
Tier 1 génère code → validation échoue → escalader en Tier 2
Tier 2 génère code → validation échoue → escalader en Tier 3
Tier 3 génère code → validation échoue → marquer needs_review=True, code d'erreur
```

**Questions concrètes :**

**A)** L'escalade devrait-elle être automatique ou nécessiter un seuil (ex: confiance Tier 1 < 0.85 → escalade directe sans même tenter la validation) ?

**B)** Quelle information transmettre au tier supérieur lors de l'escalade ?
- Juste le `reason` de l'échec de validation ?
- Le code incorrect généré par le tier précédent ?
- Les deux ?

**C)** Comment éviter les boucles infinies dans l'escalade (ex: Tier 3 qui échoue en boucle si le LLM hallucine) ?

**D)** Est-ce que la stratégie d'escalade justifie d'augmenter le seuil de confiance Tier 1 (ex: 0.8 → 0.9) pour réduire les faux positifs entrant dans Tier 1 ?

---

## Ce qu'on attend

Une recommandation concrète et opinée sur chacune des 6 questions, avec les trade-offs honnêtes.
Prioriser la simplicité pour une petite équipe, mais pas au détriment de la robustesse du pipeline.
