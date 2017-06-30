from TD_with_RULES.utils_tdo import utils_writing_results


def run_sums_saving_iter(T, F_s, S, initial_confidence, max_iteration_number, output_file):
	# traditional sums model
	T_iter = dict()

	print("START : traditional sums " + " _ Convergence criteria : max iteration number (" + str(
		max_iteration_number) + ")")
	convergence = False
	iteration_number = 0

	# confidences for all the facts
	# <key = dataitem + value, value = confidence>
	C = dict()
	for fact_id in S:
		C[fact_id] = initial_confidence

	# iteration for estimating C and T
	while (not convergence):

		for source_id in T:
			sum = 0
			facts = F_s.get(source_id)  # get facts provided by this source
			for f in facts:
				if not f in C:
					print("Error cannot find confidence for ", f)
					exit()
				sum = sum + (C.get(f))
			T[source_id] = sum

		# normalizing using the maximum value in the list of T
		max_value = max(T.values())
		for source_id in T:
			T[source_id] = T[source_id] / max_value

		C.clear()  # in this way - without creating a new obj - is more fast

		for fact_id in S:  # S represents all the sources that claim a specific fact <key = dataitem + value, value = set of source ids>
			sum = 0
			for s in S.get(fact_id):  # source provining the fact <d+v>
				if not s in T:
					print("Error cannot find trustwordiness for ", s)
					print(S.get(fact_id))
					exit()
				sum = sum + T[s]
			C[fact_id] = sum

		# normalization
		max_value = max(C.values())
		for fact_id in C:
			C[fact_id] = C.get(fact_id) / max_value

		# save result iteration
		for source_id in T:
			if source_id not in T_iter:
				str_app = str(T[source_id])
			else:
				str_app = str(T_iter[source_id]) + "\t" + str(T[source_id])
			T_iter[source_id] = str_app

		# check conditions ---> 20th iteration has been reached
		if (iteration_number >= max_iteration_number - 1):
			convergence = True

		iteration_number += 1
		print('Iteration ' + str(iteration_number) + ' ----- ')

	utils_writing_results.writing_trust_results(output_file, T_iter)  # puntual results

	return [T, C]


# END SUMS MODEL


def run_sums_and_boost_saving_iter(T, F_s, S, initial_confidence, max_iteration_number, output_file_iter, sources_dataItemValues, boost_dict, gamma):
	# function that implements the adapted model
	#gamma = 0.7
	T_iter = dict()
	T_iter_delta = dict()
	print("START : sums_ADAPTED " + " _ Convergence criteria : max iteration number (" + str(max_iteration_number) + ")")

	convergence = False
	iteration_number = 0
	# confidences for all the facts
	# <key = dataitem + value, value = confidence>
	C = dict()
	for fact_id in S:
		C[fact_id] = initial_confidence

	# iteration for estimating C and T
	while (not convergence):

		for source_id in T:
			sum = 0
			facts = F_s.get(source_id)  # get facts provided by this source
			for f in facts:
				if not f in C:
					print("Error cannot find confidence for ", f)
					exit()
				sum = sum + (C.get(f))
			T[source_id] = sum

		# normalizing using the maximum value in the list of T
		max_value = max(T.values())
		for source_id in T:
			T[source_id] = T[source_id] / max_value

		C = dict()
		for fact_id in S:
			source_plus_set = S.get(fact_id)#.split(";")  # .split(";")
			sum = 0
			for s in source_plus_set:
				try:
					s = int(s)
					sum = sum + T[s]
				except ValueError:
					sum = sum + T[int(s.replace("source", ""))]

			C[fact_id] = sum
		# normalization
		max_value = max(C.values())
		for item in C:
			C[item] = C.get(item) / max_value

		##add rule influence
		for d in sources_dataItemValues:
			for value in sources_dataItemValues[d]:
				#fact = [d, "<http://dbpedia.org/ontology/birthPlace>", value]
				#gamma = boost_dict[d+ "<http://dbpedia.org/ontology/birthPlace>" + value]
				C[d + value] = (1 - gamma) * (C[d + value]) + gamma * boost_dict[
					d + "<http://dbpedia.org/ontology/birthPlace>" + value]
		# normalize
		max_value = max(C.values())
		for item in C:
			C[item] = C.get(item) / max_value

		# save result iteration
		for source_id in T:
			if source_id not in T_iter:
				str_app = str(T[source_id])
			else:
				str_app = str(T_iter[source_id]) + "\t" + str(T[source_id])

			T_iter[source_id] = str_app

		# check conditions --> the number of iteration is 20
		if iteration_number >= (max_iteration_number - 1):
			convergence = True

		iteration_number += 1
		print(str(iteration_number))

	# convergence reached -- end process
	utils_writing_results.writing_trust_results(output_file_iter, T_iter)

	return [T, C]


