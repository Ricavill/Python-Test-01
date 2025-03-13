import json
import os

from huggingface_hub import InferenceClient

from config.error import ValidationException

LLAMA_TOKEN = os.getenv("LLAMA_TOKEN")


class Llama:

    def __init__(self):
        self.client = InferenceClient(
            provider="novita",
            api_key=LLAMA_TOKEN,
        )
        self.messages = []

    def add_user_message(self, content):
        self.messages.append({
            "role": "user",
            "content": content
        })

    def get_response(self):
        completion = self.client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages=self.messages,
            max_tokens=500,
        )
        return completion.choices[0].message.content

    def convert_json_str_to_json(self, json_str):
        json_str = json_str.strip('```json').strip('```')
        try:
            json_dict = json.loads(json_str)
            return json_dict
        except json.decoder.JSONDecodeError:
            raise ValidationException("Llama JSON is invalid")
