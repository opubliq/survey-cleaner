# Critique des Propositions d'Architecture

## Vue d'ensemble des propositions

Toutes les propositions convergent vers une **approche hybride (C)** avec variations sur:
- Le degré de déterminisme (65-70% de règles)
- La granularité des appels LLM (batch vs individuel)
- Le choix des modèles (gratuits vs payants)
- L'importance accordée à l'extraction structurée du codebook

---

## Analyse par proposition

### 1. anth-claude-opus (Approche D pure)

**Forces:**
- Vision claire du coût cible (<$0.50/sondage)
- Architecture à 3 phases bien définies
- Insistance sur la reproductibilité et le débogage

**Faiblesses:**
- Sous-estime la complexité des codebooks réels (PDF non structurés, formats variables)
- Néglige le coût caché de maintenance des templates Jinja2
- "Edge cases" à 10% peuvent en réalité être 30-40% sur des sondages atypiques

**Angle mort:**
- Ne traite pas la question de la validation qualité automatisée
- Ignore le coût de développement initial (estime 2-3 jours, probablement 1-2 semaines)

---

### 2. anth-claude-sonnet (D+C hybride)

**Forces:**
- Diagnostic correct sur l'échec du caching (prompt dynamique)
- Stratégie de fallback élégante
- Analyse des coûts réaliste par tier

**Faiblesses:**
- Classification Type A/B/C trop optimiste (65/25/10%)
- Ne propose pas de mécanisme d'apprentissage des échecs
- Sous-estime la difficulté de la "validation déterministe"

**Angle mort:**
- Le classifier Python "gratuit" nécessite un entraînement/maintien coûteux
- Ne mentionne pas la gestion des versions du pattern library

---

### 3. google-gemini-2.5-flash (C hybride)

**Forces:**
- Reconnaissance du coût d'extraction initiale du codebook
- Vision à long terme avec testing rigoureux
- Intégration avec l'existant (orchestrator.py)

