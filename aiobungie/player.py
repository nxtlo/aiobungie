class Player:
    __slots__ = ("response", "icon", "type", "displayname", "id")
    def __init__(self, data):
        self.response = data.get("Response")
        self.icon = data.get('iconPath')
        self.type = data.get('membershipType')
        self.displayname = data.get('displayName')
        self.id = data.get('membershipId')