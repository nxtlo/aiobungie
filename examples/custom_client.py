"""Example of defining a specific set of routes that're not specifically implemented by the library, but rather the user."""

# aiobungie provides a REST client for the API, but not all methods are implemented.
# for an example, "/Content/Rss/NewsArticles/{pageToken}/" this route is not yet implemented as of the date
# of the creation of this example. heres how you can implement this easily yourself.

# The route we're implementing here is
# * https://bungie-net.github.io/multi/operation_get_Content-RssNewsArticles.html#operation_get_Content-RssNewsArticles

import aiobungie

# * inheritance based client.


class CustomClient(aiobungie.RESTClient):
    """Here we define a custom REST client, It is also possible to derive from `aiobungie.Client`, both are fine.

    Use whatever fits your needs.
    """

    __slots__ = ()

    # implement your custom method.
    # fmt: off
    async def fetch_rss_news_articles(self, page_token: int) -> aiobungie.typedefs.JSONObject:
        response = await self._request(
            "GET", f"/Content/Rss/NewsArticles/{page_token}"
        )  # make the API call.
        assert isinstance(response, dict)  # ensure the response a dictionary object.
        return response
    # fmt: on


async def start_custom() -> None:
    client = CustomClient("token")
    async with client:
        news = await client.fetch_rss_news_articles(0)

    articles = news["NewsArticles"]

    for article in articles:
        print(article)


# * default based implementation
# aiobungie also provides a method called `static_request` which
# allows you to send your own HTTP requests to the API with the given route.


async def start_base() -> None:
    client = aiobungie.RESTClient("token")

    async with client:
        page_token = "0"
        # Does exactly the same as the custom class, but without all the
        # inheritance boilerplate
        news = await client.static_request(
            "GET", "/Content/Rss/NewsArticles/" + page_token
        )
    assert isinstance(news, dict)
    for article in news["NewsArticles"]:
        print(article)
