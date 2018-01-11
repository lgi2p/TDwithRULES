import os
import sys
import datetime
import copy
import gc
import shutil
from TDO.utils_tdo import utils_rules
from TDO.utils_tdo import utils_predicate
from TDO.experiments.model import preprocessing_sums_model
from TDO.utils_tdo import utils_dataset
from TDO.utils_tdo import utils_writing_results
from TDO.experiments.truth_selection import selection_algorithm
from TDO.experiments.model import sums_model
from TDO.utils_tdo import utils_normalize_conf

from SPARQLWrapper import SPARQLWrapper, JSON

if __name__ == '__main__':
#birthPlace [0.0] 5 False True False EXP False False
#birthPlace [0.0] 5 False True False EXP True False
#birthPlace [0.0] 5 False True False EXP True True

	MTD_pc = True
	str_ext = ""
	if MTD_pc:
		str_ext = "data_VALE"

	base_dir_anal = "D:\\" + str(str_ext) + "\\analysis_distr\\"
	if not os.path.exists(base_dir_anal): os.makedirs(base_dir_anal)

	str_hc = "0.01"
	hc_constant = 0.01

	print("_______________________________Experiments and evaluation - Script launched_______________________________")
	#input
	predicate = sys.argv[1]
	path_datasets = "D:\\" + str(str_ext) + "\\thesis_code\\TDO\\datasets\\dataset_" + str(predicate)

	threshold_list = (sys.argv[2][1:-1]).split(",")
	index_ = 0
	for threshold in threshold_list:
		threshold = float(threshold)
		threshold_list[index_] = threshold
		index_ += 1

	k_expected = int(sys.argv[3])
	if sys.argv[4] == 'True':
		Sums_flag = True
	else:
		if sys.argv[4] == 'False':
			Sums_flag = False

	if sys.argv[5] == 'True':
		TSbC_flag = True
	else:
		if sys.argv[5] == 'False':
			TSbC_flag = False

	if sys.argv[6] == 'True':
		TSaC_flag = True
	else:
		if sys.argv[6] == 'False':
			TSaC_flag = False

	trust_average_normalized = True
	already_processed = list()
	if len(sys.argv) > 10:
		str_list = sys.argv[10]
		str_list = str_list[+1:-1]
		for item in str_list.split(','):
			already_processed.append(item)
	# end initialization parameter from the user
	#already_processed.append("dataset_100")
	type_to_anal = sys.argv[7] #"EXP"
	bayes_score_flag = sys.argv[8]#True
	bayes_score_flag_boosting = sys.argv[9]#True

	f_out = open("analysis_ic_medio_"+str(predicate)+"_" + str(type_to_anal) + ".txt", "w")
	if bayes_score_flag == 'True':
		if bayes_score_flag_boosting == 'True':
			prefix_results_dir = "BAYES_BOTH"
			bayes_score_flag = True
			bayes_score_flag_boosting = True
		else:
			prefix_results_dir = "BAYES_"
			bayes_score_flag = True
			bayes_score_flag_boosting = False
	else:
		prefix_results_dir = "NORMAL"
		bayes_score_flag = False
		bayes_score_flag_boosting = False

	if not (utils_predicate.set_predicate(predicate)):
		print("Error in setting predicate name")
		exit()

	base_dir = "D:/" + str(str_ext) + "/thesis_code/TDO/required_files/"# "../datasets/"
	#base_dir = "D:/thesis_code/TDO/datasets/dataset_birthPlace/EXP"

	if predicate == "genre":
		path_ground_file ='D:/" + str(str_ext) + "/thesis_code/TDO/required_files/genre/sample_genre_base_3.csv'
	elif predicate == "birthPlace":
		path_ground_file = 'D:/" + str(str_ext) + "/thesis_code/TDO/required_files/birthPlace/sample_ground_grouped.csv'

	#predicate_info = utils_predicate.loading_predicate_info(base_dir, predicate)
	#ancestors = predicate_info[2]
	#g = predicate_info[5]

	dir = os.path.dirname(__file__)
	base_directory = "D:\\" + str(str_ext) + "\\RULES_with_PROP_" + str(predicate) + "_results\\" + prefix_results_dir

	cont_subfolders = 0
	cont_datasets = 0

	#output
	model_name = "sums"
	# Constants
	initial_trustworthiness = 0.8
	initial_confidence = 0.5
	max_iteration_number = 8
	#initialization
	D = list()
	T = list()
	S_set = list()
	fact_and_source_info = list()
	dataitem_values_info= list()
	F_s= dict()
	S_prop = dict()
	S=dict()
	sources_dataItemValues = dict()
	dataitem_ids = dict()
	truth_adapt = set()
	truth_trad = set()
	truth_ground_truth = set()

	predicate_info = utils_predicate.loading_predicate_info(base_dir, predicate)
