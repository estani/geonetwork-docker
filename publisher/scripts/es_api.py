#!/usr/bin/env python
from elasticsearch import Elasticsearch
from datetime import datetime
import os

class ESFactory(object):
    
    @staticmethod
    def fromDockerEnvironment(port=9200, ssl=False):
        "port is the elastic search internal port (typically 9200)"
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
            #simple ssl setting for all servers
            server['use_ssl'] = ssl
        
        return Elasticsearch(servers.values())

class ES(object):
    INDEX = 'geonetwork'
    FILE_TYPE = 'file'

    def __init__(self, connector = None):
        if connector is None:
            self.es = ESFactory.fromDockerEnvironment()
        else:
            self.es = connector
    def getId(self, data):
        "Extract an id for the given data"
        if 'original_path' in data:
            return data['original_path']
        else:
            return None
              
    def publish(self, values):
        "publish the dictionary in values to elastic search"
        self.es.index(index=ES.INDEX, doc_type=ES.FILE_TYPE, id=self.getId(values), body=values)
