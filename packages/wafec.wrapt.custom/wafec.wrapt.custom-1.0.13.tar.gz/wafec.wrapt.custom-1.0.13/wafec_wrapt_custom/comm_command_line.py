import argparse

from wafec_wrapt_custom.comm.servers import start_server
from wafec_wrapt_custom.comm.clients import add_proxy_interception_info


def define_clients_add_proxy_interception_info(subparsers):
    def defaults(args):
        add_proxy_interception_info(args.name)
    parser = subparsers.add_parser('add_proxy_interception_info')
    parser.add_argument('-n', '--name', dest='name', type=str, required=True)
    parser.set_defaults(func=defaults)


def define_clients(subparsers):
    parser = subparsers.add_parser('clients')
    subparsers = parser.add_subparsers()
    define_clients_add_proxy_interception_info(subparsers)


def define_servers_start(subparsers):
    def defaults(args):
        start_server()

    parser = subparsers.add_parser('start')
    parser.set_defaults(func=defaults)


def define_servers(subparsers):
    parser = subparsers.add_parser('servers')
    subparsers = parser.add_subparsers()
    define_servers_start(subparsers)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    define_servers(subparsers)
    define_clients(subparsers)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
