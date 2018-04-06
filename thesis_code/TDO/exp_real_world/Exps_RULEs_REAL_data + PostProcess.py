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
import random
from SPARQLWrapper import SPARQLWrapper, JSON


def save_results(dict_solution, threshold_list, gamma_, ground):

	for thr in threshold_list:
		#print(set(dict_solution))
		f_out = open("D://out_TSbC_" + str(gamma_) + "_" + str(thr) + "_preprocessing_aft.txt" , "w", encoding="utf-8")
		for d in dict_solution[thr]:
			if d not in ground:
				continue
			if len(dict_solution[thr][d]) == 0:
				pred_sol == "None"
			else:
				pred_sol = dict_solution[thr][d][0]
			str_out = d.lower() + "birthPlace"  + "\t" + str(pred_sol) + "\n"
			f_out.write(str_out)

		for d in ground:
			if d not in dict_solution[thr]:
				str_out = d.lower() + "birthPlace" + "\tNone\n"
				f_out.write(str_out)
		f_out.flush()
		f_out.close()
	return 1

if __name__ == '__main__':
	str_hc = "0.012"
	hc_constant = 0.012

	print("_______________________________Experiments and evaluation - Script launched_______________________________")
	# input
	predicate = "birthPlace"

	k_expected = 1
	Sums_flag = False

	TSbC_flag = True
	TSaC_flag = True

	if not (utils_predicate.set_predicate(predicate)):
		print("Error in setting predicate name")
		exit()

	dir = os.path.dirname(__file__)

	# # initialization
	dir_base = dir[:dir.index("TDO")] + "TDO/"

	base_dir = dir_base + "/required_files/"  # "../datasets/"
	base_directory = dir_base
	base_dir_anal = dir_base

	#output
	model_name = "sums"
	# Constants
	initial_trustworthiness = 0.8
	initial_confidence = 1.0
	max_iteration_number = 400
	#initialization


	predicate_info = utils_predicate.loading_predicate_info(base_dir, predicate)
	ancestors = predicate_info[2]
	# predicate_info[0].clear()
	predicate_info[3].clear()

	g = predicate_info[5]

	ic_values = predicate_info[6]
	root_el = predicate_info[4]
	gc.collect()

	results_folder = base_directory + "\\results\\" + str(predicate) + "\\"
	if not os.path.exists(results_folder):
		os.makedirs(results_folder)
	solution_folder_trad_base = base_directory + "/results_final_trad/" + str(predicate) + "/"
	solution_folder_adapt_base = base_directory + "/results_final/" + str(predicate) + "/"

	# rule part##################################################
	if predicate == "birthPlace":
		rule_path = base_dir + "/rules_files/KB_tot.birthplace.out"
		rule_path_bayes_metrics = base_dir + "/rules_files/prova_bayes_rules_birthPlace.out"
	else:
		print("error")
		exit()

	load_rules_results = utils_rules.load_rules_with_threshold(rule_path, hc_constant, True, rule_path_bayes_metrics)
	R = load_rules_results[0]
	R_id = load_rules_results[1]
	R_bayes = load_rules_results[2]
	id_R = dict()
	for r in R_id:
		id_R[R_id[r]] = r
	print("regole caricate - our KB : " + str(len(R)))

	rule_desc = None
	print("elibible rule has to be found, time start " + str(datetime.datetime.now()).split('.')[0])
	cont_d = 0
	cont_zero_eligible_rules = 0

	f_in_eligible = open("eligible_rules_hc_" + str(str_hc) + "_real_world.csv", "r")
	eligible_rules = dict()
	#app_set = set()
	for line in f_in_eligible:
		if predicate == "genre":
			line = line.strip().split("\\t")
		else:
			line = line.strip().split("\t")
		d = line[0].replace("http://dbpedia.org/resource/", "").replace("_", " ") + " AND was born"#[1:-1]
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

	valid_values_for_r_and_d = utils_rules.read_valid_values_dict_real_world("valid_values_for_el_rules_hc_" + str(str_hc) + "_real_world.csv")

	initial_trustworthiness = 0.8
	initial_confidence = 1.0
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

	facts_file = 'D:\\GoogleDrive\\famous_people_claims_v1.txt'#'D:\\Google Drive\\person_birthLocation_webpage_con_codifica_vale_2.txt'  # Output FILE where the extrated claims are saved
	facts_file = "C:\\Users\\valen\\Dropbox\\thesis_code\\TDO\\real_world_dataset\\DataA.txt" #'D:\\GoogleDrive\\famous_people_claims_v3.txt'
	#facts_file = "C:\\Users\\vberetta\\Google Drive\\famous_people_claims_v1.txt"
	#facts_file = "D:\\c1_no_hub_sources_no_imdb.txt"

	#facts_file = "D:\\v3_no_hub_sources.txt"
	#facts_file = 'D:\\GoogleDrive\\famous_people_claims_CC_single_component.txt'
	#facts_file = os.path.join(dir, facts_file)

	confidence_value_computation_info_dir = "D:/real_world/confidence_value_computation_info_CC_aft1101/"
	if not os.path.exists(confidence_value_computation_info_dir): os.makedirs(
		confidence_value_computation_info_dir)
	dataitem_index_file = "D:/real_world/dataitems_index_real_world_CC_aft1101.csv"


	res_list = preprocessing_sums_model.preprocess_before_running_model_real_world("", facts_file,confidence_value_computation_info_dir,dataitem_index_file, g, ancestors)

	ground_file = "D:/GoogleDrive/ground_real_world_v2.csv"
	#ground_file = "C:\\Users\\vberetta\\Google Drive\\ground_real_world.csv"
	ground = dict()
	f_in = open(ground_file, 'r', encoding='utf-8')
	for line in f_in:
		line = line.strip().split(";")
		ground[line[0] + " AND was born"] = line[1]
	f_in.close()
	print("Number of data items in ground truth : " + str(len(ground)))
	remove_from_ground = set()
	for d in ground:
		if ground[d] not in ancestors:
			remove_from_ground.add(d)
	for d in remove_from_ground:
		del ground[d]


	if True:
		if True:
			sources_dataItemValues = res_list[2]
			print("Cardinality of data items: " + str(len(sources_dataItemValues)))
			D = res_list[3]
			F_s = res_list[4]
			S = res_list[5]
			#print("**" + str(len(S)))
			S_prop = res_list[6]
			app_conf_dict = res_list[7]
			#create source dictionary
			T = dict()
			for d in sources_dataItemValues:
				for v in sources_dataItemValues[d]:
					for s in sources_dataItemValues[d][v]:
						if s not in T:
							T[s] = 0.5

			# load facts
			header = False
			sources_dataItemValues = utils_dataset.load_facts_real_world(facts_file, header, ancestors)
			D = list(sources_dataItemValues.keys())
			# compute (1) all the facts that are claimed by a source and (2) all the sources that claim a specific fact
			# (1) set of facts that are claimed by a specific source < key = source id, value = set of facts (dataitem + value) >
			# (2) all the sources that claim a specific fact <key = dataitem + value, value = set of source ids>
			print("Info about claims .... loading")
			fact_and_source_info = utils_dataset.load_fact_and_source_info(sources_dataItemValues)
			F_s = fact_and_source_info[0]
			print("Number of sources (url domains) : " + str(len(F_s)))
			S = fact_and_source_info[1]
			print("number of claims : " + str(len(S)))
			if True:
				print("Compute boost dict propagated!")

				boost_dict_prop = utils_rules.get_propagated_boost_dict_fuseky_optimized_BAYES(sources_dataItemValues,
					                                                                         eligible_rules, R_bayes,
					                                                                         valid_values_for_r_and_d,
					                                                                         ancestors,
					                                                                         True)

				print("Adapted Sums run + RULES ")
				gamma_list =[0.3]#[0.10, 0.25, 0.5, 0.6, 0.75, 0.9, 1.0] #0, 0.25, 0.5, 0.75,
				threshold_list = [0.0, 0.001, 0.005, 0.01, 0.05, 0.1, 0.3, 0.5]
				#threshold_list = [0.0]
				for gamma_ in gamma_list:
					print("GAMMA : " + str(gamma_))
					trust_file_base = os.path.join(results_folder + "/" + str(gamma_), "dataset_real_world")
					if not os.path.exists(trust_file_base):
						os.makedirs(trust_file_base)

					trust_file_adapt_for_iter = os.path.join(trust_file_base ,
						                                         "trad_trust_est_at_eac_iter_real_world.csv")
					trust_file_adapt = os.path.join(trust_file_base, "trad_trust_est_real_world.csv")

					res_a = sums_model.run_adapted_sums_and_boost_saving_iter_real_world(copy.deepcopy(T), F_s, S_prop, initial_confidence, max_iteration_number,sources_dataItemValues, trust_file_adapt_for_iter, boost_dict_prop, gamma_, "_real_world", base_dir_anal, predicate)

					if res_a:
						T_adapt_rules = res_a[0]
						C_adapt_rules = res_a[1]

						solution_folder_adapt = solution_folder_adapt_base + str(gamma_) + "/"
						if not os.path.exists(solution_folder_adapt): os.makedirs(solution_folder_adapt)

						trust_average = utils_dataset.compute_average_trustworhiness(S_prop,
						                                                             T_adapt_rules)  # T_average is a dict with key = claim_id and

						descendants = predicate_info[1]
						ancestors = predicate_info[2]
						T_average_normalized = utils_dataset.normalize_trust_average(trust_average, ancestors,
						                                                             descendants,
						                                                             sources_dataItemValues)
						##############################################################################################################
						print("computing normalized confidence")
						conf_adapt_norm = utils_normalize_conf.creating_normalized_for_d_estimation_optimized(D,
						                                                                                      C_adapt_rules,
						                                                                                      app_conf_dict)

						#for claim in conf_adapt_norm:
						#	if "James G. Blaine AND was born" in claim:
						#		print(" *** \t" + str(claim) + "\t" + str(conf_adapt_norm[claim])+ "\t" + str(C_adapt_rules[claim]))

						gc.collect()


						for d in sources_dataItemValues: #dictionary containing for each data item, the provided values, and the sources that provide this value
							#sources_dataItemValues[key = dataitem] --> value = dict_ [key = value_1] --> value = set of sources for value_1
							#                                                   dict_ [key = value_2] --> value = set of sources for value_2
							count_dict = dict()
							for v in sources_dataItemValues[d]:  #for each provided value (and therefore its ancestors) I count how many source provided it
								for a in ancestors[v]:
									for s in sources_dataItemValues[d][v]:
										if a not in count_dict:
											count_dict[a] = 0
										count_dict[a] += 1
							for v in count_dict:
								if count_dict[v] == 1:   #when the value has been provided only by one source I put its confidence to 0.
									C_adapt_rules[d+v] = 0
									conf_adapt_norm[d+v] = 0

						if TSbC_flag:
							print(
								"Starting selection of true values algorithm for adapt model and NORMALIZED trust average.....")
							print("TESTING MODEL -- BestChildren -- delta = 0")
							first_ranking_criteria = "ic"
							second_ranking_criteria = "source_average"
							is_coherent = True
							solutions_dict = selection_algorithm.compute_solution_best_children_final_real_world(D, predicate_info,
							                                                                          C_adapt_rules,
							                                                                          conf_adapt_norm,
							                                                                          T_average_normalized,
							                                                                          "", k_expected,
							                                                                          first_ranking_criteria,
							                                                                          second_ranking_criteria, threshold_list)

							dict_solution_IC_final = solutions_dict[0]
							save_results(dict_solution_IC_final, threshold_list, gamma_, ground)
							print("Statistic dict_sol_IC for best chidlren")
							for threshold in threshold_list:
								corr = 0
								gen = 0
								more_spec = 0
								err = 0
								cont_1 = 0
								for dataitem in sources_dataItemValues:
									if dataitem not in ground:
										continue
									if dataitem not in dict_solution_IC_final[threshold]:
										cont_1 += 0
										continue
									expec_sol = ground[dataitem]
									if len(dict_solution_IC_final[threshold][dataitem]) > 0:
										pred_sol = dict_solution_IC_final[threshold][dataitem][0]
									else:
										pred_sol = "None"

									if pred_sol == expec_sol:
										corr += 1
									else:
										if expec_sol in ancestors:
											if pred_sol in ancestors[expec_sol]:
												gen += 1
											else:
												if pred_sol in ancestors:
													if expec_sol in ancestors[pred_sol]:
														more_spec+= 1
													else:
														err += 1
												else:
													err += 1
										else:
											if pred_sol in ancestors:
												if expec_sol in ancestors[pred_sol]:
													more_spec += 1
												else:
													err += 1
											else:
												err += 1

								if cont_1>0:
									print(cont_1)
								print("TSbC_IC\t"+str(threshold) + "\t" + str(round(corr / len(ground), 4)) + "\t" + str(
										round(gen / len(ground), 4))+ "\t" + str(round(more_spec / len(ground), 4)) + "\t" + str(round(err / len(ground), 4)) + "\t" + str(corr) + "\t" + str(
										gen) + "\t" + str(more_spec)+ "\t" + str(err) + "\t" + str(corr + gen + err+ more_spec) + "\t" + str(
										len(ground)))



					else:
						print("Error in adapted model")

			cont_datasets += 1
			# elimina folder with info for belief propagation

			print("End dataset ")





