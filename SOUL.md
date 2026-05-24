# SOUL.md — Operator preferences for the Operator Pass API skill

This pack calls a real API on your behalf. SOUL.md captures HOW you
want it called — not voice fingerprints (that's for content skills),
but operational preferences.

## How I use the API

<2-3 sentences on your usage pattern. E.g. "I batch tool calls
weekly — Monday cold-email-linter on Wednesday's send queue, Friday
competitive-teardown on the top 3 prospects. I rarely call ad-hoc.">

## Tools I rely on most

<List 3-5 tools you call most often. The skill prioritizes these in
routing suggestions:>

- `cold-email-linter` — every Wednesday before send
- `competitive-teardown` — when new ICP prospects appear
- `evp-generator` — quarterly retier
- ...

## Tools I won't call

<List any tools you specifically don't want the skill auto-invoking.
E.g. expensive long-running ones, or tools whose schema you haven't
locked yet:>

- `<tool-slug>` — reason

## How I handle failures

<How should the skill react when the API returns 429 / 5xx / quota
exhaustion? E.g. "Retry once on 429 with 30s backoff. On 402
subscription-expired, surface the renewal link and stop. On 5xx,
log + skip + continue the batch.">

## Quota budget

<If you have a known monthly quota, document it. E.g. "1,000 calls/mo
included in my Pass tier. Warn me when I'm at 80%.">

---

## How the skill uses this

- Tool-routing suggestions prioritize your "rely on most" list
- Auto-skip your "won't call" tools
- Apply your failure-handling rules
- Surface quota warnings at your configured threshold

The framework rules (never call anonymously, never fabricate results,
never auto-invoke without permission) are enforced regardless.
