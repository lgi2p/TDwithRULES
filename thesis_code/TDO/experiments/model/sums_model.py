import os
import sys
from copy import deepcopy
import math

cwd = os.getcwd()
if ("TDO") in cwd:
	from TDO.utils_tdo import utils_writing_results
else:
	sys.path.append('D:/Dropbox/thesis_code/TDO')
	from utils_tdo import utils_writing_results
import time
import pandas as pd
from scipy.spatial.distance import cosine
import rpy2.robjects as ro
import pandas as pd
from rpy2.robjects import pandas2ri
from TDO.utils_tdo import empirical_Bayes
import math
import copy

def cosine_dic(dic1,dic2):
	numerator = 0
	dena = 0
	for key1 in dic1:
		val1 = dic1[key1]
		numerator += val1*dic2.get(key1,0.0)
		dena += val1*val1
	denb = 0
	for val2 in dic2.values():
		denb += val2*val2
	return numerator/math.sqrt(dena*denb)

def cosine_similarity(vec1,vec2):
	sum11, sum12, sum22 = 0, 0, 0
	for i in range(len(vec1)):
		x = vec1[i]
		y = vec2[i]
		sum11 += x*x
		sum22 += y*y
		sum12 += x*y
	sum11 = sum11**0.5
	sum22 = sum22**0.5
	if (sum11 * sum22) == 0:
		return sys.float_info.max
	if math.isinf(sum12):
		if math.isinf(sum11 * sum22):
			return 1.0
	cosineSimilarity = sum12 / (sum11 * sum22);


	return cosineSimilarity;

def define_r_function():
	pandas2ri.activate()
	print("define function in R")
	r_src = """ function(dataf, col_name_to_select){
					library(dplyr)
					library(tidyr)
					library(ggplot2)
					
					p <- ggplot(dataf, aes(vote_for_list / tot_list))
					p <- p + geom_histogram()
					ggsave(filename="a.jpg", plot=p)
					p <- ggplot(dataf, aes(vote_for_list))
					p <- p + geom_histogram()
					ggsave(filename="b.jpg", plot=p)
					p <- ggplot(dataf, aes(tot_list))
					p <- p + geom_histogram()
					ggsave(filename="c.jpg", plot=p)
					
					library(ebbr)

					prior <- dataf %>% ebb_fit_prior(vote_for_list, tot_list, method="mm")

						augmented_prior <- (augment(prior, data = dataf))

						result_augmented <- select(augmented_prior, col_name_to_select, .fitted)
						}
				"""
	r_funct = ro.r(r_src)
	return  r_funct


def normalization_with_bayes(item_list_, vote_for_list, tot_list, r_funct):
	# create the complete dataframe - each of them is a column
	# start_time = time.time()
	df = pd.DataFrame({
		'item_list_': item_list_,
		'vote_for_list': vote_for_list,
		'tot_list': tot_list
	})
	# convert the format of dataframe from py to R
	# start_time = time.time()
	dataf = pandas2ri.py2ri(df)
	print("--- %s seconds to convert data frame in R format ---" % (time.time()))
	# launch R function for estimating the new posteriori
	augment_prior = r_funct(dataf, 'item_list_')
	# convert the format of dataframe from R to py
	augment_prior = pandas2ri.ri2py(augment_prior)
	# re-assigne the new confidence level to each C[d+v]
	app_dict_ = augment_prior.set_index('item_list_').to_dict()
	app_dict_ = app_dict_['.fitted']
	return app_dict_

def run_sums_new_normalization_2(T, F_s, S, initial_confidence, max_iteration_number, output_file, sources_dataItemValues_,data_item_sources):
	# traditional sums model


	r_funct_ = define_r_function()
	T_iter = dict()
	sources_list = list()
	for source_id in T:
		sources_list.append(source_id)
	claims_list = list()
	claims_list_no_tab = list()
	for d in sources_dataItemValues_:
		for v in sources_dataItemValues_[d]:
			claims_list.append(d + '\t' + v)
			claims_list_no_tab.append(d+v)
	print("START : traditional sums " + " _ Convergence criteria : max iteration number (" + str(
		max_iteration_number) + ")")
	convergence = False
	iteration_number = 0

	# confidences for all the facts
	# <key = dataitem + value, value = confidence>
	C = dict()
	for fact_id in S:
		C[fact_id] = initial_confidence
	for source_id in T:
		T[source_id] = 0.7
	source_for_list = list()
	source_tot_list = list()
	claims_for_list = list()
	claims_tot_list = list()

	# iteration for estimating C and T
	while (not convergence):

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
		claims_for_list.clear()
		for claims_id in claims_list:
			claims_for_list.append(C[claims_id.replace("\t", "")])

		claims_tot_list.clear()
		for claims_id in claims_list:
			data_item = claims_id.split("\t")[0]
			v = claims_id.split("\t")[1]
			tot_est = len(sources_dataItemValues_[data_item][v])
			claims_tot_list.append(tot_est)
			#if tot_est == C[claims_id.replace("\t", "")]:
			#	print()
		# print("lengh vote for " + str(len()))
		print("here avant C")
		C = normalization_with_bayes(claims_list_no_tab, claims_for_list, claims_tot_list, r_funct_)
		print("here C")
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
		source_for_list.clear()
		source_tot_list.clear()
		for source_id in sources_list:
			source_for_list.append(T[source_id])
			#print("Trust of source " + str(source_id) + " " + str(T[source_id]))
			claims_set = F_s[source_id]
			#print(len(claims_set))
			source_tot_list.append(len(claims_set))
			#if T[source_id] == len(claims_set):
			#	print()

		T = normalization_with_bayes(sources_list, source_for_list, source_tot_list, r_funct_)
		print("here T")

		# save result iteration
		for source_id in T:
			if source_id not in T_iter:
				str_app = str(T[source_id])
			else:
				str_app = str(T_iter[source_id]) + "\t" + str(T[source_id])
			T_iter[source_id] = str_app

		## check conditions --> the number of iteration is 20
		if (iteration_number >= max_iteration_number - 1):
			convergence = True

		iteration_number += 1
		print('Iteration ' + str(iteration_number) + ' ----- ')

		if iteration_number < 6:
			T_old_s = pd.Series(T)
			C_old_s = pd.Series(C)
		else:
			#cosine for claim
			start_time = time.time()
			C_s = pd.Series(C)
			sim = 1 - cosine(C_old_s, C_s)
			print("cosine similarity CLAIMS " + str(sim))
			C_old_s = pd.Series(C)
			end_time = time.time()
			print("running time cosine for claims " + str(end_time - start_time))

			#cosine for source
			start_time = time.time()
			#T_old_s = pd.Series(T_)
			T_s = pd.Series(T)
			sim = 1 - cosine(T_old_s, T_s)
			print("cosine similarity SOURCES " + str(sim))
			if (1-sim) < 0.0001:
				convergence = True
			else:
				T_old_s = pd.Series(T)
			end_time = time.time()
			print("running time cosine for source " + str(end_time-start_time))


	# convergence reached -- end process
	utils_writing_results.writing_trust_results(output_file, T_iter)

	return [T, C]


