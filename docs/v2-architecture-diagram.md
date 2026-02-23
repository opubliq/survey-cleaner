# Architecture Survey Cleaner v2

## Vue d'ensemble du Flux de Traitement

```mermaid
flowchart TB
    subgraph INPUT["📥 DONNÉES D'ENTRÉE"]
        direction TB
        A1["_SharedFolder_data_produit/"]
        A2["sondage_exemple/"]
        A3["data.csv<br/>codebook.pdf"]
    end

    subgraph ORCH["⚙️ ORCHESTRATEUR v2"]
        O1["orchestrator.py"]
    end

    subgraph PREP["📋 PHASE 1: PRÉPARATION"]
        direction LR
        P1["1. Codebook Parser<br/>PDF/Excel → JSON structuré"]
        P2["2. Pattern Classifier<br/>Analyse stats (min/max/unique)"]
        P3["3. Pattern Matcher<br/>Matching signature-based"]
    end

    subgraph PATTERN["🔍 PATTERN ENGINE"]
        direction TB
        PL["pattern_library.json<br/>(patterns partagés)"]
        subgraph PATTERNS["Patterns"]
            L1["likert_scales<br/>(3/4/5/7 points)"]
            D1["demographics<br/>(age, sexe, province)"]
            B1["binary<br/>(oui/non, 0/1)"]
            S1["scales<br/>(0-10, thermomètres)"]
        end
    end

    subgraph LLM["🧠 PROCESSEURS LLM (3-TIERS)"]
        direction TB
        subgraph T1["Tier 1: Validation"]
            T1A["tier1_validator.py<br/>Kimi/GLM-5"]
            T1B["Validate règles générées"]
        end
        subgraph T2["Tier 2: Batch"]
            T2A["tier2_batch.py<br/>GLM-5/GLM-4.7"]
            T2B["Variables semi-standards"]
        end
        subgraph T3["Tier 3: Individual"]
            T3A["tier3_individual.py<br/>Claude Haiku"]
            T3B["Variables complexes<br/>cas spécial"]
        end
    end

    subgraph VALID["✅ COUCHE VALIDATION"]
        V1["validator.py<br/>(syntaxe, range, types)"]
        V2["quality_reporter.py<br/>(rapport qualité)"]
        V3["conflict_resolver.py"]
    end

    subgraph OUTPUT["📤 SORTIE"]
        O2["surveys/sondage/clean.py"]
        O3["processed/data_cleaned.csv"]
        O4["processed/codebook.json<br/>(metadata + labels)"]
    end

    A1 --> A2 --> A3
    A3 --> O1
    O1 --> PREP
    PREP --> PATTERN
    PATTERN --> LLM
    LLM --> VALID
    VALID --> OUTPUT
    O1 -.->|génère| O4

    style INPUT fill:#e3f2fd,stroke:#1976d2
    style ORCH fill:#fff3e0,stroke:#f57c00
    style PREP fill:#e8f5e9,stroke:#388e3c
    style PATTERN fill:#f3e5f5,stroke:#7b1fa2
    style LLM fill:#ffebee,stroke:#c62828
    style VALID fill:#fff8e1,stroke:#fbc02d
    style OUTPUT fill:#e0f2f1,stroke:#00796b
```

---

## Exemple: Sondage Fictif "satisfaction_employes_2024"

### Données d'entrée

```mermaid
flowchart LR
    subgraph INPUT_DATA["Données: satisfaction_employes_2024"]
        D1["data.csv (500 lignes)"]
        D2["codebook.docx"]
    end
    
    subgraph VARIABLES["12 Variables"]
        V1["Q1: Âge (1-100)"]
        V2["Q2: Sexe (1=H, 2=F, 3=Autre)"]
        V3["Q3: Province (1-10)"]
        V4["Q4: Satisfaction 1-5 (Likert)"]
        V5["Q5: Recommandation 0-10"]
        V6["Q6: Oui/Non (1/2)"]
    end

    D1 --> VARIABLES
    D2 --> VARIABLES
```

### Phase 1: Parsing & Classification

```mermaid
flowchart LR
    subgraph CODEBOOK_PARSER["1. Codebook Parser"]
        CP1["codebook.docx<br/>↓<br/>codebook.json"]
        CP2["{&quot;Q1&quot;:{&quot;label&quot;:&quot;Âge&quot;,&quot;values&quot;:{...}}}"]
    end

    subgraph PATTERN_CLASSIFIER["2. Pattern Classifier (Data-Driven)"]
        PC1["Analyse statistics"]
        PC2["min=1, max=100<br/>→ numeric"]
        PC3["unique=3<br/>→ categorical"]
        PC4["min=1, max=5<br/>→ likert_5"]
    end

    CP1 --> CP2 --> PC1
    PC1 --> PC2 & PC3 & PC4
```

