#!/usr/bin/env python

import os

from flask import Flask, render_template, jsonify
import sqlsoup

app = Flask(__name__)
app.config['ASSETS_DEBUG'] = True
app.config['DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:////tmp/kenbot.db')

db = sqlsoup.SQLSoup(app.config['DATABASE_URI'])

import kenbot.assets
from kenbot import data

@app.route('/')
def index():
    return render_template('index.html',
                           msas=data.msas())

@app.route('/denial_rates')
def denial_rates():
    return render_template('chart_sample.html')

@app.route('/denial_rates_data/<int:msa_md>')
def denial_rates_data(msa_md=None):

    return results_to_json(data.denial_rates(msa_md))

@app.route('/denial_by_income/<int:msa_md>')
@app.route('/denial_by_income/')
def denial_by_income(msa_md=None):

    return results_to_json(data.denial_by_income(msa_md))

# Much of this could be replaced with a single generic query that accepted config options to control filtering, pivoting, etc

@app.route('/hal_gov_backed_by_income/<int:msa_md>')
@app.route('/hal_gov_backed_by_income/')
def hal_gov_backed_by_income(msa_md=None):

    return results_to_json(data.hal_gov_backed_by_income(msa_md))

@app.route('/hal_gov_backed_by_race/<int:msa_md>')
@app.route('/hal_gov_backed_by_race/')
def hal_gov_backed_by_race(msa_md=None):

    return results_to_json(data.hal_gov_backed_by_race(msa_md))

@app.route('/gov_backed_by_race_purpose/<int:msa_md>')
@app.route('/gov_backed_by_race_purpose/')
def gov_backed_by_race_purpose(msa_md=None):

    return results_to_json(data.gov_backed_by_race_purpose(msa_md))

@app.route('/gov_backed_by_income_purpose/<int:msa_md>')
@app.route('/gov_backed_by_income_purpose/')
def gov_backed_by_income_purpose(msa_md=None):

    return results_to_json(data.gov_backed_by_income_purpose(msa_md))



@app.route('/states')
def states():
    s = db.execute("select * from state").fetchall()
    return jsonify(states = to_dicts(s))

def results_to_json(query_result):
    return jsonify(result = to_dicts(query_result))

def to_dicts(query_result):
    return [dict(items) for items in query_result]
