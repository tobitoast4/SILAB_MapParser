import json

def read_json(file_name):
    with open(file_name, "r") as f:
        return json.load(f)

def write_json(file_name, data):
    with open(file_name, "w") as f:
        data = sorted(data)
        json.dump(data, f, indent=4) 