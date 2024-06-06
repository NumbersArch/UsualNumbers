#!/bin/bash  
#bash timechart.sh "10/2023" "05/2024"

proceed=true
if [ "$#" -lt 2 ]; then
    echo "Needs 2 date parameters (month/year)"
    proceed=false  
fi
if [ "$#" -gt 2 ]; then
    echo "Too many parameters"
    proceed=false  
fi

if [ "$proceed" = true ]; then

date1="$1"
date1assigned=false
if [[ $date1 == *"-"* ]]; then
	month1="$(echo "$date1" | cut -d'-' -f1)"; month1="$( echo "${month1#0}")"
	year1="$(echo "$date1" | cut -d'-' -f2)"
	
	date1assigned=true
fi
if [[ $date1 == *"/"* ]]; then
	month1="$(echo "$date1" | cut -d/ -f1)"; month1="$( echo "${month1#0}")"
	year1="$(echo "$date1" | cut -d/ -f2)"
	date1assigned=true
fi

date2="$2"
date2assigned=false
if [[ $date2 == *"-"* ]]; then
	month2="$(echo "$date2" | cut -d'-' -f1)"; month2="$( echo "${month2#0}")"
	year2="$(echo "$date2" | cut -d'-' -f2)"
	
	date2assigned=true
fi
if [[ $date2 == *"/"* ]]; then
	month2="$(echo "$date2" | cut -d/ -f1)"; month2="$( echo "${month2#0}")"
	year2="$(echo "$date2" | cut -d/ -f2)"
	date2assigned=true
fi

if [ "$date1assigned" = false ] || [ "$date2assigned" = false ]  ; then
echo "dates input improperly"
else

datestring1="$year1-$month1"
datestring2="$year2-$month2"

python3 py/assemble_timechart.py "$datestring1" "$datestring2"

fi
fi
