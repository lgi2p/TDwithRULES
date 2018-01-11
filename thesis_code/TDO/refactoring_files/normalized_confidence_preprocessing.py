import sys
import os
cwd = os.getcwd()
index_tdo = cwd.index("TDO")
cwd = cwd[:index_tdo]
sys.path.append(cwd)
from TDO.utils_tdo import utils_normalize_conf
from TDO.utils_tdo import utils_writing_results
from TDO.utils_tdo import utils_dataset
from TDO.utils_tdo import utils_predicate
import timeit


if __name__ == '__main__':
    predicate = sys.argv[1]
    estimations_dir = "../estimations/results_sums_" + str(predicate) + "/"
    estimations_dir_new = "../estimations_normalized/results_sums_" + str(predicate) + "/"
    if not os.path.exists(estimations_dir_new): os.makedirs(estimations_dir_new)

    base_dir = "../required_files/"
    base_dir = base_dir + predicate + "/"
    if predicate == 'genre':
        path_ground_file = base_dir + 'sample_genre_base_3.csv'

    else:  # the predicate is 'birthPlace'
        if predicate == 'birthPlace':
            path_ground_file = base_dir + 'sample_ground_grouped.csv'
        else:  # the predicate is CC, ...
            path_ground_file = base_dir + 'sample_ground_' + predicate + '.csv'

    ground = utils_predicate.loading_ground_truth(path_ground_file)[0]
    base_dir = "../required_files/"
    predicate_info = utils_predicate.loading_predicate_info(base_dir, predicate)

    path_datasets = "../datasets/dataset_" + str(predicate)

    for root, dirs, files in os.walk(estimations_dir):
        if "EXP" in dirs or "LOW_E" in dirs or "UNI" in dirs: continue
        if ["EXP"] == dirs: continue
        if ["LOW_E"] == dirs: continue
        if ["UNI"] == dirs: continue
        if root.count('/') != 3: continue
        #if root.count('/') != 4 and root.count('\\') != 1: continue
        performances_tot_adapt_norm = list()
        performances_tot_adapt_not = list()
        performances_tot_trad = list()

        for dir_name in dirs:
            print("dir name :" + str(dir_name))
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

            if "EXP" in root:
                dataset_kind_ = "EXP"
                subfolder_path = "EXP/dataset" + str(n_folder_app) + "/"
                facts_file = path_datasets + "/EXP/dataset" + str(n_folder_app) + "/facts_" + str(
                    n_dataset) + ".csv"

            if "LOW_E" in root:
                dataset_kind_ = "LOW_E"
                subfolder_path = "LOW_E/dataset" + str(n_folder_app) + "/"
                facts_file = path_datasets + "/LOW_E/dataset" + str(n_folder_app) + "/facts_" + str(
                    n_dataset) + ".csv"

            output_estimations = os.path.join(estimations_dir, subfolder_path)
            trust_file_adapt = os.path.join(output_estimations, "adapt_est_trust_" + str(n_dataset) + ".csv")
            conf_file_adapt = os.path.join(output_estimations, "adapt_est_conf_" + str(n_dataset) + ".csv")
            output_estimations_new = os.path.join(estimations_dir_new, subfolder_path)
            if not os.path.exists(output_estimations_new): os.makedirs(output_estimations_new)
            conf_file_adapt_NEW = os.path.join(output_estimations_new, "adapt_est_conf_" + str(n_dataset) + ".csv")

            start = timeit.default_timer()

            res_a = utils_dataset.read_estimation_file(trust_file_adapt, conf_file_adapt, False)
            print("files loaded")
            if res_a:
                conf_adapt = res_a[1]
                trust_average = res_a[2]  # T_average is a dict with key = claim_id and
                T_average_normalized = res_a[3]


                if len(T_average_normalized) == 0:
                    sources_dataItemValues = utils_dataset.load_facts(facts_file, True)
                    descendants = predicate_info[1]
                    ancestors = predicate_info[2]
                    T_average_normalized = utils_dataset.normalize_trust_average(trust_average, ancestors,
                                                                                 descendants,
                                                                                 sources_dataItemValues)
                conf_adapt_norm = utils_normalize_conf.creating_normalized_for_d_estimation(ground, conf_adapt)

                utils_writing_results.writing_confidence_results_adapted(conf_file_adapt_NEW, conf_adapt_norm, trust_average, T_average_normalized)

            # Your statements here
            stop = timeit.default_timer()
            print("running time ")
            print((stop - start)/60)
            print("End this dataset")

    print("Complete procedure")