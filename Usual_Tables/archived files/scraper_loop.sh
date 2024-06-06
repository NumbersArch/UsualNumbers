#!/bin/bash  
#example command: bash scraper_loop.sh "10/2023" "05/2024" "y"
#runs "scraper.sh" between two dates, optional query answer 


queryanswer=""
answered=false
proceed=true
if [ "$#" -lt 2 ]; then
    echo "Needs 2 date parameters (month/year)"
    proceed=false  
fi
if [ "$#" -eq 3 ]; then
	if [ "$3" = "y" ] || [ "$3" = "n" ]; then
		queryanswer="$3"
		answered=true
	else 
    		proceed=false
    	fi  
fi

if [ "$#" -gt 3 ]; then
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

y=$year1; m=$month1
while [[ $y -lt $year2 ]] || [[ $m -le $month2 ]]
do
	if [ $answered = true ]; then
		bash scraper.sh "$m/$y" "$queryanswer"
	else
		bash scraper.sh "$m/$y"
	fi
	m=$((m+1))
	if [[ $m -gt 12 ]] ; then
		m=1
		y=$((y+1))
	fi
done

fi
fi
