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

@app.route('/denial_rates_data/<int:msa_md>')
def denial_rates_data(msa_md=None):
#    return jsonify(data=(
#        {'total':30563, 'approval_count':13448, 'denial_rate':18.42, 'race':'American Indian'}
#        ,{'total':255645, 'approval_count':135681, 'denial_rate':11.61, 'race':'Asian'}
#        ,{'total':12345, 'approval_count':135681, 'denial_rate':22.61, 'race':'White'}
#    ))

    sql = """with denials_by_race as (
  select count(*) as total
  ,sum(case when action_type = 1 then 1 else 0 end) as approval_count
  ,sum(case when action_type = 3 then 1 else 0 end) as denial_count
  , applicant_race_1, loan_purpose
  from hmda
  where  msa_md = %d
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
  order by loan_purpose, race""" % (msa_md)
    result = data.conn().execute(sql).fetchall()
    return jsonify(result = to_dicts(result))

@app.route('/states')
def states():
    s = data.conn().execute("select * from state").fetchall()
    return jsonify(states = to_dicts(s))

def to_dicts(query_result):
    return [dict(items) for items in query_result]