def run_sums_and_boost_saving_iter_2(T, F_s, S, initial_confidence, max_iteration_number, output_file_iter, sources_dataItemValues, boost_dict):
	# function that implements the adapted model
	gamma = 0.9
	T_iter = dict()
	T_iter_delta = dict()
	print("START : sums_ADAPTED " + " _ Convergence criteria : max iteration number (" + str(max_iteration_number) + ")")

	convergence = False
	iteration_number = 0
	# confidences for all the facts
	# <key = dataitem + value, value = confidence>
	C = dict()
	for fact_id in S:
		C[fact_id] = initial_confidence

	# iteration for estimating C and T
	while (not convergence):

		for source_id in T:
			sum = 0
			facts = F_s.get(source_id)  # get facts provided by this source
			for f in facts:
				if not f in C:
					print("Error cannot find confidence for ", f)
					exit()
				sum = sum + (C.get(f))
			T[source_id] = sum

		# normalizing using the maximum value in the list of T
		max_value = max(T.values())
		for source_id in T:
			T[source_id] = T[source_id] / max_value

		C = dict()
		for fact_id in S:
			source_plus_set = S.get(fact_id).split(";")  # .split(";")
			sum = 0
			for s in source_plus_set:
				try:
					s = int(s)
					sum = sum + T[s]
				except ValueError:
					sum = sum + T[int(s.replace("source", ""))]

			C[fact_id] = sum
		# normalization
		max_value = max(C.values())
		for item in C:
			C[item] = C.get(item) / max_value

		##add rule influence
		for d in sources_dataItemValues:
			for value in sources_dataItemValues[d]:
				#fact = [d, "<http://dbpedia.org/ontology/birthPlace>", value]
				# gamma = boost_dict[d+ "<http://dbpedia.org/ontology/birthPlace>" + value]
				C[d + value] = (1 - gamma) * (C[d + value]) + gamma * boost_dict[
					d + "<http://dbpedia.org/ontology/birthPlace>" + value]
		# normalize
		max_value = max(C.values())
		for item in C:
			C[item] = C.get(item) / max_value

		# save result iteration
		for source_id in T:
			if source_id not in T_iter:
				str_app = str(T[source_id])
			else:
				str_app = str(T_iter[source_id]) + "\t" + str(T[source_id])

			T_iter[source_id] = str_app

		# check conditions --> the number of iteration is 20
		if iteration_number >= (max_iteration_number - 1):
			convergence = True

		iteration_number += 1
		print(str(iteration_number))

	# convergence reached -- end process
	utils_writing_results.writing_trust_results(output_file_iter, T_iter)

	return [T, C]


# END FUNCTION ADAPTED MODEL  with rules


def run_adapted_sums_saving_iter(T_, F_s_, S_prop_, initial_confidence_, max_iteration_number_, sources_dataItemValues_,
								 output_file_):
	# function that implements the adapted model
	T_iter = dict()
	print(
		"START : sums_ADAPTED " + " _ Convergence criteria : max iteration number (" + str(max_iteration_number_) + ")")

	convergence = False
	iteration_number = 0
	# confidences for all the facts
	# <key = dataitem + value, value = confidence>
	C = dict()
	for fact_id in S_prop_:
		C[fact_id] = initial_confidence_

	# iteration for estimating C and T
	while (not convergence):
		# t_start_iter = time.time()

		for source_id in T_:
			sum = 0
			facts = F_s_.get(source_id)  # get facts provided by this source
			for f in facts:
				if not f in C:
					print("Error cannot find confidence for ", f)
					exit()
				sum = sum + (C.get(f))
			T_[source_id] = sum

		# normalizing using the maximum value in the list of T
		max_value = max(T_.values())
		for source_id in T_:
			T_[source_id] = T_[source_id] / max_value

		C = dict()

		for fact_id in S_prop_:
			source_plus_set = S_prop_.get(fact_id).split(";")
			sum = 0
			for s in source_plus_set:
				try:
					s = int(s)
					sum = sum + T_[s]
				except ValueError:
					sum = sum + T_[int(s.replace("source", ""))]

			C[fact_id] = sum
		# normalization
		max_value = max(C.values())
		for item in C:
			C[item] = C.get(item) / max_value

		# save result iteration
		for source_id in T_:
			if source_id not in T_iter:
				str_app = str(T_[source_id])
			else:
				str_app = str(T_iter[source_id]) + "\t" + str(T_[source_id])
			T_iter[source_id] = str_app

		# check conditions --> the number of iteration is 20
		if (iteration_number >= max_iteration_number_ - 1):
			convergence = True

		iteration_number += 1
		print('Iteration ' + str(iteration_number) + ' ----- ')

	# convergence reached -- end process
	utils_writing_results.writing_trust_results(output_file_, T_iter)

	return [T_, C]


# END FUNCTION ADAPTED MODEL


