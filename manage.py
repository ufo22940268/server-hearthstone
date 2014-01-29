#!/usr/bin/env python
import os

from flask.ext.script import Manager, Server
from hearthstone import create_app
from hearthstone.models import db, User
import json
import urllib2
from bs4 import BeautifulSoup
import re
from bson import ObjectId

env = os.environ.get('APPNAME_ENV', 'prod')
app = create_app('hearthstone.settings.%sConfig' % env.capitalize(), env=env)
manager = Manager(app)
manager.add_command("server", Server())

from hearthstone import mongo

@manager.shell
def make_shell_context():
    """ Creates a python REPL with several default imports
        in the context of the app
    """

    return dict(app=app, User=User)


@manager.command
def createdb():
    """ Creates a database with all of the tables defined in
        your Alchemy models
    """

    db.create_all()

@manager.command
def import_data():
    #Clear card data.
    mongo.db.card.remove()
    
    with open("data.json") as f:
        d = json.loads(f.read())
        items = []
        for k in d.keys():
            x = d[k]
            x['card_id'] = k
            x['picurl'] = 'http://img.dwstatic.com/ls/deckbuilder/pic/' \
            + urllib2.quote(x['picname']) + ".png"
            items.append(x)
        
        for x in items:
            mongo.db.card.insert(x)

@manager.command
def import_cards_decks():
    decks = fetch_main_index()
    mongo.db.deck.insert(decks)

def get_encoded_page(url):
    os.system('wget \'%s\' -O /tmp/a.html' % (url,))
    return BeautifulSoup(open('/tmp/a.html').read())
    

def fetch_main_index():
    url = 'http://ls.duowan.com/'
    soup = get_encoded_page(url)
    ml30s = soup.find('div', class_="mod-kazhu").find_all('div', class_="info ml30")

    heros = []
    for ml30 in ml30s:
        hero = dict()
        hero_name = ml30.find('div', class_="tit").text.split()[0]
        hero['name'] = hero_name
        anchors = ml30.find_all('a', href=re.compile("deckbuilder"))
        decks = []
        for a in anchors:
            deck = {}
            u = a['href']
            deck['desc'] = a.text
            deck['_id'] = ObjectId()
            cards = parse_cards(u)
            deck['cards'] = cards
            decks.append(deck)

        hero['decks'] = decks
        heros.append(hero)

    return heros

def parse_cards(url):
    cards = []
    if url.find(r'#^'):
        #We can fetch data in index page.
        ts = url.split(r'&')[1:]
        for x in ts:
            card = {}
            xs = x.strip().split(r'.')
            card['id'] = xs[0]
            card['count'] = xs[1]
            cards.append(card)
    else:
        #Should enter into detail page and dig data again.
        pass

    return cards
    


if __name__ == "__main__":
    manager.run()
