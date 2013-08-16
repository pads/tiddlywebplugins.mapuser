"""
A simple handler that takes a POST request and creates a tiddler
in the MAPUSER bag with the title extracted from the route and the
mapped_user value taken from the POST body.
"""


from httpexceptor import HTTP415, HTTP400

import simplejson

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

    try:
        content_type = environ['tiddlyweb.type']
        length = environ['CONTENT_LENGTH']
        if content_type != 'application/json':
            raise HTTP415('application/json required')
        content = environ['wsgi.input'].read(int(length))
    except KeyError, exc:
        raise HTTP400('Missing content-type or content-length headers: %s' % exc)

    try:
        json_dict = simplejson.loads(content)
        mapped_user = json_dict['mapped_user']
    except (ValueError, KeyError), exc:
        raise HTTP400('Invalid input, %s' % exc)

    tiddler_title = get_route_value(environ, 'user')
    tiddler = Tiddler(tiddler_title, 'MAPUSER')
    tiddler.modifier = tiddler_title
    tiddler.text = ''
    tiddler.tags = []
    tiddler.fields = {'mapped_user': mapped_user}

    store.put(tiddler)

    start_response('201 Created', [('Content-Type', 'text/html; charset=UTF-8')])
    return []
