#!/usr/bin/env bash
# Bootstrap / update of the AI Engineering Harness (this repository is the template).
# Usage:
#   ./scripts/init-harness.sh /path/to/project [name] [--adapters=list|all|none] [--fill] [--enrich]
#   ./scripts/init-harness.sh /path/to/project --update [--adapters=list]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KIT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATE="$KIT_ROOT/template"
ADAPTERS_ROOT="$KIT_ROOT/adapters"
KIT_VERSION="$(tr -d '[:space:]' < "$KIT_ROOT/VERSION" 2>/dev/null || echo unknown)"

TARGET=""
PROJECT_NAME=""
ADAPTERS_CSV="agents-md"
ADAPTERS_EXPLICIT=0
MODE="install"
RUN_FILL=0
RUN_ENRICH=0

usage() {
  cat >&2 <<'EOF'
Usage:
  ./scripts/init-harness.sh /path/to/project [name] [--adapters=list|all|none] [--fill] [--enrich]
  ./scripts/init-harness.sh /path/to/project --update [--adapters=list]

This repository is the *template*. The target project receives .ai-harness/ (do not copy the whole kit).

Adapters: cursor, copilot, claude, windsurf, continue, aider, agents-md, jetbrains, all, none
Install default: --adapters=agents-md (open AGENTS.md convention; the harness does not depend on any tool)
--update           refreshes the canonical rules without deleting Knowledge/Specs/project.md
--fill             after install/update, runs fill-harness.py
--enrich           after fill, runs deep-fill + enrich
EOF
}

for arg in "$@"; do
  case "$arg" in
    --adapters=*)
      ADAPTERS_CSV="${arg#--adapters=}"
      ADAPTERS_EXPLICIT=1
      ;;
    --update)
      MODE="update"
      ;;
    --fill)
      RUN_FILL=1
      ;;
    --enrich)
      RUN_FILL=1
      RUN_ENRICH=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      if [[ -z "$TARGET" ]]; then
        TARGET="$arg"
      elif [[ -z "$PROJECT_NAME" ]]; then
        PROJECT_NAME="$arg"
      else
        echo "Unexpected argument: $arg" >&2
        usage
        exit 1
      fi
      ;;
  esac
done

if [[ -z "$TARGET" ]]; then
  usage
  exit 1
fi

if [[ ! -d "$TEMPLATE" ]]; then
  echo "Template not found at: $TEMPLATE" >&2
  exit 1
fi

mkdir -p "$TARGET"
TARGET="$(cd "$TARGET" && pwd)"
PROJECT_NAME="${PROJECT_NAME:-$(basename "$TARGET")}"

if [[ "$TARGET" == "$KIT_ROOT" ]]; then
  echo "The target is the template kit itself. Point to another repository." >&2
  exit 1
fi

HARNESS_DST="$TARGET/.ai-harness"

