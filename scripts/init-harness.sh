#!/usr/bin/env bash
# Bootstrap do AI Engineering Harness.
# Uso:
#   ./scripts/init-harness.sh /caminho/projeto [nome] [--adapters=cursor,copilot,...|all|none]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KIT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATE="$KIT_ROOT/template"
ADAPTERS_ROOT="$KIT_ROOT/adapters"

TARGET=""
PROJECT_NAME=""
ADAPTERS_CSV="cursor"

usage() {
  cat >&2 <<'EOF'
Uso: ./scripts/init-harness.sh /caminho/projeto [nome-do-projeto] [--adapters=lista|all|none]

Adapters: cursor, copilot, claude, windsurf, continue, aider, agents-md, jetbrains, all, none
Padrão: --adapters=cursor
Instala .ai-harness/ no projeto alvo.
EOF
}

for arg in "$@"; do
  case "$arg" in
    --adapters=*)
      ADAPTERS_CSV="${arg#--adapters=}"
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
        echo "Argumento inesperado: $arg" >&2
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

TARGET="$(cd "$TARGET" && pwd)"
PROJECT_NAME="${PROJECT_NAME:-$(basename "$TARGET")}"

if [[ ! -d "$TEMPLATE" ]]; then
  echo "Template não encontrado em: $TEMPLATE" >&2
  exit 1
fi

HARNESS_DST="$TARGET/.ai-harness"

if [[ -d "$HARNESS_DST" ]]; then
  echo "Já existe $HARNESS_DST — abortando para não sobrescrever." >&2
  exit 1
fi

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

if [[ "$ADAPTERS_CSV" == "all" ]]; then
  ADAPTERS_CSV="cursor,copilot,claude,windsurf,continue,aider,agents-md,jetbrains"
fi

ADAPTER_IDS=()
IFS=',' read -ra RAW_ADAPTER_IDS <<< "$ADAPTERS_CSV"
for raw in "${RAW_ADAPTER_IDS[@]}"; do
  id="$(normalize_id "$raw")"
  if ! known_adapter "$id"; then
    echo "Adapter desconhecido: $id" >&2
    usage
    exit 1
  fi
  ADAPTER_IDS+=("$id")
done

echo "→ Copiando template → $HARNESS_DST"
cp -a "$TEMPLATE" "$HARNESS_DST"

while IFS= read -r -d '' file; do
  if grep -q '{{PROJECT}}' "$file" 2>/dev/null; then
    sed -i "s/{{PROJECT}}/${PROJECT_NAME}/g" "$file"
  fi
done < <(find "$HARNESS_DST" -type f -print0)

mkdir -p "$HARNESS_DST/Runtime/state/runs"
mkdir -p "$HARNESS_DST/Runtime/sandbox/worktrees"
touch "$HARNESS_DST/Runtime/state/runs/.gitkeep"

install_adapter() {
  local id="$1"
  case "$id" in
    none|"")
      return 0
      ;;
    cursor)
      mkdir -p "$TARGET/.cursor/rules"
      cp -a "$ADAPTERS_ROOT/cursor/rules/"*.mdc "$TARGET/.cursor/rules/"
      echo "  • Cursor → $TARGET/.cursor/rules/*.mdc"
      ;;
    copilot|github-copilot)
      local dst="$TARGET/.github/copilot-instructions.md"
      mkdir -p "$(dirname "$dst")"
      cp -a "$ADAPTERS_ROOT/github-copilot/copilot-instructions.md" "$dst"
      echo "  • GitHub Copilot → $dst"
      ;;
    claude|claude-code)
      cp -a "$ADAPTERS_ROOT/claude-code/CLAUDE.md" "$TARGET/CLAUDE.md"
      echo "  • Claude Code → $TARGET/CLAUDE.md"
      ;;
    windsurf)
      cp -a "$ADAPTERS_ROOT/windsurf/.windsurfrules" "$TARGET/.windsurfrules"
      echo "  • Windsurf → $TARGET/.windsurfrules"
      ;;
    continue)
      local dst="$TARGET/.continue/rules/harness-sdd.md"
      mkdir -p "$(dirname "$dst")"
      cp -a "$ADAPTERS_ROOT/continue/rules/harness-sdd.md" "$dst"
      echo "  • Continue → $dst"
      ;;
    aider)
      cp -a "$ADAPTERS_ROOT/aider/CONVENTIONS.md" "$TARGET/CONVENTIONS.md"
      echo "  • Aider → $TARGET/CONVENTIONS.md"
      ;;
    agents-md|agents)
      cp -a "$ADAPTERS_ROOT/agents-md/AGENTS.md" "$TARGET/AGENTS.md"
      echo "  • AGENTS.md → $TARGET/AGENTS.md"
      ;;
    jetbrains)
      local dst="$TARGET/.aiassistant/rules/harness.md"
      mkdir -p "$(dirname "$dst")"
      cp -a "$ADAPTERS_ROOT/jetbrains/rules/harness.md" "$dst"
      echo "  • JetBrains AI → $dst"
      ;;
    *)
      echo "Adapter desconhecido: $id" >&2
      exit 1
      ;;
  esac
}

echo "→ Instalando adapters ($ADAPTERS_CSV)"
for id in "${ADAPTER_IDS[@]}"; do
  install_adapter "$id"
done

GITIGNORE="$TARGET/.gitignore"
IGNORE_BLOCK=$'.ai-harness/Runtime/state/runs/\n.ai-harness/Runtime/sandbox/worktrees/\n.ai-harness/Runtime/state/CURRENT'

if [[ -f "$GITIGNORE" ]]; then
  if ! grep -qF '.ai-harness/Runtime/state/runs/' "$GITIGNORE"; then
    printf '\n# AI Engineering Harness (ephemeral)\n%s\n' "$IGNORE_BLOCK" >> "$GITIGNORE"
    echo "→ Entradas adicionadas em .gitignore"
  fi
else
  printf '# AI Engineering Harness (ephemeral)\n%s\n' "$IGNORE_BLOCK" > "$GITIGNORE"
  echo "→ .gitignore criado"
fi

cat <<EOF

AI Engineering Harness → $HARNESS_DST
Projeto:                 $PROJECT_NAME
Adapters:                $ADAPTERS_CSV

Próximos passos:
  1. Preencher Knowledge/ (Architecture, Domain, Standards)
  2. Ajustar Tools/ à stack + Governance/permissions.md
  3. Substituir Specification/features/example
  4. docs/adoption-guide.md · docs/ide-adapters.md · docs/sdlc-mapping.md

EOF
