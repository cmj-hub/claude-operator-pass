# Changelog

## [0.1.0] — 2026-05-23

Initial release.

### Added
- Main `operator-pass/` orchestrator skill
- Sub-skill `operator-pass-call` — invoke a specific tool by slug
- Sub-skill `operator-pass-list` — live catalog list with schemas
- One-line install script
- Claude Code plugin manifest

### Notes
- Requires active Operator Pass subscription + API key
- All calls go to api.jaymountconsulting.com/v1/tools/<slug>
- No anonymous calls — skill refuses if OPERATOR_PASS_API_KEY is missing
