class GameEvent:
    def __init__(self):
        pass

    #static method
    def deserialize(string):
        event_type = string.split(",")[0]
        if event_type == "player":
            return PlayerEvent.deserialize(string)

class PlayerEvent(GameEvent):
    def __init__(self, player_id, x, y, code):
        self.type = "player"
        self.player_id = player_id
        self.x = x
        self.y = y
        self.code = code

    def serialize(self):
        return ("player,%d,%d,%d,%s" % (self.player_id, self.x, self.y, self.code)).encode('utf-8')

    #static method
    def deserialize(string):
        player_id, x, y, code = string.split(",")[1:]
        player_id = int(player_id)
        x = float(x)
        y = float(y)
        return PlayerEvent(player_id, x, y, code)