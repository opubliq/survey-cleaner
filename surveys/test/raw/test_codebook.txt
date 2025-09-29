# CODEBOOK - Sondage Politique Quebec 2024

## Variables démographiques

### id
- Type: Numérique
- Description: Identifiant unique du répondant
- Valeurs: 1-20

### nom
- Type: Texte
- Description: Nom complet du répondant
- Format: Prénom Nom

### age
- Type: Numérique
- Description: Age du répondant en années
- Valeurs: 18-65

### sexe
- Type: Catégoriel
- Description: Sexe du répondant
- Valeurs: M = Masculin, F = Féminin

### education
- Type: Catégoriel
- Description: Niveau d'éducation le plus élevé
- Valeurs: 
  - Primaire = École primaire
  - Secondaire = École secondaire
  - Collegial = Cégep/Collège
  - Universitaire = Université

### region
- Type: Catégoriel
- Description: Région de résidence
- Valeurs: Quebec, Montreal, Laval, Gatineau, Sherbrooke, Trois-Rivieres, Longueuil

## Variables d'opinion

### opinion_immigration
- Type: Échelle Likert
- Description: Opinion sur l'immigration au Québec
- Échelle: 1 = Très défavorable, 5 = Très favorable
- Valeurs manquantes: 99

### opinion_economie
- Type: Échelle Likert
- Description: Opinion sur la situation économique actuelle
- Échelle: 1 = Très mauvaise, 5 = Très bonne
- Valeurs manquantes: 99

### opinion_environnement
- Type: Échelle Likert
- Description: Importance accordée aux enjeux environnementaux
- Échelle: 1 = Pas important, 5 = Très important
- Valeurs manquantes: 99

### satisfaction_gouv
- Type: Échelle Likert
- Description: Satisfaction envers le gouvernement actuel
- Échelle: 1 = Très insatisfait, 5 = Très satisfait
- Valeurs manquantes: 99

## Variables politiques

### vote_intention
- Type: Catégoriel
- Description: Intention de vote aux prochaines élections
- Valeurs:
  - PLQ = Parti Libéral du Québec
  - CAQ = Coalition Avenir Québec
  - PQ = Parti Québécois
  - QS = Québec Solidaire
  - 99 = Ne sait pas/Refuse de répondre

## Instructions de nettoyage

1. Variables démographiques: Renommer avec préfixe "demo_"
2. Variables d'opinion: Renommer avec préfixe "op_" et standardiser sur échelle 0-1
3. Variables politiques: Garder comme catégorielles
4. Valeurs manquantes: Convertir 99 en NA
5. Format de sortie: Fichier .rds

## Conventions Opubliq

- Préfixe démographique: demo_
- Préfixe opinion: op_
- Encodage NA: NA pour toutes les valeurs manquantes
- Échelles standardisées: 0-1 pour toutes les variables d'opinion