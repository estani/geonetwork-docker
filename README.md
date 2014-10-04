geonetwork-docker
=================

Docker environments for differen geonetwork servers and uses.

geonode
-------

A simple geonetwork node.

Commands
~~~~~~~~

build.sh := to build the image
run.sh := to start it (-h for some options, default shared directory /tmp/`<image_name>`)
stop.sh := stop gracefully geonetwork (you must provide either the container shared directory (-c) or the container name (-C))
