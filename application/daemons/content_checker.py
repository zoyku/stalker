import datetime
import json
import time

import requests
import whois
import logging
import dns
import dns.resolver

from whois.parser import PywhoisError
from dns.exception import DNSException

from application import create_app, db
from application.models import User, KeywordTypo, PossiblePhishing, PhishingPageContent
from application.utils.core_utils import CoreUtils
from application.utils.words_utils import WordUtils

logging.basicConfig(filename='../logs/content_checker.log',
                    format="[%(asctime)s] %(levelname)s %(funcName)s: %(message)s",
                    level=logging.INFO)


def store_content(id):
    app = create_app()
    with app.app_context():
        users = User.query.filter_by(id=id).all()
        for user in users:
            phishing_domains = PossiblePhishing.query.filter_by(user_id=user.id).all()
            for phishing_domain in phishing_domains:
                phishing_web_page_content = None
                try:
                    phishing_web_page_content = requests.get('https://' + phishing_domain)
                except requests.exceptions.RequestException:
                    pass

                try:
                    phishing_web_page_content = requests.get('http://' + phishing_domain)
                except requests.exceptions.RequestException:
                    pass

                if phishing_web_page_content is not None:
                    new_phishing_page_content = PhishingPageContent(user_id=user.id,
                                                                    register_name=user.register_name,
                                                                    content=phishing_web_page_content.text,
                                                                    response_code=phishing_web_page_content.status_code,
                                                                    headers=phishing_web_page_content.headers)
                    db.session.add(new_phishing_page_content)
                    db.session.commit()
                else:
                    new_phishing_page_content = PhishingPageContent(user_id=user.id,
                                                                    register_name=user.register_name,
                                                                    content=None,
                                                                    response_code=0)
                    db.session.add(new_phishing_page_content)
                    db.session.commit()
    return 0
