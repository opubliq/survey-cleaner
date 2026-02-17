# Critique des Propositions

## Points de Consensus

1. **Approche hybride (C)** : Toutes les propositions converges vers une stratégie hybride règles + LLM
2. **Modèles gratuits** : GLM-5, Kimi K2.5, Minimax sont jugés suffisants
3. **Codebook JSON** : Convertir le codebook en JSON structuré une fois
4. **Batching** : Éviter 1 appel/variable

## Divergences Clés

| Sujet | Position A | Position B |
|-------|------------|------------|
| Granularité LLM | 1 appel complet (oc-big-pickle) | Tiers structurés (zai-glm-4.7) |
| Déterminisme | 70% règles, 30% LLM | 50% règles, 50% LLM |
| Estimation coût | ~$0.05-0.10 | $4-7 |

## Faiblesses par Proposition

| Proposal | Weakness |
|----------|----------|
| anth-claude-opus | **Trop optimiste sur le $0.50** - suppose que le parsing codebook est trivial |
| anth-claude-sonnet | Complexe avec 3 tiers, maintenance élevée |
| oc-big-pickle | **CRITIQUE**: 1 appel pour 80 variables = risque de failure complete. Si le modèle hallucine, tout est à retry |
| zai-glm-4.7 | 2 semaines d'investissement upfront, sous-estime la complexité du pattern matching |
| oc-glm-5-free | Meilleure estimation ($0.05-0.10) mais忽略了 le risque de qualité des modèles gratuits |

## Mon Top Pick: **oc-glm-5-free**

理由:
1. **Estimation réaliste**: $0.05-0.10/survey est atteignable avec free models
2. **Architecture simple**: 3 stages clairs (parse → classify → generate)
3. **Validation intégrée**: Propose une couche validation pour catches les erreurs
4. **Trade-offs honnêtes**: Admets le risque de 5-10% d'erreurs

**Alternative**: Si oc-glm-5-free échoue sur la qualité, **zai-glm-4.7-flash** avec batch de 10-15 (pas 80) comme fallback.

Le problème critique avec oc-big-pickle: un seul appel pour 80 variables est une **single point of failure**. Si le modèle rate 5 variables, tu dois retry tout le batch. Batch de 15-20 est plus pragmatique.
