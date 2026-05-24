#!/usr/bin/env bash
# install.sh — Install claude-operator-pass skill ecosystem
# Usage: curl -fsSL https://raw.githubusercontent.com/cmj-hub/claude-operator-pass/main/install.sh | bash

set -euo pipefail

REPO_URL="https://github.com/cmj-hub/claude-operator-pass"
SKILLS_DIR="${HOME}/.claude/skills"

if ! command -v git >/dev/null 2>&1; then
    echo "ERROR: git is required but not installed." >&2
    exit 1
fi

mkdir -p "$SKILLS_DIR"
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

echo "Installing claude-operator-pass..."
git clone --depth 1 "$REPO_URL" "$TEMP_DIR" >/dev/null 2>&1

echo "  + operator-pass (orchestrator)"
rm -rf "$SKILLS_DIR/operator-pass"
cp -r "$TEMP_DIR/operator-pass" "$SKILLS_DIR/"

for skill_dir in "$TEMP_DIR/skills"/operator-pass-*; do
    if [[ -d "$skill_dir" ]]; then
        skill_name=$(basename "$skill_dir")
        rm -rf "${SKILLS_DIR:?}/$skill_name"
        cp -r "$skill_dir" "$SKILLS_DIR/"
        echo "  + $skill_name"
    fi
done

echo ""
echo "Done. Restart Claude Code to pick up the new skill."
echo ""
echo "Setup:"
echo "  export OPERATOR_PASS_API_KEY=\"op_live_...\""
echo "  Get a key at https://jaymountconsulting.com/operator-pass"
echo ""
echo "Try it:"
echo "  > Lint this cold email: <paste>"
echo "  > What tools are available?"
echo ""
echo "Source:  $REPO_URL"
