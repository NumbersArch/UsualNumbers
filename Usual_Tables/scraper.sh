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
autoanswer=""
if [ "$#" -eq 2 ]; then
    if [ "$2" == "y" ] || [ "$2" == "n" ]; then
    	autoanswer="$2"
    else
    	proceed=false
    fi
    
fi

if [ "$#" -gt 2 ]; then
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
urls="$(echo "$ids" | awk '{print "'$prestring'" $0 "'/$datestring'"}')"

rname="raw"
if [ ! -d "$rname"  ]; then mkdir "$rname"; fi
dname="$rname/Html"
if [ ! -d "$dname"  ]; then mkdir "$dname"; fi
filestring="$dname/$datestring"
if [ ! -d "$filestring"  ]; then mkdir "$filestring"; fi

while IFS= read -r line; do
	url="$line"
	filename=${url#"$prestring"}
	filename=${filename%"/$datestring"}
	if [ ! -f "$filestring/$filename"  ]; then
		wget --random-wait -w 3 -O "$filestring/$filename" "$url"
	fi
done <<< "$urls"

# query the user to overwrite processed
overwrite=false
broken=true
if [[ $autoanswer == "y" ]]; then
	overwrite=true
	broken=false
elif [[ $autoanswer == "n" ]]; then
	overwrite=false
	broken=false
else

	printf "Overwrite process files [y/n]? (q to quit) \n"
	while true; do
		read answer

		if [ "$answer" != "${answer#[Yy]}" ] ;then 
			overwrite=true
			broken=false
			break;
		elif [ "$answer" != "${answer#[Nn]}" ] ;then 
			broken=false
			break;
		elif [ "$answer" != "${answer#[Qq]}" ] ;then 
			broken=true; break;
		else
		    echo "Wrong option selected."
		fi
	done

fi

if [ "$broken" = false ]; then 
echo "================================="
python3 .py/process.py "$datestring" "$overwrite"
python3 .py/assemble_list.py
fi
echo "Done"
fi
fi
