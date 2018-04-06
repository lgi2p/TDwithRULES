import sys
import os
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

from TDO.utils_tdo import utils_predicate
from TDO.utils_tdo import utils_rules
from TDO.utils_tdo import utils_analysis_results

def read_file_results_trad(path_file, predicate_):
	dict_solution = dict()

	f_in = open(path_file, 'r')
	for line in f_in:
		#print(line)
		if predicate_ == 'genre':
			line = bytes(line, 'utf-8')
			line = str(line, 'unicode-escape')
		line = line.strip().split('\t')
		if len(line) != 2:
			print("error ici")
			print(line)
			exit()
		dataitem = line[0]
		sol_trad = line[1].split(" ")
		dict_solution[dataitem] = sol_trad


	return dict_solution


if __name__ == '__main__':
	# genre D:/thesis_code/TDO/ D:/results_rules_8_jan/ True True [0.1,0.9]
	predicate = sys.argv[1]
	#str_ext = "data_VALE"
	#base_dir = "D:/" + str(str_ext) + "/thesis_code/TDO/required_files/"
	base_dir = sys.argv[2]+ "required_files/"
	base_results_dir = sys.argv[3]
	Sums_and_Rules_flag = False
	if sys.argv[4] == "True":
		Sums_and_Rules_flag = True
	AdaptSums_and_Rules_flag = False
	if sys.argv[5] == "True":
		AdaptSums_and_Rules_flag = True

	if Sums_and_Rules_flag:
		base_results_dir+= "Sums_and_Rules/"
	else:
		base_results_dir += "AdaptSums_and_Rules/"
	gamma_list = (sys.argv[6][1:-1]).split(",")
	index_ = 0
	for threshold in gamma_list:
		threshold = float(threshold)
		gamma_list[index_] = threshold
		index_ += 1

	try:
		#analysis results with K = 1
		threshold_list = [0]#, 0.1, 0.2, 0.3, 0.4, 0.5]

		dataset_kind_list = ["EXP"]  #"EXP","LOW_E",
		if predicate == "birthPlace":
			str_hc = "012"  # "0.012"
		else:
			str_hc = "0.01"  # "0.012"
		prefix_str_list = ["sol_Sums_and_rules", "sol_AdaptedSums_and_rules_TSbC_"]  # , "solutions_all_children"]

		if not (utils_predicate.set_predicate(predicate)):
			print("Error in setting predicate name")
			exit()

		if predicate == "birthPlace":
			graph_file = base_dir + predicate + "/" + 'ancestors_heuristic.csv'
			path_ground_file = base_dir + predicate + "/" + 'sample_ground_grouped.csv'
			print(graph_file)
			ancestors = utils_predicate.loading_ancestors_dbpedia(graph_file)
			print("number of ancestors " + str(len(ancestors)))
			res_gt = utils_predicate.loading_ground_truth(path_ground_file)
			ground = res_gt[0]
		else:
			predicate_info = utils_predicate.loading_predicate_info(base_dir, predicate)
			ground = predicate_info[7]
			ancestors = predicate_info[2]

		dataitem_with_rules = utils_rules.get_dataitem_with_some_boosting(str_hc, base_dir, predicate)

		performances_tot_rules = dict()
		performances_tot_no_rules = dict()

		for prefix_str in prefix_str_list:
			for dataset_kind in dataset_kind_list:
				for gamma in gamma_list:
					#path_results = "C:\\results_final_no_desc\\" + str(predicate) + "\\" + str(dataset_kind)  # sys.argv[2]
					path_results = base_results_dir + str(predicate) + "/" + str(gamma) + "\\" + str(dataset_kind)
					#path_results = base_results_dir + "/results_final/" + str(predicate) + "/" + str(gamma) + "\\" + str(dataset_kind)
					print(path_results)
					n_count = 0
					performances_tot_trad = dict()
					for root, dirs, files in os.walk(path_results):
						for file_to_read in files:
							if file_to_read.startswith(prefix_str):
								id_dataset = file_to_read.replace(prefix_str, "")
								id_dataset = id_dataset.replace(".csv", "")
								if Sums_and_Rules_flag:
									solutions_dict = read_file_results_trad(str(root) + "\\" + str(file_to_read), predicate)
								else:
									if predicate == "birthPlace":
										solutions_dict = utils_analysis_results.read_file_results_rules(
											str(root) + "\\" + str(file_to_read), predicate)
										solutions_dict = solutions_dict[0][0.0]
									else:
										solutions_dict = utils_analysis_results.read_file_results_rules(
											str(root) + "\\" + str(file_to_read), predicate)
										solutions_dict = solutions_dict[0][0.0]

								if id_dataset not in performances_tot_trad: performances_tot_trad[id_dataset] = dict()

								# print("ALL CHILDREN - IC")
								cont_d = 0
								n_expected = 0
								n_general = 0
								n_error = 0
								for d in solutions_dict:
									cont_d += 1
									returned_sol_list = solutions_dict[d]
									returned_sol = returned_sol_list[0]
									expected_sol = ground[d]

									if expected_sol == returned_sol:
										n_expected += 1
									elif returned_sol in ancestors[expected_sol]:
										n_general += 1
									else:
										n_error += 1

								# print(cont_d)

								n_expected /= cont_d
								n_general /= cont_d
								n_error /= cont_d
								performances_tot_trad[id_dataset] = [n_expected, n_general, n_error]
								print(str(n_expected).replace(".", ",") + "\t" + str(n_general).replace(".",
																										",") + "\t" + str(
									n_error).replace(".", ","))

					# average
					if len(performances_tot_trad)>0:
						n_expected_average = 0
						n_general_average = 0
						n_error_average = 0

						for id_dataset in performances_tot_trad:
							n_expected_average += performances_tot_trad[id_dataset][0]
							n_general_average += performances_tot_trad[id_dataset][1]
							n_error_average += performances_tot_trad[id_dataset][2]

						n_expected_average /= len(performances_tot_trad)
						n_general_average /= len(performances_tot_trad)
						n_error_average /= len(performances_tot_trad)

						# print('precision\tSums\t' + str(predicate) + '\t' + str(dataset_kind) + '\t' + str(prec_at_k_average[1]) + '\t' + str(prec_at_k_average[2]) + '\t' + str(prec_at_k_average[3]) + '\t' + str(prec_at_k_average[4]) + '\t' + str(prec_at_k_average[5]))
						print("AVERAGE\t\tSums\t" + str(predicate) + '\t' + str(dataset_kind) + '\t' + str(
							n_expected_average).replace(".", ",") + '\t' + str(n_general_average).replace(".",
																										  ",") + '\t' + str(
							n_error_average).replace(".", ","))


	#still corr	with rules	still incorr	with rules	from corr to inc	with rules	from incorr to corr	with rules
	except:
		print("Unexpected error:", sys.exc_info()[0])