# END SUMS MODEL


def run_sums_new_normalization(T, F_s, S, initial_confidence, max_iteration_number, output_file, sources_dataItemValues_,data_item_sources):
	# traditional sums model
	import pandas as pd
	from rpy2.robjects import pandas2ri
	pandas2ri.activate()

	print("define function in R")
	r_src = """ function(dataf, n_iteration, col_name_to_select){
				library(dplyr)
				library(tidyr)
				library(ggplot2)
				if(n_iteration==0 | n_iteration == 19){
					p <- ggplot(dataf, aes(est_positive / est_total))
					p <- p + geom_histogram()
					ggsave(filename="a.jpg", plot=p)
					p <- ggplot(dataf, aes(est_positive))
					p <- p + geom_histogram()
					ggsave(filename="b.jpg", plot=p)
					p <- ggplot(dataf, aes(est_total))
					p <- p + geom_histogram()
					ggsave(filename="c.jpg", plot=p)
				}
				library(ebbr)

				prior <- dataf %>% ebb_fit_prior(est_positive, est_total, method="mm")

					augmented_prior <- (augment(prior, data = dataf))

					result_augmented <- select(augmented_prior, col_name_to_select, .fitted)
					}
			"""
	import rpy2.robjects as ro
	r_funct = ro.r(r_src)

	T_iter = dict()
	sources_list = list()
	for source_id in T:
		sources_list.append(source_id)
	claims_list = list()
	claims_list_no_tab = list()
	for d in sources_dataItemValues_:
		for v in sources_dataItemValues_[d]:
			claims_list.append(d + '\t' + v)
			claims_list_no_tab.append(d+v)
	print("START : traditional sums " + " _ Convergence criteria : max iteration number (" + str(
		max_iteration_number) + ")")
	convergence = False
	iteration_number = 0

	# confidences for all the facts
	# <key = dataitem + value, value = confidence>
	C = dict()
	for fact_id in S:
		C[fact_id] = 0.51#initial_confidence
	for source_id in T:
		T[source_id] = 0.7
	source_for_list = list()
	source_tot_list = list()
	claims_for_list = list()
	claims_tot_list = list()

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
		source_for_list.clear()
		source_tot_list.clear()
		for source_id in sources_list:
			source_for_list.append(T[source_id])
			#print("Trust of source " + str(source_id) + " " + str(T[source_id]))
			claims_set = F_s[source_id]
			#print(len(claims_set))
			source_tot_list.append(len(claims_set))
			#if T[source_id] == len(claims_set):
			#	print()
		print("here T")
		#for index_app in range(0, len(source_for_list)):
		#	print(str(source_for_list[index_app]) + "\t" + str(source_tot_list[index_app]))

		# create the complete dataframe - each of them is a column
		# start_time = time.time()
		df = pd.DataFrame({
			'sources_list': sources_list,
			'est_positive': source_for_list,
			'est_total': source_tot_list
		})
		# print("--- %s seconds to create data frame ---" % (time.time() - start_time))
		# print(df)
		# convert the format of dataframe from py to R
		# start_time = time.time()
		dataf = pandas2ri.py2ri(df)
		# print("--- %s seconds to convert data frame in R format ---" % (time.time() - start_time))
		# launch R function for estimating the new posteriori
		# start_time = time.time()
		augment_prior = r_funct(dataf, iteration_number,'sources_list')
		# print("--- %s seconds to execute R function ---" % (time.time() - start_time))
		# convert the format of dataframe from R to py
		# start_time = time.time()
		augment_prior = pandas2ri.ri2py(augment_prior)
		# print("--- %s seconds to reconvert data frame in PY format ---" % (time.time() - start_time))
		# re-assigne the new confidence level to each C[d+v]
		# start_time = time.time()
		T_ = augment_prior.set_index('sources_list').to_dict()
		T = T_['.fitted']
		print("here T")

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
		claims_tot_list.clear()
		claims_for_list.clear()
		for claims_id in claims_list:
			claims_for_list.append(C[claims_id.replace("\t", "")])
			data_item = claims_id.split("\t")[0]
			v = claims_id.split("\t")[1]
			tot_est = len(sources_dataItemValues_[data_item][v])
			claims_tot_list.append(tot_est)
			#if tot_est == C[claims_id.replace("\t", "")]:
			#	print()
		# print("lengh vote for " + str(len()))
		print("here avant C")
		# create the complete dataframe - each of them is a column
		# start_time = time.time()
		df = pd.DataFrame({
			'claims_list': claims_list_no_tab,
			'est_positive': claims_for_list,#'vote_for_list'
			'est_total': claims_tot_list #'tot_list'
		})
		# convert the format of dataframe from py to R
		# start_time = time.time()
		dataf = pandas2ri.py2ri(df)
		print("step 1 ---")
		# launch R function for estimating the new posteriori
		augment_prior = r_funct(dataf, iteration_number, 'claims_list')
		print("step 2 ---" )
		# convert the format of dataframe from R to py
		augment_prior = pandas2ri.ri2py(augment_prior)
		print("step 3 ---")
		# re-assigne the new confidence level to each C[d+v]
		app_dict_ = augment_prior.set_index('item_list_').to_dict()
		print("step 4 ---" )
		C = app_dict_['.fitted']
		print("here C")



		# save result iteration
		for source_id in T:
			if source_id not in T_iter:
				str_app = str(T[source_id])
			else:
				str_app = str(T_iter[source_id]) + "\t" + str(T[source_id])
			T_iter[source_id] = str_app

		## check conditions --> the number of iteration is 20
		if (iteration_number >= max_iteration_number - 1):
			convergence = True

		iteration_number += 1
		print('Iteration ' + str(iteration_number) + ' ----- ')

		if iteration_number < 6:
			T_old_s = pd.Series(T)
			C_old_s = pd.Series(C)
		else:
			#cosine for claim
			start_time = time.time()
			C_s = pd.Series(C)
			sim = 1 - cosine(C_old_s, C_s)
			print("cosine similarity CLAIMS " + str(sim))
			C_old_s = pd.Series(C)
			end_time = time.time()
			print("running time cosine for claims " + str(end_time - start_time))

			#cosine for source
			start_time = time.time()
			#T_old_s = pd.Series(T_)
			T_s = pd.Series(T)
			sim = 1 - cosine(T_old_s, T_s)
			print("cosine similarity SOURCES " + str(sim))
			if (1-sim) < 0.0001:
				convergence = True
			else:
				T_old_s = pd.Series(T)
			end_time = time.time()
			print("running time cosine for source " + str(end_time-start_time))


	# convergence reached -- end process
	utils_writing_results.writing_trust_results(output_file, T_iter)

	return [T, C]


