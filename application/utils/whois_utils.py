import whois as whois
from application import db
from application.models_module import User, KeywordTypo
from application.utils.home_utils import HomeUtils


class WhoisUtils:
    @staticmethod
    def is_registered(new_word):
        try:
            w = whois.whois(new_word)
        except Exception:
            return False
        else:
            return w.name
