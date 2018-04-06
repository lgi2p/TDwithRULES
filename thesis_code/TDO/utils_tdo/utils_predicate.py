import csv
import os
import sys

cwd = os.getcwd()
if ("TDO") in cwd:
	index_tdo = cwd.index("TDO")
	cwd = cwd[:index_tdo]
	sys.path.append(cwd)
	from TDO.utils_tdo import utils_taxonomy
else:
	sys.path.append('D:/Dropbox/thesis_code/TDO')
	from utils_tdo import utils_taxonomy

predicate = ""


def set_predicate(new_predicate):
	global predicate
	try:
		predicate = new_predicate
		return True
	except:
		return False


def get_predicate():
	return predicate


def load_ic(file_path):
	try:
		ic_values = dict()

		f = open(file_path, "r")
		for line in f:
			line = line.strip()
			line = line.split('\t')
			item_id = line[0]
			ic = float(line[1])
			ic_values[item_id] = ic
		f.close()

		return ic_values

	except:
		print("No children file")
		print("Unexpected error:", sys.exc_info()[0])
		return None


def loading_taxonomy_dbpedia(ancestors_):
	try:
		tax_domain = set()
		for v_ in ancestors_:
			tax_domain.add(v_)
			tax_domain.update(set(ancestors_[v_]))

		return tax_domain
	except:
		print("Error in loading the taxonomy")
		return None




def loading_ancestors_dbpedia(path_ancestor_file_):
	'''the ancestor file should have the header part
	the ancestor file tr have  not the header part
	return a dictionary <key= value, values = inclusive ancestors of the value>
	'''
	try:
		ancestors = dict()
		with open(path_ancestor_file_, "r") as file_ancestor:
			if not (path_ancestor_file_.endswith("_tr.csv")):
				file_ancestor.readline()  # there is the header
			for row in file_ancestor:
				row = row.strip()
				data = row.split('\t')
				key = data[0]
				line_anc = (data[1]).replace(';http', '_____http')
				values = line_anc.split('_____')
				ancestors[key] = values

			'''european_country = {"http://dbpedia.org/resource/Poland", "http://dbpedia.org/resource/France", "http://dbpedia.org/resource/Italy", "http://dbpedia.org/resource/Germany", "http://dbpedia.org/resource/Spain", "http://dbpedia.org/resource/Netherlands", "http://dbpedia.org/resource/United_Kingdom","http://dbpedia.org/resource/Belgium", "http://dbpedia.org/resource/Romania"}
			to_add_set= {"http://dbpedia.org/ontology/Place","http://dbpedia.org/ontology/Continent","http://dbpedia.org/resource/Europe","http://www.w3.org/2002/07/owl#Thing","http://dbpedia.org/ontology/PopulatedPlace"}
			for v in ancestors:
				for a in ancestors[v]:
					if a in european_country:
						#print(v)
						ancestors[v].update(to_add_set)
						break
			#print("OKOKOK")
			to_add_set = {"http://dbpedia.org/ontology/Place", "http://dbpedia.org/ontology/Continent", "http://www.w3.org/2002/07/owl#Thing",
			              "http://dbpedia.org/ontology/PopulatedPlace"}

			for v in ancestors:
				for a in ancestors[v]:
					if a == "http://dbpedia.org/ontology/Country":
						#print(v)
						#print("A")
						ancestors[v].update(to_add_set)
						#print("B")
						break

			#print("AAAA")
			f_out = open("D:\\data_VALE\\thesis_code\\TDO\\required_files\\birthPlace\\ancestors_heuristic.csv", "w", encoding='utf-8')
			for v in ancestors:
				str_out = v + "\t"
				for a in ancestors[v]:
					str_out += a + ";"
				str_out = str_out[:-1] + "\n"
				f_out.write(str_out)
				f_out.flush()
			f_out.close()
			exit()'''
			'''print(ancestors["http://dbpedia.org/resource/France"])'''
		return ancestors
	except:

		e = sys.exc_info()[0]
		print(e)
		print("No ancestor file")
		return None

