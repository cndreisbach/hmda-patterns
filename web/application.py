import sys
import os
sys.path.append(os.getcwd())

from flask import Flask, render_template, jsonify

import kenbot

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return 'Hello World 2!'

@app.route('/denial_rates')
def denial_rates():
    return render_template('chart_sample.html')

@app.route('/denial_rates_data')
def denial_rates_data():
    return jsonify(data=(
        {'total':30563, 'approval_count':13448, 'denial_rate':18.42, 'race':'American Indian'}
        ,{'total':255645, 'approval_count':135681, 'denial_rate':11.61, 'race':'Asian'}
    ))

if __name__ == '__main__':
    app.run()
