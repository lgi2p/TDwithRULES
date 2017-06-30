from SPARQLWrapper import SPARQLWrapper, JSON
import copy
import sys


def load_rules(file_rules):
	#return a dict containing for each rule its information (positive example, pca, support...)
	#the rules have head coverage higher than threshold, in this case hc_threshold is = 0,
	return load_rules_with_threshold(file_rules, 0.00)


def load_rules_with_threshold(file_rules, hc_threshold):
	R = dict()  # dict with key = rule str, values = list with positive example, conf pca, ..,.., and set of atoms of the body
	R_id = dict()  # dict for retriving the id of each rule - note that the id of a rule is its line number in the file of the rules

	header = True
	cont_lines = 0
	f = open(file_rules, "r")
	for line in f:
		cont_lines += 1
		if cont_lines % 10000 == 0:
			print(cont_lines)
		if line.startswith("Rule"):
			header = False
			continue
		if not header:
			line = line.strip()
			line_arr = line.split("\t")
			if len(line_arr) == 11:
				r = line_arr[0]
				r = ' '.join(r.split())
				head = r.split(" => ")[1]
				if head.count("?") != 2:
					continue
				if float(line_arr[1]) <= hc_threshold:
					continue
				body = r.split(" => ")[0]
				body_set = set()
				body_array = body.split(" ")

				i = 0
				while i < len(body_array):
					str_app = ""
					s = body_array[i]
					p = body_array[i + 1]
					o = body_array[i + 2]
					i += 3
					str_app += s + " " + p + " " + o + " "
					body_set.add(str_app[:-1])

				R_id[r] = cont_lines
				# support, PCA conf, Std conf, head coverage + bodyseet
				R[r] = [line_arr[4], line_arr[3], line_arr[2], line_arr[1], body_set]

	print("number of found rules " + str(len(R)))
	return [R, R_id]


def load_predicates_of_rules(rule_path):
	predicate_set = set()
	f = open(rule_path, "r")
	header = True

	cont_lines = 0
	for line in f:
		cont_lines += 1
		if cont_lines % 50000 == 0:
			print(cont_lines)
		if line.startswith("Rule"):
			header = False
			continue
		if not header:
			line = line.strip()
			line_arr = line.split("\t")
			if len(line_arr) == 11:
				r = line_arr[0]
				r = ' '.join(r.split())
				head = (r.split(" => ")[1])
				head = head.split(" ")
				p_head = head[1]
				predicate_set.add(p_head)

				body = (r.split(" => ")[0])
				body_array = body.split(" ")

				i = 0
				while i < len(body_array):
					p = body_array[i + 1]
					i += 3
					predicate_set.add(p)

	print('number of found predicates ' + str(len(predicate_set)))
	return predicate_set


def get_score(r, R):
	# score is evaluated aggregating support and pca confidencee
	metrics = R[r]
	support = float(metrics[0])
	PCA_conf = float(metrics[1])
	score = (1 - (1 / support)) * PCA_conf  # support = 1 --> it never happens
	'''
	alternativa
	head = (r.split(" => ")[1])
	H_size = get_size(head, KB)
	score = ( support / H_size ) * PCA_conf
	'''
	return score


# function with fuseky
def get_eligible_rules_fuseky(fact, R, sparql, rule_desc):
	eligible_rules_for_d = list()

	subj = fact[0]
	pred = fact[1]
	R_app = copy.deepcopy(R)
	cont = 0
	rule_key = list(R_app.keys())
	while rule_key:
		r = rule_key.pop(0)
		cont += 1
		# print(r)
		head = (r.split(" => ")[1])
		body = (r.split(" => ")[0])
		if pred in head:
			subj_var = head.split(" ")[0]
			if (subj_var.startswith("?")):
				body = body.replace(subj_var, subj)
				body_array = body.split(" ")

				str_app = ""
				i = 0
				while i < len(body_array):
					s = body_array[i]
					p = body_array[i + 1]
					# p = body_array[i + 1].replace("<", "")
					# p = p.replace(">", "")
					o = body_array[i + 2]
					i += 3
					str_app += str(s) + " " + str(p) + " " + str(o) + " . "

				query_str = "PREFIX dbo: <http://dbpedia.org/ontology/> PREFIX dbp: <http://dbpedia.org/property/> PREFIX foaf: <http://xmlns.com/foaf/0.1/> SELECT * WHERE { " + str(
					str_app) + " }"

				app = bytes(query_str, 'utf-8')
				query_str = str(app, 'unicode-escape')

				sparql.setQuery(str(query_str))
				sparql.setReturnFormat(JSON)
				qres = sparql.query().convert()

				if len(qres["results"]["bindings"]) > 0:
					eligible_rules_for_d.append(r)

			else:
				print("HERE")
				# il soggetto nella testa non è una variable
				# dovrei controllare verifico che il body sia elegible senza fare il replacement della variable con il soggetto del mio fatto
				# visto che è una regola sara sicuramente verificato e quindi lo metto eligible
				eligible_rules_for_d.append(r)

	return eligible_rules_for_d


