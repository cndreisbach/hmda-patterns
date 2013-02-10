from flask import Blueprint, render_template, jsonify, g
from . import data

views = Blueprint('views', __name__,
                  template_folder='templates')

@views.route('/')
def index():
    return render_template('index.html',
                           msas=data.msas())

@views.route('/denial_rates')
def denial_rates():
    return render_template('chart_sample.html')

@views.route('/denial_rates_data/<int:msa_md>')
def denial_rates_data(msa_md=None):

    return results_to_json(data.denial_rates(msa_md))

@views.route('/denial_by_income/<int:msa_md>')
@views.route('/denial_by_income/')
def denial_by_income(msa_md=None):

    return results_to_json(data.denial_by_income(msa_md))

# Much of this could be replaced with a single generic query that accepted config options to control filtering, pivoting, etc

@views.route('/hal_gov_backed_by_income/<int:msa_md>')
@views.route('/hal_gov_backed_by_income/')
def hal_gov_backed_by_income(msa_md=None):

    return results_to_json(data.hal_gov_backed_by_income(msa_md))

@views.route('/hal_gov_backed_by_race/<int:msa_md>')
@views.route('/hal_gov_backed_by_race/')
def hal_gov_backed_by_race(msa_md=None):

    return results_to_json(data.hal_gov_backed_by_race(msa_md))

@views.route('/gov_backed_by_race_purpose/<int:msa_md>')
@views.route('/gov_backed_by_race_purpose/')
def gov_backed_by_race_purpose(msa_md=None):

    return results_to_json(data.gov_backed_by_race_purpose(msa_md))

@views.route('/gov_backed_by_income_purpose/<int:msa_md>')
@views.route('/gov_backed_by_income_purpose/')
def gov_backed_by_income_purpose(msa_md=None):

    return results_to_json(data.gov_backed_by_income_purpose(msa_md))


def results_to_json(query_result):
    return jsonify(result = [dict(items) for items in query_result])

