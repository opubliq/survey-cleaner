1. Utiliser **agent survey-init** pour initier le dossier de cleaning du sondage avec template python vide

2. Utiliser **agent transform-codebook** pour transformer le codebook en format lisible par Claude

Pour chaque variable:
    3. Utiliser **agent clean-variable** pour générer le code de cleaning pour une variable. Être le plus spécifique possible, donner des instructions etc.
    4. Utiliser **agent validate-cleaning** qui va exécuter le code de cleaning de cette variable et le comparer à la distribution raw.
    5. Utiliser **agent generate-codebook-entry** pour générer le code qui map les valeurs de la variable nettoyée à leur labels dans le codebook json (liste)

6. Une fois le script de cleaning généré, updater le document nécessaire pour que le tracking automatique se fasse.