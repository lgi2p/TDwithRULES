#!/usr/bin/python
import os

'''
	THIS DOCUMENTATION HAS TO BE CHECKED

	Considering
		(i) a given graph defining a partial order among values
		(ii) sources associated to values in specific contexts (e.g. claiming values for a specific dataitem)

	the script generates for each context (dataitem) the set of sources associated to a value considering inferences made possible by the specified value partial ordering.
	For instance, if the graph specifies
		c -> b -> a (i.e. b generalizes a that is to say b \prec a)

	and we know that
		source 0 claims c,
		source 1 and 2 claim b,
		no source claim a,

	we will generate the following result:

	http://dbpedia.org/resource/Stranraer	none	source603;source459;source597;source325;source121;source974;source858;source870;source
743;source919	none	source603;source459;source597;source325;source121;source974;source858;source870;source743;source919
http://dbpedia.org/ontology/Village	http://dbpedia.org/resource/Helen%C3%B3w,_Gmina_Be%C5%82chat%C3%B3w	none	none	source
763


	[1] URI of the value
	[2] URIs of the values on which this value depends (children)  - the dependencies among value confidences -  confidence of this values have to be sum
	[3] set of the source trustwordiness to add - trustwordiness of these sources have to be added
	[4] set of pairs sources/nb_times defining how much time the trustworthiness of a source has to be substracted
	-- see code for details


	if no source is associated to a value no entry will be generated


	Since several contexts can be processed an ID is generated for each of them.
	The index defining the id for each context is stored into a file:
	context_uri[\t]id
	The results will be stored into specified directory (see code) - those related to a specific context will be stored in the file named [id].csv

	[Optional] To reduce computation time the transitive reduction of the provided graph of values is also computed, it is  stored into a file.


	[INPUTS]

		GRAPH -
			The graph must be a directed acyclic graph (no test performed).

			Input graph of values in the form of adjency lists specifying the ancestors of each node
			format:
				URI_value_0[\t]URI_ancestor0;URI_ancestor1;...
				URI_value_1[\t]URI_ancestor34;URI_ancestor1;...

			URIs are expected to start by http://

			example:
				http://dbpedia.org/resource/Mostafa_Chay	http://dbpedia.org/resource/Iran;http://dbpedia.org/resource/Owch_Hacha_Rural_District...
				http://dbpedia.org/resource/Tr%C4%85bin-Rumunki	http://dbpedia.org/resource/Tr%C4%85bin-Rumunki;http://dbpedia.org/ontology/Village;http://dbpedia.org/ontology/Place


		CONTEXTS AND SOURCES/VALUES RELATIONSHIP -

			Contexts to process and sources associated to each value for each context are specified by a file of the form:

			factID	context_id	value	sourceID (header expected)
			0	http://dbpedia.org/resource/Norah_Al_Faiz	http://www.w3.org/2002/07/owl#Thing	source416
			1	http://dbpedia.org/resource/Norah_Al_Faiz	http://dbpedia.org/ontology/Country	source240
			2	http://dbpedia.org/resource/toto	http://dbpedia.org/resource/Irandegan_Rural_District	source87

			In this example two contexts (dataitems) are specified http://dbpedia.org/resource/Norah_Al_Faiz and http://dbpedia.org/resource/toto



'''


class Graph():
	''' Oriented Graph'''
	nodes = None  # set of nodes ids
	adjacents = None  # map< key: node id, value: set of adjacent node ids >

	def __init__(self):
		self.nodes = set()
		self.adjacents = dict()

	def addNode(self, node):
		if not node in self.nodes: self.nodes.add(node)

	def addNodes(self, nodes):
		for n in nodes: self.addNode(n)

	def addLink(self, source, target):
		if not source in self.adjacents: self.adjacents[source] = set()
		if not target in self.adjacents.get(source):self.adjacents.get(source).add(target)
		if not source in self.nodes: self.nodes.add(source)
		if not target in self.nodes: self.nodes.add(target)

	def __str__(self):
		out = "-----------------------------------------------------------------\n"
		out += "Graph: " + str(len(self.nodes)) + "\n"
		out += "-----------------------------------------------------------------\n"
		return out


'''
Flush the specified graph into a file respecting the following format
adjancency list, one entry per line, e.g.
node_id[\t]node_id_O;node_id_1;...

g: graph stored into adjacency lists using a dictionary key node value iterable collection of adjacent nodes
file_: file path
'''


def flushGraph(g, file_):
	f = open(file_, 'w')
	for k in g.nodes:
		s = ""
		if not k in g.adjacents:
			s = "none"
		else:
			for v in g.adjacents.get(k):
				if len(s) != 0:
					s += ";"
				s += v
		f.write(k + "\t" + s + '\n')  # python will convert \n to os.linesep
	f.close()


