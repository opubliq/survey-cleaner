---
description: Lance l'agent autonome de nettoyage de sondage
argument-hint: [survey_name] [num_vars]
autoApprove:
  - Bash(*)
  - mcp__ide__executeCode
---

Tu vas lancer l'agent survey-cleaner-agent pour nettoyer un sondage.

## Arguments:
- $1: Nom du sondage (obligatoire)
- $2: Nombre de variables à nettoyer (optionnel, défaut: "all")
  - "all": Nettoyer toutes les variables
  - Un nombre (ex: "5"): Nettoyer les N premières variables non traitées

## Étapes:

1. Si $1 n'est pas fourni, liste les sondages disponibles dans surveys/ et demande lequel traiter

2. Vérifier que le sondage existe dans surveys/$1/

3. Déterminer le nombre de variables à traiter:
   - Si $2 n'est pas fourni ou vaut "all": traiter toutes les variables
   - Sinon: traiter les $2 premières variables non traitées

4. Lancer l'agent survey-cleaner-agent avec Task tool:
   - subagent_type: "survey-cleaner-agent"
   - description: "Clean survey $1"
   - prompt: "Process survey in surveys/$1/ following your complete workflow. Process [number] variables (all or first N non-completed from variables_todo.md). Report summary when done."

5. Attendre que l'agent termine et présenter son rapport final au user

IMPORTANT:
- L'agent a toutes les instructions dans survey-cleaner-agent.md, pas besoin de les répéter
- L'agent est autonome et suit le workflow variable-par-variable automatiquement
- Ne pas interrompre son travail sauf en cas d'erreur bloquante
- L'agent doit respecter la limite de variables spécifiée