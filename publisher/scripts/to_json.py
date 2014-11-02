#!/usr/bin/env python

from netCDF4 import Dataset
import sys, os, datetime
import json

def get_test_data():
    pass

def extract_variable(netcdfVar):
    meta = {}
    #basic metadata
    meta['dimensions'] = netcdfVar.dimensions
    #extract variable attributes
    for att in netcdfVar.ncattrs():
        meta[att] = netcdfVar.getncattr(att)
    return meta

def extract_dimension(dim):
    meta = {}
    meta['size'] = len(dim)
    meta['unlimited'] = dim.isunlimited()
    return meta

def get_metadata(filename):
    meta = {}
    with Dataset(filename, 'r') as f:
        meta['global'] = {}
        for g_att in f.ncattrs():
            meta['global'][str(g_att)] = getattr(f, g_att)
        meta['variables'] = {}
        for var in f.variables:
            meta['variables']['var'] = extract_variable(f.variables[var])
        meta['dimensions'] = {}
        for dim in f.dimensions:
            meta['dimensions'][dim] = extract_dimension(f.dimensions[dim])
    return meta

def main(args=sys.argv):
    #handle input properly
    filename=args[1]
    print json.dumps(get_metadata(filename), indent=2)

if __name__ == '__main__':
  main()

