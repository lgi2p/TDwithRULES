import os
import shutil
import sys
cwd = os.getcwd()
if ("TDO") in cwd:
	index_tdo = cwd.index("TDO")
	cwd = cwd[:index_tdo]
	sys.path.append(cwd)
	from TDO.utils_tdo import utils_taxonomy
	from TDO.utils_tdo import utils_dataset
else:
	sys.path.append('D:/Dropbox/thesis_code/TDO')
	from utils_tdo import utils_taxonomy
	from utils_tdo import utils_dataset


def preprocess_before_running_model(source_file_, facts_file_, confidence_value_computation_info_dir_,
									dataitem_index_file_, g_):
	# load source information
	header = False  # dictionary with the original trustworthiness
	T_actual_ = utils_dataset.load_sources_info(source_file_, header)
	T_ = utils_dataset.load_sources_info(source_file_, header)
	print(str(len(T_)) + " sources loaded")
	# load fact information
	header = True
	sources_dataItemValues_ = utils_dataset.load_facts(facts_file_, header)
	# load data item set
	D_ = list(sources_dataItemValues_.keys())

	# compute (1) all the facts that are claimed by a source and (2) all the sources that claim a specific fact
	# (1) set of facts that are claimed by a specific source < key = source id, value = set of facts (dataitem + value) >
	# (2) all the sources that claim a specific fact <key = dataitem + value, value = set of source ids>
	print("Fact loading")
	fact_and_source_info_ = utils_dataset.load_fact_and_source_info(sources_dataItemValues_)
	F_s_ = fact_and_source_info_[0]
	S_ = fact_and_source_info_[1]

	print(
		"Computing sources for " + str(len(sources_dataItemValues_)) + " data items FOR COMPUTATION PURPOSE")
	if not (len(os.listdir(confidence_value_computation_info_dir_)) == len(D_)):
		# compute the files for belief propagation information
		print("graph nodes " + str(len(g_.nodes)))
		print("LENGH source data item values" + str(len(sources_dataItemValues_.values())))
		res = utils_taxonomy.create_value_info_computation(g_, sources_dataItemValues_, dataitem_index_file_,
																  confidence_value_computation_info_dir_)
		print("LENGH source data item values dopo prop" + str(len(sources_dataItemValues_.values())))
		sources_dataItemValues_.clear()
		header = True
		sources_dataItemValues_ = utils_dataset.load_facts(facts_file_, header)
		print("LENGH source data item values dopo reload" + str(len(sources_dataItemValues_.values())))
		if res:
			print("Computation DONE")
	# else: the files for contained the info for the belief propagation have been already computed
	# then load the relative dataitem id for using the files
	dataitem_ids_ = utils_dataset.load_dataitem_ids(dataitem_index_file_)
	# load the information
	dataitem_values_info_ = utils_dataset.load_all_dataitem_values_confidence_infos_low_memory(dataitem_ids_,
																									  confidence_value_computation_info_dir_,
																									  sources_dataItemValues_)
	# S_prop is a dictionary contained for each fact all the sources that it has to take into account for leveraging the belief propagation framework
	S_prop_ = dataitem_values_info_[2]
	app_conf_dict_ = dataitem_values_info_[3]
	app_source_dict_ = dataitem_values_info_[4]
	# delete folder confidence_value_computation_info_dir_ and the relative index file
	#shutil.rmtree(confidence_value_computation_info_dir_)
   # os.remove(dataitem_index_file_)

	return [T_, T_actual_, sources_dataItemValues_, D_, F_s_, S_, S_prop_, app_conf_dict_, app_source_dict_]


def preprocess_before_running_model_only_trad(source_file_, facts_file_):
	# load source information
	header = False  # dictionary with the original trustworthiness
	T_ = utils_dataset.load_sources_info(source_file_, header)
	print(str(len(T_)) + " sources loaded")
	# load fact information
	header = True
	sources_dataItemValues_ = utils_dataset.load_facts(facts_file_, header)
	# load data item set

	# compute (1) all the facts that are claimed by a source and (2) all the sources that claim a specific fact
	# (1) set of facts that are claimed by a specific source < key = source id, value = set of facts (dataitem + value) >
	# (2) all the sources that claim a specific fact <key = dataitem + value, value = set of source ids>
	print("Fact loading")
	fact_and_source_info_ = utils_dataset.load_fact_and_source_info(sources_dataItemValues_)
	F_s_ = fact_and_source_info_[0]
	S_ = fact_and_source_info_[1]


	sources_dataItemValues_.clear()
	header = True
	sources_dataItemValues_ = utils_dataset.load_facts(facts_file_, header)

	return [T_, sources_dataItemValues_, F_s_, S_]

def preprocess_before_running_model_real_world(source_file_, facts_file_, confidence_value_computation_info_dir_,
									dataitem_index_file_, g_, ancestors_):

	# load fact information
	header = False
	sources_dataItemValues_ = utils_dataset.load_facts_real_world(facts_file_, header, ancestors_)
	# removing data item for which there are values not contained in ancestors

	#print("New cardinality : " + str(len(sources_dataItemValues_)))

	# load data item set
	D_ = list(sources_dataItemValues_.keys())

	# compute (1) all the facts that are claimed by a source and (2) all the sources that claim a specific fact
	# (1) set of facts that are claimed by a specific source < key = source id, value = set of facts (dataitem + value) >
	# (2) all the sources that claim a specific fact <key = dataitem + value, value = set of source ids>
	print("Fact loading")
	fact_and_source_info_ = utils_dataset.load_fact_and_source_info(sources_dataItemValues_)
	F_s_ = fact_and_source_info_[0]
	S_ = fact_and_source_info_[1]

	print(
		"Computing sources for " + str(len(sources_dataItemValues_)) + " data items FOR COMPUTATION PURPOSE")
	if not (len(os.listdir(confidence_value_computation_info_dir_)) == len(D_)):
		# compute the files for belief propagation information
		print("graph nodes " + str(len(g_.nodes)))
		print("LENGH source data item values" + str(len(sources_dataItemValues_.values())))
		res = utils_taxonomy.create_value_info_computation(g_, sources_dataItemValues_, dataitem_index_file_,
																  confidence_value_computation_info_dir_)
		print("LENGH source data item values dopo prop" + str(len(sources_dataItemValues_.values())))
		sources_dataItemValues_.clear()
		header = False
		sources_dataItemValues_ = utils_dataset.load_facts_real_world(facts_file_, header, ancestors_)

		print("LENGH source data item values dopo reload" + str(len(sources_dataItemValues_.values())))
		if res:
			print("Computation DONE")
	# else: the files for contained the info for the belief propagation have been already computed
	# then load the relative dataitem id for using the files
	dataitem_ids_ = utils_dataset.load_dataitem_ids(dataitem_index_file_)
	# load the information
	dataitem_values_info_ = utils_dataset.load_all_dataitem_values_confidence_infos_low_memory(dataitem_ids_,
																									  confidence_value_computation_info_dir_,
																									  sources_dataItemValues_)
	# S_prop is a dictionary contained for each fact all the sources that it has to take into account for leveraging the belief propagation framework
	S_prop_ = dataitem_values_info_[2]
	app_conf_dict_ = dataitem_values_info_[3]
	app_source_dict_ = dataitem_values_info_[4]


	return [None, None, sources_dataItemValues_, D_, F_s_, S_, S_prop_, app_conf_dict_, app_source_dict_]