**Exemple de résultat:**
| Variable | Stats | Pattern Détecté |
|----------|-------|-----------------|
| Q1_age | min=18, max=85 | `numeric` → Match: `demographics.age` |
| Q2_sexe | unique=3 | `categorical` → Match: `demographics.gender` |
| Q3_province | unique=10 | `categorical` → Match: `demographics.province` |
| Q4_satisfaction | min=1, max=5 | `likert_5` → Match: `likert_scales.agreement_5` |
| Q5_recommendation | min=0, max=10 | `scale_0_10` → Match: `scales.nps` |
| Q6_aval_entreprise | unique=2 | `binary` → Match: `binary.yes_no` |

### Phase 2: Génération des Règles via Patterns

```mermaid
flowchart TB
    subgraph RULE_GEN["Rule Generator"]
        RG1["Pattern + Codebook<br/>↓<br/>Règles Python"]
    end

    subgraph EXAMPLE["Exemple: Q4_satisfaction"]
        E1["Pattern: likert_scales.agreement_5"]
        E2["Codebook: 1=Très insatisfait<br/>2=Insatisfait<br/>3=Neutre<br/>4=Satisfait<br/>5=Très satisfait"]
        E3["↓ Génère"]
        E4["```python<br/>df['op_satisfaction'] = df['Q4'].map({<br/>    1.0: 0.0,<br/>    2.0: 0.25,<br/>    3.0: 0.5,<br/>    4.0: 0.75,<br/>    5.0: 1.0<br/>})<br/>```"]
    end

    RG1 --> E1 & E2
    E1 --> E3
    E2 --> E3
    E3 --> E4
```

### Phase 3: Routage LLM 3-Tiers

```mermaid
flowchart TB
    subgraph ROUTING["Tier Routing"]
        R1{"Type de variable?"}
        R2["Match pattern?<br/>→ règles claires"]
        R3["Cas spécial?<br/>→ borderline"]
        R4["Complexe?<br/>→ edge case"]
    end

    subgraph TIER1["Tier 1: Validation (Gratuit/Economic)"]
        T1A["Kimi/GLM-5"]
        T1B["Valide les règles<br/>générées par patterns"]
        T1C["```json<br/>{&quot;valid&quot;: true,<br/> &quot;confidence&quot;: 0.95}<br/>```"]
    end

    subgraph TIER2["Tier 2: Batch (Semi-auto)"]
        T2A["GLM-5/GLM-4.7"]
        T2B["Traite 5-10 variables<br/>similaires ensemble"]
        T2C["Prompt cache<br/>codebook + patterns"]
    end

    subgraph TIER3["Tier 3: Individual (Complexe)"]
        T3A["Claude Haiku"]
        T3B["Variables difficiles<br/>cas edge"]
        T3C["Coût plus élevé<br/>mais nécessaire"]
    end

    R1 --> R2 & R3 & R4
    R2 --> TIER1
    R3 --> TIER2
    R4 --> TIER3
```

### Exemple de Routing pour notre sondage:

```mermaid
flowchart LR
    subgraph ROUTING_EX["Routage réel: satisfaction_employes_2024"]
        direction TB
        RE1["✅ Tier 1 (8 vars)<br/>Q1_age, Q2_sexe, Q3_province<br/>Q4_satisfaction, Q5_recommendation<br/>Q6_aval, Q7_entendu, Q8_anciennete"]
        RE2["⚡ Tier 2 (3 vars)<br/>Q9_commentaires (texte libre)<br/>Q10_ameliorations (texte)<br/>Q11_conseils (texte)"]
        RE3["🔧 Tier 3 (1 var)<br/>Q12_satisfaction_globale<br/>(scale inhabituelle 1-7 + texte)"]
    end

    style RE1 fill:#c8e6c9,stroke:#388e3c
    style RE2 fill:#fff9c4,stroke:#f9a825
    style RE3 fill:#ffcdd2,stroke:#c62828
```

### Phase 4: Validation & Nettoyage

```mermaid
flowchart LR
    subgraph VALIDATION["Validation Layer"]
        V1["Syntax Check<br/>Python valide?"]
        V2["Range Check<br/>valeurs 0-1?"]
        V3["Type Check<br/>float?"]
        V4["Conflict Check<br/>doublons?"]
    end

    subgraph EXECUTION["Exécution & Vérification"]
        E1["Exécute transformation<br/>sur données brutes"]
        E2["Compare freq raw vs cleaned<br/>Affichage visuel"]
        E3["Approve/Reject"]
    end

    V1 --> V2 --> V3 --> V4 --> E1
    E1 --> E2 --> E3
```

**Exemple de validation Q4_satisfaction:**

