#!/usr/bin/env python
from elasticsearch import Elasticsearch
from datetime import datetime
import os

class ESFactory(object):
    
    @staticmethod
    def fromDockerEnvironment(port=9200):
        "Read connection from docker linked container. Port is the elastic search internal port (typically 9200)"
        servers = {}
        for var_name in [var for var in os.environ if ("_PORT_%s_TCP" % port) in var]:
            parts = var_name.split('_')
            if parts[0] not in servers:
                servers[parts[0]] = {}
            server = servers.get(parts[0])
            if parts[-1] == 'ADDR':
                server['host'] = os.environ[var_name]
            elif parts[-1] == 'PORT':
                server['port'] = int(os.environ[var_name])
        
        return ES(Elasticsearch(servers.values()))

    @staticmethod
    def basicConnector(host, port=9200, url_prefix='', use_ssl=False, timeout=10, **other_options):
        "Create a simple elastic search connector"
        options = dict(host=host, port=port, url_prefix=url_prefix, use_ssl=use_ssl, timeout=timeout)
        options.update(other_options)
    
        return ES(Elasticsearch([options]))

class ES(object):
    INDEX = 'geonetwork'
    FILE_TYPE = 'file'

    def __init__(self, connector):
        self.es = connector

    def getId(self, data):
        "Extract an id for the given data"
        if 'original_path' in data:
            return data['original_path']
        else:
            return None
              
    def publish(self, values):
        "publish the dictionary in values to elastic search"
        return self.es.index(index=ES.INDEX, doc_type=ES.FILE_TYPE, id=self.getId(values), body=values)

    def get(self, id):
        "Get the document for the given id"
        return self.es.get(index=ES.INDEX, doc_type=ES.FILE_TYPE, id=id)

    def search(self, body, **options):
        return self.es.search(index=ES.INDEX, doc_type=ES.FILE_TYPE, body=body, **options)
