import os
from hearthstone import mongo, create_app

env = os.environ.get('APPNAME_ENV', 'prod')
app = create_app('hearthstone.settings.%sConfig' % env.capitalize(), env=env)
test_app = app.test_client()
context = app.test_request_context('/')
context.push()

