import Cookie

import httplib2

import wsgi_intercept
from wsgi_intercept import httplib2_intercept

from tiddlyweb.web.serve import load_app
from tiddlywebconfig import config

config['server_host'] = {
    'scheme': 'http',
    'host': 'our_test_domain',
    'port': '8001',
}

config['secret'] = ['ssh!']


def initialize_app():
    app = load_app()

    def app_fn():
        return app

    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('0.0.0.0', 8080, app_fn)


def get_auth(username, password):
    http = httplib2.Http()
    response, content = http.request(
        'http://0.0.0.0:8080/challenge/cookie_form',
        body='user=%s&password=%s' % (username, password),
        method='POST',
        headers={'Content-Type': 'application/x-www-form-urlencoded'})
    assert response.previous['status'] == '303'

    user_cookie = response.previous['set-cookie']
    cookie = Cookie.SimpleCookie()
    cookie.load(user_cookie)
    return cookie['tiddlyweb_user'].value
