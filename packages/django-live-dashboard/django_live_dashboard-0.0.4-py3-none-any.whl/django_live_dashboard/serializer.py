import json


def serialize(data):
    return json.dumps(data)


def deserialize(message):
    return json.loads(message)
