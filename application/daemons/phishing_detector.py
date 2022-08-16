import datetime
import json
import time
import whois
import logging
import dns
import dns.resolver

from whois.parser import PywhoisError
from dns.exception import DNSException

from application import create_app, db
from application.models import User, KeywordTypo, PossiblePhishing
from application.utils.core_utils import CoreUtils
from application.utils.words_utils import WordUtils

logging.basicConfig(filename='../logs/phishing_detector.log', format="[%(asctime)s] %(levelname)s %(funcName)s: %(message)s",
                    level=logging.INFO)


def change_date_format(domain_date):
    if type(domain_date) == list:
        domain_date = domain_date[0].strptime(domain_date[0].strftime('%Y-%b-%d'),
                                              '%Y-%b-%d')

    return domain_date


def adding_tlds(keywords):
    tlds = CoreUtils.get_tlds()
    checked_domains = []
    for keyword in keywords:
        for tld in tlds:
            checked_domains.append(keyword.typo + tld)

    return checked_domains


def adding_words_and_tlds(user):
    keyword = user.keyword
    words = WordUtils.get_words(user.category)
    tlds = CoreUtils.get_tlds()
    word_added_domains = []
    checked_domains = []
    for word in words:
        word_added_domains.append(keyword + word)
        word_added_domains.append(word + keyword)

    for word in word_added_domains:
        for tld in tlds:
            checked_domains.append(word + tld)

    return checked_domains


def domain_info_to_dict(domain_info):
    domain_creation_time = None
    domain_expiration_time = None
    domain_updated_time = None
    if domain_info.creation_date is not None:
        domain_creation_time = change_date_format(domain_info.creation_date).strftime("%Y-%b-%d")
    if domain_info.expiration_date is not None:
        domain_expiration_time = change_date_format(domain_info.expiration_date).strftime("%Y-%b-%d")
    if domain_info.updated_date is not None:
        domain_updated_time = change_date_format(domain_info.updated_date).strftime("%Y-%b-%d")
    domain_info_changed = dict(domain_info)
    update = {'updated_date': domain_updated_time, 'creation_date': domain_creation_time,
              'expiration_date': domain_expiration_time}
    domain_info_changed.update(update)

    return domain_info_changed


def dns_a_lookup(domain):
    # logging.info(domain)
    dns_a_check = []

    try:
        dnsA = dns.resolver.resolve(domain, 'A')
    except DNSException:
        pass
    else:
        for data in dnsA:
            dns_a_check += [str(data)]

    if not dns_a_check:
        return None
    else:
        return dns_a_check


def dns_ns_lookup(domain):
    # logging.info(domain)
    dns_ns_check = []

    try:
        dnsNS = dns.resolver.resolve(domain, 'NS')
    except DNSException:
        pass
    else:
        for data in dnsNS:
            dns_ns_check += [str(data)]

    if not dns_ns_check:
        return None
    else:
        return dns_ns_check


def dns_mx_lookup(domain):
    # logging.info(domain)
    dns_mx_check = []

    try:
        dnsMX = dns.resolver.resolve(domain, 'A')
    except DNSException:
        pass
    else:
        for data in dnsMX:
            dns_mx_check += [str(data)]

    if not dns_mx_check:
        return None
    else:
        return dns_mx_check


def detect_phishings(total_number_of_daemons, daemon_number):
    app = create_app()
    with app.app_context():
        while True:
            users = User.query.filter(User.id % total_number_of_daemons == daemon_number).all()
            for user in users:
                app.logger.info("Checking for keyword '%s' for user %s" % (user.keyword, user.register_name))
                keywords = KeywordTypo.query.filter_by(user_id=user.id)
                checked_domains = adding_tlds(keywords)
                checked_domains += adding_words_and_tlds(user)
                for checked_domain in checked_domains:
                    is_exist = PossiblePhishing.query.filter_by(possible_phishing_domain=checked_domain).first()
                    if is_exist is None:
                        try:
                            domain_info = whois.whois(checked_domain)
                        except PywhoisError:
                            continue
                        if domain_info.domain_name is not None:
                            domain_creation_time = (change_date_format(domain_info.creation_date))
                            if True or domain_creation_time > datetime.datetime.now() - datetime.timedelta(
                                    days=2):  # todo
                                app.logger.info("Found a registered possible phishing domain.")
                                domain_info_changed = domain_info_to_dict(domain_info)
                                app.logger.debug(domain_info_changed)
                                dns_a_check = dns_a_lookup(checked_domain)
                                dns_ns_check = dns_ns_lookup(checked_domain)
                                dns_mx_check = dns_mx_lookup(checked_domain)
                                phishing_domain = PossiblePhishing(possible_phishing_domain=checked_domain,
                                                                   insert_date=datetime.date.today(),
                                                                   update_date=datetime.date.today(),
                                                                   from_which_keyword=user.keyword,
                                                                   user_id=user.id,
                                                                   register_name=user.register_name,
                                                                   is_approved=None,
                                                                   is_false=None,
                                                                   whois_record=domain_info_changed,
                                                                   dns_a_record=json.dumps(dns_a_check),
                                                                   dns_ns_record=json.dumps(dns_ns_check),
                                                                   dns_mx_record=json.dumps(dns_mx_check))
                                db.session.add(phishing_domain)
                                db.session.commit()
                                user.update_date = datetime.date.today()
                                db.session.commit()
                                app.logger.info("Possible phishing domain added to the database. User is "
                                                "updated.")
                        else:
                            continue

            app.logger.info("Finished the job, sleeping for 60 seconds.")
            time.sleep(60)
            app.logger.info("60 seconds passed.")


if __name__ == '__main__':
    total_number_of_daemons = 1
    daemon_number = 0
    detect_phishings(total_number_of_daemons, daemon_number)