def run_sums_new_normalization_3(T_, F_s_, S_prop_, initial_confidence_, max_iteration_number_,
									   sources_dataItemValues_, output_file_, app_conf_dict, data_item_sources, root_el):
	# preprocessing F_s_prop
	F_s_prop = dict()
	for item in S_prop_:
		if type(S_prop_[item]) is set:
			for s in S_prop_[item]:
				s = int(s)
				if s not in F_s_prop:
					F_s_prop[s] = set()
				F_s_prop[s].add(item)
		else:
			for s in S_prop_[item].split(';'):
				s = int(s)
				if s not in F_s_prop:
					F_s_prop[s] = set()
				F_s_prop[s].add(item)

	import rpy2.robjects as ro
	import pandas as pd
	from rpy2.robjects import pandas2ri
	pandas2ri.activate()

	print("define function in R")
	r_src = """ function(dataf, n_iteration, col_name_to_select){
			library(dplyr)
			library(tidyr)
			library(ggplot2)
			if(n_iteration==0 | n_iteration == 19){
				p <- ggplot(dataf, aes(est_positive / est_total))
				p <- p + geom_histogram()
				ggsave(filename="a.jpg", plot=p)
				p <- ggplot(dataf, aes(est_positive))
				p <- p + geom_histogram()
				ggsave(filename="b.jpg", plot=p)
				p <- ggplot(dataf, aes(est_total))
				p <- p + geom_histogram()
				ggsave(filename="c.jpg", plot=p)
			}
			library(ebbr)

			prior <- dataf %>% ebb_fit_prior(est_positive, est_total, method="mm")

				augmented_prior <- (augment(prior, data = dataf))

				result_augmented <- select(augmented_prior, col_name_to_select, .fitted)
				}
		"""
	import rpy2.robjects as ro
	r_funct = ro.r(r_src)
	# r_funct_2 = ro.r(r_src_2)
	# define list of d+v (in order to keep always the same order)
	dataitem_values_list = list()
	for d in app_conf_dict:
		for v in app_conf_dict[d]:
			dataitem_values_list.append(d + '\t' + v)
	###define list of sources (in order to keep always the same order)
	sources_list = list()
	for s in T_:
		sources_list.append(s)

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
		# trustworthiness computation
		for source_id in T_:
			sum = 0
			facts = F_s_.get(source_id)  # get facts provided by this source
			for f in facts:
				if not f in C:
					print("Error cannot find confidence for ", f)
					exit()
				sum = sum + (C.get(f))
			T_[source_id] = sum

		# print(T_[0])
		#### normalization
		# create list of est_positive for each
		print("source for vector")
		source_for_vect = list()
		for source_id in sources_list:
			estimation = T_[source_id]
			source_for_vect.append(estimation)
		# create list of number of sources vector for each claim
		if iteration_number >= 0:  # 0:
			print("number of claims provided by each source vector")
			all_claims_vote_vect = list()
			for source_id in sources_list:
				#OLDclaims_plus_set = F_s_prop[source_id]
				#OLD# claims_plus_set = F_s_[source_id]
				#OLDall_claims_vote_vect.append(len(claims_plus_set))
				#max_conf = 0
				#value_max_conf = ""
				tot = 0
				for d in data_item_sources[source_id]:
					max_conf = 0
					for v in sources_dataItemValues_[d]:
						if C[d+v]>max_conf:
							max_conf= C[d+v]
							#value_max_conf = v
					tot += max_conf
				all_claims_vote_vect.append(tot)

		# create the complete dataframe - each of them is a column
		# start_time = time.time()
		df = pd.DataFrame({
			'sources_list': sources_list,
			'est_positive': source_for_vect,
			'est_total': all_claims_vote_vect
		})
		# print("--- %s seconds to create data frame ---" % (time.time() - start_time))
		# print(df)
		# convert the format of dataframe from py to R
		# start_time = time.time()
		dataf = pandas2ri.py2ri(df)
		# print("--- %s seconds to convert data frame in R format ---" % (time.time() - start_time))
		# launch R function for estimating the new posteriori
		# start_time = time.time()
		augment_prior = r_funct(dataf, iteration_number, 'sources_list')
		# print("--- %s seconds to execute R function ---" % (time.time() - start_time))
		# convert the format of dataframe from R to py
		# start_time = time.time()
		augment_prior = pandas2ri.ri2py(augment_prior)
		# print("--- %s seconds to reconvert data frame in PY format ---" % (time.time() - start_time))
		# re-assigne the new confidence level to each C[d+v]
		# start_time = time.time()
		T_ = augment_prior.set_index('sources_list').to_dict()
		T_ = T_['.fitted']
		# print("--- %s seconds to reassigned the normalized trustowrhtiness ---" % (time.time() - start_time))

		##compute confidence of claims
		C = dict()

		for fact_id in S_prop_:
			if type(S_prop_[fact_id]) is set:
				source_plus_set = S_prop_.get(fact_id)
			else:
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
		# create list of est_positive
		print("vote for vector")
		vote_for_vect = list()
		for fact_id in dataitem_values_list:
			estimation = C[fact_id.replace('\t', '')]
			vote_for_vect.append(estimation)
		# create list of number of sources vector for each claim
		'''print("number of sources vector")
		all_vote_vect = list()
		for claim in dataitem_values_list:
			d = claim.split('\t')[0]
			v = claim.split('\t')[1]
			source_plus_set = S_prop_.get(d+v).split(";")
			all_vote_vect.append(len(source_plus_set))
			#if d == 'O15399_1':
			#	print(str(v) + '\t' + str(len(source_plus_set)))
		'''
		print("est tot for each d vector")
		all_vote_vect = list()
		d_prec = ""
		for claim in dataitem_values_list:
			d = claim.split('\t')[0]
			#v = claim.split('\t')[1]
			if d == d_prec:
				all_vote_vect.append(tot)  # = r_funct_all_vote(tot, all_vote_vect)
			else:
				source_plus_set_total = set()
				for v_app in sources_dataItemValues_[d]:
					if type(S_prop_[d + v_app]) is set:
						source_plus_set_total = source_plus_set_total.union(S_prop_.get(d + v_app))
					else:
						source_plus_set_total = source_plus_set_total.union(set(S_prop_.get(d + v_app).split(";")))
				'''
				for v in app_conf_dict[d]:
					source_plus_set = S_prop_.get(d+v).split(";")
					source_plus_set_total = source_plus_set_total.union(source_plus_set)
				'''
				tot = 0
				for s in source_plus_set_total:
					try:
						s = int(s)
						tot += T_[s]
					except ValueError:
						tot += T_[int(s.replace("source", ""))]
				all_vote_vect.append(tot)
				# all_vote_vect.append(len(source_plus_set_total))
				d_prec = d




		# create the complete dataframe - each of them is a column
		# start_time = time.time()
		df = pd.DataFrame({
			'claims_list': dataitem_values_list,
			'est_positive': vote_for_vect,
			'est_total': all_vote_vect
		})
		# print("--- %s seconds to create data frame ---" % (time.time() - start_time))
		# convert the format of dataframe from py to R
		# start_time = time.time()
		dataf = pandas2ri.py2ri(df)
		# print("--- %s seconds to convert data frame in R format  ---" % (time.time() - start_time))
		# launch R function for estimating the new posteriori
		# start_time = time.time()
		augment_prior = r_funct(dataf, iteration_number, 'claims_list')
		# print("--- %s seconds to execute R function ---" % (time.time() - start_time))

		# convert the format of dataframe from R to py
		# start_time = time.time()
		augment_prior = pandas2ri.ri2py(augment_prior)
		# print("--- %s seconds to reconvert data frame in PY format ---" % (time.time() - start_time))
		# re-assigne the new confidence level to each C[d+v]
		# start_time = time.time()
		augment_prior['claims_list'].replace('\t', '', regex=True, inplace=True)
		C = augment_prior.set_index('claims_list').to_dict()
		C = C['.fitted']
		# C = C['claims_list'].replace('\t', '', regex=True, inplace=True)

		# print("--- %s seconds to reassigned the normalized confidence ---" % (time.time() - start_time))

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