normalize_id() {
  local id="$1"
  id="$(echo "$id" | tr '[:upper:]' '[:lower:]')"
  id="${id#"${id%%[![:space:]]*}"}"
  id="${id%"${id##*[![:space:]]}"}"
  printf '%s' "$id"
}

known_adapter() {
  case "$1" in
    none|""|cursor|copilot|github-copilot|claude|claude-code|windsurf|continue|aider|agents-md|agents|jetbrains)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

replace_project_placeholders() {
  local root="$1"
  local escaped
  escaped="$(printf '%s' "$PROJECT_NAME" | sed -e 's/[\/&]/\\&/g')"
  while IFS= read -r -d '' file; do
    if grep -q '{{PROJECT}}' "$file" 2>/dev/null; then
      sed -i "s/{{PROJECT}}/${escaped}/g" "$file"
    fi
  done < <(find "$root" -type f -print0)
}

# Copy an adapter without overwriting a project file that does not belong to the harness.
install_file() {
  local src="$1" dst="$2" label="$3"
  mkdir -p "$(dirname "$dst")"
  if [[ -f "$dst" ]] && ! grep -q 'ai-harness' "$dst"; then
    echo "  ! $label: $dst already exists and is not from the harness — not overwritten (add: see .ai-harness/agents.md)"
    return 0
  fi
  cp "$src" "$dst"
  echo "  • $label → $dst"
}

# Kit < 1.1 used upper-case names (AGENTS.md, Standards.md, LOOP.md…). Rename them to lower-case
# preserving content; works on case-sensitive and case-insensitive file systems.
migrate_legacy_names() {
  local count=0 f dir base lower tmp
  while IFS= read -r -d '' f; do
    dir="$(dirname "$f")"
    base="$(basename "$f")"
    lower="$(printf '%s' "$base" | tr '[:upper:]' '[:lower:]')"
    [[ "$base" == "$lower" ]] && continue
    if [[ -e "$dir/$lower" && ! "$f" -ef "$dir/$lower" ]]; then
      if cmp -s "$f" "$dir/$lower"; then
        rm -f "$f"
      else
        mv "$f" "$dir/$lower.legacy"
        echo "  ! conflict: $dir/$lower already exists — old content in $lower.legacy (review and delete)"
      fi
    else
      tmp="$dir/.harness-mv-$$"
      mv "$f" "$tmp"
      mv "$tmp" "$dir/$lower"
    fi
    count=$((count + 1))
  done < <(find "$HARNESS_DST" -type f -name '*.md' -print0)
  if [[ "$count" -gt 0 ]]; then
    echo "→ Migrated $count file(s) to lower-case names"
  fi
}

# Update stack packs: all of them if the project has none yet; otherwise only the ones the project kept.
update_stack_packs() {
  local src="$TEMPLATE/Knowledge/stacks" dst="$HARNESS_DST/Knowledge/stacks" f base kept=0
  mkdir -p "$dst"
  for f in "$dst/"*.md; do
    [[ -e "$f" && "$(basename "$f")" != "readme.md" ]] && kept=1
  done
  cp -a "$src/readme.md" "$dst/readme.md"
  for f in "$src/"*.md; do
    base="$(basename "$f")"
    [[ "$base" == "readme.md" ]] && continue
    if [[ "$kept" -eq 0 || -f "$dst/$base" ]]; then
      cp -a "$f" "$dst/$base"
    fi
  done
}

stamp_version() {
  printf '%s\n' "$KIT_VERSION" > "$HARNESS_DST/.kit-version"
}

if [[ "$ADAPTERS_CSV" == "all" ]]; then
  ADAPTERS_CSV="cursor,copilot,claude,windsurf,continue,aider,agents-md,jetbrains"
fi

ADAPTER_IDS=()
IFS=',' read -ra RAW_ADAPTER_IDS <<< "$ADAPTERS_CSV"
for raw in "${RAW_ADAPTER_IDS[@]}"; do
  id="$(normalize_id "$raw")"
  if ! known_adapter "$id"; then
    echo "Unknown adapter: $id" >&2
    usage
    exit 1
  fi
  ADAPTER_IDS+=("$id")
done

install_adapter() {
  local id="$1"
  case "$id" in
    none|"")
      return 0
      ;;
    # Destinations use the exact name each tool looks for (case-sensitive).
    cursor)
      install_file "$ADAPTERS_ROOT/cursor/rules/harness-sdd.mdc" "$TARGET/.cursor/rules/harness-sdd.mdc" "Cursor"
      ;;
    copilot|github-copilot)
      install_file "$ADAPTERS_ROOT/github-copilot/copilot-instructions.md" "$TARGET/.github/copilot-instructions.md" "GitHub Copilot"
      ;;
    claude|claude-code)
      install_file "$ADAPTERS_ROOT/claude-code/claude.md" "$TARGET/CLAUDE.md" "Claude Code"
      ;;
    windsurf)
      install_file "$ADAPTERS_ROOT/windsurf/.windsurfrules" "$TARGET/.windsurfrules" "Windsurf"
      ;;
    continue)
      install_file "$ADAPTERS_ROOT/continue/rules/harness-sdd.md" "$TARGET/.continue/rules/harness-sdd.md" "Continue"
      ;;
    aider)
      install_file "$ADAPTERS_ROOT/aider/conventions.md" "$TARGET/CONVENTIONS.md" "Aider"
      ;;
    agents-md|agents)
      install_file "$ADAPTERS_ROOT/agents-md/agents.md" "$TARGET/AGENTS.md" "AGENTS.md (open convention)"
      ;;
    jetbrains)
      install_file "$ADAPTERS_ROOT/jetbrains/rules/harness.md" "$TARGET/.aiassistant/rules/harness.md" "JetBrains AI"
      ;;
    *)
      echo "Unknown adapter: $id" >&2
      exit 1
      ;;
  esac
}

