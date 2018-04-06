import os
import sys
cwd = os.getcwd()
if ("TDO") not in cwd:
	print("error with sys.path")
	exit()
else:
	index_tdo = cwd.index("TDO")
	cwd = cwd[:index_tdo+3]#+3] #+  "/"
	sys.path.append(cwd)
	cwd = cwd[:index_tdo]  # +3] #+  "/"
	sys.path.append(cwd)

print("Experiments with rules -- Sums & Rules -- genre ")
#os.system("python selection_algorithm_experiments_normalized.py birthPlace 0 1 False ic source_average False [dataset-2_100,dataset-2_101,dataset-2_102,dataset-2_103,dataset-3_100,dataset-3_101,dataset-3_102,dataset-3_103,dataset-4_100,dataset-4_101,dataset-4_102,dataset-4_103,dataset-5_100,dataset-5_101,dataset-5_102,dataset-5_103,dataset_200,dataset_201,dataset_202,dataset_301,dataset_50,dataset_51,dataset_52,dataset_53,dataset_54]")
os.system("python dataset_analysis.py")
