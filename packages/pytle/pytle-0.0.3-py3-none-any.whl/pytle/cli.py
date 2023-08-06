#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#from pytle.pytle import main
from pytle import pytle
from pytle.argsc import argsc
import json

def handler(args, tle):
    if args.args.output == "text":
        for sat in args.args.sats:
            print(tle.get_sat_info_text(sat))
    elif args.args.output == "json":
        response = []
        for sat in args.args.sats:
            response.append(tle.get_sat_info(sat))

        print(json.dumps({'sats': response}))


def main():
    import sys
    args = argsc(sys.argv[1:])
    tle = pytle(keps_url="http://www.amsat.org/amsat/ftp/keps/current/nasabare.txt", cache=True)
    handler(args, tle)


if __name__ == '__main__':
    main()
