import json
import logging
from bs4 import BeautifulSoup

import requests

from application import create_app, db
from application.models import User, PossiblePhishing, PhishingPageContent

logging.basicConfig(filename='../logs/content_checker.log',
                    format="[%(asctime)s] %(levelname)s %(funcName)s: %(message)s",
                    level=logging.INFO)


def store_content(total_number_of_daemons, daemon_number):
    app = create_app()
    with app.app_context():
        phishing_domains = PossiblePhishing.query.filter(PossiblePhishing.id % total_number_of_daemons == daemon_number).all()
        for phishing_domain in phishing_domains:
            control = PhishingPageContent.query.filter_by(domain=phishing_domain.possible_phishing_domain).first()
            if control is None:
                phishing_web_page_content = None
                try:
                    phishing_web_page_content = requests.get('https://' + phishing_domain.possible_phishing_domain)
                except requests.exceptions.RequestException:
                    pass

                try:
                    phishing_web_page_content = requests.get('http://' + phishing_domain.possible_phishing_domain)
                except requests.exceptions.RequestException:
                    pass

                if phishing_web_page_content is not None:
                    soup = BeautifulSoup(phishing_web_page_content.text, 'html.parser')
                    css_links = []
                    for link in soup.find_all('link'):
                        css_links += [link.get('href')]
                    new_phishing_page_content = PhishingPageContent(user_id=phishing_domain.user_id,
                                                                    register_name=phishing_domain.register_name,
                                                                    domain=phishing_domain.possible_phishing_domain,
                                                                    content=phishing_web_page_content.text,
                                                                    response_code=phishing_web_page_content.status_code,
                                                                    headers=str(phishing_web_page_content.headers),
                                                                    css_links=json.dumps(css_links))
                    db.session.add(new_phishing_page_content)
                    db.session.commit()
                else:
                    new_phishing_page_content = PhishingPageContent(user_id=phishing_domain.user_id,
                                                                    register_name=phishing_domain.register_name,
                                                                    domain=phishing_domain.possible_phishing_domain,
                                                                    content=None,
                                                                    response_code=0,
                                                                    headers=None,
                                                                    css_links=None)
                    db.session.add(new_phishing_page_content)
                    db.session.commit()
            else:
                continue
    return 0


if __name__ == '__main__':
    total_number_of_daemons = 1
    daemon_number = 0
    store_content(total_number_of_daemons, daemon_number)


