from flask import Blueprint

bp = Blueprint('handlers',
                 __name__,
                template_folder='../_templates',
                static_folder='../_static')

from app.handlers import errpages

from app import app
if app.config['LOG_TO_FILE'] is True:
    from app.handlers import server_log