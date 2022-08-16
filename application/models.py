import datetime
import enum

from application import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    insert_date = db.Column(db.String(), nullable=False)
    update_date = db.Column(db.String(), nullable=False, onupdate=datetime.datetime.utcnow())
    register_name = db.Column(db.String(length=30), nullable=False)
    keyword = db.Column(db.String(), nullable=False, unique=True)
    category = db.Column(db.String())
    domain = db.Column(db.String(), nullable=False)
    keyword_typos = db.relationship('KeywordTypo', backref='keyword_typo', lazy=True)
    domains_with_typos = db.relationship('PossiblePhishing', backref='possible_phishing', lazy=True)


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
    user_id=db.Column(db.Integer(), db.ForeignKey('user.id'))
    from_which_keyword = db.Column(db.String())
    insert_date = db.Column(db.String(), nullable=False)
    update_date = db.Column(db.String(), nullable=False, onupdate=datetime.datetime.utcnow())
    is_approved = db.Column(db.Boolean)
    is_false = db.Column(db.Boolean)
    whois_record = db.Column(db.JSON)
    dns_a_record = db.Column(db.JSON())
    dns_ns_record = db.Column(db.JSON())
    dns_mx_record = db.Column(db.JSON())

