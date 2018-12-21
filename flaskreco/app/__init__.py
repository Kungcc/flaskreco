from flask import Flask, render_template
from config import Config, DevConfig, basedir

# instance init  #########################################################
app = Flask(__name__,  static_folder='_static', template_folder='_templates')
app.config.from_object(DevConfig)

# flask-bootstrap
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

# flask-markdown
from flaskext.markdown import Markdown
Markdown(app)

# db setting #########################################################
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# flask-admin instance #########################################################

# admin settings
if app.config['ADMIN'] is True:
    from flask_admin import Admin
    from flask_admin.contrib.sqla import ModelView
    admin = Admin(app, name='Admin', template_mode='bootstrap3')
    ### adding views for db tables
    from app.models import Todo
    admin.add_view(ModelView(Todo, db.session))    

## flask-flatpages #########################################################
from flask_flatpages import FlatPages
pages = FlatPages(app)

# blueprint registration #########################################################

# error & log handler 
from app.handlers import bp as handlers_bp
app.register_blueprint(handlers_bp)

# views
from app.main import bp as main_bp
app.register_blueprint(main_bp, url_prefix='/')

# autocomp
from app.movielens import bp as movielens_bp
app.register_blueprint(movielens_bp, url_prefix='/')

# checking  #########################################################
# print('database dir:' + basedir)
# print(DevConfig)
print(app.url_map)
# print(app.config['UPLOAD_FOLDER'])
