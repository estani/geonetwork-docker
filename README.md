geonetwork-docker
=================

Docker environments for different containers and uses.


General
-------

Most containers are controlled by the same commands and have a similar construction


Commands
~~~~~~~~

build.sh := to build the image
run.sh := to start it (-h for some options, default shared directory /tmp/`<image_name>`)
stop.sh := stop gracefully geonetwork (you must provide either the container shared directory (-c) or the container name (-C))

Architecture
~~~~~~~~~~~~

For containers meant to be run as daemons, there will be a xinetd installed which will listen to some port (default 10101) which in turn
starts a command handler passing commands to underlying scripts.
This construct is meant to be reused, so by adding a simple stop.sh script in *image*/container/controller.d which takes care of shutting down
the container in some proper manner, you'll be able to properly shut down the container from your host by issuing:
```bash
nc $ip 10101 <<<stop
```
where `$ip` is the ip of the conainer holding it (so the access is effectively concelaid from the outside)

This is only one example. You may develop any other script that can be called from the outside in the same manner.

Implementations
---------------

[search](search/Readme.md): elastic-search container
[publisher](publisher/Readme.md): meta-data extractor which writes NetCDF files metadata to json and can send it directly to an elastic-search instance
