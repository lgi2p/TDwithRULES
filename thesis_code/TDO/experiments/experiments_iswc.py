import datetime
import copy
import gc
import os
import sys
cwd = os.getcwd()
if ("TDO") not in cwd:
	print("error with sys.path")
	exit()
else:
	index_tdo = cwd.index("TDO")
	cwd = cwd[:index_tdo+3]#+3] #+  "/"
	sys.path.append(cwd)
	cwd = cwd[:index_tdo]  # +3] #+  "/"
	sys.path.append(cwd)

from TDO.utils_tdo import utils_rules
from TDO.utils_tdo import utils_predicate
from TDO.utils_tdo import utils_dataset
from TDO.utils_tdo import utils_writing_results
from TDO.experiments.truth_selection import selection_algorithm
from TDO.experiments.model import sums_model
from TDO.experiments.model import preprocessing_sums_model
from TDO.utils_tdo import utils_normalize_conf

if __name__ == '__main__':
	print("_______________________________Experiments and evaluation - Script launched_______________________________")
	#input only predicate + Sums & Rules or AdaptedSums & Rules + gamma list to test
	#genre True False [0.0, 0.1, 0.9] D:\\data_VALE/thesis_code/TDO/ 20
	# genre True False [0.0,0.1,0.9] D:/thesis_code/TDO/ D:/results_rules_8_jan/ 20
	predicate = sys.argv[1]
	Sums_and_Rules_flag = False
	if sys.argv[2] == 'True':
		Sums_and_Rules_flag = True

	AdaptedSums_and_Rules_flag = False
	if sys.argv[3] == 'True':
		AdaptedSums_and_Rules_flag = True

	gamma_list = (sys.argv[4][1:-1]).split(",")
	index_ = 0
	for threshold in gamma_list:
		threshold = float(threshold)
		gamma_list[index_] = threshold
		index_ += 1

	abs_path_app_folder = sys.argv[5]
	abs_path_results = sys.argv[6]

	max_iteration_number = int(sys.argv[7])

	already_processed = list()

	threshold_list = ("0.0").split(",")
	index_ = 0
	for threshold in threshold_list:
		threshold = float(threshold)
		threshold_list[index_] = threshold
		index_ += 1
	k_expected = 5

	boos_EBS_flag = True  # both EBS score and boosting
	score_EBS_flag = True  # EBS only for score
	Sums_flag = False
	TSbC_flag = True
	TSaC_flag = False

	trust_average_normalized = True
	# end initialization parameter from the user
	if not (utils_predicate.set_predicate(predicate)):
		print("Error in setting predicate name")
		exit()

	base_dir = abs_path_app_folder + "required_files/"# "../datasets/"

	if predicate == "genre":
		str_hc = "0.01"
		hc_constant = 0.01
	else:
		str_hc = "0.012"
		hc_constant = 0.012
	dir = os.path.dirname(__file__)
	predicate_info = utils_predicate.loading_predicate_info(base_dir, predicate)
	ancestors = predicate_info[2]
	truth = predicate_info[7]
	g = None
	if AdaptedSums_and_Rules_flag:
		g = predicate_info[5]
		descendants = predicate_info[1]
	else:
		predicate_info[5] = None
		predicate_info[1].clear()
		predicate_info[0].clear()
		predicate_info[6] = None
	predicate_info[3].clear()
	predicate_info[9] = None
	predicate_info[10] = None
	gc.collect()

	cont_subfolders = 0
	cont_datasets = 0

	path_datasets = abs_path_app_folder + "\\datasets\\dataset_" + str(predicate)
	count_char = path_datasets.count("\\") + 1

	solution_folder_base_Sums_and_Rules = abs_path_results + "/Sums_and_Rules/" + str(predicate) + "/"
	solution_folder_base_AdaptSums_and_Rules = abs_path_results + "/AdaptSums_and_Rules/" + str(predicate) + "/"
	solution_folder_trust_Sums_and_Rules = abs_path_results + "/Sums_and_Rules_trust/" + str(predicate) + "/"
	solution_folder_trust_AdaptSums_and_Rules = abs_path_results + "/AdaptSums_and_Rules_trust/" + str(predicate) + "/"

	# rule part##################################################
	bayes_score_flag = True
	if predicate == "birthPlace":
		rule_path = abs_path_app_folder + "required_files/rules_files/KB_tot.birthplace.out"
		rule_path_bayes_metrics = abs_path_app_folder + "required_files/rules_files/prova_bayes_rules_birthPlace.out"
	elif predicate == "genre" :
		rule_path = abs_path_app_folder + "required_files/rules_files/genre_rules_ok.out"
		rule_path_bayes_metrics = abs_path_app_folder + "required_files/rules_files\\prova_bayes_rules.out"
	#load all rules
	load_rules_results = utils_rules.load_rules_with_threshold(rule_path, hc_constant, bayes_score_flag, rule_path_bayes_metrics)
	R = load_rules_results[0]
	R_id = load_rules_results[1]
	R_bayes = load_rules_results[2]

	id_R = dict()
	for r in R_id:
		id_R[R_id[r]] = r
	print("loaded rules from our KB : " + str(len(R)))

	# load all eligible rules for each data item
	rule_desc = None
	print("elibible rule has to be found, time start " + str(datetime.datetime.now()).split('.')[0])
	cont_d = 0
	cont_zero_eligible_rules = 0
	f_in_eligible = open(base_dir + str(predicate) + "/eligible_rules_hc_" + str(str_hc) + ".csv", "r")
	eligible_rules = dict()
	for line in f_in_eligible:
		if predicate == "genre":
			line = line.strip().split("\\t")
		else:
			line = line.strip().split("\t")
		d = line[0]#[1:-1]
		list_of_rules = list()
		for rule_id in line[1].split(" "):
			rule = id_R[int(rule_id)]  # de indenta
			list_of_rules.append(rule)  # de indenta
			'''if int(rule_id) in id_R:#
				app_set.add(rule_id)#
				rule = id_R[int(rule_id)]#de indenta
				list_of_rules.append(rule)#de indenta'''
		if len(list_of_rules)>0: #
			eligible_rules[d] = list_of_rules#de indenta
	f_in_eligible.close()
	#load all conclusions inferred by eligible rules given a specific data item
	valid_values_for_r_and_d = utils_rules.read_valid_values_dict(base_dir + str(predicate) + "/valid_values_for_el_rules_hc_" + str(str_hc) + ".csv")

	#model computation starts
	initial_trustworthiness = 0.8
	initial_confidence = 0.5
	D = list()
	T = list()
	S_set = list()
	fact_and_source_info = list()
	dataitem_values_info = list()
	F_s = dict()
	S_prop = dict()
	S = dict()
	sources_dataItemValues = dict()
	dataitem_ids = dict()

	for root, dirs, files in os.walk(path_datasets):

		if ["EXP", "LOW_E", "UNI"] == dirs: continue
		if root.count('\\') != count_char: continue
		#if "UNI" not in root: continue
		for dir_name in dirs:
			print("dir name :" + str(dir_name))
			if dir_name in already_processed:
				cont_datasets += 1
				continue
			dir_name = dir_name.replace("dataset", "")

			n_dataset = dir_name
			#obtaining important informaiton related to location and name of dataset we are analysing
			if "-" in n_dataset:
				n_dataset = n_dataset.replace("UNI-", "")
				n_dataset = n_dataset.replace("EXP-", "")
				n_dataset = n_dataset.replace("LOW_E-", "")
				n_dataset = n_dataset.replace("-", "")
				n_folder_app = "-" + str(n_dataset[0:2])
				n_dataset = n_dataset[2:]
				n_folder_app = n_folder_app + n_dataset

			else:
				n_dataset = n_dataset.replace("UNI_", "")
				n_dataset = n_dataset.replace("EXP_", "")
				n_dataset = n_dataset.replace("LOW_E_", "")
				n_dataset = n_dataset.replace("_", "")
				n_folder_app = "_"
				n_folder_app = n_folder_app + n_dataset
			# facts file path
			if "UNI" in root:
				dataset_kind_ = "UNI"
				subfolder_path = "UNI/dataset" + str(n_folder_app) + "/"
				facts_file = path_datasets + "/UNI/dataset" + str(n_folder_app) + "/facts_" + str(
					n_dataset) + ".csv"
				source_file = path_datasets + "/UNI/dataset" + str(n_folder_app) + "/Output_acc_" + str(
					n_dataset) + ".txt"
				dataitem_index_file = path_datasets + "/UNI/dataset" + str(
					n_folder_app) + "/dataitems_index_" + str(n_dataset) + ".csv"
				confidence_value_computation_info_dir = path_datasets + "/UNI/dataset" + str(
					n_folder_app) + "/confidence_value_computation_info/"

			if "EXP" in root:
				dataset_kind_ = "EXP"
				subfolder_path = "EXP/dataset" + str(n_folder_app) + "/"
				facts_file = path_datasets + "/EXP/dataset" + str(n_folder_app) + "/facts_" + str(
					n_dataset) + ".csv"
				source_file = path_datasets + "/EXP/dataset" + str(n_folder_app) + "/Output_acc_" + str(
					n_dataset) + ".txt"
				dataitem_index_file = path_datasets + "/EXP/dataset" + str(
					n_folder_app) + "/dataitems_index_" + str(n_dataset) + ".csv"
				confidence_value_computation_info_dir = path_datasets + "/EXP/dataset" + str(
					n_folder_app) + "/confidence_value_computation_info/"

			if "LOW_E" in root:
				dataset_kind_ = "LOW_E"
				subfolder_path = "LOW_E/dataset" + str(n_folder_app) + "/"
				facts_file = path_datasets + "/LOW_E/dataset" + str(n_folder_app) + "/facts_" + str(
					n_dataset) + ".csv"
				source_file = path_datasets + "/LOW_E/dataset" + str(n_folder_app) + "/Output_acc_" + str(
					n_dataset) + ".txt"
				dataitem_index_file = path_datasets + "/LOW_E/dataset" + str(
					n_folder_app) + "/dataitems_index_" + str(n_dataset) + ".csv"
				confidence_value_computation_info_dir = path_datasets + "/LOW_E/dataset" + str(
					n_folder_app) + "/confidence_value_computation_info/"

			if not os.path.exists(confidence_value_computation_info_dir): os.makedirs(
				confidence_value_computation_info_dir)

			# output files
			trust_file_base = os.path.join(solution_folder_trust_Sums_and_Rules+ "/" + str(dataset_kind_), "dataset" + dir_name)
			if not os.path.exists(trust_file_base):
				os.makedirs(trust_file_base)

			# end to declare  output file

			# clear all the variable to not overload the memory
			dataitem_ids.clear()
			D.clear()
			T.clear()
			S_set.clear()
			S.clear()
			F_s.clear()
			S_prop.clear()
			sources_dataItemValues.clear()
			dataitem_values_info.clear()
			fact_and_source_info.clear()

			source_file = os.path.join(dir, source_file)
			facts_file = os.path.join(dir, facts_file)

			if AdaptedSums_and_Rules_flag:
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
				app_conf_dict = res_list[7]

			header = False  # original trustworthiness file
			T_actual = utils_dataset.load_sources_info(source_file, header)

			header = False # load trustworthiness of sources
			T = utils_dataset.load_sources_info(source_file, header)
			print(str(len(T)) + " sources loaded")
			S_set = list(T.keys())

			# load facts
			header = True
			sources_dataItemValues = utils_dataset.load_facts(facts_file, header)
			D = list(sources_dataItemValues.keys())

			# compute (1) all the facts that are claimed by a source and (2) all the sources that claim a specific fact
			# (1) set of facts that are claimed by a specific source < key = source id, value = set of facts (dataitem + value) >
			# (2) all the sources that claim a specific fact <key = dataitem + value, value = set of source ids>
			print("Fact loading")
			fact_and_source_info = utils_dataset.load_fact_and_source_info(sources_dataItemValues)
			F_s = fact_and_source_info[0]
			S = fact_and_source_info[1]

			#######################################################################################################
			if Sums_and_Rules_flag:
				#print("Compute boost dict")
				#compute boosting factor based on EB method
				boost_dict = utils_rules.compute_boost_dict_EBS(sources_dataItemValues, R_bayes, eligible_rules, valid_values_for_r_and_d)

				print("Sums & Rules -- Sums&Rules + gamma = 0 == Sums")
				#gamma_list =[0.1]# [0.10, 0.25, 0.5, 0.6, 0.75, 0.9, 1.0]
				for gamma_ in gamma_list:
					# de comment if you want to study trustworhniess or convergence
					# trust_file_base = os.path.join(solution_folder_trust_Sums_and_Rules + "/" + str(gamma_) + "/" + str(dataset_kind_), "dataset" + dir_name)
					#if not os.path.exists(trust_file_base):
					#	os.makedirs(trust_file_base)
					trust_file_adapt_for_iter = ""
					#trust_file_adapt_for_iter = os.path.join(trust_file_base , "trad_trust_est_at_eac_iter" + str(dir_name) + ".csv")
					#trust_file_adapt = os.path.join(trust_file_base, "trad_trust_est" + str(dir_name) + ".csv")

					res_a = sums_model.run_sums_and_boost_saving_iter(copy.deepcopy(T), F_s, S, initial_confidence, max_iteration_number, trust_file_adapt_for_iter,sources_dataItemValues, boost_dict, gamma_)

					if res_a:
						T_trad_rules = res_a[0]
						C_trad_rules = res_a[1]
						#if you want to save source trustworthiness decomment the following line
						#res = utils_writing_results.writing_trust_results(trust_file_adapt, T_trad_rules)

						print("Starting selection of true values algorithm for trad sums.....")
						dict_solution_highest_conf = selection_algorithm.compute_trad_performance_final(predicate_info,C_trad_rules,sources_dataItemValues,k_expected)

						#save results/SOLUTION in output files named Sums_and_Rules_*iddataet*.csv
						solution_folder_adapt = solution_folder_base_Sums_and_Rules + str(gamma_) + "/" + str(
							dataset_kind_) + "/"
						if not os.path.exists(solution_folder_adapt): os.makedirs(solution_folder_adapt)
						f_out_trad_and_rules = open(solution_folder_adapt + "sol_Sums_and_rules" + str(n_folder_app) + ".csv", "w")
						missing_dataitems = 0
						#some data items are never claims by sources in some datasets
						for dataitem in truth:
							if dataitem not in dict_solution_highest_conf:
								missing_dataitems += 1
							else:
								list_app = dict_solution_highest_conf[dataitem]
								out_str = ""
								for item in list_app:
									out_str += str(item) + " "
								out_str = out_str[:-1]
								if predicate == "genre":
									dataitem = bytes(dataitem, 'unicode-escape')
									dataitem = str(dataitem, 'utf-8')
									f_out_trad_and_rules.write(str(dataitem) + '\t' + str(out_str) + '\n')
								else:
									f_out_trad_and_rules.write(str(dataitem) + '\t' + str(out_str) + '\n')
							f_out_trad_and_rules.flush()
						f_out_trad_and_rules.close()
					else:
						print("Error during the computation of Sums&Rules model")

			if AdaptedSums_and_Rules_flag:
				#print("Compute propagated boost dict")
				boost_dict_prop = utils_rules.get_propagated_boost_dict_fuseky_optimized_BAYES(
						sources_dataItemValues,eligible_rules, R_bayes,valid_values_for_r_and_d,ancestors,bayes_score_flag)
				print("ADAPTEDSums & Rules -- ADAPTEDSums&Rules + gamma = 0 == AdaptedSums")
				#gamma_list = [0.10, 0.25, 0.6]  # 0, 0.25, 0.5, 0.75, [0.10, 0.25, 0.5, 0.6, 0.75, 0.9, 1.0]
				for gamma_ in gamma_list:
					#de comment to study trustworthniess and convergenence
					trust_file_adapt_for_iter = ""
					'''trust_file_base = os.path.join(solution_folder_trust_AdaptSums_and_Rules + "/" + str(gamma_) + "/" + str(dataset_kind_), "dataset" + dir_name)
					if not os.path.exists(trust_file_base):	os.makedirs(trust_file_base)
					
					trust_file_adapt_for_iter = os.path.join(trust_file_base,"trad_trust_est_at_eac_iter" + str(dir_name) + ".csv")
					trust_file_adapt = os.path.join(trust_file_base, "trad_trust_est" + str(dir_name) + ".csv")'''

					res_a = sums_model.run_adapted_sums_and_boost_saving_iter(copy.deepcopy(T), F_s, S_prop,
																			  initial_confidence, max_iteration_number,
																			  sources_dataItemValues,
																			  trust_file_adapt_for_iter, boost_dict_prop,
																			  gamma_)

					if res_a:
						T_adapt_rules = res_a[0]
						C_adapt_rules = res_a[1]
						# res = utils_writing_results.writing_trust_results(trust_file_adapt, T_adapt_rules)
						trust_average = utils_dataset.compute_average_trustworhiness(S_prop,T_adapt_rules)  # T_average is a dict with key = claim_id and
						T_average_normalized = utils_dataset.normalize_trust_average(trust_average, ancestors,descendants,sources_dataItemValues)
						#print("computing normalized confidence")
						conf_adapt_norm = utils_normalize_conf.creating_normalized_for_d_estimation_optimized(truth,C_adapt_rules,app_conf_dict)
						gc.collect()
						if TSbC_flag:
							print(
								"Starting selection of true values algorithm for adapt model and NORMALIZED trust average.....")
							print("TESTING MODEL -- BestChildren -- delta = 0")
							first_ranking_criteria = "ic"
							second_ranking_criteria = "source_average"
							#is_coherent = True
							solutions_dict = selection_algorithm.compute_solution_best_children_final(predicate_info,
																									  C_adapt_rules,
																									  conf_adapt_norm,
																									  T_average_normalized,
																									  "", k_expected,
																									  first_ranking_criteria,
																									  second_ranking_criteria)

							dict_solution_IC_final = solutions_dict[0]
							dict_solution_TRUST_final = solutions_dict[1]

							missing_dataitems_IC = 0
							missing_dataitems_TRUST = 0
							solution_folder_adapt = solution_folder_base_AdaptSums_and_Rules + "/" + str(gamma_) + "/" + str(
								dataset_kind_) + "/"
							if not os.path.exists(solution_folder_adapt): os.makedirs(solution_folder_adapt)

							f_out_TSbC = open(
								solution_folder_adapt + "sol_AdaptedSums_and_rules_TSbC_" + str(n_folder_app) + ".csv", "w")

							for dataitem in truth:
								for threshold in threshold_list:
									if dataitem not in dict_solution_IC_final[threshold] and dataitem not in \
											dict_solution_TRUST_final[threshold]:
										missing_dataitems_IC += 1
									else:
										list_app_IC = dict_solution_IC_final[threshold][dataitem]
										out_IC = ""
										for item in list_app_IC:
											out_IC += str(item) + " "
										out_IC = out_IC[:-1]
										list_app_TRUST = dict_solution_TRUST_final[threshold][dataitem]
										out_TRUST = ""
										for item in list_app_TRUST:
											out_TRUST += str(item) + " "
										out_TRUST = out_TRUST[:-1]
										if predicate == "genre":
											dataitem_to_out = bytes(dataitem, 'unicode-escape')
											dataitem_to_out = str(dataitem_to_out, 'utf-8')
											f_out_TSbC.write(str(threshold) + '\t' + str(dataitem_to_out) + '\t' + str(
												out_IC) + '\t' + str(out_TRUST) + '\n')
										else:
											f_out_TSbC.write(
												str(threshold) + '\t' + str(dataitem) + '\t' + str(out_IC) + '\t' + str(
													out_TRUST) + '\n')
								f_out_TSbC.flush()
							f_out_TSbC.close()
						##############################################################################################################
			cont_datasets += 1
			#############################################################################################################
			print("process dataset " + str(cont_datasets) + "/20")
			exit()

		# only the first level of subfolder
		cont_subfolders += 1
		#end one dataset




