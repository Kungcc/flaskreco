from app import app

import logging
from logging.handlers import RotatingFileHandler
import os
from flask import request

## log requests #######################################################################
from flask import Flask, request, jsonify

@app.after_request
def after_request(response):
    """ Logging after every request. """
    # This avoids the duplication of registry in the log,
    # since that 500 is already logged via @app.errorhandler.
    if response.status_code != 500:
        # ts = strftime('[%Y-%b-%d %H:%M]')
        app.logger.info('%s %s %s %s', 
        response.status_code,        
        request.remote_addr, 
        request.method, 
        request.full_path)
    return response

########################################################################################

## log to files
if not os.path.exists('logs'):
    os.mkdir('logs')

## logger setting
# getLogger(__name__):   decorators loggers to file + werkzeug loggers to stdout
# getLogger('werkzeug'): decorators loggers to file + nothing to stdout
app.logger = logging.getLogger(__name__)
app.logger.setLevel(logging.INFO)

## handler setting
file_handler = RotatingFileHandler('logs/logging.log', maxBytes=10240, backupCount=10)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))

## handler registration
app.logger.addHandler(file_handler)

