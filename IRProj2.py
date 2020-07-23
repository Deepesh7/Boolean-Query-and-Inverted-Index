import sys


class Node:
	def __init__(self, data):
		self.data = data
		self.next = None
		self.term_freq = 0
		self.tf = 0
		self.idf = 0
		self.tf_idf = 0


class LinkedList:
    def __init__(self):
        self.tail = self.head = None



def writeList(llist,postings_file):
	temp = llist.head
	while(temp):
		postings_file.write(str(temp.data) + "->")
		temp = temp.next
	postings_file.write("\n")


def containsElem(llist,doc_id):
	var = llist.head
	while(var):
		if(var.data == doc_id):
			return var
		else:
			var = var.next
	return False

def update_tf(dict, len_docs):
	for term in dict:
		llist = dict[term].head
		while(llist):
			len_ = len_docs[llist.data]
			llist.tf = llist.term_freq / len_
			llist = llist.next

def update_tfidf(dict , total_no_of_docs):
	for term in dict:
		len_ = findLen(dict[term].head)
		idf = total_no_of_docs/len_
		llist = dict[term].head
		while(llist):
			llist.idf = idf
			llist.tf_idf = llist.tf*idf
			llist = llist.next

def getPostingList(tokens):
	dictionary = {}
	for doc_id in tokens:
		len_ = len(tokens[doc_id])
		for term in tokens[doc_id]:
			if(term in dictionary):
				contains_e = containsElem(dictionary[term],doc_id)
				if(contains_e):
					contains_e.term_freq+=1
				else:
					llist = dictionary[term]
					lnode = llist.tail
					posting_elem = Node(doc_id)
					posting_elem.term_freq+=1
					lnode.next = posting_elem
					llist.tail = lnode.next
			else:
				dictionary[term] = LinkedList()
				posting_elem = Node(doc_id)
				posting_elem.term_freq+=1
				dictionary[term].tail = dictionary[term].head = posting_elem
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
	or_list_tfidf = {}
	list_of_llist=[]
	for term in terms:
		list_of_llist.append(postings[term].head)
	smallest_node = list_of_llist[0]
	smallest_ctr = 0
	match = []
	cmp = 0
	exit_cond = False
	sum_of_len = 0
	over_list = []
	similar_list = []
	for llist in list_of_llist:
		sum_of_len += findLen(llist)
		over_list.append(0)
		similar_list.append(0)
	i=0
	while(i < sum_of_len):
		for x2 in range(len(list_of_llist)):
			similar_list[x2] = 0
		if not (0 in over_list):
			break
		if(smallest_node == None):
			for ctr1 in range(len(list_of_llist)):
				if(list_of_llist[ctr1]):
					smallest_node = list_of_llist[ctr1]
					over_list[smallest_ctr] = 1
					smallest_ctr = ctr1
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
		or_list_tfidf[smallest_node.data] = smallest_node.tf_idf
		for x1 in range(len(list_of_llist)):
			if(similar_list[x1] == 1):
				or_list_tfidf[smallest_node.data] += list_of_llist[x1].tf_idf
				list_of_llist[x1] = list_of_llist[x1].next
				if(list_of_llist[x1] == None):
					over_list[x1] = 1
		smallest_node = smallest_node.next
		if(smallest_node == None):
			over_list[smallest_ctr] = 1
		list_of_llist[smallest_ctr] = list_of_llist[smallest_ctr].next
		i+=1
	output_file.write("Results:")
	for terms in or_list:
		output_file.write(" "+str(terms))
	if(len(or_list) == 0):
		output_file.write(" empty")
	output_file.write("\nNumber of documents in results: "+str(len(or_list)))
	output_file.write("\nNumber of comparisons: "+str(cmp)+"\n")
	return or_list_tfidf

