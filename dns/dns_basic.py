# basic dns query

import argparse
import dns.resolver


def lookup(name):
    for qtype in "A", "AAAA", "CNAME", "MX", "NS":
        answer = dns.resolver.query(name, rdtype=qtype, raise_on_no_answer=False)
        if answer.rrset is not None:
            print(answer.rrset)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="resolve a name using dns")
    parser.add_argument("name", help="name that you want to look up in dns")
    lookup(parser.parse_args().name)
