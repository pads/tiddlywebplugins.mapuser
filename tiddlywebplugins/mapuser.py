"""
A simple handler that takes a POST request and creates a tiddler
in the MAPUSER bag with the title extracted from the route and the
mapped_user value taken from the POST body.
"""


from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.web.util import get_route_value


def init(config):
    """
    Add the /map_user route.
    """
    if 'selector' in config:
        config['selector'].add('/map_user/{user:segment}', POST=handle)


def handle(environ, start_response):

    store = environ['tiddlyweb.store']

    query = environ['tiddlyweb.query']
    mapped_user = query['mapped_user'][0]

    tiddler_title = get_route_value(environ, 'user')
    tiddler = Tiddler(tiddler_title, 'MAPUSER')
    tiddler.modifier = tiddler_title
    tiddler.text = ''
    tiddler.tags = []
    tiddler.fields = {'mapped_user': mapped_user}

    store.put(tiddler)

    start_response('201', [('Content-Type', 'text/html; charset=UTF-8')])
    return []
