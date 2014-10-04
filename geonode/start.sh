#!/bin/bash

cd /geonetwork/node/jetty
(rm logs/*request.log* 
rm logs/output.log
mv logs/geonetwork.log.* logs/archive
mv logs/geoserver.log.* logs/archive) 2>/dev/null

data_dir=/data/geonetwork_data
lucene_dir=/data/lucene

(mkdir -p /data_dir
mkdir -p /lucene_dir) 2>/dev/null

java -Xms48m -Xmx512m -Xss2M -XX:MaxPermSize=128m -Dgeonetwork.dir="$data_dir" -Dgeonetwork.lucene.dir="$lucene_dir" -Djeeves.filecharsetdetectandconvert=enabled -Dmime-mappings=../web/geonetwork/WEB-INF/mime-types.properties -DSTOP.PORT=8079 -Djava.awt.headless=true -DSTOP.KEY=geonetwork -jar start.jar
