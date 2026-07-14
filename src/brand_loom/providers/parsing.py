"""JSON response parsing — extract JSON from LLM text output.

Handles three shapes:
  1. Fenced: ```json ... ```
  2. Embedded: text before/after a JSON object/array
  3. Raw: the entire string is valid JSON
"""

from __future__ import annotations

import json
import re


def parse_json_response(text: str) -> dict | list:
    """Extract and parse JSON from an LLM response string.

    Tries fenced blocks first, then raw JSON, then embedded JSON.
    Raises ValueError if no valid JSON can be extracted.
    """
    # 1. Fenced code block
    m = re.search(r"```(?:json)?\s*\n?(.*?)```", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1).strip())
        except json.JSONDecodeError:
            pass

    # 2. Raw — entire string is JSON
    stripped = text.strip()
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        pass

    # 3. Embedded — find first { or [ and match to closing
    for start_char, end_char in [("{", "}"), ("[", "]")]:
        start = stripped.find(start_char)
        if start == -1:
            continue
        end = stripped.rfind(end_char)
        if end <= start:
            continue
        try:
            return json.loads(stripped[start : end + 1])
        except json.JSONDecodeError:
            continue

    raise ValueError(f"No valid JSON found in response: {text[:200]!r}")
