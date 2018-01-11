import os
import sys

cwd = os.getcwd()
sys.path.append('D:\\code_to_publish\\thesis_code\\')
print("BB")
if ("TDO") in cwd:
	#sys.path.append(cwd)
	index_tdo = cwd.index("TDO")
	cwd = cwd[:index_tdo+3]
	sys.path.append(cwd)
	cwd = cwd[:index_tdo]
	sys.path.append(cwd)
	print(sys.path)