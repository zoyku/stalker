from flask import abort
import logging

from application import db
from application.models import User, KeywordTypo
from application.models_module.app_models import BaseResponse
from application.utils.typo_utils import TypoUtils
import datetime


class HomeUtils:
    @staticmethod
    def create_user_and_keyword(keyword, register_name):
        response = BaseResponse()
        users = User.query.filter_by(register_name=register_name).all()
        for user in users:
            if user.keyword == keyword:
                response.response_code = 400
                response.is_okay = False
                response.message = 'You can not search for the same keyword.'
                abort(400)

        new_user = User(insert_date=datetime.datetime.utcnow(), update_date=datetime.datetime.utcnow(), register_name=register_name, keyword=keyword)
        db.session.add(new_user)
        db.session.commit()

        keywords_with_typo = TypoUtils.callToTypo(keyword)

        for keyword in list(set(keywords_with_typo)):
            typo1 = KeywordTypo(user_id=new_user.id,
                                register_name=new_user.register_name,
                                from_which_keyword=new_user.keyword,
                                typo=keyword)
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
            abort(500)

        return response
