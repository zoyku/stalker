import datetime
import enum

from application import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    insert_date = db.Column(db.String(), nullable=False)
    update_date = db.Column(db.String(), nullable=False, onupdate=datetime.datetime.today())
    register_name = db.Column(db.String(length=30), nullable=False)
    keyword = db.Column(db.String(), nullable=False, unique=True)
    category = db.Column(db.String())
    domain = db.Column(db.String(), nullable=False)
    keyword_typos = db.relationship('KeywordTypo', backref='keyword_typo', lazy=True)
    domains_with_typos = db.relationship('PossiblePhishing', backref='possible_phishing', lazy=True)
    real_domain_content = db.relationship('RealWebPageContent', backref='real_web_page_content', lazy=True)
    phishing_domain_content = db.relationship('PhishingPageContent', backref='phishing_page_content', lazy=True)


class KeywordTypo(db.Model):
    __tablename__ = 'keyword_typo'
    id = db.Column(db.Integer(), primary_key=True)
    register_name = db.Column(db.String())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    from_which_keyword = db.Column(db.String())
    typo = db.Column(db.String(), nullable=False, unique=True)


class PossiblePhishing(db.Model):
    __tablename__ = 'possible_phishing'
    id = db.Column(db.Integer(), primary_key=True)
    possible_phishing_domain = db.Column(db.String(), nullable=False, unique=True)
    register_name = db.Column(db.String())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    from_which_keyword = db.Column(db.String())
    insert_date = db.Column(db.String(), nullable=False)
    update_date = db.Column(db.String(), nullable=False, onupdate=datetime.datetime.today())
    is_approved = db.Column(db.Boolean)
    is_false = db.Column(db.Boolean)
    whois_record = db.Column(db.JSON)
    dns_a_record = db.Column(db.JSON())
    dns_ns_record = db.Column(db.JSON())
    dns_mx_record = db.Column(db.JSON())


class RealWebPageContent(db.Model):
    __tablename__ = 'real_web_page_content'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    register_name = db.Column(db.String())
    domain = db.Column(db.String())
    content = db.Column(db.TEXT)
    response_code = db.Column(db.Integer)
    headers = db.Column(db.String)
    css_links = db.Column(db.JSON)



class PhishingPageContent(db.Model):
    __tablename__ = 'phishing_page_content'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    register_name = db.Column(db.String())
    domain = db.Column(db.String())
    content = db.Column(db.TEXT)
    response_code = db.Column(db.Integer)
    headers = db.Column(db.String)
    css_links = db.Column(db.JSON)

