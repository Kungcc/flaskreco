from flask import Blueprint

bp = Blueprint('movielens',
                 __name__,
                template_folder='../_templates',
                static_folder='../_static')

from app.movielens import routes