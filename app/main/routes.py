from flask import render_template
from app.main import bp
from snippets import flash_errors

### 

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('main/index.html', title='Mini Flask Website Example')

## flask-pages #####################
from app import pages

@bp.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return render_template('main/flatpages.html', page=page)    

## pygments css register ##
from flask_flatpages import pygments_style_defs
@bp.route('pygments.css')
def pygments_css():
    return pygments_style_defs(style='colorful'), 200, {'Content-Type': 'text/css'}

####################################

# general page example
@bp.route('/general')
def general():
    mktxt = '''
# General page content

render_template with `functions` & `markdown`

'''
    return render_template('main/general.html', content = mktxt)

