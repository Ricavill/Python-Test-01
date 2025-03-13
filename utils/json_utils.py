import json


def convert_json_str_to_json(json_str: str):
    if not json_str or type(json_str) is not str:
        return None
    json_str = json_str.replace(' ', '').strip('```json').strip('```').strip()
    try:
        json_dict = json.loads(json_str)
        return json_dict
    except json.decoder.JSONDecodeError:
        return None