install_adapters() {
  echo "→ Installing adapters ($ADAPTERS_CSV)"
  for id in "${ADAPTER_IDS[@]}"; do
    install_adapter "$id"
  done
}

ensure_gitignore() {
  local gitignore="$TARGET/.gitignore"
  local ignore_block=$'.ai-harness/Runtime/state/runs/\n.ai-harness/Runtime/sandbox/worktrees/\n.ai-harness/Runtime/state/CURRENT'
  if [[ -f "$gitignore" ]]; then
    if ! grep -qF '.ai-harness/Runtime/state/runs/' "$gitignore"; then
      printf '\n# AI Engineering Harness (ephemeral)\n%s\n' "$ignore_block" >> "$gitignore"
      echo "→ Entries added to .gitignore"
    fi
  else
    printf '# AI Engineering Harness (ephemeral)\n%s\n' "$ignore_block" > "$gitignore"
    echo "→ .gitignore created"
  fi
}

update_canonical() {
  echo "→ Updating canonical rules → $HARNESS_DST (kit $KIT_VERSION)"
  cp -a "$TEMPLATE/agents.md" "$HARNESS_DST/agents.md"
  cp -a "$TEMPLATE/readme.md" "$HARNESS_DST/readme.md"

  mkdir -p "$HARNESS_DST/Agents"
  local f base
  for f in "$TEMPLATE/Agents/"*.md; do
    base="$(basename "$f")"
    if [[ "$base" == "project.md" && -f "$HARNESS_DST/Agents/project.md" ]]; then
      continue
    fi
    cp -a "$f" "$HARNESS_DST/Agents/"
  done

  cp -a "$TEMPLATE/Workflows/." "$HARNESS_DST/Workflows/"
  cp -a "$TEMPLATE/Governance/." "$HARNESS_DST/Governance/"
  cp -a "$TEMPLATE/Tools/." "$HARNESS_DST/Tools/"
  cp -a "$TEMPLATE/Specification/readme.md" "$HARNESS_DST/Specification/readme.md"
  mkdir -p "$HARNESS_DST/Specification/templates"
  cp -a "$TEMPLATE/Specification/templates/." "$HARNESS_DST/Specification/templates/"

  cp -a "$TEMPLATE/Runtime/loop.md" "$HARNESS_DST/Runtime/loop.md"
  cp -a "$TEMPLATE/Runtime/run.md" "$HARNESS_DST/Runtime/run.md"
  cp -a "$TEMPLATE/Runtime/readme.md" "$HARNESS_DST/Runtime/readme.md"
  mkdir -p "$HARNESS_DST/Runtime/sandbox" "$HARNESS_DST/Runtime/state/templates"
  cp -a "$TEMPLATE/Runtime/sandbox/readme.md" "$HARNESS_DST/Runtime/sandbox/readme.md"
  cp -a "$TEMPLATE/Runtime/state/readme.md" "$HARNESS_DST/Runtime/state/readme.md"
  cp -a "$TEMPLATE/Runtime/state/templates/." "$HARNESS_DST/Runtime/state/templates/"

  update_stack_packs

  mkdir -p "$HARNESS_DST/Knowledge/ADR"
  cp -a "$TEMPLATE/Knowledge/readme.md" "$HARNESS_DST/Knowledge/readme.md"
  cp -a "$TEMPLATE/Knowledge/ADR/readme.md" "$HARNESS_DST/Knowledge/ADR/readme.md"
  cp -a "$TEMPLATE/Knowledge/ADR/template.md" "$HARNESS_DST/Knowledge/ADR/template.md"

  replace_project_placeholders "$HARNESS_DST"
  stamp_version
}

