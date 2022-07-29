import whois as whois
from application import db
from application.models import User, KeywordTypo
from application.utils.typo_utils import TypoUtils


class CoreUtils:
    @staticmethod
    def get_tlds():
        tld_list = ['.ml', '.tk', ]

        return tld_list
