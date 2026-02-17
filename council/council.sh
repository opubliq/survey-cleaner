#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# council.sh - Multi-LLM Technical Decision Council
# 
# Usage:
#   ./council.sh new "My technical question here"
#   ./council.sh new --file question.md
#   ./council.sh propose <session>
#   ./council.sh critique <session>
#   ./council.sh vote <session>
#   ./council.sh verdict <session>
#   ./council.sh run "My question"          # Full pipeline
#   ./council.sh run --file question.md     # Full pipeline from file
#   ./council.sh status <session>
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SESSIONS_DIR="$SCRIPT_DIR/sessions"
TEMPLATES_DIR="$SCRIPT_DIR/templates"

# Load config
source "$SCRIPT_DIR/config.sh"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

log()  { echo -e "${BLUE}[council]${NC} $*"; }
ok()   { echo -e "${GREEN}[  ok  ]${NC} $*"; }
warn() { echo -e "${YELLOW}[ warn ]${NC} $*"; }
err()  { echo -e "${RED}[error ]${NC} $*" >&2; }

# ============================================================================
# Helpers
# ============================================================================

get_project_context() {
  # Grab key project info for context
  local context=""
  if [[ -f "$PROJECT_ROOT/README.md" ]]; then
    context+="### README.md (first 60 lines)
$(head -60 "$PROJECT_ROOT/README.md")

"
  fi
  if [[ -f "$PROJECT_ROOT/CLAUDE.md" ]]; then
    context+="### CLAUDE.md (first 80 lines)
$(head -80 "$PROJECT_ROOT/CLAUDE.md")
"
  fi
  echo "$context"
}

