# TDwithRULES

Author:
 - Valentina Beretta
	
Co-authors:
 - Sylvie Ranwez
 - Sebastien Harispe
 - Isabelle Mougenot

TD with RULES permits to run experiments on an adaptation of a truth discovery model that takes into account the dependencies may exist among data items to enhance the results. As proof of concept, Sums model has been modified.
This kind of dependencies are detected identifying the frequent patterns from an external knowledge base (in our experiments DBPEDIA).
We use AMIE+ (https://www.mpi-inf.mpg.de/departments/databases-and-information-systems/research/yago-naga/amie/) to extract rules (that represent the frequent patterns) from DBpedia.

## REFERENCES
Paper under review.


## EXPERIMENTS
For repeat the experiments you have to follow the following steps:

 - make sure that "Pyhton 3.4" is installed on your computer and use it to run the .py files 
 
## INPUTs:
 - the real world datasets are already in the "real_world_dataset" project folder
 - download the birthPlace synthetic datasets at https://dx.doi.org/10.6084/m9.figshare.5777790, unzip the archive and put the folder contained the dataset that you want analyze (you can choose one predicate dataset at time) in the empty project folder named "datasets". In this way the obtained folder hierarchy is TD_withRULES/datasets/dataset_birthPlace/EXP/... .
 - download the required file folder at https://doi.org/10.6084/m9.figshare.5777778, unzip the archive and put it in the folder named "required_files" of the project. The obtained folder hierarchy is TD_withRULES/required_files/birthPlace/

## RUN the experiments on Real-world Data
 - open the terminal and move in the "exp_real_world" folder contained in the main project folder
 - write the following command line:  
  \> python Exps_RULEs_REAL_data.py 
 - outputs:
   - all results will be directly displayed
 - note that the source code of the extraction protocols that were used to create these datasets is provided  in "extraction_protocols" folder
  
## RUN the experiments on Synthetic Data
 - open the terminal and move in the "experiments" folder contained in the main project folder
 - write the following command line:  
     \> python experiments\_iswc.py *predicate Sums&Rules\_flag AdaptedSums&Rules\_flag gamma\_list absolute\_path\_of\_required\_files\_dir absolute\_path\_of\_results\_dir max\_iteration\_number*  
	where *predicate* specifies the predicate to test, *Sums&Rules\_flag* == True and *AdaptedSums&Rules\_flag* == True specify that both model will be tested.  
    Example:  
    \> python experiments\_iswc.py genre True False [0.0,0.1,0.9] D:/thesis\_code/TDO/ D:/results\_rules\_8\_jan/ 20   
- outputs:
  - all the results file will be stored in the directory indicated in absolute\_path\_of\_results\_dir parameter.
  - they can be summarised writing the following command line:  
    \> python analysis\_res\_iswc.py *predicate absolute\_path\_of\_required\_files\_dir absolute\_path\_of\_results\_dir gamma\_list*  
    Example:  
    \> python analysis\_res\_iswc.py genre D:/thesis\_code/TDO/ D:/results\_rules\_8\_jan/ True True [0.1,0.9]
 

