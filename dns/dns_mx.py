# looking up a mail domain

import argparse
import dns.resolver


def resolve_hostname(hostname, indent=""):
    """ print an A or AAAA record for "hostname"; follow CANMEs if necessary """
    indent = indent + '   '
    answer = dns.resolver.query(hostname, 'A')

    if answer.rrset is not None:
        for record in answer:
            print(indent, hostname, "has A address", record.address)
        return

    answer = dns.resolver.query(hostname, 'AAAA')
    if answer.rrset is not None:
        for record in answer:
            print(indent, hostname, "has AAAA address", record.address)

    answer = dns.resolver.query(hostname, "CNAME")
    if answer.rrset is not None:
        record = answer[0]
        cname = record.address
        print(indent, hostname, "is a CNAME alias for", cname)
        resolve_hostname(cname, indent)
        return
    print(indent, 'ERROR: no A, AAAA, or CNAME records for', hostname)


def resolve_email_domain(domain):
    """ for an email address "name@domain" find its mail server ip addresses """
    try:
        answer = dns.resolver.query(domain, 'MX', raise_on_no_answer=False)
    except dns.resolver.NXDOMAIN:
        print("error: no suck domain:", domain)
        return
    else:
        if answer.rrset is not None:
            records = sorted(answer, key=lambda record: record.preference)
            for record in records:
                name = record.exchange.to_text(omit_final_dot=True)
                print("priority ", record.preference)
                resolve_hostname(name)
        else:
            print("this domain has no explicit MX records")
            print("attempting to resolve it as an A, AAAA, or CNAME")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="find mail server ip address")
    parser.add_argument("domain", help="domain that you want to send mail to")
    resolve_email_domain(parser.parse_args().domain)
