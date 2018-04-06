import sys
import copy
import os
cwd = os.getcwd()
if ("TDO") in cwd:
	from TDO.experiments.truth_selection import adapted_model_selection
	from TDO.utils_tdo import utils_taxonomy
	from TDO.utils_tdo import utils_writing_results
else:
	sys.path.append('D:/Dropbox/thesis_code/TDO')
	from experiments.truth_selection import adapted_model_selection
	from utils_tdo import utils_taxonomy
	from utils_tdo import utils_writing_results

def compute_trad_solution_for_dataset(predicate_info_local, conf_trad_model, sources_dataitem_values_local, k_expected):
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
			rank_list = rank_list[0]
			# no filter is apply, but it is done to maintain coerency in code writing for the compute_adapt_performance function
			filtered_rank_list = rank_list

			solution_dict[d] = filtered_rank_list

			cont_d += 1
			if cont_d % 1000 == 0:
				print("processed data items  " + str(cont_d) + "/" + str(tot_n_dataitems))

		# calculating performance for this dataset -- Precision Recall f1 accuracy

		return solution_dict
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise
		exit()

def compute_trad_solution(predicate_info_local, conf_trad_model, sources_dataitem_values_local):
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
			rank_list = rank_list[0]
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


def compute_trad_performance_for_dataset(predicate_info_local, conf_trad_model, sources_dataitem_values_local, k_expected):
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
			if cont_d % 1000 == 0:
				print("processed data items  " + str(cont_d) + "/" + str(tot_n_dataitems))

		# calculating performance for this dataset -- Precision Recall f1 accuracy
		performances_trad_model = performance_measures.get_complete_performance_measures_at_k_1(solution_dict, ground, sources_dataitem_values_local)

		return performances_trad_model
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise
		exit()

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

def compute_trad_performance_for_dataset_writing(predicate_info_local, conf_trad_model, sources_dataitem_values_local, k_expected):
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
			if cont_d % 1000 == 0:
				print("processed data items  " + str(cont_d) + "/" + str(tot_n_dataitems))

		#writing solution on file
		utils_writing_results.writing_sol_dictionary("estimation_rules/trad_sol.csv", solution_dict)

		# calculating performance for this dataset -- Precision Recall f1 accuracy
		performances_trad_model = performance_measures.get_complete_performance_measures_at_k_1(solution_dict, ground, sources_dataitem_values_local)

		return performances_trad_model
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise
		exit()


def filter_on_confidence_threshold(d_, conf_adapt_, v_star_temp_, threshold_):
	to_remove = set()
	for item in v_star_temp_:
		#print(" -- " + str(conf_adapt_[d_+item]))
		if conf_adapt_[d_+item] < threshold_:
			to_remove.add(item)

	for item in to_remove:
		v_star_temp_.remove(item)

	return v_star_temp_


def compute_adapt_solution_for_dataset_with_threshold_optimized_greedy(predicate_info, conf_adapt, trust_average_adapt, is_coherent, threshold_list, delta, k_expected, first_ranking_criteria, second_ranking_criteria, sources_dataitem_values):

	try:
		root_element = predicate_info[4]
		threshold_list = [0]#, 0.0001, 0.001, 0.005, 0.01, 0.1]

		####initiliazation predicate and its information
		children = predicate_info[0]
		print("number of children " + str(len(children)))
		incl_descendants = predicate_info[1]
		print("number of descendants " + str(len(incl_descendants)))
		incl_ancestors = predicate_info[2]
		print("number of ancestors " + str(len(incl_ancestors)))
		ic_values = predicate_info[6]
		ground = predicate_info[7]
		dataitems = predicate_info[8]
		print("ic values loaded, number of instances " + str(len(ic_values)))

		cont_d = 0
		sol_dict = dict()
		for d in dataitems:
			# print("Start selection procedure: ")
			if d not in sources_dataitem_values:
				continue

			copy_ancestors = dict()
			for item in sources_dataitem_values[d]:
				if conf_adapt[d + item] > 0:
					copy_ancestors[item] = incl_ancestors[item]
					for anc in incl_ancestors[item]:
						copy_ancestors[anc] = incl_ancestors[anc]

			for threshold_index in range(0, len(threshold_list)):
				threshold = threshold_list[threshold_index]
				copy_ancestors_list = list(copy_ancestors)
				for item in copy_ancestors_list:
					if conf_adapt[d+item] <= threshold:
						del copy_ancestors[item]

				g = utils_taxonomy.loadGraphOfURIs(copy_ancestors)
				g_red = utils_taxonomy.perform_transitive_reduction(g)
				children_d = utils_taxonomy.reverse_transitive_reduction(g_red)
				if root_element not in children_d.nodes:
					v_star_temp = set()
				else:
					v_star_temp = adapted_model_selection.selection_phase_for_delta_0(d, conf_adapt, 0, delta, children_d,
															   incl_ancestors, root_element)

				rank_list_firs_Rank = adapted_model_selection.ranking_phase(d, first_ranking_criteria, second_ranking_criteria,
															   v_star_temp, ic_values, trust_average_adapt)

				# print("Start filterning procedure: ")
				if len(rank_list_firs_Rank) == 0:
					sol_dict[d] = None
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants, incl_ancestors,
																				 rank_list_firs_Rank, k_expected)
					# if len(filtered_rank_list) == 0:
					#	cont_min += 1
					sol_dict[d] = filtered_rank_list[0]
					####

			cont_d += 1
			if cont_d % 100 == 0:
				print("processed data items  " + str(cont_d) + "/" + str(len(dataitems)))

		# calculating performance Precision Recall f1 accuracy
		##performances = performance_measures.get_performance_measures(solution_dict, ground, k_expected)

		return sol_dict
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise
		exit()

