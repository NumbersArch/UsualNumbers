#!/usr/bin/env python
#
import sys
import os
from os import listdir
from os.path import isfile, join

vname = "Vtubers_all.txt"
lname = "list_all.txt"
marker = ") "

workingdirectory = os.path.dirname(os.path.realpath(__file__))
up1directory = os.path.dirname(workingdirectory)
path = join(up1directory,vname)
finalpath = join(up1directory,lname)

def splitMarker(instring, marker):
	if marker in instring:
		return instring.split(marker,1)[1]
	return instring

# interpreting file
with open(path, 'r') as reader:
	text=reader.readlines()
names = []; ids = [];
name="";
for t in text:
	if(t.startswith("Company: ")):
		company = splitMarker(t.replace("Company: ", ""), marker).strip(); continue;
	if(t.startswith("Agency: ")):
		agency = splitMarker(t.replace("Agency: ", ""),marker).strip(); continue;
	if(t.startswith("Gen: ")):
		gen = splitMarker(t.replace("Gen: ", ""),marker).strip(); continue;
	if(t.startswith("Name: ")):
		prestring = company + " > " + agency + " > " + gen + " > "
		name = prestring + splitMarker(t.replace("Name: ", ""),marker).strip(); continue;
	if(t.startswith("ID: ")):
		names.append(name)

# sorting list
active = names
itemlist = []; dex = []
previtem = ""
for k in range(1, 4):
	cut=k
	for i in range(len(active)):
		fullnow = active[i]
		itemnow = fullnow.rsplit(" > ",cut)[0]
		if(itemnow != previtem):
			if(itemnow in itemlist):
				pos = itemlist.index(itemnow)
				dindex = dex[pos+1]
				for e in range(pos+1, len(dex)):
					dex[e] = dex[e]+1
				active.pop(i); 
				active.insert(dindex, fullnow)
			else:
				previtem = itemnow
				itemlist.append(itemnow)
				dex.append(i)

# assembling printfile
name=""; agency=""; company=""; gen=""
prevagency=""; prevcompany=""; prevgen=""
printstring=""
for en, n in enumerate(names):
	company, agency, gen, name = n.split(" > ")
	blockstring = ""
	if(prevcompany != company):
		prevcompany = company
		blockstring = blockstring+"\n"+company
	if(prevagency != agency):
		prevagency = agency
		blockstring = blockstring+"\n"+"\t"+agency
	if(prevgen != gen):
		prevgen = gen
		blockstring = blockstring+"\n"+"\t\t"+gen
		
	blockstring = blockstring+"\n"+"\t\t\t"+name
	printstring = printstring + blockstring
	
printstring = printstring.strip()
finalfile = open(finalpath, "w")
finalfile.write(printstring)
finalfile.close()
print(lname + " updated")
	
	
	
	
	
	
