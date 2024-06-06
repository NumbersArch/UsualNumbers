Vstats Data scraper.
(see "how to use" below)

>> ** Requirements ** <<
----------------------
-- bash
-- python3
-- pandas

=== FILE DESCRIPTIONS ===
-------------------
Vtubers_all.txt
description) Where all vtuber names are collected. 
~ tagging ~ 
The file is read from top to bottom and applies the attributes "Company, Agency, Gen, Sex, Name" to the ID's below them. 
EX] There is no need to write the agency for each individual, all ID's below that "agency" tag are applied with the tag, until a new agency is declared.
-- The tags need a colon and space. 'Company: Cover' 
** Including the ID's is mandatory (They are easily found in the URL of the vtuber's page on Vrabi or Vstats)
** leaving out any attributes could potentially cause errors
** Lines without tags such as "~~~~~~" are simply used to structure things visually. They aren't necessary.
~ numbering ~
You can number the tags to sort your file structure. To do this apply a number to the name with a ") ". 
EX] "Company: 1) Cover". Now the "Cover" folder will be ordered first in the file structure. This feature is most useful for ordering gens.
** numbering is not mandatory but is nice for ordering the folders

Vtubers.txt
Uses the same format as Vtubers_all.txt, except only include the names you want downloaded/processed. This way the list can be limited as you desire. 

scraper.sh [date] [query answer y/n (optional)]
# example command 1: bash scraper.sh "05/2024"
# example command 2: bash scraper.sh "04-2023"
** The month and year are mandatory, two formats are supported either "/" or "-"
# example command 3: bash scraper.sh "03/2022" "y"
** you can also input the query answer beforehand to save time if you like
description) 
> Reads Vtubers.txt and downloads html files to the "raw/HTML" folder. If the file already exists in the html folder the download will be skipped. 
** if you download data midway through the month, you will be stuck with an html file with partial data. The file will have to be deleted to be re-downloaded. 
> It then pulls the relevant data from the file and places it in the "raw/txt" folder. 
> If the option is selected, it will then copy the files to the "processed" folder and overwrite them.
** the purpose of the "processed" folder is to manually adjust values. If those files are overwritten your manual adjustments will be lost. 

list_all.txt
All vtubers in the "Vtubers_all.txt" file are placed here in a structured order. This is a reference file to be used with other charting programs.

chart.txt
A copy of list_all.txt, except you can select which vtubers you want included in the chart. 
~ commenting ~
If a company, agency, gen, or name is unwanted, simply comment the line "#". No need to comment every name.
EX]
Cover
	Hololive EN
		Myth
			Gawr Gura
			Ninomae Ina'nis
	#		Ame
			Calliope Mori
			Takanashi Kiara
		#Promise
			Ceres Fauna
			Nanashi Mumei
			Hakos Baelz
			Ouro Kronii
			IRyS
Nobody in Promise, nor Ame will be included in the chart. 
** remember the handy command Ctrl+H can help you remove the "#"
** comments anywhere on the left side work, but the tabbing needs to remain the same

chart.sh [date]
# example command 1: bash chart.sh "05/2024"
# example command 2: bash chart.sh "04-2023"
** The month and year are mandatory, two formats are supported either "/" or "-"
description) 
> Reads processed files and constructs a chart from the data. Charts are placed into the "charts" directory. 
> Two different charts are assembled. A combined chart with all the data, or a separated side-by-side chart in the format of the "Usual tables"

timechart.txt
A copy of list_all.txt, except you can select which vtubers you want included in the chart. 
~ commenting ~
If a company, agency, gen, or name is unwanted, simply comment the line "#". No need to comment every name.

timechart.sh [date 1] [date 2]
# example command 1: bash timechart.sh "03/2023" "05/2024"
# example command 1: bash timechart.sh "03-2023" "05-2024"
** The month and year are mandatory, two formats are supported either "/" or "-"
description)
Reads processed files, all files between two dates are read and placed into a timeseries chart. This way you can track the performance of multiple metrics over time. 


=== HOW TO USE ===
------------------
Downloading/Processing Data
Step 1) Add vtubers to "Vtubers_all.txt". Build out the list as much as you desire. Get their ID's by going to their vrabi or vstats page. "https://www.vstats.jp/brands" to get started. It's in the URL and starts with "UC".
Step 2) Copy "Vtubers_all.txt" and rename the copy "Vtubers.txt", deleting the old "Vtubers.txt" if necessary. Edit the list and remove the vtubers you don't want downloaded. Number the items as you wish (see "numbering" above)
Step 3) Run "scraper.sh" for the desired month/year. Open the raw folder and check your files downloaded properly. If it's the first run, select "y" to copy the files into the "processed" folder. 
Step 4) Open the "processed" folder and edit the data as you wish. If you feel a stream should have a lower peak, go ahead and edit it. Be cautious that any edits will be overwritten by "scraper.sh" if you select "y" again.

Charting
Step 5) Copy "list_all.txt" and rename the copy "chart.txt". Comment or delete the agencies/names you don't want included in the chart (see "commenting" above)
Step 6) Run "chart.sh" for the desired month/year. Check the data in the "charts/tables" folder. 
Step 7) Rename or relocate the charts you don't want overwritten by the next run of "charts.sh". 

Timeseries Charting
Step 8) Copy "list_all.txt" and rename the copy "timechart.txt". Comment or delete the agencies/names you don't want included in the chart (see "commenting" above)
Step 9) Run "timechart.sh" between the desired dates. Check the data in the "charts/timeseries" folder.
Step 10) Rename or relocate the charts you don't want overwritten by the next run of "charts.sh". 
** scraper_loop.sh can help you