# END SUMS MODEL

def run_sums_new_normalization_JSE(T, F_s, S, initial_confidence, max_iteration_number, sources_dataItemValues, output_file, app, data_item_sources, root_el):
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
		source_list = list()
		conf_list = list()
		for claim in S:
			for source_id in S[claim]:
				source_list.append(source_id)
				conf_list.append(C[claim]*100)

		# normalizing using the maximum value in the list of T
		df = pd.DataFrame({
			'species': source_list,
			'conf_estimation': conf_list
		})
		df_ret = empirical_Bayes.multi_sample_size_js_estimator(df, group_id_col='species', data_col='conf_estimation', pooled=False)
		T = df_ret.to_dict()#stats
		#T = T['theta_hat_js']
		T.update((x, y / 100) for x, y in T.items())

		C.clear()  # in this way - without creating a new obj - is more fast

		source_list = list()
		trust_list = list()
		for claim in S:
			for source_id in S[claim]:
				source_list.append(claim)
				trust_list.append(T[source_id]*100)

		# normalizing using the maximum value in the list of T
		df = pd.DataFrame({
			'species': source_list,
			'trust_estimation': trust_list
		})
		df_ret = empirical_Bayes.multi_sample_size_js_estimator(df, group_id_col='species', data_col='trust_estimation', pooled=False)
		C = df_ret.to_dict()#['theta_hat_js']#stats['theta_hat_js']
		C.update((x, y /100) for x, y in C.items())

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


