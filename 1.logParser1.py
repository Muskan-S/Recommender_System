# Program for parsing Dspace Log files

import csv
import os

PATH = "/home/muskan/Downloads/dspacelogs"  			#mention the absolute path of log folder
myfile = open("parse.csv", "w+") 		#opening csv file
os.chmod("parse.csv", 0777)		#Change permissions of csv
fieldnames = ['user','ip_address','event','event_id']
wr = csv.DictWriter(myfile,fieldnames=fieldnames,quoting=csv.QUOTE_ALL)	#get csv writer object
wr.writeheader()

i = 1         # to know total log files

for file in os.listdir(PATH): 
	f = open(PATH+"/"+file,"r")
	i = i + 1;
	lines = f.readlines()
	for line in lines:
		split_list = line.split(":")
		if(len(split_list)>5 and (split_list[5].startswith("se") or split_list[5].startswith("vi"))):
				# To filter out unnecessary logged events...
			user = split_list[2][split_list[2].find("@")+2:]
			#session_id = split_list[3][split_list[3].find("=")+1:]	
			ip_address = split_list[4][split_list[4].find("=")+1:]
			event_id = split_list[6][split_list[6].find("=")+1:].rstrip() # rstrip used to trim \n
			wr.writerow({'user':user,'ip_address':ip_address,'event':split_list[5],'event_id':event_id})
	f.close()

print(i),
print("log files have been parsed sucessfully !!!!***");
