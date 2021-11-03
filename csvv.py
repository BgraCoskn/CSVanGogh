import os.path
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib as mpl

def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if name in file:
                result.append(os.path.join(root, file))
    return result

def _init_():
    welcometext = "\nWelcome to CSVanGogh: An automated plotter for multiple CSV files and Logs"
    print(welcometext); print("For ")
    print("-"*len(welcometext))
    mainpath = os.path.dirname(os.path.abspath(__file__))
    lcsvs = find_all(".csv", mainpath)
    print("\nFound %i"%len(lcsvs) + " csv files.")
    ind = 0
    for thecsv in lcsvs:
        ind+=1
        print(str(ind)+"> " + thecsv)
    print("\nWhich ones do you want to use?\
            \n(none, all or index numbers seperated by spaces eg. 2 10 3)")

    while True:
        validinps = list()
        keyinput = input(">> ")
        if keyinput == "none": return 1 # trigger termination
        elif keyinput == "all": return lcsvs # use all csv files

        elif keyinput == "":
            print("False input. Retry.")
            continue

        inputlist = keyinput.split()
        for inp in inputlist:
            if inp.isnumeric():
                if not (int(inp) > 0 and (int(inp) <= len(lcsvs))): continue
                else: validinps.append(lcsvs[int(inp)-1])
            else:
                print("False input. Retry.")
                continue
        if len(validinps) != 0: break
    return validinps

def lst_hasnumeric(lst):
    summ = 0
    for el in lst:
        summ += int(el.isnumeric())
    return bool(summ)

class csvf:

    def __init__(self, filepath):
        headpad = 30; footpad = 20
        self.name = os.path.basename(filepath)
        self.data = pd.read_csv(filepath,\
                engine='python', skiprows=headpad, skipfooter=footpad)
        self.colcount = len(self.data.columns)
        self.rowcount = len(self.data)

        with open(filepath) as wf:
            # read the file to find the column names,
        # if the read lines length is the same as the
        # body and is only strings
        # loop over lines in a file
            for pos, l_num in enumerate(wf):
                # check if the line number is specified in the lines to read array
                cols = l_num.split(',')
                if len(cols) == self.colcount and\
                not lst_hasnumeric(cols):
                    break
            colnames = list()
            for colname in cols:
                colname = colname.title()
                colname = colname.replace(' ', '')
                colname = colname.replace('\n', '')
                colnames.append(colname)

            self.data = self.data.set_axis(colnames, axis=1)
            print(self.data)
    
    def poptime(self,popcol):
        self.timeser = self.data.pop(popcol)

def _main_(csvfs):
    if csvfs == 1:
        print("Chosen [none] exiting.")
        return 0
    
    lstobj = [0 for x in range(len(csvfs))] 
    for ind in range(0,len(csvfs)):
        cv = csvfs[ind]
        lstobj[ind] = csvf(cv)
        cvobj = lstobj[ind]
        print(cvobj)
        while(True):
            poptm = input("What column should be used as the time series?\n>>")
            try:
                lstobj[ind].poptime(poptm)
            except KeyError:
                print("Wrong key, try again")
                continue
            break
        print(lstobj[ind].data.head())
        if input("Remove columns with only zeros? [y/n]\n>>") == 'y':
            for colname in lstobj[ind].data.columns:
                if lstobj[ind].data[colname].sum() == 0:
                    lstobj[ind].data.pop(colname)
        print(lstobj[ind].data.head())

_main_(_init_())

# Find the files with the last 3 letters csv instead of searching for
# any with csv.

# There is an error with validinps being references before assignment check
# that out.