def run_sums_saving_iter(T, F_s, S, initial_confidence, max_iteration_number, output_file, sources_dataItemValues):
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
		##to remove
		'''for source_id in T:
			if len(F_s[source_id])/len(sources_dataItemValues) > 0.80:
				if T[source_id] - 0.3 < 0:
					T[source_id] = 0.3
				else:
					T[source_id] = T[source_id]-0.3
			if len(F_s[source_id]) / len(sources_dataItemValues) < 0.20:
				T[source_id] = T[source_id] + 0.3'''
		##end to rempve
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
	T_prec = dict()
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
					#s = int(s)
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

		#if iteration_number > 0:
			#utils_writing_results.writing_trust_results_for_convergence(output_file_iter, T, T_prec)
		T_prec = deepcopy(T)

		# check conditions --> the number of iteration is 20
		if iteration_number >= (max_iteration_number - 1):
			convergence = True

		iteration_number += 1
		#print(str(iteration_number))

	# convergence reached -- end process
	#utils_writing_results.writing_trust_results(output_file_iter, T_iter)


	return [T, C]

def run_adapted_sums_and_boost_saving_iter_real_world_v2(T_,F_s_, S_prop_, initial_confidence_, max_iteration_number_,
										   sources_dataItemValues_, output_file_, boost_dict, gamma, id_dataset, base_dir_anal_, predicate_):
	domain_ = dict()
	for d in sources_dataItemValues_:
		domain_[d] = set()
		for fact in S_prop_:
			if fact.startswith(d):
				domain_[d].add(fact)



	T_list_abs = list(T_.keys())
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
			cont_=0
			facts = F_s_.get(source_id)  # get facts provided by this source
			for f in facts:
				if not f in C:
					print("Error cannot find confidence for ", f)
					exit()
				sum = sum + (C.get(f))
				cont_ +=1
			T_[source_id] = sum/cont_

		# normalizing using the maximum value in the list of T
		#max_value = max(T_.values())
		#for source_id in T_:
		#	T_[source_id] = T_[source_id] / max_value
		##add to try
		'''max_v =  max(T_.values())
		set_app = set()
		set_app.add(max_v)
		second_max_v = max(set(T_.values()).difference(set_app))
		set_app.add(second_max_v)
		third_max_v = max(set(T_.values()).difference(set_app))
		for source_id in T_:
			if T_[source_id]== max_v or T_[source_id] ==second_max_v:
				T_[source_id] = third_max_v'''
		'''for source_id in T_:
			if len(F_s_[source_id])/len(sources_dataItemValues_) > 0.80:
				if T_[source_id] - 0.5 < 0:
					T_[source_id] = 0.0
				else:
					T_[source_id] = T_[source_id]-0.5
			if len(F_s_[source_id]) / len(sources_dataItemValues_) < 0.20:
				if T_[source_id] + 0.5 > 1.0:
					T_[source_id] = 1.0
				else:
					T_[source_id] = T_[source_id] + 0.5'''

		C = dict()
		###
		for d in sources_dataItemValues_:
			denomin = 0.0
			for fact_id in domain_[d]:
				source_plus_set = S_prop_.get(fact_id).split(";")
				sum = 0.0
				for s in source_plus_set:

					try:
						# s = int(s)
						sum = sum + T_[s]
					except ValueError:
						sum = sum + T_[int(s.replace("source", ""))]

				C[fact_id] = sum
				#denomin += sum
				if sum>denomin:
					denomin = sum
			for fact_id in domain_[d]:
				C[fact_id] /= denomin
		'''for fact_id in S_prop_:
			source_plus_set = S_prop_.get(fact_id).split(";")
			sum = 0
			for s in source_plus_set:

				try:
					#s = int(s)
					sum = sum + T_[s]
				except ValueError:
					sum = sum + T_[int(s.replace("source", ""))]

			C[fact_id] = sum'''
		# normalization
		#max_value = max(C.values())
		#for item in C:
		#	C[item] = C.get(item) / max_value
		###add rule influence
		#####add rule influence
		if (iteration_number >= max_iteration_number_ - 1):
			f_out_app = open(base_dir_anal_ + "distribution_id_" + str(id_dataset) + "_gamma_" + str(gamma) +".csv", 'w')

			for fact_id in S_prop_:
				fact_id_list = fact_id.split("http")
				d = fact_id_list[0]
				#print(d)
				value = "http"+fact_id_list[1]
				boost_factor = boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + value]
				#f_out_app.write(str(C[fact_id]) + '\t' + str(boost_factor) + '\n')
				initial_str = str(C[fact_id]) + '\t' + str(boost_factor)
				C[fact_id] = (1 - gamma) * (C[fact_id]) + gamma * math.sqrt(boost_factor)
				if predicate_ == "genre":
					dataitem_to_out = bytes(d, 'unicode-escape')
					d = str(dataitem_to_out, 'utf-8')
					value_to_out = bytes(value, 'unicode-escape')
					value = str(value_to_out, 'utf-8')
				f_out_app.write(str(initial_str) + '\t' + str(d) + '\t' + str(value) + '\t' + str(C[fact_id]) + '\n')

			f_out_app.close()
		else:
			for fact_id in S_prop_:
				fact_id_list = fact_id.split("http")
				d = fact_id_list[0]
				#print(d)
				value = "http"+fact_id_list[1]
				#print(value)
					# fact = [d, "<http://dbpedia.org/ontology/birthPlace>", value]
					# gamma = boost_dict[d+ "<http://dbpedia.org/ontology/birthPlace>" + value]
				boost_factor = boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + value]
				C[fact_id] = (1 - gamma) * (C[fact_id]) + gamma *  math.sqrt(boost_factor)
				#if boost_factor> 0.0: print(str(C[fact_id]) + "\t" + str(boost_factor))

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

		if iteration_number > 100000000:
			prec_T_list = list()
			T_list = list()
			for s_ in T_list_abs:
				prec_T_list.append(prec_T_[s_])
				T_list.append(T_[s_])

			newCosineSimilarity = cosine_similarity(prec_T_list, T_list)

			#cosineSimilarityDifference = abs(trustworthinessCosineSimilarity - newCosineSimilarity)

			if (1- newCosineSimilarity) <= 0.000001:
				convergence = True
				print(newCosineSimilarity)
			#trustworthinessCosineSimilarity = newCosineSimilarity;
		prec_T_ = copy.deepcopy(T_)
		iteration_number += 1
		if iteration_number % 200 == 0: print('Iteration ' + str(iteration_number) + ' ----- ')

	# convergence reached -- end process
	print("end after " + str(iteration_number))
	utils_writing_results.writing_trust_results(output_file_, T_iter)

	return [T_, C]


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
def run_adapted_sums_new_normalization(T_, F_s_, S_prop_, initial_confidence_, max_iteration_number_, sources_dataItemValues_,
								 output_file_, app_conf_dict, app_source_dict, root_el):
	#preprocessing F_s_prop
	F_s_prop = dict()
	for item in S_prop_:
		if type(S_prop_[item]) is set:
			for s in S_prop_[item]:
				s = int(s)
				if s not in F_s_prop:
					F_s_prop[s] = set()
				F_s_prop[s].add(item)
		else:
			for s in S_prop_[item].split(';'):
				s = int(s)
				if s not in F_s_prop:
					F_s_prop[s] = set()
				F_s_prop[s].add(item)

	import rpy2.robjects as ro
	import pandas as pd
	from rpy2.robjects import pandas2ri
	pandas2ri.activate()

	print("define function in R")
	r_src = """ function(dataf, n_iteration, col_name_to_select){
			library(dplyr)
			library(tidyr)
			library(ggplot2)
			if(n_iteration==0 | n_iteration == 19){
				p <- ggplot(dataf, aes(est_positive / est_total))
				p <- p + geom_histogram()
				ggsave(filename="a.jpg", plot=p)
				p <- ggplot(dataf, aes(est_positive))
				p <- p + geom_histogram()
				ggsave(filename="b.jpg", plot=p)
				p <- ggplot(dataf, aes(est_total))
				p <- p + geom_histogram()
				ggsave(filename="c.jpg", plot=p)
			}
			library(ebbr)

			prior <- dataf %>% ebb_fit_prior(est_positive, est_total, method="mm")
			
				augmented_prior <- (augment(prior, data = dataf))

				result_augmented <- select(augmented_prior, col_name_to_select, .fitted)
				}
		"""
	import rpy2.robjects as ro
	r_funct = ro.r(r_src)
	#r_funct_2 = ro.r(r_src_2)
	#define list of d+v (in order to keep always the same order)
	dataitem_values_list = list()
	for d in app_conf_dict:
		for v in app_conf_dict[d]:
			dataitem_values_list.append(d+ '\t' + v)
	###define list of sources (in order to keep always the same order)
	sources_list = list()
	for s in T_:
		sources_list.append(s)


	# function that implements the adapted model
	T_iter = dict()
	print("START : sums_ADAPTED " + " _ Convergence criteria : max iteration number (" + str(max_iteration_number_) + ")")

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
		#trustworthiness computation
		for source_id in T_:
			sum = 0
			facts = F_s_.get(source_id)  # get facts provided by this source
			for f in facts:
				if not f in C:
					print("Error cannot find confidence for ", f)
					exit()
				sum = sum + (C.get(f))
			T_[source_id] = sum

		#print(T_[0])
		#### normalization
		#create list of est_positive for each
		print("source for vector")
		source_for_vect = list()
		for source_id in sources_list:
			estimation = T_[source_id]
			source_for_vect.append(estimation)
		# create list of number of sources vector for each claim
		if iteration_number >= 0:#0:
			print("number of claims provided by each source vector")
			all_claims_vote_vect = list()
			for source_id in sources_list:
				claims_plus_set = F_s_prop[source_id]
				#claims_plus_set = F_s_[source_id]
				all_claims_vote_vect.append(len(claims_plus_set))

		else:
			print("lenght di app source dict " + str(len(app_source_dict)))
			all_claims_vote_vect = list()
			for source_id in sources_list:
				dataitem_set = app_source_dict[source_id]
				v = root_el#'0005575'
				tot = 0
				for d in dataitem_set:
					tot += C[d+v]
				all_claims_vote_vect.append(tot)

		#create the complete dataframe - each of them is a column
		#start_time = time.time()
		df = pd.DataFrame({
			'sources_list': sources_list,
			'est_positive': source_for_vect,
			'est_total': all_claims_vote_vect
		})
		#print("--- %s seconds to create data frame ---" % (time.time() - start_time))
		#print(df)
		#convert the format of dataframe from py to R
		#start_time = time.time()
		dataf = pandas2ri.py2ri(df)
		#print("--- %s seconds to convert data frame in R format ---" % (time.time() - start_time))
		#launch R function for estimating the new posteriori
		#start_time = time.time()
		augment_prior = r_funct(dataf, iteration_number, 'sources_list')
		#print("--- %s seconds to execute R function ---" % (time.time() - start_time))
		# convert the format of dataframe from R to py
		#start_time = time.time()
		augment_prior = pandas2ri.ri2py(augment_prior)
		#print("--- %s seconds to reconvert data frame in PY format ---" % (time.time() - start_time))
		#re-assigne the new confidence level to each C[d+v]
		#start_time = time.time()
		T_ = augment_prior.set_index('sources_list').to_dict()
		T_ = T_['.fitted']
		#print("--- %s seconds to reassigned the normalized trustowrhtiness ---" % (time.time() - start_time))
		#math.isnan(x)
		##compute confidence of claims
		C = dict()

		for fact_id in S_prop_:
			if type(S_prop_[fact_id]) is set:
				source_plus_set = S_prop_.get(fact_id)
			else:
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
		# create list of est_positive
		print("vote for vector")
		vote_for_vect = list()
		for fact_id in dataitem_values_list:
			estimation = C[fact_id.replace('\t', '')]
			vote_for_vect.append(estimation)
		# create list of number of sources vector for each claim
		'''print("number of sources vector")
		all_vote_vect = list()
		for claim in dataitem_values_list:
			d = claim.split('\t')[0]
			v = claim.split('\t')[1]
			source_plus_set = S_prop_.get(d+v).split(";")
			all_vote_vect.append(len(source_plus_set))
			#if d == 'O15399_1':
			#	print(str(v) + '\t' + str(len(source_plus_set)))
		'''
		print("est tot for each d vector")
		all_vote_vect = list()
		d_prec = ""
		for claim in dataitem_values_list:
			d = claim.split('\t')[0]
			if d == d_prec:
				all_vote_vect.append(tot)  # = r_funct_all_vote(tot, all_vote_vect)
			else:
				source_plus_set_total = set()
				v = root_el
				if type(S_prop_[d + v]) is set:
					source_plus_set_total = S_prop_.get(d + v)
				else:
					source_plus_set_total = S_prop_.get(d + v).split(";")
				'''
				for v in app_conf_dict[d]:
					source_plus_set = S_prop_.get(d+v).split(";")
					source_plus_set_total = source_plus_set_total.union(source_plus_set)
				'''
				tot = 0
				for s in source_plus_set_total:
					try:
						s = int(s)
						tot += T_[s]
					except ValueError:
						tot += T_[int(s.replace("source", ""))]
				all_vote_vect.append(tot)
				# all_vote_vect.append(len(source_plus_set_total))
				d_prec = d

		# create the complete dataframe - each of them is a column
		#start_time = time.time()
		df = pd.DataFrame({
			'claims_list': dataitem_values_list,
			'est_positive': vote_for_vect,
			'est_total': all_vote_vect
		})
		#print("--- %s seconds to create data frame ---" % (time.time() - start_time))
		# convert the format of dataframe from py to R
		#start_time = time.time()
		dataf = pandas2ri.py2ri(df)
		#print("--- %s seconds to convert data frame in R format  ---" % (time.time() - start_time))
		# launch R function for estimating the new posteriori
		#start_time = time.time()
		augment_prior = r_funct(dataf, iteration_number, 'claims_list')
		#print("--- %s seconds to execute R function ---" % (time.time() - start_time))

		# convert the format of dataframe from R to py
		#start_time = time.time()
		augment_prior = pandas2ri.ri2py(augment_prior)
		#print("--- %s seconds to reconvert data frame in PY format ---" % (time.time() - start_time))
		# re-assigne the new confidence level to each C[d+v]
		#start_time = time.time()
		augment_prior['claims_list'].replace('\t', '', regex=True, inplace=True)
		C = augment_prior.set_index('claims_list').to_dict()
		C = C['.fitted']
		#C = C['claims_list'].replace('\t', '', regex=True, inplace=True)

		#print("--- %s seconds to reassigned the normalized confidence ---" % (time.time() - start_time))

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

