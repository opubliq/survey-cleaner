# Critique des Propositions

## Points de Consensus

1. **Approche hybride (C)** - Tous s'accordent sur un mélange règles déterministes + LLM
2. **Modèles gratuits d'abord** - GLM-5, Kimi K2.5 ou Minimax comme choix principal
3. **Batching obligatoire** - Grouper les variables (10-20/call) au lieu de 1/variable
4. **Codebook en JSON** - Conversion structurée une fois, réutilisation ensuite

---

## Points de Désaccord

| Sujet | Position A | Position B |
|-------|-----------|------------|
| Investissement initial | Minimal (1-2 jours) | 2-3 semaines (pattern library complète) |
| % déterminisme | 50-60% | 65-70% |
| Modèle gratuit seul | Suffisant | Nécessite fallbackpaid |
| Coût cible | ~$0-0.50/survey | $1-4/survey |

---

## Forces et Faiblesses par Proposition

### anth-claude-opus (Approche D pure)
- **Force**: Architecture claire en 2 phases, coût le plus bas (~0.10$)
- **Faiblesse**: Dépendance forte à la qualité d'extraction JSON initiale
- **Angle mort**: Comment gérer les patterns non-vus sans boucle LLM?

### anth-claude-sonnet 
- **Force**: Explique clairement pourquoi le caching a échoué
- **Force**: Estimation réaliste ($0.13-0.50)
- **Faiblesse**: Trop similaire à opus, moins tranchant

### google-gemini-2.5-flash
- **Force**: Classification A/B/C bien définie
- **Faiblesse**: Estimation $0 réaliste? J'en doute - sous-estime les coûts de validation
- **Angle mort**: Que se passe-t-il si free models produisent 15% d'erreurs?

### oc-big-pickle
- **Force**: Simplicité - un seul batch pour tout
- **Faiblesse**: Un seul failure = tout à recommencer
- **Angle mort**: Risque de dépasser context window

### oc-glm-5-free
- **Force**: Meilleure estimation ($0.05-0.10)
- **Force**: Distribution Type A/B/C claire
- **Faiblesse**: Trop ambitieux sur le coût

### zai-glm-4.7
- **Force**: La plus détaillée - code d'implémentation inclus
- **Force**: 3-tier avec percentages précis
- **Force**: Meilleure couverture des risques

---

## Problème Critique Identifié

**Proposition zai-glm-4.7-flash**: Estimation $0 coût - irréaliste. La validation humaine et les retries ne sont pas comptabilisés. Le true cost sera au minimum $0.50-1.00 même avec free models.

**Tous**: Sous-estiment le coût de la maintenance de la pattern library sur 57+ surveys.

---

## Ma Position

**TOP PICK: zai-glm-4.7 (3-tier hybrid)**

Pourquoi:
1. **Couverture complète** - Définit explicitement Tier 1/2/3 avec pourcentages
2. **Coût réaliste** - $1-3/survey avec fallback paid pour edge cases
3. **Implémentation concrète** - Code provided, pas que de la théorie
4. **Autonomie** - State machine avec status.json
5. **Pattern library** - Structure JSON réutilisable

**Hybride avec refinement**:
- Commencer avec zai-glm-4.7
- Ajouter validation layer plus robuste (sampling 10% minimum)
- Allouer budget pour fallback paid (~5% des variables)

**Coût реальiste**: $1.50-3.00/survey au lieu de $38 - suffit amplement pour 57+ surveys.
