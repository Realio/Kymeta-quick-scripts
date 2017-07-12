
'''
Created on Jul 10, 2017

@authors: kau,jwilcox
'''

import os
from shutil import copy
from Tkinter import *
from tkFileDialog import askopenfilename
from tkFileDialog import askdirectory

json_list = []

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
my_values = askopenfilename(initialdir = "Desktop", title = "Please choose your text file that contains the BEST serial numbers")
my_path = askdirectory(initialdir =  "K:\Public\Engineering\LabData\Ku Radial\Test Data\Ku 70cm\mTennaU7 (5.1 TFT)", title = "Please choose the directory where the optimized Jsons reside")
my_destination = askdirectory(initialdir =  my_path, title = "Where do you want the chosen BEST Jsons to go?")
print "Here is where you are getting your best serial numbers from:" + (my_values)
print "Here is which files you are choosing from:" + (my_path)
print "Here is where you are writing the files to:" + (my_destination)


with open(my_values) as myfile:
    a = myfile.readlines()  #   parsing values in from text file
    json_list[:] = [line.rstrip('\n') for line in a]  #   removing newlines
print "These are the selected serial numbers:"
print json_list

for file in os.listdir(my_path):
    if file.endswith(".s2p") or (file.endswith('.json')):  #select files
        for i in json_list:
            if i == file.split('_',1)[0]:
                #print file
                copy(os.path.join(my_path,file),my_destination)  #copy that file to a new folder


print 'script was successfull'
