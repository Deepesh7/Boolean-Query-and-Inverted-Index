import sys


class Node:
	def __init__(self, data):
		self.data = data
		self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    # def printList(self):
    #     temp = self.head
    #     while (temp):
    #         print(temp.data)
    #         temp = temp.next


def printList(llist):
    temp = llist.head
    while(temp):
        print(temp.data,end="->")
        temp = temp.next
    print()


def containsElem(llist,doc_id):
	var = llist.head
	while(var):
		if(var.data == doc_id):
			return True
		else:
			# print(var.data)
			var = var.next
	return False


def getPostingList(tokens):
    dictionary = {}
    for doc_id in tokens:
        for term in tokens[doc_id]:
            # print(term+": ")
            # dictionary[term] = LinkedList()
            # posting = Node(doc_id)
            # dictionary[term].head = posting
            # printList(dictionary[term])

            if(term in dictionary):
                if(containsElem(dictionary[term],doc_id)):
                    print("Duplicate: "+str(doc_id))
                    print("Term: "+str(term))
                    print()
                else:
                    print("Adding to "+term)
                    llist = dictionary[term]
                    lnode = llist.head
                    print(lnode.data)
                    while(lnode.next != None):
                        print(lnode.data)
                        lnode = lnode.next
                    print("Doc_id: "+str(doc_id))
                    lnode.next = Node(doc_id)
                    lnode = lnode.next
                    print(lnode.data)
                    print()
                    printList(llist)
                    print()
            else:
                print(term+": ")
                dictionary[term] = LinkedList()
                posting_elem = Node(doc_id)
                dictionary[term].head = posting_elem
                printList(dictionary[term])
                print()
            #print(dictionary)
    print('\n\n\n\n')
    for i in sorted(dictionary.keys(), key = str.lower):
        print (i,end = ': ')
        printList(dictionary[i])
    return dictionary

def findMaxlen(list_of_llist):
    max = 0
    for llist in list_of_llist:
        ctr = 0
        while(llist != None):
            ctr += 1
            llist = llist.next
        if(ctr > max):
            max = ctr
    return max

def findLen(llist):
	len = 0
	while(llist != None):
		len+=1
		llist = llist.next

	return len

def DAAT_OR(postings, terms, output_file):
	or_list=[]
	list_of_llist=[]
	for term in terms:
		list_of_llist.append(postings[term].head)
	print()
	smallest_node = list_of_llist[0]
	smallest_ctr = 0
	match = []
	cmp = 0
	exit_cond = False
	sum_of_len = 0
	over_list = []
	similar_list = []
	for llist in list_of_llist:
		# print(i.data)
		sum_of_len += findLen(llist)
		over_list.append(0)
		similar_list.append(0)
	print(sum_of_len)
	i=0
	while(i < sum_of_len):
		for x2 in range(len(list_of_llist)):
			similar_list[x2] = 0
		#print(over_list)
		if not (0 in over_list):
			print(over_list)
			break
		if(smallest_node == None):
			for ctr1 in range(len(list_of_llist)):
				if(list_of_llist[ctr1]):
					smallest_node = list_of_llist[ctr1]
					over_list[smallest_ctr] = 1
					smallest_ctr = ctr1
					print(over_list)
					break
		for ctr in range(len(list_of_llist)):
			if(ctr == smallest_ctr):
				continue
			elif(over_list[ctr] == 1):
				continue
			if(smallest_node.data == list_of_llist[ctr].data):
				similar_list[ctr] = 1
				pass
			elif(smallest_node.data > list_of_llist[ctr].data):
				smallest_node = list_of_llist[ctr]
				smallest_ctr = ctr
				for x in range(len(list_of_llist)):
					similar_list[x] = 0
			cmp+=1
		or_list.append(smallest_node.data)
		for x1 in range(len(list_of_llist)):
			if(similar_list[x1] == 1):
				list_of_llist[x1] = list_of_llist[x1].next
				if(list_of_llist[x1] == None):
					over_list[x1] = 1
		smallest_node = smallest_node.next
		if(smallest_node == None):
			over_list[smallest_ctr] = 1
		list_of_llist[smallest_ctr] = list_of_llist[smallest_ctr].next
		i+=1
	output_file.write("Results: ")
	for terms in or_list:
		output_file.write(str(terms)+" ")
	if(len(or_list) == 0):
		output_file.write("empty ")
	output_file.write("\nNumber of documents in results: "+str(len(or_list)))
	output_file.write("\nNumber of comparisons: "+str(cmp)+"\n")
	print("\n\n")
	print(or_list)
	print(cmp)





def DAAT_AND(postings, terms, output_file):
	and_list = []
	list_of_llist=[]
	for term in terms:
		list_of_llist.append(postings[term].head)
	print()
	smallest_node = list_of_llist[0]
	smallest_ctr = 0
	match = []
	cmp = 0
	exit_cond = False
	while(not exit_cond):
		count = 1
		if(smallest_node == None or exit_cond):
			break
		for ctr in range(len(list_of_llist)):
			if(ctr == smallest_ctr):
				continue
			if(smallest_node.data == list_of_llist[ctr].data):
				count+=1
			elif(smallest_node.data > list_of_llist[ctr].data):
				smallest_node = list_of_llist[ctr]
				smallest_ctr = ctr
			cmp+=1
		if(count == len(list_of_llist)):
			match.append(smallest_node.data)
			smallest_node = smallest_node.next
			i=0
			while(i<len(list_of_llist)):
				list_of_llist[i] = list_of_llist[i].next
				if(list_of_llist[i] == None):
					exit_cond = True
				i+=1
		else:
			smallest_node = smallest_node.next
			list_of_llist[smallest_ctr] = list_of_llist[smallest_ctr].next
		if(exit_cond):
			break
	output_file.write("Results: ")
	for terms in match:
		output_file.write(str(terms)+" ")
	if(len(match) == 0):
		output_file.write("empty")
	output_file.write("\n")
	output_file.write("Number of documents in results: "+str(len(match)))
	output_file.write("\nNumber of comparisons: "+str(cmp)+"\n")
	print(match)
	print("Comparisons: "+str(cmp))


def getPostingTerm(indexes,term,output_file):
	llist = indexes[term].head
	while(llist):
		output_file.write(str(llist.data)+" ")
		llist = llist.next
	output_file.write("\n")




input_filename = sys.argv[1]
result_file = sys.argv[2]
queries = sys.argv[3]
tokens=[]
docs =[]
dict_postings = {}

output_file = open(result_file,"w+")

with open(input_filename) as f:
    for lines in f.readlines():
        terms = lines.split()
        docs.append(terms[0])
        tokens.append(terms[1:])
        dict_postings[int(terms[0])] = terms[1:]


print(dict_postings)
dict_postings_sorted = {}
print()
for i in sorted(dict_postings.keys()):
	dict_postings_sorted[i] = dict_postings[i]

print(dict_postings_sorted)

indexes = getPostingList(dict_postings_sorted)

with open(queries) as queries_file:
	for lines in queries_file.readlines():
		query_terms = lines.split()
		for t in query_terms:
			output_file.write("GetPostings\n")
			output_file.write(t+"\n")
			output_file.write("Posting list: ")
			getPostingTerm(indexes,t,output_file)
		output_file.write("DaatAnd\n")
		for t in query_terms:
			output_file.write(t+" ")
		output_file.write("\n")
		DAAT_AND(indexes,query_terms,output_file)
		output_file.write("DaatOr\n")
		for t in query_terms:
			output_file.write(t+" ")
		output_file.write("\n")
		DAAT_OR(indexes,query_terms,output_file)
		output_file.write("\n")
