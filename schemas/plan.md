# Plan Survey Cleaner - Architecture n8n

## Vue d'ensemble
Le Survey Cleaner est un workflow n8n qui automatise le nettoyage de fichiers de sondages pour l'intégration dans l'infrastructure Opubliq. Il traite les données variables par variable pour garantir la qualité et la conformité aux conventions.

## Étape 1 - Upload utilisateur
**Interface Web Simple**
- L'utilisateur (employé Opubliq) accède à une page web locale
- Upload de deux fichiers obligatoires :
  - **Fichier data** : données brutes du sondage (CSV, SAV, SPSS, Stata, etc.)
  - **Fichier codebook** : documentation des variables (PDF, Excel, CSV, TXT)

## Étape 2 - Réception webhook
**Webhook n8n**
- Le workflow reçoit les fichiers via endpoint `/webhook/survey-cleaner`
- Validation de la présence des fichiers requis
- Initialisation du processus de nettoyage

## Étape 3 - Lecture du codebook
**Node : `codebook_reader`**
- **Input** : Fichier codebook (tous formats)
- **Traitement** : Extraction et normalisation du contenu
- **Output** : Codebook structuré en format Markdown standardisé
- **Formats supportés** : PDF, Excel, CSV, TXT

## Étape 4 - Lecture des données
**Node : `data_reader`**  
- **Input** : Fichier data (tous formats)
- **Traitement** : Parsing et normalisation des données
- **Output** : DataFrame Python structuré et métadonnées
- **Formats supportés** : CSV, SAV, SPSS, Stata, Excel

## Étape 5 - Nettoyage des données
**Node principale : `data_cleaner`**

### 5.1 Initialisation
- Lecture du codebook.md structuré  
- Exploration initiale du DataFrame
- Identification de toutes les variables à traiter

### 5.2 Traitement variable par variable
**Boucle automatisée pour chaque variable :**

1. **Analyse du codebook**
   - Identification du type de variable (démographique/opinion/technique)
   - Extraction des valeurs possibles et étiquettes
   - Détection des valeurs manquantes spécifiques

2. **Attribution du nom Opubliq**
   - Application des conventions de nommage :
     - `demo_` pour les variables démographiques
     - `op_` pour les variables d'opinion
     - Autres préfixes selon le type

3. **Analyse de la structure raw**
   - Exécution de code Python pour examiner la variable
   - Identification des types de données réels
   - Détection d'anomalies ou incohérences

4. **Génération du code de nettoyage**
   - Création du script Python spécifique à la variable
   - Application des transformations nécessaires
   - Gestion des valeurs manquantes (standardisation à `NA`)

5. **Exécution et validation**
   - Exécution du code de nettoyage généré
   - Vérification des distributions post-nettoyage
   - Validation de conformité avec le codebook
   - Tests de qualité automatisés

6. **Consolidation**
   - Ajout du code validé au script Python final
   - Passage à la variable suivante

### 5.3 Finalisation
- Assemblage du script Python complet
- Application des conventions pipeline-sondage Opubliq
- Ajout des métadonnées et documentation
- Validation finale du script

**Capacités techniques requises :**
- Génération de code Python dynamique
- Exécution de code dans un environnement sécurisé
- Validation automatisée des résultats

## Étape 6 - Output et déploiement
**Options de sortie :**

### Option A - Download manuel
- Retour du script Python à l'utilisateur
- Téléchargement via l'interface web
- Validation manuelle avant déploiement

### Option B - Déploiement automatique (FONCTIONNEL)
- Intégration directe dans pipeline-sondage
- Dépôt automatique des fichiers :
  - Script Python de nettoyage
  - Données originales
  - Codebook traité
- Déclenchement automatique du pipeline

## Architecture technique
- **Framework** : n8n workflows
- **Langage principal** : Python pour le nettoyage
- **API** : Claude (Anthropic) pour l'intelligence de nettoyage
- **Formats supportés** : CSV, SAV, SPSS, Stata, Excel, PDF
- **Integration** : Pipeline-sondage Opubliq existant