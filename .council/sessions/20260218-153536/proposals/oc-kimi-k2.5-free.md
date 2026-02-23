**Summary:** L'orchestrateur actuel traite les variables séquentiellement, ce qui empêche le batching Tier 2 d'opérer efficacement. La classification déterministe à 100% est pragmatique pour l'instant. La validation non connectée est un risque majeur. Je recommande la structure deux-passes (Option A) avec activation immédiate du vrai batching, maintien de la classification stat-only (Option A), et connexion de la validation non-LLM dès maintenant.

---

## Q1 — Structure de l'orchestrateur : Option A (Deux passes)

**Recommandation:** Séparer explicitement en deux passes — (1) classification de toutes les variables, (2) traitement par tier avec vrai batching Tier 2.

L'orchestrateur actuel (`orchestrator.py:517-559`) traite les variables une par une, créant un batch de 1 variable pour Tier 2. Le `Batcher` existe mais n'est pas utilisé. La solution la plus simple est de modifier `run()` pour :

1. **Passe 1** (lignes 495-500): Classifier toutes les variables → dictionnaire `var_name → (tier, pattern, confidence)`
2. **Passe 2**: Grouper par tier et traiter :
   - Tier 1: boucle simple (déjà instantané)
   - Tier 2: utiliser `create_batches()` avec `batch_size=15`, puis `process_tier2_batch()` par lot
   - Tier 3: boucle individuelle

**Trade-offs:**
- **+** Structure claire, testable, résume l'état entre les passes
- **+** Le vrai batching réduit les appels API de 40× (15 vars/appel vs 1)
- **−** Nécessite de charger toutes les métadonnées en mémoire (acceptable pour 500-2000 variables)

**Implementation sketch:**
```python
def run(self):
    # Passe 1: Classification
    classified = self._classify_all(df)
    
    # Passe 2: Traitement par tier
    tier1_vars = [v for v, c in classified.items() if c.tier == 1]
    tier2_vars = [v for v, c in classified.items() if c.tier == 2]
    tier3_vars = [v for v, c in classified.items() if c.tier == 3]
    
    # Tier 1: synchrone
    for var in tier1_vars:
        self._process_tier1(var, ...)
    
    # Tier 2: vrai batching
    batches = create_batches(tier2_vars, batch_size=15)
    for batch in batches:
        self._process_tier2_batch(batch)
    
    # Tier 3: individuel
    for var in tier3_vars:
        self._process_tier3(var, ...)
```

---

## Q2 — LLM dans la classification : Option A (Statu quo)

**Recommandation:** Garder la classification 100% déterministe. Ne PAS ajouter de LLM dans le chemin critique de classification.

**Rationale:** Le coût d'un faux Tier 1 (code incorrect généré) est absorbé par la validation (une fois connectée). Ajouter GLM-5 pour les cas borderline (0.5-0.79) les enverrait de toute faço&#x303;n en Tier 2, donc aucun gain. L'audit périodique (Option C) peut attendre — priorité absolue: connecter la validation existante.

**Trade-offs:**
- **+** Zéro coût, déterminisme total, pas de latence API dans la classification
- **+** Pas de dépendance LLM pour le 50% Tier 1 (gratuit et rapide)
- **−** Quelques faux Tier 1 possibles → mais la validation les attrapera

---

## Q3 — Optimisation des patterns : Reporter à plus tard

**Recommandation:** NE PAS faire la "battue" de 500 variables maintenant. Attendre d'avoir des métriques réelles de taux Tier 1 sur 5-10 sondages complets.

**Rationale:** GLM-5 est gratuit. Si le taux Tier 1 réel est de 40% au lieu de 50%, le surcoût est négligeable. La battue prend 2-4 jours qui seraient mieux investis dans la connexion de la validation et l'activation du batching.

**Quand agir:** Si après 10 sondages, le taux Tier 1 est < 35% OU si des patterns évidents sont manqués (ex: 20% des variables sont des thermomètres 0-10 non reconnus).

**Métrique à suivre:** `tier1_rate = len(tier1_vars) / total_vars` par sondage, loggué dans `status.json`.

---

## Q4 — Stratégie de nommage : Option C (Codebook labels)

**Recommandation:** Utiliser `var_label` du codebook comme base pour le nommage Tier 1, avec fallback sur le nom brut.

