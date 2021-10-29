import os.path
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib as mpl

mainpath = os.path.dirname(os.path.abspath(__file__))
print("Current directory is", mainpath)
ext = '.csv'
dirs = os.listdir(mainpath)

def write_to_matfile(contstr, file_name):
		with open(file_name, 'w', encoding='utf-8') as matfile:
				matfile.write(contstr)
				print("Writing to matlab file completed")


class plotter:
		def __init__(self, y_name, fig_title, fig_shape=[1,1,1], x_name = "Time"):
				self.x_name = x_name
				self.y_name = y_name
				self.fig_shape = fig_shape
				self.fig_title = fig_title
		def dotmat(self):
				dotmat_plot_ = "subplot(%i,%i,%i);\nplot(%s,%s);\n"%(\
				self.fig_shape[0], self.fig_shape[1], self.fig_shape[2],\
				self.x_name, self.y_name)

				dotmat_plot = "figure;\nplot(%s,%s);\n"%(\
				self.x_name, self.y_name)

				dotmat_labels = "title('%s');\nxlabel('%s');\nylabel('%s')"%(\
				self.fig_title, self.x_name, self.y_name)
				dotmat_footer = "\ngrid on;\nax=gca;\nax.GridColor=[0 0.75 0.75];\n"+\
				"ax.GridLineStyle='--';\nax.GridAlpha=0.5;\nax.Layer='top';"
				return dotmat_plot + dotmat_labels + dotmat_footer + "\n\n"

def matcoder():
	for _dir in dirs:
			if _dir[0] != "2": continue # if the directory isn't from test data
			print("processing the directory: ", _dir)
			MATname = "analysis_" + _dir + ".mat"
			print("Naming the matlab file as " + MATname)
			datestr = _dir[6:] + "." + _dir[4:6] + "." + _dir[:4]
			MATheader =\
					"\nTest Date: %s \
					\nclc; clear all; close all; warning off all;\n\
					isOctave = exist('OCTAVE_VERSION', 'builtin') ~= 0;\n"\
					%datestr
			curpath = os.path.join(mainpath, _dir)
			csvlist = os.listdir(curpath)

			for csvi in csvlist:
					if csvi[-3:] != "csv": continue # if it isn't a csv file skip it
					with open(os.path.join(curpath, csvi)) as wf:
							# lines to print
							specified_lines = [6]
							# loop over lines in a file
							for pos, l_num in enumerate(wf):
									# check if the line number is specified in the lines to read array
									if pos in specified_lines:
											# print the required line number
											cols = l_num.split(',')
					colnames = list()
					for colname in cols:
							colname = colname.title()
							colname = colname.replace(' ', '')
							colname = colname.replace('\n', '')
							colnames.append(colname)
					csvdf = pd.read_csv(os.path.join(curpath, csvi),\
							engine='python', skiprows=26, skipfooter=50)
					# for the names of the data get the 7th line from the file
					# open a file
					csvdf = csvdf.set_axis(colnames, axis=1)
					#print(csvdf.columns)
					csvdf.pop('Name') # Remove the name columns (timeseries)
					print(csvdf) 
					csv_newtitle = "dm_" + ((csvi.title()).replace(' ', ''))\
							.replace('Csv', 'csv')
					csvdf.to_csv(csv_newtitle, index = False)

					MATheader =\
					"\n %% Test Date: %s"%datestr+\
					"\nisOctave = exist('OCTAVE_VERSION', 'builtin') ~= 0;\n"\
					

					MATtop = "clc; clear all; close all; warning off all;\n"+\
							"data = csvread('%s', 1);\n"%(csv_newtitle)

					MATbody = MATheader + MATtop # Add to this string

					MATbody += "Time = 1:1:%i;\n"%(csvdf.shape[0])

					clist = csvdf.columns
					lt_plot = [None for x in range(len(clist))]
					for ind in range(1,csvdf.shape[1]):
							cname = clist[ind-1]
							dataline = "%s = data(:,%i);\n"%(cname, ind)
							MATbody += dataline
							lt_plot = plotter(x_name='Time', y_name=cname,\
							fig_title="%s by time"%cname)
							MATbody += lt_plot.dotmat()
					
					print(MATbody)
					write_to_matfile(MATbody, csv_newtitle[:-4] + ".m")


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
	lcsvs = find_all(ext, mainpath)
	print("\nFound %i"%len(lcsvs) + " csv files.")
	ind = 0
	for thecsv in lcsvs:
		ind+=1
		print(str(ind)+"> " + thecsv)
	print("\nWhich ones do you want to use?\
		\n(none, all or index numbers seperated by spaces eg. 2 10 3)")
	
	while(True):

		keyinput = input(">> ")
		if keyinput == "none": return 1 # trigger termination
		elif keyinput == "all": return lcsvs # use all csv files

		elif keyinput == "":
			print("False input. Retry.")
			continue
		
		inputlist = keyinput.split()
		validinps = list()
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

class csvfile:

	def __init__(self, filepath):
		headpad = 30; footpad = 50
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

		self.xseries = csvdf.pop('Name') # Remove the name columns (timeseries)
		print(csvdf)


class dataset(csvfile):
	pass

def _main_(csvfs):
	if csvfs == 1:
		print("Chosen [none] exiting.")
		return 0
	for cv in csvfs 


_main_(_init_())



		
		


