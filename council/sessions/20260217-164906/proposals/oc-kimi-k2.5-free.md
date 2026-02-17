**Summary**

L'approche hybride (C) est la seule viable économiquement. Investissez 2-3 jours pour construire une pattern library déterministe qui traitera 65-70% des variables à 0 token, et utilisez les modèles gratuits (GLM-5, Kimi K2.5) pour les cas complexes. Cible réaliste : **$2-4 par sondage** au lieu de $38.

---

**Recommendation**

**Architecture : Pipeline hybride à 3 niveaux**

```
Survey → Classifier → [Règles (70%) | Batch LLM (25%) | LLM individuel (5%)] → Validate → clean.py
```

**1. Pattern Library Déterministe (Niveau 1 - 70% des variables)**

Construisez un système de règles qui capture les patterns récurrents :
- **Pattern matching** : Regex sur les noms (Q*_age → demographics), valeurs uniques (1-5 avec labels Likert), distributions
- **Standardisation automatique** : Mapping déterministe vers vos conventions de nommage (ses_*, dv_*, etc.)
- **Exemples de patterns** :
  - `^[Qq].*province.*` → `ses_province` avec mapping {1: 'qc', 2: 'on', ...}
  - Valeurs [1,2,3,4,5] + labels ["Très insatisfait", ...] → Likert 5 points standardisé

**2. Batch LLM pour cas non-standard (Niveau 2 - 25%)**

Pour les variables non reconnues par les règles :
- **Groupez par 15-20 variables** (pas 1 par 1)
- **Prompt structuré** : JSON schema avec exemples, pas de Markdown verbeux
- **Modèles gratuits via opencode zen** : GLM-5 ou Kimi K2.5 sont suffisants pour cette tâche structurée
- **Output JSON strict** : forcez un format machine-readable pour parsing fiable

**3. LLM individuel pour edge cases (Niveau 3 - 5%)**

Variables complexes/codebook ambigu :
- Traitement individuel avec modèle gratuit
- Flag pour review humaine si confidence < 0.8

**Gestion du Codebook**

- **Extraction structurée** : Convertissez le codebook en JSON schema dès l'entrée, pas Markdown dans le prompt
- **Embeddings légers** : Si besoin de matching sémantique (variable Q5 correspond à quelle entrée du codebook?), utilisez des embeddings locaux (sentence-transformers) pas de vector DB complexe

**Autonomie**

State machine simple avec fichier `surveys/{id}/status.json` :
```json
{
  "stage": "cleaning",
  "current_batch": 3,
  "completed": ["var1", "var2", ...],
  "failed": [],
  "retry_count": 0
}
```

Le script reprend automatiquement là où il s'est arrêté.

---

**Trade-offs**

| Approche | Coût/sondage | Dév initial | Qualité | Maintenance |
|----------|--------------|-------------|---------|-------------|
| A. API directe (actuel) | $38 | 1 jour | Élevée | Moyenne |
| **C. Hybride (recommandé)** | **$2-4** | **3 jours** | **Bonne** | **Faible** |
| D. 100% déterministe | $0.50 | 2 semaines | Faible | Élevée |

**Risques de l'hybride** :
- Besoin d'une phase d'apprentissage initiale pour enrichir la pattern library
- Edge cases peuvent échapper au système → nécessite validation humaine périodique
- Moins flexible que LLM pur pour des patterns totalement nouveaux

---

**Implementation Sketch**

**Semaine 1 : Infrastructure**
```bash
# Créer le classifier
surveys/
  classifier.py      # Pattern matching + règles
  llm_batch.py       # Appels batch aux modèles gratuits
  validator.py       # Validation des outputs
  status.py          # Gestion d'état
```

**Semaine 2 : Pattern Library**
```python
# patterns/demographics.py
PATTERNS = [
    {
        'regex': r'[Qq].*province.*',
        'output_name': 'ses_province',
        'type': 'categorical',
        'value_map': {1: 'qc', 2: 'on', 3: 'bc', ...}
    },
    # ... autres patterns
]
```

**Workflow final** :
1. `python surveys/orchestrator.py <survey_id>` → charge status.json
2. Classifier analyse chaque variable, assigne niveau 1/2/3
3. Exécute niveau 1 (instantané), batch niveau 2, individuel niveau 3
4. Génère clean.py à partir des résultats
5. Met à jour status.json

**Choix technique concret** :
- **Modèles** : GLM-5 via opencode zen (gratuit) pour tous les appels LLM
- **Batch size** : 15-20 variables par appel pour niveau 2
- **Fallback** : Si modèle gratuit échoue 3x, bascule sur Claude Haiku (pas Sonnet)
- **Validation** : Script de test qui vérifie que clean.py s'exécute sans erreur et produit les bonnes colonnes

**Estimation réaliste pour 84 variables** :
- 60 variables × $0 (règles) = $0
- 20 variables × 1 batch × $0.05 (modèle gratuit via opencode, coût négligeable) = ~$0.10
- 4 variables × $0.10 (edge cases) = ~$0.40
- **Total : $0.50-2.00 par sondage** (vs $38 actuel)

L'investissement initial de 3 jours sera amorti dès le 2ème sondage.
