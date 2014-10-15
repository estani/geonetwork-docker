#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
image="$(basename $SCRIPT_DIR)"

usage() {
    cat<<EOF
Usage: $0 [options] [container_name] 

Either define the container name or pass the shrade directory of this container.

options:
$(sed -n '/^#OPTIONS START/,/#OPTIONS END/ {s/ *\([^)]\+\))[^#]\+#\(.*\)/\1\t: \2/p}' $0)
EOF
}

get_container_ip () {
    $(dirname $SCRIPT_DIR)
    docker inspect --format '{{.NetworkSettings.IPAddress}}' $1
}

#defaults
container_dir=/tmp/$image
while getopts "c:" opt; do
    case "$opt" in
        c) container_dir="$OPTARG";;    #defines the directory for the container files
        h) usage; exit 0;;              #this help
        *) echo "Unknown command $opt"; exit 1;;
    esac
done
shift $((OPTIND-1))
[[ "$1" ]] && container_name="$1"

[[ -z "$container_name" && "$container_dir" ]] && container_name="$(cat "$container_dir/var/run/container.name")"

ip=$(get_container_ip $container_name)
port=10101

nc $ip $port <<<'stop'