def DAAT_AND(postings, terms, output_file):
	and_list = []
	and_list_tfidf = {}
	list_of_llist = []
	nodes_with_val_same_as_large = []
	for term in terms:
		list_of_llist.append(postings[term].head)
		nodes_with_val_same_as_large.append(0)
	len_of_llist = len(list_of_llist)
	largest_node = list_of_llist[0]
	largest_ctr = 0

	cmp = 0
	break_flag = False
	exit_cond = False
	while(not exit_cond):
		count = 1
		for len_ctr in range(len_of_llist):
			if(list_of_llist[len_ctr] == None):
				break_flag = True
				break
		if(break_flag):
			break

		for ctr in range(len(list_of_llist)):
			if(ctr == largest_ctr):
				continue
			if(largest_node.data == list_of_llist[ctr].data):
				count+=1
				nodes_with_val_same_as_large[ctr] = 1
			elif(largest_node.data < list_of_llist[ctr].data):

				for f in range(len(nodes_with_val_same_as_large)):
					nodes_with_val_same_as_large[f] = 0
				largest_node = list_of_llist[ctr]
				largest_ctr = ctr
			cmp+=1
		if(count == len(list_of_llist)):
			and_list.append(largest_node.data)
			tfidf = 0
			for llist in list_of_llist:
				tfidf+=llist.tf_idf
			and_list_tfidf[largest_node.data] = tfidf
			largest_node = largest_node.next
			i=0
			while(i<len(list_of_llist)):
				list_of_llist[i] = list_of_llist[i].next
				if(list_of_llist[i] == None):
					exit_cond = True
				i+=1
		else:
			u=0
			while(u<len_of_llist):
				if(u == largest_ctr):
					u+=1
					continue
				if(nodes_with_val_same_as_large[u] == 1):
					u+=1
					continue
				else:
					list_of_llist[u] = list_of_llist[u].next
				u+=1
		for f1 in range(len(nodes_with_val_same_as_large)):
			nodes_with_val_same_as_large[f1] = 0
		if(exit_cond):
			break
	output_file.write("Results:")
	for terms in and_list:
		output_file.write(" "+str(terms))
	if(len(and_list) == 0):
		output_file.write(" empty")
	output_file.write("\n")
	output_file.write("Number of documents in results: "+str(len(and_list)))
	output_file.write("\nNumber of comparisons: "+str(cmp)+"\n")
	return and_list_tfidf


def getPostingTerm(indexes,term,output_file):
	llist = indexes[term].head
	l1 = []
	while(llist):
		l1.append(int(llist.data))
		llist = llist.next
	for i in sorted(l1):
		output_file.write(" "+str(i))
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


dict_postings_sorted = {}
for i in sorted(dict_postings.keys()):
	dict_postings_sorted[i] = dict_postings[i]


total_no_of_docs = len(dict_postings_sorted)
len_docs={}
for i in dict_postings_sorted:
	len_docs[i] = len(dict_postings_sorted[i])

indexes = getPostingList(dict_postings_sorted)
indexes_sort = {}
update_tf(indexes,len_docs)
update_tfidf(indexes,total_no_of_docs)

postings_file = open('postings.txt','w+')

for i in sorted(indexes.keys(), key = str.lower):
	postings_file.write(i+': ')
	writeList(indexes[i],postings_file)

postings_file.close()

for i in sorted(indexes.keys(), key = str.lower):
	indexes_sort[i] = indexes[i]


with open(queries) as queries_file:
	for lines in queries_file.readlines():
		query_terms = lines.split()
		for t in query_terms:
			output_file.write("GetPostings\n")
			output_file.write(t+"\n")
			output_file.write("Postings list:")
			getPostingTerm(indexes,t,output_file)
		output_file.write("DaatAnd\n")
		for t in query_terms[:-1]:
			output_file.write(t+" ")
		output_file.write(query_terms[-1])
		output_file.write("\n")
		and_list_tfidf = DAAT_AND(indexes,query_terms,output_file)
		output_file.write("TF-IDF\n")
		output_file.write("Results:")
		if(not and_list_tfidf):
			output_file.write(" empty")
		for node in sorted(and_list_tfidf.items(), key=lambda x: x[1], reverse = True):
			#print(node)
			output_file.write(" "+str(node[0]))
		output_file.write("\n")
		output_file.write("DaatOr\n")
		for t in query_terms[:-1]:
			output_file.write(t+" ")
		output_file.write(query_terms[-1])
		output_file.write("\n")
		or_list_tfidf = DAAT_OR(indexes,query_terms,output_file)
		output_file.write("TF-IDF\n")
		output_file.write("Results:")
		if(not or_list_tfidf):
			output_file.write(" empty")
		for node in sorted(or_list_tfidf.items(), key=lambda x: x[1], reverse = True):
			output_file.write(" "+str(node[0]))
		output_file.write("\n\n")
	output_file.truncate(output_file.tell()-1)
