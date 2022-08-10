import logging
from logging.config import dictConfig

from flask import Flask, render_template
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

    logging.basicConfig(filename='stalker.log', format="[%(asctime)s] %(levelname)s %(message)s")
    app.logger.setLevel(app.config['LOG_LEVEL'])

    app.register_blueprint(page_module)

    def __page_wrong_request(e):
        app.logger.error('Same username and keyword.')
        return render_template('400.html'), 400

    app.register_error_handler(400, __page_wrong_request)

    app.logger.info('App started.')

    return app
