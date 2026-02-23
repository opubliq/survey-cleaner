# Critique Architecturale des Propositions

## Points de Consensus

**Q1 — Batching Tier 2 :** Toutes les propositions reconnaissent que le batching n'est pas activé et doit l'être.

**Q4 — Nommage :** Consensus fort pour utiliser les labels du codebook plutôt que les noms bruts (`Option C`).

**Q5 — Connexion validation :** Validation doit être branchée (actuellement non connectée).

---

## Désaccords Clés

**Q1 — Structure :**
- `oc-kimi-k2.5-free` : Option A (two-pass explicite)
- `google-gemini-2.5-flash`, `oc-minimax-m2.5-free` : Option B (accumulator)
- `oc-big-pickle` : Option B aussi, mais en utilisant `create_batches()` existant

**Q2 — LLM dans classification :**
- `google-gemini-2.5-flash` : Ajouter GLM-5 pour borderline (0.5-0.79)
- Autres : Garder statique (`oc-big-pickle`, `oc-kimi-k2.5-free`) ou audit post-hoc (`oc-minimax-m2.5-free`)

**Q3 — Battue empirique :**
- `oc-kimi-k2.5-free` : Reporter à plus tard
- `oc-minimax-m2.5-free` : 100 variables suffisent
- `google-gemini-2.5-flash`, `oc-big-pickle` : 500 variables avec seuil 60%

**Q5 — Validation timing :**
- `google-gemini-2.5-flash` : Après chaque variable + LLM-light Tier 1
- `oc-big-pickle`, `oc-kimi-k2.5-free`, `oc-minimax-m2.5-free` : En fin de pipeline, sans LLM

---

## Analyse des Forces/Faiblesses

| Proposition | Forces | Faiblesses |
|-------------|--------|------------|
| **google-gemini-2.5-flash** | Complète, détaillée, LLM-light pour Tier 1 (bien!), escalade avec max retries | Complexe (LLM partout), threshold 0.85 arbitraire |
| **oc-big-pickle** | Utilise `create_batches()` existant, connecte validation, restructure bien | Threshold 0.85 sans donnée, battue optionnelle |
| **oc-kimi-k2.5-free** | Two-pass clair, validation en fin (simple), circuit-breaker | Two-pass overkill, reporte battue |
| **oc-minimax-m2.5-free** | Pragmatique, battue légère (100 vars), garde 0.8, priorisation claire | Moins détaillée sur implémentation |

---

## Flaw Critique

**`google-gemini-2.5-flash`** : Trop de LLM dans le pipeline critique (classification + validation). Ajoute de la complexité et de la latence pour un gain marginal — les variables borderline vont de toute façon en Tier 2 (gratuit). C'est de la sur-ingénierie pour une petite équipe.

---

## Mon Top Pick

**`oc-minimax-m2.5-free`** — avec des éléments de **`oc-big-pickle`**.

**Pourquoi :**
1. **Pragmatique** : Commencer par 100 vars pour la battue (pas 500), garder threshold 0.8 car l'escalade absorbe les faux positifs
2. **Priorisation claire** : Connecter validation d'abord, puis batching, puis le reste
3. **Simplicité** : Validation en fin de pipeline, pas de LLM dans le chemin critique classification

**Éléments à intégrer des autres :**
- Utiliser `create_batches()` existant comme propose `oc-big-pickle` (plus propre que l'accumulator manuel)
- La structure two-pass de `oc-kimi-k2.5-free` si l'accumulator devient complexe
- Le LLM-light pour Tier 1 uniquement (post-validation) de `google-gemini-2.5-flash` — mais SEULEMENT si la battue montre un problème réel

**Rationale finale :** Une petite équipe doit éviter la paralysie par analyse. Les données gratuites de GLM-5 justifient une approche conservative : valider empiriquement (100 vars) avant d'ajouter de la complexité. L'escalade automatique + validation connectée résout 80% des problèmes décrits.
