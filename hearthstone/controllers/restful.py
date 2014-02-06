#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.restful import reqparse, abort, Api, Resource
from flask.ext.restful.types import date
from flask.ext import restful
from hearthstone import mongo
from bson.json_util import dumps
import json
from bson import ObjectId 

def cursor_to_dict(c):
    """Convert mongodb cursor object to python dict object
    If the cursor object contains _id, then convert it to a plain string."""
    r = json.loads(dumps(c))
    
    if type(r) == list:
        for x in r:
            if x.get('_id'):
                x['_id'] = x['_id']['$oid']
                
    else:
        r['_id'] = r['_id']['$oid']

    return r

class HeroDeck(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=unicode, required=True)
        args = parser.parse_args()
        decks = mongo.db.deck.find_one({'name': args['name']})['decks']
        decks = cursor_to_dict(decks)
        for cs in [d['cards'] for d in decks]:
            for c in cs:
                self.setup_card(c)

            cs.sort(cmp=lambda x, y: cmp(int(x['mana']), int(y['mana'])))
            
        return decks

    def setup_card(self, c):
        card =  mongo.db.card.find_one({"card_id": c['id']})
        if not card:
            raise Exception("card_id %s not founded in card collection" % c['id'])
        c['pic'] = card['picurl']
        c['name'] = card['name']
        c['mana'] = card['mana']
        
def register(api):
    api.add_resource(HeroDeck, '/hero_deck')
