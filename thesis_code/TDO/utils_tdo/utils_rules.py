from SPARQLWrapper import SPARQLWrapper, JSON
import copy
import sys
from TDO.utils_tdo import empirical_Bayes


def get_dataitem_with_some_boosting(str_hc_, base_dir_, predicate_):
	dataitem_with_rules = set()
	f_in_eligible = open(base_dir_ + str(predicate_) + "/eligible_rules_hc_" + str(str_hc_) + ".csv", "r")
	for line in f_in_eligible:
		if predicate_ == "genre":
			line = line.strip().split("\\t")
		else:
			line = line.strip().split("\t")
		d = line[0]  # [1:-1]
		dataitem_with_rules.add(d)
	f_in_eligible.close()
	return dataitem_with_rules


def load_rules(file_rules, bayes_score_flag):
	return load_rules_with_threshold(file_rules, 0.00, bayes_score_flag)


def load_rules_with_threshold(file_rules, hc_threshold, bayes_score_flag, file_rules_bayes):
	R = dict()  # dict with key = rule str, values = list with positive example, conf pca, ..,.., and set of atoms of the body
	R_id = dict()  # dict for retriving the id of each rule - note that the id of a rule is its line number in the file of the rules

	header = True
	cont_lines = 0
	f = open(file_rules, "r")
	for line in f:
		cont_lines += 1
		#if cont_lines == 54:
		#	print()
		#if cont_lines % 10000 == 0:
		#	print(cont_lines)
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
				if float(line_arr[1].replace(",", ".")) <= hc_threshold:
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
	f.close()
	R_bayes = dict()
	if bayes_score_flag:
		f = open(file_rules_bayes, "r")
		for line in f:
			line = line.strip().split("\t")
			rule = line[0]
			score_bayes = line[1]
			R_bayes[rule] = float(score_bayes.replace(",", "."))
		f.close()
	print("number of found rules " + str(len(R)))
	return [R, R_id, R_bayes]


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
	PCA_conf = float(metrics[1].replace(",", "."))
	score = (1 - (1 / support)) * PCA_conf  # support = 1 --> it never happens
	'''
	alternativa
	head = (r.split(" => ")[1])
	H_size = get_size(head, KB)
	score = ( support / H_size ) * PCA_conf
	'''
	return score


def get_score_bayes(r, R_bayes):
	score = R_bayes[r] # support = 1 --> it never happens
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
def get_eligible_rules_fuseky_optimized_person(R, sparql, D_, predicate_):
	eligible_rules_ = dict()
	dataitem_set = set(D_)

	str_dataitems_1 = ""
	str_dataitems_2 = ""
	cont_d = 0
	for d in dataitem_set:
		#str_dataitems += "<" + str(d) + ">, "
		cont_d += 1
		if cont_d > 5000:
			str_dataitems_2 += "(<" + str(d) + ">) "
		else:
			str_dataitems_1 += "(<" + str(d) + ">) "
	#str_dataitems = str_dataitems[:-2]

	cont = 0
	for rule in R:
		cont += 1
		if cont % 1 == 0:
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

				#query_str = "PREFIX dbo: <http://dbpedia.org/ontology/> PREFIX dbp: <http://dbpedia.org/property/> PREFIX foaf: <http://xmlns.com/foaf/0.1/> SELECT distinct " + str(subj_head) + " WHERE { " + str(str_app) #+ " }"
				#query_str += " VALUES (?a) {" + str(str_dataitems) + "}"
				query_str = "PREFIX dbo: <http://dbpedia.org/ontology/> PREFIX dbp: <http://dbpedia.org/property/> PREFIX foaf: <http://xmlns.com/foaf/0.1/> SELECT distinct " + str(
					subj_head) + " WHERE { VALUES (?a) {" + str(str_dataitems_1) + "} " + str(str_app)  # + " }"

				query_str = query_str + " }"
				app = bytes(query_str, 'utf-8')
				query_str = str(app, 'unicode-escape')

				sparql.setQuery(str(query_str))
				sparql.setReturnFormat(JSON)
				qres = sparql.query().convert()

				res_set = set()
				for v_res in qres["results"]["bindings"]:
					str_res = str(v_res[subj_head.replace("?", "")]["value"])
					res_set.add(str_res)

				#second part
				query_str = "PREFIX dbo: <http://dbpedia.org/ontology/> PREFIX dbp: <http://dbpedia.org/property/> PREFIX foaf: <http://xmlns.com/foaf/0.1/> SELECT distinct " + str(
					subj_head) + " WHERE { VALUES (?a) {" + str(str_dataitems_2) + "} " + str(str_app)  # + " }"

				query_str = query_str + " }"
				app = bytes(query_str, 'utf-8')
				query_str = str(app, 'unicode-escape')

				sparql.setQuery(str(query_str))
				sparql.setReturnFormat(JSON)
				qres = sparql.query().convert()

				for v_res in qres["results"]["bindings"]:
					str_res = str(v_res[subj_head.replace("?", "")]["value"])
					res_set.add(str_res)
				##

				#intersection_set = dataitem_set.intersection(res_set)
				intersection_set = res_set

				for d in intersection_set:
					if d not in eligible_rules_:
						eligible_rules_[d] = list()
					eligible_rules_[d].append(rule)

			else:
				# il soggetto nella testa non è una variable
				# dovrei controllare verifico che il body sia elegible senza fare il replacement della variable con il soggetto del mio fatto
				# visto che è una regola sara sicuramente verificato e quindi lo metto eligible
				eligible_rules_[subj_head.replace("<", "").replace(">", "")].append(rule)

	return eligible_rules_


