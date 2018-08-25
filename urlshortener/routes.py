from handlers.shortener import UrlShortenerHandler

routes = [
    ('/shorten_url', UrlShortenerHandler()),
    ('/{shortened_url}', UrlShortenerHandler())
]


def setup_routes(api):
    for route in routes:
        api.add_route(*route)
