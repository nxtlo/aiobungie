
class Careers(object):
    __slots__ = ("response",)
    
    def __init__(self, data):
        self.response = data.get("Response")

    @property
    def _(self):
        pass


class News(object):
    __slots__ = ('response')

    def __init__(self, data):
        self.response = data.get('response')

    @property
    def _(self):
        pass


class DestinyContent(object):
    __slots__ = ('response')

    def __init__(self, data):
        self.response = data.get('response')

    @property
    def _(self):
        pass