def loading_ancestors_dbpedia_V2(path_ancestor_file_):
	'''the ancestor file should have the header part
	the ancestor file tr have  not the header part
	return a dictionary <key= value, values = inclusive ancestors of the value>
	'''
	try:
		ancestors = dict()
		with open(path_ancestor_file_, "r") as file_ancestor:
			if not (path_ancestor_file_.endswith("_tr.csv")):
				file_ancestor.readline()  # there is the header
			for row in file_ancestor:
				row = row.strip()
				data = row.split('\t')
				key = data[0]
				line_anc = (data[1]).replace(';http', '_____http')
				values = line_anc.split('_____')
				ancestors[key] = set(values)

			'''european_country = {"http://dbpedia.org/resource/Poland", "http://dbpedia.org/resource/France", "http://dbpedia.org/resource/Italy", "http://dbpedia.org/resource/Germany", "http://dbpedia.org/resource/Spain", "http://dbpedia.org/resource/Netherlands", "http://dbpedia.org/resource/United_Kingdom","http://dbpedia.org/resource/Belgium", "http://dbpedia.org/resource/Romania"}
			to_add_set= {"http://dbpedia.org/ontology/Place","http://dbpedia.org/ontology/Continent","http://dbpedia.org/resource/Europe","http://www.w3.org/2002/07/owl#Thing","http://dbpedia.org/ontology/PopulatedPlace"}
			for v in ancestors:
				for a in ancestors[v]:
					if a in european_country:
						#print(v)
						ancestors[v].update(to_add_set)
						break
			#print("OKOKOK")
			to_add_set = {"http://dbpedia.org/ontology/Place", "http://dbpedia.org/ontology/Continent", "http://www.w3.org/2002/07/owl#Thing",
			              "http://dbpedia.org/ontology/PopulatedPlace"}

			for v in ancestors:
				for a in ancestors[v]:
					if a == "http://dbpedia.org/ontology/Country":
						#print(v)
						#print("A")
						ancestors[v].update(to_add_set)
						#print("B")
						break

			#print("AAAA")
			f_out = open("D:\\data_VALE\\thesis_code\\TDO\\required_files\\birthPlace\\ancestors_heuristic.csv", "w", encoding='utf-8')
			for v in ancestors:
				str_out = v + "\t"
				for a in ancestors[v]:
					str_out += a + ";"
				str_out = str_out[:-1] + "\n"
				f_out.write(str_out)
				f_out.flush()
			f_out.close()
			exit()'''
			'''print(ancestors["http://dbpedia.org/resource/France"])'''
		return ancestors
	except:

		e = sys.exc_info()[0]
		print(e)
		print("No ancestor file")
		return None


def loading_descendants_dbpedia(path_file):
	try:
		descendants = dict()

		with open(path_file, "r") as reader:
			# no header
			for row in reader:
				row = row.strip()
				data = row.split('\t')
				key = data[0]
				if len(data) > 1:
					line_desc = (data[1]).replace(';http', '_____http')
					values = line_desc.split('_____')
					descendants[key] = set(values)
				else:
					descendants[key] = set()

		return descendants
	except:
		print("No descendent file")
		print("Unexpected error:", sys.exc_info()[0])
		return None


def loading_children_dbpedia(file_path_):
	'''given a file where each row contains the URI of a node (e.g. a value) and all its URI's children
	return a dictionary <key= value, values = children of the value>
	'''
	try:
		children_ = dict()
		with open(file_path_, "r") as file:
			for line in file:
				line = line.strip()
				data = line.split('\t')
				key = data[0]
				if len(data) == 1:
					values = []
				else:
					child_str = (data[1]).replace(';http', '_____http')
					values = child_str.split('_____')
				# update dictionary of children of each node
				children_[key] = set(values)

		return children_
	except:
		print ("No children file")
		print ("Unexpected error:", sys.exc_info()[0])
		return None


def loading_descendants_or_ancestors_go(path_descendant_file):
	try:
		gene_values = dict()
		tax_domain = set()
		f = open(path_descendant_file, "r")
		for line in f.readlines():
			line = line.strip()
			data = line.split('\t')
			gene_id = data[0]
			values = set()
			for index in range(1, len(data)):
				values.add(data[index])
			gene_values[gene_id] = values
			tax_domain.update(values)
		return [gene_values, tax_domain]
	except:
		print("No descendant or ancestors file")
		return None


def loading_ground_truth(path_ground_file):
	'''read GROUNDTRUTH csv file where all the triple are saved.
	format of GROUNDTRUTH.csv file is "subject, predicate, value"
	example PabloPicasso, bornIn, Malaga
	#        Giovanni, bornIn, Renate
	#        etc
	return an array where in the first position there is a dictionary <key= data item, values = true value>
	and in the second position the set of data items
	'''
	try:
		D = []
		truth = dict()
		with open(path_ground_file, "r") as csvfile:
			reader = csv.DictReader(csvfile, delimiter='\t', quotechar='|')

			for row in reader:
				dataitem = row['subject']  # for the moment I don't use predicate ---> + ';' + row['predicate']
				value = row['value']
				truth[dataitem] = value
				D.append(dataitem)

		return [truth, D]
	except:
		print("Error in loading ground truth")
		print(sys.exc_info()[0])
		D = []
		truth = dict()
		reader = open(path_ground_file, "r", encoding="utf-8")
		header = True
		for row in reader:
			if header:
				header=False
				continue
			row = row.strip().split('\t')
			dataitem = row[0]  # for the moment I don't use predicate ---> + ';' + row['predicate']
			value = row[2]
			truth[dataitem] = value
			D.append(dataitem)

		return [truth, D]


