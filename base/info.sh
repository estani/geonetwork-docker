#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
image="$(basename $SCRIPT_DIR)"

usage() {
    cat<<EOF
Usage: $0 [options]

options:
$(sed -n '/^#OPTIONS START/,/#OPTIONS END/ {s/ *\([^)]\+\))[^#]\+#\(.*\)/\1\t: \2/p}' $0)
EOF
}

get_ip() {
     docker inspect --format '{{.NetworkSettings.IPAddress}}' $container_name
}

list_containers_for() {
    local image=${1:${image}}
    echo "------------------"
    echo "Running Containers"
    echo "------------------"
    docker ps | grep ${image} | awk '{print $NF}'
    echo "------------------"
}

#defaults
container_dir=/tmp/$image
[[ $# == 0 ]] && { list_containers_for ${image} ; exit $?; }
#OPTIONS START
while getopts "c:n:l:h" opt; do
    case "$opt" in
        c) container_dir="$OPTARG";;    #defines the directory for the container files
        n) container_name="$OPTARG";;   #defines the container name
        h) usage && exit 0;; #this help info
        l) list_containers_for $OPTARG;; #list names running containers
    esac
done
#OPTIONS END
shift $((OPTIND-1))
[[ -z "$container_name" && "$container_dir" ]] && container_name="$(cat "$container_dir/var/run/container.name")"

#process commands
while (($#)); do
 case "$1" in
    ip) get_ip;;
     *) usage && exit 1;;
 esac

 shift
done

