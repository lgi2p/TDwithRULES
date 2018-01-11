import matplotlib.pyplot as pl
import matplotlib.image as mpimg
import os
import ast
import copy


def desing_summary(predicate, approach_name, k_expected, graph_summary_for_thr_dir, base_dir_save_fig, norm_flag_):
	if norm_flag_:
		norm_str = "_norm"
	else:
		norm_str = "not_norm"
	array_path = list()
	for k_index in range(1, k_expected+1):
		array_path.append(graph_summary_for_thr_dir + str(predicate) + '\\'+str(approach_name) +'\\k_' + str(k_index) + '\\graph_theta_disc_'+ str(norm_str) + '.png')
		array_path.append(graph_summary_for_thr_dir + str(predicate) + '\\'+str(approach_name) +'\\k_' + str(k_index) + '\\graph_theta_disc_'+ str(norm_str) + '.png')
		array_path.append(graph_summary_for_thr_dir + str(predicate) + '\\'+str(approach_name) +'\\k_' + str(k_index) + '\\graph_theta_disc_'+ str(norm_str) + '.png')
		array_path.append(graph_summary_for_thr_dir + str(predicate) + '\\'+str(approach_name) +'\\k_' + str(k_index) + '\\graph_theta_disc_'+ str(norm_str) + '.png')
	pl.clf()
	fig, axes = pl.subplots(nrows=4, ncols=5)
	fig.suptitle(predicate, fontsize=16)

	pos = 0
	for ax in axes.flat:
		path_graph = array_path[pos]
		img = mpimg.imread(path_graph)
		ax.imshow(img)
		ax.set_xticklabels([])
		ax.set_yticklabels([])
		pos+=1

	pl.subplots_adjust(wspace=0.02, hspace=0.02)

	save_image_path = base_dir_save_fig + str(predicate) + "/threshold_analysis_"+ str(predicate) + "_" + str(approach_name)+".png"
	pl.savefig(save_image_path, bbox_inches='tight', dpi=1200)
	pl.close(fig)

def graph_threshold(average_dict_k_datasetType, theta_list, save_image_path, approach_sel):
	pl.clf()
	x = list()
	for i in range(1, len(average_dict_k_datasetType)+1):
		x.append(i)
	va = list()
	va_plus = list()
	not_va_and_not_va_plus = list()
	for theta in theta_list:
		va.append(average_dict_k_datasetType[theta][0]/10000)
		va_plus.append(average_dict_k_datasetType[theta][1]/10000)
		not_va_and_not_va_plus.append(average_dict_k_datasetType[theta][2]/10000)

	ax = pl.subplot(111)
	list_label = list()
	list_App = copy.deepcopy(theta_list)
	list_label.append(0)
	list_label = list_label + list_App
	ax.set_xticklabels(list_label)
	# print("va")
	# print(va)
	# print("va_plus")
	# print(va_plus)
	# print("not va")
	# print(not_va_and_not_va_plus)
	x_1 = [i -0.2 for i in x]
	ax.bar(x_1, va, width=0.2, color='b', align='center')
	ax.bar(x, va_plus, width=0.2, color='g', align='center')
	x_2 = [i + 0.2 for i in x]
	ax.bar(x_2, not_va_and_not_va_plus, width=0.2, color='r', align='center')

	pl.title('impact of threhsold - ' +str(approach_sel))
	pl.xlabel('threshold')  # Nomi degli assi
	pl.ylabel('precision')

	pl.legend(numpoints=3)  # Legenda
	pl.legend(loc='center left', bbox_to_anchor=(1, 0.815), numpoints=1)

	pl.savefig(save_image_path, bbox_inches='tight')

def compute_average_performances_results(path_res_file, k_list, dataset_type_list, approach_sel, threshold_list):
	if approach_sel == "Adapt14" or approach_sel == "Adapt15":
		col_index = 3
	else:
		col_index = 4
	res_for_dataset_type = dict()
	for item in dataset_type_list:
		res_for_dataset_type[item] = dict()
	f_in = open(path_res_file, 'r')
	for line in f_in:
		line = line.strip().split('\t')
		if len(line) != 5:
			print("error in results file "+str(path_res_file))
			exit()
		res_for_dataset_type[line[2]][line[1]] = ast.literal_eval(line[col_index])

	#sum up and average
	average_dict = dict()
	for k in k_list:
		k = int(k)
		type_average_list = dict()
		for type_d in res_for_dataset_type:

			threshold_average_list = dict()
			for threshold_index in range(0, len(threshold_list)):

				sum_for_type = [0,0,0]
				for dataset_id in res_for_dataset_type[type_d]:
					single_list = res_for_dataset_type[type_d][dataset_id][threshold_index][k-1]
					for index in range(0, len(sum_for_type)):
						sum_for_type[index] += single_list[index]
				average_score = [x /float(len(res_for_dataset_type[type_d])) for x in sum_for_type]
				threshold_average_list[threshold_list[threshold_index]] = average_score

			type_average_list[type_d] = threshold_average_list
		average_dict[k] = type_average_list
	return average_dict

