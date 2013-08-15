"""
Test POSTs to the local TiddlyWeb instance
"""


import httplib2
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.store import Store
from tiddlyweb.config import config

from test.fixtures import initialize_app


def setup_module(module):
    initialize_app()

    module.store = Store(config['server_store'][0], config['server_store'][1], {'tiddlyweb.config': config})
    bag = Bag('MAPUSER')
    module.store.put(bag)


def test_handler_valid_post_responds_with_201():
    query = 'mapped_user=pads'

    http = httplib2.Http()
    response, content = http.request('http://our_test_domain:8001/map_user/ben',
                                     method='POST',
                                     headers={'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'},
                                     body=query)

    assert response['status'] == '201'


def test_handler_valid_post_creates_mapuser_tiddler():
    query = 'mapped_user=cdent'

    http = httplib2.Http()
    http.request('http://our_test_domain:8001/map_user/chris',
                 method='POST',
                 headers={'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'},
                 body=query)

    tiddler = Tiddler('chris', 'MAPUSER')
    tiddler = store.get(tiddler)

    assert tiddler.modifier == 'chris'
    assert tiddler.text == ''
    assert 'mapped_user' in tiddler.fields
    assert tiddler.fields['mapped_user'] == 'cdent'
