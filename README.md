# TDwithRULES

Author:
 - Valentina Beretta
	
Co-authors:
 - Sebastien Harispe
 - Sylvie Ranwez
 - Isabelle Mougenot

TD with RULES permits to run experiments on an adaptation of a truth discovery model that takes into account the dependencies may exist among data items to enhance the results.
This kind of dependencies are detected identify the frequent patterns in an external knowledge base (in our experiments DBPEDIA).
We use AMIE+ (https://www.mpi-inf.mpg.de/departments/databases-and-information-systems/research/yago-naga/amie/) to extract rules (that represent the frequent patterns) from DBpedia.

## REFERENCES
*“Identification de règles pour renforcer la détection de vérité.”*. Valentina Beretta, Sébastien Harispe, Sylvie Ranwez, Isabelle Mougenot. To be published in the proceedings of WIMS 2016.


## EXPERIMENTS
For repeat the experiments you have to follow the following steps:

 - make sure that "Pyhton 3.4" is installed on your computer and use it to run the .py files 
 
## INPUTs:
 - download the birthPlace datasets at https://dx.doi.org/10.6084/m9.figshare.3393706, unzip the archive and put the folder contained the dataset that you want analyze (you can choose one predicate dataset at time) in the empty project folder named "datasets". In this way the obtained folder hierarchy is TD_withRULES/datasets/dataset_birthPlace/EXP/... .
 - download the required file wims folder at https://dx.doi.org/10.6084/m9.figshare.3393817, unzip the archive and put it in the folder named "required_files" of the project. The obtained folder hierarchy is TD_withRULES/required_files/birthPlace/

 
## RUN the experiments
 - open the terminal and move in the "experiments_with_rules" folder contained in the main project folder
 - write the following command line
	> python Experiments_with_rules.py  (to obtain the results of M1 and M2)
  or 
  > python Experiments_with_rules_with_partial_order.py  (to obtain the results of  M3 and M4)
  
## OUTPUTs:
 - all the results file will be stored in "experiments_with_rules" located in the "TD_withRULES" project folder.
 

