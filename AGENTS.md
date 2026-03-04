# Agent Instructions

This project uses **bd** (beads) for issue tracking. Run `bd onboard` to get started.

## Environment Setup

```bash
source venv/bin/activate   # Always use this venv for Python commands
```

All Python commands should use the venv:
- `venv/bin/python -m pytest tests/`
- `venv/bin/python -m <module>`

## Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --status in_progress  # Claim work
bd close <id>         # Complete work
bd sync               # Sync with git
```

## Landing the Plane (Session Completion)

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd sync
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds

Use 'bd' for task tracking

## Definition of Done

**An issue is NOT closeable until the component is tested.** Closing without testing = incomplete work.

### How to test each component

| Component | Test command |
|-----------|-------------|
| Agent `.claude/agents/*.md` | `opencode run --agent <name> --model <model> '<json context>'` on a real survey |
| Python module | `venv/bin/python -m pytest tests/` |
| Pipeline step | Run end-to-end on a sample survey in `_SharedFolder_data_produit/` |

### Agent testing checklist

Before closing an agent refactor issue:
1. Run the agent on at least one real input (not mocked)
2. Verify the expected output file was created (`codebook.json`, `vars/{var}.py`, etc.)
3. Inspect the output — does it match the format spec in `docs/v3-plan.md`?
4. If the agent fails, fix it before closing