'''def get_eligible_rules_fuseky_optimized(R, sparql, truth_, predicate_):
	eligible_rules_ = dict()
	dataitem_set = set(truth_.keys())

	cont = 0
	for rule in R:
		cont += 1
		if cont % 10 == 0:
			print("Number rules preprocessed " + str(cont))
		# print(r)
		head = rule.split(" => ")[1]
		body = rule.split(" => ")[0]
		if predicate_ in head:
			subj_head = head.split(" ")[0]
			if subj_head.startswith("?"):
				#body = body.replace(subj_var, subj)
				body_array = body.split(" ")

				str_app = ""
				i = 0
				while i < len(body_array):
					s = body_array[i]
					p = body_array[i + 1]
					o = body_array[i + 2]
					i += 3
					str_app += str(s) + " " + str(p) + " " + str(o) + " . "

				query_str = "PREFIX dbo: <http://dbpedia.org/ontology/> PREFIX dbp: <http://dbpedia.org/property/> PREFIX foaf: <http://xmlns.com/foaf/0.1/> SELECT " + str(subj_head) + " WHERE { " + str(str_app) + " }"

				app = bytes(query_str, 'utf-8')
				query_str = str(app, 'unicode-escape')

				sparql.setQuery(str(query_str))
				sparql.setReturnFormat(JSON)
				qres = sparql.query().convert()

				res_set = set()
				for v_res in qres["results"]["bindings"]:
					str_res = str(v_res[subj_head.replace("?", "")]["value"])
					res_set.add(str_res)

				intersection_set = dataitem_set.intersection(res_set)

				for d in intersection_set:
					if d not in eligible_rules_:
						eligible_rules_[d] = list()
					eligible_rules_[d].append(rule)

			else:
				# il soggetto nella testa non è una variable
				# dovrei controllare verifico che il body sia elegible senza fare il replacement della variable con il soggetto del mio fatto
				# visto che è una regola sara sicuramente verificato e quindi lo metto eligible
				eligible_rules_[subj_head.replace("<", "").replace(">", "")].append(rule)

	return eligible_rules_'''

def apply_rules_to_f_fuseky(r, fact, sparql):
	subj = fact[0]
	value = fact[2]

	head = (r.split(" => ")[1])
	body = (r.split(" => ")[0])
	obj_head = head.split(" ")[2]
	if not obj_head.startswith("?"):
		# costante - confronto direttamente
		if value == obj_head:
			return True
		else:
			return False
	else:
		# faccio query per recuperare tutti i possibili valori dell oggetto per una certa instnziazione delle var
		subj_var = head.split(" ")[0]
		body = body.replace(subj_var, subj)

		r_array = body.split(" ")
		str_app = ""
		i = 0
		while i < len(r_array):
			s = r_array[i]
			p = r_array[i + 1]
			o = r_array[i + 2]
			i += 3
			str_app += s + " " + p + " " + o + " . "

		query_str = "PREFIX dbo: <http://dbpedia.org/ontology/> PREFIX dbp: <http://dbpedia.org/property/> PREFIX foaf: <http://xmlns.com/foaf/0.1/> SELECT distinct " + str(
			obj_head) + " WHERE { " + str_app + " }"

		app = bytes(query_str, 'utf-8')
		query_str = str(app, 'unicode-escape')

		sparql.setQuery(query_str)
		sparql.setReturnFormat(JSON)
		qres = sparql.query().convert()

		for v_res in qres["results"]["bindings"]:
			str_res = "<" + str(v_res[obj_head.replace("?", "")]["value"]) + ">"
			if value == str_res:
				return True
		# se arrivo qui perchè non è corrisposto
		return False

	print("ERROR")
	return False


