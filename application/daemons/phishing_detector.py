import datetime
import time
import whois

from application import create_app, db
from application.models import User, KeywordTypo, PossiblePhishing
from application.utils.core_utils import CoreUtils


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
                print("Checking for user: %s" % user.register_name)
                print(user.keyword_typos)
                keywords = KeywordTypo.query.filter_by(register_name=user.register_name)
                for keyword in keywords:
                    for tld in tlds:
                        checked_domain = keyword.typo + tld
                        is_exist = PossiblePhishing.query.filter_by(possible_phishing_domain=checked_domain).first()
                        if is_exist is None:
                            try:
                                domain_info = whois.whois(checked_domain)
                            except Exception as e:
                                print(e)
                                continue
                            else:
                                if domain_info.domain_name is not None:
                                    domain_creation_time = change_date_format(domain_info.creation_date)
                                    if domain_creation_time > datetime.datetime.now() - datetime.timedelta(
                                            days=2):
                                        print("found domain")
                                        is_exist_in_ppd = PossiblePhishing.query.filter_by(
                                            possible_phishing_domain=checked_domain).first()
                                        if is_exist_in_ppd is None:
                                            phishing_domain = PossiblePhishing(possible_phishing_domain=checked_domain,
                                                                               insert_date=datetime.datetime.utcnow(),
                                                                               update_date=datetime.datetime.utcnow(),
                                                                               from_which_keyword=user.keyword,
                                                                               register_name=user.register_name)
                                            db.session.add(phishing_domain)
                                            db.session.commit()
                                            print("possible phishing domain added")
                                        else:
                                            continue
                        else:
                            continue

            print("finished the job, sleeping for 60 seconds")
            time.sleep(60)
            print("60 seconds passed")


if __name__ == '__main__':
    total_number_of_daemons = 1
    daemon_number = 0
    detect_phishings(total_number_of_daemons, daemon_number)
