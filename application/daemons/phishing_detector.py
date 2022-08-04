import datetime
import time

import whois as whois

from application import create_app, db
from application.models import User, KeywordTypo, PossiblePhishing
from application.utils.core_utils import CoreUtils


def detect_phishings(total_number_of_daemons, daemon_number):
    app = create_app()
    with app.app_context():
        while True:
            users = User.query.filter(User.id % total_number_of_daemons == daemon_number).all()
            tlds = CoreUtils.get_tlds()
            for user in users:
                print("Checking for user: %s" % user.register_name)
                keywords = KeywordTypo.query.filter_by(user_id=user.id)
                for keyword in keywords:
                    for tld in tlds:
                        checked_domain = keyword.typo + tld
                        is_exist = PossiblePhishing.query.filter_by(possible_phishing_domain=checked_domain).first()
                        if is_exist is None:
                            try:
                                w = whois.whois(checked_domain)
                            except Exception:
                                continue
                            else:
                                if w.domain_name is not None:
                                    print("found domain")
                                    is_exist_in_ppd = PossiblePhishing.query.filter_by(
                                        possible_phishing_domain=checked_domain).first()
                                    if is_exist_in_ppd is None:
                                        phishing_domain = PossiblePhishing(possible_phishing_domain=checked_domain,
                                                                           insert_date=datetime.datetime.utcnow(),
                                                                           update_date=datetime.datetime.utcnow(),
                                                                           from_which_typo=keyword.typo,
                                                                           user_id=user.id)
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
    total_number_of_daemons = 3
    daemon_number = 0
    detect_phishings(total_number_of_daemons, daemon_number)