def apply_rules_to_d_fuseky(d, r, sparql):
	# return the set of values that are possible to obtain with this rule
	valid_values = set()
	subj = "<" + str(d) + ">"

	head = (r.split(" => ")[1])
	body = (r.split(" => ")[0])
	obj_head = head.split(" ")[2]
	if (not obj_head.startswith("?")):
		# costante - confronto direttamente
		valid_values.add(obj_head)
		return valid_values

	else:
		# faccio query per recuperare tutti i possibili valori dell oggetto per una certa instnziazione delle var
		subj_var = head.split(" ")[0]
		body = body.replace(subj_var, subj)

		r_array = body.split(" ")
		str_app = ""
		i = 0
		while i < len(r_array):
			s = r_array[i]
			p = r_array[i + 1]
			o = r_array[i + 2]
			i += 3
			str_app += s + " " + p + " " + o + " . "

		query_str = "PREFIX dbo: <http://dbpedia.org/ontology/> PREFIX dbp: <http://dbpedia.org/property/> PREFIX foaf: <http://xmlns.com/foaf/0.1/> SELECT distinct " + str(
			obj_head) + " WHERE { " + str_app + " }"

		app = bytes(query_str, 'utf-8')
		query_str = str(app, 'unicode-escape')
		sparql.setQuery(query_str)
		sparql.setReturnFormat(JSON)
		qres = sparql.query().convert()

		for v_res in qres["results"]["bindings"]:
			str_res = "<" + str(v_res[obj_head.replace("?", "")]["value"]) + ">"
			valid_values.add(str_res)

		# se arrivo qui perchè non è corrisposto
		return valid_values

	print("ERROR")
	return None


def boost_fuseky(fact, rule_set, sparql, eligible_rules_for_d):
	score_to_add = 0
	norm_factor = 0

	if len(eligible_rules_for_d) == 0: return 0

	for r in eligible_rules_for_d:
		score_value = get_score(r, rule_set)
		norm_factor += score_value
		outcome = apply_rules_to_f_fuseky(r, fact, sparql)
		if outcome:
			score_to_add += score_value

	overall_score = (1 - (1 / (1 + norm_factor))) * (score_to_add / norm_factor)
	return overall_score


def read_valid_rule_file(path_file):
	valid_rules_for_d = dict()
	f_in = open(path_file, "r")
	for line in f_in:
		line = line.strip().split("\t")
		d = line[0]
		rule = line[1]
		values = line[2].split(" ")
		if d not in valid_rules_for_d:
			valid_rules_for_d[d] = dict()
		valid_rules_for_d[d][rule] = values
	f_in.close()
	return valid_rules_for_d


def read_boost_dict(path_file, sources_dataItemValues, eligible_rules, R):
	valid_rules_for_d = read_valid_rule_file(path_file)
	boost_dict = dict()  # for each fact (d+v) return the boost factor
	cont_ = 0

	for d in sources_dataItemValues:
		cont_ += 1

		if cont_ % 500 == 0:
			print(cont_)
		# initialize for each fact its boost value to 0
		for value in sources_dataItemValues[d]:
			boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + value] = 0

		if d not in eligible_rules or (d in eligible_rules and d not in valid_rules_for_d):
			# the data item has not eligible rule --> boost factor = 0
			continue

		norm_factor = 0
		for rule in eligible_rules[d]:
			score_value = get_score(rule, R)
			norm_factor += score_value

			if rule in valid_rules_for_d[d]:
				for value in valid_rules_for_d[d][rule]:
					if value in sources_dataItemValues[d]:
						boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + value] += score_value

		for value in sources_dataItemValues[d]:
			score_to_add = boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + value]
			overall_score = (1 - (1 / (1 + norm_factor))) * (score_to_add / norm_factor)
			boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + value] = overall_score

	return boost_dict


