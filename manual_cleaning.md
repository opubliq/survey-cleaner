## 🎯 Priorités

- [x] Pour chaque variable, recherche fuzzy si une variable presque pareille a été créée. Si oui, essayer le plus possible d'avoir le même nom. Chercher dans les codebooks existants dans les dossiers processed/.
- [x] Initialisation plus simple d'un nouveau sondage. par exemple simplement créer un dossier {survey_id}/ et mettre directement dedans les fichiers de données et le codebook, et l'agent s'occupe du reste (copier la structure de template, le script, etc.).
- [x] Argument dans la slash command /clean-survey pour dire le nombre de variables à cleaner, par défaut à "all"
- [x] Commande pour reprendre un nettoyage interrompu (lire variables_todo.md et continuer où on était rendu)
  - [x] Mode "resume" après crash: détecter automatiquement si variables_todo.md existe et proposer de continuer
- [x] Commit clean.py après chaque variable pour un historique (ou après des listes de variables?)
- [x] Rapport final de nettoyage: tableau récapitulatif des transformations (X variables traitées, Y recodages, Z missing ajoutés)