def graph_for_predicate_v2(precision_k, selection_strategies, save_image_path):
	x = [1, 2, 3, 4, 5]  # Crea un array dei valori x1
	format_dish = dict()
	format_dish["Sums"] = 'Db-'
	format_dish["adapt_11"] = '^g-'
	format_dish["adapt_15"] = 'om-'
	format_dish["adapt_10"] = 'xy-'
	format_dish["adapt_14"] = 'sr-'
	rename_dict = dict()
	rename_dict["Sums"] = "Sums"
	rename_dict["adapt_11"] = "Model A"
	rename_dict["adapt_15"] = "Model B"
	rename_dict["adapt_10"] = "Model C"
	rename_dict["adapt_14"] = "Model D"
	selection_strategies = ["Sums", "adapt_11","adapt_15","adapt_10","adapt_14" ]
	pl.clf()

	ax = pl.subplot(131)

	for selection_strategy in selection_strategies:
		y = list()
		for k in x:
			y.append(precision_k[selection_strategy][k]["EXP"][0])
		ax.plot(x, y, format_dish[selection_strategy], label=rename_dict[selection_strategy])  # Usa pylab per tracciare con  x1,y1


	pl.title('EXP')
	pl.xlabel('top_k')  # Nomi degli assi
	pl.ylabel('precision')
	pl.xlim(0.0, 6)  # Imposta limiti degli assi
	pl.ylim(0.0, 1.0)

	ax = pl.subplot(132)
	for selection_strategy in selection_strategies:
		#y = precision_k[selection_strategy]["LOW_E"]
		y = list()
		for k in x:
			y.append(precision_k[selection_strategy][k]["LOW_E"][0])
		ax.plot(x, y, format_dish[selection_strategy], label=rename_dict[selection_strategy])  # Usa pylab per tracciare con  x1,y1

	pl.title('LOW_E')
	pl.xlabel('top_k')  # Nomi degli assi
	pl.ylabel('precision')
	# pl.legend(numpoints=3)  # Legenda
	# pl.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
	pl.xlim(0.0, 6)  # Imposta limiti degli assi
	pl.ylim(0.0, 1.0)

	ax = pl.subplot(133)
	for selection_strategy in selection_strategies:
		y = list()
		for k in x:
			y.append(precision_k[selection_strategy][k]["UNI"][0])
		ax.plot(x, y, format_dish[selection_strategy], label=rename_dict[selection_strategy])  # Usa pylab per tracciare con  x1,y1

	pl.title('UNI')
	pl.xlabel('top_k')  # Nomi degli assi
	pl.ylabel('precision')
	# pl.legend(numpoints=3)  # Legenda
	# pl.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
	pl.xlim(0.0, 6)  # Imposta limiti degli assi
	pl.ylim(0.0, 1.0)



	pl.tight_layout()

	# Shrink current axis by 20%
	box = ax.get_position()
	ax.set_position([box.x0, box.y0, box.width * 1, box.height])

	# Put a legend to the right of the current axis
	#ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size':10})
	# Place a legend above this subplot, expanding itself to
	# fully use the given bounding box.
	#ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
	#           ncol=2, mode="expand", borderaxespad=0.)
	#labels = ax.get_xticklabels()
	#setp(labels, rotation=60, fontsize=8)

	pl.legend(numpoints=3)  # Legenda
	pl.legend(loc='center left', bbox_to_anchor=(1, 0.815), numpoints=1)

	pl.savefig(save_image_path, bbox_inches='tight')


