def compute_precision_with_general(sol_dict_, truth_, ancestors_):
    #function that compute the number of expected/general/erroneous values returned by the approach
    #note that the general values are all the returned values that are more general than the expected one (therefore they are still true)
    #note that the erronous values are values that are neither general or expected
    n_exp_ = 0
    n_gen_ = 0
    n_err_ = 0
    for d in sol_dict_:
        returned_value = sol_dict_[d]
        expected = truth_[d]
        if returned_value == expected:
            n_exp_ += 1
        else:
            if returned_value in ancestors_[expected]:
                n_gen_ += 1
            else:
                n_err_ += 1

    return n_exp_, n_gen_, n_err_