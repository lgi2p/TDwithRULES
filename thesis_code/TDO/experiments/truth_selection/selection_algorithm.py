import sys

from TDO.experiments.truth_selection import adapted_model_selection
from TDO.utils_tdo import utils_taxonomy


def compute_trad_performance_final(predicate_info_local, conf_trad_model, sources_dataitem_values_local, k_expected):
	# function that select the solution given by traditional model
	# it takes has solution the K values with the highest confidence
	# (0) for each data item :
	#        (1) it creates a dict containing only the value associated to it <key = value, value= confidence for that value>
	#		 (2) it ordered -in descending ordering - reverse order - the dict w.r.t. the confidence values
	#        (3) takes as solution the first K elemement in the ordered array
	try:
		####initiliazation predicate and its information
		ground = predicate_info_local[7]
		tot_n_dataitems = len(predicate_info_local[8])

		cont_d = 0
		solution_dict = dict()
		for d in sources_dataitem_values_local:
			domain_conf_dict = dict()
			for value in sources_dataitem_values_local[d]:
				domain_conf_dict[value] = conf_trad_model[d + value]
			# ordering the list
			rank_list = sorted(domain_conf_dict, key=domain_conf_dict.__getitem__, reverse=True)
			rank_list = rank_list[0:k_expected]
			# no filter is apply, but it is done to maintain coerency in code writing for the compute_adapt_performance function
			filtered_rank_list = rank_list

			solution_dict[d] = filtered_rank_list

			cont_d += 1
			if cont_d % 2000 == 0:
				print("processed data items  " + str(cont_d) + "/" + str(tot_n_dataitems))

		return solution_dict
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise
		exit()


def filter_on_confidence_threshold(d_, conf_adapt_, v_star_temp_, threshold_):
	to_remove = set()
	for item in v_star_temp_:
		if conf_adapt_[d_+item] <= threshold_:
			to_remove.add(item)

	for item in to_remove:
		v_star_temp_.remove(item)

	return v_star_temp_


def compute_solution_best_children_final(predicate_info, conf_adapt, conf_adapt_norm, trust_average_adapt, is_coherent, k_expected, first_ranking_criteria, second_ranking_criteria):
	is_coherent = True
	try:
		threshold_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5]#, 0.0001, 0.001, 0.005, 0.01, 0.1]

		####initiliazation predicate and its information
		children = predicate_info[0]
		print("number of children " + str(len(children)))
		incl_descendants = predicate_info[1]
		print("number of descendants " + str(len(incl_descendants)))
		incl_ancestors = predicate_info[2]
		print("number of ancestors " + str(len(incl_ancestors)))
		root_element = predicate_info[4]
		ic_values = predicate_info[6]
		ground = predicate_info[7]
		dataitems = predicate_info[8]
		print("ic values loaded, number of instances " + str(len(ic_values)))

		cont_d = 0
		dict_solution_TRUST = dict()
		dict_solution_IC = dict()
		for threshold_index in range(0, len(threshold_list)):
			threshold = threshold_list[threshold_index]
			dict_solution_TRUST[threshold] = dict()
			dict_solution_IC[threshold] = dict()

		for d in dataitems:
			#if d.startswith("http://dbpedia.org/resource/El_Coraz"):
			#	print()
			# print("Start selection procedure: ")
			#for best_children -- greedy procedure
			v_star_temp = adapted_model_selection.selection_phase(d, conf_adapt_norm, 0, 0, children, incl_ancestors, root_element)

			# print("Start ranking procedure: ")
			if len(v_star_temp) == 1: ##note that the selection procedure returns at least the root elements
				element = v_star_temp.pop()
				if element == root_element:
					if d + element not in conf_adapt:
						continue
					# there is no claims on this dataitem
					else:
						v_star_temp.add(element)
				else:
					v_star_temp.add(element)

			for threshold_index in range(0, len(threshold_list)):
				threshold = threshold_list[threshold_index]
				v_star_temp = filter_on_confidence_threshold(d, conf_adapt_norm, v_star_temp, threshold)

				rank_list_firs_Rank = adapted_model_selection.ranking_phase(d, first_ranking_criteria, second_ranking_criteria,
															   v_star_temp, ic_values, trust_average_adapt)

				# print("Start filterning procedure: ")
				if len(rank_list_firs_Rank) == 0:
					filtered_rank_list = list()
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants, incl_ancestors,
																				 rank_list_firs_Rank, k_expected)


				dict_solution_IC[threshold][d] = filtered_rank_list
					####
				rank_list_second_Rank = adapted_model_selection.ranking_phase(d, second_ranking_criteria, first_ranking_criteria,
																			v_star_temp, ic_values, trust_average_adapt)
				if len(rank_list_second_Rank) == 0:
					filtered_rank_list = list()
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants,
																			 incl_ancestors,
																			 rank_list_second_Rank, k_expected)

				dict_solution_TRUST[threshold][d] = filtered_rank_list

			cont_d += 1
			if cont_d % 2000 == 0:
				print("processed data items  " + str(cont_d) + "/" + str(len(dataitems)))

		return [dict_solution_IC, dict_solution_TRUST]
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise
		exit()