def get_eligible_rules_fuseky_optimized(R, sparql, truth_, predicate_):
	eligible_rules_ = dict()
	dataitem_set = set(truth_.keys())

	str_dataitems_1 = ""
	str_dataitems_2 = ""
	cont_d = 0
	for d in dataitem_set:
		#str_dataitems += "<" + str(d) + ">, "
		cont_d += 1
		if cont_d > 5000:
			str_dataitems_2 += "(<" + str(d) + ">) "
		else:
			str_dataitems_1 += "(<" + str(d) + ">) "
	#str_dataitems = str_dataitems[:-2]

	cont = 0
	for rule in R:
		cont += 1
		if cont % 1 == 0:
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

				#query_str = "PREFIX dbo: <http://dbpedia.org/ontology/> PREFIX dbp: <http://dbpedia.org/property/> PREFIX foaf: <http://xmlns.com/foaf/0.1/> SELECT distinct " + str(subj_head) + " WHERE { " + str(str_app) #+ " }"
				#query_str += " VALUES (?a) {" + str(str_dataitems) + "}"
				query_str = "PREFIX dbo: <http://dbpedia.org/ontology/> PREFIX dbp: <http://dbpedia.org/property/> PREFIX foaf: <http://xmlns.com/foaf/0.1/> SELECT distinct " + str(
					subj_head) + " WHERE { VALUES (?a) {" + str(str_dataitems_1) + "} " + str(str_app)  # + " }"

				query_str = query_str + " }"
				app = bytes(query_str, 'utf-8')
				query_str = str(app, 'unicode-escape')

				sparql.setQuery(str(query_str))
				sparql.setReturnFormat(JSON)
				qres = sparql.query().convert()

				res_set = set()
				for v_res in qres["results"]["bindings"]:
					str_res = str(v_res[subj_head.replace("?", "")]["value"])
					res_set.add(str_res)

				#second part
				query_str = "PREFIX dbo: <http://dbpedia.org/ontology/> PREFIX dbp: <http://dbpedia.org/property/> PREFIX foaf: <http://xmlns.com/foaf/0.1/> SELECT distinct " + str(
					subj_head) + " WHERE { VALUES (?a) {" + str(str_dataitems_2) + "} " + str(str_app)  # + " }"

				query_str = query_str + " }"
				app = bytes(query_str, 'utf-8')
				query_str = str(app, 'unicode-escape')

				sparql.setQuery(str(query_str))
				sparql.setReturnFormat(JSON)
				qres = sparql.query().convert()

				for v_res in qres["results"]["bindings"]:
					str_res = str(v_res[subj_head.replace("?", "")]["value"])
					res_set.add(str_res)
				##

				#intersection_set = dataitem_set.intersection(res_set)
				intersection_set = res_set

				for d in intersection_set:
					if d not in eligible_rules_:
						eligible_rules_[d] = list()
					eligible_rules_[d].append(rule)

			else:
				# il soggetto nella testa non è una variable
				# dovrei controllare verifico che il body sia elegible senza fare il replacement della variable con il soggetto del mio fatto
				# visto che è una regola sara sicuramente verificato e quindi lo metto eligible
				eligible_rules_[subj_head.replace("<", "").replace(">", "")].append(rule)

	return eligible_rules_

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


