#!/usr/bin/env python

from netCDF4 import Dataset
import sys, os, datetime
import json

import es_api

class SimpleDirectoryParser(object):
    """Simple directory parser strategy that is initialized with a string of the form:
        /*/*/*/model/institute/*/variable
        
        When passed a path like: /data/project1/something/mymodel/ABCD/production/ps
        produces a map: {'model': 'mymodel, 'institute':'ABCD', 'variable':ps}"""
    DIR_SEP = '/'
    SKIP = '*'

    def __init__(self, parsingDescription):
        position = 0
        self.metadict = {}
        for value in parsingDescription.split(SimpleDirectoryParse.DIR_SEP):
            if value != SimpleDirectoryParser.SKIP:
                self.metadict[position] = value
            position += 1

    def extract(self, path):
        parts = path.split(os.sep)
        meta = {}
        for pos, name in self.metadict.items():
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
            realpath = os.path.join(realpath[len(NetCDFFileHandler.CONTAINER_DATA_DIR):],
                                        os.getenv(NetCDFFileHandler.HOST_DATA_DIR_VAR).strip('/'))
        if self.path_parser is not None:
            meta = self.path_parser(realpath)
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

def main(args=sys.argv[1:]):
    import argparse
    parser = argparse.ArgumentParser(description='Extracts metadata from Netcdf files')
    parser.add_argument('files', nargs='+')
    parser.add_argument('--show', action='store_true', help='show produced json')
    parser.add_argument('--dry-run', action='store_true', help="Don't publish anything")
    pargs = parser.parse_args(args)

    #handle input properly
    handler = NetCDFFileHandler()
    es = es_api.ES()
    for filename in pargs.files:
        file_meta = handler.get_metadata(filename)
        if pargs.show:
            print json.dumps(file_meta, indent=2)
        if not pargs.dry_run:
            es.publish(file_meta)

if __name__ == '__main__':
  main()