def compute_adapt_performance_for_dataset_with_threshold(predicate_info, conf_adapt, trust_average_adapt, is_coherent, threshold_list, delta, k_expected, first_ranking_criteria, second_ranking_criteria):
	# function that select the solution given by adapted model ---application of true value selection algorithm
	# it takes has solution the K values
	# (0) for each data item :
	#        (1) it select a set of possible true value
	#		 (2) it rank them w.r.t. two different criteria
	#        (3) it filter out the values that do not respect coherency property

	try:
		threshold_list = [0, 0.0001, 0.001, 0.005, 0.01, 0.1]
		performances_tot_ic_source = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]
		performances_tot_source_ic = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]

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
		for d in dataitems:
			# print("Start selection procedure: ")
			v_star_temp = adapted_model_selection.selection_phase(d, conf_adapt, 0, delta, children,
															   incl_ancestors, root_element)

			# print("Start ranking procedure: ")
			if len(v_star_temp) == 1:
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
				v_star_temp = filter_on_confidence_threshold(d, conf_adapt, v_star_temp, threshold)

				rank_list_firs_Rank = adapted_model_selection.ranking_phase(d, first_ranking_criteria, second_ranking_criteria,
															   v_star_temp, ic_values, trust_average_adapt)

				# print("Start filterning procedure: ")
				if len(rank_list_firs_Rank) == 0:
					performances_tot_ic_source = performance_measures.get_performance_measures_single_dataitem_error(performances_tot_ic_source, k_expected, threshold_index)
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants, incl_ancestors,
																				 rank_list_firs_Rank, k_expected)
					# if len(filtered_rank_list) == 0:
					#	cont_min += 1

					performances_tot_ic_source = performance_measures.get_performance_measures_single_dataitem(filtered_rank_list, ground[d], k_expected, performances_tot_ic_source, threshold_index,
																									 incl_ancestors)
					####
				rank_list_second_Rank = adapted_model_selection.ranking_phase(d, second_ranking_criteria, first_ranking_criteria,
																			v_star_temp, ic_values, trust_average_adapt)
				if len(rank_list_second_Rank) == 0:
					performances_tot_source_ic = performance_measures.get_performance_measures_single_dataitem_error(performances_tot_source_ic, k_expected, threshold_index)
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants,
																			 incl_ancestors,
																			 rank_list_second_Rank, k_expected)

					performances_tot_source_ic = performance_measures.get_performance_measures_single_dataitem(filtered_rank_list,
																								 ground[d], k_expected,
																								 performances_tot_source_ic,
																								 threshold_index,
																								 incl_ancestors)
			cont_d += 1
			if cont_d % 100 == 0:
				print("processed data items  " + str(cont_d) + "/" + str(len(dataitems)))

		# print("dimensione sol dictionary " + str(len(solution_dict)))
		# print(cont_min)

		# calculating performance Precision Recall f1 accuracy
		##performances = performance_measures.get_performance_measures(solution_dict, ground, k_expected)

		# print(performances)
		return [performances_tot_ic_source, performances_tot_source_ic]
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise
		exit()


def compute_adapt_performance_for_dataset_with_threshold_optimized(predicate_info, conf_adapt, trust_average_adapt, is_coherent, threshold_list, delta, k_expected, first_ranking_criteria, second_ranking_criteria, sources_dataitem_values):
	# function that select the solution given by adapted model ---application of true value selection algorithm
	# it takes has solution the K values
	# (0) for each data item :
	#        (1) it select a set of possible true value
	#		 (2) it rank them w.r.t. two different criteria
	#        (3) it filter out the values that do not respect coherency property

	try:
		threshold_list = [0]#, 0.0001, 0.001, 0.005, 0.01, 0.1]
		performances_tot_ic_source = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]
		performances_tot_source_ic = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]

		####initiliazation predicate and its information
		children = predicate_info[0]
		print("number of children " + str(len(children)))
		incl_descendants = predicate_info[1]
		print("number of descendants " + str(len(incl_descendants)))
		incl_ancestors = predicate_info[2]
		print("number of ancestors " + str(len(incl_ancestors)))
		ic_values = predicate_info[6]
		ground = predicate_info[7]
		dataitems = predicate_info[8]
		print("ic values loaded, number of instances " + str(len(ic_values)))

		cont_d = 0

		sol_dict_first_ranking = dict()
		sol_dict_second_ranking = dict()
		for d in dataitems:
			# print("Start selection procedure: ")
			if d not in sources_dataitem_values:
				continue
			for threshold_index in range(0, len(threshold_list)):
				threshold = threshold_list[threshold_index]
				copy_ancestors = dict()

				for item in sources_dataitem_values[d]:
					if conf_adapt[d+item] > threshold:
						copy_ancestors[item] = incl_ancestors[item]
				g = utils_taxonomy.loadGraphOfURIs(copy_ancestors)
				v_star_temp = utils_taxonomy.return_leaves(g)

				rank_list_firs_Rank = adapted_model_selection.ranking_phase(d, first_ranking_criteria, second_ranking_criteria,
															   v_star_temp, ic_values, trust_average_adapt)

				# print("Start filterning procedure: ")
				if len(rank_list_firs_Rank) == 0:
					sol_dict_first_ranking[d] = ""
					performances_tot_ic_source = performance_measures.get_performance_measures_single_dataitem_error(performances_tot_ic_source, k_expected, threshold_index)
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants, incl_ancestors,
																				 rank_list_firs_Rank, k_expected)
					# if len(filtered_rank_list) == 0:
					#	cont_min += 1
					sol_dict_first_ranking[d] = filtered_rank_list[0]
					performances_tot_ic_source = performance_measures.get_performance_measures_single_dataitem(filtered_rank_list, ground[d], k_expected, performances_tot_ic_source, threshold_index,
																									 incl_ancestors)
					####
				rank_list_second_Rank = adapted_model_selection.ranking_phase(d, second_ranking_criteria, first_ranking_criteria,
																			v_star_temp, ic_values, trust_average_adapt)
				if len(rank_list_second_Rank) == 0:
					sol_dict_second_ranking[d] = ""
					performances_tot_source_ic = performance_measures.get_performance_measures_single_dataitem_error(performances_tot_source_ic, k_expected, threshold_index)
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants,
																			 incl_ancestors,
																			 rank_list_second_Rank, k_expected)
					sol_dict_second_ranking[d] = filtered_rank_list[0]
					performances_tot_source_ic = performance_measures.get_performance_measures_single_dataitem(filtered_rank_list,
																								 ground[d], k_expected,
																								 performances_tot_source_ic,
																								 threshold_index,
																								 incl_ancestors)
			cont_d += 1
			if cont_d % 100 == 0:
				print("processed data items  " + str(cont_d) + "/" + str(len(dataitems)))

		# calculating performance Precision Recall f1 accuracy
		##performances = performance_measures.get_performance_measures(solution_dict, ground, k_expected)
		utils_writing_results.writing_sol_dictionary("estimation_rules/adapt_sol_prop_first_ranking_delta1.csv",
		                                             sol_dict_first_ranking)
		utils_writing_results.writing_sol_dictionary(
			"estimation_rules/adapt_sol_prop_second_ranking_delta1.csv", sol_dict_second_ranking)

		return [performances_tot_ic_source, performances_tot_source_ic]
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise
		exit()