def run_adapted_sums_and_boost_saving_iter(T_, F_s_, S_prop_, initial_confidence_, max_iteration_number_,
										   sources_dataItemValues_, output_file_, boost_dict, gamma):
	# function that implements the adapted model using the rules
	#gamma = 0.9
	T_iter = dict()
	print("START : sums_ADAPTED with rules " + " _ Convergence criteria : max iteration number (" + str(
		max_iteration_number_) + ")")

	convergence = False
	iteration_number = 0
	# confidences for all the facts
	# <key = dataitem + value, value = confidence>
	C = dict()
	for fact_id in S_prop_:
		C[fact_id] = initial_confidence_

	# iteration for estimating C and T
	while (not convergence):
		# t_start_iter = time.time()

		for source_id in T_:
			sum = 0
			facts = F_s_.get(source_id)  # get facts provided by this source
			for f in facts:
				if not f in C:
					print("Error cannot find confidence for ", f)
					exit()
				sum = sum + (C.get(f))
			T_[source_id] = sum

		# normalizing using the maximum value in the list of T
		max_value = max(T_.values())
		for source_id in T_:
			T_[source_id] = T_[source_id] / max_value

		C = dict()
		for fact_id in S_prop_:
			source_plus_set = S_prop_.get(fact_id).split(";")
			sum = 0
			for s in source_plus_set:
				try:
					s = int(s)
					sum = sum + T_[s]
				except ValueError:
					sum = sum + T_[int(s.replace("source", ""))]

			C[fact_id] = sum
		# normalization
		max_value = max(C.values())
		for item in C:
			C[item] = C.get(item) / max_value
		###add rule influence
		#####add rule influence
		for fact_id in S_prop_:
			fact_id_list = fact_id.split("http")
			d = "http"+fact_id_list[1]
			#print(d)
			value = "http"+fact_id_list[2]
			#print(value)
				# fact = [d, "<http://dbpedia.org/ontology/birthPlace>", value]
				# gamma = boost_dict[d+ "<http://dbpedia.org/ontology/birthPlace>" + value]
			boost_factor = boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + value]
			C[fact_id] = (1 - gamma) * (C[fact_id]) + gamma * boost_factor

		max_value = max(C.values())
		for item in C:
			C[item] = C.get(item) / max_value

		# save result iteration
		for source_id in T_:
			if source_id not in T_iter:
				str_app = str(T_[source_id])
			else:
				str_app = str(T_iter[source_id]) + "\t" + str(T_[source_id])
			T_iter[source_id] = str_app

		# check conditions --> the number of iteration is 20
		if (iteration_number >= max_iteration_number_ - 1):
			convergence = True

		iteration_number += 1
		print('Iteration ' + str(iteration_number) + ' ----- ')

	# convergence reached -- end process
	utils_writing_results.writing_trust_results(output_file_, T_iter)

	return [T_, C]


# END FUNCTION ADAPTED MODEL with rules

def run_adapted_sums_and_boost_adapted_saving_iter(T_, F_s_, S_prop_, initial_confidence_, max_iteration_number_,
										   sources_dataItemValues_, output_file_, boost_dict_prop):
	# function that implements the adapted model using the rules
	gamma = 0.6
	T_iter = dict()
	print("START : sums_ADAPTED with rules " + " _ Convergence criteria : max iteration number (" + str(
		max_iteration_number_) + ")")

	convergence = False
	iteration_number = 0
	# confidences for all the facts
	# <key = dataitem + value, value = confidence>
	C = dict()
	for fact_id in S_prop_:
		C[fact_id] = initial_confidence_

	# iteration for estimating C and T
	while (not convergence):
		# t_start_iter = time.time()

		for source_id in T_:
			sum = 0
			facts = F_s_.get(source_id)  # get facts provided by this source
			for f in facts:
				if not f in C:
					print("Error cannot find confidence for ", f)
					exit()
				sum = sum + (C.get(f))
			T_[source_id] = sum

		# normalizing using the maximum value in the list of T
		max_value = max(T_.values())
		for source_id in T_:
			T_[source_id] = T_[source_id] / max_value

		C = dict()

		for fact_id in S_prop_:
			source_plus_set = S_prop_.get(fact_id).split(";")
			sum = 0
			for s in source_plus_set:
				try:
					s = int(s)
					sum = sum + T_[s]
				except ValueError:
					sum = sum + T_[int(s.replace("source", ""))]

			C[fact_id] = sum
		# normalization
		max_value = max(C.values())
		for item in C:
			C[item] = C.get(item) / max_value

		###add rule influence
		for d in sources_dataItemValues_:
			for value in sources_dataItemValues_[d]:
				#fact = [d, "<http://dbpedia.org/ontology/birthPlace>", value]
				# gamma = boost_dict[d+ "<http://dbpedia.org/ontology/birthPlace>" + value]
				C[d + value] = (1 - gamma) * (C[d + value]) + gamma * boost_dict_prop[
					d + "<http://dbpedia.org/ontology/birthPlace>" + value]
		# normalize
		max_value = max(C.values())
		for item in C:
			C[item] = C.get(item) / max_value

		# save result iteration
		for source_id in T_:
			if source_id not in T_iter:
				str_app = str(T_[source_id])
			else:
				str_app = str(T_iter[source_id]) + "\t" + str(T_[source_id])
			T_iter[source_id] = str_app

		# check conditions --> the number of iteration is 20
		if (iteration_number >= max_iteration_number_ - 1):
			convergence = True

		iteration_number += 1
		print('Iteration ' + str(iteration_number) + ' ----- ')

	# convergence reached -- end process
	utils_writing_results.writing_trust_results(output_file_, T_iter)

	return [T_, C]

# END FUNCTION ADAPTED MODEL with rules
