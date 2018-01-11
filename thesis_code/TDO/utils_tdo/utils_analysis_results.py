import os
from TDO.utils_tdo import utils_dataset
from TDO.utils_tdo import utils_writing_results

def read_file_results_rules_birth(path_file, predicate_):
	dict_solution_TRUST = dict()
	dict_solution_IC = dict()

	f_in  = open(path_file, 'r')
	for line in f_in:
		sol_IC = list()
		if predicate_ == 'genre':
			line = bytes(line, 'utf-8')
			line = str(line, 'unicode-escape')
		line = line.strip().split('\t')
		if len(line) > 2:
			print("error ici")
			print(line)
			exit()
		threshold = 0
		dataitem = line[0]
		if len(line) == 1:
			sol_IC = "None"

		else:
			sol_IC_app = line[1].replace(" ", "")
			sol_IC.append(sol_IC_app)
		if threshold not in dict_solution_IC:
			dict_solution_IC[threshold] = dict()
		dict_solution_IC[threshold][dataitem] = sol_IC

	return dict_solution_IC


def read_file_results_rules(path_file, predicate_):
	dict_solution_TRUST = dict()
	dict_solution_IC = dict()

	f_in  = open(path_file, 'r')
	for line in f_in:
		if predicate_ == 'genre':
			line = bytes(line, 'utf-8')
			line = str(line, 'unicode-escape')
		line = line.strip().split('\t')
		if len(line) != 4 and len(line) != 2:
			print("error ici")
			print(line)
			exit()
		threshold = float(line[0])
		dataitem = line[1]

		if len(line) == 2:
			sol_IC = "None"
			sol_TRUST = "None"
		else:
			sol_IC = line[2].split(" ")
			sol_TRUST = line[3].split(" ")
		if threshold not in dict_solution_IC:
			dict_solution_IC[threshold] = dict()
		dict_solution_IC[threshold][dataitem] = sol_IC
		if threshold not in dict_solution_TRUST:
			dict_solution_TRUST[threshold] = dict()
		dict_solution_TRUST[threshold][dataitem] = sol_TRUST

	return [dict_solution_IC, dict_solution_TRUST]

def compute_error_rate_for_trustworthiness(T, T_estimated):
    #print("flushing the trust result comparison into file.....")
    try:
        error_rate = dict()
        for source_id in T:
            v_act = T[source_id]
            v_est = T_estimated[source_id]
            est_vs_act = abs(v_act - v_est)
            error_rate[source_id] = est_vs_act

        return error_rate
    except:
        print("Errors in computing trust error rate")
        return None


def analysis_trustworthiness_estimations(dataset_dir, dir_path, output_error_rate_dir):

    if not os.path.exists(output_error_rate_dir): os.makedirs(output_error_rate_dir)

    for root, dirs, files in os.walk(dir_path):
        if ["EXP", "LOW_E", "UNI"] == dirs: continue
        if ["EXP"] == dirs: continue
        if ["UNI"] == dirs: continue
        if ["LOW_E"] == dirs: continue
        if root.count('/') != 3: continue

        for dir_name in dirs:
            #print("dir name :" + str(dir_name))
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
                subfolder_path_results = "UNI/"
                subfolder_path = "UNI/dataset" + str(n_folder_app) + "/"
                source_file = dataset_dir + "/UNI/dataset" + str(n_folder_app) + "/Output_acc_" + str(
                    n_dataset) + ".txt"

            if "EXP" in root:
                subfolder_path_results = "EXP/"
                subfolder_path = "EXP/dataset" + str(n_folder_app) + "/"
                source_file = dataset_dir + "/EXP/dataset" + str(n_folder_app) + "/Output_acc_" + str(
                    n_dataset) + ".txt"

            if "LOW_E" in root:
                subfolder_path_results = "LOW_E/"
                subfolder_path = "LOW_E/dataset" + str(n_folder_app) + "/"
                source_file = dataset_dir + "/LOW_E/dataset" + str(n_folder_app) + "/Output_acc_" + str(
                    n_dataset) + ".txt"


            output_estimations = os.path.join(output_estimations_main_dir, subfolder_path)
            output_error_rate = os.path.join(output_error_rate_dir, subfolder_path_results)
            if not os.path.exists(output_error_rate): os.makedirs(output_error_rate)

            output_file_path = output_error_rate + "/trust_error_rate_dataset_" + str(n_folder_app) +".csv"

            header = False  # dictionary with the original trustworthiness
            T_actual = utils_dataset.load_sources_info(source_file, header)

            trust_file_trad = os.path.join(output_estimations, "trad_est_trust_" + str(n_dataset) + ".csv")
            trust_trad = utils_dataset.read_trust_estimation_file(trust_file_trad)
            error_rate_trad = compute_error_rate_for_trustworthiness(T_actual, trust_trad)

            # adapted model 1 (only confidence) results files and dir
            trust_file_adapt = os.path.join(output_estimations, "adapt_est_trust_" + str(n_dataset) + ".csv")
            trust_adapt= utils_dataset.read_trust_estimation_file(trust_file_adapt)
            error_rate_adapt = compute_error_rate_for_trustworthiness(T_actual, trust_adapt)

            utils_writing_results.writing_trustworthiness_error_rate_file(output_file_path, error_rate_trad, error_rate_adapt)

    return True


def compute_average_trust_error_rate(dir_path, dataset_kind):
    f_in_path = os.path.join(dir_path, dataset_kind)
    trust_trad_average_for_dataset = list()
    trust_adapt_average_for_dataset = list()
    for root, dirs, files in os.walk(f_in_path):
        for file in files:
            if file.startswith("trust_error_rate_dataset_"):
                f_in = open(os.path.join(root, file), "r")
                average_trad = 0
                average_adapt = 0
                source_count = 0
                for line in f_in:
                    line = line.strip().split('\t')
                    average_trad += float(line[1])
                    average_adapt += float(line[2])
                    source_count += 1
                trust_trad_average_for_dataset.append(average_trad / float(source_count))
                trust_adapt_average_for_dataset.append(average_adapt / float(source_count))
                f_in.close()
    f_out_path = os.path.join(dir_path, str(dataset_kind) + "/average_trust_error_rate_" + str(dataset_kind) + ".csv")
    res_writing = utils_writing_results.writing_error_rate_summary_file(f_out_path, trust_trad_average_for_dataset, trust_adapt_average_for_dataset )
    #[True, summary_str]
    return res_writing[1]

if __name__ == '__main__':
    predicate = "birthPlace"
    dataset_dir = "D:/datasets/dataset_" + str(predicate) + "/"
    output_estimations_main_dir = "../estimations/results_sums_" + str(predicate) + "/"
    output_error_rate_dir = "../results/" + str(predicate) + "/error_rate/"

    #analysis_trustworthiness_estimations(dataset_dir, output_estimations_main_dir, output_error_rate_dir)

    dataset_kind_list = ["EXP", "LOW_E", "UNI"]
    for dataset_kind in dataset_kind_list:
        str_out_average = compute_average_trust_error_rate(output_error_rate_dir, dataset_kind)
        if str_out_average != "":
            print(str(dataset_kind) + " dataset : " + str(str_out_average))