def compute_adapt_performance_for_dataset_with_threshold_optimized_greedy_2(predicate_info, conf_adapt, trust_average_adapt, is_coherent, threshold_list, delta, k_expected, first_ranking_criteria, second_ranking_criteria, sources_dataitem_values):
	# function that select the solution given by adapted model ---application of true value selection algorithm
	# it takes has solution the K values
	# (0) for each data item :
	#        (1) it select a set of possible true value
	#		 (2) it rank them w.r.t. two different criteria
	#        (3) it filter out the values that do not respect coherency property

	try:
		root_element = predicate_info[4]
		threshold_list = [1.1, 1, 0.75, 0.5, 0.25, 0.0]#, 0.0001, 0.001, 0.005, 0.01, 0.1]
		performances_tot_ic_source = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]
		performances_tot_source_ic = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]

		####initiliazation predicate and its information
		children = predicate_info[0]
		print("number of children " + str(len(children)))
		incl_descendants = predicate_info[1]
		print("number of descendants " + str(len(incl_descendants)))
		incl_ancestors = predicate_info[2]
		print("number of ancestors " + str(len(incl_ancestors)))
		ic_values = predicate_info[6]
		ground = predicate_info[7]
		dataitems = predicate_info[8]
		print("ic values loaded, number of instances " + str(len(ic_values)))

		cont_d = 0

		for d in dataitems:
			# print("Start selection procedure: ")
			if d not in sources_dataitem_values:
				continue

			copy_ancestors = dict()
			for item in sources_dataitem_values[d]:
				if conf_adapt[d + item] > 0:
					copy_ancestors[item] = incl_ancestors[item]

			for threshold_index in range(0, len(threshold_list)):
				threshold = threshold_list[threshold_index]
				copy_ancestors_list = list(copy_ancestors)
				for item in copy_ancestors_list:
					if conf_adapt[d+item] <= 0: # <= threhsold
					#if (1 - ic_values[item]) < 1:
						del copy_ancestors[item]

				g = utils_taxonomy.loadGraphOfURIs(copy_ancestors)
				g_red = utils_taxonomy.perform_transitive_reduction(g)
				children_d = utils_taxonomy.reverse_transitive_reduction(g_red)
				if root_element not in children_d.nodes:
					v_star_temp = set()
				else:
					v_star_temp = adapted_model_selection.selection_phase_for_delta_0(d, conf_adapt, 0, delta, children_d,
															   incl_ancestors, root_element)

				rank_list_firs_Rank = adapted_model_selection.ranking_phase(d, first_ranking_criteria, second_ranking_criteria,
															   v_star_temp, ic_values, trust_average_adapt)

				# print("Start filterning procedure: ")
				if len(rank_list_firs_Rank) == 0:
					performances_tot_ic_source = performance_measures.get_performance_measures_single_dataitem_error(performances_tot_ic_source, k_expected, threshold_index)
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants, incl_ancestors,
																				 rank_list_firs_Rank, 10000)
					# if len(filtered_rank_list) == 0:
					#	cont_min += 1
					filtered_rank_list_app = copy.deepcopy(filtered_rank_list)
					for item in filtered_rank_list_app:
						if ic_values[item] > threshold:
							filtered_rank_list.remove(item)

					performances_tot_ic_source = performance_measures.get_performance_measures_single_dataitem(filtered_rank_list, ground[d], k_expected, performances_tot_ic_source, threshold_index,
																									 incl_ancestors)
					####
				rank_list_second_Rank = adapted_model_selection.ranking_phase(d, second_ranking_criteria, first_ranking_criteria,
																			v_star_temp, ic_values, trust_average_adapt)
				if len(rank_list_second_Rank) == 0:
					performances_tot_source_ic = performance_measures.get_performance_measures_single_dataitem_error(performances_tot_source_ic, k_expected, threshold_index)
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants,
																			 incl_ancestors,
																			 rank_list_second_Rank, 10000)

					filtered_rank_list_app = copy.deepcopy(filtered_rank_list)
					for item in filtered_rank_list_app:
						if ic_values[item] > threshold:
							filtered_rank_list.remove(item)
					performances_tot_source_ic = performance_measures.get_performance_measures_single_dataitem(filtered_rank_list,
																								 ground[d], k_expected,
																								 performances_tot_source_ic,
																								 threshold_index,
																								 incl_ancestors)
			cont_d += 1
			if cont_d % 100 == 0:
				print("processed data items  " + str(cont_d) + "/" + str(len(dataitems)))

		# calculating performance Precision Recall f1 accuracy
		##performances = performance_measures.get_performance_measures(solution_dict, ground, k_expected)

		return [performances_tot_ic_source, performances_tot_source_ic]
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise
		exit()



def compute_adapt_performance_for_dataset_with_threshold_optimized_greedy(predicate_info, conf_adapt, trust_average_adapt, is_coherent, threshold_list, delta, k_expected, first_ranking_criteria, second_ranking_criteria, sources_dataitem_values):
	# function that select the solution given by adapted model ---application of true value selection algorithm
	# it takes has solution the K values
	# (0) for each data item :
	#        (1) it select a set of possible true value
	#		 (2) it rank them w.r.t. two different criteria
	#        (3) it filter out the values that do not respect coherency property

	try:
		root_element = predicate_info[4]
		threshold_list = [0]#, 0.0001, 0.001, 0.005, 0.01, 0.1]
		performances_tot_ic_source = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]
		performances_tot_source_ic = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]

		####initiliazation predicate and its information
		children = predicate_info[0]
		print("number of children " + str(len(children)))
		incl_descendants = predicate_info[1]
		print("number of descendants " + str(len(incl_descendants)))
		incl_ancestors = predicate_info[2]
		print("number of ancestors " + str(len(incl_ancestors)))
		ic_values = predicate_info[6]
		ground = predicate_info[7]
		dataitems = predicate_info[8]
		print("ic values loaded, number of instances " + str(len(ic_values)))

		cont_d = 0
		sol_dict_second_ranking = dict()
		sol_dict_first_ranking = dict()
		for d in dataitems:
			# print("Start selection procedure: ")
			if d not in sources_dataitem_values:
				continue

			copy_ancestors = dict()
			for item in sources_dataitem_values[d]:
				if conf_adapt[d + item] > 0:
					copy_ancestors[item] = incl_ancestors[item]

			for threshold_index in range(0, len(threshold_list)):
				threshold = threshold_list[threshold_index]
				copy_ancestors_list = list(copy_ancestors)
				for item in copy_ancestors_list:
					if conf_adapt[d+item] <= threshold:
					#if (1 - ic_values[item]) < 1:
						del copy_ancestors[item]

				g = utils_taxonomy.loadGraphOfURIs(copy_ancestors)
				g_red = utils_taxonomy.perform_transitive_reduction(g)
				children_d = utils_taxonomy.reverse_transitive_reduction(g_red)
				if root_element not in children_d.nodes:
					v_star_temp = set()
				else:
					v_star_temp = adapted_model_selection.selection_phase_for_delta_0(d, conf_adapt, 0, delta, children_d,
															   incl_ancestors, root_element)

				rank_list_firs_Rank = adapted_model_selection.ranking_phase(d, first_ranking_criteria, second_ranking_criteria,
															   v_star_temp, ic_values, trust_average_adapt)

				# print("Start filterning procedure: ")
				if len(rank_list_firs_Rank) == 0:
					sol_dict_first_ranking[d] = ""
					performances_tot_ic_source = performance_measures.get_performance_measures_single_dataitem_error(performances_tot_ic_source, k_expected, threshold_index)
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants, incl_ancestors,
																				 rank_list_firs_Rank, k_expected)
					# if len(filtered_rank_list) == 0:
					#	cont_min += 1
					'''filtered_rank_list_app = copy.deepcopy(filtered_rank_list)
					for item in filtered_rank_list_app:
						if ic_values[item] > threshold:
							filtered_rank_list.remove(item)'''
					sol_dict_first_ranking[d] = filtered_rank_list[0]
					performances_tot_ic_source = performance_measures.get_performance_measures_single_dataitem(filtered_rank_list, ground[d], k_expected, performances_tot_ic_source, threshold_index,
																									 incl_ancestors)
					####
				rank_list_second_Rank = adapted_model_selection.ranking_phase(d, second_ranking_criteria, first_ranking_criteria,
																			v_star_temp, ic_values, trust_average_adapt)
				if len(rank_list_second_Rank) == 0:
					sol_dict_second_ranking[d] = ""
					performances_tot_source_ic = performance_measures.get_performance_measures_single_dataitem_error(performances_tot_source_ic, k_expected, threshold_index)
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants,
																			 incl_ancestors,
																			 rank_list_second_Rank, k_expected)

					'''filtered_rank_list_app = copy.deepcopy(filtered_rank_list)
					for item in filtered_rank_list_app:
						if ic_values[item] > threshold:
							filtered_rank_list.remove(item)'''

					sol_dict_second_ranking[d] =filtered_rank_list[0]
					performances_tot_source_ic = performance_measures.get_performance_measures_single_dataitem(filtered_rank_list,
																								 ground[d], k_expected,
																								 performances_tot_source_ic,
																								 threshold_index,
																								 incl_ancestors)
			cont_d += 1
			if cont_d % 100 == 0:
				print("processed data items  " + str(cont_d) + "/" + str(len(dataitems)))

		# calculating performance Precision Recall f1 accuracy
		##performances = performance_measures.get_performance_measures(solution_dict, ground, k_expected)
				# writing solution on file
		utils_writing_results.writing_sol_dictionary("estimation_rules/adapt_sol_prop_first_ranking_delta0.csv",
				                                             sol_dict_first_ranking)
		utils_writing_results.writing_sol_dictionary(
					"estimation_rules/adapt_sol_prop_second_ranking_delta0.csv", sol_dict_second_ranking)

		return [performances_tot_ic_source, performances_tot_source_ic]
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise
		exit()