def compute_solution_all_children_final(predicate_info, conf_adapt, conf_adapt_norm, trust_average_adapt, k_expected, first_ranking_criteria, second_ranking_criteria, sources_dataitem_values_prop, threshold_list):
	is_coherent = False
	try:
		#threshold_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5]#, 0.0001, 0.001, 0.005, 0.01, 0.1]

		####initiliazation predicate and its information
		#children = predicate_info[0]
		#print("number of children " + str(len(children)))
		incl_descendants = predicate_info[1]
		print("number of descendants " + str(len(incl_descendants)))
		incl_ancestors = predicate_info[2]
		print("number of ancestors " + str(len(incl_ancestors)))
		root_element = predicate_info[4]
		ic_values = predicate_info[6]
		#ground = predicate_info[7]
		dataitems = predicate_info[8]
		print("ic values loaded, number of instances " + str(len(ic_values)))

		cont_d = 0
		dict_solution_TRUST = dict()
		dict_solution_IC = dict()

		for threshold_index in range(0, len(threshold_list)):
			threshold = threshold_list[threshold_index]
			dict_solution_TRUST[threshold] = dict()
			dict_solution_IC[threshold] = dict()

		for d in dataitems:
			# print("Start selection procedure: ")
			#for allt_children -- selects sets of alternatives
			if d not in sources_dataitem_values_prop:
				continue
			for threshold_index in range(0, len(threshold_list)):
				threshold = threshold_list[threshold_index]
				copy_ancestors = dict()
				for item in sources_dataitem_values_prop[d]:
					if conf_adapt_norm[d + item] > threshold:
						copy_ancestors[item] = incl_ancestors[item]
				g = utils_taxonomy.loadGraphOfURIs(copy_ancestors)
				v_star_temp = utils_taxonomy.return_leaves(g)

				# print("Start ranking procedure: ")
				if len(v_star_temp) == 1: ##note that the selection procedure returns at least the root elements
					element = v_star_temp.pop()
					if element == root_element:
						if d + element not in conf_adapt:
							continue
						# there is no claims on this dataitem
						else:
							v_star_temp.add(element)
					else:
						v_star_temp.add(element)

				rank_list_firs_Rank = adapted_model_selection.ranking_phase(d, first_ranking_criteria, second_ranking_criteria,
																   v_star_temp, ic_values, trust_average_adapt)

				# print("Start filterning procedure: ")
				if len(rank_list_firs_Rank) == 0:
					filtered_rank_list = list()
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants, incl_ancestors,
																					 rank_list_firs_Rank, k_expected)

				dict_solution_IC[threshold][d] = filtered_rank_list
						####
				rank_list_second_Rank = adapted_model_selection.ranking_phase(d, second_ranking_criteria, first_ranking_criteria,
																				v_star_temp, ic_values, trust_average_adapt)
				if len(rank_list_second_Rank) == 0:
					filtered_rank_list = list()
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants,
																				 incl_ancestors,
																				 rank_list_second_Rank, k_expected)

				dict_solution_TRUST[threshold][d] = filtered_rank_list

			cont_d += 1
			if cont_d % 2000 == 0:
				print("processed data items  " + str(cont_d) + "/" + str(len(dataitems)))

		return [dict_solution_IC, dict_solution_TRUST]
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise
		exit()

