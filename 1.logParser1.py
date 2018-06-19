# Program for parsing Dspace Log files

import csv
import os
import datetime

PATH = "/home/muskan/Downloads/dspacelogs"  			#mention the absolute path of log folder
myfile = open("parse1.csv", "w+") 		#opening csv file
os.chmod("parse1.csv", 0777)			#Change permissions of csv
fieldnames = ['user','ip_address','event','event_id']
wr = csv.DictWriter(myfile,fieldnames=fieldnames,quoting=csv.QUOTE_ALL)	#get csv writer object
wr.writeheader()



######## Run for the first time only
for file in os.listdir(PATH): 
	f = open(PATH+"/"+file,"r")
	lines = f.readlines()
	for line in lines:
		split_list = line.split(":")
		if(len(split_list)>5 and (split_list[5].startswith("view_collection"))):
				# To filter out unnecessary logged events...
			user = split_list[2][split_list[2].find("@")+2:]
			#session_id = split_list[3][split_list[3].find("=")+1:]	
			ip_address = split_list[4][split_list[4].find("=")+1:]
			event_id = split_list[6][split_list[6].find("=")+1:].rstrip() # rstrip used to trim \n
			wr.writerow({'user':user,'ip_address':ip_address,'event':split_list[5],'event_id':event_id})
	f.close()
########

now = str(datetime.datetime.now()).split();

fName = PATH+"/dspace.log."+now[0];
if os.path.exists(fName):
	f = open(fName,"r") 
	lines = f.readlines()
	for line in lines:
		split_list = line.split(":")
		if(len(split_list)>5 and (  split_list[5].startswith("view_collection"))):          # split_list[5].startswith("se") or
				# To filter out unnecessary logged events...
			user = split_list[2][split_list[2].find("@")+2:]
			#session_id = split_list[3][split_list[3].find("=")+1:]	
			ip_address = split_list[4][split_list[4].find("=")+1:]
			event_id = split_list[6][split_list[6].find("=")+1:].rstrip()        # rstrip used to trim \n
			wr.writerow({'user':user,'ip_address':ip_address,'event':split_list[5],'event_id':event_id})
							# split_list[5] = event
	f.close()
	print("log files have been parsed sucessfully !!!!***");


os.system('(head -n 1 parse1.csv  && tail -n +2 parse1.csv | sort | uniq) > parse1uniq.csv')
#to save only unique lines in the csv file in the sorted order without altering the header row 
