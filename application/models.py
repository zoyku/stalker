import datetime

from application import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    insert_date = db.Column(db.String(), nullable=False)
    update_date = db.Column(db.String(), nullable=False, onupdate=datetime.datetime.utcnow())
    register_name = db.Column(db.String(length=30), nullable=False, unique=True)
    keyword = db.Column(db.String(),  nullable=False, unique=True)
    keyword_typos = db.relationship('KeywordTypo', backref='keyword_typo', lazy=True)


class KeywordTypo(db.Model):
    __tablename__ = 'keyword_typo'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    typo = db.Column(db.String(), nullable=False, unique=True)