**Implementation:**
```python
def _generate_clean_var_name(self, var_name, var_schema, pattern):
    base = var_schema.var_label if var_schema and var_schema.var_label else var_name
    # Clean: minuscule, snake_case, sans accents
    clean_base = self._slugify(base)[:25]
    
    prefix = "ses_" if pattern.pattern_type == "demographic" else \
             "behav_" if "comportement" in base.lower() or "behavior" in base.lower() else \
             "op_"
    return f"{prefix}{clean_base}"
```

**Trade-offs:**
- **+** Noms lisibles sans coût LLM
- **+** Cohérent entre tiers (Tier 2 utilise déjà le label implicitemment)
- **−** Nécessite un codebook parsé (sinon fallback sur nom brut)

---

## Q5 — Validation : Connecter maintenant, sans LLM

**Recommandation:** Connecter `CleanValidator` à l'orchestrateur immédiatement, après assemblage de `clean.py`. Pas de LLM dans la validation pour l'instant.

**Sous-question A:** Validation en **fin de pipeline uniquement** (pas après chaque variable). Une passe sur le `clean.py` complet est plus efficace et détecte les conflits inter-variables (doublons de noms).

**Sous-question B:** Option **Non-LLM** pour commencer. Le `CleanValidator` existant fait déjà:
- Validation AST (syntaxe Python)
- Détection d'assignations dupliquées
- Vérification des types et ranges

**Implementation sketch:**
```python
# Dans orchestrator.py:565-571, avant écriture du fichier
from surveys.validation.validator import CleanValidator

validator = CleanValidator()
validation_result = validator.validate(clean_py, df_sample)

if not validation_result.is_valid:
    # Log erreurs, marquer variables concernées comme "error"
    # Ne PAS écrire clean.py invalide
    self._handle_validation_errors(validation_result.errors)
    return

# Écrire clean.py seulement si valide
with open(target, "w") as f:
    f.write(clean_py)
```

---

## Q6 — Escalade de tier : Automatique avec circuit-breaker

**Recommandation:** Implémenter l'escalade automatique avec un "circuit-breaker" de 2 tentatives maximum.

**Réponses concrètes:**

**A)** Escalade **automatique** sur échec de validation, sans seuil de confiance intermédiaire. Si Tier 1 échoue la validation, c'est qu'il n'était pas assez sûr.

**B)** Transmettre au tier supérieur:
- Le `reason` de l'échec de validation
- Le code incorrect généré (commenté) pour diagnostic
- La classification originale (pattern, confiance)

**C)** **Circuit-breaker:** Maximum 2 tentatives par variable (Tier 1 → Tier 2 → Tier 3). Si Tier 3 échoue: marquer `needs_review=True`, stocker `# TODO: Manual review needed - {reason}`.

**D)** Garder le seuil à **0.8**. L'escalade gère les faux positifs; augmenter à 0.9 risquerait d'envoyer trop de variables en Tier 2 payant (Claude) inutilement.

**Implementation sketch:**
```python
MAX_ATTEMPTS = 2

def _process_with_escalation(self, var_name, classification, attempt=1):
    try:
        if classification.tier == 1:
            code = self._process_tier1(...)
        elif classification.tier == 2:
            code = self._process_tier2(...)
        else:
            code = self._process_tier3(...)
        
        # Validation
        validation = self._validate_code(code)
        if validation.is_valid:
            return code
        
        # Échec validation → escalade si possible
        if attempt < MAX_ATTEMPTS:
            new_tier = min(classification.tier + 1, 3)
            classification.tier = new_tier
            return self._process_with_escalation(var_name, classification, attempt + 1)
        else:
            return f"# TODO: Manual review needed - {validation.errors[0]}"
            
    except Exception as e:
        # Échec technique → escalade
        if attempt < MAX_ATTEMPTS:
            classification.tier = min(classification.tier + 1, 3)
            return self._process_with_escalation(var_name, classification, attempt + 1)
        raise
```

---

**Priorité d'implémentation:**
1. **Cette semaine:** Connecter la validation non-LLM (Q5)
2. **Semaine prochaine:** Restructurer l'orchestrateur en deux passes avec vrai batching Tier 2 (Q1)
3. **Ensuite:** Implémenter l'escalade automatique (Q6)
4. **Plus tard:** Optimiser le nommage avec codebook labels (Q4) et évaluer les patterns sur données réelles (Q3)
