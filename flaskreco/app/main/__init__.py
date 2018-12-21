from flask import Blueprint

bp = Blueprint('main',
                 __name__,
                template_folder='../_templates',
                static_folder='../_static')

from app.main import routes