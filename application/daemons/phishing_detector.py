import datetime

import whois as whois

from application import create_app, db
from application.models import User, KeywordTypo, PossiblePhishing
from application.utils.core_utils import CoreUtils


# while True
# mod%5


def detect_phishings(total_number_of_daemons, daemon_number):
    app = create_app()
    with app.app_context():
        users = User.query.filter(User.id % total_number_of_daemons==daemon_number).all()
        tlds = CoreUtils.get_tlds()
        for user in users:
            keywords = KeywordTypo.query.filter_by(user_id=user.id)
            for keyword in keywords:
                for tld in tlds:
                    checked_domain = keyword.typo + tld
                    try:
                        w = whois.whois(checked_domain)
                    except Exception:
                        continue
                    else:
                        if w.domain_name is not None:
                            phishing_domain = PossiblePhishing(possible_phishing_domain=checked_domain,
                                                               insert_date=datetime.datetime.utcnow(),
                                                               update_date=datetime.datetime.utcnow(),
                                                               from_which_typo=keyword.typo,
                                                               user_id=user.id)
                            db.session.add(phishing_domain)
                            db.session.commit()


if __name__ == '__main__':
    total_number_of_daemons = 1
    daemon_number = 0
    detect_phishings(total_number_of_daemons, daemon_number)