run_python_chain() {
  if [[ "$RUN_FILL" -eq 0 ]]; then
    return 0
  fi
  if ! command -v python3 >/dev/null 2>&1; then
    echo "python3 not found — skip --fill/--enrich or install Python 3." >&2
    exit 1
  fi
  echo "→ fill-harness.py"
  python3 "$SCRIPT_DIR/fill-harness.py" "$TARGET"
  if [[ "$RUN_ENRICH" -eq 1 ]]; then
    echo "→ deep-fill-harness.py"
    python3 "$SCRIPT_DIR/deep-fill-harness.py" "$TARGET"
    echo "→ enrich-harness.py"
    python3 "$SCRIPT_DIR/enrich-harness.py" "$TARGET"
  fi
}

if [[ "$MODE" == "update" ]]; then
  if [[ ! -d "$HARNESS_DST" ]]; then
    echo "$HARNESS_DST does not exist — install first (without --update)." >&2
    exit 1
  fi
  migrate_legacy_names
  update_canonical
  if [[ "$ADAPTERS_EXPLICIT" -eq 1 ]]; then
    install_adapters
  fi
  ensure_gitignore
  mkdir -p "$HARNESS_DST/Runtime/state/runs" "$HARNESS_DST/Runtime/sandbox/worktrees"
  run_python_chain
  cat <<EOF

AI Engineering Harness updated → $HARNESS_DST
Kit:                     $KIT_VERSION
Project:                 $PROJECT_NAME

Knowledge (architecture, domain, standards), kept stack packs, features and Agents/project.md were preserved.
Check: python3 $HARNESS_DST/Tools/bin/check-harness.py
If Governance had a project overlay, run: python3 $SCRIPT_DIR/enrich-harness.py $TARGET

EOF
  exit 0
fi

if [[ -d "$HARNESS_DST" ]]; then
  echo "$HARNESS_DST already exists — use --update to refresh the rules, or remove it to reinstall." >&2
  exit 1
fi

echo "→ Copying template → $HARNESS_DST (kit $KIT_VERSION)"
cp -a "$TEMPLATE" "$HARNESS_DST"
replace_project_placeholders "$HARNESS_DST"
stamp_version

mkdir -p "$HARNESS_DST/Runtime/state/runs"
mkdir -p "$HARNESS_DST/Runtime/sandbox/worktrees"
touch "$HARNESS_DST/Runtime/state/runs/.gitkeep"

install_adapters
ensure_gitignore
run_python_chain

cat <<EOF

AI Engineering Harness → $HARNESS_DST
Kit:                     $KIT_VERSION
Project:                 $PROJECT_NAME
Adapters:                $ADAPTERS_CSV

This project now uses the template. Next steps:
  1. Fill in Knowledge/ (architecture, domain, standards) and delete unused packs in Knowledge/stacks/ — or --fill/--enrich
  2. Adjust Tools/ to the stack + Governance/permissions.md
  3. Replace Specification/features/example
  4. Agents: read .ai-harness/agents.md
  5. Check: python3 .ai-harness/Tools/bin/check-harness.py  (optional git hook: --install-hook)

Update the rules later:
  $KIT_ROOT/scripts/init-harness.sh $TARGET --update

EOF
