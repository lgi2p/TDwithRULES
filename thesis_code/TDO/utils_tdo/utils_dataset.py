import copy


class ValueConfidenceInfo:

	'Information required for computing the confidence of a specific value'
	value = None # value associated to the object
	confidence = None # current confidence of the value
	valueDependencies = None # the dependencies among value confidences -  confidence of this values have to be sum
	sourceTrustwordinessToAdd = None # set of the source trustwordiness to add - trustwordiness of these sources have to be added
	sourceTrustwordinessToRemove = None # dictionary of the source trustwordiness to remove (potentially several times for a same source)  - trustwordiness of these sources have to be added

	def __init__(self, value, confidence):
		self.value = value
		self.confidence = confidence

	def setValueDependencies(self, vd):
		self.valueDependencies = vd

	def setSourceTrustwordinessToAdd(self, d):
		self.sourceTrustwordinessToAdd = d

	def setSourceTrustwordinessToRemove(self, d):
		self.sourceTrustwordinessToRemove = d

	def __str__(self):

		value_dependencies_string = "None"
		source_trustwordiness_to_add_string = "None"
		source_trustwordiness_to_remove_string = "None"
		if not self.valueDependencies == None: value_dependencies_string = self.valueDependencies
		if not self.sourceTrustwordinessToAdd == None: source_trustwordiness_to_add_string = self.sourceTrustwordinessToAdd
		if not self.sourceTrustwordinessToRemove == None: source_trustwordiness_to_remove_string = self.sourceTrustwordinessToRemove
		out = "-----------------------------------------------------------------\n"
		out += "value: "+ self.value + "\n"
		out += "-----------------------------------------------------------------\n"
		out += "confidence: " + str(self.confidence) + "\n"
		out += "-----------------------------------------------------------------\n"
		out += "value conf to sum " + value_dependencies_string + "\n"
		out += "-----------------------------------------------------------------\n"
		out += "source to add " + source_trustwordiness_to_add_string + "\n"
		out += "-----------------------------------------------------------------\n"
		out += "source to remove " + source_trustwordiness_to_remove_string + "\n"
		out += "-----------------------------------------------------------------"
		return out


def __init__(self):
	self.D = list()
	self.F_d = dict()


def load_sources_info(sources_file, header):
	''' return a dictionary contained for each source its trustworthiness level
	<key = source_id, value = source_trustworthiness level>'''
	accuracies_source = {}

	with open(sources_file, "r") as reader:
		for line in reader:
			if header:
				header = False
				continue

			line = line.strip()
			data = line.split("\t")

			if (len(data) != 2):
				print ("[Warning] skipping " + str(line))
				continue

			s = int(data[0].replace("source", ""))
			acc = float(data[1])

			if not (s in accuracies_source):
				accuracies_source[s] = acc
			else:
				"WARNING DUPLICATE SOURCES"

	return accuracies_source


def load_facts(facts_file, header):
	'''upload a dictionary of this form
	<key = dataitem , value = <key = value_for_d, value = sources> >
	using the fact_XXX file - our dataset
	'''
	sources_dataItemValues = {}
	fact_cont = 0
	with open(facts_file, "r", encoding="utf-8") as reader:

		for line in reader:
			fact_cont = fact_cont + 1

			if header:
				header = False
				continue

			line = line.strip()
			data = line.split("\t")

			if (len(data) != 4):
				print(fact_cont)
				print ("[Warning] skipping " + str(line))
				continue

			d = data[1]
			v = data[2]

			s = int(data[3].replace("source", ""))
			if not (d in sources_dataItemValues): sources_dataItemValues[d] = {}
			if not (v in sources_dataItemValues[d]): sources_dataItemValues[d][v] = set()
			sources_dataItemValues[d][v].add(s)

	return sources_dataItemValues


def load_facts_with_ids(facts_file, header, dataitem_ids):
	'''required if there are problems with memory space
	It does the same function of load_facts, but it load the ids not the string of data items'''
	sources_dataItemValues = {}
	with open(facts_file, "r", encoding="utf-8") as reader:
		for line in reader:
			if header:
				header = False
				continue

			line = line.strip()
			data = line.split("\t")

			if (len(data) != 4):
				print ("[Warning] skipping " + str(line))
				continue

			d = data[1]
			d = int(dataitem_ids[d])
			v = data[2]
			s = int(data[3].replace("source", ""))

			if not (d in sources_dataItemValues): sources_dataItemValues[d] = {}
			if not (v in sources_dataItemValues[d]): sources_dataItemValues[d][v] = set()
			sources_dataItemValues[d][v].add(s)

	return sources_dataItemValues


