from app import app, db
from app.models import Todo

## for flask shell
## using flask shell to work with database entities without having to import them

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Todo': Todo}

## python .\microblog.py
if __name__ == '__main__':
    app.run()

## python -m flask run
# using .flaskenv