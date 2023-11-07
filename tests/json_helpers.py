import json
import os


def parse_json_file(path, filename):
    full_path = os.path.join(path, filename)
    with open(full_path, 'r') as file:
        return json.loads(file.read())




