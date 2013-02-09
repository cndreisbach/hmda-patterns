from flask.ext import assets
from . import app

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
                       'chosen/chosen.jquery.js',
                       'js/app.js',
                       'js/kenbot.js',
                       output='gen/app.js')
asset_pkg.register('app_js', app_js)

app_css = assets.Bundle('css/foundation.css',
                        'chosen/chosen.css',
                        'css/app.css',
                        output='gen/app.css')
asset_pkg.register('app_css', app_css)
