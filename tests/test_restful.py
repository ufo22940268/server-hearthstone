#! ../env/bin/python
# -*- coding: utf-8 -*-
from hearthstone import create_app
from hearthstone.models import db
import urllib
import json

def setup_module():
    global app
    app = create_app('hearthstone.settings.DevConfig', env='dev')
    app = app.test_client()

def make_request_url(url, params):
    if params:
        return '%s?%s' % (url, urllib.urlencode(params))
    else:
        return url

def get_result(url, params):
    rv = app.get(make_request_url(url, params))
    if rv.status_code != 200:
        raise Exception("Responce status code %d error" % rv.status_code)
    else:
        return json.loads(rv.data)

class TestURLs:
    def setup(self):
        app = create_app('hearthstone.settings.DevConfig', env='dev')
        self.app = app.test_client()
        db.app = app
        db.create_all()

    def teardown(self):
        db.session.remove()
        db.drop_all()

    def test_home(self):
        rv = self.app.get('/')
        assert rv.status_code == 200

    def test_form(self):
        rv = self.app.get('/wtform')
        assert rv.status_code == 200

class TestAPIs:
    def test_hero_deck(self):
        result = get_result('/hero_deck', {'name': u'法师'.encode('utf-8')})
        assert len(result) > 0
        first = result[0]
        
        assert first.get("_id") is not None
        assert first.get("desc") is not None

        card = first.get('cards')[0]
        assert card['pic']
        assert card['name']
