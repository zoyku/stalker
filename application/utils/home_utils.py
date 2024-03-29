import json
import requests
import datetime

from flask import abort
from bs4 import BeautifulSoup

from application import db
from application.models import User, KeywordTypo, RealWebPageContent
from application.models_module.app_models import BaseResponse
from application.utils.typo_utils import TypoUtils


class HomeUtils:
    @staticmethod
    def create_user_and_keyword(keyword, register_name, domain, category):
        response = BaseResponse()
        users = User.query.filter_by(register_name=register_name).all()
        for user in users:
            if user.keyword == keyword:
                response.response_code = 400
                response.is_okay = False
                response.message = 'You can not search for the same keyword.'
                abort(400)

        new_user = User(insert_date=datetime.datetime.utcnow(), update_date=datetime.datetime.utcnow(),
                        register_name=register_name, keyword=keyword, domain=domain, category=category)
        db.session.add(new_user)
        db.session.commit()

        user_web_page_content = None
        try:
            user_web_page_content = requests.get('https://' + domain)
        except requests.exceptions.RequestException:
            pass

        try:
            user_web_page_content = requests.get('http://' + domain)
        except requests.exceptions.RequestException:
            pass

        if user_web_page_content is not None:
            soup = BeautifulSoup(user_web_page_content.text, 'html.parser')
            css_links = []
            for link in soup.find_all('link'):
                css_links += [link.get('href')]
            new_web_page_content = RealWebPageContent(user_id=new_user.id,
                                                      register_name=new_user.register_name,
                                                      content=user_web_page_content.text,
                                                      domain=new_user.domain,
                                                      response_code=user_web_page_content.status_code,
                                                      headers=str(user_web_page_content.headers),
                                                      css_links=json.dumps(css_links))
            db.session.add(new_web_page_content)
            db.session.commit()
        else:
            abort(404)

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