'''def get_valid_values_fuseky_optimized(truth_, eligible_rules, sparql, output_file_path):
	try:
		cont_ = 0
		f_out_valid = open(output_file_path, "w")

		for d in truth_:
			cont_ += 1
			if cont_ % 500 == 0:
				print(cont_)

			if d not in eligible_rules:  # the data item has not eligible rule --> boost factor = 0
				continue

			for rule in eligible_rules[d]:
				value_set_valid = apply_rules_to_d_fuseky(d, rule, sparql)

				value_out = ""
				for value in value_set_valid:
					value = value[1:-1]
					value_out += value + " "

				if value_out != "":
					app = bytes(value_out[:-1], 'unicode-escape')
					value_out_encoded = str(app, 'utf-8')
					str_out = str(d) + "\t" + str(rule) + "\t" + str(value_out_encoded) + "\n"
					f_out_valid.write(str_out)
					f_out_valid.flush()

		f_out_valid.close()
		return True
	except:
		f_out_valid.close()
		print("Unexpected error:", sys.exc_info()[0])
		return False
'''

def read_valid_values_dict(valid_values_file_):
	valid_values_dict = dict()
	f_in = open(valid_values_file_, "r")

	for line in f_in:
		line = line.strip().split("\t")
		d = line[0]
		r = line[1]
		values_set = line[2]
		app = bytes(values_set,'utf-8')
		values_set = str(app,'unicode-escape')
		values_set = set(values_set.split(" "))
		if d not in valid_values_dict:
			valid_values_dict[d] = dict()
		valid_values_dict[d][r] = values_set

	print("number of data items in valid values for each dataitem - rules dictionary : " + str(len(valid_values_dict)))
	return valid_values_dict


def get_boost_dict_fuseky_optimized(sources_dataItemValues, eligible_rules, R, sparql, f_out_valid_path):
	boost_dict = dict()  # for each fact (d+v) return the boost factor
	cont_ = 0
	f_out_valid = open(f_out_valid_path, "w")
	print("Doing get boost dict fuseky optimized")
	for d in sources_dataItemValues:
		cont_ += 1
		if cont_ % 1000 == 0: print(cont_)
		# initialize for each fact its boost value to 0
		for value in sources_dataItemValues[d]:
			boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + value] = 0

		if d not in eligible_rules:  # the data item has not eligible rule --> boost factor = 0
			continue

		norm_factor = 0
		for rule in eligible_rules[d]:
			value_set_valid = apply_rules_to_d_fuseky(d, rule, sparql)
			score_value = get_score(rule, R)
			norm_factor += score_value

			value_out = ""
			for value in value_set_valid:
				value = value[1:-1]#cut < and >
				if value in sources_dataItemValues[d]:
					boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + value] += score_value
					value_out += value + " "

			if value_out != "":
				str_out = str(d) + "\t" + str(rule) + "\t" + str(value_out[:-1]) + "\n"
				f_out_valid.write(str_out)
				f_out_valid.flush()

		for value in sources_dataItemValues[d]:
			score_to_add = boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + value]
			overall_score = (1 - (1 / (1 + norm_factor))) * (score_to_add / norm_factor)
			boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + value] = overall_score

	f_out_valid.close()

	return boost_dict


def compute_boost_dict(sources_dataItemValues, R_, eligible_rules_, valid_values_for_r_and_d_):
	boost_dict = dict()  # for each fact (d+v) return the boost factor
	cont_ = 0

	for d in sources_dataItemValues:
		cont_ += 1
		if cont_ % 1000 == 0:
			print(cont_)
		# initialize for each fact its boost value to 0
		for value in sources_dataItemValues[d]:
			boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + value] = 0

		if d not in eligible_rules_:  # the data item has not eligible rule --> boost factor = 0
			continue

		norm_factor = 0
		for rule in eligible_rules_[d]:
			value_set_valid = set()
			if d in valid_values_for_r_and_d_:
				if rule in valid_values_for_r_and_d_[d]:
					value_set_valid = valid_values_for_r_and_d_[d][rule]

			score_value = get_score(rule, R_)
			norm_factor += score_value

			for value in value_set_valid:
				if value in sources_dataItemValues[d]:
					boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + value] += score_value

		for value in sources_dataItemValues[d]:
			score_to_add = boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + value]
			overall_score = (1 - (1 / (1 + norm_factor))) * (score_to_add / norm_factor)
			boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + value] = overall_score

	print("Dimension of boost dict " + str(len(boost_dict)))
	return boost_dict