def run_adapted_sums_and_boost_saving_iter(T_, F_s_, S_prop_, initial_confidence_, max_iteration_number_,
										   sources_dataItemValues_, output_file_, boost_dict, gamma, id_dataset, base_dir_anal_, predicate_):
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
					#s = int(s)
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
		if (iteration_number >= max_iteration_number_ - 1):
			f_out_app = open(base_dir_anal_ + "distribution_id_" + str(id_dataset) + "_gamma_" + str(gamma) +".csv", 'w')

			for fact_id in S_prop_:
				fact_id_list = fact_id.split("http")
				d = "http"+fact_id_list[1]
				#print(d)
				value = "http"+fact_id_list[2]
				boost_factor = boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + value]
				#f_out_app.write(str(C[fact_id]) + '\t' + str(boost_factor) + '\n')
				initial_str = str(C[fact_id]) + '\t' + str(boost_factor)
				C[fact_id] = (1 - gamma) * (C[fact_id]) + gamma * boost_factor
				if predicate_ == "genre":
					dataitem_to_out = bytes(d, 'unicode-escape')
					d = str(dataitem_to_out, 'utf-8')
					value_to_out = bytes(value, 'unicode-escape')
					value = str(value_to_out, 'utf-8')
				f_out_app.write(str(initial_str) + '\t' + str(d) + '\t' + str(value) + '\t' + str(C[fact_id]) + '\n')

			f_out_app.close()
		else:
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

