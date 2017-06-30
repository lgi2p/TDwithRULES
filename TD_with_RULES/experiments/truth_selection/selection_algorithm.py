import sys
from TD_with_RULES.experiments.truth_selection import adapted_model_selection
from TD_with_RULES.utils_tdo import utils_taxonomy


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

		return sol_dict
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise
		exit()




