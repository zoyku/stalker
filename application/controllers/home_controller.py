from flask import render_template, request, make_response, jsonify
from application.models import User, KeywordTypo, PossiblePhishing
from flask import render_template, redirect, url_for
from application.forms import RegisterForm
from application import db
from application.controller import mod_pages
from application.utils.home_utils import HomeUtils


@mod_pages.route('/')
@mod_pages.route('/home')
def home_page():
    return render_template('home.html')


@mod_pages.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        HomeUtils.create_user_and_keyword(form.keyword.data, form.username.data)
        return redirect(url_for('pages.user'))

    return render_template('register.html', form=form)


@mod_pages.route('/user')
def user():
    users = User.query.all()

    return render_template('users.html', users=users)


@mod_pages.route('/keyword_typos')
def keyword_typos():
    users = User.query.all()

    return render_template('keyword_typos.html', users=users)


@mod_pages.route('/possible_phishing_domains')
def possible_phishing_domains():
    possible_phishings = PossiblePhishing.query.all()

    return render_template('possible_phishing_domains.html', possible_phishings=possible_phishings)
