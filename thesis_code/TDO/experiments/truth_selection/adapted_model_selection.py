import operator


def get_conf_max_for_delta_0(d, conf_dict, v_children):
	conf_list = list()
	for child in v_children:
		conf_list.append(conf_dict[d + child])
	return max(conf_list)


def get_conf_max_delta_0_opt(d, conf_dict, v_children):
	conf_list = list()
	max_v = 0
	set_of_elements = set()
	for child in v_children:
		if d + child in conf_dict:
			if (conf_dict[d + child]> max_v):
				max_v = conf_dict[d + child]
				set_of_elements.clear()
				set_of_elements.add(child)
			elif (conf_dict[d + child]== max_v):
				set_of_elements.add(child)

	return set_of_elements

def get_conf_max(d, conf_dict, v_children):
	conf_list = list()
	for child in v_children:
		if d + child in conf_dict:
			conf_list.append(conf_dict[d + child])
		else:
			# no one provides this value
			conf_list.append(0)
	return max(conf_list)

def selection_phase(d, conf_dict, threshold, delta, children, ancestors, root_element):
	v_star_temp = set()

	queue = list()
	queue.append(root_element)

	if delta == 0:
		#print("delta is 0")
		while len(queue) != 0:
			v = queue.pop()
			v_star_temp.add(v)
			if v in children:
				v_children = children[v]
			else:
				print("error, not children for value " + str(v))
				exit()
			if len(v_children) == 0:
				continue
			#conf_max = get_conf_max(d, conf_dict, v_children)
			# if conf_max > threshold:
			v_children_star = get_conf_max_delta_0_opt(d, conf_dict, v_children)
			v_to_add = v_children_star.difference(v_star_temp)
			for item in v_to_add:
				queue.append(item)

	else:
		while len(queue) != 0:
			v = queue.pop()
			v_star_temp.add(v)
			if v in children:
				v_children = children[v]
			else:
				print("error, not children for value " + str(v))
				exit()
			if len(v_children) == 0:
				continue
			conf_max = get_conf_max(d, conf_dict, v_children)
			#if conf_max > threshold:
			v_children_star = set()
			relative_delta = conf_max * delta
			for child in v_children:
				if d + child not in conf_dict:
					continue
				if abs(conf_max - conf_dict[d + child]) <= relative_delta:
					v_children_star.add(child)
			v_to_add = v_children_star.difference(v_star_temp)
			for item in v_to_add:
				queue.append(item)

	v_to_add = set()
	for item in v_star_temp:
		if item in ancestors:
			v_to_add.update(ancestors[item])
		else:
			print("ancestors not found ")
			print(item)
			exit()
	v_star_temp.update(v_to_add)

	return v_star_temp

def selection_phase_for_delta_0(d, conf_dict, threshold, delta, children_d, ancestors, root_element):
	v_star_temp = set()

	queue = list()
	queue.append(root_element)

	while len(queue) != 0:
		v = queue.pop()
		v_star_temp.add(v)
		if v in children_d.nodes:
			v_children = children_d.adjacents.get(v)
		else:
			print("error, not children for value " + str(v))
			exit()
		if v_children == None:
			continue
		conf_max = get_conf_max_for_delta_0(d, conf_dict, v_children)
		v_children_star = set()

		for child in v_children:
			if abs(conf_max - conf_dict[d + child]) <= 0:
				v_children_star.add(child)
		v_to_add = v_children_star.difference(v_star_temp)
		for item in v_to_add:
			queue.append(item)

	v_to_add = set()
	for item in v_star_temp:
		if item in ancestors:
			v_to_add.update(ancestors[item])
		else:
			print("ancestors not found ")
			print(item)
			exit()
	v_star_temp.update(v_to_add)

	return v_star_temp

def selection_phase_for_delta_1(d, conf_dict, threshold, delta, children, ancestors, root_element):
	v_star_temp = set()

	queue = list()
	queue.append(root_element)

	while len(queue) != 0:
		v = queue.pop()
		v_star_temp.add(v)
		if v in children:
			v_children = children[v]
		else:
			print("error, not children for value " + str(v))
			exit()
		if len(v_children) == 0:
			continue
		#conf_max = get_conf_max(d, conf_dict, v_children)
		conf_max = 1
		v_children_star = set()
		for child in v_children:
			if d + child not in conf_dict:
				continue
			v_children_star.add(child)
		v_to_add = v_children_star.difference(v_star_temp)
		for item in v_to_add:
			queue.append(item)

	v_to_add = set()
	for item in v_star_temp:
		if item in ancestors:
			v_to_add.update(ancestors[item])
		else:
			print("ancestors not found ")
			print(item)
			exit()
	v_star_temp.update(v_to_add)

	return v_star_temp

