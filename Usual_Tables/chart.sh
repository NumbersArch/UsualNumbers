#!/bin/bash  
#bash scraper.sh "05/2024"
filename="Vtubers.txt"
prestring="https://www.vstats.jp/channels/1:"
sleeptime=1

proceed=true
if [ "$#" -lt 1 ]; then
    echo "Input date parameter (month/year)"
    proceed=false  
fi
if [ "$#" -gt 1 ]; then
    echo "Too many parameters"
    proceed=false  
fi

if [ "$proceed" = true ]; then

date="$1"
dateassigned=false
if [[ $date == *"-"* ]]; then
	month="$(echo "$date" | cut -d'-' -f1)"; month="$( echo "${month#0}")"
	year="$(echo "$date" | cut -d'-' -f2)"
	
	dateassigned=true
fi
if [[ $date == *"/"* ]]; then
	month="$(echo "$date" | cut -d/ -f1)"; month="$( echo "${month#0}")"
	year="$(echo "$date" | cut -d/ -f2)"
	dateassigned=true
fi

if [ "$dateassigned" = false ]; then
echo "no date assigned"
else
ids="$(grep ^'ID: ' $filename | cut -d' ' -f2- | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"

datestring="$year-$month"

python3 py/assemble_chart.py "$datestring"

fi
fi
