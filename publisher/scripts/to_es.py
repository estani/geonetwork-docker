#!/usr/bin/env python
from elasticsearch import Elasticsearch
from datetime import datetime
import os

class ESFactory(object):
    DEFAULT_PORT = 9200
    
    @staticmethod
    def fromDockerEnvironment(port=ESFactory.DEFAULT_PORT, ssl=False):
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