def graph_for_predicate_v3(useful_cont_results_for_theta, save_image_path, trad_performances):



	x = [1, 2, 3, 4, 5]  # Crea un array dei valori x1

	pl.clf()

	ax = pl.subplot(131)
	#for EXP
	ax.plot(x, trad_performances["EXP"], label="Sums")
	for selection_strategy in useful_cont_results_for_theta["EXP"]:
		y_app = useful_cont_results_for_theta["EXP"][selection_strategy]
		y = list()
		for item in x:
			y.append(y_app[item]/10000)
		ax.plot(x, y, label=selection_strategy)  # Usa pylab per tracciare con  x1,y1


	pl.title('EXP')
	pl.xlabel('top_k')  # Nomi degli assi
	pl.ylabel('precision')
	pl.xlim(0.0, 6)  # Imposta limiti degli assi
	pl.ylim(0.0, 1.0)

	ax = pl.subplot(132)
	ax.plot(x, trad_performances["LOW_E"], label="Sums")
	for selection_strategy in useful_cont_results_for_theta["LOW_E"]:
		y_app = useful_cont_results_for_theta["LOW_E"][selection_strategy]
		y = list()
		for item in x:
			y.append(y_app[item]/10000)
		ax.plot(x, y, label=selection_strategy)  # Usa pylab per tracciare con  x1,y1

	pl.title('LOW_E')
	pl.xlabel('top_k')  # Nomi degli assi
	pl.ylabel('precision')
	# pl.legend(numpoints=3)  # Legenda
	# pl.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
	pl.xlim(0.0, 6)  # Imposta limiti degli assi
	pl.ylim(0.0, 1.0)

	ax = pl.subplot(133)
	ax.plot(x, trad_performances["UNI"], label="Sums")
	for selection_strategy in useful_cont_results_for_theta["UNI"]:
		y_app = useful_cont_results_for_theta["UNI"][selection_strategy]
		y = list()
		for item in x:
			y.append(y_app[item]/10000)
		ax.plot(x, y, label=selection_strategy)  # Usa pylab per tracciare con  x1,y1

	pl.title('UNI')
	pl.xlabel('top_k')  # Nomi degli assi
	pl.ylabel('precision')
	# pl.legend(numpoints=3)  # Legenda
	# pl.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
	pl.xlim(0.0, 6)  # Imposta limiti degli assi
	pl.ylim(0.0, 1.0)



	pl.tight_layout()

	# Shrink current axis by 20%
	box = ax.get_position()
	ax.set_position([box.x0, box.y0, box.width * 1, box.height])

	# Put a legend to the right of the current axis
	#ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size':10})
	# Place a legend above this subplot, expanding itself to
	# fully use the given bounding box.
	#ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
	#           ncol=2, mode="expand", borderaxespad=0.)
	#labels = ax.get_xticklabels()
	#setp(labels, rotation=60, fontsize=8)

	pl.legend(numpoints=3)  # Legenda
	pl.legend(loc='center left', bbox_to_anchor=(1, 0.815), numpoints=1)

	pl.savefig(save_image_path, bbox_inches='tight')

def read_average_performances_results_file(file_path):
	dict_precision_at_k = dict()  # for dataset KIND
	print("read from performance results file ...")
	f_in = open(file_path, "r")

	for line in f_in:
		line = line.strip()
		line = line.split('\t')
		if len(line) != 2:
			print("Error in reading file of results")
			print(line)
			exit()
		key = ""
		if "EXP" in line[0]:
			key = "EXP"
		else:
			if "LOW_E" in line[0]:
				key = "LOW_E"
			else:
				if "UNI" in line[0]:
					key = "UNI"
		precision_list = list()
		line[1] = line[1][1:-1]
		for str_line in line[1].split(', '):
			precision_list.append(float(str_line)/10000)
		dict_precision_at_k[key] = precision_list
	f_in.close()
	if "EXP" not in dict_precision_at_k:
		precision_list = [0, 0, 0, 0, 0]
		dict_precision_at_k["EXP"] = precision_list
	if "LOW_E" not in dict_precision_at_k:
		precision_list = [0, 0, 0, 0, 0]
		dict_precision_at_k["LOW_E"] = precision_list
	if "UNI" not in dict_precision_at_k:
		precision_list = [0, 0, 0, 0, 0]
		dict_precision_at_k["UNI"] = precision_list

	return dict_precision_at_k

