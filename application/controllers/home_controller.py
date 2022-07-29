from flask import render_template, request, make_response, jsonify
from application.models import User, KeywordTypo
from application import db
from application.controller import mod_pages
from application.utils.home_utils import HomeUtils


@mod_pages.route('/')
@mod_pages.route('/home')
def home_page():
    return render_template('home.html')


@mod_pages.route('/save_keyword')
def save_keyword():

    keyword = request.args.get('keyword')
    register_name = request.args.get('register_name')

    is_unique = HomeUtils.is_unique(register_name)

    if is_unique:
        is_okay = HomeUtils.create_user_and_keyword(keyword, register_name)
    else:
        return make_response(jsonify({"Result": "Register name is already taken."}), 400)

    if is_okay:
        return make_response(jsonify({"Result": "OK"}), 200)
    else:
        return make_response(jsonify({"Result": "Error"}), 500)
