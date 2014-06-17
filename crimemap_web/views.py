from flask import render_template, flash, redirect, session, request, url_for, make_response
from crimemap_web import app, db

@app.route('/')
def index():
    return render_template('leaflet.html', crimes=db['crimes'].values(), fires=db['fires'].values())

@app.route('/raw.csv')
def csv():
    response = make_response(render_template('raw.csv', crimes=db['crimes'].values()))
    response.headers['content-type'] = 'text/csv'
    return response