def loadGraphOfURIs(ancestors):
	# print ("Loading the graph from: ",file_)
	g = Graph()

	for item in ancestors:
		g.addNode(item)
		for other in ancestors[item]:
			g.addLink(item, other)
	#print(g)
	return g


def loadGraphOfURIs_from_file(file_, header):
	print ("Loading the graph from: ",file_)
	g = Graph()

	with open(file_, "r") as reader:

		for line in reader:

			if header:
				header = False
				continue

			line = line.strip()

			data = line.split("\t")
			uri_c = data[0]

			if len(data)!=2:
				print ("[warning] excluding line ", line)
				continue
			if(data[1] == "none"):
				g.addNode(uri_c)
				continue

			if ";http" in data[1]:
				ancestors = data[1].split(";http")

				for a in range(0,len(ancestors)):

					uri_a = ancestors[a]
					if(a != 0): uri_a = "http"+uri_a
					if uri_c!=uri_a:
						g.addLink(uri_c, uri_a)
			else:
				ancestors = data[1].split(";")

				for a in range(0, len(ancestors)):

					uri_a = ancestors[a]
					if (a != 0): uri_a = uri_a
					if uri_c != uri_a:
						g.addLink(uri_c, uri_a)

	print (g.__str__())
	return g


def load_graph(graph_file, graph_file_reduced, apply_transitive_reduction):
	print("loading graph")
	if apply_transitive_reduction:
		g = loadGraphOfURIs_from_file(graph_file, True)
		print("performing the transitive reduction (to avoid useless propagations)")
		g = perform_transitive_reduction(g)

		print("Flushing reduction into: ", graph_file_reduced)
		flushGraph(g, graph_file_reduced)

	else:
		g = loadGraphOfURIs_from_file(graph_file_reduced, False)
	return g


def compute_exclusive_descendants(g):
	d = {}
	for node in g.nodes:
		if node not in d:
			d[node] = 0

		#print("-_----" + str(node))
		if g.adjacents.get(node) == None:
			continue
		for a in g.adjacents.get(node):
			if (a == node): continue
			if not a in d:
				d[a] = 1
			else:
				d[a] += 1
			#print(a)
	return d


def reverse_transitive_reduction(g_red):
	g_rev = Graph()
	for n in g_red.nodes:
		if n not in g_rev.nodes:
			g_rev.addNode(n)
		if g_red.adjacents.get(n) == None:
			continue
		for adj_n in g_red.adjacents.get(n):
			if adj_n not in g_rev.nodes:
				g_rev.addNode(adj_n)
			if adj_n != n:
				g_rev.addLink(adj_n, n)


	return g_rev

def perform_transitive_reduction(g):
	nb_descendants = compute_exclusive_descendants(g)
	# detects the leaves
	leaves_ = set()
	for d in nb_descendants:
		if nb_descendants[d] == 0:
			leaves_.add(d)

	#print("Number of detected leaves", str(len(leaves_)))

	queue = list(leaves_)

	desc = {}
	rel_removed = 0

	j = 0

	g_reduced = Graph()
	g_reduced.addNodes(g.nodes)

	while queue:

		j += 1

		if j % 10000 == 0:
			print(str(j) + "/" + str(len(g.nodes)))

		c = queue.pop(0)

		if not c in desc: desc[c] = set()

		desc[c].add(c)

		if c not in g.adjacents:
			continue  # no ancestors for that value

		# propagation of the descendants of c to it's ancestors
		for a in g.adjacents.get(c):

			if a == c:
				continue  # we don't want to add c -> a and the number of descendants is already exclusive

			g_reduced.addLink(c, a)

			todel = set()
			if not a in desc: desc[a] = set()

			# propagation
			for d in desc[c]:

				if (d in desc[a]) or (d == a):  # the relationship can be removed
					todel.add(d)  # d -> a can be removed since we have d -> ... -> c -> a
				else:
					desc[a].add(d)

			# reduce the graph considering detected redundancies
			for d in todel:
				if a in g.adjacents.get(d):  # the error is maybe already corrected
					g.adjacents.get(d).remove(a)
					rel_removed += 1

			nb_descendants[a] -= 1

			# now we can propagate the descendants of this node
			# since we are sure all the descendants have been propagated
			if nb_descendants[a] == 0:
				queue.append(a)

	#print("Number of relations removed ", str(rel_removed))

	return g

def return_leaves(g):
	nb_descendants = compute_exclusive_descendants(g)
	# detects the leaves
	leaves_ = set()
	for d in nb_descendants:
		if nb_descendants[d] == 0:
			leaves_.add(d)

	#print("Number of detected leaves", str(len(leaves_)))

	return leaves_



