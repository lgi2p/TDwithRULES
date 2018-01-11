def creating_normalized_for_d_estimation(ground, conf_adapt_):
	n_substituition = 0
	d_cont = 0
	for d in ground:
		present = False
		conf_dict = dict()
		for item in conf_adapt_:
			if item.startswith(d):
				conf_dict[item] = conf_adapt_[item]
				present = True
		if present:
			norm_factor = max(conf_dict.values())

			for item in conf_dict:
				conf_adapt_[item] = float(conf_adapt_[item]) / float(norm_factor)
				n_substituition += 1
		d_cont += 1
		if d_cont % 2000 == 0:
			print("processed data items : " + str(d_cont))
	print("number of replacement " + str(n_substituition))
	return conf_adapt_


def creating_normalized_for_d_estimation_optimized(ground, conf_adapt_, app_conf_dict_):
	n_substituition = 0
	d_cont = 0
	for d in ground:
		conf_dict = dict()
		if d in app_conf_dict_:
			for v in app_conf_dict_[d]:
				#for v in domain_d:
				conf_dict[d+v] = conf_adapt_[d+v]

			norm_factor = max(conf_dict.values())
			if norm_factor != 0:
				for item in conf_dict:
					conf_adapt_[item] = float(conf_adapt_[item]) / float(norm_factor)
					n_substituition += 1

		d_cont += 1
		if d_cont % 5000 == 0:
			print("processed data items : " + str(d_cont))
	print("number of replacement " + str(n_substituition))
	return conf_adapt_