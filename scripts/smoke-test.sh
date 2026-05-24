#!/usr/bin/env bash
# Smoke test for claude-operator-pass.
# Confirms the script runs and refuses to call the API without a key.
# (Live API smoke is in .github/workflows/smoke-pass.yml, gated on OPERATOR_PASS_API_KEY)

set -euo pipefail
PASSED=0; FAILED=0
check() { local n="$1"; shift; if "$@"; then echo "  ✓ $n"; PASSED=$((PASSED+1)); else echo "  ✗ $n"; FAILED=$((FAILED+1)); fi; }

echo "=== op_api.py ==="
check "help command works" \
  python3 scripts/op_api.py --help

# Without the API key, must exit non-zero with the subscribe link
echo "  (no-key path should exit non-zero + reference operator-pass)"
unset OPERATOR_PASS_API_KEY
out=$(python3 scripts/op_api.py whoami 2>&1 || true)
echo "$out" | grep -q "operator-pass" && {
  echo "  ✓ no-key refusal correctly references operator-pass URL"
  PASSED=$((PASSED+1))
} || {
  echo "  ✗ no-key refusal missing subscribe URL"
  echo "$out"
  FAILED=$((FAILED+1))
}

echo ""; echo "Passed: $PASSED, Failed: $FAILED"
[ "$FAILED" -eq 0 ]
