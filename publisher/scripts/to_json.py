#!/usr/bin/env python

from netCDF4 import Dataset
import sys, os, datetime
import json
import logging

import es_api

class SimplePathParser(object):
    """Simple directory parser strategy that is initialized with a string of the form:
        /*/*/*/model/institute/*/variable
        
        When passed a path like: /data/project1/something/mymodel/ABCD/production/ps
        produces a map: {'model': 'mymodel, 'institute':'ABCD', 'variable':ps}"""
    SKIP = '*'
    
    @staticmethod
    def parse_structure(structure, separator):
        metadict = {}
        if structure is not None and len(structure) > 0:
            position = 0
            for value in structure.split(separator):
                if len(value) > 0 and value != SimplePathParser.SKIP:
                    metadict[position] = value
                position += 1
        return metadict

    def __init__(self, dir_structure='', dir_sep=os.sep, file_structure=None, file_sep='_'):
        """The separators are used for splitting the directory and file parts. 
        In the case of directories is only used for parsing the structure, the real separator will be
        read from the OS."""
        self.file_sep = file_sep
        if len(dir_structure) > 0 and dir_structure[0] != '/':
            dir_structure = '/' + dir_structure 
        self.dir_metadict = SimplePathParser.parse_structure(dir_structure, dir_sep)
        self.file_metadict = SimplePathParser.parse_structure(file_structure, file_sep)

    def extract(self, path):
        meta = {}
        parts = os.path.dirname(path).split(os.sep)
        for pos, name in self.dir_metadict.items():
            meta[name] = parts[pos]
        
        parts = os.path.basename(path).split(self.file_sep)
        if '.' in parts[-1]:
            parts[-1] = parts[-1][:parts[-1].rfind('.')]
        for pos, name in self.file_metadict.items():
            meta[name] = parts[pos]
        return meta
            

class NetCDFFileHandler(object):
    CONTAINER_DATA_DIR = '/data/'
    HOST_DATA_DIR_VAR = 'DATA_PATH'

    def __init__(self, path_parser = None):
        self.path_parser = path_parser

    def __extract_from_filename(self, filename):
        
        realpath = os.path.abspath(filename)
        if realpath.startswith(NetCDFFileHandler.CONTAINER_DATA_DIR):
            realpath = os.path.join(os.getenv(NetCDFFileHandler.HOST_DATA_DIR_VAR),
                                    realpath[len(NetCDFFileHandler.CONTAINER_DATA_DIR):])
        if self.path_parser is not None:
            meta = self.path_parser.extract(realpath)
        else:
            meta = {}
        meta['original_path'] = realpath
        return meta
        
    def __extract_variable(self, netcdfVar):
        "Extracts metadata from the given variable."
        meta = {}
        #basic metadata
        meta['dimensions'] = netcdfVar.dimensions
        #extract variable attributes
        for att in netcdfVar.ncattrs():
            meta[att] = netcdfVar.getncattr(att)
        return meta

    def __extract_dimension(self, dim):
        "Extracts metadata from the given dimension"
        meta = {}
        meta['size'] = len(dim)
        meta['unlimited'] = dim.isunlimited()
        return meta

    def crawl_dir(self, path, exclude=[], include=None):
        for root, subdirs, files in os.walk(path):
            for f in files:
                skip = False
                current = os.path.join(root, f)
                for e in exclude:
                    if e.match(current):
                        skip = True
                        break
                if include is not None and not skip:
                    for i in include:
                        if not i.match(current):
                            skip = True
                            break
                if not skip:
                    try:
                        yield self.get_metadata(current)
                    except Exception as e:
                        logging.log(logging.ERROR, "Could not process %s (%s)" % (f, e)) 

    def get_metadata(self, filename):
        meta = self.__extract_from_filename(filename)
        with Dataset(filename, 'r') as f:
            meta['global'] = {}
            for g_att in f.ncattrs():
                meta['global'][str(g_att)] = getattr(f, g_att)
            meta['variables'] = {}
            for var in f.variables:
                meta['variables'][var] = self.__extract_variable(f.variables[var])
            meta['dimensions'] = {}
            for dim in f.dimensions:
                meta['dimensions'][dim] = self.__extract_dimension(f.dimensions[dim])
        return meta
    
def process(meta, elasticsearch, show=True, dry_run=True):
    if show:
        print json.dumps(meta, indent=2)
    if not dry_run:
        elasticsearch.publish(meta)

def main(args=sys.argv[1:]):
    import argparse
    parser = argparse.ArgumentParser(description='Extracts metadata from Netcdf files')
    parser.add_argument('files', nargs='+')
    parser.add_argument('--show', action='store_true', help='show produced json')
    parser.add_argument('--dry-run', action='store_true', help="Don't publish anything")
    parser.add_argument('--dir-structure', help='Metadata directory structure (e.g. /*/institute/model/realm so /a/b/c/d/e -> institute=b, model=c,realm=d) ')
    parser.add_argument('--exclude-crawl', help='Exclude the given regular expression while crawling')
    parser.add_argument('--include-crawl', help='Include only the given regular expression while  crawling')
    parser.add_argument('-p', '--port', type=int, help='elastic search port (default 9200)', default=9200)
    parser.add_argument('--host', help='Elastic search host')
    pargs = parser.parse_args(args)

    #handle input properly
    if pargs.dir_structure is not None:
        path_parser = SimplePathParser(pargs.dir_structure)
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
        es = es_api.ES(es_api.ESFactory.basicConnector(pargs.host, port=pargs.port))
    else:
        es = es_api.ES()

    for filename in pargs.files:
        if os.path.isdir(filename):
            for file_meta in handler.crawl_dir(filename, exclude=exclude, include=include):
                process(file_meta, es, show=pargs.show, dry_run=pargs.dry_run)
        elif os.path.isfile(filename):
            file_meta = handler.get_metadata(filename)
            process(file_meta, es, show=pargs.show, dry_run=pargs.dry_run)
        else:
            print "%s is not a file/dir. skipping" % filename
if __name__ == '__main__':
  main()

