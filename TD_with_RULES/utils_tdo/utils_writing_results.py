import sys
import os


def writing_confidence_results_adapted(adapted_1_output_conf_file_, C_adapt_1, T_average, T_average_norm):
    try:
        f_confidence = open(adapted_1_output_conf_file_, "w")
        for fact_id in C_adapt_1:
            f_confidence.write(
                str(fact_id) + '\t' + str(C_adapt_1[fact_id]) + '\t' + str(T_average[fact_id]) + '\t' + str(
                    T_average_norm[fact_id]) + '\n')
        f_confidence.close()
        return True
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
        return False


def writing_confidence_results_trad(trad_output_conf_file_, C_trad):
    try:
        f_confidence = open(trad_output_conf_file_, "w")
        for fact_id in C_trad:
            f_confidence.write(str(fact_id) + '\t' + str(C_trad[fact_id]) + '\n')
        f_confidence.close()
        return True
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
        return False


def writing_trust_results(output_file, T):
    print("flushing the trust result into file.....")
    try:
        file = open(output_file, "w")
        for source_id in T:
            file.write(str(source_id) + "\t" + str(T[source_id]) + "\n")

        file.close()
        return True
    except:
        print("Errors in saving error rate trust estimations")
        return False


def writing_confidence_results(output_file, sources_dataItemValues, dataitem_ids, C):
    '''this saving required a lot of disk space.
    To do only if it is necessary
    '''
    print("flushing the confidence result into file.....")
    try:
        for d in sources_dataItemValues:
            file = open(output_file + "/" + str(dataitem_ids.get(d)) + ".csv", "w")
            app = dict()
            for v in sources_dataItemValues.get(d).keys():
                app[v] = C.get(d + v)
            app_ord = sorted(app, key=app.__getitem__, reverse=True)
            for item in app_ord:
                file.write(str(item) + "\t" + str(C[d + item]) + "\n")
            file.close()
        return True
    except:
        print("Errors in saving confidence estimations")
        return False


def writing_comparsion_file(adapted_out_comparison_trust_file, T, T_trad, T_adapt):
    print("flushing the trust result comparison into file.....")
    try:
        file = open(adapted_out_comparison_trust_file, "w")
        average_err_trad = 0
        average_err_adapt = 0
        for source_id in T:
            v_act = T[source_id]
            v_trad = T_trad[source_id]
            v_adapt = T_adapt[source_id]
            trad_vs_act = abs(v_act - v_trad)
            adapt_vs_act = abs(v_act - v_adapt)
            error_advantages = adapt_vs_act - trad_vs_act  # if it is negative our model is better, the error is evaluated

            file.write(str(source_id) + "\t" + str(v_trad) + "\t" + str(v_adapt) + "\t" + str(v_act) + "\t" + str(
                trad_vs_act) + "\t" + str(adapt_vs_act) + "\t" + str(error_advantages) + "\n")

            average_err_trad = average_err_trad + trad_vs_act
            average_err_adapt = average_err_adapt + adapt_vs_act

        file.write("\n")
        average_err_trad = average_err_trad / len(T)
        average_err_adapt = average_err_adapt / len(T)
        file.write("AVERAGE" + "\t" + str(average_err_trad) + "\t" + str(average_err_adapt) + "\t" + str(
            average_err_adapt - average_err_trad) + "\n")

        file.close()
        return True
    except:
        print("Errors in saving trust estimation comparison file")
        return False


def writing_trustworthiness_error_rate_file(output_file_path, error_rate_trad, error_rate_adapt):
    try:
        f_out = open(output_file_path, "w")

        for source_id in error_rate_trad:
            str_out = str(source_id) + '\t' + str(error_rate_trad[source_id]) + '\t' + str(error_rate_adapt[source_id]) + '\n'
            f_out.write(str_out)

        f_out.close()
        return True
    except:
        print("error in writing comparison file")
        print("Unexpected error:", sys.exc_info()[0])
        return False


def writing_error_rate_summary_file(f_out_path, trust_trad_average_for_dataset, trust_adapt_average_for_dataset):
    try:
        f_out = open(f_out_path, "w")
        average_trad = 0
        average_adapt = 0
        for index_pos in range(0, len(trust_trad_average_for_dataset)):
            str_out = str(index_pos) + '\t' + str(trust_trad_average_for_dataset[index_pos]) + '\t' + str(trust_adapt_average_for_dataset[index_pos]) + '\n'
            average_trad += float(trust_trad_average_for_dataset[index_pos])
            average_adapt += float(trust_adapt_average_for_dataset[index_pos])
            f_out.write(str_out)

        f_out.write('\n')
        summary_str = "AVERAGE\t" + str(float(average_trad) / float(len(trust_trad_average_for_dataset))) + '\t' + str(float(average_adapt) / float(len(trust_adapt_average_for_dataset)))
        f_out.write(summary_str)
        f_out.close()
        return [True, summary_str]
    except:
        if not os.path.isfile(f_out_path):
            return [False, ""]
        print("error in writing summary trust error file")
        print("Unexpected error:", sys.exc_info()[0])
        return [False, ""]


def writing_sol_dictionary(file_path_, solution_dict_):
    f_out = open(file_path_, "w")
    for d in solution_dict_:
        str_out = str(d) + "\t" + str(solution_dict_[d]) + "\n"
        f_out.write(str_out)
    f_out.close()

def save_results_book_dataset(returned_sol_, output_path):
	f_out = open(output_path, "w")
	for d in returned_sol_:
		str_out = str(d) + "\t" + str(returned_sol_[d]) + "\n"
		f_out.write(str_out)
	f_out.close()

def writing_results_on_precision_with_rules(file_name, id_dataset_, n_exp, n_gen, n_err):
    f_out_prec_trad = open(file_name, "a")
    f_out_prec_trad.write(
        str(id_dataset_) + "\t" + str(n_exp) + "\t" + str(n_gen) + "\t" + str(n_err) + "\n")
    f_out_prec_trad.flush()
    f_out_prec_trad.close()