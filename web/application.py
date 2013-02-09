import sys
import os
sys.path.append(os.getcwd())

from flask import Flask, render_template

import kenbot

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return 'Hello World 2!'

@app.route('/denial_rates')
def denial_rates():
    return render_template('chart_sample.html')

if __name__ == '__main__':
    app.run()
