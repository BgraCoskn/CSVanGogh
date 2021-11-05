import os.path
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

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
    """
        CSV file class,
        inputs = string type, path to CSV file
        methods =
            poptime #
    """

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
        # If there is a column to be used as time series
        if popcol != "":
            self.timeser = self.data.pop(popcol)


class pltcls:
    """
        Plot class
        inputs: Pandas.DataFrame
        methods:
            set_title: sets title for the plot
            set_labels: sets axis labels
    """
    def __init__(self, dataset):
        sumcol = ""
        nmint = 0

        for coln in dataset.columns:
            sumcol += coln.title()
        for char in sumcol:
            nmint += ord(char)
        self.nn = sumcol + "_plot"
        self.name = str(nmint)
        self.fig, self.axs = plt.subplots(figsize=(20,20))
        self.dataset = dataset
        self.dataset.plot(ax=self.axs)
        print("Created plot object: " + self.name)

    def set_title(self, titlestr):
        # set the title for the plot
        self.axs.set_title(titlestr)

    def save(self):
        self.fig.savefig(self.name+".png")

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

        while True :
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
        print("Column names are: ")
        print(lstobj[ind].data.columns)

        while True :
            rnmcol=input(\
            "Do you want to rename any of them? [no, 1, 2,...]\n>>")
            if rnmcol.isnumeric():
                if int(rnmcol) <= len(lstobj[ind].data.columns)\
                and int(rnmcol) > 0:
                    nwname = input("Input new name:\n>>")
                    lstobj[ind].data.rename(\
                    columns={lstobj[ind].data.columns[int(rnmcol)-1]:nwname},\
                    inplace=True)
            elif rnmcol == "no": break
            else:
                print("Wrong input, try again")
                continue
        print(lstobj[ind].data.columns)

        print(\
            "What columns do you want to plot together?"+\
            "\nWrite the column names you want to group seperated by commas"+\
            "\nAnd seperate the groups with spaces"+\
            "\nExample: XTorque,Xspeed YTorque,Yspeed")


        while True:
            wrongkey = 0 # Wrong input flag
            grps = input(">> ") # groups input

            if grps != "":
                for grp in grps.split():
                    for col in grp.split(','):
                        if not col in lstobj[ind].data.columns:
                            # If even one of the columns entered by the user
                            # doesn't match The data in the object then raise a
                            # flag and continue the infinite loop
                            wrongkey = 1

            if wrongkey == 0: break # no false input entered, break out the loop
            print("False input, try again")
            continue

        # Create the plot objects
        pltobj = [0 for x in range(len(grps))]
        for grpn, grp in enumerate(grps.split()):
            pltobj[grpn] = pltcls(lstobj[ind].data[grp.split(',')])
            figtitle = input("Do you want to give a title to "+\
                pltobj[grpn].nn + "?" + "\nLeave empty if no." + ">> ")
            if figtitle != "":
                pltobj[grpn].set_title(figtitle)

            pltobj[grpn].save()
            #plt.show()




_main_(_init_())

# Find the files with the last 3 letters csv instead of searching for
# any with csv.