def get_valid_values_fuseky_optimized(truth_, eligible_rules, sparql, output_file_path):
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

def read_valid_values_dict_real_world(valid_values_file_):
	valid_values_dict = dict()
	f_in = open(valid_values_file_, "r")

	for line in f_in:
		line = line.strip().split("\t")
		d = line[0].replace("http://dbpedia.org/resource/", "").replace("_", " ") + " AND was born"
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

def compute_boost_dict_EBS_score(sources_dataItemValues, R_, eligible_rules_, valid_values_for_r_and_d_):
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

			score_value = R_[rule]
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

def compute_boost_dict_EBS(sources_dataItemValues, R_, eligible_rules_, valid_values_for_r_and_d_):
	boost_dict = dict()  # for each fact (d+v) return the boost factor
	cont_ = 0

	claims_list = list()
	verified_rules_list = list()
	eligible_rules_list = list()

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

			score_value = R_[rule]
			norm_factor += score_value

			for value in value_set_valid:
				if value in sources_dataItemValues[d]:
					boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + value] += score_value

		for value in sources_dataItemValues[d]:
			fact_complete = d + "<http://dbpedia.org/ontology/birthPlace>" + value
			score_to_add = boost_dict[fact_complete]
			claims_list.append(fact_complete)
			verified_rules_list.append(score_to_add)
			eligible_rules_list.append(norm_factor)
		##

	import pandas as pd
	from rpy2.robjects import pandas2ri
	pandas2ri.activate()

	print("define function in R")
	r_src_bayes = """ function(dataf, col_name_to_select){
						library(dplyr)
						library(tidyr)
						library(ggplot2)
						library(ebbr)
												
						prior <- dataf %>% ebb_fit_prior(est_positive, est_total, method="mm")
						alpha0 <- tidy(prior)$alpha
						beta0 <- tidy(prior)$beta
						print(alpha0)
						print(beta0)
							augmented_prior <- (augment(prior, data = dataf))

							result_augmented <- select(augmented_prior, col_name_to_select, .fitted)
							}
					"""

	import rpy2.robjects as ro
	print("step 1 ")
	r_funct = ro.r(r_src_bayes)
	print("step 2 ")
	df = pd.DataFrame({
			'sources_list': claims_list,
			'est_positive': verified_rules_list,
			'est_total': eligible_rules_list
	})
	# print("--- %s seconds to create data frame ---" % (time.time() - start_time))
	# print(df)
	print("step 3 ")
	# convert the format of dataframe from py to R
	# start_time = time.time()
	dataf = pandas2ri.py2ri(df)
	# print("--- %s seconds to convert data frame in R format ---" % (time.time() - start_time))
	# launch R function for estimating the new posteriori		# start_time = time.time()
	print("step 4 ")
	augment_prior = r_funct(dataf, 'sources_list')
	# print("--- %s seconds to execute R function ---" % (time.time() - start_time))
	# convert the format of dataframe from R to py
	# start_time = time.time()
	print("step 5 ")
	augment_prior = pandas2ri.ri2py(augment_prior)
	# print("--- %s seconds to reconvert data frame in PY format ---" % (time.time() - start_time))
	# re-assigne the new confidence level to each C[d+v]
	# start_time = time.time()
	print("step 6 ")
	R_bayes_score = augment_prior.set_index('sources_list').to_dict()
	boost_dict_app = R_bayes_score['.fitted']

	for fact_complete in boost_dict_app:
		boost_dict[fact_complete] = boost_dict_app[fact_complete]

	print("Dimension of boost dict " + str(len(boost_dict)))
	return boost_dict


def get_propagated_boost_dict_fuseky_optimized(sources_dataItemValues, eligible_rules, R, valid_values_for_r_and_d_, ancestors_, bayes_score):

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
			if value not in ancestors_:
				print(d)
			for anc in ancestors_[value]:
				boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + anc] = 0
				if value == "http://dbpedia.org/resource/Byzantine_Empire":
					print(anc)
					print(boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + anc])
					print("----")

		if d not in eligible_rules: #the data item has not eligible rule --> boost factor = 0
			continue

		norm_factor = 0
		for rule in eligible_rules[d]:
			value_set_valid = set()
			if d in valid_values_for_r_and_d_:
				if rule in valid_values_for_r_and_d_[d]:
					value_set_valid = valid_values_for_r_and_d_[d][rule]

			if bayes_score:
				score_value = R[rule]
			else:
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
			if bayes_score:
				overall_score = (score_to_add / norm_factor)
			else:
				overall_score = (1 - (1 / (1 + norm_factor))) * (score_to_add / norm_factor)
			boost_dict[fact_complete] = overall_score


	return boost_dict