def run_adapted_sums_and_boost_saving_iter_real_world(T_, F_s_, S_prop_, initial_confidence_, max_iteration_number_,
										   sources_dataItemValues_, output_file_, boost_dict, gamma, id_dataset, base_dir_anal_, predicate_):
	# function that implements the adapted model using the rules
	T_list_abs = list(T_.keys())
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
		if (iteration_number >= max_iteration_number_ - 1):
			f_out_app = open(base_dir_anal_ + "distribution_id_" + str(id_dataset) + "_gamma_" + str(gamma) +".csv", 'w')

			for fact_id in S_prop_:
				fact_id_list = fact_id.split("http")
				d = fact_id_list[0]
				#print(d)
				value = "http"+fact_id_list[1]
				boost_factor = boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + value]
				initial_str = str(C[fact_id]) + '\t' + str(boost_factor)
				C[fact_id] = (1 - gamma) * (C[fact_id]) + gamma * boost_factor
				if predicate_ == "genre":
					dataitem_to_out = bytes(d, 'unicode-escape')
					d = str(dataitem_to_out, 'utf-8')
					value_to_out = bytes(value, 'unicode-escape')
					value = str(value_to_out, 'utf-8')
				f_out_app.write(str(initial_str) + '\t' + str(d) + '\t' + str(value) + '\t' + str(C[fact_id]) + '\n')

			f_out_app.close()
		else:
			for fact_id in S_prop_:
				fact_id_list = fact_id.split("http")
				d = fact_id_list[0]
				value = "http"+fact_id_list[1]
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

		prec_T_ = copy.deepcopy(T_)
		iteration_number += 1
		if iteration_number % 200 == 0: print('Iteration ' + str(iteration_number) + ' ----- ')

	# convergence reached -- end process
	print("end after " + str(iteration_number))
	utils_writing_results.writing_trust_results(output_file_, T_iter)

	return [T_, C]


