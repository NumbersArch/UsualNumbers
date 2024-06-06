#!/usr/bin/env python
#example: python3 process.py "2024-5"
#takes html files and strips relevant data. Copies to processed folder if option selected
import html2text
import sys
import os
from os import listdir
from os.path import isfile, join

sname = join("raw","Html")
rname = join("raw","txt")
pname = "processed"
vname = "Vtubers.txt"

datestring=str(sys.argv[1])
overwriteinput=sys.argv[2]

overwrite=False
if overwriteinput == "true": overwrite=True;
if overwriteinput == "false": overwrite=False;

workingdirectory = os.path.dirname(os.path.realpath(__file__))
up1directory = os.path.dirname(workingdirectory)
filedirectory = join(up1directory,sname,datestring)
txtdirectory = join(up1directory,rname,datestring)
finisheddirectory = join(up1directory,pname,datestring)
textpath = join(up1directory,vname)
if not os.path.exists(finisheddirectory):
    os.makedirs(finisheddirectory)
if not os.path.exists(filedirectory):
    os.makedirs(filedirectory)
if not os.path.exists(txtdirectory):
    os.makedirs(txtdirectory)

files = [f for f in listdir(filedirectory) if isfile(join(filedirectory, f))]	
allids = [f for f in files]

# getting names and ID's from the vtubers file, in order to assign names to files
def interpretText(path):
	with open(path, 'r') as reader:
		text=reader.readlines()
	names = []; ids = []; sexes = [];
	name=""; agency=""; sx=""; gen=""; company=""
	for t in text:
		if(t.startswith("Company: ")):
			company = t.replace("Company: ", "").strip(); continue;
		if(t.startswith("Agency: ")):
			agency = t.replace("Agency: ", "").strip(); continue;
		if(t.startswith("Sex: ")):
			sx = t.replace("Sex: ", "").strip(); continue;
		if(t.startswith("Gen: ")):
			gen = t.replace("Gen: ", "").strip(); continue;
		if(t.startswith("Name: ")):
			name = t.replace("Name: ", "").strip(); continue;
		if(t.startswith("ID: ")):
			idname = t.replace("ID: ","").strip();
			rs = company +" > " +agency +" > " +gen +" > " +name
			sexes.append(sx)
			names.append(rs)
			ids.append(idname)
	return names, sexes, ids

def getPaths(idarr, totalarr, directory):
	returnids = []
	for i in idarr:
		if i not in totalarr:
			print("HTML file missing: " + i)
			sys.exit(0)
		else:
			returnids.append(join(directory, i))
	return returnids
	
namearr, sexarr, idarr = interpretText(textpath)
paths = getPaths(idarr, allids, filedirectory)

# Naming the interpreted files
titlearr = []
for e, n in enumerate(namearr):
	filestring = namearr[e].rsplit(" > ",1)[1]
	titlearr.append(filestring)

for e, f in enumerate(paths):
	cpn, agn, gen, name = namearr[e].split(" > ")
	idn=idarr[e];
	filename = titlearr[e]; path = paths[e]
	genpath = join(txtdirectory, cpn, agn, gen)
	endpath = join(genpath,filename +".txt")
	
	if not os.path.exists(endpath):
		h = html2text.HTML2Text(); h.ignore_links = True
		htmlfile = open(path, 'r')
		html_string = htmlfile.read()    
		s = h.handle(html_string)
		
		# getting values out of html file
		durarray=[]; timearray=[]; meanarray=[]; peakarray=[]; namearray=[]
		prevline = ""
		sp = s.split("\n\n")
		for en, line in enumerate(sp):
			if(" / " in line and line.startswith("__") and ":" in prevline and prevline.startswith("__")):
				rawtime, rawdur = prevline.rsplit(" ",1)
				rawdur = rawdur.replace("_","").strip()
				rawtime = rawtime.replace("_","").strip()
				hours, minutes = rawdur.split(":")
				totmin = int(hours)*60+int(minutes)
				
				numbers = line.split("__")[1].strip()
				numbers = numbers.replace(",","")
				mean, peak = numbers.split(" / ")
				
				title = sp[en-2]
				
				durarray.append(totmin); meanarray.append(mean); peakarray.append(peak); namearray.append(title); timearray.append(rawtime)
			prevline = line
		
		printstring = ""
		for i in range(len(namearray)): 
			blockstring = "Title: "+namearray[i]+"\n" 
			blockstring = blockstring+ "Time: " + str(timearray[i])+"\n" 
			blockstring = blockstring+ "Duration: " + str(durarray[i])+"\n" 
			blockstring = blockstring+ "Mean: " + str(meanarray[i])+"\n" 
			blockstring = blockstring+ "Peak: " + str(peakarray[i])
			printstring = printstring+"\n\n"+blockstring
		printstring = printstring.strip()
	
		if not os.path.exists(genpath):
			os.makedirs(genpath)
		endfile = open(endpath, "w")
		endfile.write(printstring)
		endfile.close()
	if overwrite == True:
		finaldirectory = join(finisheddirectory, cpn, agn,gen)
		finalpath = join(finaldirectory,filename +".txt")
		fn = open(endpath, 'r')
		wstring = fn.read() 
		if wstring.strip() != "":
			if not os.path.exists(finaldirectory):
				os.makedirs(finaldirectory)
			finalfile = open(finalpath, "w")
			finalfile.write(wstring)
			finalfile.close()
	
print("HTML files interpreted and placed in "+ "\""+ rname+ "\"")
if overwrite == True:
	print("Copied to "+ "\""+ pname+ "\""+" directory")


