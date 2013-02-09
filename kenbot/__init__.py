#!/usr/bin/env python

import os

from flask import Flask, render_template, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['ASSETS_DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:////tmp/kenbot.db')

db = SQLAlchemy(app)

import kenbot.assets
from kenbot import data

@app.route('/')
def index():
    return render_template('index.html',
                           msas=data.msas())

@app.route('/denial_rates')
def denial_rates():
    return render_template('chart_sample.html')

@app.route('/denial_rates_data')
def denial_rates_data():
    return jsonify(data=(
        {'total':30563, 'approval_count':13448, 'denial_rate':18.42, 'race':'American Indian'}
        ,{'total':255645, 'approval_count':135681, 'denial_rate':11.61, 'race':'Asian'}
        ,{'total':12345, 'approval_count':135681, 'denial_rate':22.61, 'race':'White'}
    ))

@app.route('/states')
def states():
    s = data.conn().execute("select * from state").fetchall()
    return jsonify(states = to_dicts(s))

def to_dicts(query_result):
    return [dict(items) for items in query_result]
