#! /usr/bin/python3

import glob
import os
import stat
import shutil
import re

current_dir = os.getcwd() + "/"
os.chdir(current_dir)

resummino_dir = current_dir + "resummino-releases"
input_dir = current_dir + "output/"
output_dir = current_dir + "Juri_results/"

if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
    os.mkdir(output_dir)
else:
    os.mkdir(output_dir)

######################
### 1. INPUT FILES ###
######################

### list files to remove
temp_filenames = ["hino.in", "slha.in", "wino.in"]

input_file_list = sorted(glob.glob(input_dir + "/*.in"))

for i in range(len(temp_filenames)):
    for j in range(len(input_file_list)):
        
        check = input_file_list[j].find(temp_filenames[i])
        
        if (check != -1):
            del(input_file_list[j])
            break

################################
#### 2. WRITE BATCH FUNCTION ###
################################
    
def process_ID(resummino_input_file):
    
    resummino_input = open(resummino_input_file, "r", encoding='utf-8')
    lines = resummino_input.readlines()
    
    # Strips the newline character
    for i in range(len(lines)):
        i += 1
        
        check = lines[i].find("particle1 = ")
        if not(check == -1):
            temp1 = lines[i].split()
            particle_1_id = int(temp1[len(temp1)-1])
            break
        
    temp2 = lines[i+1].split()
    particle_2_id = int(temp2[len(temp2)-1])
    

    ###
    # 0 - all processes
    # 1 - slepton pair
    # 2 - electroweakino pair
    ###

    process_ID = 0

    if ((abs(particle_1_id) == 1000011) and (abs(particle_1_id) == abs(particle_2_id))): ### slepton pair production
        process_ID = 1
    elif ((abs(particle_1_id) == 1000022) and (abs(particle_1_id) == abs(particle_2_id))): ### electroweakino pair production
        process_ID = 2
    
    
    if ((process_ID == 1) or (process_ID == 2)):
        flag_accuracy = "--nnll"
    elif (process_ID == 0):
        flag_accuracy = "--nll"
    
    return flag_accuracy
        
    
def write_batch(input_file_list_arg):

    run_file_name = "run_file.run"
    run_file = open(run_file_name, "w")
    run_text = ""

    for i in range(len(input_file_list_arg)):
        
        process_flag = process_ID(input_file_list_arg[i])
        
        temp = input_file_list_arg[i].split("/")
        filename = temp[len(temp) - 1]
                
        indent = "#!/bin/bash\n\n#SBATCH --ntasks-per-node=1      # Tasks per node\n#SBATCH --nodes=1                # Number of nodes requested\n#SBATCH --time=60:00:00          # walltime\n\n#SBATCH --mail-type=ALL\n#SBATCH --mail-user=fiaschi@liverpool.ac.uk\n\nmodule load gsl\nmodule load boost\n\ncd " + current_dir + "\n"

        sub_file_name = "batch_" + filename + ".sub"
        output_file_name = filename[:-3] + "_temp.out"
        
        indent += "./resummino-releases/bin/resummino " + process_flag + " " + input_file_list_arg[i] + " > " + output_dir + output_file_name

        batch_file = open(sub_file_name, "w")
        batch_file.write(indent)
        batch_file.close()
        
        run_text += "sbatch " + sub_file_name + "\n\n"
        
    run_file.write(run_text)
    run_file.close()

    st = os.stat(run_file_name)
    os.chmod(run_file_name, st.st_mode | stat.S_IEXEC)


write_batch(input_file_list)
