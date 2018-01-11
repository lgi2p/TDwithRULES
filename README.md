# TDwithRULES

Author:
 - Valentina Beretta
	
Co-authors:
 - Sylvie Ranwez
 - Sebastien Harispe
 - Isabelle Mougenot

TD with RULES permits to run experiments on an adaptation of a truth discovery model that takes into account the dependencies may exist among data items to enhance the results. As proof of concept, Sums and Adapted Sums model have been modified.
This kind of dependencies are detected identifying the frequent patterns from an external knowledge base (in our experiments DBPEDIA).
We use AMIE+ (https://www.mpi-inf.mpg.de/departments/databases-and-information-systems/research/yago-naga/amie/) to extract rules (that represent the frequent patterns) from DBpedia.

## REFERENCES
Paper under review.


## EXPERIMENTS
For repeat the experiments you have to follow the following steps:

 - make sure that "Pyhton 3.4" is installed on your computer and use it to run the .py files 
 
## INPUTs:
 - download the birthPlace datasets at https://dx.doi.org/10.6084/m9.figshare.5777790, unzip the archive and put the folder contained the dataset that you want analyze (you can choose one predicate dataset at time) in the empty project folder named "datasets". In this way the obtained folder hierarchy is TD_withRULES/datasets/dataset_birthPlace/EXP/... .
 - download the required file wims folder at https://doi.org/10.6084/m9.figshare.5777778, unzip the archive and put it in the folder named "required_files" of the project. The obtained folder hierarchy is TD_withRULES/required_files/birthPlace/

 
## RUN the experiments
 - open the terminal and move in the "experiments" folder contained in the main project folder
 - write the following command line
	> python experiments_eswc.py predicate Sums&Rules_flag AdaptedSums&Rules_flag gamma_list absolute_path_of_required_files_dir absolute_path_of_results_dir max_iteration_number
	where predicate specifies the predicate to test, Sums&Rules_flag == True and AdaptedSums&Rules_flag == True specify that both model will be tested.
   Example:
	> python experiments_eswc.py genre True False [0.0,0.1,0.9] D:/thesis_code/TDO/ D:/results_rules_8_jan/ 20
 
  
## OUTPUTs:
 - all the results file will be stored in the directory indicated in absolute_path_of_results_dir parameter.
 - they can be summarised writing the following command line:
  	> python analysis_res_eswc.py predicate absolute_path_of_required_files_dir absolute_path_of_results_dir gamma_list
   Example:
	genre D:/thesis_code/TDO/ D:/results_rules_8_jan/ True True [0.1,0.9]
 

