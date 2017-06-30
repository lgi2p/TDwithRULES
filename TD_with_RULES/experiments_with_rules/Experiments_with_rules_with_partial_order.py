import os
import datetime
import copy
from TD_with_RULES.utils_tdo import utils_rules
from TD_with_RULES.utils_tdo import utils_predicate
from TD_with_RULES.utils_tdo import utils_evaluation
from TD_with_RULES.utils_tdo import utils_writing_results
from TD_with_RULES.experiments.model import preprocessing_sums_model
from TD_with_RULES.utils_tdo import utils_dataset
from TD_with_RULES.experiments.truth_selection import selection_algorithm
from TD_with_RULES.experiments.model import sums_model



if __name__ == '__main__':
	predicate = "birthPlace"
	path_datasets = "..\\datasets\\dataset_" + str(predicate)

	str_hc = "012"
	hc_constant = 0.012
	print("_______________________________Experiments with rules and evaluation and evaluation - Script launched_______________________________")
	#input
	already_processed = list()
	threshold = 0
	delta = 0
	if "True" == 'True':
		coherent = True
	else:
		if "True"  == 'False':
			coherent = False
	first_ranking_criteria = "source_average"
	second_ranking_criteria = "ic"
	trust_average_normalized = False
	# end initialization parameter from the user

	k_expected = 1
	base_dir = "../required_files/"# "../datasets/"
	#base_dir = "D:/thesis_code/TDO/datasets/dataset_birthPlace/EXP"
	path_ground_file = '../required_files/' + str(predicate) + '/sample_ground_grouped.csv'

	#######output
	output_estimations_main_dir = "../new_estimations_rules/results_sums_" + str(predicate) + "/"
	output_conf_evaluations_main_dir = "../conf_evaluations_rules/" + str(predicate) + "/"

	if not os.path.exists(output_estimations_main_dir): os.makedirs(output_estimations_main_dir)
	if not os.path.exists(output_conf_evaluations_main_dir): os.makedirs(output_conf_evaluations_main_dir)

	dir = os.path.dirname(__file__)
	if coherent:
		str_coherent = "ordered"
	else:
		str_coherent = "not_ordered"

	trad_sub_folder_dir = "delta_" + str(delta) + "_" + str(str_coherent) + "/" + str(
		first_ranking_criteria) + "_" + str(second_ranking_criteria) + "/"
	adapt_sub_folder_dir = "delta_" + str(delta) + "_" + str(str_coherent) + "/" + str(
		first_ranking_criteria) + "_" + str(second_ranking_criteria) + "/theta_" + str(threshold).replace(".",
	                                                                                                      "-") + "/"

	trad_output_conf_evaluations_dir = os.path.join(output_conf_evaluations_main_dir, trad_sub_folder_dir)
	adapt_output_conf_evaluations_dir = os.path.join(output_conf_evaluations_main_dir, adapt_sub_folder_dir)

	if not os.path.exists(trad_output_conf_evaluations_dir): os.makedirs(trad_output_conf_evaluations_dir)
	if not os.path.exists(adapt_output_conf_evaluations_dir): os.makedirs(adapt_output_conf_evaluations_dir)

	trad_conf_perf_path = os.path.join(trad_output_conf_evaluations_dir, "trad_perf_res_" + str(predicate) + ".csv")
	adapt_perf_path_norm = os.path.join(adapt_output_conf_evaluations_dir,
	                                    "adapt_perf_res_" + str(predicate) + "_norm.csv")

	file_out_trad = open(trad_conf_perf_path, "a")
	file_out_adapt_norm = open(adapt_perf_path_norm, "a")

	file_out_trad_precision = "precision_conf_propagated_sums.csv"
	file_out_adapt_precision = "precision_conf_sums_adapted_with_RULES.csv"

	predicate_info = utils_predicate.loading_predicate_info(base_dir, predicate)
	ancestors = predicate_info[2]
	g = predicate_info[5]
	ic_values = predicate_info[6]
	truth = utils_predicate.loading_ground_truth(path_ground_file)[0]
	print("number of data item in truth  " +str(len(truth)))

	# rule part##################################################
	rule_path = "../external_KB/dbpedia/KB_tot.birthplace.out"
	f_in_eligible = open(base_dir + str(predicate) + "/eligible_rules_hc_" + str(str_hc) + ".csv", "r")

	load_rules_results = utils_rules.load_rules_with_threshold(rule_path, hc_constant)
	R = load_rules_results[0]
	R_id = load_rules_results[1]
	id_R = dict()
	for r in R_id:
		id_R[R_id[r]] = r

	print("number of loaded rules from the external KB : " + str(len(R)))

	rule_desc = None
	print("elibible rule has to be found, time start " + str(datetime.datetime.now()).split('.')[0])
	cont_d = 0
	cont_zero_eligible_rules = 0

	eligible_rules = utils_rules.load_eligible_rules(f_in_eligible, id_R)
	valid_values_for_r_and_d = utils_rules.read_valid_values_dict(
		base_dir + str(predicate) + "/valid_values_for_el_rules_hc_" + str(str_hc) + ".csv")

	#Constant
	# output
	model_name = "sums"
	# Constants
	initial_trustworthiness = 0.8
	initial_confidence = 0.5
	max_iteration_number = 20
	# initialization
	T = list()
	fact_and_source_info = list()
	dataitem_values_info = list()
	F_s = dict()
	S_prop = dict()
	S = dict()
	sources_dataItemValues = dict()

	cont_datasets = 0
	for root, dirs, files in os.walk(path_datasets):

		if ["EXP", "LOW_E", "UNI"] == dirs: continue
		if root.count('\\') != 3: continue

		performances_tot_adapt_norm = list()
		performances_tot_adapt_not = list()
		performances_tot_trad = list()

		for dir_name in dirs:
			print("dir name :" + str(dir_name))
			if dir_name in already_processed:
				cont_datasets += 1
				continue
			n_dataset, n_folder_app, dataset_kind_, subfolder_path, facts_file, source_file, dataitem_index_file, confidence_value_computation_info_dir = utils_dataset.get_all_useful_name_and_paths(
				dir_name, root, path_datasets)

			if not os.path.exists(confidence_value_computation_info_dir): os.makedirs(
				confidence_value_computation_info_dir)
			# output information
			output_estimations = os.path.join(output_estimations_main_dir, subfolder_path)
			if not os.path.exists(output_estimations): os.makedirs(output_estimations)
			# results files and dir for trad model
			trust_file_trad = os.path.join(output_estimations, "trad_est_trust_" + str(n_dataset) + ".csv")
			trust_file_trad_for_iter = os.path.join(output_estimations,
													"trad_est_trust_for_iter" + str(n_dataset) + ".csv")
			conf_file_trad = os.path.join(output_estimations, "trad_est_conf_" + str(n_dataset) + ".csv")
			# results files and dir for the adapt model
			trust_file_adapt = os.path.join(output_estimations, "adapt_est_trust_" + str(n_dataset) + ".csv")
			trust_file_adapt_for_iter = os.path.join(output_estimations,
													 "adapt_est_trust_for_iter" + str(n_dataset) + ".csv")
			conf_file_adapt = os.path.join(output_estimations, "adapt_est_conf_" + str(n_dataset) + ".csv")

			# end to declare input - output file

			# clear all the variable to not overload the memory
			if True:
				T.clear()
				S.clear()
				F_s.clear()
				S_prop.clear()
				sources_dataItemValues.clear()
				dataitem_values_info.clear()
				fact_and_source_info.clear()

			source_file = os.path.join(dir, source_file)
			facts_file = os.path.join(dir, facts_file)

			res_list = preprocessing_sums_model.preprocess_before_running_model(source_file, facts_file,
																				confidence_value_computation_info_dir,
																				dataitem_index_file,
																				g)
			T = res_list[0]
			T_actual = res_list[1]
			sources_dataItemValues = res_list[2]
			D = res_list[3]
			F_s = res_list[4]
			S = res_list[5]
			S_prop = res_list[6]

			header = False  # load original trustworthiness
			T_actual = utils_dataset.load_sources_info(source_file, header)

			header = False  # create dict that contains for each soure its trustworthiness
			T = utils_dataset.load_sources_info(source_file, header)
			print(str(len(T)) + " sources loaded")

			header = True  # load claims
			sources_dataItemValues = utils_dataset.load_facts(facts_file, header)

			# compute (1) all the facts that are claimed by a source and (2) all the sources that claim a specific fact
			# (1) set of facts that are claimed by a specific source < key = source id, value = set of facts (dataitem + value) >
			# (2) all the sources that claim a specific fact <key = dataitem + value, value = set of source ids>
			print("Claims loading")
			fact_and_source_info = utils_dataset.load_fact_and_source_info(sources_dataItemValues)
			F_s = fact_and_source_info[0]
			S = fact_and_source_info[1]
			#######################################################################################################
			# (2) Computation of the boosting factor (it takes into account the information given by rules)
			print("Compute boost dict")
			boost_dict_prop = utils_rules.get_propagated_boost_dict_fuseky_optimized(sources_dataItemValues,
																					 eligible_rules, R,
																					 valid_values_for_r_and_d,
																					 ancestors)
			#print("min boost factor " + str(min(boost_dict_prop.values())))
			#print("max boost factor " + str(max(boost_dict_prop.values())))
			#######################################################################################################
			# (3) Now the model can be applied!
			if True:
				print("Sums propagated run___________________________________________________________________________")
				res_t = sums_model.run_adapted_sums_saving_iter(copy.deepcopy(T), F_s, S_prop, initial_confidence,
				                                                max_iteration_number, sources_dataItemValues,
				                                                trust_file_adapt_for_iter)

				if res_t:
					T_trad = res_t[0]
					C_trad = res_t[1]

					trust_average = utils_dataset.compute_average_trustworhiness(S_prop,
					                                                             T_trad)  # T_average is a dict with key = claim_id and
					T_average_normalized = list()
					if len(T_average_normalized) == 0:
						descendants = predicate_info[1]
						ancestors = predicate_info[2]
						T_average_normalized = utils_dataset.normalize_trust_average(trust_average, ancestors,
						                                                             descendants,
						                                                             sources_dataItemValues)
						print("T average computed for number of instances " + str(len(T_average_normalized)))

					print(
						"Selection of true values algorithm for Sums considering partial order --> true values are the one with the greedy alg.")
					threshold_list = list()
					is_coherent = True

					sol_dict_trad = selection_algorithm.compute_adapt_solution_for_dataset_with_threshold_optimized_greedy(
						predicate_info, C_trad, T_average_normalized, is_coherent, threshold_list, 0, 5, "ic",
						"source_average", sources_dataItemValues)
					n_expected, n_general, n_error = utils_evaluation.compute_precision_with_general(sol_dict_trad, truth,
																									 ancestors)
					utils_writing_results.writing_results_on_precision_with_rules(file_out_trad_precision,
																				  n_folder_app, n_expected,
																				  n_general, n_error)
				else:
					print("Error in traditional model")
		#######################################################################################################
			if True:

				print("Adapted Sums run")
				gamma_list = [0.25, 0.5, 0.75, 0.9, 1.0]#0.05, 0.15,
				for gamma_ in gamma_list:
					res_a = sums_model.run_adapted_sums_and_boost_saving_iter(copy.deepcopy(T), F_s, S_prop,
					                                                          initial_confidence, max_iteration_number,
					                                                          sources_dataItemValues,
					                                                          trust_file_adapt_for_iter,
					                                                          boost_dict_prop, gamma_)

					if res_a:
						T_adapt = res_a[0]
						C_adapt = res_a[1]

						trust_average = utils_dataset.compute_average_trustworhiness(S_prop,
						                                                             T_adapt)  # T_average is a dict with key = claim_id and
						T_average_normalized = list()
						if len(T_average_normalized) == 0:
							descendants = predicate_info[1]
							ancestors = predicate_info[2]
							T_average_normalized = utils_dataset.normalize_trust_average(trust_average, ancestors,
							                                                             descendants,
							                                                             sources_dataItemValues)
							print("T average computed for number of instances " + str(len(T_average_normalized)))
						print(
							"Selection of true values algorithm for Sums considering partial order + RULES--> true values are the one with the greedy alg.")
						threshold_list = list()
						is_coherent = True
						sol_dict_adapt = selection_algorithm.compute_adapt_solution_for_dataset_with_threshold_optimized_greedy(
							predicate_info, C_adapt, T_average_normalized, is_coherent, threshold_list, 0, 5, "ic",
							"source_average", sources_dataItemValues)

						n_expected, n_general, n_error = utils_evaluation.compute_precision_with_general(sol_dict_adapt,
																										 truth,
																										 ancestors)
						utils_writing_results.writing_results_on_precision_with_rules(file_out_adapt_precision,
																					  n_folder_app, n_expected,
																					  n_general, n_error)

				else:
					print("Error in adapted model")

			cont_datasets += 1
			#############################################################################################################
			print("process dataset " + str(cont_datasets) + "/20")

		#end one dataset




