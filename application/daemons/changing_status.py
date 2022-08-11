from application.models import User, KeywordTypo, PossiblePhishing
from application import create_app, db


class ChangeStatus:
    @staticmethod
    def changing_status(phishing_domain,status):
        if status == 'false_positive':
            PossiblePhishing.query.filter_by(possible_phishing_domain=phishing_domain).first().is_approved = False
            db.session.commit()

        elif status == 'approved':
            PossiblePhishing.query.filter_by(possible_phishing_domain=phishing_domain).first().is_approved = True
            db.session.commit()