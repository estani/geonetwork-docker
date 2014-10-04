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

#defaults
log_dir=/tmp/$image/logs
data_dir=/tmp/data

#OPTIONS START
while getopts 'hdiD:l:' opt; do
    case "$opt" in
        D) data_dir="$OPTARG";; #defines dir for data
        l) log_dir="$OPTARG";;  #defines dir for logs
        d) debug=1;;            #turns debugging on
        i) interactive=1;;      #starts a shell in the container
        h) usage; exit 0;;      #shows this help
        *) echo "Unknown option $opt"; usage; exit 1;;
    esac
done
#OPTIONS END

[[ -d "$data_dir" ]] || { echo "data dir '$data_dir' is missing."; usage; exit 1; }
[[ -d "$log_dir" ]] || mkdir -p "$log_dir"


((debug)) && cat <<EOF
data_dir=$data_dir
log_dir=$log_dir
EOF

if ((interactive)); then
    docker run -ti --rm -v "$data_dir:/data" -v "$log_dir:/logs" $image /bin/bash
else
    docker run -d -v "$data_dir:/data" -v "$log_dir:/logs" $image /start.sh
fi
