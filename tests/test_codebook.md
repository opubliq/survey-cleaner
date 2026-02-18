# Test Survey Codebook

## Variables

### id
- **Type**: numeric
- **Description**: Identifiant unique du répondant
- **Values**: 1-20

### nom
- **Type**: text
- **Description**: Nom complet du répondant

### age
- **Type**: numeric
- **Description**: Age du répondant en années
- **Values**: 18-65

### sexe
- **Type**: categorical
- **Description**: Sexe du répondant
- **Values**: M=Masculin, F=Féminin
- **Missing values**: 

### education
- **Type**: categorical
- **Description**: Niveau d'éducation le plus élevé
- **Values**: Primaire=École primaire, Secondaire=École secondaire, Collegial=Cégep/Collège, Universitaire=Université

### region
- **Type**: categorical
- **Description**: Région de résidence
- **Values**: Quebec, Montreal, Laval, Gatineau, Sherbrooke, Trois-Rivieres, Longueuil

### opinion_immigration
- **Type**: likert
- **Description**: Opinion sur l'immigration au Québec
- **Values**: 1=Très défavorable, 2=Défavorable, 3=Neutre, 4=Favorable, 5=Très favorable
- **Missing values**: 99

### opinion_economie
- **Type**: likert
- **Description**: Opinion sur la situation économique actuelle
- **Values**: 1=Très mauvaise, 2=Mauvaise, 3=Neutre, 4=Bonne, 5=Très bonne
- **Missing values**: 99

### opinion_environnement
- **Type**: likert
- **Description**: Importance accordée aux enjeux environnementaux
- **Values**: 1=Pas important, 2=Peu important, 3=Neutre, 4=Important, 5=Très important
- **Missing values**: 99

### satisfaction_gouv
- **Type**: likert
- **Description**: Satisfaction envers le gouvernement actuel
- **Values**: 1=Très insatisfait, 2=Insatisfait, 3=Neutre, 4=Satisfait, 5=Très satisfait
- **Missing values**: 99

### vote_intention
- **Type**: categorical
- **Description**: Intention de vote aux prochaines élections
- **Values**: PLQ=Parti Libéral du Québec, CAQ=Coalition Avenir Québec, PQ=Parti Québécois, QS=Québec Solidaire
- **Missing values**: 99
