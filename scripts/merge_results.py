#! /usr/bin/python3

import os
import shutil
import glob
import re

##############################
### 0. SETTING DIRECTORIES ###
##############################

current_dir = os.getcwd() + "/"


processes = ["sleptons_2000011_-2000011", "hino_deg_1000022_1000023", "hino_deg_1000022_1000024", "hino_deg_1000022_-1000024", "hino_deg_1000024_-1000024"]

#energy = 13600
energy = 13000


current_process = processes[4]
input_dir = current_dir + "output_" + str(energy) + "_" + current_process + "/"

input_file_list = sorted(glob.glob(input_dir + "/*.in"))



for j in range(len(input_file_list)):

    input_filename = input_file_list[j]


    ### read the input file
    input_file = open(input_filename, "r")
    input_text = input_file.read()
    input_file.close()

    ### read the slha file name associated to the input file
    slha_line = re.findall("^.*slha =.*$", input_text, re.MULTILINE)[0]
    slha_filename = slha_line.split()[2]

    ### open and read the slha file associated to the input file
    slha_file = open(input_dir + slha_filename, "r")
    slha_text = slha_file.read()
    slha_file.close()

    ### open and read the output file
    output_filename = input_filename[:-3] + "_temp.out"
    output_file = open(output_filename, "r")
    output_text = output_file.read()
    output_file.close()

    ### merge all three
    text = ""
    text += input_text
    text += "\n"
    text += "\n"
    text += slha_text
    text += "\n"
    text += "\n"
    text += output_text

    complete_output_filename = input_filename[:-3] + ".out"
    complete_output_file = open(complete_output_filename, "w+")
    complete_output_file.write(text)
    complete_output_file.close()
