from application import db

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    insert_date = db.Column(db.String(), nullable=False)
    update_date = db.Column(db.String(), nullable=False)
    register_name = db.Column(db.String(length=30), nullable=False, unique=True)
    keyword = db.Column(db.String(),  nullable=False, unique=True)
    keyword_typos = db.relationship('Keyword_typo', backref='owned_user', lazy=True)

class Keyword_typo(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    keyword_user = db.Column(db.Integer(), db.ForeignKey('user.id'))
    typo = db.Column(db.String(), nullable=False, unique=True)
