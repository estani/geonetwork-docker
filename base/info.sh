#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
image="$(basename $SCRIPT_DIR)"

get_ip() {
     docker inspect --format '{{.NetworkSettings.IPAddress}}' $container_name
}

#defaults
container_dir=/tmp/$image
while getopts "c:C:" opt; do
    case "$opt" in
        c) container_dir="$OPTARG";;    #defines the directory for the container files
        C) container_name="$OPTARG";;   #defines the container name
    esac
done
shift $((OPTIND-1))
[[ -z "$container_name" && "$container_dir" ]] && container_name="$(cat "$container_dir/var/run/container.name")"

#process commands
while (($#)); do
 case "$1" in
    ip) get_ip;;
 esac

 shift
done

