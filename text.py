import json

json_strings = ['{"name": "John", "age": 25}', '{"city": "New York", "country": "USA"}', '{"score": 95}']

final_json_string = json.dumps({k: v for json_str in json_strings for k, v in json.loads(json_str).items()}, indent=2)

print(final_json_string)