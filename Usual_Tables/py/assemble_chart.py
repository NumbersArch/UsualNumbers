#!/usr/bin/env python
#example: python3 process.py "2024-5"
import sys
import os
import statistics as stats
import pandas as pd
from os import listdir
from os.path import isfile, join

pname = "processed"
dname = join("charts", "tables")
cname = "chart.txt"
vname = "Vtubers.txt"
esc = "#"
marker = ") "

datestring=str(sys.argv[1])
workingdirectory = os.path.dirname(os.path.realpath(__file__))
up1directory = os.path.dirname(workingdirectory)
filedirectory = join(up1directory,pname,datestring)
finisheddirectory = join(up1directory,dname)
textpath = join(up1directory,vname)
chartpath = join(up1directory, cname)

if not os.path.exists(finisheddirectory):
    os.makedirs(finisheddirectory)
if not os.path.exists(filedirectory):
    os.makedirs(filedirectory)

# interpreting the input file
def interpretText(path):
	with open(path, 'r') as reader:
		text=reader.readlines()
	names = []; ids = []; sexes = [];
	name=""; agency=""; sx=""; gen=""; company=""
	for t in text:
		if(t.startswith("Company: ")):
			company = splitMarker(t.replace("Company: ", ""),marker).strip(); continue;
		if(t.startswith("Agency: ")):
			agency = splitMarker(t.replace("Agency: ", ""),marker).strip(); continue;
		if(t.startswith("Sex: ")):
			sx = splitMarker(t.replace("Sex: ", ""),marker).strip(); continue;
		if(t.startswith("Gen: ")):
			gen = splitMarker(t.replace("Gen: ", ""),marker).strip(); continue;
		if(t.startswith("Name: ")):
			name = splitMarker(t.replace("Name: ", ""),marker).strip(); continue;
		if(t.startswith("ID: ")):
			idname = t.replace("ID: ","").strip();
			rs = company +" > " +agency +" > " +gen +" > " +name
			sexes.append(sx)
			names.append(rs)
			ids.append(idname)
	return names, sexes, ids
	
# interpreting text from data file
# ldarr = includes all time, darr skips nodata entires
def interpretData(path):
	ifile = open(path, 'r')
	text=ifile.read()
	ifile.close()
	blocks = text.split("\n\n")
	ldarr = []; darr = []; marr = []; parr = []; 
	lduration = 0; duration = 0; mean = 0; peak = 0 
	for b in blocks:
		if "" == b.strip():
			continue
		nixed=False
		ba = b.split("\n")
		for t in ba:
			if(t.startswith("Duration: ")):
				duration = int(t.replace("Duration: ", "").strip()); continue
			if(t.startswith("Mean: ")):
				if("\\" in t): t="0"; nixed=True;
				mean = int(t.replace("Mean: ", "").strip()); continue;
			if(t.startswith("Peak: ")):
				if("\\" in t): t="0"; nixed=True;
				peak = int(t.replace("Peak: ", "").strip()); continue;
		if(nixed == False):
			lduration = duration
			darr.append(duration); marr.append(mean); parr.append(peak)
		ldarr.append(duration); 
	return ldarr, darr, marr, parr  
# determines what items are allowed by the list
def interpretList(path, esc):
	ifile = open(path, 'r')
	text=ifile.read()
	ifile.close()
	cleantext = text.replace(esc,'')
	textarr = text.split("\n")
	cleanarr = cleantext.split("\n")
	
	company = ""; agency = ""; gen = ""; name = "";
	companies = []; agencies = []; gens = []; names = [];
	bool1=True; bool2=True; bool3=True;
	for en, ct in enumerate(cleanarr):
		t = textarr[en]
		if(ct.strip() == ""):
			continue
		if(ct.startswith("\t\t\t")):
			if(bool1 == True):
				name = t.strip()
				if(name.startswith(esc) == False):
					rs = company +" > " +agency +" > " +gen +" > " +name
					names.append(rs)
			continue
		elif(ct.startswith("\t\t")):
			if(bool2 == True):
				gen = t.strip()
				if(gen.startswith(esc)):
					bool1 = False
				else:
					bool1 = True
			continue
		elif(ct.startswith("\t")):
			if(bool3 == True):
				agency = t.strip()
				if(agency.startswith(esc)):
					bool1 = False
					bool2 = False
				else:
					bool2 = True
			continue
		else:
			company = t.strip()
			if(company.startswith(esc)):
				bool1 = False
				bool2 = False
				bool3 = False
				continue	
			else:
				bool3 = True	
	return names

# splits string for designated marker if exists.
def splitMarker(instring, marker):
	if marker in instring:
		return instring.split(marker,1)[1]
	return instring

