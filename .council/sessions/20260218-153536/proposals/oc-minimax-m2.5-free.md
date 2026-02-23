# Recommandations d'Architecture - Pipeline Survey Cleaner

## Question 1 : Rôle deateur

**Summary:** L'approche l'orchestr séquentielle actuelle est correcte mais le batching Tier 2 est incomplet. Un accumulator avec flush périodique est la solution la plus simple.

**Recommendation:** Implémenter l'**Option B** (accumulator avec flush) — c'est le juste milieu entre complexité et efficacité:

```python
# Pseudo-code à ajouter dans orchestrator.py
tier2_accumulator = []
BATCH_SIZE = 15

for var in pending_vars:
    if var.tier == 1:
        process_tier1(var)
    elif var.tier == 2:
        tier2_accumulator.append(var)
        if len(tier2_accumulator) >= BATCH_SIZE:
            flush_tier2_batch()
    elif var.tier == 3:
        process_tier3(var)

# Flush final
if tier2_accumulator:
    flush_tier2_batch()
```

**Pourquoi pas Option A (two-pass):** Ajoute une passe supplémentaire qui n'est pas nécessaire — on peut regrouper par tier pendant la classification initiale.

**Pourquoi pas Option C (event-driven):** Overkill pour une petite équipe. Introduit de la complexité asynchrone non justifiée par le volume.

---

## Question 2 : Classification statique ou LLM-assistée

**Summary:** Le classifier déterministe est suffisant en l'état. Ajouter du LLM maintenant serait de la sur-ingénierie.

**Recommendation:** **Option C** (audit post-classification) — collecter des données avant de complexifier:

1. Logger les décisions de classification dans `status.json` (tier_assigné, confidence, pattern_id)
2. Après 5-10 sondages, auditor 5% des décisions Tier 1 manuellement
3. Si le taux d'erreur > 10%, alors intégrer GLM-5 pour les cas borderline (confidence 0.5-0.79)

**Justification:** 
- GLM-5 est gratuit donc le coût n'est pas le blocker
- Le vrai problème est que vous n'avez pas de données sur les performances réelles
- L'audit vous dira si le classifier est assez bon sans ajouter de la complexité

---

## Question 3 : Validation empirique des patterns

**Summary:** Oui, vale la peine, mais pas 500 variables — commencer avec 100.

**Recommendation:** Faire une "battue" légère:

1. **Échantillonnage:** 100 variables aléatoires (pas 500), stratifié par type de fichier (CSV vs SAV)
2. **Outil:** CSV simple avec colonnes: `var_name, raw_values, codebook_label, classification_auto, classification_manual`
3. **Métrique:** Taux de accord Tier 1 (classifier vs humain)
4. **Seuil:** Si Tier 1 réel > 50%, les patterns sont OK. Si < 40%, creuser.

**Temps estimé:** 1 jour (pas 2-4), car:
- 100 variables c'est 1h de classification manuelle
- 1h d'analyse des écarts
- 2h de corrections si needed

**Sous-question C:** Le seuil de 60% est arbitraire. Avec GLM-5 gratuit, visez 40% — en dessous, ça vaut le coup d'optimiser.

---

## Question 4 : Stratégie de nommage

**Summary:** Le mixed-mode actuel crée de l'incohérence. Utiliser le label du codebook comme base pour tous les tiers.

**Recommendation:** **Option C hybrid:**

- **Tier 1:** Utiliser `var_label` du codebook → snake_case → préfixe selon pattern_type
  - Ex: "Satisfaction envers le gouvernement" → `ses_satisfaction_gouvernement`
- **Tier 2:** Garder le nommage LLM (il suit déjà la convention)
- **Tier 3:** Garder le nommage LLM

**Implémentation:** Ajouter une fonction `_normalize_label_to_var_name()` dans `pattern_engine/rule_generator.py`:

```python
def _normalize_label_to_var_name(label: str, pattern_type: str) -> str:
    # Enlever punctuation, lowercase, snake_case
    base = re.sub(r'[^a-zA-Z0-9\s]', '', label)
    base = '_'.join(base.lower().split())[:20]
    prefix = {'demographic': 'ses_', 'likert': 'op_', 'binary': 'op_'}.get(pattern_type, 'op_')
    return f"{prefix}{base}"
```

**Pourquoi pas B (LLM pour tous):** Cout supplémentaire (même si minime), ajoute une dépendance au LLM pour une tâche simple.

---

## Question 5 : Validation dans le pipeline

**Summary:** Connecter d'abord le validateur existant avant d'ajouter du LLM.

**Recommendation:**

**Sous-question A:** Validation en **deux temps**:
1. **Après assemblage final du clean.py** — une passe complète (plus simple, moins de retries)
2. Si validation échoue → logs détaillés pour audit manuel

**Pourquoi pas après chaque variable:** Le validateur dynamique (types, ranges) nécessite le DataFrame complet. Faire tourner la validation complète à chaque variable est inefficace.

**Sous-question B:** **Option Non-LLM d'abord:**
- Brancher le validateur statique (AST) déjà existant
- Le validateur dynamique est déjà là, juste pas utilisé

**Quand ajouter LLM-light:** Seulement si le validateur statique/dynamique montre > 20% d'échecs Tier 1. À ce moment-là, faire une passe LLM de vérification sémantique sur les échecs uniquement.

---

## Question 6 : Escalade de tier

**Summary:** Implémenter l'escalade automatique mais avec guardrails simples.

**Recommendation:**

**A) Automatic avec seuil:** 
- Escalade automatique si validation échoue
- **Mais:** Si confidence Tier 1 < 0.85, envoyer directement en Tier 2 sans passer par Tier 1 (économie d'un aller-retour)

**B) Info à transmettre:**
```python
escalation_context = {
    'reason': 'validation_failed',
    'error_details': validation_error.message,
    'generated_code': failed_code,
    'confidence_original': 0.82
}
```

**C) Prévention boucles:**
- **Max 1 escalation par variable** (Tier 1 → Tier 2, pas plus)
- Si Tier 3 échoue → `needs_review = True`, pas d'escalade

**D) Augmenter le seuil:** 
- **Non** — garder à 0.8
- L'escalade automatique résout le problème des faux positifs sans limiter les vrai positifs

**Implémentation:**
```python
def process_with_escalation(var, tier, context=None):
    code = generate_code(var, tier, context)
    if not validate(code):
        if tier == 1:
            return process_with_escalation(var, 2, {'escalated_from': 1, 'reason': 'validation_failed'})
        elif tier == 2:
            return process_with_escalation(var, 3, {'escalated_from': 2, 'reason': 'validation_failed'})
        else:
            return {'status': 'needs_review', 'code': code, 'error': validation_error}
    return {'status': 'ok', 'code': code}
```

---

## Priorisation pour une petite équipe

| Priorité | Action | Effort |
|----------|--------|--------|
| 1 | Connecter le validateur existant (Q5) | 2h |
| 2 | Implémenter accumulator Tier 2 (Q1) | 4h |
| 3 | Audit 100 variables (Q3) | 1 jour |
| 4 | Améliorer nommage Tier 1 (Q4) | 2h |
| 5 | Ajouter escalade automatique (Q6) | 4h |
| 6 | Audit classification LLM (Q2) | Si Q3 montre des problèmes |
