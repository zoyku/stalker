#from stalker.application.models import Keyword_typo
#from stalker.application import app
from flask import render_template, request
from application.models import User
from application import db
from application.controller import mod_pages
import string
import random


@mod_pages.route('/')
@mod_pages.route('/home')
def home_page():
    a = User.query.first()
    print(a)
    return render_template('home.html')


@mod_pages.route('/users')
def user_page():

    keyword = request.args.get('keyword')
    user1 = User(insert_date='01.01.2000', update_date='01.01.2000', register_name='ilkbank', keyword='ilkbank1')
    db.session.add(user1)
    db.session.commit()
#    i = 0
#    while i < 50:
#        keyword1 = KeywordTypo()
#        db.session.add(keyword1)
#        db.session.commit()
#        db.create_all()
#        i += 1

    return render_template('user.html')


def typo_generator(phrase):

    ix = random.choice(range(len(phrase)))
    new_word = ''.join([phrase[w] if w != ix else random.choice(string.ascii_letters) for w in range(len(phrase))])

    return new_word
