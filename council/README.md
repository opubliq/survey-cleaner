# Council - Portable Multi-LLM Technical Decision Tool

Deploy council to any project in 2 commands.

## Quick Install (One-time)

```bash
cd /path/to/survey-cleaner/council
./council-install.sh
```

This installs `council-init` globally in `~/.local/bin/`.

## Quick Usage

In any new project:

```bash
council-init                    # Creates council/ folder with everything
cd council
./council.sh check              # Verify all models work
./council.sh run "Your question here"
```

Or from a file:

```bash
council-init
cd council
./council.sh run --file ../question.md
```

## What It Does

Council runs your technical question through 10+ LLMs in parallel:

1. **Propose** - Each model proposes a solution
2. **Critique** - Each model critiques all proposals
3. **Vote** - Each model votes for best proposal
4. **Verdict** - Judge synthesizes final recommendation

Results stored in `sessions/<timestamp>/`:
- `proposals/*.md` - Individual model proposals
- `critiques/*.md` - Model critiques
- `votes/*.md` - Model votes
- `verdict.md` - Final synthesized answer

## Commands

```bash
./council.sh check                  # Sanity check all models
./council.sh run "question"         # Full pipeline
./council.sh run --file q.md        # From file
./council.sh new "question"         # Create session
./council.sh propose <session>      # Phase 1
./council.sh critique <session>     # Phase 2
./council.sh vote <session>         # Phase 3
./council.sh verdict <session>      # Phase 4
./council.sh status <session>       # Show status
./council.sh list                   # List all sessions
```

## Configuration

Edit `config.sh` to add/remove models:

```bash
COUNCIL_MODELS=(
  "opencode/big-pickle"
  "google/gemini-2.5-flash"
  "anthropic/claude-sonnet-4-6"
)
```

## Example Question Template

`question.md`:

```markdown
# Your Technical Question Here

## Context
Briefly describe your project context...

## Problem
What problem are you trying to solve?

## Constraints
Any constraints or requirements...

## Question
Your actual question here...
```
