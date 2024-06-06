#!/usr/bin/env python
#example: python3 process.py "2024-5"
import sys
import os
import statistics as stats
import pandas as pd
from os import listdir
from os.path import isfile, join

cname = "timechart.txt"
pname = "processed"
dname = join("charts", "timeseries")
marker = ") "
esc = "#"

datestring1=str(sys.argv[1])
datestring2=str(sys.argv[2])
workingdirectory = os.path.dirname(os.path.realpath(__file__))
up1directory = os.path.dirname(workingdirectory)
filedirectory = join(up1directory,pname)
finisheddirectory = join(up1directory,dname)
textpath = join(up1directory,cname)

if not os.path.exists(finisheddirectory):
    os.makedirs(finisheddirectory)
if not os.path.exists(filedirectory):
    os.makedirs(filedirectory)
    
# adding "0" to single digit months so lists can be sorted properly
def zipNames(l):
	returnme=[]
	for i in l:
		y, m = i.split("-", 1)
		if(len(m) == 1):
			m="0"+m
		returnme.append(y+"-"+m)
	return returnme
# removing "0" from single digit months so directories can be referenced properly
def unzipNames(l):
	returnme=[]
	for i in l:
		y, m = i.split("-", 1)
		if(m.startswith("0")):
			m = m[1:]
		returnme.append(y+"-"+m)
	return returnme
# gets all .txt file paths within directory
def allFiles(path):
	rlist = []
	for cd in listdir(path):
		cpath=join(path,cd)
		for ad in listdir(cpath):
			apath=join(cpath,ad)
			for gn in listdir(apath):
				gpath=join(apath,gn)
				for t in listdir(gpath):
					tpath = join(gpath,t)
					rlist.append(tpath)
	return rlist	
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
# splits string for designated marker if exists.
def splitMarker(instring, marker):
	if marker in instring:
		return instring.split(marker,1)[1]
	return instring
# gets N'th basename of path
def baseN (p, N):
	N-=1
	l=p
	for i in range(N):
		l=os.path.dirname(l)
	return os.path.basename(l)
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
cnames = interpretList(textpath,esc)
		
# Getting directory names between input dates
y1, m1 = datestring1.split("-", 1)
if(len(m1) == 1):
	m1="0"+m1
zipstring1 = y1+"-"+m1
y2, m2 = datestring2.split("-", 1)
if(len(m2) == 1):
	m2="0"+m2
zipstring2 = y2+"-"+m2

zipnames = sorted(zipNames(listdir(filedirectory)))
returnable=[]
for z in zipnames:
	y, m = z.split("-",1)
	if(z > zipstring2):
		break
	if(zipstring1 <= z):
		returnable.append(y+"-"+m)
alldir = unzipNames(returnable)

dfnumber = pd.DataFrame(columns = alldir)
dfhours = pd.DataFrame(columns = alldir)
dfaverage = pd.DataFrame(columns = alldir)
dfmedianpeak = pd.DataFrame(columns = alldir)
dfhourswatched = pd.DataFrame(columns = alldir)
paths = []
for d in alldir:
	path=join(filedirectory,d)
	paths = allFiles(path)
	for p in paths:
		name = splitMarker(baseN(p,1).split(".")[0],marker)
		gen = splitMarker(baseN(p,2).split(".")[0],marker)
		agency = splitMarker(baseN(p,3).split(".")[0],marker)
		company = splitMarker(baseN(p,4).split(".")[0],marker)
		elementname = company+" > "+agency+" > "+gen+" > "+name
		
		if elementname in cnames:
			ltimes, times, means, peaks = interpretData(p)
			number = len(ltimes)
			members = len(ltimes) - len(times)
			if(len(peaks)>0): 
				medianpeak =round(stats.median(peaks)); 
				meanpeak =round(stats.mean(peaks))
			else: medianpeak =0; meanpeak =0;
			if(len(times)>0): 
				minutes = sum(times)
				minuteswatched = round(sum([times[i] * means[i] for i in range(len(times))]))
				hourswatched = round(minuteswatched/60)
			else: minutes = 0
			if(len(ltimes)>0): lminutes = sum(ltimes)
			else: lminutes = 0
			lhours = round(lminutes/60)
			if(lminutes >0): average = round(minuteswatched/minutes)
			else: average=0
			
			dfnumber.at[elementname,d] = number
			dfhours.at[elementname,d] = lhours
			dfaverage.at[elementname,d] = average
			dfmedianpeak.at[elementname,d] = medianpeak
			dfhourswatched.at[elementname,d] = hourswatched

#orders dataframe columns and sorts
def orderDF(df):
	df = df.reset_index()
	df = df.rename(columns={"index" : "Name"})
	df[["Company","Agency","Gen","Name"]] = df["Name"].str.split(' > ',expand=True)
	df = df.sort_values(by=["Company","Agency","Gen","Name"], ascending=True)
	df.set_index(["Company","Agency","Gen","Name"], inplace=True)
	df = df.reset_index()
	return df
dfnumber = orderDF(dfnumber)
dfhours = orderDF(dfhours)
dfaverage = orderDF(dfaverage)
dfmedianpeak = orderDF(dfmedianpeak)
dfhourswatched = orderDF(dfhourswatched)

#adds header row
def addHeader(df,name):
	headerframe = pd.DataFrame(columns = dfnumber.columns.values, index=range(3))
	headerframe.iloc[2] = df.columns.values
	headerframe.iat[1,0] = name
	df = pd.concat([headerframe,df]); 
	df=df.reset_index(drop=True)
	return df
start = 0

dfnumber = addHeader(dfnumber, "Number")
dfhours = addHeader(dfhours, "Hours")
dfaverage = addHeader(dfaverage, "Average")
dfmedianpeak = addHeader(dfmedianpeak, "Median Peak")
dfhourswatched = addHeader(dfhourswatched, "Hours Watched")

df = pd.concat([dfnumber, dfhours, dfaverage, dfmedianpeak, dfhourswatched])
df = df.iloc[1:]
df = df.reset_index(drop=True)

datestring="("+zipstring1+")-("+zipstring2+").csv"
dfpath = join(finisheddirectory, datestring)
df.to_csv(dfpath, index=False, header=False)  

print("\""+datestring + "\""+ " exported to "+ "\""+dname + "\""+" directory")







