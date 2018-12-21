from app import app, db
from app.models import Todo

## for flask shell
## using flask shell to work with database entities without having to import them

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Todo': Todo}

if __name__ == '__main__':
    app.run(debug=True)

## python -m flask run
# using .flaskenv