**Faiblesses:**
- Architecture trop complexe pour une "petite équipe"
- Néglige la latence des appels batch (temps d'attente cumulé)
- Sous-estime la difficulté de parser des codebooks PDF/PPTX

**Angle mort:**
- Le "comprehensive testing" proposé est irréaliste en pratique
- Pas de stratégie de rollback si le batch échoue

---

### 4. oc-big-pickle (Batch unique)

**Forces:**
- Insight puissant: "1 appel pour tout le survey"
- Simplicité radicale de l'approche
- Réduction drastique de l'overhead (2200 tokens/variable)

**Faiblesses:**
- **FAILLE CRITIQUE:** Batch de 80 variables = échec catastrophique si l'output est invalide
- GLM-5 gratuit peu fiable pour 80 variables complexes
- Pas de mécanisme de retry granulaire
- Validation "humaine" proposée = non-autonome

**Angle mort:**
- Ignore complètement la contrainte d'autonomie ("presque pas de babysitting")
- Le coût de retry complet est identique au coût initial

---

### 5. oc-glm-5-free (3-Stage Pipeline)

**Forces:**
- Équilibre coût/qualité bien pensé
- Stratégie de fallback claire
- Estimation réaliste des proportions par tier

**Faiblesses:**
- 3 semaines de développement = trop long pour valider rapidement
- "Validation catches >90% of errors" = métrique irréaliste
- Dépendance forte aux modèles gratuits (risque de disponibilité)

**Angle mort:**
- Ne traite pas la variabilité des formats de codebook
- Le pattern library demande une expertise métier importante

---

### 6. oc-kimi-k2.5-free (Pipeline 3 niveaux)

**Forces:**
- State machine simple pour l'autonomie
- Embeddings locaux suggérés (bonne idée pour matching sémantique)
- Focus sur la reprise sur erreur

**Faiblesses:**
- Pattern library à "enrichir" = dette technique cachée
- 70% en règles = surestimation (tester sur 3-5 sondages d'abord)
- Le state machine JSON ajoute de la complexité

**Angle mort:**
- Les embeddings locaux nécessitent des ressources GPU/CPU
- Pas de discussion sur le coût de stockage des patterns

---

### 7. oc-minimax-m2.5-free (Hybride batch)

**Forces:**
- Recommandation pragmatique de tester en 2-3 heures
- Batch par type = bon compromis
- LLM gateway = abstraction utile

**Faiblesses:**
- Minimax M2.5 peu documenté/testé
- "15 variables Likert" = hypothèse forte sur la distribution
- Pas de mécanisme de validation automatique

**Angle mort:**
- Sous-estime la variété des types de variables
- Le "batch par type" suppose une classification parfaite en amont

---

### 8. zai-glm-4.5 (C+ Enhanced)

**Forces:**
- Pattern library builder avec apprentissage historique
- 3-tier processing bien structuré
- Validation explicite des outputs

**Faiblesses:**
- 2-3 semaines de dev = trop long
- GLM-4.5 pour validation = surcoût inutile
- "Self-improving" = feature complexe non prioritaire

**Angle mort:**
- L'analyse des 57 sondages existants est un projet en soi
- Ne précise pas comment gérer les conflits de patterns

---

### 9. zai-glm-4.7-flash (Hybrid + bootstrap)

**Forces:**
- Bootstrap extraction JSON = bonne idée
- Pattern library auto-populée
- Coût réaliste ($1.50-2.00)

**Faiblesses:**
- 30% en LLM = surestimation (peut-être 50%)
- GLM-4.7 à $0.005/var = coût qui s'accumule
- "Pattern library grows" = dette technique

**Angle mort:**
- Ne traite pas la question du "cold start" (premiers sondages)
- La mise à jour auto du pattern library peut introduire des erreurs

---

### 10. zai-glm-4.7 (3-Tier Strategy)

**Forces:**
- Architecture la plus complète et réfléchie
- Pattern library minimal viable (MVP)
- Stratégie de fallback graduée
- Discussion honnête des trade-offs

**Faiblesses:**
- 2 semaines = sous-estimation (probablement 3-4 semaines)
- 50% Tier 1 = optimiste sans données historiques
- Claude Sonnet à 20% = encore trop cher

**Angle mort:**
- Ne mentionne pas la maintenance du pattern library
- La "sampling validation" à 10% = coût humain caché

---

## Points de consensus

Tous les architectes s'accordent sur:

1. **L'approche actuelle ($38/sondage) est intenable**
2. **Le hybride règles+LLM est la seule voie viable**
3. **L'extraction structurée du codebook (JSON) est nécessaire**
4. **Les modèles gratuits sont suffisants pour 60-80% des tâches**
5. **Le batching est essentiel pour réduire les coûts**
6. **Le pattern library est un investissement rentable à long terme**

---

## Désaccords clés

### 1. Granularité optimale des appels LLM
- **Batch total (80 vars)** : big-pickle, GLM-4.7-flash
- **Batch partiel (10-20 vars)** : Sonnet, GLM-5-free, GLM-4.5
- **Individuel avec caching** : Aucun ne le recommande plus

**Mon inclinaison:** Batch de 10-15 variables. Batch total trop risqué, individuel trop cher.

### 2. Degré de déterminisme
- **70% règles / 30% LLM** : Sonnet, GLM-5-free, Kimi K2.5
- **50% règles / 50% LLM** : GLM-4.7 (plus prudent)
- **Presque 100% règles** : Opus (trop optimiste)

**Mon inclinaison:** Commencer à 40% règles / 60% LLM, viser 60/40 après 10 sondages.

### 3. Modèle pour le parsing du codebook
- **Gratuit (GLM-5, Kimi)** : big-pickle, GLM-5-free, Kimi K2.5
- **Payant cheap (Haiku)** : Sonnet
- **Payant premium (Sonnet)** : Gemini 2.5 (trop cher)

**Mon inclinaison:** Gratuit d'abord, fallback Haiku si qualité <80%.

### 4. Temps de développement initial
- **2-3 jours** : Opus (irréaliste)
- **1-2 semaines** : Sonnet, GLM-4.7-flash
- **2-3 semaines** : GLM-5-free, GLM-4.5, GLM-4.7

**Mon inclinaison:** 1 semaine pour MVP, 3 semaines pour système robuste.

---

## Propositions avec failles critiques

### oc-big-pickle (Batch unique de 80 vars)
**Problème:** Si l'appel échoue ou produit un output invalide, on doit tout recommencer. Aucune granularité de retry. Non viable pour l'autonomie requise.

---

## Mon choix final

**zai-glm-4.7 (3-Tier Strategy)** avec modifications:

### Pourquoi cette proposition?

1. **Architecture pragmatique:** Le 3-tier (pattern/free/paid) est la bonne abstraction
2. **Pattern library MVP:** Commencer petit, itérer (vs GLM-4.5 qui veut tout analyser)
3. **Estimation de coût réaliste:** $1-3/sondage est atteignable
4. **Discussion honnête:** Reconnaît les 2 semaines de dev et les limitations

### Modifications recommandées:

1. **Démarrer à 40% règles, pas 50%** - Valider sur 3-5 sondages d'abord
2. **Utiliser GLM-5 gratuit pour Tier 2 et 3** - Tester avant de payer
3. **Batch de 15 variables max** - Équilibre entre coût et granularité de retry
4. **Ajouter un mécanisme de feedback** - Flag les échecs pour enrichir les patterns
5. **Validation humaine échantillon** - 5-10 variables par sondage, pas 10%

### Plan d'action modifié:

**Semaine 1:**
- Analyser 3 sondages existants pour identifier patterns
- Construire pattern library avec 5 patterns simples
- Implémenter orchestrateur avec routing 3-tier

**Semaine 2:**
- Tester sur 5 nouveaux sondages avec GLM-5 gratuit
- Mesurer taux de succès par tier
- Ajuster proportions et patterns

**Semaine 3 (si nécessaire):**
- Implémenter fallback Haiku pour échecs
- Ajouter validation automatisée basique
- Documenter patterns pour maintenance

**Coût cible réaliste:** $0.50-2.00/sondage (vs $38 actuel, 95% de réduction)

---

**Verdict:** zai-glm-4.7 offre le meilleur équilibre entre ambition technique et pragmatisme, avec une roadmap réaliste pour une petite équipe.
