##read from configuration file
inputarg = dict()
configfile = open('apconfig','r') 
lines = configfile.readlines()
for line in lines:
	line=str(line).strip()
	split_list = line.split(":")
	inputarg[str(split_list[0])]=str(split_list[1])

print inputarg.keys()

##read from file
transactions = []
items = set()
myfile=open(inputarg["inputfile"],'r')
lines = myfile.readlines()
for line in lines:
	split_list = line.split(inputarg["separator"])
	l1=[]
	for i in range(1,len(split_list)-1):	#split_list[0] is username and split_list[len(split_list)-1] is '\n'
		l1.append(split_list[i])	
	transactions.append(list(l1))		#list of lists

##Storing distinct collection_ids in set items
for i in range(len(transactions)):
	for j in range(len(transactions[i])):
		if transactions[i][j] in items:
			continue
		else:
			items.add(transactions[i][j])
	

t = len(transactions)
n = len(items)		
print "Distinct items = ",n
for s in items:
	print s
items=list(items)
combine = {}
l1 = []
list_is = []
list_is2 = []	
itemsets = []
list_is.append('-1')
list_is2.append(list(list_is))
itemsets.append(list(list_is2))	##itemset[0]=-1 as 0-itemset is not possible
support = []
support.append(list(list_is))

thresh_supp = float(inputarg["thresh_support"])
thresh_conf = float(inputarg["thresh_confidence"])	

##printing transactions
print "The transactions are:"
for trans in transactions:
	print trans

del list_is[:]
del list_is2[:]

##computing 1-itemset
for item in items:
	list_is.append(item)
	c=0
	for i in transactions:
		for j in i:
			if j == item:	
				c+=1
	l1.append(str(c))
	list_is2.append(list(list_is))	## or list_is2.insert(-1,list_is)
	del list_is[:]	
	
itemsets.append(list(list_is2))
support.append(list(l1))

del list_is2[:]
del l1[:]

##computing k-itemset
i=2
while itemsets[i-1]:		##while previous list is not empty
	for j in range(0,len(itemsets[i-1])-1):
		for k in range(j+1,len(itemsets[i-1])):
			##if both (i-1)-itemsets have exactly i-1 items common, then they can be combined to give i-itemset
			if len(set(itemsets[i-1][j]).intersection(set(itemsets[i-1][k]))) == i-2:
				combine = set(itemsets[i-1][j]).union(set(itemsets[i-1][k]))
				c=0
				flag = 1
				##match every set in list_is2 with set combine
				for x in list_is2:
					if set(x).difference(combine):	##atleast 1 element different
						continue
					else:
						flag = 0
						break

				##if the set combine is not already present in the itemset
				if flag == 1:		
					for trans in transactions:
						if len(combine.intersection(set(trans))) == i:	
							##itemset is a subset of the transaction
							c+=1
					if c >= thresh_supp:
						l1.append(c) 
						list_is2.append(list(combine))
	itemsets.append(list(list_is2))
	support.append(list(l1))
	del list_is2[:]	
	del l1[:]			
	i+=1

itemsets.pop()		##removing last empty item
support.pop()
count_itemset = i-2

##printing itemsets and support
print "\nThe itemsets are:"
for i in range(1,count_itemset+1):
	print i,"\b-Itemset\t\tSupport"
	for j in range(0,len(itemsets[i])):
		print itemsets[i][j],"\t\t\t",support[i][j]


##Association rule mining
combine = set()
asso_rules = []	
confidence = []	
rule = []
l2 = []
print('\nAssociation rules\tConfidence')
for i in range(0,len(itemsets[count_itemset])):
	supp_set = support[count_itemset][i]
	supp_item = 0
	for item in range(0,len(itemsets[count_itemset][i])):
		for it in range(len(items)):
			if items[it]==itemsets[count_itemset][i][item]:
				supp_item=int(support[1][it])
				ele=items[it]
				break
		l1.append(list(itemsets[count_itemset][i]))
		#num = int(itemsets[count_itemset][i][item])
		#supp_item = support[1][num-1]
		conf = float(float(supp_set)/supp_item)
		if conf >= thresh_conf:
			confidence.append(conf)
			l2.append(itemsets[count_itemset][i][item])
			combine = set(l1[0]).difference(set(l2))	
			##all elements of the set except item
			rule.append(ele)
			rule.append(list(combine))
			asso_rules.append(list(rule))
			del rule[:]
			del l2[:]
		del l1[:]

for index, rule in enumerate(asso_rules):
	print rule,"\t\t",confidence[index]



