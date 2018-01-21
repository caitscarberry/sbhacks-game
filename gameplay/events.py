import json

class GameEvent:
    def __init__(self, params):
        self.params = params

    def serialize(self):
        return json.dumps(self.params)

    def deserialize(string):
        return GameEvent(json.loads(string))