def compute_adapt_performance_for_dataset(predicate_info, conf_adapt, trust_average_adapt, is_coherent, threshold,
										  delta, k_expected, first_ranking_criteria, second_ranking_criteria):
	# function that select the solution given by adapted model ---application of true value selection algorithm
	# it takes has solution the K values
	# (0) for each data item :
	#        (1) it select a set of possible true value
	#		 (2) it rank them w.r.t. two different criteria
	#        (3) it filter out the values that do not respect coherency property

	try:
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
		solution_dict = dict()
		for d in dataitems:
			# print("Start selection procedure: ")
			v_star_temp = adapted_model_selection.selection_phase(d, conf_adapt, threshold, delta, children,
																  incl_ancestors, root_element)

			# print("Start ranking procedure: ")
			if len(v_star_temp) == 1:
				element = v_star_temp.pop()
				if element == root_element:
					if d + element not in conf_adapt:
						continue
					# there is no claims on this dataitem
					else:
						v_star_temp.add(element)
				else:
					v_star_temp.add(element)

			rank_list = adapted_model_selection.ranking_phase(d, first_ranking_criteria, second_ranking_criteria,
															  v_star_temp, ic_values, trust_average_adapt)

			# print("Start filterning procedure: ")

			filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants, incl_ancestors,
																		 rank_list, k_expected)
			# if len(filtered_rank_list) == 0:
			#	cont_min += 1

			solution_dict[d] = filtered_rank_list

			cont_d += 1
			if cont_d % 1000 == 0:
				print("processed data items  " + str(cont_d) + "/" + str(len(dataitems)))

		# print("dimensione sol dictionary " + str(len(solution_dict)))
		# print(cont_min)

		# calculating performance Precision Recall f1 accuracy
		performances = performance_measures.get_performance_measures(solution_dict, ground, k_expected)

		# print(performances)
		return performances
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise
		exit()


def compute_adapt_performance_for_dataset_with_threshold_and_norm(predicate_info, conf_adapt, conf_adapt_norm, trust_average_adapt, is_coherent, threshold_list, delta, k_expected, first_ranking_criteria, second_ranking_criteria):

	try:
		threshold_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5]#, 0.0001, 0.001, 0.005, 0.01, 0.1]
		performances_tot_ic_source = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]
		performances_tot_source_ic = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]

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
		for d in dataitems:
			# print("Start selection procedure: ")
			v_star_temp = adapted_model_selection.selection_phase(d, conf_adapt_norm, 0, delta, children,
															   incl_ancestors, root_element)

			# print("Start ranking procedure: ")
			if len(v_star_temp) == 1:
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
					performances_tot_ic_source = performance_measures.get_performance_measures_single_dataitem_error(performances_tot_ic_source, k_expected, threshold_index)
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants, incl_ancestors,
																				 rank_list_firs_Rank, k_expected)
					# if len(filtered_rank_list) == 0:
					#	cont_min += 1

					performances_tot_ic_source = performance_measures.get_performance_measures_single_dataitem(filtered_rank_list, ground[d], k_expected, performances_tot_ic_source, threshold_index,
																									 incl_ancestors)
					####
				rank_list_second_Rank = adapted_model_selection.ranking_phase(d, second_ranking_criteria, first_ranking_criteria,
																			v_star_temp, ic_values, trust_average_adapt)
				if len(rank_list_second_Rank) == 0:
					performances_tot_source_ic = performance_measures.get_performance_measures_single_dataitem_error(performances_tot_source_ic, k_expected, threshold_index)
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants,
																			 incl_ancestors,
																			 rank_list_second_Rank, k_expected)

					performances_tot_source_ic = performance_measures.get_performance_measures_single_dataitem(filtered_rank_list,
																								 ground[d], k_expected,
																								 performances_tot_source_ic,
																								 threshold_index,
																								 incl_ancestors)
			cont_d += 1
			if cont_d % 2000 == 0:
				print("processed data items  " + str(cont_d) + "/" + str(len(dataitems)))

		return [performances_tot_ic_source, performances_tot_source_ic]
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise
		exit()


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

def compute_solution_best_children_final_real_world(dataitems, predicate_info, conf_adapt, conf_adapt_norm, trust_average_adapt, is_coherent, k_expected, first_ranking_criteria, second_ranking_criteria,threshold_list):
	is_coherent = True
	try:
		#threshold_list = [0.000000001]#, 0.0001, 0.001, 0.005, 0.01, 0.1]

		####initiliazation predicate and its information
		children = predicate_info[0]
		#print("number of children " + str(len(children)))
		incl_descendants = predicate_info[1]
		#print("number of descendants " + str(len(incl_descendants)))
		incl_ancestors = predicate_info[2]
		#print("number of ancestors " + str(len(incl_ancestors)))
		root_element = predicate_info[4]
		ic_values = predicate_info[6]

		#print("ic values loaded, number of instances " + str(len(ic_values)))

		cont_d = 0
		dict_solution_TRUST = dict()
		dict_solution_IC = dict()
		for threshold_index in range(0, len(threshold_list)):
			threshold = threshold_list[threshold_index]
			dict_solution_TRUST[threshold] = dict()
			dict_solution_IC[threshold] = dict()

		for d in dataitems:
			#d = "Charlie Chaplin AND was born"#"James G. Blaine AND was born"
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

