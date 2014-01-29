#! ../env/bin/python
# -*- coding: utf-8 -*-

import manage
from hearthstone import mongo, create_app
import os
import test_base
import pytest

class TestManage:

    @pytest.mark.slow
    def test_fetch_url(self):
        heros = manage.fetch_main_index()
        assert len(heros) > 5
        
        hero = heros[0]
        assert hero['name']
        assert hero['decks']
        
        deck = hero['decks'][0]
        assert deck['desc']
        assert deck['_id']
        card = deck['cards'][0]
        assert card['count']
        assert card['id'] is not None

    @pytest.mark.slow
    def test_fetch_decks(self):
        mongo.db.deck.remove()
        assert mongo.db.deck.find().count() == 0
        manage.import_cards_decks()
        assert mongo.db.deck.find().count()
