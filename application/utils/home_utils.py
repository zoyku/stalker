import whois as whois
from application import db
from application.models import User, KeywordTypo
from application.utils.typo_utils import TypoUtils
import datetime


class HomeUtils:
    @staticmethod
    def create_user_and_keyword(keyword, register_name):

        user1 = User(insert_date=datetime.datetime.utcnow(), update_date=datetime.datetime.utcnow(), register_name=register_name, keyword=keyword)
        db.session.add(user1)
        db.session.commit()

        keywords_with_typo = TypoUtils.callToTypo(keyword)

        for keyword in list(set(keywords_with_typo)):
            typo1 = KeywordTypo(user_id=User.query.filter_by(register_name=register_name).first().id, typo=keyword)
            db.session.add(typo1)
            db.session.commit()

        if KeywordTypo.query.all()!=[]:
            return True
        else:
            return False


    @staticmethod
    def is_unique(register_name):
        if User.query.filter_by(register_name=register_name).all()!=[]:
            return False
        else:
            return True
