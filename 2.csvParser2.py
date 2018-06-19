# Program for parsing parsed log files into the required format for providing input to apriori algorithm.

import csv
import os

usersummary = dict()	
with open('parse1.csv','r') as csv_file:
	csv_reader = csv.DictReader(csv_file,delimiter=",")
	for row in csv_reader:
		if  row['event']=="view_collection":
	
			if row['user']=="anonymous":
				user = row['ip_address']
			else:
				user = row['user']

			if user in usersummary:
			#dictionary => key is string and value is set. Set is taken to avoid duplicates else take list.
				s=usersummary[user]
				s.add(row['event_id'])
			else :
				a=set()
				a.add(row['event_id'])
				usersummary[user]=a
				#usersummary[user]=set(row['event_id']) --> wrong: breaks up row['event_id'] into characters

print "Dictionary"
for key,value in usersummary.items():
	print "\n",key,value
	

with open('parse2.csv', 'wb') as csv_file:
	for key,value in usersummary.items():
		csv_file.write(key+",")
		for i in list(value):
			csv_file.write(i+",")
		csv_file.write("\n")			

print("CSV file has been parsed sucessfully !!!!***");