def compute_average_performances_results_file(file_path, k_expected):
	dict_precision_at_k = dict()  # for dataset KIND
	print("read from performance results file ...")
	f_in = open(file_path, "r")

	for line in f_in:
		line = line.strip()
		line = line.split('\t')
		if len(line) != 5:
			print("Error in reading file of results")
			print(line)
			exit()
		key = ""
		if "EXP" in line[2]:
			key = "EXP"
		else:
			if "LOW_E" in line[2]:
				key = "LOW_E"
			else:
				if "UNI" in line[2]:
					key = "UNI"
		if key not in dict_precision_at_k:
			dict_precision_at_k[key] = list()
		precision_list = list()
		line[4] = line[4][1:-1].replace("[","").replace("]", "")
		for str_line in line[4].split(', '):
			precision_list.append(float(str_line))
		dict_precision_at_k[key].append(precision_list)

	f_in.close()
	if "EXP" not in dict_precision_at_k:
		precision_list = [0, 0, 0, 0, 0]
		dict_precision_at_k["EXP"] = precision_list
	if "LOW_E" not in dict_precision_at_k:
		precision_list = [0, 0, 0, 0, 0]
		dict_precision_at_k["LOW_E"] = precision_list
	if "UNI" not in dict_precision_at_k:
		precision_list = [0, 0, 0, 0, 0]
		dict_precision_at_k["UNI"] = precision_list
	average_at_k = dict()
	for key in dict_precision_at_k:

		sum_at_k = [0,0,0,0,0]
		for id_dataset in range(0, len(dict_precision_at_k[key])):
			for k_index in range(0,k_expected):
				sum_at_k[k_index] +=dict_precision_at_k[key][id_dataset][k_index]
		for n in range(0, len(sum_at_k)):
			sum_at_k[n] /= float(len(dict_precision_at_k[key]))
		average_at_k[key] = sum_at_k
	return average_at_k

def compute_average_precision_results_file(file_path, k_expected):
	dict_precision_at_k = dict()  # for dataset KIND
	print("read from performance results file ...")
	f_in = open(file_path, "r")

	for line in f_in:
		line = line.strip()
		line = line.split('\t')
		if len(line) != 5:
			print("Error in reading file of results")
			print(line)
			exit()
		key = ""
		if "EXP" in line[2]:
			key = "EXP"
		else:
			if "LOW_E" in line[2]:
				key = "LOW_E"
			else:
				if "UNI" in line[2]:
					key = "UNI"
		if key not in dict_precision_at_k:
			dict_precision_at_k[key] = list()
		precision_list = list()
		line[4] = line[4][1:-1].replace("[","").replace("]", "")
		for str_line in line[4].split(', '):
			precision_list.append(float(str_line))
		dict_precision_at_k[key].append(precision_list)

	f_in.close()
	if "EXP" not in dict_precision_at_k:
		precision_list = [0, 0, 0, 0, 0]
		dict_precision_at_k["EXP"] = precision_list
	if "LOW_E" not in dict_precision_at_k:
		precision_list = [0, 0, 0, 0, 0]
		dict_precision_at_k["LOW_E"] = precision_list
	if "UNI" not in dict_precision_at_k:
		precision_list = [0, 0, 0, 0, 0]
		dict_precision_at_k["UNI"] = precision_list
	average_at_k = dict()

	k_expected =1
	for key in dict_precision_at_k:

		sum_at_k = [0,0,0,0,0]
		for id_dataset in range(0, len(dict_precision_at_k[key])):
			for k_index in range(0,k_expected):
				sum_at_k[k_index] +=dict_precision_at_k[key][id_dataset][k_index]
		for n in range(0, len(sum_at_k)):
			sum_at_k[n] /= float(len(dict_precision_at_k[key]))
		average_at_k[key] = sum_at_k
	return average_at_k

def loading_configuration_setup(conf_file_path, base_res_dir, predicate_):
	path_dir = dict()
	path_dir["Sums"] = base_res_dir + "/trad_perf_res_" + str(predicate_) + ".csv"
	f_conf = open(conf_file_path, 'r')
	header = True
	for line in f_conf:
		if header:
			header = False
			continue
		if line.startswith("#"):
			continue
		line = line.strip().split('\t')
		print(line)
		name_id = line[0]
		delta_path = line[1]
		ord_or_not = line[2]
		first_criteria_ = line[3]
		second_criteria_ = line[4]
		threshold = line[5]
		if norm:
			path_dir[name_id] = "../results/conf_evaluations/" + str(predicate_) + "/delta_" + str(
				delta_path) + "_" + ord_or_not + "/" + str(first_criteria_) + "_" + str(second_criteria_) \
								+ "/theta_" + str(threshold) + "/adapt_perf_res_" + str(predicate_) + "_norm.csv"
		else:
			path_dir[name_id] = "../results/conf_evaluations/" + str(predicate_) + "/delta_" + str(
				delta_path) + "_" + ord_or_not + "/" + str(second_criteria_) + "_" + str(first_criteria_) \
								+ "/theta_" + str(threshold) + "/adapt_perf_res_" + str(predicate_) + "_not_norm.csv"
	f_conf.close()

	return path_dir

