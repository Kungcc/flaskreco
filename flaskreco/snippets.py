### fix flask_login @login_required decorator for blueprint

from flask import request, redirect, url_for, flash
# from flask_login import current_user
from functools import wraps

# def login_required(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if current_user.is_authenticated:
#             pass
#         else:
#             next_url = request.path # However you do this in Flask
#             login_url = '%s?next=%s' % (url_for('auth.login'), next_url)
#             return redirect(login_url)
#         return f(*args, **kwargs)   
#     return wrap

### wtf error to flash message 
# http://flask.pocoo.org/snippets/12/

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))