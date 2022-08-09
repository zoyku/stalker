import datetime
import time
import whois
import logging

from application import create_app, db
from application.models import User, KeywordTypo, PossiblePhishing
from application.utils.core_utils import CoreUtils

logging.basicConfig(filename='../logs/phishing_detector.log', format="[%(asctime)s] %(levelname)s %(message)s", level=logging.INFO)


def change_date_format(domain_creation_date):
    if type(domain_creation_date) == list:
        domain_creation_date = domain_creation_date[0].strptime(domain_creation_date[0].strftime('%Y-%b-%d'),
                                                                '%Y-%b-%d')

    return domain_creation_date


def detect_phishings(total_number_of_daemons, daemon_number):
    app = create_app()
    with app.app_context():
        while True:
            users = User.query.filter(User.id % total_number_of_daemons == daemon_number).all()
            tlds = CoreUtils.get_tlds()
            for user in users:
                app.logger.info("Checking for keyword '%s' for user %s" % (user.keyword, user.register_name))
                keywords = KeywordTypo.query.filter_by(user_id=user.id)
                for keyword in keywords:
                    for tld in tlds:
                        checked_domain = keyword.typo + tld
                        is_exist = PossiblePhishing.query.filter_by(possible_phishing_domain=checked_domain).first()
                        if is_exist is None:
                            try:
                                domain_info = whois.whois(checked_domain)
                            except Exception as e:
                                continue
                            else:
                                if domain_info.domain_name is not None:
                                    domain_creation_time = change_date_format(domain_info.creation_date)
                                    if domain_creation_time > datetime.datetime.now() - datetime.timedelta(
                                            days=2):
                                        app.logger.info("Found a registered possible phishing domain")
                                        is_exist_in_ppd = PossiblePhishing.query.filter_by(
                                            possible_phishing_domain=checked_domain).first()
                                        if is_exist_in_ppd is None:
                                            phishing_domain = PossiblePhishing(possible_phishing_domain=checked_domain,
                                                                               insert_date=datetime.datetime.utcnow(),
                                                                               update_date=datetime.datetime.utcnow(),
                                                                               from_which_keyword=user.keyword,
                                                                               user_id=user.id,
                                                                               register_name=user.register_name)
                                            db.session.add(phishing_domain)
                                            db.session.commit()
                                            app.logger.info("Possible phishing domain added to the database.")
                                        else:
                                            continue
                        else:
                            continue

            app.logger.info("Finished the job, sleeping for 60 seconds.")
            time.sleep(60)
            app.logger.info("60 seconds passed.")


if __name__ == '__main__':
    total_number_of_daemons = 1
    daemon_number = 0
    detect_phishings(total_number_of_daemons, daemon_number)
