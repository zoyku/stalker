from application import db
from application.models import User, KeywordTypo
from application.models_module.app_models import BaseResponse
from application.utils.typo_utils import TypoUtils
import datetime


class HomeUtils:
    @staticmethod
    def create_user_and_keyword(keyword, register_name):
        response = BaseResponse()
        user = User.query.filter_by(register_name=register_name).first()
        if not user:
            user = User(insert_date=datetime.datetime.utcnow(), update_date=datetime.datetime.utcnow(), register_name=register_name, keyword=keyword)
            db.session.add(user)
            db.session.commit()

            keywords_with_typo = TypoUtils.callToTypo(keyword)

            for keyword in list(set(keywords_with_typo)):
                typo1 = KeywordTypo(register_name=User.query.filter_by(register_name=register_name).first().register_name, from_which_keyword=User.query.filter_by(register_name=register_name).first().keyword, typo=keyword)
                db.session.add(typo1)
            try:
                db.session.commit()
                response.response_code = 200
                response.is_okay = True
                response.message = 'OK'
            except:
                response.response_code = 500
                response.is_okay = False
                response.message = 'Error'
        else:
            response.response_code = 400
            response.is_okay = False
            response.message = 'Register Name already taken.'

        return response
