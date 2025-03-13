import json

from config.error import ValidationException


def convert_json_str_to_json(self, json_str):
    json_str = json_str.strip('```json').strip('```')
    try:
        json_dict = json.loads(json_str)
        return json_dict
    except json.decoder.JSONDecodeError:
        return None