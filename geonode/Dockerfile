FROM ubuntu:14.04

#tell debian based distros to forget about user input
ENV DEBIAN_FRONTEND noninteractive

#update the de distro and install some basic tools
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y curl git vim emacs

#Install java (curl command will certainly break if oracle changes his download policy)
RUN echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections
RUN curl -L -C - -b "oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/7u67-b01/jdk-7u67-linux-x64.tar.gz >jdk-7u67-linux-x64.tar.gz
RUN mkdir -p /opt/java && \
	cd /opt/java && \
	tar xzvf /jdk-7u67-linux-x64.tar.gz && \
    rm /jdk-7u67-linux-x64.tar.gz
ENV PATH /opt/java/jdk1.7.0_67/bin:$PATH
ENV JAVA_HOME /opt/java/jdk1.7.0_67

#install geonetwork
RUN mkdir /geonetwork && \
    cd /geonetwork && \
    curl 'http://downloads.sourceforge.net/project/geonetwork/GeoNetwork_opensource/v2.10.3/geonetwork-install-2.10.3-0.jar?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fgeonetwork%2Ffiles%2FGeoNetwork_opensource%2Fv2.10.3%2F&ts=1412423208&use_mirror=softlayer-ams' -L > /geonetwork/installer.jar
ADD install.xml /geonetwork/install.xml
RUN cd /geonetwork && java -jar installer.jar install.xml
RUN rm /geonetwork/installer.jar

#setting up the node
RUN rm -r /geonetwork/node/jetty/logs && \
    ln -s /logs /geonetwork/node/jetty/logs

#experimenting with xinet.d
RUN apt-get -y install xinetd && \
    echo "container\t10101/tcp" >>/etc/services 

ADD container /etc/xinetd.d/container
ADD controller /container/controller
ADD start /container/controller.d/start
ADD stop /container/controller.d/stop
ADD boot /container/boot

ENV CONTAINER_DATA /container_data

#8080  main web server
#10101 container controller
EXPOSE 8080 10101

