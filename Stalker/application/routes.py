#from Stalker.application.models import Keyword_typo
from application import app
from flask import render_template
from application.models import User
from application import db

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/users')
def user_page():
    user1 = User(insert_date='01.01.2000', update_date='01.01.2000', register_name='ilkbank', keyword='ilkbank')
    db.create_all()
    return render_template('user.html')