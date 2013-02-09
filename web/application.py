import sys
import os
sys.path.append(os.getcwd())

from flask import Flask, render_template
from flask.ext import assets

import kenbot

app = Flask(__name__)
app.debug = True
app.config['ASSETS_DEBUG'] = app.debug

@app.route('/')
def index():
    return 'Hello World 2!'

@app.route('/denial_rates')
def denial_rates():
    return render_template('chart_sample.html')

@app.route('/stuff')
def stuff():
    pass

asset_pkg = assets.Environment(app)

raphael = assets.Bundle('js/raphael-min.js',
                        'js/g.raphael-min.js',
                        'js/g.pie-min.js',
                        'js/g.bar-min.js',
                        'js/g.line-min.js',
                        'js/g.dot-min.js',
                        output='gen/raphael.js')
asset_pkg.register('raphael', raphael)

app_js = assets.Bundle('js/jquery.js',
                       'js/jquery.foundation.mediaQueryToggle.js',
                       'js/jquery.foundation.forms.js',
                       'js/jquery.event.move.js',
                       'js/jquery.event.swipe.js',
                       'js/jquery.foundation.reveal.js',
                       'js/jquery.foundation.navigation.js',
                       'js/jquery.foundation.buttons.js',
                       'js/jquery.foundation.tabs.js',
                       'js/jquery.foundation.tooltips.js',
                       'js/jquery.foundation.accordion.js',
                       'js/jquery.placeholder.js',
                       'js/jquery.foundation.alerts.js',
                       'js/jquery.foundation.topbar.js',
                       'js/app.js',
                       output='gen/app.js')
asset_pkg.register('app_js', app_js)

app_css = assets.Bundle('css/foundation.css',
                        'css/app.css',
                        output='gen/app.css')
asset_pkg.register('app_css', app_css)

if __name__ == '__main__':
    app.run()
