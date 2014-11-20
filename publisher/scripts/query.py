#!/usr/bin/env python

import sys
import json

from es_api import ESFactory

def handle_results(docs, pargs, full=True):
    if docs:
        if pargs.full:
            print json.dumps(docs, indent=2)
        elif docs.get('hits',{}).get('hits', False):
            for doc in docs['hits']['hits']:
                if pargs.all:
                    print json.dumps(doc, indent=2)
                else:
                    for path in doc.get('fields', {}).get('__extra.original_path', []):
                        print path
def main(args=sys.argv[1:]):
    import argparse
    parser = argparse.ArgumentParser(description='Basic interaction with elastic search')
    parser.add_argument('ids', nargs='*', help='Any number of ids (the full path name)')
    parser.add_argument('-p', '--port', type=int, help='Elastic search port (default 9200)', default=9200)
    parser.add_argument('--host', help='Elastic search host')
    parser.add_argument('-q', '--query', help="""Simple lucene query: "a:1 AND b:2" to search for documents with attribute a having value 1 and attribute b having value 2.""")    
    parser.add_argument('--full-query', help="""Some QueryDSL elastic search query string. (e.g. 
    '{"query":{"match":{"attribute":"value"}}}' see: http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/query-dsl.html""")    
    parser.add_argument('-f', '--full', action='store_true', help='Show the complete response, instead of the docs only.')
    parser.add_argument('--all', action='store_true', help='Shows all data instead of just the file name')
    pargs = parser.parse_args(args)

    if pargs.host:
        es = ESFactory.basicConnector(pargs.host, port=pargs.port)
    else:
        es = ESFactory.fromDockerEnvironment()
    
    options={}
    if not pargs.all:
        options['fields']='__extra.original_path'
    if pargs.ids:
        handle_results(es.get(pargs.ids, **options), pargs, full=pargs.full)
    if pargs.full_query:
        handle_results(es.search(pargs.full_query, **options), pargs, full=pargs.full)
    if pargs.query:
        handle_results(es.basicSearch(pargs.query, **options), pargs, full=pargs.full)
        
if __name__ == '__main__':
    main()

