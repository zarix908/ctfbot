from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()


def init(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{config.db_user}:{config.db_password}@' \
                                            f'{config.db_host}:5432/{config.db_name}'
    global db
    db.init_app(app)
    with app.app_context():
        db.create_all()
