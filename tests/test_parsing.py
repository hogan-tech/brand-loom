"""Tests for JSON response parsing."""

import pytest

from brand_loom.providers.parsing import parse_json_response


def test_fenced_json():
    text = 'Here is the result:\n```json\n{"key": "value"}\n```\nDone.'
    assert parse_json_response(text) == {"key": "value"}


def test_fenced_no_lang_tag():
    text = '```\n{"key": "value"}\n```'
    assert parse_json_response(text) == {"key": "value"}


def test_raw_json_object():
    assert parse_json_response('{"a": 1}') == {"a": 1}


def test_raw_json_array():
    assert parse_json_response('[1, 2, 3]') == [1, 2, 3]


def test_embedded_json():
    text = 'Sure! Here is your data: {"items": [1, 2]} — hope that helps!'
    assert parse_json_response(text) == {"items": [1, 2]}


def test_embedded_json_array():
    text = "The list is: [1, 2, 3] and that's it."
    assert parse_json_response(text) == [1, 2, 3]


def test_no_json_raises():
    with pytest.raises(ValueError, match="No valid JSON"):
        parse_json_response("This has no JSON at all")


def test_whitespace_padding():
    text = "   \n  {\"x\": 42}  \n  "
    assert parse_json_response(text) == {"x": 42}