def compute_solution_all_children_final_real_world(D, predicate_info, conf_adapt, conf_adapt_norm, trust_average_adapt, k_expected, first_ranking_criteria, second_ranking_criteria, sources_dataitem_values_prop, threshold_list):
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
		print("ic values loaded, number of instances " + str(len(ic_values)))

		cont_d = 0
		dict_solution_TRUST = dict()
		dict_solution_IC = dict()

		for threshold_index in range(0, len(threshold_list)):
			threshold = threshold_list[threshold_index]
			dict_solution_TRUST[threshold] = dict()
			dict_solution_IC[threshold] = dict()

		for d in D:
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
				print("processed data items  " + str(cont_d) + "/" + str(len(D)))

		return [dict_solution_IC, dict_solution_TRUST]
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise
		exit()


def compute_adapt_performance_for_dataset_with_threshold_optimized_and_norm(predicate_info, conf_adapt, conf_adapt_norm, trust_average_adapt, is_coherent, threshold_list, delta, k_expected, first_ranking_criteria, second_ranking_criteria, sources_dataitem_values):
	# function that select the solution given by adapted model ---application of true value selection algorithm
	# it takes has solution the K values
	# (0) for each data item :
	#        (1) it select a set of possible true value
	#		 (2) it rank them w.r.t. two different criteria
	#        (3) it filter out the values that do not respect coherency property

	try:
		threshold_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
		performances_tot_ic_source = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]
		performances_tot_source_ic = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]

		####initiliazation predicate and its information
		children = predicate_info[0]
		print("number of children " + str(len(children)))
		incl_descendants = predicate_info[1]
		print("number of descendants " + str(len(incl_descendants)))
		incl_ancestors = predicate_info[2]
		print("number of ancestors " + str(len(incl_ancestors)))
		ic_values = predicate_info[6]
		ground = predicate_info[7]
		dataitems = predicate_info[8]
		print("ic values loaded, number of instances " + str(len(ic_values)))

		cont_d = 0

		for d in dataitems:
			# print("Start selection procedure: ")
			if d not in sources_dataitem_values:
				continue
			for threshold_index in range(0, len(threshold_list)):
				threshold = threshold_list[threshold_index]
				copy_ancestors = dict()

				for item in sources_dataitem_values[d]:
					if conf_adapt_norm[d+item] > threshold:
						copy_ancestors[item] = incl_ancestors[item]
				g = utils_taxonomy.loadGraphOfURIs(copy_ancestors)
				v_star_temp = utils_taxonomy.return_leaves(g)

				rank_list_firs_Rank = adapted_model_selection.ranking_phase(d, first_ranking_criteria, second_ranking_criteria,
															   v_star_temp, ic_values, trust_average_adapt)

				# print("Start filterning procedure: ")
				if len(rank_list_firs_Rank) == 0:
					performances_tot_ic_source = performance_measures.get_performance_measures_single_dataitem_error(performances_tot_ic_source, k_expected, threshold_index)
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants, incl_ancestors,
																				 rank_list_firs_Rank, k_expected)
					# if len(filtered_rank_list) == 0:
					#	cont_min += 1

					performances_tot_ic_source = performance_measures.get_performance_measures_single_dataitem(filtered_rank_list, ground[d], k_expected, performances_tot_ic_source, threshold_index,
																									 incl_ancestors)
					####
				rank_list_second_Rank = adapted_model_selection.ranking_phase(d, second_ranking_criteria, first_ranking_criteria,
																			v_star_temp, ic_values, trust_average_adapt)
				if len(rank_list_second_Rank) == 0:
					performances_tot_source_ic = performance_measures.get_performance_measures_single_dataitem_error(performances_tot_source_ic, k_expected, threshold_index)
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants,
																			 incl_ancestors,
																			 rank_list_second_Rank, k_expected)

					performances_tot_source_ic = performance_measures.get_performance_measures_single_dataitem(filtered_rank_list,
																								 ground[d], k_expected,
																								 performances_tot_source_ic,
																								 threshold_index,
																								 incl_ancestors)
			cont_d += 1
			if cont_d % 100 == 0:
				print("processed data items  " + str(cont_d) + "/" + str(len(dataitems)))

		return [performances_tot_ic_source, performances_tot_source_ic]
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise
		exit()


def compute_adapt_performance_for_dataset_with_threshold_optimized_greedy_and_norm(predicate_info, conf_adapt, conf_adapt_norm, trust_average_adapt, is_coherent, threshold_list, delta, k_expected, first_ranking_criteria, second_ranking_criteria, sources_dataitem_values):

	try:
		root_element = predicate_info[4]
		threshold_list = [0, 0.0001, 0.001, 0.005, 0.01, 0.1]
		performances_tot_ic_source = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]
		performances_tot_source_ic = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]

		####initiliazation predicate and its information
		children = predicate_info[0]
		print("number of children " + str(len(children)))
		incl_descendants = predicate_info[1]
		print("number of descendants " + str(len(incl_descendants)))
		incl_ancestors = predicate_info[2]
		print("number of ancestors " + str(len(incl_ancestors)))
		ic_values = predicate_info[6]
		ground = predicate_info[7]
		dataitems = predicate_info[8]
		print("ic values loaded, number of instances " + str(len(ic_values)))

		cont_d = 0

		for d in dataitems:
			# print("Start selection procedure: ")
			if d not in sources_dataitem_values:
				continue

			copy_ancestors = dict()
			for item in sources_dataitem_values[d]:
				if conf_adapt_norm[d + item] > 0:
					copy_ancestors[item] = incl_ancestors[item]

			for threshold_index in range(0, len(threshold_list)):
				threshold = threshold_list[threshold_index]
				copy_ancestors_list = list(copy_ancestors)
				for item in copy_ancestors_list:
					if conf_adapt_norm[d+item] <= threshold:
						del copy_ancestors[item]

				g = utils_taxonomy.loadGraphOfURIs(copy_ancestors)
				g_red = utils_taxonomy.perform_transitive_reduction(g)
				children_d = utils_taxonomy.reverse_transitive_reduction(g_red)
				if root_element not in children_d.nodes:
					v_star_temp = set()
				else:
					v_star_temp = adapted_model_selection.selection_phase_for_delta_0(d, conf_adapt, 0, delta, children_d,
															   incl_ancestors, root_element)

				rank_list_firs_Rank = adapted_model_selection.ranking_phase(d, first_ranking_criteria, second_ranking_criteria,
															   v_star_temp, ic_values, trust_average_adapt)

				# print("Start filterning procedure: ")
				if len(rank_list_firs_Rank) == 0:
					performances_tot_ic_source = performance_measures.get_performance_measures_single_dataitem_error(performances_tot_ic_source, k_expected, threshold_index)
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants, incl_ancestors,
																				 rank_list_firs_Rank, k_expected)
					# if len(filtered_rank_list) == 0:
					#	cont_min += 1

					performances_tot_ic_source = performance_measures.get_performance_measures_single_dataitem(filtered_rank_list, ground[d], k_expected, performances_tot_ic_source, threshold_index,
																									 incl_ancestors)
					####
				rank_list_second_Rank = adapted_model_selection.ranking_phase(d, second_ranking_criteria, first_ranking_criteria,
																			v_star_temp, ic_values, trust_average_adapt)
				if len(rank_list_second_Rank) == 0:
					performances_tot_source_ic = performance_measures.get_performance_measures_single_dataitem_error(performances_tot_source_ic, k_expected, threshold_index)
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants,
																			 incl_ancestors,
																			 rank_list_second_Rank, k_expected)

					performances_tot_source_ic = performance_measures.get_performance_measures_single_dataitem(filtered_rank_list,
																								 ground[d], k_expected,
																								 performances_tot_source_ic,
																								 threshold_index,
																								 incl_ancestors)
			cont_d += 1
			if cont_d % 100 == 0:
				print("processed data items  " + str(cont_d) + "/" + str(len(dataitems)))

		# calculating performance Precision Recall f1 accuracy
		##performances = performance_measures.get_performance_measures(solution_dict, ground, k_expected)

		return [performances_tot_ic_source, performances_tot_source_ic]
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise
		exit()