def load_nb_descendants_d(g, value_sources):
	nb_descendants_d = {}

	queue_p = list(value_sources.keys())
	visited = set(queue_p)

	while queue_p:

		c = queue_p.pop(0)
		visited.add(c)
		if c not in nb_descendants_d:
			nb_descendants_d[c] = 0

		if c not in g.adjacents:
			continue

		for a in g.adjacents.get(c):

			if not a in visited:
				queue_p.append(a)
				visited.add(a)

			if not a in nb_descendants_d:
				nb_descendants_d[a] = 1
			else:
				nb_descendants_d[a] += 1

	return nb_descendants_d

def load_nb_descendants_d_new(g, value_sources):
	nb_descendants_d = {}

	queue_p = list(value_sources.keys())
	visited = set(queue_p)

	while queue_p:

		c = queue_p.pop(0)
		visited.add(c)
		if c not in nb_descendants_d:
			nb_descendants_d[c] = 0

		if c not in g.adjacents:
			continue

		for a in g.adjacents.get(c):

			if not a in visited:
				queue_p.append(a)
				visited.add(a)

			if not a in nb_descendants_d:
				nb_descendants_d[a] = 1
			else:
				nb_descendants_d[a] += 1

	return nb_descendants_d

def create_value_info_computation(g, sources_dataItemValues, dataitem_index_file,
								  confidence_value_computation_info_dir):
	# in source dataitemValues the dataitem are present in form of ID
	print("Results will be stored into: ", confidence_value_computation_info_dir)
	if not os.path.exists(confidence_value_computation_info_dir):
		os.makedirs(confidence_value_computation_info_dir)
	d_cont = 0
	dataItemIds = {}  # dataitems will be indexed to generate file names

	for d in sources_dataItemValues:
		d_cont += 1
		print(str(d_cont), "/", str(len(sources_dataItemValues)))

		# sources for each value
		d_value_sources = sources_dataItemValues[d]

		print("computing reduction")
		# Now we compute the number of descendants of each nodes
		# which require to be considered in order to be able to apply the BFS
		# for propagating sources
		# Remember that a transitive reduction has been applied

		nb_descendants_d = load_nb_descendants_d_new(g, d_value_sources)

		# if you need the subgraph considered you just have to load
		# the adjacency lists of the graph (with transitive reduction)
		# for the visited values - these values will be stored in the result file
		# generated below

		# Propagation will start for the leaves of the redution
		queue_tmp = list()

		for c in nb_descendants_d.keys():
			if nb_descendants_d[c] == 0: queue_tmp.append(c)

		print("initial queue contains ", len(queue_tmp), "/", len(nb_descendants_d.keys()), "/", len(g.nodes),
			  " values")

		value_confidence_to_sum = {}
		new_sources = {}
		source_trustwordiness_to_remove = {}
		source_trustwordiness_to_add = {}

		visited = list()

		while (queue_tmp):

			n = queue_tmp.pop(0)
			if ";" in n:
				print()
			if not n in new_sources: new_sources[n] = set()
			if not n in d_value_sources: d_value_sources[n] = set()

			source_trustwordiness_to_add[n] = d_value_sources[n].difference(new_sources[n])
			new_sources[n] = new_sources[n] | d_value_sources[n]

			visited.append(n)

			if not n in g.adjacents: continue

			for a in g.adjacents.get(n):
				if not a in new_sources: new_sources[a] = set()
				if not a in source_trustwordiness_to_remove: source_trustwordiness_to_remove[a] = {}

				for t in new_sources[a].intersection(d_value_sources[n]):
					if not t in source_trustwordiness_to_remove[a]:
						source_trustwordiness_to_remove[a][t] = 1
					else:
						source_trustwordiness_to_remove[a][t] += 1

				new_sources[a] = new_sources[a] | new_sources[n]

				nb_descendants_d[a] -= 1
				if nb_descendants_d[a] == 0: queue_tmp.append(a)

				if not a in value_confidence_to_sum:
					value_confidence_to_sum[a] = set()

				value_confidence_to_sum[a].add(n)

		# just to check - this is for debugging
		# it can be removed after careful proof-reading
		for c in nb_descendants_d:
			if nb_descendants_d[c] != 0:
				print("Error detected... refer to devs")
				quit()

		print("Flushing results into: " + confidence_value_computation_info_dir + "/" + str(d_cont) + ".csv")
		f = open(confidence_value_computation_info_dir + "/" + str(d_cont) + ".csv", 'w', encoding='utf-8')

		stop = False

		for n in visited:

			n_value_confidence_to_sum = "none"
			n_source_trustwordiness_to_add = "none"
			n_source_trustwordiness_to_remove = "none"

			if n in value_confidence_to_sum and len(value_confidence_to_sum[n]) != 0:
				n_value_confidence_to_sum = ""
				for v in value_confidence_to_sum[n]:
					if (len(n_value_confidence_to_sum) != 0):
						n_value_confidence_to_sum += "-----"
					n_value_confidence_to_sum += v

			if n in source_trustwordiness_to_add and len(source_trustwordiness_to_add[n]) != 0:
				n_source_trustwordiness_to_add = ""
				for v in source_trustwordiness_to_add[n]:
					if (len(n_source_trustwordiness_to_add) != 0):
						n_source_trustwordiness_to_add += ";"
					n_source_trustwordiness_to_add += str(v)

			if n in source_trustwordiness_to_remove and len(source_trustwordiness_to_remove[n]) != 0:

				n_source_trustwordiness_to_remove = ""

				for v in source_trustwordiness_to_remove[n]:
					if (len(n_source_trustwordiness_to_remove) != 0):
						n_source_trustwordiness_to_remove += ";"
					n_source_trustwordiness_to_remove += v + "=" + str(source_trustwordiness_to_remove[n][v])

				print("Things to remove to compute ", n)
				stop = True

			source_string_propagated = ""
			for ns in new_sources[n]:
				if (len(source_string_propagated) != 0): source_string_propagated += ";"
				source_string_propagated += str(ns)

			f.write(
				n + "\t" + n_value_confidence_to_sum + "\t" + n_source_trustwordiness_to_add + "\t" + n_source_trustwordiness_to_remove + "\t" + source_string_propagated + '\n')

		f.close()
		if (stop): exit()

		dataItemIds[d] = d_cont  # stores the id of the value

	print("flushing dataitem index into: " + dataitem_index_file)
	# Write dataitem index
	f = open(dataitem_index_file, 'w', encoding='utf-8')
	for k in dataItemIds:
		f.write(k + "\t" + str(dataItemIds[k]) + '\n')
	f.close()

