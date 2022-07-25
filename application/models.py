from application import db


class User(db.Model):
    __tablename__='uUser'
    id = db.Column(db.Integer(), primary_key=True)
    insertDate = db.Column(db.String(), nullable=False)
    updateDate = db.Column(db.String(), nullable=False)
    registerName = db.Column(db.String(length=30), nullable=False, unique=True)
    keyword = db.Column(db.String(),  nullable=False, unique=True)
    keywordTypos = db.relationship('KeywordTypo', backref='owned_user', lazy=True)


class KeywordTypo(db.Model):
    __tablename__='KeywordTypo'
    id = db.Column(db.Integer(), primary_key=True)
    keywordUser = db.Column(db.Integer(), db.ForeignKey('user.id'))
    typo = db.Column(db.String(), nullable=False, unique=True)