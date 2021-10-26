from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init(app):
    user = 'ctfbot'
    password = 'ctfbot'
    db_name = 'ctfbot'

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@localhost:5432/{db_name}'
    global db
    db.init_app(app)
    with app.app_context():
        db.create_all()
