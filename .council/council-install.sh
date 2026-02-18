#!/usr/bin/env bash
# council-install.sh - Install council-init globally
# Usage: council-install.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}[council-install]${NC} $*"; }
ok()  { echo -e "${GREEN}[  ok  ]${NC} $*"; }

# Target locations
BIN_DIR="$HOME/.local/bin"
SYMLINK="$BIN_DIR/council-init"

# Create bin directory if needed
mkdir -p "$BIN_DIR"

# Create symlink
log "Creating symlink: $SYMLINK -> $SCRIPT_DIR/council-init.sh"
ln -sf "$SCRIPT_DIR/council-init.sh" "$SYMLINK"

ok "Installed! Usage:"
log ""
log "  cd /path/to/your/project"
log "  council-init"
log ""
log "Then:"
log "  cd council"
log "  ./council.sh check"
