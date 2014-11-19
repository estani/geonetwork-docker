#!/usr/bin/env python

import sys, os
import json

from publisher import SimplePathParser, NetCDFFileHandler
from es_api import ESFactory
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return json.JSONEncoder.default(self, obj)
        except:
            return str(obj)

def process(meta, elasticsearch, show=True):
    meta_json = json.dumps(meta, indent=2, cls=SetEncoder) 
    if show:
        print meta_json
    if elasticsearch:
        elasticsearch.publish(json.loads(meta))

def main(args=sys.argv[1:]):
    import argparse
    parser = argparse.ArgumentParser(description='Extracts metadata from Netcdf files')
    parser.add_argument('files', metavar="FILE/DIR", nargs=1)
    parser.add_argument('--show', action='store_true', help='show produced json')
    parser.add_argument('--dry-run', action='store_true', help="Don't publish anything")
    parser.add_argument('-n', metavar='CONTAINER', help='Contair name with an elasticsearch instance running in it where we will be publishing')
    parser.add_argument('-p', '--port', type=int, help='Elastic search port (default 9200)', default=9200)
    #parser.add_argument('--dump', help='Directory where json will get dumped')
    #This is not used here, but used by the calling script. Still we want to show a single help.
    parser.add_argument('--host', help='Elastic search host')
    parser.add_argument('--dir-structure', help='Metadata directory structure (e.g. /*/institute/model/realm so /a/b/c/d/e -> institute=b, model=c,realm=d) ')
    parser.add_argument('--file-structure', help='Metadata File structure. (e.g. institute_model_realm so ABC_mod1_atmos_blah.nc -> institute=ABC, model=mod1,realm=atmos) ')
    parser.add_argument('--file-structure-sep', help='Separator used in the filename for structuring data (default "_")', default='_')
    parser.add_argument('--exclude-crawl', help='Exclude the given regular expression while crawling')
    parser.add_argument('--include-crawl', help='Include only the given regular expression while  crawling')

    pargs = parser.parse_args(args)

    #handle input properly
    if pargs.dir_structure is not None or pargs.file_structure is not None:
        path_parser = SimplePathParser(dir_structure=pargs.dir_structure,
                                        file_structure=pargs.file_structure,
                                        file_sep=pargs.file_structure_sep)
    else:
        path_parser = None
    handler = NetCDFFileHandler(path_parser=path_parser)

    exclude = []
    include = None
    if pargs.exclude_crawl:
        import re
        exclude.append(re.compile(pargs.exclude_crawl))
    if pargs.include_crawl:
        import re
        include = [re.compile(pargs.include_crawl)]

    if pargs.host:
        es = ESFactory.basicConnector(pargs.host, port=pargs.port)
    elif not pargs.dry_run:
        es = ESFactory.fromDockerEnvironment()
    else:
        es = None

    for filename in pargs.files:
        if os.path.isdir(filename):
            for file_meta in handler.crawl_dir(filename, exclude=exclude, include=include):
                process(file_meta, es, show=pargs.show)
        elif os.path.isfile(filename):
            file_meta = handler.get_metadata(filename)
            process(file_meta, es, show=pargs.show)
        else:
            print "%s is not a file/dir. skipping" % filename
if __name__ == '__main__':
    main()

