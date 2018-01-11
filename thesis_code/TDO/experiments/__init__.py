import os
import sys

cwd = os.getcwd()
#if ("TDO") in cwd:
#	index_tdo = cwd.index("TDO")
#	cwd = cwd[:index_tdo]
#	sys.path.append(cwd)
sys.path.append('D:\\code_to_publish\\thesis_code\\')
print("CC")
cwd = os.getcwd()
if ("TDO") in cwd:
	index_tdo = cwd.index("TDO")
	cwd = cwd[:index_tdo + 3]
	sys.path.append(cwd)
	cwd = cwd[:index_tdo]
	sys.path.append(cwd)
	print(sys.path)