# [children, descendants, ancestors, tax, root_element, g, ic_values, ground, dataitems, graph_file,graph_file_reduced]
	ancestors = predicate_info[2]
	predicate_info[0].clear()
	predicate_info[1].clear()
	predicate_info[3].clear()
	predicate_info[8].clear()

	g = predicate_info[5]
	truth = predicate_info[7]
	root_el = predicate_info[4]
	ic_values = predicate_info[6]
	gc.collect()

	print("number of data item in truth  " +str(len(truth)))

	path_datasets = base_directory + "\\datasets\\dataset_" + str(predicate)
	path_datasets = "D:\\" + str(str_ext) + "/thesis_code\\TDO\\datasets\\dataset_" + str(predicate)
	results_folder = base_directory + "\\results\\" + str(predicate) + "\\"
	if not os.path.exists(results_folder):
		os.makedirs(results_folder)
	solution_folder_trad_base = base_directory + "/results_final_trad/" + str(predicate) + "/"
	solution_folder_adapt_base = base_directory + "/results_final/" + str(predicate) + "/"

	# rule part##################################################
	#rule_path = "D:/dbpedia/KB_tot.birthplace.out"
	#rule_path = "D:/genre_rules_ok.out"
	if predicate == "birthPlace":
		rule_path = "D:/data_VALE/dbpedia/KB_tot.birthplace.out"
		rule_path_bayes_metrics = "D:/data_VALE\\dbpedia/prova_bayes_rules_birthPlace.out"
	elif predicate == "genre" :
		rule_path = "D:\\" + str(str_ext) + "/dbpedia/genre_rules_ok.out"
		rule_path_bayes_metrics = "D:\\" + str(str_ext) + "/dbpedia//prova_bayes_rules.out"
		#rule_path = "D:\\" + str(str_ext) + "/Vale/Downloads/genre_rules_ok.out"
		#rule_path_bayes_metrics = "D:\\" + str(str_ext) + "/prova_bayes_rules.out"
	else:
		print("error")
		exit()

	load_rules_results = utils_rules.load_rules_with_threshold(rule_path, hc_constant, bayes_score_flag, rule_path_bayes_metrics)
	R = load_rules_results[0]
	R_id = load_rules_results[1]
	R_bayes = load_rules_results[2]
	id_R = dict()
	for r in R_id:
		id_R[R_id[r]] = r
	print("regole caricate - our KB : " + str(len(R)))

	for r in R:
		print(r+'\t'+str(R[r]))
	exit()
	rule_desc = None
	print("elibible rule has to be found, time start " + str(datetime.datetime.now()).split('.')[0])
	cont_d = 0
	cont_zero_eligible_rules = 0

	f_in_eligible = open(base_dir + str(predicate) + "/eligible_rules_hc_" + str(str_hc) + ".csv", "r")
	eligible_rules = dict()
	#app_set = set()
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
	#print("control !! " + str(len(app_set)))

	valid_values_for_r_and_d = utils_rules.read_valid_values_dict(base_dir + str(predicate) + "/valid_values_for_el_rules_hc_" + str(str_hc) + ".csv")

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
		if root.count('\\') != 5: continue
		if type_to_anal not in root: continue

		performances_tot_adapt_norm = list()
		performances_tot_adapt_not = list()
		performances_tot_trad = list()

		for dir_name in dirs:
			print("dir name :" + str(dir_name))
			if dir_name in already_processed:
				cont_datasets += 1
				continue

			dir_name = dir_name.replace("dataset", "")

			n_dataset = dir_name
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
			trust_file_base = os.path.join(results_folder+ "/" + str(dataset_kind_), "dataset" + dir_name)
			if not os.path.exists(trust_file_base):
				os.makedirs(trust_file_base)
			if Sums_flag:
				trust_file_trad_for_iter = os.path.join(trust_file_base ,
				                                        "trad_trust_est_at_eac_iter" + str(dir_name) + ".csv")
				trust_file_trad = os.path.join(trust_file_base, "trad_trust_est" + str(dir_name) + ".csv")
				solution_folder_trad = solution_folder_trad_base + str(dataset_kind_) + "/"
				if not os.path.exists(solution_folder_trad): os.makedirs(solution_folder_trad)
				f_out_trad = open(solution_folder_trad + "solutions_trad_Sums" + str(n_folder_app) + ".csv", "w")

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

			'''res_list = preprocessing_sums_model.preprocess_before_running_model(source_file, facts_file,
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
'''
			header = False  # original trustworthiness
			T_actual = utils_dataset.load_sources_info(source_file, header)

			header = False
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

			if True:
				print("Compute boost dict propagated!")
				if bayes_score_flag_boosting:
					boost_dict_prop = utils_rules.get_propagated_boost_dict_fuseky_optimized_BAYES(sources_dataItemValues,
					                                                                         eligible_rules, R_bayes,
					                                                                         valid_values_for_r_and_d,
					                                                                         ancestors,
					                                                                         bayes_score_flag)
				elif bayes_score_flag:
					print("Bayes in score, not in boosting")
					boost_dict_prop = utils_rules.get_propagated_boost_dict_fuseky_optimized(sources_dataItemValues,
			                                                                         eligible_rules, R_bayes,
			                                                                         valid_values_for_r_and_d,
			                                                                         ancestors, bayes_score_flag)
				else:
					print("Bayes not in score, not in boosting")
					boost_dict_prop = utils_rules.get_propagated_boost_dict_fuseky_optimized(sources_dataItemValues,
					                                                                         eligible_rules, R,
					                                                                         valid_values_for_r_and_d,
					                                                                         ancestors,
					                                                                         bayes_score_flag)

				cont_true_values = 0
				ic_true_values = 0
				ic_rule_values = 0
				contr_rules_values = 0
				for d in sources_dataItemValues:
					for v in sources_dataItemValues[d]:
						true_value = truth[d]

						cont_true_values += 1
						ic_true_values += ic_values[true_value]
				average_ic_true_values = float(ic_true_values) / float(cont_true_values)

				for d in sources_dataItemValues:
					if d not in eligible_rules:continue
					for rule in eligible_rules[d]:
						value_set_valid = set()
						if d in valid_values_for_r_and_d:
							if rule in valid_values_for_r_and_d[d]:
								value_set_valid = valid_values_for_r_and_d[d][rule]

						for value in value_set_valid:
							if value not in ic_values:
								max_ic = 0
								if value not in ancestors:
									continue
								for anc in ancestors[value]:
									if anc in ic_values:
										if ic_values[anc] > max_ic:
											max_ic = ic_values[anc]
								if max_ic == 0 :
									continue
							else:
								max_ic = ic_values[value]
							ic_rule_values += max_ic
							contr_rules_values += 1
				average_ic_rules_values = float(ic_rule_values) / float(contr_rules_values)

				f_out.write(str(n_folder_app) + "\t" + str(average_ic_true_values)+ "\t" + str(average_ic_rules_values)+"\n")
				f_out.flush()
			cont_datasets += 1
			# elimina folder with info for belief propagation
			#shutil.rmtree(confidence_value_computation_info_dir)
			#os.remove(dataitem_index_file)
			print("process dataset " + str(cont_datasets) + "/20")
			#############################################################################################################
			print("process dataset " + str(cont_datasets) + "/20")
			#exit()

		# only the first level of subfolder
		cont_subfolders += 1
		#end one dataset

	f_out.close()



