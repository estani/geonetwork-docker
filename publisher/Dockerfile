FROM ubuntu:14.04

#tell debian based distros to forget about user input
ENV DEBIAN_FRONTEND noninteractive

#update the de distro and install some basic tools
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y curl git vim emacs

#prepare the build environment
RUN apt-get update && apt-get install -y build-essential

#*************  DEPENDENCIES
#szip dependency
RUN curl ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4/szip-2.1.tar.gz | tar xz && \
    cd szip-2.1 && \
    ./configure && \
    make && \
    make install
#hdf5 dependency
RUN curl ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4/hdf5-1.8.13.tar.gz | tar xz && \
    cd hdf5-1.8.13 && \
    ./configure && \
    make && \
    make install

#LD_LIBRARY_PATH
#install
RUN curl ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4.3.2.tar.gz | tar xz && \
    
#setting up the node
#RUN rm -r /geonetwork/node/jetty/logs && \
#    ln -s /logs /geonetwork/node/jetty/logs

#experimenting with xinet.d
#RUN apt-get -y install xinetd && \
#    echo "container\t10101/tcp" >>/etc/services 

#ADD xinetd.d/container /etc/xinetd.d/container
#ADD container/controller /container/controller
#ADD container/controller.d/start /container/controller.d/start
#ADD container/controller.d/stop /container/controller.d/stop
#ADD container/boot /container/boot

#ENV CONTAINER_DATA /container_data

#9200  elastic search
#10101 container controller


