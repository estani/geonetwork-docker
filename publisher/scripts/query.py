#!/usr/bin/env python

import sys, os
import json

from es_api import ESFactory

def main(args=sys.argv[1:]):
    import argparse
    parser = argparse.ArgumentParser(description='Basic interaction with elastic search')
    parser.add_argument('ids', nargs='*', help='Any number of ids (the full path name)')
    parser.add_argument('-q', '--query', help='Some elastic search query string.')    
    parser.add_argument('-p', '--port', type=int, help='Elastic search port (default 9200)', default=9200)
    parser.add_argument('--host', help='Elastic search host')
    pargs = parser.parse_args(args)

    if pargs.host:
        es = ESFactory.basicConnector(pargs.host, port=pargs.port)
    else:
        es = ESFactory.fromDockerEnvironment()

    if pargs.ids:
        for doc in es.get(pargs.ids):
            print json.dumps(doc, indent=2)
    if pargs.query:
        for doc in es.search(pargs.query):
            print json.dumps(doc, indent=2)
        
if __name__ == '__main__':
    main()

