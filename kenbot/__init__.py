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


    sql = """with denials_by_race as (
                select count(*) as total
                    ,sum(case when action_type = 1 then 1 else 0 end) as approval_count
                    ,sum(case when action_type = 3 then 1 else 0 end) as denial_count
                    , applicant_race_1, loan_purpose
                from hmda
                where  msa_md = :msa_md
                    and applicant_race_1 < 6
                    and loan_purpose != 2
                group by applicant_race_1, loan_purpose
        )

        select total, approval_count, denial_count
        , cast(denial_count as float) / cast(total as float) * 100 as denial_rate
        , r.race, lp.loan_purpose
        from denials_by_race d
        join race r on d.applicant_race_1 = r.id
        join loan_purpose lp on d.loan_purpose = lp.id
        order by loan_purpose, race"""

    result = db.execute(sql, params={'msa_md':msa_md}).fetchall()
    return jsonify(result = to_dicts(result))

@app.route('/states')
def states():
    s = db.execute("select * from state").fetchall()
    return jsonify(states = to_dicts(s))

@app.route('/virginia1')
def virginia():
	return render_template('virginia.html')

def to_dicts(query_result):
    return [dict(items) for items in query_result]
