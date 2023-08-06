# Evan Widloski - 2020-10-29
# Mavlink debug tool

from pymavlink import mavutil
import argparse
import pprint as pretty

pp = pretty.PrettyPrinter(indent=4)
pprint = pp.pprint

def main():

    parser = argparse.ArgumentParser()
    parser._positionals.title = "commands"
    subparsers = parser.add_subparsers()
    subparsers.required = True
    subparsers.dest = 'command'
    parser.add_argument('--port', default='/dev/ttyACM0', type=str, help='mavlink device port')

    show_subparser = subparsers.add_parser('show', help="print mavlink messages as they are received")
    show_subparser.add_argument('--type', default=None, type=str, help='filter messages by type')
    show_subparser.add_argument('--exclude', action='append', default=None, type=str, help='filter messages by type')
    show_subparser.set_defaults(func=show)

    unique_subparser = subparsers.add_parser('unique', help="record message types and number received until keyboard interrupt")
    unique_subparser.set_defaults(func=unique)

    args = parser.parse_args()
    args.func(args)

def open_connection(port):
    return mavutil.mavlink_connection(port)

def show(args):
    """Print matching messages to console"""

    c = open_connection(args.port)

    while True:
        msg = c.recv_match(blocking=True)

        if args.type is not None:
            if msg.get_type() == args.type:
                print(msg)
        elif args.exclude is not None:
            if msg.get_type() not in args.exclude:
                print(msg)
        else:
            print(msg)

def unique(args):
    """Print unique message types and number of types received"""

    c = open_connection(args.port)

    types = {}

    try:
        while True:
            msg = c.recv_match(blocking=True)
            if msg.get_type() not in types:
                types[msg.get_type()] = 1
            else:
                types[msg.get_type()] += 1
    except KeyboardInterrupt:
        print()
        pprint(types)