def load_fact_and_source_info(sources_dataItemValues):
	'''this function retrieves two dictionary
	- F_s represents the set of facts claimed by a source (<key = source, value = facts claimed by the source>)
	- S represents the set of sources that claim a fact (<key = fact, value = sources claimed the fact>)'''
	print ("Loading facts and source info")
	F_s = {}
	S = {}

	for d in sources_dataItemValues:
		for v in sources_dataItemValues.get(d):
			fact_id = d + v
			for s in sources_dataItemValues.get(d).get(v):

				if not s in F_s: F_s[s] = set()
				F_s.get(s).add(fact_id)

				if not fact_id in S: S[fact_id] = set()
				S.get(fact_id).add(s)

	return [F_s, S]


def load_dataitem_ids(file_path):
	# dataitem ids for storing informaiton for the propagation of belief phase
	dataitem_ids = {}
	print ("Loading dataitem ids from: ", file_path)

	file = open(file_path, 'r', encoding="utf-8")
	for row in file.readlines():
		row = (row[0:-1]).split('\t')  # not consider \n char
		dataitem_ids[row[0]] = row[1]
	file.close()
	print ("dataitems loaded: ", len(dataitem_ids))

	return dataitem_ids


def load_all_dataitem_values_confidence_infos_low_memory(dataitem_ids, dir_path, sources_dataItemValues):
	'''read the file where the information required for computing the effects of belief propagation'''
	print ("Loading information to compute confidence of facts (dataitem + values) ")
	print ("processing ", len(dataitem_ids), " dataitems")
	print ("source directory: ", dir_path)

	S_prop = {}
	app_conf_dict = dict()
	app_source_dict = dict()

	cont = 0
	cont_no_facts = 0
	for data_item in dataitem_ids:
		cont = cont + 1
		if (cont % 1000 == 0):
			print ("Processed " + str(cont) + "/" + str(len(dataitem_ids)))
		fpath = dir_path + "/" + str(dataitem_ids.get(data_item)) + ".csv"

		f = open(fpath, 'r', encoding="utf-8")

		for row in f.readlines():

			row = row.strip()
			data = row.split("\t")
			if (len(data) != 5):
				print ("[2_Warning] Excluding: " + row)
			else:
				if data[0] in sources_dataItemValues[data_item]:
					S_prop[data_item + data[0]] = data[4]
				else:
					S_prop[data_item + data[0]] = data[4]
					cont_no_facts = cont_no_facts + 1

				if data_item not in app_conf_dict:
					app_conf_dict[data_item] = set()
				app_conf_dict[data_item].add(data[0])

				for s in data[4].split(';'):
					s = int(s)
					if s not in app_source_dict:
						app_source_dict[s] = set()
					app_source_dict[s].add(data_item)

		f.close()

	print ("number of values confidence infos loaded: " + str(len(S_prop)))
	print ("number of values confidence infos for which no source provided this facts: " + str(cont_no_facts))
	return [None, None, S_prop, app_conf_dict, app_source_dict]

def load_all_dataitem_values_confidence_infos_low_memory_small(sources_dataItemValues):
	'''read the file where the information required for computing the effects of belief propagation'''

	for data_item in dataitem_ids:
		cont = cont + 1
		if (cont % 1000 == 0):
			print ("Processed " + str(cont) + "/" + str(len(dataitem_ids)))
		fpath = dir_path + "/" + str(dataitem_ids.get(data_item)) + ".csv"

		f = open(fpath, 'r', encoding="utf-8")

		for row in f.readlines():

			row = row.strip()
			data = row.split("\t")
			if (len(data) != 5):
				print ("[2_Warning] Excluding: " + row)
			else:
				if data[0] in sources_dataItemValues[data_item]:
					S_prop[data_item + data[0]] = data[4]
				else:
					S_prop[data_item + data[0]] = data[4]
					cont_no_facts = cont_no_facts + 1

				if data_item not in app_conf_dict:
					app_conf_dict[data_item] = set()
				app_conf_dict[data_item].add(data[0])

				for s in data[4].split(';'):
					s = int(s)
					if s not in app_source_dict:
						app_source_dict[s] = set()
					app_source_dict[s].add(data_item)

		f.close()

	print ("number of values confidence infos loaded: " + str(len(S_prop)))
	print ("number of values confidence infos for which no source provided this facts: " + str(cont_no_facts))
	return [None, None, S_prop, app_conf_dict, app_source_dict]

def loading_values_sim_ids(path_ids_file_):
	try:
		ids = {}
		with open(path_ids_file_, encoding='utf-8') as file:
			for row in file.readlines():
				row = row.split('\t')
				ids[row[1][0:-1]] = row[0]  # do not consider \n digit
		return ids
	except:
		print("Errors in loading values sim ids")
		return None