def compute_boost_dict_new_formula(sources_dataItemValues, R_, eligible_rules_, valid_values_for_r_and_d_):
	boost_dict = dict()  # for each fact (d+v) return the boost factor
	cont_ = 0

	for d in sources_dataItemValues:
		cont_ += 1
		if cont_ % 1000 == 0:
			print(cont_)
		# initialize for each fact its boost value to 0
		for value in sources_dataItemValues[d]:
			boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + value] = 0

		if d not in eligible_rules_:  # the data item has not eligible rule --> boost factor = 0
			continue

		norm_factor = 0
		for rule in eligible_rules_[d]:
			value_set_valid = set()
			if d in valid_values_for_r_and_d_:
				if rule in valid_values_for_r_and_d_[d]:
					value_set_valid = valid_values_for_r_and_d_[d][rule]

			score_value = get_score(rule, R_)
			norm_factor += score_value

			for value in value_set_valid:
				if value in sources_dataItemValues[d]:
					boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + value] += 1

		for value in sources_dataItemValues[d]:
			score_to_add = boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + value]
			overall_score = (score_to_add / norm_factor)
			boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + value] = overall_score

	print("Dimension of boost dict " + str(len(boost_dict)))
	return boost_dict


def get_propagated_boost_dict_fuseky_optimized(sources_dataItemValues, eligible_rules, R, valid_values_for_r_and_d_, ancestors_):
	boost_dict = dict()  # for each fact (d+v) return the boost factor
	cont_ = 0
	for d in sources_dataItemValues:
		claims_prop_for_d = set()
		cont_ += 1
		if cont_ % 500 == 0:
			print(cont_)
		#initialize for each fact its boost value to 0
		for value in sources_dataItemValues[d]:
			boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + value] = 0
			for anc in ancestors_[value]:
				boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + anc] = 0
		if d not in eligible_rules: #the data item has not eligible rule --> boost factor = 0
			continue

		norm_factor = 0
		for rule in eligible_rules[d]:
			value_set_valid = set()
			if d in valid_values_for_r_and_d_:
				if rule in valid_values_for_r_and_d_[d]:
					value_set_valid = valid_values_for_r_and_d_[d][rule]

			score_value = get_score(rule, R)
			norm_factor += score_value

			interested_value_where_add = set()
			for value in value_set_valid:
				value = value#[1:-1]
				if value in sources_dataItemValues[d]:
					for anc in ancestors_[value]:
						interested_value_where_add.add(anc)

			for anc in interested_value_where_add:
				boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + anc] += score_value
				claims_prop_for_d.add(d + "<http://dbpedia.org/ontology/birthPlace>" + anc)



		for fact_complete in claims_prop_for_d:
			score_to_add = boost_dict[fact_complete]
			overall_score = (1 - (1 / (1 + norm_factor))) * (score_to_add / norm_factor)
			boost_dict[fact_complete] = overall_score

	return boost_dict

def get_propagated_boost_dict_fuseky_optimized_new_formula(sources_dataItemValues, eligible_rules, R, valid_values_for_r_and_d_, ancestors_):

	boost_dict = dict()  # for each fact (d+v) return the boost factor
	cont_ = 0
	for d in sources_dataItemValues:
		claims_prop_for_d = set()
		cont_ += 1
		if cont_ % 500 == 0:
			print(cont_)
		#initialize for each fact its boost value to 0
		for value in sources_dataItemValues[d]:
			boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + value] = 0
			for anc in ancestors_[value]:
				boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + anc] = 0

		if d not in eligible_rules: #the data item has not eligible rule --> boost factor = 0
			continue

		norm_factor = 0
		number_of_elibible_rules = dict()

		for rule in eligible_rules[d]:
			value_set_valid = set()
			if d in valid_values_for_r_and_d_:
				if rule in valid_values_for_r_and_d_[d]:
					value_set_valid = valid_values_for_r_and_d_[d][rule]

			score_value = get_score(rule, R)
			norm_factor += score_value

			interested_value_where_add = set()
			for value in value_set_valid:
				value = value#[1:-1]
				if value in sources_dataItemValues[d]:
					for anc in ancestors_[value]:
						interested_value_where_add.add(anc)

			for anc in interested_value_where_add:
				boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + anc] += 1
				claims_prop_for_d.add(d + "<http://dbpedia.org/ontology/birthPlace>" + anc)



		for fact_complete in claims_prop_for_d:
			 score_to_add = boost_dict[fact_complete]
			 overall_score = (1 - (1 / (1 + norm_factor))) * (score_to_add / norm_factor)
			 boost_dict[fact_complete] = overall_score


	return boost_dict

