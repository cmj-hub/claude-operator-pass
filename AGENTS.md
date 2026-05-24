# AGENTS.md — Behavior rules for claude-operator-pass

## Rules

1. **Always validate API key first.** Missing env var → tell user how to subscribe. Invalid → 401 → renewal link. Never call anonymously.
2. **Always load brand-config.json before calling.** Missing → route to onboarding.
3. **Always fetch the tool schema before calling.** Validate inputs against the published JSON Schema; ask for missing required fields before the API call.
4. **Never fabricate tool results.** If the API call fails, surface the actual error. Don't make up an answer.
5. **Respect rate limits.** If `retry_on_429` is true, retry once with exponential backoff. Otherwise surface 429 immediately.
6. **Cache the catalog.** Per `cache.tool_catalog_ttl_seconds`. Don't re-fetch on every call.
7. **Log every call.** If `usage.log_calls` is true, append to the log path with timestamp + tool slug + result summary.
8. **Warn at quota threshold.** If remaining quota drops below `usage.warn_at_remaining_quota_percent`, surface a warning before the next call.
9. **Pretty-print results, don't dump JSON.** Convert structured output into a human-readable summary unless user explicitly asks for raw.

## What the agent NEVER does

- Calls the API without OPERATOR_PASS_API_KEY (refuses anonymous calls)
- Auto-invokes a tool on the user's "won't call" list
- Retries on 401/402 (key invalid / subscription expired — these need user action)
- Calls more than once per request without explicit user confirmation
- Sends customer data to the API without explicit user confirmation
- Caches sensitive customer data outside `.operator-pass-cache`

## Onboarding flow

Missing brand-config + SOUL on first invocation → route to `skills/operator-pass-onboarding`.