def load_values_sim_measure(path_values_sim_file_, myzipfile_, value_id_, sim_dict_):
	file = myzipfile_.open(path_values_sim_file_ + value_id_)
	# read file of sim measures for this solution
	for row in file.readlines():
		row = (row.decode()).split('\t')
		sim_dict_[row[0]] = float(row[1][0:-1])  # not consider \n char

	file.close()
	return sim_dict_


def read_estimation_file_trad(trad_output_trust_file, trad_output_conf_file):

	T_trad = dict()
	f = open(trad_output_trust_file, "r")
	for line in f:
		line = line.strip()
		line = line.split('\t')
		T_trad[int(line[0])] = float(line[1])
	f.close()

	C_trad = dict()
	f = open(trad_output_conf_file, "r",encoding="utf8")
	for line in f:
		line = line.strip()
		line = line.split('\t')
		C_trad[line[0]] = float(line[1])
	f.close()

	return [T_trad, C_trad]


def read_trust_estimation_file(trust_file):
	T_trad = dict()
	f = open(trust_file, "r")
	for line in f:
		line = line.strip()
		line = line.split('\t')
		T_trad[int(line[0])] = float(line[1])
	f.close()
	return T_trad


def read_estimation_file_adapt(adapted_1_output_trust_file, adapted_1_output_conf_file):

	T_adapt = dict()
	f = open(adapted_1_output_trust_file, "r")
	for line in f:
		line = line.strip()
		line = line.split('\t')
		T_adapt[int(line[0])] = float(line[1])
	f.close()

	C_adapt = dict()
	T_average = dict()
	T_average_normalized = dict()
	f = open(adapted_1_output_conf_file, "r", encoding="utf8")
	for line in f:
		line = line.strip()
		line = line.split('\t')
		C_adapt[line[0]] = float(line[1])
		T_average[line[0]] = float(line[2])
		if len(line)>3:
			T_average_normalized[line[0]] = float(line[3])
	f.close()

	return [T_adapt, C_adapt, T_average, T_average_normalized]


def read_estimation_file(trust_file, conf_file, flag_traditional_model):
	if flag_traditional_model:
		return read_estimation_file_trad(trust_file, conf_file)
	else:
		return read_estimation_file_adapt(trust_file, conf_file)


def read_estimation_file_conf_trad(trad_output_conf_file):
	C_trad = dict()
	f = open(trad_output_conf_file, "r",encoding="utf8")
	for line in f:
		line = line.strip()
		line = line.split('\t')
		C_trad[line[0]] = float(line[1])
	f.close()

	return [None, C_trad]


def read_estimation_file_conf_adapt(adapted_1_output_conf_file):
	C_adapt = dict()
	T_average = dict()
	T_average_normalized = dict()
	f = open(adapted_1_output_conf_file, "r", encoding="utf8")
	for line in f:
		line = line.strip()
		line = line.split('\t')
		C_adapt[line[0]] = float(line[1])
		T_average[line[0]] = float(line[2])
		if len(line)>3:
			T_average_normalized[line[0]] = float(line[3])
	f.close()

	return [None, C_adapt, T_average, T_average_normalized]


def read_conf_estimation_file(conf_file, flag_traditional_model):
	if flag_traditional_model:
		return read_estimation_file_conf_trad(conf_file)
	else:
		return read_estimation_file_conf_adapt(conf_file)


def normalize_trust_average(trust_average_adapt_dict, incl_ancestors, incl_descendants, sources_dataitem_values_local):
	# function that normalizes the source trust average assosiated to each fact

	trust_average_adapt_normalized = copy.deepcopy(trust_average_adapt_dict)

	for d in sources_dataitem_values_local:
		dom_d = set(sources_dataitem_values_local[d])

		for v in sources_dataitem_values_local[d]:
			n_claims = 0
			set_app = dom_d.intersection(incl_descendants[v])
			for element in set_app:
				n_claims += len(sources_dataitem_values_local[d][element])
			trust_average_adapt_normalized[d + v] *= (1.00 - (1.00 / (0.1 + n_claims)))

	# preprocessing necessario per normalizzare anche fatti propagati
	for d in sources_dataitem_values_local:
		dom_d = sources_dataitem_values_local[d]
		values_to_prop = set()
		for v in sources_dataitem_values_local[d]:
			values_to_prop = values_to_prop.union(incl_ancestors[v])
		values_to_prop = values_to_prop.difference(dom_d)
		n_claims = 0
		for v in values_to_prop:
			app_set = incl_descendants[v].intersection(dom_d)
			for item in app_set:
				n_claims += len(sources_dataitem_values_local[d][item])

			if d + v in trust_average_adapt_normalized:
				trust_average_adapt_normalized[d + v] *= (1.00 - (1.00 / (0.1 + n_claims)))

	return trust_average_adapt_normalized