def old_main():

	predicates = ["CC"]#, "BP", "MF", "birthPlace", "genre"]
	results_dir = "./performance_results/"
	precision_k = dict()  #precision_k is a dict : <[model_name], subdict_at_k is a dict <dataset_kind, [list with k precision level]
	selection_strategies = ["Sums", "Adapt1", "Adapt2", "Adapt3", "Adapt4", "Adapt5", "Adapt6", "Adapt7", "Adapt8"]
	selection_strategies = ["Sums", "Adapt1"]
	graph_dir = ".average_summary/"
	if not os.path.exists(graph_dir): os.makedirs(graph_dir)

	for predicate in predicates:
		results_dir += str(predicate)
		trad_file_path = results_dir + "/True/param_0_1_source_average_ic/average_trad_perf_res_" + str(predicate) + ".csv"
		name_file_adapt = "average_adapt_perf_res_" + str(predicate) + ".csv"
		adapt_1_file_path = results_dir + "/True/param_0_1_source_average_ic/" + name_file_adapt
		adapt_2_file_path = results_dir + "/True/param_0_0_source_average_ic/" + name_file_adapt
		adapt_3_file_path = results_dir + "/False/param_0_1_source_average_ic/" + name_file_adapt
		adapt_4_file_path = results_dir + "/False/param_0_0_source_average_ic/" + name_file_adapt
		adapt_5_file_path = results_dir + "/True/param_0_1_ic_source_average/" + name_file_adapt
		adapt_6_file_path = results_dir + "/True/param_0_0_ic_source_average/" + name_file_adapt
		adapt_7_file_path = results_dir + "/False/param_0_1_ic_source_average/" + name_file_adapt
		adapt_8_file_path = results_dir + "/False/param_0_0_ic_source_average/" + name_file_adapt

		precision_k["Sums"] = read_average_performances_results_file(trad_file_path)
		precision_k["Adapt1"] = read_average_performances_results_file(adapt_1_file_path)
		#precision_k["Adapt2"] = read_average_performances_results_file(adapt_2_file_path)
	   # precision_k["Adapt3"] = read_average_performances_results_file(adapt_3_file_path)
		#precision_k["Adapt4"] = read_average_performances_results_file(adapt_4_file_path)
		#precision_k["Adapt5"] = read_average_performances_results_file(adapt_5_file_path)
		#precision_k["Adapt6"] = read_average_performances_results_file(adapt_6_file_path)
		#precision_k["Adapt7"] = read_average_performances_results_file(adapt_7_file_path)
		#precision_k["Adapt8"] = read_average_performances_results_file(adapt_8_file_path)

		save_image_path= graph_dir + "graph_total_"  + str(predicate) + ".png"
		graph_for_predicate_v2(precision_k, selection_strategies, save_image_path)


