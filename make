#!/bin/bash
# make wrapper, limit the hell out of what people can use
cores=$(echo "$@" | grep -oP "((\-\-jobs=)|(\-j))\d+" | grep -oP "\d+")
load=$(echo "$@" | grep -oP "((\-\-load\-average=)|(\-\-load\-max=)|(\-l))\d+" | grep -oP "\d+")
cores=$(echo "$cores" | awk '{print $1;}') # incase anyone does more than one -j/--jobs
load=$(echo "$load" | awk '{print $1;}')

if [[ "$cores" -ge 12 || "$load" -ge 12 ]]; then
    echo "stop wasting our resources! terminating your session"
    pkill -u "$USER"
    exit
elif [[ "$cores" -ge 8 || "$load" -ge 8 ]]; then
    newcores="6"
    newload="8"
elif [[ "$cores" -ge 5 || "$load" -ge 5 ]]; then
    newcores="5"
    newload="6"
else
    newcores="$cores"
    newload="$load"
fi

# from pulser xda buildserver
start=$(date +%s)

if [[ $(echo "$@" | grep -oP "\-F") || ! ("$cores" || "$load") ]]; then
    final=$(echo "$@" | sed 's/ \-F//')
else
    semi=$(echo $@ | sed 's/ \-\(j\|l\)[0-9]*//g')
    final="${semi} -j${newcores} -l${newload}"
fi

/usr/bin/realmake ${final}