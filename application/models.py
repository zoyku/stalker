from application import db


class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer(), primary_key=True)
    insert_date = db.Column(db.String(), nullable=False)
    update_date = db.Column(db.String(), nullable=False)
    register_name = db.Column(db.String(length=30), nullable=False, unique=True)
    keyword = db.Column(db.String(),  nullable=False, unique=True)
    keyword_typos = db.relationship('KeywordTypo', backref='owned_user', lazy=True)


class KeywordTypo(db.Model):
    __tablename__='keywordTypo'
    id = db.Column(db.Integer(), primary_key=True)
    keywordUser = db.Column(db.Integer(), db.ForeignKey('user.id'))
    typo = db.Column(db.String(), nullable=False, unique=True)