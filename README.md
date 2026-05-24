# claude-operator-pass

A Claude Code skill that wraps the **JMC tools API** for cross-runtime
agent use. Cold Email Linter, EVP Generator, Pipeline Calculator, GEO
Visibility Audit, Competitive Teardown, Paid Media Teardown, and 16
more — all server-side, schema-validated, real-result endpoints (not
prompts).

Subscriber-gated. Bring your own [Operator Pass](https://jaymountconsulting.com/operator-pass) API key.

## What it does

Each JMC tool is a deterministic, schema-validated endpoint. This
skill:

1. Detects the tool the user wants from intent
2. Fetches the per-tool input schema from the API
3. Validates / collects the required inputs
4. Calls the endpoint (POST)
5. Pretty-prints the structured response + offers the natural next step

No LLM calls inside the skill itself — the skill is the wiring; the
API is the engine.

## Available tools (current catalog)

The skill calls the live catalog endpoint, so this list is always
current — but as of v0.1.0 the API exposes 22+ tools across 4
categories. Examples:

| Category | Slug | Job |
|---|---|---|
| Outbound | `cold-email-linter` | Per-email score + line-level rewrite |
| Outbound | `linkedin-post-critic` | Critique + 3 rewrites |
| Outbound | `nurture-sequence-planner` | 5-email nurture stream |
| Foundation | `evp-generator` | EVP variants by Schwartz tier |
| Foundation | `evp-brief-generator` | Structured 3-tier brief |
| Foundation | `persona-from-crm` | CSV → clusters → PSPs |
| Demand | `geo-visibility` | URL → AI-visibility 5-dim score |
| Demand | `competitive-teardown` | URL → 6-bullet teardown |
| Demand | `paid-media-teardown` | 5-lever ad teardown |
| Revenue | `cohort-economics-modeler` | LTV/payback/cohort contribution |
| Revenue | `blended-gtm-dashboard` | 11-slider modeler |
| Revenue | `gtm-architecture-diagrammer` | Canvas + AI coherence audit |

Full live catalog: `/operator-pass list`.

## Auth

Bring your own API key:

```bash
export OPERATOR_PASS_API_KEY="op_live_..."
```

The skill detects a missing / invalid key and tells the user how to
subscribe. **No anonymous calls.**

Get a key at **[jaymountconsulting.com/operator-pass](https://jaymountconsulting.com/operator-pass)**
— $2,400/yr Founder rate, locked through July 16 2026. 100 Founder
seats available.

## Sub-skills

| Sub-skill | Job |
|---|---|
| `operator-pass-call` | Invoke a specific tool by slug; validates inputs, calls API, pretty-prints |
| `operator-pass-list` | Live catalog list with slugs + descriptions + per-tool schema detail |

## Install

### Claude Code

```bash
/plugin marketplace add cmj-hub/claude-operator-pass
/plugin install operator-pass
```

### One-line install

```bash
curl -fsSL https://raw.githubusercontent.com/cmj-hub/claude-operator-pass/main/install.sh | bash
```

## Usage

```
> Lint this cold email: [paste]
```

→ Routes to `operator-pass-call`, calls `cold-email-linter`, returns
per-line scores + rewrite recommendations.

```
> Generate an EVP for Series-B SaaS in pipeline-gap pain, Tier 3
```

→ Routes to `operator-pass-call`, calls `evp-generator`, returns
schema-validated variants.

```
> What tools are available?
```

→ Routes to `operator-pass-list`, fetches live catalog, groups by
category.

```
> GEO audit on https://my-site.com
```

→ Routes to `operator-pass-call`, calls `geo-visibility`, returns the
5-dim score + ranked fixes.

## Plugs into

The free framework skills give you the methodology. The API gives you
the deterministic execution layer:

- **[claude-cold-email](https://github.com/cmj-hub/claude-cold-email)** + `cold-email-linter` → write the email by framework, validate by API
- **[claude-evp](https://github.com/cmj-hub/claude-evp)** + `evp-generator` → think through tiers manually, then generate variants at scale
- **[claude-psp](https://github.com/cmj-hub/claude-psp)** + `persona-from-crm` → think through PSP manually, then cluster real prospect data into segment PSPs

## Operator Pass

[Operator Pass](https://jaymountconsulting.com/operator-pass) is the
all-access subscription to:

- The full Compounding Engine course catalog (27 courses, 4 modules)
- The 22-tool API (this skill wraps it)
- Weekly office hours with Jay
- Founder pricing locked at **$2,400/yr** through **July 16 2026** —
  only 100 Founder seats available

→ [jaymountconsulting.com/operator-pass](https://jaymountconsulting.com/operator-pass)

## License

MIT (skill code). The API itself is subscription-gated. Built by
[Jay Mount Consulting](https://jaymountconsulting.com).