#comparsion with existing model
def compute_adapt_perf_complete_threshold_and_norm(predicate_info, conf_adapt, conf_adapt_norm, trust_average_adapt, is_coherent, threshold_list, delta, k_expected, first_ranking_criteria, second_ranking_criteria, sources_dataitem_values):

	try:
		threshold_list = [0]#, 0.1, 0.2, 0.3, 0.4, 0.5]
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
		solution_dict_first_rank = dict()
		solution_dict_second_rank = dict()
		for d in dataitems:
			# print("Start selection procedure: ")
			v_star_temp = adapted_model_selection.selection_phase(d, conf_adapt_norm, 0, delta, children,
															   incl_ancestors, root_element)

			# print("Start ranking procedure: ")
			if len(v_star_temp) == 1:
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
				if len(rank_list_firs_Rank) == 0:
					solution_dict_first_rank[d] = list()
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants, incl_ancestors,
																				 rank_list_firs_Rank, k_expected)
					solution_dict_first_rank[d] = filtered_rank_list

				####
				rank_list_second_Rank = adapted_model_selection.ranking_phase(d, second_ranking_criteria, first_ranking_criteria,
																			v_star_temp, ic_values, trust_average_adapt)
				if len(rank_list_second_Rank) == 0:
					solution_dict_second_rank[d] = list()
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants,
																			 incl_ancestors,
																			 rank_list_second_Rank, k_expected)

					solution_dict_second_rank[d] = filtered_rank_list

			cont_d += 1
			if cont_d % 2000 == 0:
				print("processed data items  " + str(cont_d) + "/" + str(len(dataitems)))

		performances_first = performance_measures.get_complete_performance_measures_at_k_1(solution_dict_first_rank, ground,
																		   sources_dataitem_values)
		performances_second = performance_measures.get_complete_performance_measures_at_k_1(solution_dict_second_rank, ground,
																			sources_dataitem_values)
		return [performances_first, performances_second]
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise
		exit()


def compute_adapt_perf_complete_threshold_optimized_and_norm(predicate_info, conf_adapt, conf_adapt_norm, trust_average_adapt, is_coherent, threshold_list, delta, k_expected, first_ranking_criteria, second_ranking_criteria, sources_dataitem_values):
	# function that select the solution given by adapted model ---application of true value selection algorithm
	# it takes has solution the K values
	# (0) for each data item :
	#        (1) it select a set of possible true value
	#		 (2) it rank them w.r.t. two different criteria
	#        (3) it filter out the values that do not respect coherency property

	try:
		threshold_list = [0]# 0.0001, 0.001, 0.005, 0.01, 0.1]
		####initiliazation predicate and its information
		children = predicate_info[0]
		print("number of children " + str(len(children)))
		incl_descendants = predicate_info[1]
		print("number of descendants " + str(len(incl_descendants)))
		incl_ancestors = predicate_info[2]
		print("number of ancestors " + str(len(incl_ancestors)))
		ic_values = predicate_info[6]
		ground = predicate_info[7]
		dataitems = predicate_info[8]
		print("ic values loaded, number of instances " + str(len(ic_values)))

		cont_d = 0
		solution_dict_first_rank = dict()
		solution_dict_second_rank = dict()
		for d in dataitems:
			# print("Start selection procedure: ")
			if d not in sources_dataitem_values:
				continue
			for threshold_index in range(0, len(threshold_list)):
				threshold = threshold_list[threshold_index]
				copy_ancestors = dict()

				for item in sources_dataitem_values[d]:
					if conf_adapt_norm[d+item] > threshold:
						copy_ancestors[item] = incl_ancestors[item]
				g = utils_taxonomy.loadGraphOfURIs(copy_ancestors)
				v_star_temp = utils_taxonomy.return_leaves(g)

				rank_list_firs_Rank = adapted_model_selection.ranking_phase(d, first_ranking_criteria, second_ranking_criteria,
															   v_star_temp, ic_values, trust_average_adapt)

				# print("Start filterning procedure: ")
				if len(rank_list_firs_Rank) == 0:
					solution_dict_first_rank[d] = list()
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants, incl_ancestors,
																				 rank_list_firs_Rank, k_expected)
					solution_dict_first_rank[d] = filtered_rank_list

					####
				rank_list_second_Rank = adapted_model_selection.ranking_phase(d, second_ranking_criteria, first_ranking_criteria,
																			v_star_temp, ic_values, trust_average_adapt)
				if len(rank_list_second_Rank) == 0:
					solution_dict_second_rank[d] = list()
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants,
																			 incl_ancestors,
																			 rank_list_second_Rank, k_expected)

					solution_dict_second_rank[d] = filtered_rank_list
			cont_d += 1
			if cont_d % 1000 == 0:
				print("processed data items  " + str(cont_d) + "/" + str(len(dataitems)))

		performances_first = performance_measures.get_complete_performance_measures_at_k_1(solution_dict_first_rank, ground,
																		   sources_dataitem_values)
		performances_second = performance_measures.get_complete_performance_measures_at_k_1(solution_dict_second_rank, ground,
																			sources_dataitem_values)
		return [performances_first, performances_second]
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise
		exit()


