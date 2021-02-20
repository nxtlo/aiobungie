
class Clans(object):
    """
    A class that returns information about a Destiny2 Clan.
    """
    __slots__ = ("response",)

    def __init__(self, data):
        self.response = data.get("Response")

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def __getitem__(self, item):
        for _item in self.response.values():
            return _item[item]

    @property
    def get(self):
        return self.__getitem__

    @property
    def id(self):
        """
        Returns
        --------
        :class:`int`
            The clan's id.
        """
        return self.get('groupId')

    @property
    def name(self):
        """
        Returns
        --------
        :class:`str`
            The clan's name.
        """
        return self.get('name')

    @property
    def created_at(self):
        """
        Returns
        --------
        Optional[:class: `datetime.datetime`]
            When was the clan created at.
        """
        return self.get('creationDate')

    @property
    def edited_at(self):
        """
        Returns
        --------
        Optional[:class: `datetime.datetime`]
            last time the clan was updated.
        """
        return self.get("modificationDate")

    @property
    def member_count(self):
        """
        Returns
        --------
        :class:`int`
            The clan's member count.
        """
        return self.get("memberCount")

    @property
    def description(self):
        """
        Returns
        --------
        :class"`str`:
            The clan's long description.
        """
        return self.get("about")

    @property
    def is_public(self):
        """
        Returns
        --------
        :class:`bool`
            Returns `True` if the clan is Public, `False` if not.
        """
        return self.get("isPublic")

    @property
    def banner(self):
        """
        Returns
        --------
        The clan's banner path.
        """
        return self.get("bannerPath")

    @property
    def avatar(self):
        """
        Returns
        --------
        :class:`str`
            The clan's avatar path.
        """
        return self.get("avatarPath")

    @property
    def about(self):
        """
        Returns
        --------
        :class:`str`
            The clans's short info.
        """
        return self.get("motto")

    @property
    def tag(self):
        """
        Returns
        --------
        :class:`str`
            The clans's tag.
        """
        return self.get("clanInfo")['clanCallsign']


    @property
    def owner(self):
        """
        Returns
        --------
        :class:`str`
            The clan owner's name.
        """
        for item in self.response['founder']['destinyUserInfo'].values():
            return item