def get_propagated_boost_dict_fuseky_optimized_BAYES(sources_dataItemValues, eligible_rules, R, valid_values_for_r_and_d_, ancestors_, bayes_score):

	boost_dict_app = dict()  # for each fact (d+v) return the boost factor
	boost_dict = dict()
	cont_ = 0

	claims_list = list()
	verified_rules_list= list()
	eligible_rules_list= list()

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

			if bayes_score:
				score_value = R[rule]
			else:
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
			if bayes_score:
				if norm_factor != 0:
					claims_list.append(fact_complete)
					verified_rules_list.append(score_to_add)
					eligible_rules_list.append(norm_factor)
			else:
				overall_score = (1 - (1 / (1 + norm_factor))) * (score_to_add / norm_factor)

	import pandas as pd
	from rpy2.robjects import pandas2ri
	pandas2ri.activate()

	print("define function in R")
	r_src_bayes = """ function(dataf, col_name_to_select){
						library(dplyr)
						library(tidyr)
						library(ggplot2)
						library(ebbr)

						prior <- dataf %>% ebb_fit_prior(est_positive, est_total, method="mm")
						alpha0 <- tidy(prior)$alpha
						beta0 <- tidy(prior)$beta
						print(alpha0)
						print(beta0)
							augmented_prior <- (augment(prior, data = dataf))

							result_augmented <- select(augmented_prior, col_name_to_select, .fitted)
							}
					"""

	import rpy2.robjects as ro
	print("step 1 ")
	r_funct = ro.r(r_src_bayes)
	print("step 2 ")
	df = pd.DataFrame({
			'sources_list': claims_list,
			'est_positive': verified_rules_list,
			'est_total': eligible_rules_list
	})
	# print("--- %s seconds to create data frame ---" % (time.time() - start_time))
	# print(df)
	print("step 3 ")
	# convert the format of dataframe from py to R
	# start_time = time.time()
	dataf = pandas2ri.py2ri(df)
	# print("--- %s seconds to convert data frame in R format ---" % (time.time() - start_time))
	# launch R function for estimating the new posteriori		# start_time = time.time()
	print("step 4 ")
	augment_prior = r_funct(dataf, 'sources_list')
	# print("--- %s seconds to execute R function ---" % (time.time() - start_time))
	# convert the format of dataframe from R to py
	# start_time = time.time()
	print("step 5 ")
	augment_prior = pandas2ri.ri2py(augment_prior)
	# print("--- %s seconds to reconvert data frame in PY format ---" % (time.time() - start_time))
	# re-assigne the new confidence level to each C[d+v]
	# start_time = time.time()
	print("step 6 ")
	R_bayes_score = augment_prior.set_index('sources_list').to_dict()
	boost_dict_app = R_bayes_score['.fitted']

	for fact_complete in boost_dict_app:
		boost_dict[fact_complete] = boost_dict_app[fact_complete]

	return boost_dict


def get_propagated_boost_dict_fuseky_optimized_JSE(sources_dataItemValues, eligible_rules, R, valid_values_for_r_and_d_, ancestors_, bayes_score):
	boost_dict = dict()
	cont_ = 0

	claims_list = list()
	proportion_rules_list= list()

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

			if bayes_score:
				score_value = R[rule]
			else:
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
			score_boost = score_to_add/norm_factor
			if norm_factor != 0:
				for rule in eligible_rules[d]:
					claims_list.append(fact_complete)
					proportion_rules_list.append(score_boost)

	import pandas as pd
	from rpy2.robjects import pandas2ri
	pandas2ri.activate()

	print("step 2 ")
	df = pd.DataFrame({
			'sources_list': claims_list,
			'est_positive': proportion_rules_list
	})
	print("step 3 ")
	# convert the format of dataframe from py to R
	# start_time = time.time()
	stats_mss_js = empirical_Bayes.multi_sample_size_js_estimator(df, group_id_col='sources_list', data_col='est_positive', pooled=False)

	boost_dict_app = stats_mss_js.to_dict()
	#boost_dict_app = R_bayes_score['.fitted']

	for fact_complete in boost_dict_app:
		boost_dict[fact_complete] = boost_dict_app[fact_complete]

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


