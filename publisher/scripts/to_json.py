#!/usr/bin/env python

from netCDF4 import Dataset
import sys, os, datetime
import json

def get_test_data():
    pass

def get_metadata(filename):
    meta = {}
    with Dataset(filename, 'r') as f:
        #meta['global'] = {}
        for g_att in f.ncattrs():
            meta[g_att] = getattr(f, g_att)
    return meta

def main(args=sys.argv):
    #handle input properly
    filename=args[1]
    print json.dumps(get_metadata(filename), indent=2)

if __name__ == '__main__':
  main()