def compute_average_precision_trad_results(file_path, k_expected, tot_dataitems):
	dict_precision_at_k = dict()  # for dataset KIND
	print("read from performance results file ...")
	f_in = open(file_path, "r")

	for line in f_in:
		line = line.strip()
		line = line.split('\t')
		if len(line) != 5:
			print("Error in reading file of results")
			print(line)
			exit()
		key = ""
		if "EXP" in line[2]:
			key = "EXP"
		else:
			if "LOW_E" in line[2]:
				key = "LOW_E"
			else:
				if "UNI" in line[2]:
					key = "UNI"
		if key not in dict_precision_at_k:
			dict_precision_at_k[key] = dict()
		precision_list = list()
		line[4] = line[4][1:-1].replace("[","").replace("]", "")
		for str_line in line[4].split(', '):
			precision_list.append(float(str_line))
		id_dataset = line[1]#.replace("_", "")
		dict_precision_at_k[key][id_dataset] = precision_list

	f_in.close()
	if "EXP" not in dict_precision_at_k:
		precision_list = [0, 0, 0, 0, 0]
		dict_precision_at_k["EXP"] = precision_list
	if "LOW_E" not in dict_precision_at_k:
		precision_list = [0, 0, 0, 0, 0]
		dict_precision_at_k["LOW_E"] = precision_list
	if "UNI" not in dict_precision_at_k:
		precision_list = [0, 0, 0, 0, 0]
		dict_precision_at_k["UNI"] = precision_list
	average_at_k = dict()
	for key in dict_precision_at_k:

		sum_at_k = [0, 0, 0, 0, 0]
		for id_dataset in dict_precision_at_k[key]:
			for k_index in range (0, len(sum_at_k)):
				sum_at_k[k_index] += (dict_precision_at_k[key][id_dataset][k_index] / tot_dataitems[key][id_dataset])
		for n in range(0, len(sum_at_k)):
			sum_at_k[n] /= float(len(dict_precision_at_k[key]))
		for k_index in range(0, len(sum_at_k)):
			if k_index+1 not in average_at_k:
				average_at_k[k_index+1] = dict()
			if key not in average_at_k[k_index+1]:
				average_at_k[k_index+1][key]= dict()
			average_at_k[k_index+1][key][0] = sum_at_k[k_index]
	return average_at_k


def compute_average_precision_results(path_res_file, k_list, dataset_type_list, approach_sel, threshold_list):
	if approach_sel == "adapt_14" or approach_sel == "adapt_15":
		col_index = 3
	else:
		col_index = 4
	res_for_dataset_type = dict()
	for item in dataset_type_list:
		res_for_dataset_type[item] = dict()
	f_in = open(path_res_file, 'r')
	for line in f_in:
		line = line.strip().split('\t')
		if len(line) != 5:
			print("error in results file "+str(path_res_file))
			exit()
		res_for_dataset_type[line[2]][line[1]] = ast.literal_eval(line[col_index])

	#sum up and average
	average_dict = dict()
	for k in k_list:
		k = int(k)
		type_average_list = dict()
		for type_d in res_for_dataset_type:

			threshold_average_list = dict()
			for threshold_index in range(0, len(threshold_list)):

				sum_ = 0
				for dataset_id in res_for_dataset_type[type_d]:
					single_list = res_for_dataset_type[type_d][dataset_id][threshold_index][k-1]
					prec = single_list[0] / sum(single_list)
					sum_ += prec
				average_score = sum_ /float(len(res_for_dataset_type[type_d]))
				threshold_average_list[threshold_list[threshold_index]] = average_score

			type_average_list[type_d] = threshold_average_list
		average_dict[k] = type_average_list
	return average_dict


def compute_tot_dataitem_from_results(path_res_file, k_list, dataset_type_list, approach_sel, threshold_list):
	if approach_sel == "adapt14" or approach_sel == "adapt15":
		col_index = 3
	else:
		col_index = 4
	res_for_dataset_type = dict()
	for item in dataset_type_list:
		res_for_dataset_type[item] = dict()
	f_in = open(path_res_file, 'r')
	for line in f_in:
		line = line.strip().split('\t')
		if len(line) != 5:
			print("error in results file "+str(path_res_file))
			exit()
		res_for_dataset_type[line[2]][line[1]] = ast.literal_eval(line[col_index])

	#sum up and average
	tot_dataitem_dict = dict()
	k = 1

	for type_d in res_for_dataset_type:
		tot_dataitem_dict[type_d] = dict()
		threshold_index = 0

		for dataset_id in res_for_dataset_type[type_d]:
			single_list = res_for_dataset_type[type_d][dataset_id][threshold_index][k-1]
			tot_d = sum(single_list)
			tot_dataitem_dict[type_d][dataset_id] = tot_d

	return tot_dataitem_dict

def cm2inch(value):
	return value / 2.54

