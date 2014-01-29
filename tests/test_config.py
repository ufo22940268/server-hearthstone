#! ../env/bin/python
# -*- coding: utf-8 -*-
from hearthstone import create_app


# class TestConfig:
#     def test_dev_config(self):
#         app = create_app('hearthstone.settings.DevConfig', env='dev')

#         assert app.config['DEBUG'] is True
#         assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///../database.db'
#         assert app.config['SQLALCHEMY_ECHO'] is True
#         assert app.config['CACHE_TYPE'] == 'null'

#     def test_prod_config(self):
#         app = create_app('hearthstone.settings.ProdConfig', env='prod')

#         assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///../database.db'
#         assert app.config['CACHE_TYPE'] == 'simple'
