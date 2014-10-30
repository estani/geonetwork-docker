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

#OPTIONS START
while getopts 'hdip:D:' opt; do
    case "$opt" in
        d) debug=1;;            	#turns debugging on
        i) interactive=1;;      	#starts a shell in the container
        p) script="$OPTARG";;   	#runs python script
	D) dirs="$dirs $OPTARG";;		#directories to share
        h) usage; exit 0;;      	#shows this help
        *) echo "Unknown option $opt"; usage; exit 1;;
    esac
done
#OPTIONS END

#check extra files
[[ -f extra_env ]] && . extra_env


((debug)) && cat <<EOF
script=$script
dirs=$dirs
EOF



if ((interactive)); then
    docker run -ti --rm $image /bin/bash
else
    container="$(docker run -d $docker_opt -v "$container_dir:/container_data" $image /container/boot)"
    mkdir -p "$container_dir/var/run"
    echo "$container" > "$container_dir/var/run/container.name"
    echo "Container $container started with share dir: $container_dir" >&2
fi
