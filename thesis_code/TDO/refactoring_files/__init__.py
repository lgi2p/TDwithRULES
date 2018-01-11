import os
import sys

cwd = os.getcwd()
index_tdo = cwd.index("TDO")
cwd = cwd[:index_tdo]
sys.path.append(cwd)