from utils.json_utils import convert_json_str_to_json


def test_valid_json():
    json_str = '{"key": "value"}'
    expected = {"key": "value"}
    assert convert_json_str_to_json(json_str) == expected


def test_json_with_json_markers():
    json_str = '```json{"key": "value"}```'
    expected = {"key": "value"}
    assert convert_json_str_to_json(json_str) == expected


def test_json_with_extra_whitespace():
    json_str = ' ```  json {"key": "value"}   ``` '
    expected = {"key": "value"}
    assert convert_json_str_to_json(json_str) == expected

def test_invalid_json():
    json_str = '{key: value}'  # Invalid JSON format
    assert convert_json_str_to_json(json_str) is None


def test_empty_string():
    json_str = ''
    assert convert_json_str_to_json(json_str) is None


def test_none_input():
    assert convert_json_str_to_json(None) is None


def test_numeric_json():
    json_str = '42'
    expected = 42
    assert convert_json_str_to_json(json_str) == expected

def test_convert_number():
    json_str = 42
    assert convert_json_str_to_json(json_str) is None

def test_json_with_nested_structure():
    json_str = '{"outer": {"inner": "value"}}'
    expected = {"outer": {"inner": "value"}}
    assert convert_json_str_to_json(json_str) == expected
