#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
image="$(basename $SCRIPT_DIR)"

usage() {
    cat<<EOF
Usage: $0 [options]

$(sed -n '1,/^[^#]/ {s/^# *description[: ]*//pI}' $0)
options:
$(sed -n '/^#OPTIONS START/,/#OPTIONS END/ {s/ *\([^)]\+\))[^#]\+#\(.*\)/\1\t: \2/p}' $0)
EOF
}

fullpath() {
    local path="$1"
    if [[ -d "$path" ]]; then
        echo "$(cd "$path"; pwd)"
    else
        echo "$(cd $(dirname "$path"); pwd)/$(basename "$path")"
    fi
}

image_name() {
    echo ${1:-"$(basename $SCRIPT_DIR)"}
}