def compute_adapt_perf_complete_threshold_optimized_greedy_and_norm(predicate_info, conf_adapt, conf_adapt_norm, trust_average_adapt, is_coherent, threshold_list, delta, k_expected, first_ranking_criteria, second_ranking_criteria, sources_dataitem_values):

	try:
		root_element = predicate_info[4]
		threshold_list = [0]#, 0.0001, 0.001, 0.005, 0.01, 0.1]
		####initiliazation predicate and its information
		children = predicate_info[0]
		print("number of children " + str(len(children)))
		incl_descendants = predicate_info[1]
		print("number of descendants " + str(len(incl_descendants)))
		incl_ancestors = predicate_info[2]
		print("number of ancestors " + str(len(incl_ancestors)))
		ic_values = predicate_info[6]
		ground = predicate_info[7]
		dataitems = predicate_info[8]
		print("ic values loaded, number of instances " + str(len(ic_values)))

		cont_d = 0
		solution_dict_first_rank = dict()
		solution_dict_second_rank = dict()
		for d in dataitems:
			# print("Start selection procedure: ")
			if d not in sources_dataitem_values:
				continue

			copy_ancestors = dict()
			for item in sources_dataitem_values[d]:
				if conf_adapt_norm[d + item] > 0:
					copy_ancestors[item] = incl_ancestors[item]

			for threshold_index in range(0, len(threshold_list)):
				threshold = threshold_list[threshold_index]
				copy_ancestors_list = list(copy_ancestors)
				for item in copy_ancestors_list:
					if conf_adapt_norm[d+item] <= threshold:
						del copy_ancestors[item]

				g = utils_taxonomy.loadGraphOfURIs(copy_ancestors)
				g_red = utils_taxonomy.perform_transitive_reduction(g)
				children_d = utils_taxonomy.reverse_transitive_reduction(g_red)
				if root_element not in children_d.nodes:
					v_star_temp = set()
				else:
					v_star_temp = adapted_model_selection.selection_phase_for_delta_0(d, conf_adapt, 0, delta, children_d,
															   incl_ancestors, root_element)

				rank_list_firs_Rank = adapted_model_selection.ranking_phase(d, first_ranking_criteria, second_ranking_criteria,
															   v_star_temp, ic_values, trust_average_adapt)

				# print("Start filterning procedure: ")
				if len(rank_list_firs_Rank) == 0:
					solution_dict_first_rank[d] = list()
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants, incl_ancestors,
																				 rank_list_firs_Rank, k_expected)
					# if len(filtered_rank_list) == 0:
					#	cont_min += 1

					solution_dict_first_rank[d] = filtered_rank_list
					####
				rank_list_second_Rank = adapted_model_selection.ranking_phase(d, second_ranking_criteria, first_ranking_criteria,
																			v_star_temp, ic_values, trust_average_adapt)
				if len(rank_list_second_Rank) == 0:
					solution_dict_second_rank[d] = list()
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants,
																			 incl_ancestors,
																			 rank_list_second_Rank, k_expected)

					solution_dict_second_rank[d] = filtered_rank_list
			cont_d += 1
			if cont_d % 100 == 0:
				print("processed data items  " + str(cont_d) + "/" + str(len(dataitems)))

		# calculating performance Precision Recall f1 accuracy
		performances_first = performance_measures.get_complete_performance_measures_at_k_1(solution_dict_first_rank, ground, sources_dataitem_values)
		performances_second = performance_measures.get_complete_performance_measures_at_k_1(solution_dict_second_rank, ground,
																		   sources_dataitem_values)
		return [performances_first, performances_second]
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise
		exit()


#for fuseky
def compute_adapt_performance_for_dataset_with_threshold_optimized_fuseky(predicate_info, conf_adapt, trust_average_adapt, is_coherent, threshold_list, delta, k_expected, first_ranking_criteria, second_ranking_criteria, sources_dataitem_values):
	# function that select the solution given by adapted model ---application of true value selection algorithm
	# it takes has solution the K values
	# (0) for each data item :
	#        (1) it select a set of possible true value
	#		 (2) it rank them w.r.t. two different criteria
	#        (3) it filter out the values that do not respect coherency property

	try:
		threshold_list = [1, 0.75,0.5,0.25, 0.0]#, 0.8, 0.6, 0.4, 0.2, 0]
		performances_tot_ic_source = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]
		performances_tot_source_ic = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]

		####initiliazation predicate and its information
		children = predicate_info[0]
		print("number of children " + str(len(children)))
		incl_descendants = predicate_info[1]
		print("number of descendants " + str(len(incl_descendants)))
		incl_ancestors = predicate_info[2]
		print("number of ancestors " + str(len(incl_ancestors)))
		ic_values = predicate_info[6]
		ground = predicate_info[7]
		dataitems = predicate_info[8]
		print("ic values loaded, number of instances " + str(len(ic_values)))

		cont_d = 0
		sol_dict_first_ranking = dict()
		sol_dict_second_ranking = dict()
		for d in dataitems:
			# print("Start selection procedure: ")
			if d not in sources_dataitem_values:
				continue
			for threshold_index in range(0, len(threshold_list)):
				threshold = threshold_list[threshold_index]
				copy_ancestors = dict()

				set_prop = set()
				for item in sources_dataitem_values[d]:
					if ic_values[item] < threshold:
						copy_ancestors[item] = incl_ancestors[item]
						set_prop.update(incl_ancestors[item])

				for item in set_prop:
					if item not in copy_ancestors:
						copy_ancestors[item] = incl_ancestors[item]
				g = utils_taxonomy.loadGraphOfURIs(copy_ancestors)
				v_star_temp = utils_taxonomy.return_leaves(g)

				rank_list_firs_Rank = adapted_model_selection.ranking_phase(d, first_ranking_criteria, second_ranking_criteria,
															   v_star_temp, ic_values, trust_average_adapt)

				if len(rank_list_firs_Rank) == 0:
					sol_dict_first_ranking[d] = ""
					performances_tot_ic_source = performance_measures.get_performance_measures_single_dataitem_error(performances_tot_ic_source, k_expected, threshold_index)
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants, incl_ancestors,
																				 rank_list_firs_Rank, k_expected)
					sol_dict_first_ranking[d] = filtered_rank_list[0]
					performances_tot_ic_source = performance_measures.get_performance_measures_single_dataitem(filtered_rank_list, ground[d], k_expected, performances_tot_ic_source, threshold_index,
																									 incl_ancestors)
					####
				rank_list_second_Rank = adapted_model_selection.ranking_phase(d, second_ranking_criteria, first_ranking_criteria,
																			v_star_temp, ic_values, trust_average_adapt)
				if len(rank_list_second_Rank) == 0:
					sol_dict_second_ranking[d] = ""
					performances_tot_source_ic = performance_measures.get_performance_measures_single_dataitem_error(performances_tot_source_ic, k_expected, threshold_index)
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants,
																			 incl_ancestors,
																			 rank_list_second_Rank, k_expected)
					sol_dict_second_ranking[d] = filtered_rank_list[0]
					performances_tot_source_ic = performance_measures.get_performance_measures_single_dataitem(filtered_rank_list,
																								 ground[d], k_expected,
																								 performances_tot_source_ic,
																								 threshold_index,
																								 incl_ancestors)
			cont_d += 1
			if cont_d % 100 == 0:
				print("processed data items  " + str(cont_d) + "/" + str(len(dataitems)))

		# calculating performance Precision Recall f1 accuracy
		# writing solution on file
		utils_writing_results.writing_sol_dictionary("estimation_rules/adapt_sol_prop_first_ranking_delta1.csv", sol_dict_first_ranking)
		utils_writing_results.writing_sol_dictionary("estimation_rules/adapt_sol_prop_second_ranking_delta1.csv", sol_dict_second_ranking)
		##performances = performance_measures.get_performance_measures(solution_dict, ground, k_expected)
		print(performances_tot_ic_source)
		print(performances_tot_source_ic)
		return [performances_tot_ic_source, performances_tot_source_ic]
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise
		exit()


