# Question: Quelle approche pour un agent de nettoyage de sondages scalable et economique?

## Le probleme

On nettoie des sondages (CSV/SAV/XLSX). Chaque sondage a 80-200 variables brutes (ex: `Q2_province = 1, 2, 3`) qu'on transforme en variables standardisees (ex: `ses_province = "qc", "on", "bc"`) en generant un script Python (`clean.py`). Un codebook (documentation des variables) accompagne chaque sondage et explique ce que chaque valeur signifie.

Le nombre de sondages n'est pas fixe. On veut un systeme ou des qu'on a un nouveau sondage, on le traite. Actuellement on a ~57 sondages, mais ca va continuer a grossir.

## Ce qu'on a essaye (et les couts reels)

### Tentative 1: CLI coding agent (Claude Code avec agents slash/Task tool)
- Approche: Un agent CLI qui a acces au filesystem, lit les fichiers, ecrit du code
- 186,900 tokens pour nettoyer **1 variable** sur 84
- Cause: le Task tool recharge le contexte complet a chaque appel agent (~46K tokens d'overhead/variable)
- Projection: 3.9M tokens par sondage = impraticable
- **Cout: session epuisee avant de finir**

### Tentative 2: Script Python appelant l'API directe + prompt caching
- Approche: orchestrator.py qui appelle l'API Claude (Sonnet) programmatiquement, 1 call par variable, avec prompt caching pour reduire les couts
- Theorie: 92K tokens/sondage grace au cache (500 tokens/variable apres la premiere)
- **Realite: 38$ pour nettoyer UN sondage de 84 variables**
- Le prompt caching n'a pas donne les economies esperees

### Strategie hybride (documentee, jamais implementee)
- Idee: classifier variables en types et n'utiliser le LLM que pour les cas complexes (~35%)
  - Type A (~65%): pattern standard (Likert, oui/non, demographics) → regles deterministes, 0 tokens
  - Type B (~25%): pattern non-standard → LLM en batch
  - Type C (~10%): codebook incomplet → LLM individuel
- Pattern library qui s'enrichit avec chaque sondage
- Estimation: ~$4-5/sondage
- **Jamais construite. On ne sait pas si c'est realiste.**

## Patterns de donnees observes

Certaines variables suivent des patterns reconnaissables (Likert 5 points, binaires oui/non, demographics), MAIS meme pour ces variables "simples", un LLM doit quand meme prendre des decisions: quel nom standardise donner? quels codes representent des valeurs manquantes (98? 99? -9?)? comment normaliser l'echelle? Le pattern aide a orienter, mais la decision finale pour chaque variable requiert du jugement.

## Contraintes

- **Budget**: Le moins cher possible. Le 38$/sondage actuel est inacceptable pour 57+ sondages.
- **Autonome apres lancement**: On lance l'agent manuellement ("clean le sondage XXX"), mais ensuite il doit rouler sans intervention humaine (ou presque). Pas de babysitting.
- **Qualite**: Quelques erreurs rattrapees par validation humaine = OK. 50% d'erreurs = pas OK.
- **Simplicite**: Petite equipe. Pas envie de maintenir une usine a gaz.
- **Outils disponibles**: opencode (CLI multi-provider), Claude Code, APIs directes (Anthropic, Google, OpenAI), modeles gratuits via opencode zen (big-pickle, GLM-5, Kimi K2.5, Minimax M2.5) et z.ai (GLM-4.7, GLM-4.5).

## Les grandes approches possibles

Je vois au moins 4 philosophies fondamentalement differentes. Laquelle choisir?

### A. API directe (ce qu'on fait)
Script Python qui appelle l'API programmatiquement. On controle tout (prompts, batching, caching). Mais on paie chaque token et on doit tout coder nous-meme (orchestration, retry, validation...).

### B. CLI coding agent (Claude Code, opencode, aider)
On lance un agent CLI sur le dossier du sondage et on lui dit "genere le clean.py". L'agent a acces au filesystem, peut lire le codebook, explorer les donnees, ecrire le code. On ne controle pas les tokens -- c'est l'agent qui decide combien il consomme. Mais c'est beaucoup plus simple a utiliser.

### C. Hybride regles + LLM
On investit dans une pattern library deterministe pour guider le LLM (ou meme bypasser le LLM sur certains cas triviaux), et on utilise le LLM pour les decisions finales et les edge cases. Plus complexe a construire, potentiellement moins cher a operer.

### D. Pipeline sans LLM (ou presque)
On extrait le codebook en JSON structure, puis on genere le clean.py avec des regles purement deterministes. LLM utilise seulement pour le bootstrap initial (parser le codebook une fois). Potentiellement le moins cher, mais peut-etre pas assez flexible?

## Questions specifiques

1. **Quelle approche (A/B/C/D) recommandes-tu et pourquoi?** Peut-etre un mix?

2. **Si LLM: quel modele?** On a acces a des modeles gratuits (GLM-5, Kimi K2.5, Minimax M2.5). Sont-ils assez bons pour du nettoyage de sondages, ou faut-il un modele cher (Claude, GPT-4)?

3. **Si LLM: quelle granularite d'appel?** 1 appel par variable (actuel, cher)? Batch de 10-20 variables? Tout le sondage en un seul appel massif?

4. **Comment gerer le codebook?** Le convertir en Markdown dans le system prompt (actuel)? Extraction structuree en JSON schema? Embeddings/RAG? Autre?

5. **Comment assurer l'autonomie?** On lance manuellement, mais apres ca l'agent doit rouler tout seul jusqu'au bout. Comment structurer ca?

## Ce que j'attends

Une recommandation technique concrete et opiniee:
- L'approche choisie (A/B/C/D ou mix) et pourquoi
- Architecture recommandee (workflow, composants)
- Choix de modele(s) et strategie
- Gestion du codebook
- Estimation de cout realiste pour un sondage de 84 variables
- Trade-offs honnetes de l'approche
