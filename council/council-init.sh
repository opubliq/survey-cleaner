#!/usr/bin/env bash
# council-init.sh - Deploy council setup to any project
# Usage: council-init.sh [target-directory]
#   If no target specified, uses current directory

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${1:-.}"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${BLUE}[council-init]${NC} $*"; }
ok()  { echo -e "${GREEN}[  ok  ]${NC} $*"; }
warn() { echo -e "${YELLOW}[ warn ]${NC} $*"; }

# Resolve absolute path
TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"
COUNCIL_DIR="$TARGET_DIR/council"

# Check if council already exists
if [[ -d "$COUNCIL_DIR" ]]; then
  warn "Council directory already exists at $COUNCIL_DIR"
  read -p "Overwrite? [y/N] " -n 1 -r
  echo
  [[ ! $REPLY =~ ^[Yy]$ ]] && exit 0
  rm -rf "$COUNCIL_DIR"
fi

log "Creating council setup in $TARGET_DIR"

# Create directory structure
mkdir -p "$COUNCIL_DIR"/{sessions,templates}

# Copy files
cp "$SCRIPT_DIR/config.sh" "$COUNCIL_DIR/"
cp "$SCRIPT_DIR/council.sh" "$COUNCIL_DIR/"
cp "$SCRIPT_DIR/templates"/*.md "$COUNCIL_DIR/templates/"

# Create example question
cat > "$COUNCIL_DIR/question.md" << 'EOF'
# Your Technical Question Here

## Context

Briefly describe your project context...

## Problem

What problem are you trying to solve?

## Constraints

Any constraints or requirements...

## Question

Your actual question here...
EOF

# Make scripts executable
chmod +x "$COUNCIL_DIR/council.sh"

# Create quickstart guide
cat > "$COUNCIL_DIR/README.md" << 'EOF'
# Council - Technical Decision Multi-LLM

Quick setup from `council-init.sh`.

## Quick Start

```bash
cd council
./council.sh check          # Verify all models work
./council.sh run "My question here"
# OR
./council.sh run --file ../question.md
```

## Commands

- `check` - Sanity check all models (run first!)
- `run "question"` - Full pipeline (propose → critique → vote → verdict)
- `new "question"` - Create new session
- `propose <session>` - Phase 1: proposals
- `critique <session>` - Phase 2: critiques
- `vote <session>` - Phase 3: votes
- `verdict <session>` - Phase 4: final verdict
- `status <session>` - Show session status
- `list` - List all sessions

## Configuration

Edit `config.sh` to add/remove models.

## Results

Sessions stored in `sessions/` with timestamp ID:
- `sessions/<timestamp>/prompt.md` - Original question
- `sessions/<timestamp>/proposals/` - Individual model proposals
- `sessions/<timestamp>/critiques/` - Model critiques
- `sessions/<timestamp>/votes/` - Model votes
- `sessions/<timestamp>/verdict.md` - Final synthesis
EOF

ok "Council setup complete!"
log ""
log "Next steps:"
log "  cd $TARGET_DIR/council"
log "  ./council.sh check"
log "  ./council.sh run \"Your question here\""