def loading_predicate_info(base_dir, predicate_):
	base_dir = base_dir + predicate_ + "/"
	if predicate_ == 'genre':
		graph_file = base_dir + 'ancestors_heuristic_genre_base.csv'
		graph_file_reduced = base_dir + 'ancestors_heuristic_genre_base_tr.csv'
		children_file = base_dir + "children_genre_base.csv"
		path_ground_file = base_dir + 'sample_genre_base_3.csv'
		descendants_file = base_dir + 'descendants_genre_base.csv'
		ic_file = base_dir + "seco_IC_" + str(predicate_) + ".csv"
		root_element = "http://www.w3.org/2002/07/owl#Thing"
	else:  # the predicate is 'birthPlace'
		if predicate_ == 'birthPlace':
			graph_file = base_dir + 'ancestors_heuristic.csv'
			graph_file_reduced = base_dir + 'ancestors_heuristic_tr.csv'
			children_file = base_dir + "children.csv"
			path_ground_file = base_dir + 'sample_ground_grouped.csv'
			descendants_file = base_dir + 'specific_value_new.csv'
			ic_file = base_dir + "seco_IC_" + str(predicate_) + ".csv"
			root_element = "http://www.w3.org/2002/07/owl#Thing"
		else:  # the predicate is CC, ...
			graph_file = base_dir + 'output_' + predicate_ + '_ancestors.tsv'
			graph_file_reduced = base_dir + 'output_' + predicate_ + '_ancestors_tr.tsv'
			children_file = base_dir + 'output_' + predicate_ + '_children.tsv'
			path_ground_file = base_dir + 'sample_ground_' + predicate_ + '.csv'
			descendants_file = base_dir + 'output_' + predicate_ + '_descendants.tsv'
			ic_file = base_dir + "seco_IC_" + str(predicate_) + ".csv"
			if predicate_ == "CC":
				root_element = "0005575"
			else:
				if predicate_ == "MF":
					root_element = "0003674"
				else:
					root_element = "0008150"

	if predicate_ == 'genre' or predicate_ == 'birthPlace':
		print(children_file)
		children = loading_children_dbpedia(children_file)
		print("number of children " + str(len(children)))
		print(descendants_file)
		descendants = loading_descendants_dbpedia(descendants_file)
		print("number of descendants " + str(len(descendants)))
		print(graph_file)
		ancestors= loading_ancestors_dbpedia(graph_file)
		line_written = 0
		'''f_out = open("D:\\data_VALE\\thesis_code\\TDO\\required_files\\birthPlace\\new_ancestors.csv", "w", encoding='utf-8')
		for v in ancestors:
			str_out = v + "\t"
			for a in ancestors[v]:
				str_out += str(a) + ";"
			str_out = str_out[:-1] +"\n"
			f_out.write(str_out)
			f_out.flush()
			line_written += 1
			if line_written%10000 == 0: print(line_written)
		f_out.close()
		exit()'''
		tax = loading_taxonomy_dbpedia(ancestors)
		print("number of ancestors " + str(len(ancestors)))
	else:
		children = loading_descendants_or_ancestors_go(children_file)[0]
		print("number of children " + str(len(children)))
		descendants = loading_descendants_or_ancestors_go(descendants_file)[0]
		print("number of descendants " + str(len(descendants)))
		ancestors_and_tax = loading_descendants_or_ancestors_go(graph_file)
		ancestors = ancestors_and_tax[0]
		tax = ancestors_and_tax[1]
		print("number of ancestors " + str(len(ancestors)))

	apply_transitive_reduction = True
	if os.path.exists(graph_file_reduced):
		apply_transitive_reduction = False
	##to remove
	#apply_transitive_reduction = True
	g = utils_taxonomy.load_graph(graph_file, graph_file_reduced, apply_transitive_reduction)
	print("GRAPH FILE REDUCED " + str(graph_file_reduced))
	ic_values = load_ic(ic_file)

	res_gt = loading_ground_truth(path_ground_file)
	ground = res_gt[0]
	dataitems = res_gt[1]

	return [children, descendants, ancestors, tax, root_element, g, ic_values, ground, dataitems, graph_file,
			graph_file_reduced]