# getting all processed files in folder
fnames = []; paths = [];
for d in listdir(filedirectory):
	fcomp = join(filedirectory,d)
	for agn in listdir(fcomp):
		fagn = join(fcomp, agn)
		for gn in listdir(fagn):
			fgen = join(fagn, gn)
			for f in listdir(fgen):
				paths.append(join(fgen,f))
				d_i = splitMarker(d, marker)
				agn_i = splitMarker(agn,marker)
				gn_i = splitMarker(gn,marker)
				f_i = splitMarker(f.split(".")[0], marker)
				rs = d_i +" > " +agn_i +" > " +gn_i +" > " +f_i
				fnames.append(rs)
		
# directories = [f for f in listdir(filedirectory) if isdir(join(filedirectory, f))]	
# paths = [filedirectory+"/"+f for f in files]

names, sexes, ids = interpretText(textpath)
cnames = interpretList(chartpath,esc)


df1 = pd.DataFrame()
df2 = pd.DataFrame()
df3 = pd.DataFrame()
for en, p in enumerate(paths):
	company, agency, gen, name = fnames[en].split(" > ")
	checkstring = company +" > " +agency +" > " +gen +" > " +name
	cid = ids[en]; sx = sexes[en]
	
	if checkstring in cnames and checkstring in names:
		ltimes, times, means, peaks = interpretData(p)
		number = len(ltimes)
		members = len(ltimes) - len(times)
		if(len(peaks)>0): 
			medianpeak =round(stats.median(peaks)); 
			meanpeak =round(stats.mean(peaks))
		else: medianpeak =0; meanpeak =0;

		row1 = pd.DataFrame([{		 \
		"channel id": cid 		, \
		"channel" : name 		, \
		"Num Streams" : number 	, \
		"Median Peak" : medianpeak 	, \
		"Mean Peak" : meanpeak 	, \
		"Company" : company 		, \
		"Branch" : agency 		, \
		"Generation" : gen 		, \
		"Sex" : sx 			 \
		}])
		df1 = pd.concat([df1, row1], ignore_index=True)
		
		if(len(times)>0): 
			minutes = sum(times)
			minuteswatched = round(sum([times[i] * means[i] for i in range(len(times))]))
			hourswatched = minuteswatched/60
		else: minutes = 0
		if(len(ltimes)>0): lminutes = sum(ltimes)
		else: lminutes = 0
		lhours = round(lminutes/60)
		if(lminutes >0): average = round(minuteswatched/minutes)
		else: average=0
		
		row2 = pd.DataFrame([{		 \
		"channel id": cid 		, \
		"channel" : name 		, \
		"Num Streams" : number 	, \
		"Average" : average 		, \
		"Hours Streamed" : lhours 	, \
		"Hours Watched" : hourswatched , \
		"Company" : company 		, \
		"Branch" : agency 		, \
		"Generation" : gen 		, \
		"Sex" : sx 			 \
		}])
		df2 = pd.concat([df2, row2], ignore_index=True)
		
		row3 = pd.DataFrame([{		 \
		"Company" : company 		, \
		"Branch" : agency 		, \
		"Generation" : gen 		, \
		"Sex" : sx 			, \
		"channel id": cid 		, \
		"channel" : name 		, \
		"Num Streams" : number 	, \
		"Mem Streams" : members 	, \
		"Hours Streamed" : lhours 	, \
		"Average" : average 		, \
		"Median Peak" : medianpeak 	, \
		"Mean Peak" : meanpeak 	, \
		"Hours Watched" : hourswatched  \
		}])
		df3 = pd.concat([df3, row3], ignore_index=True)
#finisheddirectory	

df1 = df1.sort_values(by = 'Median Peak', ascending=False)
df1 = df1.reset_index()
df1 = df1.rename(columns={"index" : "ranking"})
df1["ranking"] = range(1,len(df1.index)+1)
headerframe = pd.DataFrame(columns = df1.columns.values, index=range(1))
headerframe.iloc[0] = df1.columns.values
df1 = pd.concat([headerframe,df1]); 

df2 = df2.sort_values(by = 'Average', ascending=False)
df2 = df2.reset_index()
df2 = df2.rename(columns={"index" : "ranking"})
df2["ranking"] = range(1,len(df2.index)+1)
headerframe = pd.DataFrame(columns = df2.columns.values, index=range(1))
headerframe.iloc[0] = df2.columns.values
df2 = pd.concat([headerframe,df2]); 

df1["c"] = ""
dfc = pd.concat([df1, df2], axis=1, join="outer", ignore_index=True)
dfcname = datestring+"_separated"+".csv"
dfcpath = join(finisheddirectory, dfcname)
dfc.to_csv(dfcpath, index=False, header=False)  
print("\""+dfcname + "\""+" exported to "+ "\""+dname + "\""+" directory")


df3 = df3.sort_values(by = 'Average', ascending=False)
df3 = df3.reset_index()
df3 = df3.rename(columns={"index" : "ranking"})
df3["ranking"] = range(1,len(df3.index)+1)
df3name = datestring+"_combined"+".csv"
df3path = join(finisheddirectory, df3name)
df3.to_csv(df3path, index=False)  

print("\""+df3name + "\""+ " exported to "+ "\""+dname + "\""+" directory")
print("Done")
sys.exit(0)










