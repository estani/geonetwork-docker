#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
image="$(basename $SCRIPT_DIR)"

get_container_ip () {
    docker inspect --format '{{.NetworkSettings.IPAddress}}' $1
}

#defaults
container_dir=/tmp/$image
while getopts "c:C:" opt; do
    case "$opt" in
        c) container_dir="$OPTARG";;    #defines the directory for the container files
        C) container_name="$OPTARG";;   #defines the container name
    esac
done
[[ -z "$container_name" && "$container_dir" ]] && container_name="$(cat "$container_dir/var/run/container.name")"

ip=$(get_container_ip $container_name)
port=10101

nc $ip $port <<<'stop'