# function without fuseky with rdflib
def apply_rules_to_f(r, fact, g):
	subj = fact[0]
	value = fact[2]

	head = (r.split(" => ")[1])
	body = (r.split(" => ")[0])
	obj_head = head.split(" ")[2]
	if (not obj_head.startswith("?")):
		# costante - confronto direttamente
		if value == obj_head:
			# print ("TRUE " + str(r))
			return True
		else:
			# print("FALSE " + str(r))
			return False
	else:
		# faccio query per recuperare tutti i possibili valori dell oggetto per una certa instnziazione delle var
		subj_var = head.split(" ")[0]
		body = body.replace(subj_var, subj)

		r_array = body.split(" ")
		str_app = ""
		i = 0
		while i < len(r_array):
			s = r_array[i]
			p = r_array[i + 1]
			o = r_array[i + 2]
			i += 3
			str_app += s + " " + p + " " + o + " . "

		query_str = "PREFIX dbo: <http://dbpedia.org/ontology/> PREFIX dbp: <http://dbpedia.org/property/> PREFIX foaf: <http://xmlns.com/foaf/0.1/> SELECT distinct " + str(
			obj_head) + " WHERE { " + str_app + " }"

		app = bytes(query_str, 'utf-8')
		query_str = str(app, 'unicode-escape')

		qres = g.query(query_str)
		for v_res in qres:
			str_res = "<" + str(v_res[0]) + ">"
			if value == str_res:
				# print("TRUE " + str(r))
				return True
		# se arrivo qui perchè non è corrisposto
		# print("FALSE " + str(r))
		return False

	print("ERROR")
	return False


def boost(fact, rule_set, g, eligible_rules_for_f):
	score_to_add = 0
	norm_factor = 0

	if len(eligible_rules_for_f) == 0: return 0

	for r in eligible_rules_for_f:
		# print (str(r) + "  " + str(R[r]))
		score_value = get_score(r, rule_set)
		norm_factor += score_value
		outcome = apply_rules_to_f(r, fact, g)
		if outcome:
			score_to_add += score_value
		# print("norm factor " + str(norm_factor))
		# print("score_to add " + str(norm_factor))
		# else:
		#    score_to_subtract += get_score(r, R, KB)
	# print(score_to_add)
	# print(norm_factor)
	# overall_score = ( 1 - ( 1 / norm_factor) ) * ( (score_to_add - score_to_subtract) / norm_factor)
	# overall_score = (1 - (score_to_subtract / (norm_factor))) * ((score_to_add) / norm_factor)
	overall_score = (1 - (1 / (1 + norm_factor))) * (score_to_add / norm_factor)

	return overall_score


def get_boost_dict(sources_dataItemValues, eligible_rules, R, g):
	boost_dict = dict()  # for each fact (d+v) return the boost factor
	for d in sources_dataItemValues:
		eligible_rules_for_d = eligible_rules[d]
		for value in sources_dataItemValues[d]:
			fact = [d, "<http://dbpedia.org/ontology/birthPlace>", value]
			boost_f = boost(fact, R, g, eligible_rules_for_d)
			# add to a dictionary
			boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + value] = boost_f

	return boost_dict


def load_eligible_rules(f_in_eligible_, id_R):
	eligible_rules = dict()

	for line in f_in_eligible_:
		line = line.strip().split("\t")
		d = line[0]  # [1:-1]
		list_of_rules = list()
		for rule_id in line[1].split(" "):
			rule = id_R[int(rule_id)]  # de indenta
			list_of_rules.append(rule)  # de indenta

		if len(list_of_rules) > 0:  #
			eligible_rules[d] = list_of_rules  # de indenta
	f_in_eligible_.close()

	return eligible_rules