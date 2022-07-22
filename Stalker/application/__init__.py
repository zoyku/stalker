from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config/dev.cfg', silent=True)


    #load_blueprints(app)
    return app

app = create_app()
db = SQLAlchemy(app)

#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///client.db'

from application import routes