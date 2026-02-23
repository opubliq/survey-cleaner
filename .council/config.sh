#!/usr/bin/env bash
# Council configuration - models and settings
# Edit this file to add/remove models from the council
#
# IMPORTANT: COUNCIL_MODELS and COUNCIL_NAMES must have the same number
# of entries, in the same order. Run `./council.sh check` after editing.

# Models to include in the council (opencode format: provider/model)
# Comment out any model you want to exclude (comment the matching NAME too)
COUNCIL_MODELS=(
  "opencode/big-pickle"              #  1 - opencode zen (free)
  #"opencode/glm-5-free"              #  2 - opencode zen (free)
  "opencode/kimi-k2.5-free"          #  3 - opencode zen (free)
  "opencode/minimax-m2.5-free"       #  4 - opencode zen (free)
  "google/gemini-2.5-flash"          #  5 - direct Google API
  #"anthropic/claude-opus-4-6"        #  6 - direct Anthropic API
  #"anthropic/claude-sonnet-4-6"      #  7 - direct Anthropic API
  #"zai-coding-plan/glm-4.7"          #  8 - z.ai
  #"zai-coding-plan/glm-4.5"          #  9 - z.ai
  #"zai-coding-plan/glm-4.7-flash"    # 10 - z.ai flash
)

# Short names for display (MUST match order and count above)
COUNCIL_NAMES=(
  "oc-big-pickle"                    #  1
  #"oc-glm-5-free"                    #  2
  "oc-kimi-k2.5-free"               #  3
  "oc-minimax-m2.5-free"            #  4
  "google-gemini-2.5-flash"          #  5
  #"anth-claude-opus"                 #  6
  #"anth-claude-sonnet"               #  7
  #"zai-glm-4.7"                      #  8
  #"zai-glm-4.5"                      #  9
  #"zai-glm-4.7-flash"               # 10
)

# Judge model for final synthesis (pick a strong one)
JUDGE_MODEL="google/gemini-2.5-flash"
JUDGE_NAME="gemini-judge"

# Max parallel jobs (adjust based on rate limits)
MAX_PARALLEL=4

# Timeout per model call (seconds)
TIMEOUT=300
