#! /usr/bin/python3

import os
import glob
import stat


### Function that writes the batch file
def write_batch(filepath, resummino_dir):
    
    batch_text = ""
    batch_text += "#!/bin/sh"
    batch_text += "\n"
    batch_text += "\n"
    
    batch_text += "#SBATCH --ntasks-per-node=1	 # Tasks per node"
    batch_text += "\n"
    batch_text += "#SBATCH --nodes=1                # Number of nodes requested"
    batch_text += "\n"
    batch_text += "#SBATCH --time=00:30:00          # walltime" ### for electoweakino pairs max 10-15 minutes are needed.
    #batch_text += "#SBATCH --time=00:20:00          # walltime" ### for slepton pairs max 7-8 minutes are needed.
    batch_text += "\n"
    batch_text += "\n"
    #batch_text += "#SBATCH --mail-type=ALL"
    batch_text += "#SBATCH --mail-type=FAIL,TIME_LIMIT"
    batch_text += "\n"
    batch_text += "#SBATCH --mail-user=fiaschi@liverpool.ac.uk"
    batch_text += "\n"
    batch_text += "\n"
    batch_text += "module load gsl"
    batch_text += "\n"
    batch_text += "module load boost"
    batch_text += "\n"
    batch_text += "\n"
    batch_text += "cd " + resummino_dir
    batch_text += "\n"
    batch_text += "\n"
    batch_text += "./bin/resummino --nnll " + filepath + ".in" + " > " + filepath + "_temp.out"    
    
    batch_file = open(filepath + ".run", "w+")
    batch_file.write(batch_text)
    batch_file.close()
    
    return filepath + ".run"


##############################
### 0. SETTING DIRECTORIES ###
##############################

current_dir = os.getcwd() + "/"

resummino_dir = "/home/jf4y18/Resummino/resummino-3.1.1/resummino-releases/"
#input_dir = current_dir + "outputs/"
input_dir = "/home/jf4y18/Resummino/resummino-3.1.1/SUSY_LHC/outputs/"


processes = ["sleptons_2000011_-2000011", "hino_deg_1000022_1000023", "hino_deg_1000022_1000024", "hino_deg_1000022_-1000024", "hino_deg_1000024_-1000024"]
#energy = 13600
energy = 13000


######################
### 1. INPUT FILES ###
######################

current_process = processes[4]
input_dir = "/home/jf4y18/Resummino/resummino-3.1.1/SUSY_LHC/outputs/output_" + str(energy) + "_" + current_process + "/"
#input_dir = current_dir + "outputs/output_" + str(energy) + "_" + current_process + "/"
output_dir = input_dir

#output_dir = current_dir + "output_results/" + current_process + "/"
#if not(os.path.exists(output_dir)):
    #os.mkdir(output_dir)

flag_accuracy = "--nnll"


### Read list of input files
input_file_list = sorted(glob.glob(input_dir + "/*.in"))


########################
### 2. PREPARE BATCH ###
########################

### Split the submission in blocks of 100
text_submission = ""

counter = 0
for j in range(len(input_file_list)):

    temp = input_file_list[j].split("/")
    filename = temp[len(temp) - 1][:-3]
    
    batch_file_name = write_batch(input_dir + filename, resummino_dir)
    
    text_submission += "sbatch " + batch_file_name
    text_submission += "\n"
    text_submission += "\n"
    
    ### Every 100 batches prepare one submission file
    if ((j+1)%100 == 0):
    #if ((j+1)%10 == 0):
        
        submission_file_name = output_dir + current_process + "_" + str(counter) + ".run"
        submission_file = open(submission_file_name, "w+")
        submission_file.write(text_submission)
        submission_file.close()
        
        #### Make the file executable        
        st_submission_file = os.stat(submission_file_name)
        os.chmod(submission_file_name, st_submission_file.st_mode | stat.S_IEXEC)
        
        counter += 1
        text_submission = ""
        
### Write the remaining batches
submission_file_name = output_dir + current_process + "_" + str(counter) + ".run"
submission_file = open(submission_file_name, "w+")
submission_file.write(text_submission)
submission_file.close()

#### Make the file executable
st_submission_file = os.stat(submission_file_name)
os.chmod(submission_file_name, st_submission_file.st_mode | stat.S_IEXEC)
