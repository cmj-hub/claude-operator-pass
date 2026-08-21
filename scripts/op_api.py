#!/usr/bin/env python3
"""
op_api.py — Operator Pass API client + key validator + catalog fetcher.

Deterministic CLI wrapper around the JMC API. Validates the API key,
fetches the live tool catalog, fetches per-tool schemas, calls tools
with JSON inputs. Handles 401/402/429/5xx per the brand-config rules.

USAGE:
    OPERATOR_PASS_API_KEY=jmc_live_... python3 op_api.py whoami
    OPERATOR_PASS_API_KEY=jmc_live_... python3 op_api.py list
    OPERATOR_PASS_API_KEY=jmc_live_... python3 op_api.py schema cold-email-linter
    OPERATOR_PASS_API_KEY=jmc_live_... python3 op_api.py call cold-email-linter --input '{"email":"..."}'

Zero non-stdlib deps. Uses urllib + json.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional


DEFAULT_BASE_URL = "https://api.jaymountconsulting.com/v1"
DEFAULT_TIMEOUT_S = 30
USER_AGENT = "claude-operator-pass/0.2 (https://github.com/JMC-Go-to-market/claude-operator-pass)"


def get_key() -> str:
    key = os.environ.get("OPERATOR_PASS_API_KEY", "").strip()
    if not key:
        sys.stderr.write(
            "ERROR: OPERATOR_PASS_API_KEY env var not set.\n"
            "Subscribe + get a key: https://jaymountconsulting.com/operator-pass\n"
        )
        sys.exit(2)
    return key


def base_url() -> str:
    return os.environ.get("OPERATOR_PASS_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def request(
    method: str,
    path: str,
    body: Optional[Dict[str, Any]] = None,
    timeout_s: int = DEFAULT_TIMEOUT_S,
    retry_on_429: bool = True,
) -> Dict[str, Any]:
    """Make an authenticated API request. Returns parsed JSON."""
    key = get_key()
    url = f"{base_url()}{path}"
    headers = {
        "Authorization": f"Bearer {key}",
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    for attempt in range(2 if retry_on_429 else 1):
        req = urllib.request.Request(url, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout_s) as resp:
                raw = resp.read().decode("utf-8", errors="ignore")
                return {
                    "ok": True,
                    "status": resp.status,
                    "data": json.loads(raw) if raw else {},
                    "rate_remaining": resp.headers.get("X-RateLimit-Remaining"),
                }
        except urllib.error.HTTPError as err:
            body_text = err.read().decode("utf-8", errors="ignore")
            try:
                err_data = json.loads(body_text) if body_text else {}
            except json.JSONDecodeError:
                err_data = {"raw": body_text}

            if err.code == 401:
                sys.stderr.write(
                    "ERROR 401: API key invalid or expired.\n"
                    "Renew: https://jaymountconsulting.com/operator-pass\n"
                )
                return {"ok": False, "status": 401, "data": err_data}
            if err.code == 402:
                sys.stderr.write(
                    "ERROR 402: Operator Pass subscription expired.\n"
                    "Renew: https://jaymountconsulting.com/operator-pass\n"
                )
                return {"ok": False, "status": 402, "data": err_data}
            if err.code == 429:
                if retry_on_429 and attempt == 0:
                    retry_after = int(err.headers.get("Retry-After", "30"))
                    sys.stderr.write(f"429 rate-limited — retrying in {retry_after}s...\n")
                    time.sleep(retry_after)
                    continue
                sys.stderr.write(f"ERROR 429: rate-limited. Try again later.\n")
                return {"ok": False, "status": 429, "data": err_data}
            sys.stderr.write(f"ERROR {err.code}: {body_text[:200]}\n")
            return {"ok": False, "status": err.code, "data": err_data}
        except (urllib.error.URLError, TimeoutError) as err:
            sys.stderr.write(f"ERROR network: {err}\n")
            return {"ok": False, "status": 0, "data": {"error": str(err)}}
    return {"ok": False, "status": 0, "data": {}}


# ---------------- Commands ----------------

def cmd_whoami() -> int:
    result = request("GET", "/me")
    if not result["ok"]:
        return 1
    data = result["data"]
    print(f"User:             {data.get('user_id', '—')}")
    print(f"Plan:             {data.get('plan', '—')}")
    print(f"Quota remaining:  {data.get('rate_limit_remaining', '—')}")
    print(f"Pass valid until: {data.get('valid_until', '—')}")
    return 0


def cmd_list() -> int:
    result = request("GET", "/tools")
    if not result["ok"]:
        return 1
    tools = result["data"].get("tools", result["data"]) if isinstance(result["data"], dict) else result["data"]
    if not isinstance(tools, list):
        print(json.dumps(result["data"], indent=2))
        return 0
    # Group by category
    by_cat: Dict[str, list] = {}
    for t in tools:
        cat = t.get("category", "uncategorized")
        by_cat.setdefault(cat, []).append(t)
    for cat, items in by_cat.items():
        print(f"\n## {cat}")
        for t in items:
            print(f"  {t.get('slug', '?').ljust(35)} {t.get('description', '')[:80]}")
    print(f"\nTotal: {len(tools)} tools")
    return 0


def cmd_schema(slug: str) -> int:
    result = request("GET", f"/tools/{urllib.parse.quote(slug)}/schema")
    if not result["ok"]:
        return 1
    print(json.dumps(result["data"], indent=2))
    return 0


def cmd_call(slug: str, inputs: Dict[str, Any]) -> int:
    result = request("POST", f"/tools/{urllib.parse.quote(slug)}", body=inputs)
    if not result["ok"]:
        return 1
    print(json.dumps(result["data"], indent=2))
    if result.get("rate_remaining"):
        sys.stderr.write(f"(rate_remaining: {result['rate_remaining']})\n")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("whoami", help="Validate API key + show plan + quota")
    sub.add_parser("list", help="Fetch live tool catalog")
    p_schema = sub.add_parser("schema", help="Fetch schema for a tool")
    p_schema.add_argument("slug")
    p_call = sub.add_parser("call", help="Call a tool with JSON inputs")
    p_call.add_argument("slug")
    p_call.add_argument("--input", default="{}", help="JSON input")
    p_call.add_argument("--input-file", default=None, help="Path to JSON input file")

    args = parser.parse_args()

    if args.cmd == "whoami":
        return cmd_whoami()
    if args.cmd == "list":
        return cmd_list()
    if args.cmd == "schema":
        return cmd_schema(args.slug)
    if args.cmd == "call":
        if args.input_file:
            with open(args.input_file, "r", encoding="utf-8") as f:
                inputs = json.load(f)
        else:
            try:
                inputs = json.loads(args.input)
            except json.JSONDecodeError as err:
                sys.stderr.write(f"Bad --input JSON: {err}\n")
                return 2
        return cmd_call(args.slug, inputs)
    return 2


if __name__ == "__main__":
    sys.exit(main())
