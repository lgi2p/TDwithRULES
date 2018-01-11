import rpy2
from numpy import *
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2.robjects.vectors import FloatVector
from rpy2.robjects.vectors import StrVector
from rpy2.robjects import DataFrame

import rpy2.robjects as ro

if __name__ == '__main__':
	import pandas as pd
	import numpy as np

	print("OKOK")
	n = 10
	df = pd.DataFrame({
		'claims_list': [1,34,5,5],
		'est_positive': [1,34,5,5],
		'est_total': [1,34,5,5]
	})

	pandas2ri.activate()
	dataf = pandas2ri.py2ri(df)
	print(dataf)


	#r_df = pandas2ri.py2ri("dplyr")
	#tidyr = importr("tidyr")
	#utils = importr("dplyr", on_conflict="warn")
	#Lahman = importr("Lahman")
	#inizialization
	dataitem_vect = ro.r('''dataitem_vect <- c()
			dataitem_vect
					''')
	vote_for_vect = ro.r('''vote_for_vect <- c()
				vote_for_vect
						''')
	all_vote_vect = ro.r('''all_vote_vect <- c()
					all_vote_vect
							''')
	#function for filling the vectors


	r_src_function_dataitem = """
		function(item_, dataitem_vect){
	        dataitem_vect <- c(dataitem_vect, item_)
		    dataitem_vect
	  }
	"""
	r_funct_dataitem = ro.r(r_src_function_dataitem)

	r_src_function_vote_for = """
		function(item_, dataitem_vect){
		  dataitem_vect <- c(dataitem_vect, item_)
		  dataitem_vect
		  }
		"""
	r_funct_vote_for = ro.r(r_src_function_vote_for)

	r_src_function_all_vote = """
			function(item_, dataitem_vect){
			  dataitem_vect <- c(dataitem_vect, item_)
			  dataitem_vect
			  }
			"""
	r_funct_all_vote = ro.r(r_src_function_all_vote)

	for item in list_dataitem:
		print(item)
		dataitem_vect = r_funct_dataitem(item, dataitem_vect)
	#y = ro.r(r_src)
	#tuple(y.list_attrs())  # returns ('foo')

	d = {'claims_list': id_vect, 'est_positive': FloatVector([0.58, 0.88]), 'est_total':FloatVector([0.18, 0.88])}
	dataf = ro.DataFrame(d)
	print(dataf)
	df = data.frame(claims_list, est_positive, est_total)
	print(df)
	for ob in obs:
		df = df.rbind(ro.DataFrame(ob))

	print(df)
	ro.r('''pitchers <- Pitching %>% group_by(playerID) %>% summarize(gamesPitched = sum(G)) %>% filter(gamesPitched > 3)
	df <- data.frame(Char=character(), Double=double(), Double=double(),Double=double())    
	''')

	ro.r['source']("D:\\Introducing_ebbr.R")
	#print(ro.r('pitchers'))
	print(ro.r('career'))

	career = ro.r.matrix(ro.IntVector(range(6)),3)
	ro.r('career < - Batting %>% filter(AB > 0) %>% anti_join(pitchers, by="playerID") %>% group_by(playerID) %>% summarize(H=sum(H), AB=sum(AB)) %>% mutate(average=H / AB)')
	# Add player names
	ro.r('df1 < - Master % > % tbl_df() % > % select(playerID, nameFirst, nameLast) % > % unite(name, nameFirst, nameLast, sep=" ") % > % inner_join(career, by="playerID")')




	print(rpy2.__version__)