render_template() {
  local template="$1"
  shift
  local content
  content="$(cat "$template")"
  
  # Replace placeholders with provided values
  while [[ $# -ge 2 ]]; do
    local key="$1"
    local value="$2"
    content="${content//"{{${key}}"/"${value}"}"
    shift 2
  done
  
  echo "$content"
}

call_model() {
  local model="$1"
  local name="$2"
  local prompt="$3"
  local output_file="$4"
  
  log "Calling ${BOLD}$name${NC} ($model)..."
  
  # Run opencode in non-interactive mode
  if timeout "$TIMEOUT" opencode run \
    -m "$model" \
    --dir "$PROJECT_ROOT" \
    "$prompt" \
    > "$output_file.raw" 2>/dev/null; then
    
    # Clean ANSI codes and control chars from output
    sed 's/\x1b\[[0-9;]*m//g; s/\x1b\[K//g' "$output_file.raw" | tr -d '\r' > "$output_file"
    rm -f "$output_file.raw"
    ok "$name done ($(wc -w < "$output_file") words)"
    return 0
  else
    err "$name failed or timed out"
    echo "ERROR: Model $name ($model) failed to respond within ${TIMEOUT}s" > "$output_file"
    rm -f "$output_file.raw"
    return 1
  fi
}

call_models_parallel() {
  local prompt_template="$1"
  local output_dir="$2"
  shift 2
  # Additional template vars as key=value pairs
  
  local pids=()
  local names=()
  local running=0
  
  for i in "${!COUNCIL_MODELS[@]}"; do
    local model="${COUNCIL_MODELS[$i]}"
    local name="${COUNCIL_NAMES[$i]}"
    local output_file="$output_dir/${name}.md"
    
    # Skip if already done
    if [[ -f "$output_file" ]] && [[ "$(wc -w < "$output_file")" -gt 20 ]]; then
      ok "$name already completed, skipping"
      continue
    fi
    
    # Throttle parallel jobs
    while [[ $running -ge $MAX_PARALLEL ]]; do
      # Wait for any job to finish
      for j in "${!pids[@]}"; do
        if ! kill -0 "${pids[$j]}" 2>/dev/null; then
          wait "${pids[$j]}" || true
          unset "pids[$j]"
          ((running--)) || true
        fi
      done
      sleep 1
    done
    
    # Launch in background
    call_model "$model" "$name" "$prompt_template" "$output_file" &
    pids+=($!)
    names+=("$name")
    ((running++)) || true
  done
  
  # Wait for all remaining
  for pid in "${pids[@]}"; do
    wait "$pid" || true
  done
  
  ok "All models completed"
}

collect_files() {
  local dir="$1"
  local result=""
  for f in "$dir"/*.md; do
    [[ -f "$f" ]] || continue
    local name
    name="$(basename "$f" .md)"
    result+="### $name

$(cat "$f")

---

"
  done
  echo "$result"
}

# ============================================================================
# Commands
# ============================================================================

cmd_new() {
  local prompt=""
  
  if [[ "${1:-}" == "--file" ]] && [[ -n "${2:-}" ]]; then
    prompt="$(cat "$2")"
  elif [[ -n "${1:-}" ]]; then
    prompt="$*"
  else
    err "Usage: council.sh new \"question\" or council.sh new --file question.md"
    exit 1
  fi
  
  # Create session with timestamp
  local session
  session="$(date +%Y%m%d-%H%M%S)"
  local session_dir="$SESSIONS_DIR/$session"
  
  mkdir -p "$session_dir"/{proposals,critiques,votes}
  echo "$prompt" > "$session_dir/prompt.md"
  
  ok "Session created: ${BOLD}$session${NC}" >&2
  log "Prompt saved to: sessions/$session/prompt.md" >&2
  echo "$session"
}

cmd_propose() {
  local session="$1"
  local session_dir="$SESSIONS_DIR/$session"
  
  [[ -d "$session_dir" ]] || { err "Session $session not found"; exit 1; }
  
  local prompt
  prompt="$(cat "$session_dir/prompt.md")"
  local context
  context="$(get_project_context)"
  
  local full_prompt
  full_prompt="$(render_template "$TEMPLATES_DIR/propose.md" \
    "PROJECT_CONTEXT" "$context" \
    "PROMPT" "$prompt")"
  
  log "Phase 1: PROPOSE - sending to ${#COUNCIL_MODELS[@]} models..."
  call_models_parallel "$full_prompt" "$session_dir/proposals"
  
  ok "Proposals complete. See: sessions/$session/proposals/"
}

cmd_critique() {
  local session="$1"
  local session_dir="$SESSIONS_DIR/$session"
  
  [[ -d "$session_dir" ]] || { err "Session $session not found"; exit 1; }
  
  local prompt
  prompt="$(cat "$session_dir/prompt.md")"
  local proposals
  proposals="$(collect_files "$session_dir/proposals")"
  
  local full_prompt
  full_prompt="$(render_template "$TEMPLATES_DIR/critique.md" \
    "PROMPT" "$prompt" \
    "PROPOSALS" "$proposals")"
  
  log "Phase 2: CRITIQUE - ${#COUNCIL_MODELS[@]} models reviewing all proposals..."
  call_models_parallel "$full_prompt" "$session_dir/critiques"
  
  ok "Critiques complete. See: sessions/$session/critiques/"
}

cmd_vote() {
  local session="$1"
  local session_dir="$SESSIONS_DIR/$session"
  
  [[ -d "$session_dir" ]] || { err "Session $session not found"; exit 1; }
  
  local prompt
  prompt="$(cat "$session_dir/prompt.md")"
  local proposals
  proposals="$(collect_files "$session_dir/proposals")"
  local critiques
  critiques="$(collect_files "$session_dir/critiques")"
  
  local full_prompt
  full_prompt="$(render_template "$TEMPLATES_DIR/vote.md" \
    "PROMPT" "$prompt" \
    "PROPOSALS" "$proposals" \
    "CRITIQUES" "$critiques")"
  
  log "Phase 3: VOTE - ${#COUNCIL_MODELS[@]} models casting votes..."
  call_models_parallel "$full_prompt" "$session_dir/votes"
  
  # Quick tally
  log "Quick vote tally:"
  grep -h "VOTE:" "$session_dir/votes/"*.md 2>/dev/null | sort | uniq -c | sort -rn || true
  
  ok "Votes complete. See: sessions/$session/votes/"
}

cmd_verdict() {
  local session="$1"
  local session_dir="$SESSIONS_DIR/$session"
  
  [[ -d "$session_dir" ]] || { err "Session $session not found"; exit 1; }
  
  local prompt
  prompt="$(cat "$session_dir/prompt.md")"
  local proposals
  proposals="$(collect_files "$session_dir/proposals")"
  local critiques
  critiques="$(collect_files "$session_dir/critiques")"
  local votes
  votes="$(collect_files "$session_dir/votes")"
  
  local full_prompt
  full_prompt="$(render_template "$TEMPLATES_DIR/verdict.md" \
    "PROMPT" "$prompt" \
    "PROPOSALS" "$proposals" \
    "CRITIQUES" "$critiques" \
    "VOTES" "$votes")"
  
  log "Phase 4: VERDICT - judge ($JUDGE_NAME) synthesizing..."
  call_model "$JUDGE_MODEL" "$JUDGE_NAME" "$full_prompt" "$session_dir/verdict.md"
  
  echo ""
  echo -e "${BOLD}========================================${NC}"
  echo -e "${BOLD}         COUNCIL VERDICT${NC}"
  echo -e "${BOLD}========================================${NC}"
  echo ""
  cat "$session_dir/verdict.md"
  
  ok "Verdict saved to: sessions/$session/verdict.md"
}

cmd_run() {
  # Full pipeline
  local session
  session="$(cmd_new "$@")"
  
  echo ""
  echo -e "${BOLD}========================================${NC}"
  echo -e "${BOLD}  Technical Council - Full Pipeline${NC}"
  echo -e "${BOLD}  Session: $session${NC}"
  echo -e "${BOLD}========================================${NC}"
  echo ""
  
  cmd_propose "$session"
  echo ""
  cmd_critique "$session"
  echo ""
  cmd_vote "$session"
  echo ""
  cmd_verdict "$session"
}

cmd_status() {
  local session="$1"
  local session_dir="$SESSIONS_DIR/$session"
  
  [[ -d "$session_dir" ]] || { err "Session $session not found"; exit 1; }
  
  echo -e "${BOLD}Session: $session${NC}"
  echo ""
  
  echo -e "${CYAN}Prompt:${NC}"
  head -3 "$session_dir/prompt.md"
  echo ""
  
  echo -e "${CYAN}Proposals:${NC}"
  local found_proposals=0
  for f in "$session_dir/proposals/"*.md; do
    [[ -f "$f" ]] || continue
    echo "  $(basename "$f" .md): $(wc -w < "$f") words"
    found_proposals=1
  done
  [[ $found_proposals -eq 0 ]] && echo "  (none yet)"
  
  echo -e "${CYAN}Critiques:${NC}"
  for f in "$session_dir/critiques/"*.md; do
    [[ -f "$f" ]] || continue
    echo "  $(basename "$f" .md): $(wc -w < "$f") words"
  done
  
  echo -e "${CYAN}Votes:${NC}"
  for f in "$session_dir/votes/"*.md; do
    [[ -f "$f" ]] || continue
    echo "  $(basename "$f" .md): $(wc -w < "$f") words"
  done
  
  if [[ -f "$session_dir/verdict.md" ]]; then
    echo -e "${GREEN}Verdict: ready ($(wc -w < "$session_dir/verdict.md") words)${NC}"
  fi
}

cmd_check() {
  log "Checking ${#COUNCIL_MODELS[@]} council models + judge..."
  echo ""
  
  local passed=0
  local failed=0
  local failed_names=()
  
  # Check all council models + judge
  local all_models=("${COUNCIL_MODELS[@]}" "$JUDGE_MODEL")
  local all_names=("${COUNCIL_NAMES[@]}" "$JUDGE_NAME")
  
  # Deduplicate (judge might be in council already)
  local checked=()
  
  for i in "${!all_models[@]}"; do
    local model="${all_models[$i]}"
    local name="${all_names[$i]}"
    
    # Skip if already checked this model
    local skip=0
    for c in "${checked[@]+"${checked[@]}"}"; do
      [[ "$c" == "$model" ]] && skip=1 && break
    done
    [[ $skip -eq 1 ]] && continue
    checked+=("$model")
    
    printf "  %-22s " "$name"
    
    local start_time
    start_time=$(date +%s%N 2>/dev/null || date +%s)
    
    local tmpfile
    tmpfile=$(mktemp)
    
    local errfile
    errfile=$(mktemp)
    
    if timeout 45 opencode run \
      -m "$model" \
      "Reply with exactly one word: COUNCIL_OK" \
      > "$tmpfile" 2>"$errfile"; then
      
      local end_time
      end_time=$(date +%s%N 2>/dev/null || date +%s)
      
      # Clean ANSI codes, UTF-8 multibyte artifacts, and control chars
      local response
      response=$(cat "$tmpfile" "$errfile" | sed 's/\x1b\[[0-9;]*m//g; s/\x1b\[K//g' | tr -d '\r' | strings)
      
      if echo "$response" | grep -qi "COUNCIL_OK"; then
        # Calculate elapsed time
        local elapsed="?"
        if [[ "$start_time" =~ [0-9]{10,} ]] && [[ "$end_time" =~ [0-9]{10,} ]]; then
          elapsed=$(( (end_time - start_time) / 1000000000 ))
          elapsed="${elapsed}s"
        fi
        echo -e "${GREEN}OK${NC} (${elapsed})"
        passed=$((passed + 1))
      elif echo "$response" | grep -qi "error\|unauthorized\|payment\|billing\|quota\|limit"; then
        # Extract the error message
        local errmsg
        errmsg=$(echo "$response" | grep -i "error\|unauthorized\|payment\|billing\|quota\|limit" | head -1 | sed 's/^[[:space:]]*//' | cut -c1-70)
        echo -e "${RED}ERROR${NC}"
        echo -e "    ${errmsg}"
        failed=$((failed + 1))
        failed_names+=("$name")
      else
        echo -e "${YELLOW}RESPONDED (unclear output)${NC}"
        echo "    $(echo "$response" | grep -v '^$' | head -1 | cut -c1-70)"
        passed=$((passed + 1))  # Model works, just didn't follow instruction exactly
      fi
    else
      local exit_code=$?
      local errmsg
      errmsg=$(sed 's/\x1b\[[0-9;]*m//g' "$errfile" | strings | grep -i "error\|fail\|timeout" | head -1 | cut -c1-70)
      if [[ $exit_code -eq 124 ]]; then
        echo -e "${RED}TIMEOUT${NC} (45s)"
      elif [[ -n "$errmsg" ]]; then
        echo -e "${RED}FAILED${NC}"
        echo -e "    ${errmsg}"
      else
        echo -e "${RED}FAILED${NC} (exit code $exit_code)"
      fi
      failed=$((failed + 1))
      failed_names+=("$name")
    fi
    
    rm -f "$tmpfile" "$errfile"
  done
  
  echo ""
  echo -e "${BOLD}Results: ${GREEN}$passed passed${NC}, ${RED}$failed failed${NC} out of ${#checked[@]} unique models"
  
  if [[ $failed -gt 0 ]]; then
    echo ""
    warn "Failed models: ${failed_names[*]}"
    warn "Fix these in config.sh or check your API keys/providers before running a session."
    return 1
  else
    ok "All models ready. You can run a council session."
    return 0
  fi
}

cmd_list() {
  echo -e "${BOLD}Sessions:${NC}"
  for d in "$SESSIONS_DIR"/*/; do
    [[ -d "$d" ]] || continue
    local name
    name="$(basename "$d")"
    local status="new"
    [[ -d "$d/proposals" ]] && [[ -n "$(ls "$d/proposals/" 2>/dev/null)" ]] && status="proposed"
    [[ -d "$d/critiques" ]] && [[ -n "$(ls "$d/critiques/" 2>/dev/null)" ]] && status="critiqued"
    [[ -d "$d/votes" ]] && [[ -n "$(ls "$d/votes/" 2>/dev/null)" ]] && status="voted"
    [[ -f "$d/verdict.md" ]] && status="done"
    
    local prompt_preview=""
    [[ -f "$d/prompt.md" ]] && prompt_preview="$(head -1 "$d/prompt.md" | cut -c1-60)"
    
    echo "  $name  [$status]  $prompt_preview"
  done
}

# ============================================================================
# Main
# ============================================================================

case "${1:-help}" in
  new)      shift; cmd_new "$@" ;;
  propose)  cmd_propose "$2" ;;
  critique) cmd_critique "$2" ;;
  vote)     cmd_vote "$2" ;;
  verdict)  cmd_verdict "$2" ;;
  run)      shift; cmd_run "$@" ;;
  check)    cmd_check ;;
  status)   cmd_status "$2" ;;
  list|ls)  cmd_list ;;
  help|--help|-h)
    echo "Usage: council.sh <command> [args]"
    echo ""
    echo "Commands:"
    echo "  check                 Sanity check all models (run this first!)"
    echo "  run \"question\"        Full pipeline (propose -> critique -> vote -> verdict)"
    echo "  run --file q.md       Full pipeline from file"
    echo "  new \"question\"        Create new session"
    echo "  propose <session>     Phase 1: all models propose solutions"
    echo "  critique <session>    Phase 2: all models critique proposals"
    echo "  vote <session>        Phase 3: all models vote"
    echo "  verdict <session>     Phase 4: judge synthesizes verdict"
    echo "  status <session>      Show session status"
    echo "  list                  List all sessions"
    echo ""
    echo "Models configured: ${#COUNCIL_MODELS[@]}"
    echo "Judge: $JUDGE_MODEL"
    ;;
  *)
    err "Unknown command: $1"
    exit 1
    ;;
esac
