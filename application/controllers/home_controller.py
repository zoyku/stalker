from flask import render_template, request, make_response, jsonify
from application.models import User, KeywordTypo, PossiblePhishing
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

    response = HomeUtils.create_user_and_keyword(keyword, register_name)

    # users = User.query.all()
    # keyword_typos = KeywordTypo.query.all()
    # possible_phishings = PossiblePhishing.query.all()

    return render_template('result.html')  # , users=users, keyword_typos=keyword_typos, possible_phishings=possible_phishings)
    #make_response(jsonify(response.__dict__), response.response_code)


@mod_pages.route('/users')
def users():
    users = User.query.all()

    return render_template('users.html', users=users)


@mod_pages.route('/keyword_typos')
def keyword_typos():
    keyword_typos = KeywordTypo.query.all()

    return render_template('keyword_typos.html', keyword_typos=keyword_typos)


@mod_pages.route('/possible_phishing_domains')
def possible_phishing_domains():
    possible_phishings = PossiblePhishing.query.all()

    return render_template('possible_phishing_domains.html', possible_phishings=possible_phishings)
