import copy
import math


def get_complete_performance_measures_at_k_1(solution_dict, ground, sources_dataitem_values_local):
    #check only the solution in the firstposition
    true_positive = 0
    false_positive = 0
    true_negative =0
    false_negative = 0

    for d in sources_dataitem_values_local:
        if d not in ground:
            continue
        ground_sol = ground[d]
        returned_sol = solution_dict[d][0]
        for v in sources_dataitem_values_local[d]:
            if ground_sol == v:
                if returned_sol == v:
                    true_positive += 1
                else:
                    false_negative += 1
            else:
                if returned_sol == v:
                    false_positive += 1
                else:
                    true_negative += 1

    precision = float(true_positive) / float(true_positive + false_positive)
    accuracy = float(true_positive + true_negative) / float(true_positive + true_negative + false_positive + false_negative)
    recall = float(true_positive) / float(true_positive + false_negative)
    specificity = float(true_negative) / float(false_positive + true_negative)
    if math.isnan(precision):
        precision = 0

    if math.isnan(accuracy):
        accuracy = 0;

    if math.isnan(recall):
        recall = 0;

    if math.isnan(specificity):
        specificity = 0;

     # 20 is the iteration number , 0 in the last two position time and memory
    return [precision, accuracy, recall, specificity, 20, true_positive, true_negative, false_positive, false_negative, 0, 0]


def get_performance_measures(solution_dict, ground, k):
    #return the performance measure at different level of k
    performances_at_k = [[] for i in range(k)]
    for ls in performances_at_k:
        ls.append(0)  # correct rate

    for item in solution_dict:
        ground_sol = ground[item]
        # performances_at_k = [prec, rec, f1, acc]
        rank_list = solution_dict[item]
        k_max = min(len(rank_list), k)
        for ind_k in range(0, k_max):
            if rank_list[ind_k] == ground_sol:
                performances_at_k[ind_k][0] += 1
                # print(performances_at_k)
                break

    performances_at_k_rel = copy.deepcopy(performances_at_k)

    for ind_k in range(k - 1, -1, -1):
        sum_score = 0
        for ind_prev in range(0, ind_k):
            sum_score += performances_at_k[ind_prev][0]
        performances_at_k[ind_k][0] += sum_score

    return [performances_at_k_rel, performances_at_k]


def get_performance_measures_single_dataitem(rank_list, ground_sol, k, performances_tot, threshold_index, ancestors):
    # return the performance measure at different level of k for a single data item
    general_value = False
    punctual_value = False
    k_max = min(len(rank_list), k)

    for ind_k in range(0, k_max):
        if rank_list[ind_k] == ground_sol:
            for ind_app in range(ind_k, k):
                performances_tot[threshold_index][ind_app][0] += 1

            if general_value:
                for ind_app in range(ind_k, k):
                    performances_tot[threshold_index][ind_app][1] -= 1
            punctual_value = True
            break
        else:
            if rank_list[ind_k] in ancestors[ground_sol] and not general_value and not punctual_value:
                for ind_app in range(ind_k, k):
                    performances_tot[threshold_index][ind_app][1] += 1
                general_value = True
        if not punctual_value and not general_value:
            performances_tot[threshold_index][ind_k][2] += 1

    if not punctual_value and not general_value:
        if k > k_max:
            for ind_k in range(k_max, k):
                performances_tot[threshold_index][ind_k][2] += 1

    return performances_tot #absolute, not relative


def get_performance_measures_single_dataitem_error(performances_tot, k, threshold_index):
    #add 1 to the number of error in the lsit of the performances in case there is an error
    for ind_k in range(0, k):
        performances_tot[threshold_index][ind_k][2] += 1
    return performances_tot