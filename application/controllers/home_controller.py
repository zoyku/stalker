from flask import render_template, request
from application.models import User, KeywordTypo
from application import db
from application.controller import mod_pages
from application.utils.home_utils import HomeUtils


@mod_pages.route('/')
@mod_pages.route('/home')
def home_page():
    return render_template('home.html')


@mod_pages.route('/users')
def user_page():
    keyword = request.args.get('keyword')
    register_name = request.args.get('registerName')

    HomeUtils.create_user(keyword, register_name)

    return render_template('user.html')
