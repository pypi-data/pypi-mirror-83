# from __future__ import print_function
import argparse
import logging

class argsc:
    """ A class to generate command-line args and properties """

    def __init__(self, arguments):
        parser = argparse.ArgumentParser(description=__doc__,
                                         formatter_class=argparse.RawDescriptionHelpFormatter)

        parser.add_argument('-k', '--keps-url', help="Keplerian Elements URL", default='http://www.amsat.org/amsat/ftp/keps/current/nasabare.txt')
        parser.add_argument('-s', '--sats', help="Satellites to track", default='', nargs='+')
        parser.add_argument('-o', '--output', help="Output Format (text, json)", default='text')
        parser.add_argument('-l', '--list', help="List all satellites")

        parser.add_argument('-i', '--info', dest='info', action='store_true', help="Print info debugging messages", default=False)
        parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help="Print verbose debugging messages", default=False)
        parser.add_argument('-t', '--trace', dest='trace', action='store_true', help="Print more verbose debugging messages", default=False)
        args = parser.parse_args(arguments)

        # Set log levels
        args.log_level = logging.WARN
        if args.info:
            args.log_level = logging.INFO

        if args.verbose or args.trace:
            args.log_level = logging.DEBUG

        self.args = args
