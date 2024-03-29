from flask import request, jsonify
from application.models import User, PossiblePhishing
from flask import render_template, redirect, url_for, flash
from application.forms import RegisterForm
from application.controller import mod_pages
from application.utils.home_utils import HomeUtils
from application.utils.changing_status import ChangeStatus


@mod_pages.route('/')
@mod_pages.route('/home')
def home_page():
    return render_template('home.html')


@mod_pages.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        HomeUtils.create_user_and_keyword(form.keyword.data, form.username.data, form.domain.data, form.category.data)
        return redirect(url_for('pages.user'))

    if form.errors != {}:
        for error_msg in form.errors.values():
            flash(f'There has been an error: {error_msg}')

    return render_template('register.html', form=form)


@mod_pages.route('/user')
def user():
    users = User.query.all()

    return render_template('users.html', users=users)


@mod_pages.route('/keyword_typos')
def keyword_typos():
    users = User.query.all()

    return render_template('keyword_typos.html', users=users)


@mod_pages.route('/filtered_possible_phishing_domains')
def possible_phishing_domains():
    value = request.args.get('value')

    if value == "Approved":
        possible_phishings = PossiblePhishing.query.filter_by(is_approved=True).all()
    elif value == "FalsePositive":
        possible_phishings = PossiblePhishing.query.filter_by(is_approved=False).all()
    elif value == "All":
        possible_phishings = PossiblePhishing.query.all()
    else:
        possible_phishings = PossiblePhishing.query.filter_by(is_approved=None).all()

    return render_template('possible_phishing_domains.html', possible_phishings=possible_phishings)


@mod_pages.route('/change_phishing_domain_status', methods=["POST"])
def change_phishing_domain_status():
    phishing_domain = request.form.get('phishing_domain')
    status = request.form.get('status')

    ChangeStatus.changing_status(phishing_domain, status)

    return jsonify({"Result": "OK"})