def normalize_trust_average_book(trust_average_adapt_dict, sources_dataitem_values_local):
	# function that normalizes the source trust average assosiated to each fact

	trust_average_adapt_normalized = copy.deepcopy(trust_average_adapt_dict)

	V_d = dict()  # all author names for each data item
	for d in sources_dataitem_values_local:
		V_d[d] = set()
		for v in sources_dataitem_values_local[d]:
			app_ = v.split(";")
			for other_item in app_:
				V_d[d].add(other_item)

	cont_dict = dict()
	for d in V_d:
		cont_dict[d] = dict()
		for v_single_name in V_d[d]:
			cont_dict[d][v_single_name] = 0

	for d in sources_dataitem_values_local:
		for v in sources_dataitem_values_local[d]:
			source_set = sources_dataitem_values_local[d][v]

			for v_single_name in v.split(";"):
				cont_dict[d][v_single_name] += len(source_set)

				if len(v_single_name.split(" ")) == 1:
					first_or_last = v_single_name.split(" ")[0]
					for other in sources_dataitem_values_local[d]:
						if v != other:
							for other_single in other.split(";"):
								if len(other_single.split(" ")) > 1:
									if first_or_last == other_single.split(" ")[1]:
										source_set_app = sources_dataitem_values_local[d][other]
										cont_dict[d][v_single_name] += len(source_set_app)

	for d in cont_dict:
		for v_single_name in cont_dict[d]:
			n_claims = cont_dict[d][v_single_name]
			trust_average_adapt_normalized[d + v_single_name] *= (1.00 - (1.00 / (0.1 + n_claims)))

	return trust_average_adapt_normalized


def normalize_trust_average_book_no_prop(trust_average_adapt_dict, sources_dataitem_values_local):
	# function that normalizes the source trust average assosiated to each fact

	trust_average_adapt_normalized = copy.deepcopy(trust_average_adapt_dict)

	V_d = dict()  # all author names for each data item
	for d in sources_dataitem_values_local:
		V_d[d] = set()
		for v in sources_dataitem_values_local[d]:
			app_ = v.split(";")
			for other_item in app_:
				V_d[d].add(other_item)

	cont_dict = dict()
	for d in V_d:
		cont_dict[d] = dict()
		for v_single_name in V_d[d]:
			cont_dict[d][v_single_name] = 0

	for d in sources_dataitem_values_local:
		for v in sources_dataitem_values_local[d]:
			source_set = sources_dataitem_values_local[d][v]

			for v_single_name in v.split(";"):
				cont_dict[d][v_single_name] += len(source_set)


	for d in cont_dict:
		for v_single_name in cont_dict[d]:
			n_claims = cont_dict[d][v_single_name]
			trust_average_adapt_normalized[d + v_single_name] *= (1.00 - (1.00 / (0.1 + n_claims)))

	return trust_average_adapt_normalized

def compute_average_trustworhiness(S_prop, T_final):
	T_average = dict()
	cont_sources = 0
	# evaluation of confidence of facts based on trustworthiness
	for fact_id in S_prop:
		if type(S_prop.get(fact_id)) is str:
			source_plus_set = S_prop.get(fact_id).split(";")
		else:
			source_plus_set = S_prop.get(fact_id)
		cont_sources = 0
		sum = 0
		for s in source_plus_set:
			try:
				s = int(s)
				sum = sum + T_final[s]
				cont_sources += 1
			except ValueError:
				try:
					sum = sum + T_final[int(s.replace("source", ""))]
					cont_sources += 1
				except ValueError:
					sum = sum + T_final[s]
					cont_sources += 1
		T_average[fact_id] = sum / cont_sources

	return T_average


def check_irregularities(source_dataitem_values, descendants, ground):
	for d in source_dataitem_values:
		sol = ground[d]
		desc_sol = set(descendants[sol])
		if sol in desc_sol:
			desc_sol.remove(sol)
		dom_d = set(source_dataitem_values[d])
		inter_set = desc_sol.intersection(dom_d)
		if len(inter_set)>0:
			print("error in data item "+ str(d))
			print("its domain is ")
			print(dom_d)
			return False
	return True


def read_estimation_file_conf_norm(conf_file_adapt_and_norm):
	C_adapt_norm = dict()
	f = open(conf_file_adapt_and_norm, "r", encoding="utf8")
	for line in f:
		line = line.strip()
		line = line.split('\t')
		C_adapt_norm[line[0]] = float(line[1])
	f.close()
	return C_adapt_norm