```
Avant (raw):          Après (cleaned):
1: 45 (9%)     →     0.0: 45 (9%)    [Très insatisfait]
2: 78 (16%)    →     0.25: 78 (16%)  [Insatisfait]
3: 120 (24%)   →     0.5: 120 (24%)  [Neutre]
4: 156 (31%)   →     0.75: 156 (31%) [Satisfait]
5: 101 (20%)   →     1.0: 101 (20%)  [Très satisfait]

✅ Validation passed!
```

### Phase 5: Sortie Finale

```mermaid
flowchart TB
    subgraph OUTPUT_STRUCTURE["Structure de Sortie"]
        O1["surveys/satisfaction_employes_2024/"]
        O2["├── clean.py              # Script nettoyeur"]
        O3["├── VARIABLE_METADATA    # Labels pour LLMs"]
        O4["└── processed/"]
        O5["    ├── data_cleaned.csv  # Données nettoyées"]
        O6["    └── codebook.json    # Codebook standardisé"]
    end

    subgraph CLEAN_PY["clean.py (extrait)"]
        CP["```python<br/>VARIABLE_METADATA = {<br/>  'ses_age': {<br/>    'original': 'Q1',<br/>    'type': 'numeric'<br/>  },<br/>  'op_satisfaction': {<br/>    'original': 'Q4',<br/>    'type': 'likert_5',<br/>    'labels': {<br/>      0.0: 'Très insatisfait',<br/>      1.0: 'Très satisfait'<br/>    }<br/>  }<br/>}<br/><br/>def clean_data(df):<br/>  df_clean = pd.DataFrame()<br/>  df_clean['ses_age'] = df['Q1']<br/>  df_clean['op_satisfaction'] = ...<br/>  return df_clean<br/>```"]
    end

    subgraph CODEBOOK_JSON["codebook.json (généré)"]
        CJ["```json<br/>{<br/>  &quot;survey_id&quot;: &quot;satisfaction_2024&quot;,<br/>  &quot;variables&quot;: {<br/>    &quot;ses_age&quot;: {<br/>      &quot;original&quot;: &quot;Q1&quot;,<br/>      &quot;label&quot;: &quot;Âge&quot;,<br/>      &quot;type&quot;: &quot;numeric&quot;<br/>    },<br/>    &quot;op_satisfaction&quot;: {<br/>      &quot;original&quot;: &quot;Q4&quot;,<br/>      &quot;label&quot;: &quot;Satisfaction&quot;,<br/>      &quot;type&quot;: &quot;likert_5&quot;,<br/>      &quot;scale&quot;: [0, 1],<br/>      &quot;labels&quot;: {<br/>        &quot;0.0&quot;: &quot;Très insatisfait&quot;,<br/>        &quot;0.25&quot;: &quot;Insatisfait&quot;,<br/>        &quot;0.5&quot;: &quot;Neutre&quot;,<br/>        &quot;0.75&quot;: &quot;Satisfait&quot;,<br/>        &quot;1.0&quot;: &quot;Très satisfait&quot;<br/>      }<br/>    }<br/>  }<br/>}<br/>```"]
    end

    O1 --> O2 & O3 & O4
    O4 --> O5 & O6
```

---

## Résumé du Flux v2

```mermaid
sequenceDiagram
    participant U as Utilisateur
    participant O as Orchestrator
    participant CP as Codebook Parser
    participant PC as Pattern Classifier
    participant PM as Pattern Matcher
    participant RG as Rule Generator
    participant LLM as LLM Processors (1/2/3)
    participant V as Validator
    participant OUT as Output

    U->>O: python orchestrator.py satisfaction_2024
    
    O->>CP: Parse codebook.pdf → JSON
    CP-->>O: codebook.json
    
    O->>PC: Analyse stats chaque variable
    PC-->>O: {Q1: numeric, Q4: likert_5, ...}
    
    O->>PM: Match patterns
    PM-->>O: {Q1: demographics.age, Q4: likert_scales.agreement_5}
    
    O->>RG: Génère règles Python
    RG-->>O: {Q1: df['ses_age'] = df['Q1'], Q4: df['op_sat'] = df['Q4'].map({...})}
    
    O->>LLM: Tier 1 validation
    LLM-->>O: {valid: true, confidence: 0.95}
    
    O->>V: Validate transformations
    V-->>O: ✅ All passed
    
    O->>OUT: Generate clean.py + processed/
    OUT-->>U: ✅ Sondage nettoyé!
```

---

## Métriques Attendues (v2)

| Métrique | Valeur |
|----------|--------|
| Tokens/sondage | ~25K |
| Coût/sondage | ~$0.008 |
| Temps/sondage | ~4 min |
| Couverture patterns | 80% auto |