if __name__ == '__main__':

	import numpy as np
	import matplotlib.pyplot as plt
	# red dashes, blue squares and green triangles

	t = [1,2,3,4]
	t = np.arange(len(t))

	t_low = [50, 30, 20, 20]

	t = np.arange(0., 5., 0.2)
	#t_exp = [70, 30, 20, 0]
	t_uni = [30, 30, 30, 30]
	#plt.plot( 'ro--', t, t_low, 'bs--', t, t_uni, 'g^--', label='y1', label='y1', label='y1', linewidth=0.5)
	list_X = ["Hard Tecnho", "Techno", "Electronic", "Musical Genre"]
	#plt.xlabel('Radius/Side')
	plt.figure(figsize=(cm2inch(16.8), cm2inch(4.1)))

	t_low = t ** 2.3
	t_low = t_low[::-1]
	plt.plot(t, (t / t * 10)[::-1] , marker='o', linestyle='--', color='r', label='EXP', linewidth=0.5)
	plt.plot(t, t_low, marker='s', linestyle='--', color='b', label='LOW_E', linewidth=0.5)
	plt.plot(t, (t**3)[::-1], marker='^', linestyle='--', color='g', label='UNI', linewidth=0.5)
	leg = plt.legend()
	plt.ylabel('source #')
	#plt.xticks(np.arange(x), list_X)





	plt.savefig('leg_example')
	plt.show()
	graph_dir = "../graph_summary_norm/"
	if not os.path.exists(graph_dir):
		os.makedirs(graph_dir)
	norm_flag = True
	predicates = ["genre", "MF", "birthPlace", "CC", "BP"]
	name_models = ["Adapt10", "Adapt11", "Adapt14", "Adapt15"]
	precision_k = dict()  #precision_k is a dict : <[model_name], subdict_at_k is a dict <dataset_kind, [list with k precision level]
	graph_summary_for_thr_dir = 'D:\\thesis_code\\TDO\\graph_summary_norm\\'
	'''
	for predicate in predicates:
		print(predicate)
		for name in name_models:
			print("----" + str(name))
			desing_summary(predicate, name, 5, graph_summary_for_thr_dir, graph_dir, norm_flag)#predicate, approach_name, k_expected, graph_summary_for_thr_dir, base_dir_save_fig

	graph_dir = "../graph_summary/"
	norm_flag = False
	predicates = ["birthPlace", "genre", "CC", "BP", "MF"]
	name_models = ["Adapt10", "Adapt11", "Adapt14", "Adapt15"]
	precision_k = dict()  # precision_k is a dict : <[model_name], subdict_at_k is a dict <dataset_kind, [list with k precision level]
	graph_summary_for_thr_dir = 'D:\\thesis_code\\TDO\\graph_summary\\'

	for predicate in predicates:
		print(predicate)
		for name in name_models:
			print("----" + str(name))
			desing_summary(predicate, name, 5, graph_summary_for_thr_dir,
						   graph_dir,norm_flag)  # predicate, approach_name, k_expected, graph_summary_for_thr_dir, base_dir_save_fig


	exit()
	'''
	if not os.path.exists(graph_dir): os.makedirs(graph_dir)
	norm = True

	for predicate in predicates:
		conf_file_path_ = "../experiment_configurations_" + str(predicate) + ".txt"
		base_res_dir = "../results/conf_evaluations/" + str(predicate)
		print(conf_file_path_)
		path_dir = loading_configuration_setup(conf_file_path_, base_res_dir, predicate)

		predicate_k = dict()
		dataset_type_list = ["EXP", "LOW_E", "UNI"]
		threshold_list = [0]#,0.1,0.2,0.3,0.4,0.5]
		tot_dataitems = compute_tot_dataitem_from_results(path_dir["adapt_15"], [1, 2, 3, 4, 5], dataset_type_list,
		                                                  "adapt_15", threshold_list)
		for conf_name in path_dir:
			if conf_name != "Sums":
				precision_k[conf_name] = compute_average_precision_results(path_dir[conf_name], [1,2,3,4,5], dataset_type_list, conf_name, threshold_list)#read_average_performances_results_file(path_dir[conf_name])
			else:
				precision_k[conf_name] = compute_average_precision_trad_results(path_dir[conf_name], 1, tot_dataitems)
		selection_strategies = list(path_dir)

		if norm:
			save_image_path = graph_dir + "graph_total_" + str(predicate) + "_norm.png"
		else:
			save_image_path = graph_dir + "graph_total_" + str(predicate) + "_not_norm.png"
		graph_for_predicate_v2(precision_k, selection_strategies, save_image_path)

		for conf_name in path_dir:
			print(str(predicate) + "\t" + str(conf_name) + "\t" +  str(precision_k[conf_name][1]["EXP"][0]) + "\t" +  str(precision_k[conf_name][1]["LOW_E"][0])+ "\t" +  str(precision_k[conf_name][1]["UNI"][0]))
