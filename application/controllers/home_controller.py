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
    return render_template('home.html')


@mod_pages.route('/users')
def user_page():
    keyword = request.args.get('keyword')
    register_name = request.args.get('registerName')

    create_user(keyword, register_name)



    return render_template('user.html')
