# Surveys - Nettoyage Manuel

Structure pour le nettoyage manuel des sondages en attendant l'automatisation complète.

## Structure d'un sondage

Chaque sondage doit suivre cette structure:

```
surveys/
└── survey-XXX-nom-court/
    ├── raw/                      # Fichiers originaux
    │   ├── codebook.*            # Codebook original (PDF, TXT, XLSX, etc.)
    │   └── data.*                # Données originales (CSV, SAV, XLSX)
    ├── processed/                # Fichiers traités
    │   ├── codebook.json         # Codebook standardisé
    │   └── data_cleaned.csv      # Données nettoyées
    ├── clean.py                  # Script de nettoyage Python
    └── metadata.json             # Métadonnées du sondage
```

## Conventions de nommage

- **Dossier**: `survey-XXX-nom-court` où XXX est un numéro séquentiel
- **Variables démographiques**: préfixe `demo_`
- **Variables d'opinion**: préfixe `op_`
- **Valeurs manquantes**: `np.nan` ou `None`
- **Échelles**: Standardiser sur 0-1 quand possible

## Workflow

1. Créer un nouveau dossier pour le sondage
2. Placer les fichiers originaux dans `raw/`
3. Créer `metadata.json` avec les infos de base
4. Utiliser `/clean-survey` pour générer/coder le script de nettoyage
5. Exécuter le script et vérifier les résultats dans `processed/`

## Slash Command

Utiliser `/clean-survey` dans Claude Code pour obtenir de l'aide sur:
- Analyse du codebook
- Génération du script de nettoyage
- Débogage du script
- Standardisation des variables

## Template

Copier le dossier `_template/` pour démarrer un nouveau sondage.