# END FUNCTION ADAPTED MODEL with rules

def run_adapted_sums_and_boost_saving_iter_real_world_average(T_, F_s_, S_prop_, initial_confidence_, max_iteration_number_,
										   sources_dataItemValues_, output_file_, boost_dict, gamma, id_dataset, base_dir_anal_, predicate_):
	# function that implements the adapted model using the rules
	fact_ids_d_prop = dict()
	for d in sources_dataItemValues_:
		fact_ids_d_prop[d] = set()
		for fact_id in S_prop_:
			if d in fact_id:
				fact_ids_d_prop[d].add(fact_id)


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
			cont_ = 0
			facts = F_s_.get(source_id)  # get facts provided by this source
			for f in facts:
				if not f in C:
					print("Error cannot find confidence for ", f)
					exit()
				sum = sum + (C.get(f))
				cont_ += 1
			T_[source_id] = sum/cont_

		C = dict()
		for fact_id in S_prop_:
			source_plus_set = S_prop_.get(fact_id).split(";")
			sum = 0
			cont_ = 0
			for s in source_plus_set:

				try:
					#s = int(s)
					sum = sum + T_[s]
					cont_ += 1
				except ValueError:
					sum = sum + T_[int(s.replace("source", ""))]
					cont_ += 1

			C[fact_id] = sum

		for d in sources_dataItemValues_:
			for fact_id in fact_ids_d_prop[d]:
				C[fact_id] /= len(S_prop_[fact_id])



		###add rule influence
		#####add rule influence
		if (iteration_number >= max_iteration_number_ - 1):
			f_out_app = open(base_dir_anal_ + "distribution_id_" + str(id_dataset) + "_gamma_" + str(gamma) +".csv", 'w')

			for fact_id in S_prop_:
				fact_id_list = fact_id.split("http")
				d = fact_id_list[0]
				#print(d)
				value = "http"+fact_id_list[1]
				boost_factor = boost_dict[d + "<http://dbpedia.org/ontology/birthPlace>" + value]
				#f_out_app.write(str(C[fact_id]) + '\t' + str(boost_factor) + '\n')
				initial_str = str(C[fact_id]) + '\t' + str(boost_factor)
				C[fact_id] = (1 - gamma) * (C[fact_id]) + gamma * boost_factor
				if predicate_ == "genre":
					dataitem_to_out = bytes(d, 'unicode-escape')
					d = str(dataitem_to_out, 'utf-8')
					value_to_out = bytes(value, 'unicode-escape')
					value = str(value_to_out, 'utf-8')
				f_out_app.write(str(initial_str) + '\t' + str(d) + '\t' + str(value) + '\t' + str(C[fact_id]) + '\n')

			f_out_app.close()
		else:
			for fact_id in S_prop_:
				fact_id_list = fact_id.split("http")
				d = fact_id_list[0]
				#print(d)
				value = "http"+fact_id_list[1]
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
		if iteration_number % 200 == 0: print('Iteration ' + str(iteration_number) + ' ----- ')

	# convergence reached -- end process

	utils_writing_results.writing_trust_results(output_file_, T_iter)

	return [T_, C]


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

def run_adapted_sums_saving_iter_inverted(T_, F_s_, S_prop_, initial_confidence_, max_iteration_number_, sources_dataItemValues_,
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
	for source_id in T_:
		T_[source_id] = initial_confidence_
	# iteration for estimating C and T
	while (not convergence):
		# t_start_iter = time.time()
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

def run_adapted_sums_saving_iter_new_init_conf(T_, F_s_, S_prop_, initial_confidence_, max_iteration_number_, sources_dataItemValues_,
								 output_file_, leaves, descendants, app_conf_dict):
	# function that implements the adapted model
	T_iter = dict()
	print(
		"START : sums_ADAPTED " + " _ Convergence criteria : max iteration number (" + str(max_iteration_number_) + ")")

	convergence = False
	iteration_number = 0
	# confidences for all the facts
	# <key = dataitem + value, value = confidence>
	C = dict()
	cardinality_leaves = len(leaves)
	for d_id in app_conf_dict:
		for v in app_conf_dict[d_id]:
			if d_id+v in C:
				continue
			score_leaf = 1.0 / float(cardinality_leaves)
			initial_confidence_ = len(set(descendants[v]).intersection(leaves)) * score_leaf
			C[d_id+v] = initial_confidence_

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