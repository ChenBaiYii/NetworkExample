# the maid


import argparse


def tip():
    pass


if __name__ == '__main__':
    service = {"tip": tip}
    parser = argparse.ArgumentParser(description="这是一个快捷自助帮助机器人女仆:")
    parser.add_argument("service", choices=service, help="service ?")
    parser.add_argument("-s", type=str, help="service")

    args = parser.parse_args()
    print(args.service)
    maid = service[args.service]
    maid()
