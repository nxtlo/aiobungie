
class Player:
    __slots__ = ("response",)
    def __init__(self, data):
        self.response = data.get("Response")

    @property
    def icon_path(self):
        for item in self.response:
            return item['iconPath']

    @property
    def name(self):
        for item in self.response:
            return item['displayName']

    @property
    def type(self):
        for item in self.response:
            return item['membershipType']

    @property
    def id(self):
        return [item['membershipId'] for item in self.response]
