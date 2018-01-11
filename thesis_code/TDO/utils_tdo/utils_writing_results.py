def writing_trust_results(output_file, T):
	#print("flushing the trust result into file.....")
	try:
		file = open(output_file, "w")
		for source_id in T:
			file.write(str(source_id) + "\t" + str(T[source_id]) + "\n")

		file.close()
		return True
	except:
		print("Errors in saving error rate trust estimations")
		return False


def writing_trust_results_for_convergence(output_file, T_new, T_prec):
	#print("flushing the trust result into file.....")
	try:
		file = open(output_file, "a")
		tot_diff = 0
		for source_id in T_new:
			tot_diff += abs(T_new[source_id] - T_prec[source_id])
		tot_diff /= len(T_new)
		str_out = str(tot_diff)
		if tot_diff > 0.0000001:
			str_out += "\th\n"
		else:
			str_out += "\n"
		file.write(str_out)
		file.close()
		return True
	except:
		print("Errors in saving error rate trust estimations")
		return False


