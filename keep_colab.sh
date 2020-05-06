#!/bin/bash
url="$1"
for i in `seq 0 12`
do
  echo "[$i]" ` date '+%y/%m/%d %H:%M:%S'` "connected."
  xdg-open "$url"
  sleep 3600
done