def selection_phase_for_delta_1_v_graph(d, conf_dict, threshold, delta, children, ancestors, root_element, ):
	v_star_temp = set()

	queue = list()
	queue.append(root_element)

	while len(queue) != 0:
		v = queue.pop()
		v_star_temp.add(v)
		if v in children:
			v_children = children[v]
		else:
			print("error, not children for value " + str(v))
			exit()
		if len(v_children) == 0:
			continue
		#conf_max = get_conf_max(d, conf_dict, v_children)
		conf_max = 1
		v_children_star = set()
		for child in v_children:
			if d + child not in conf_dict:
				continue
			v_children_star.add(child)
		v_to_add = v_children_star.difference(v_star_temp)
		for item in v_to_add:
			queue.append(item)

	v_to_add = set()
	for item in v_star_temp:
		if item in ancestors:
			v_to_add.update(ancestors[item])
		else:
			print("ancestors not found ")
			print(item)
			exit()
	v_star_temp.update(v_to_add)

	return v_star_temp

#######################################################################################################################

def create_list_for_ordering_purpose(d, value_list, discr_criteria_values_1, discr_criteria_values_2):
	rank_list_with_criteria_values = list()

	for item in value_list:
		if discr_criteria_values_2 is None:
			discr_2 = 0
		else:
			if d + item in discr_criteria_values_2:
				discr_2 = discr_criteria_values_2[d + item]
			else:
				if item in discr_criteria_values_2:
					discr_2 = discr_criteria_values_2[item]
				else:
					print("error --- item not found in ic or trust average arrays")
					print(d)
					print(item)
					exit()

		if item in discr_criteria_values_1:
			discr_1 = discr_criteria_values_1[item]
		else:
			if d + item in discr_criteria_values_1:
				discr_1 = discr_criteria_values_1[d + item]
			else:
				print("error --- item not found in ic or trust average arrays")
				print(d)
				print(item)
				exit()

		rank_list_with_criteria_values.append([item, discr_1, discr_2])

	return rank_list_with_criteria_values


def ranking_phase(d, first_ranking_criteria, second_ranking_criteria, value_list, ic_values, trust_average):
	if first_ranking_criteria == "ic":
		discr_criteria_values_1 = ic_values
	else:
		discr_criteria_values_1 = trust_average

	if second_ranking_criteria is None:
		discr_criteria_values_2 = None
	else:
		if second_ranking_criteria == "ic":
			discr_criteria_values_2 = ic_values
		else:
			discr_criteria_values_2 = trust_average

	rank_list_with_criteria_values = create_list_for_ordering_purpose(d, value_list, discr_criteria_values_1,
																	  discr_criteria_values_2)

	compleate_rank_list = sorted(rank_list_with_criteria_values, key=operator.itemgetter(1, 2), reverse=True)

	rank_list = list()
	for item in compleate_rank_list:
		rank_list.append(item[0])

	return rank_list


#######################################################################################################################

def check_ord_property(descendants, ancestors, rank_list, k):  # k is the number of expected value
	first_element = rank_list[0]
	v_star = list()
	v_star.append(first_element)

	for i in range(1, len(rank_list)):
		other_element = rank_list[i]
		add_flag = True
		for element in v_star:
			if not (other_element in descendants[element] or other_element in ancestors[element]):
				add_flag = False
				break
		if add_flag:
			v_star.append(other_element)
			if len(v_star) >= int(k):
				break

	return v_star


def check_disj_property(descendants, rank_list, k):  # k is the number of expected value
	v_star = list()
	for i in range(0, len(rank_list)):  # element = rank_list[i]
		single_element_set = set()
		single_element_set.add(rank_list[i])
		rank_set = set(rank_list)
		if set(descendants[rank_list[i]]).intersection(
				rank_set) == single_element_set:  # descendants are inclusive!!not exclusive
			v_star.append(rank_list[i])
		if len(v_star) >= k:
			break
	return v_star


def check_disj_property_not_good(descendants, ancestors, rank_list, k):  # k is the number of expected value
	first_element = rank_list[0]
	v_star = list()
	v_star.append(first_element)
	for i in range(1, len(rank_list)):  # element = rank_list[i]
		if set(descendants[rank_list[i]]).intersection(v_star) == set() and set(ancestors[rank_list[i]]).intersection(
				v_star) == set():  # descendants are inclusive!!not exclusive
			v_star.append(rank_list[i])
		if len(v_star) >= k:
			break
	return v_star


def filtering_phase(is_ord_property, descendants, ancestors, rank_list, k):
	# filtered_rank_list = list()
	if is_ord_property:
		filtered_rank_list = check_ord_property(descendants, ancestors, rank_list, k)
	else:
		filtered_rank_list = check_disj_property(descendants, rank_list, k)
	return filtered_rank_list
