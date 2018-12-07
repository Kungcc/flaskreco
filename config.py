import os

basedir = os.path.abspath(os.path.dirname(__file__)) + '/src'

# app.config, which uses a dictionary style to work with variables
class Config(object):
    DEBUG = False
    LOG_TO_FILE = True

    # flask-admin
    ADMIN = False

    # for flask-wtf form secret_key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # DB setting
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Theme
    THEME = 'cerulean'

    # Flatpages
    FLATPAGES_EXTENSION = ['.htm', '.html', '.md', '.txt']
    FLATPAGES_MARKDOWN_EXTENSIONS = ['extra', 'codehilite', 'fenced_code', 'toc']
    FLATPAGES_ROOT = './_static/pages'

class DevConfig(Config):
    DEBUG = True
    LOG_TO_FILE = False
    
    # flask-admin
    ADMIN = True