def compute_bayes_score_rules(file_rules, hc_threshold):
	R_bayes_score_app = dict()  # dict with key = rule str, values = list with positive example, conf pca, ..,.., and set of atoms of the body
	R_id_bayes = dict()  # dict for retriving the id of each rule - note that the id of a rule is its line number in the file of the rules

	rules_list = list()
	positive_cases_list = list()
	tot_cases_list = list()

	header = True
	cont_lines = 0
	f = open(file_rules, "r")
	for line in f:
		cont_lines += 1
		#if cont_lines == 54:
		#	print()
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
				if float(line_arr[1].replace(",", ".")) <= hc_threshold:
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

				R_id_bayes[r] = cont_lines
				# support, PCA conf, Std conf, head coverage + bodyseet
				tot_cases = int(round(float(line_arr[4]) / float(line_arr[3].replace(",", "."))))
				R_bayes_score_app[r] = [line_arr[4], tot_cases]
				rules_list.append(r)
				positive_cases_list.append(float(line_arr[4]))
				tot_cases_list.append(tot_cases)

	print("number of found rules " + str(len(R_bayes_score_app)))
	import pandas as pd
	from rpy2.robjects import pandas2ri
	pandas2ri.activate()

	print("define function in R")
	r_src_bayes = """ function(dataf, col_name_to_select){
				library(dplyr)
				library(tidyr)
				library(ggplot2)
				library(ebbr)
	
				p <-  ggplot(filter(dataf, est_positive > 0), aes(est_positive / est_total))
				p <- p + geom_histogram()
				ggsave(filename="a_score.jpg", plot=p)
						
				prior <- dataf %>% ebb_fit_prior(est_positive, est_total, method="mm")
				alpha0 <- tidy(prior)$alpha
				beta0 <- tidy(prior)$beta
				print(alpha0)
				print(beta0)
					augmented_prior <- (augment(prior, data = dataf))

					result_augmented <- select(augmented_prior, col_name_to_select, .fitted)
					}
			"""
	import rpy2.robjects as ro
	print("step 1 ")
	r_funct = ro.r(r_src_bayes)
	# r_funct_2 = ro.r(r_src_2)
	# define list of d+v (in order to keep always the same order)
	print("step 2 ")
	df = pd.DataFrame({
		'sources_list': rules_list,
		'est_positive': positive_cases_list,
		'est_total': tot_cases_list
	})
	# print("--- %s seconds to create data frame ---" % (time.time() - start_time))
	# print(df)
	print("step 3 ")
	# convert the format of dataframe from py to R
	# start_time = time.time()
	dataf = pandas2ri.py2ri(df)
	# print("--- %s seconds to convert data frame in R format ---" % (time.time() - start_time))
	# launch R function for estimating the new posteriori
	# start_time = time.time()
	print("step 4 ")
	augment_prior = r_funct(dataf, 'sources_list')
	# print("--- %s seconds to execute R function ---" % (time.time() - start_time))
	# convert the format of dataframe from R to py
	# start_time = time.time()
	print("step 5 ")
	augment_prior = pandas2ri.ri2py(augment_prior)
	# print("--- %s seconds to reconvert data frame in PY format ---" % (time.time() - start_time))
	# re-assigne the new confidence level to each C[d+v]
	# start_time = time.time()
	print("step 6 ")
	R_bayes_score = augment_prior.set_index('sources_list').to_dict()
	R_bayes_score = R_bayes_score['.fitted']
	#f_out = open("D:\\prova_bayes_rules_mle.out", "w")
	f_out = open("D:\\prova_bayes_rules_genre.out", "w")
	print("dimension of " + str(len(R_bayes_score)))
	for r in R_bayes_score:
		f_out.write(str(r) + "\t" + str(R_bayes_score[r]) + "\n")
	# print("--- %s seconds to reassigned the normalized trustowrhtiness ---" % (time.time() - start_time))
	f_out.close()
	return [R_bayes_score, R_id_bayes]


