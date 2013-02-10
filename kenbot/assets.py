from flask.ext import assets

raphael = assets.Bundle('js/raphael-min.js',
                        'js/g.raphael-min.js',
                        'js/g.pie-min.js',
                        'js/g.bar-min.js',
                        'js/g.line-min.js',
                        'js/g.dot-min.js',
                        output='gen/raphael.js')

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
                       'js/sugar.js',
                       'js/d3.v3.js',
                       'js/xcharts.js',
                       'js/app.js',
                       'js/kenbot.js',
                       filters='yui_js',
                       output='gen/app.js')

app_css = assets.Bundle('css/foundation.css',
                        'chosen/chosen.css',
                        'css/xcharts.css',
                        'css/app.css',
                        filters='yui_css',
                        output='gen/app.css')