def get_father_dict(children):
	father_dict = dict()
	for v in children:
		for child in children[v]:
			if child not in father_dict:
				father_dict[child] = set()
			father_dict[child].add(v)
	return father_dict

def get_depth(children, root):
	depth_dict = dict()

	queue = list()
	queue.append(root)

	while queue:

		n = queue.pop(0)

		if n not in depth_dict:
			depth_dict[n] = 0

		if n not in children:
			continue

		for a in children[n]:
			#if a == n:continue
			if a not in depth_dict:
				depth_dict[a] = depth_dict[n] + 1
			else:
				if depth_dict[n] + 1 > depth_dict[a]:
					depth_dict[a] = depth_dict[n] + 1
			queue.append(a)

	return depth_dict

if __name__ == '__main__':
	ancestors = dict()
	ancestors['A'] = {'A'}
	ancestors['B'] = {'A', 'B'}
	ancestors['C'] = {'A', 'B', 'C'}
	ancestors['D'] = {'A', 'B', 'C', 'D'}
	ancestors['E'] = {'A', 'B', 'C', 'E'}
	ancestors['F'] = {'A', 'B', 'F'}
	ancestors['G'] = {'A', 'B', 'G'}
	ancestors['H'] = {'A', 'H'}
	ancestors['I'] = {'A', 'H', 'I'}
	ancestors['L'] = {'A', 'H', 'I', 'L'}

	ancestors = dict()
	ancestors['root'] = {'root'}
	ancestors['a'] = {'root', 'a'}
	ancestors['b'] = {'root', 'b'}
	ancestors['c'] = {'root', 'c', 'a'}
	ancestors['d'] = {'root', 'd', 'a', 'e', 'b'}
	ancestors['e'] = {'root', 'e', 'b'}

	g = loadGraphOfURIs(ancestors)
	g_Red = perform_transitive_reduction(g)


	children = dict()
	for n in g_Red.nodes:
		for m in g_Red.adjacents.get(n):
			if n != m:
				if m not in children:
					children[m] = set()
				children[m].add(n)
	node_depths = get_depth(children, 'root')
	print("Depth of DAG " + str(max(node_depths.values())))
	exit()
	nb_descendants_d = {}

	queue_p = ['A', 'I', 'F', 'D', 'E']
	visited = set(queue_p)

	while queue_p:

		c = queue_p.pop(0)
		visited.add(c)
		if c not in nb_descendants_d:
			nb_descendants_d[c] = 0

		if c not in g.adjacents:
			continue

		for a in g.adjacents.get(c):

			if not a in visited:
				queue_p.append(a)
				visited.add(a)

			if not a in nb_descendants_d:
				nb_descendants_d[a] = 1
			else:
				nb_descendants_d[a] += 1

	leaves = {'D', 'E', 'F', 'G', 'L'}
