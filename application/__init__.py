from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config/dev.cfg', silent=False)
    db.init_app(app)
    migrate.init_app(app, db)

    from application.controllers.home_controller import mod_pages as page_module

    app.register_blueprint(page_module)

    return app