def compute_adapt_performance_for_dataset_with_threshold_optimized_greedy_fuseky(predicate_info, conf_adapt, trust_average_adapt, is_coherent, threshold_list, delta, k_expected, first_ranking_criteria, second_ranking_criteria, sources_dataitem_values):
	# function that select the solution given by adapted model ---application of true value selection algorithm
	# it takes has solution the K values
	# (0) for each data item :
	#        (1) it select a set of possible true value
	#		 (2) it rank them w.r.t. two different criteria
	#        (3) it filter out the values that do not respect coherency property

	try:
		root_element = predicate_info[4]
		threshold_list = [1]#, 0.0001, 0.001, 0.005, 0.01, 0.1]
		performances_tot_ic_source = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
							[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]
		performances_tot_source_ic = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
									  [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]

		####initiliazation predicate and its information
		children = predicate_info[0]
		print("number of children " + str(len(children)))
		incl_descendants = predicate_info[1]
		print("number of descendants " + str(len(incl_descendants)))
		incl_ancestors = predicate_info[2]
		print("number of ancestors " + str(len(incl_ancestors)))
		ic_values = predicate_info[6]
		ground = predicate_info[7]
		dataitems = predicate_info[8]
		print("ic values loaded, number of instances " + str(len(ic_values)))

		cont_d = 0
		sol_dict_first_ranking = dict()
		sol_dict_second_ranking = dict()
		for d in dataitems:
			# print("Start selection procedure: ")
			if d not in sources_dataitem_values:
				continue

			copy_ancestors = dict()
			set_prop = set()
			for item in sources_dataitem_values[d]:
				if ic_values[item] >= 0:
					copy_ancestors[item] = incl_ancestors[item]
					set_prop.update(incl_ancestors[item])
			##
			for item in set_prop:
				if item not in copy_ancestors:
					copy_ancestors[item] = incl_ancestors[item]

			for threshold_index in range(0, len(threshold_list)):
				threshold = threshold_list[threshold_index]
				copy_ancestors_list = list(copy_ancestors)
				for item in copy_ancestors_list:
					if ic_values[item] > threshold:
						del copy_ancestors[item]

				g = utils_taxonomy.loadGraphOfURIs(copy_ancestors)
				g_red = utils_taxonomy.perform_transitive_reduction(g)
				children_d = utils_taxonomy.reverse_transitive_reduction(g_red)
				if root_element not in children_d.nodes:
					v_star_temp = set()
				else:
					v_star_temp = adapted_model_selection.selection_phase_for_delta_0(d, conf_adapt, 0, delta, children_d,
															   incl_ancestors, root_element)

				rank_list_firs_Rank = adapted_model_selection.ranking_phase(d, first_ranking_criteria, second_ranking_criteria,
															   v_star_temp, ic_values, trust_average_adapt)

				# print("Start filterning procedure: ")
				if len(rank_list_firs_Rank) == 0:
					sol_dict_first_ranking[d] = ""
					performances_tot_ic_source = performance_measures.get_performance_measures_single_dataitem_error(performances_tot_ic_source, k_expected, threshold_index)
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants, incl_ancestors,
																				 rank_list_firs_Rank, k_expected)
					sol_dict_first_ranking[d] = filtered_rank_list[0]

					performances_tot_ic_source = performance_measures.get_performance_measures_single_dataitem(filtered_rank_list, ground[d], k_expected, performances_tot_ic_source, threshold_index,
																									 incl_ancestors)
					####
				rank_list_second_Rank = adapted_model_selection.ranking_phase(d, second_ranking_criteria, first_ranking_criteria,
																			v_star_temp, ic_values, trust_average_adapt)
				if len(rank_list_second_Rank) == 0:
					sol_dict_second_ranking[d] = ""
					performances_tot_source_ic = performance_measures.get_performance_measures_single_dataitem_error(performances_tot_source_ic, k_expected, threshold_index)
				else:
					filtered_rank_list = adapted_model_selection.filtering_phase(is_coherent, incl_descendants,
																			 incl_ancestors,
																			 rank_list_second_Rank, k_expected)
					sol_dict_second_ranking[d] = filtered_rank_list[0]
					performances_tot_source_ic = performance_measures.get_performance_measures_single_dataitem(filtered_rank_list,
																								 ground[d], k_expected,
																								 performances_tot_source_ic,
																								 threshold_index,
																								 incl_ancestors)
			cont_d += 1
			if cont_d % 100 == 0:
				print("processed data items  " + str(cont_d) + "/" + str(len(dataitems)))

		# calculating performance Precision Recall f1 accuracy

		# writing solution on file
		utils_writing_results.writing_sol_dictionary("estimation_rules/adapt_sol_prop_first_ranking_delta0.csv",
		                                             sol_dict_first_ranking)
		utils_writing_results.writing_sol_dictionary("estimation_rules/adapt_sol_prop_second_ranking_delta0.csv",
		                                             sol_dict_second_ranking)
		##performances = performance_measures.get_performance_measures(solution_dict, ground, k_expected)
		print(performances_tot_ic_source)
		print(performances_tot_source_ic)
		##performances = performance_measures.get_performance_measures(solution_dict, ground, k_expected)

		return [performances_tot_ic_source, performances_tot_source_ic]
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise
		exit()


if __name__ == '__main__':
	#test function select the most specific alternatives
	copy_ancestors = dict()
	sources_dataitem_values = dict()
	d = "data1"
	sources_dataitem_values[d] = dict()
	sources_dataitem_values[d]["A"] = set()
	sources_dataitem_values[d]["B"] = set()
	sources_dataitem_values[d]["C"] = set()
	sources_dataitem_values[d]["D"] = set()
	sources_dataitem_values[d]["E"] = set()
	sources_dataitem_values[d]["F"] = set()
	sources_dataitem_values[d]["G"] = set()
	sources_dataitem_values[d]["H"] = set()

	conf_adapt_norm = dict()
	conf_adapt_norm[d+"A"] = 1.0
	conf_adapt_norm[d+"B"] = 0.5
	conf_adapt_norm[d+"C"] = 0.05
	conf_adapt_norm[d+"D"] = 0.05
	conf_adapt_norm[d+"E"] = 0.4
	conf_adapt_norm[d+"F"] = 0.2
	conf_adapt_norm[d+"G"] = 0.2
	conf_adapt_norm[d+"H"] = 0.3

	incl_ancestors = dict()
	incl_ancestors["A"] = {"A"}
	incl_ancestors["B"] = {"A", "B"}
	incl_ancestors["C"] = {"A", "B", "C"}
	incl_ancestors["D"] = {"A", "B", "D"}
	incl_ancestors["E"] = {"A", "E"}
	incl_ancestors["F"] = {"A", "E", "F"}
	incl_ancestors["G"] = {"A", "E", "G"}
	incl_ancestors["H"] = {"A", "H"}

	threshold = 1
	for item in sources_dataitem_values[d]:
		if conf_adapt_norm[d + item] > threshold:
			copy_ancestors[item] = incl_ancestors[item]
	g = utils_taxonomy.loadGraphOfURIs(copy_ancestors)
	v_star_temp = utils_taxonomy.return_leaves(g)
	print(sorted(v_star_temp))