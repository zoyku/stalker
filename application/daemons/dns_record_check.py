import dns
import dns.resolver
import logging

logging.basicConfig(filename='../logs/phishing_detector.log', format="%(asctime)s %(levelname)s %(funcName)s: %("
                                                                     "message)s", level=logging.INFO)


def dns_a_lookup(domain):
    # logging.info(domain)
    dns_a_check = []

    try:
        dnsA = dns.resolver.resolve(domain, 'A')
    except Exception as e:
        logging.error(e)
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
    except Exception as e:
        logging.error(e)
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
    except Exception as e:
        logging.error(e)
    else:
        for data in dnsMX:
            dns_mx_check += [str(data)]

    if not dns_mx_check:
        return None
    else:
        return dns_mx_check
