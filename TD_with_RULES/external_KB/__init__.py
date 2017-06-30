import os
import sys

cwd = os.getcwd()
index_tdo = cwd.index("TD_with_RULES")
cwd = cwd[:index_tdo]
sys.path.append(cwd)