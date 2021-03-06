from flask import Flask
from flask.ext.zodb import ZODB

app = Flask(__name__)
app.secret_key = 'NpaguVKgv<;f;i(:T>3tn~dsOue5Vy)'

app.config['ZODB_STORAGE'] = 'zeo://localhost:8090'
db = ZODB(app)

import crimemap_web.views
