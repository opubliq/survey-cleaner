---
description: Lance l'agent autonome de nettoyage de sondage
argument-hint: [survey_name]
autoApprove:
  - Bash(*)
  - mcp__ide__executeCode
---

Tu vas lancer l'agent survey-cleaner-agent pour nettoyer un sondage.

## Étapes:

1. Si $1 n'est pas fourni, liste les sondages disponibles dans surveys/ et demande lequel traiter

2. Vérifier que le sondage existe dans surveys/$1/

3. Lancer l'agent survey-cleaner-agent avec Task tool:
   - subagent_type: "survey-cleaner-agent"
   - description: "Clean survey $1"
   - prompt simple: "Process survey in surveys/$1/ following your complete workflow. Report summary when done."

4. Attendre que l'agent termine et présenter son rapport final au user

IMPORTANT:
- L'agent a toutes les instructions dans survey-cleaner-agent.md, pas besoin de les répéter
- L'agent est autonome et suit le workflow variable-par-variable automatiquement
- Ne pas interrompre son travail sauf en cas d'erreur bloquante