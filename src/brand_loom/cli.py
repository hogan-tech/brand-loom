"""brand-loom CLI — run skills from the command line.

Usage:
    brand-loom run <skill> --text "..." [--provider fake] [--brand path.json]
    brand-loom chain <skills> --text "..." [--provider fake] [--brand path.json]
    brand-loom list
"""

from __future__ import annotations

import argparse
import json
import sys

from brand_loom.agent import _ensure_skills_loaded, run_chain, run_skill
from brand_loom.providers.base import use_provider
from brand_loom.skills.registry import list_skills


def _load_brand_context(path: str | None) -> dict | None:
    if not path:
        return None
    with open(path) as f:
        return json.load(f)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="brand-loom",
        description="Open-source marketing skills that run on any model.",
    )
    sub = parser.add_subparsers(dest="command")

    # brand-loom run <skill>
    run_p = sub.add_parser("run", help="Run a single skill")
    run_p.add_argument("skill", help="Skill name (e.g. hook, caption, hashtags)")
    run_p.add_argument("--text", required=True, help="Input text")
    run_p.add_argument("--provider", default="fake", help="Provider name (default: fake)")
    run_p.add_argument("--brand", help="Path to brand_context JSON file")

    # brand-loom chain <skills>
    chain_p = sub.add_parser("chain", help="Run a linear skill chain")
    chain_p.add_argument("skills", help="Comma-separated skill names (e.g. hook,caption)")
    chain_p.add_argument("--text", required=True, help="Input text")
    chain_p.add_argument("--provider", default="fake", help="Provider name (default: fake)")
    chain_p.add_argument("--brand", help="Path to brand_context JSON file")

    # brand-loom list
    sub.add_parser("list", help="List available skills")

    args = parser.parse_args(argv)

    if args.command == "run":
        use_provider(args.provider)
        brand_ctx = _load_brand_context(args.brand)
        result = run_skill(args.skill, args.text, brand_context=brand_ctx)
        print(result.text)
    elif args.command == "chain":
        use_provider(args.provider)
        brand_ctx = _load_brand_context(args.brand)
        names = [n.strip() for n in args.skills.split(",")]
        result = run_chain(names, args.text, brand_context=brand_ctx)
        print(result.text)
    elif args.command == "list":
        _ensure_skills_loaded()
        for name in list_skills():
            print(f"  {name}")
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
