
class AppInfo:
    __slots__ = ('response',)

    def __init__(self, data):
        self.response = data.get('Response')

    @property
    def id(self):
        """Returns the application id"""
        return self.response['applicationId']

    @property
    def name(self):
        """Returns the application name"""
        return self.response['name']

    @property
    def redirect_url(self):
        """Returns the redirect url"""
        return self.response['redirectUrl']

    @property
    def created_at(self):
        """Returns the app's CreationDate"""
        return self.response['creationDate']

    @property
    def published_at(self):
        """Returns when was the app first published"""
        return self.response['firstPublished']

    @property
    def link(self):
        """Returns the application link"""
        return self.response['link']
    
    @property
    def status(self):
        """Returns an integer of the application's status"""
        return self.response['status']

    @property
    def is_public(self):
        """Returns a bool if the app was public or Privet"""
        for item in self.response['team']:
            return item.get('user')['isPublic']

    @property
    def owner_name(self):
        """Returns a str of the app's owner"""
        for item in self.response['team']:
            return item.get('user')['displayName']


    @property
    def owner_id(self):
        """Returns the app's owner id"""
        for item in self.response['team']:
            return item.get('user')['membershipId']

    @property
    def icon_path(self):
        """Returns the icon path fot the app"""
        for item in self.response['team']:
            return item.get("user")['iconPath']

    @property
    def member_type(self):
        """Returns the member ship type"""
        for item in self.response['team']:
            return item.get('user')['membershipType']