def compute_bayes_score_rules_mixure(file_rules, hc_threshold):
	R_bayes_score_app = dict()  # dict with key = rule str, values = list with positive example, conf pca, ..,.., and set of atoms of the body
	R_id_bayes = dict()  # dict for retriving the id of each rule - note that the id of a rule is its line number in the file of the rules

	rules_list = list()
	positive_cases_list = list()
	tot_cases_list = list()

	header = True
	cont_lines = 0
	f = open(file_rules, "r")
	for line in f:
		cont_lines += 1
		# if cont_lines == 54:
		#	print()
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
				if float(line_arr[1].replace(",", ".")) <= hc_threshold:
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

				R_id_bayes[r] = cont_lines
				# support, PCA conf, Std conf, head coverage + bodyseet
				tot_cases = int(round(float(line_arr[4]) / float(line_arr[3].replace(",", "."))))
				R_bayes_score_app[r] = [line_arr[4], tot_cases]
				rules_list.append(r)
				positive_cases_list.append(float(line_arr[4]))
				tot_cases_list.append(tot_cases)

	print("number of found rules " + str(len(R_bayes_score_app)))
	import pandas as pd
	from rpy2.robjects import pandas2ri
	pandas2ri.activate()

	print("define function in R")
	r_src_bayes = """ function(dataf, col_name_to_select){
				library(dplyr)
				library(tidyr)
				library(ggplot2)
				library(ebbr)

				p <-  ggplot(filter(dataf, est_positive > 0), aes(est_positive / est_total))
				p <- p + geom_histogram()
				ggsave(filename="a_score.jpg", plot=p)

				prior <- ebb_fit_mixture(dataf, est_positive, est_total, clusters = 2,method = "mle")
				setprior <- tidy(prior)
				cl1Distr <- filter(setprior, setprior$cluster == "1")
				cl1Distr <- select(cl1Distr, alpha, beta)
				print(cl1Distr)
				# assignments of points to clusters
				dataTo <- prior$assignments
				print(dataTo)
				cl1Data <- filter(dataTo, .cluster == "1")
				
				print(cl1Data)		
				cl1Data <- select(cl1Data, sources_list, est_positive, est_total)	
				print(cl1Data)		
				
				
					}
			"""
	import rpy2.robjects as ro
	print("step 1 ")
	r_funct = ro.r(r_src_bayes)
	# r_funct_2 = ro.r(r_src_2)
	# define list of d+v (in order to keep always the same order)
	print("step 2 ")
	df = pd.DataFrame({
		'sources_list': rules_list,
		'est_positive': positive_cases_list,
		'est_total': tot_cases_list
	})
	# print("--- %s seconds to create data frame ---" % (time.time() - start_time))
	# print(df)
	print("step 3 ")
	# convert the format of dataframe from py to R
	# start_time = time.time()
	dataf = pandas2ri.py2ri(df)
	# print("--- %s seconds to convert data frame in R format ---" % (time.time() - start_time))
	# launch R function for estimating the new posteriori
	# start_time = time.time()
	print("step 4 ")
	augment_prior = r_funct(dataf, 'sources_list')
	# print("--- %s seconds to execute R function ---" % (time.time() - start_time))
	# convert the format of dataframe from R to py
	# start_time = time.time()
	print("step 5 ")
	augment_prior = pandas2ri.ri2py(augment_prior)
	# print("--- %s seconds to reconvert data frame in PY format ---" % (time.time() - start_time))
	# re-assigne the new confidence level to each C[d+v]
	# start_time = time.time()
	print("step 6 ")
	R_bayes_score = augment_prior.set_index('sources_list').to_dict()
	R_bayes_score = R_bayes_score['.fitted']
	# f_out = open("D:\\prova_bayes_rules_mle.out", "w")
	f_out = open("D:\\prova_bayes_rules_birthPlace_new_esay.out", "w")
	print("dimension of " + str(len(R_bayes_score)))
	for r in R_bayes_score:
		f_out.write(str(r) + "\t" + str(R_bayes_score[r]) + "\n")
	# print("--- %s seconds to reassigned the normalized trustowrhtiness ---" % (time.time() - start_time))
	f_out.close()
	return [R_bayes_score, R_id_bayes]

if __name__ == '__main__':
	MTD_pc = True
	if MTD_pc:
		str_ext = "data_VALE"

	rule_path = "D:\\"+ str(str_ext) + "\\dbpedia/genre_rules_ok.out"
	#rule_path = "D:/dbpedia/KB_tot.birthplace.out"

	# rule_path = "D:/Vale/Downloads/genre_rules_ok.out"
	#compute_bayes_score_rules_mixure(rule_path, 0)
	#exit()
	load_rules_results = compute_bayes_score_rules(rule_path, 0)
	print("OK")