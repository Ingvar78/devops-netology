#!/bin/bash

OUTPUT=$(cat "/proc/cpuinfo" | grep flags| uniq )

echo -e $OUTPUT
IFS=' '
read -ra flags <<< "$OUTPUT"

for i in "${flags[@]}"; do
    echo -e $i |grep sse
done

