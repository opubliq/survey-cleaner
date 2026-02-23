1. Le modele hyper hybride à 3 tiers qu'on essaie d'implementer a clairement des problemes, je crois pas que c'est la meilleure solution. Le test run qu'on a fait c'était mauvais

2. Clairement, un système avec des agents qui ont des skills spécifiques est mieux adapté à notre situation

3. Je crois qu'aucun modèle utilisé dans le système doit être gros, à part peut-être "l'orchestrateur"... Mais même là pas sur. Les taches sont simples et petites: checker la variable dans le codebook raw. Écrire du code pour la "standardiser/nettoyer". Exécuter le code. Valider que ça fonctionne. etc. Décomposées, ces taches sont tres petites.

Il y a peut-être la transformation du codebook en JSON qui doit rester hybride comme live, à voir.

4. Au lieu de calls à l'api, j'ai l'impression que de faire comme un peu dans .council/ avec opencode "prompt" --model est pt mieux?

