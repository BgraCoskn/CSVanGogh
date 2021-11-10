import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import http.server
import socketserver

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

def lst_hasnumeric(lst):
    # Check if list has any numeric values
    summ = 0
    for el in lst:
        summ += int(el.isnumeric())
    return bool(summ)

class csvf:
    #CSV file class,
    #inputs = string type, path to CSV file
    def __init__(self, filepath):
        headpad = 1; footpad = 20
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
                colname = colname.replace('_', '')
                colnames.append(colname)
            self.colnames = colnames
            self.data = self.data.set_axis(colnames, axis=1)
            print(colnames)
            print(self.data)

class pltcls:

    def __init__(self, dataobj, cols):

        sumcol = ""
        nmint = 0

        for coln in dataobj.columns:
            sumcol += coln.title()
        for char in sumcol:
            nmint += ord(char)
        self.nn = sumcol + "_plot"
        figdata = tuple()
        self.name = str(nmint)
        self.df = dataobj
        self.timeser = [*range(0,len(dataobj))] # Timeseries
        self.timeser = [x/100 for x in self.timeser] # Scaling down timeseries
        datalst = [0 for x in range(len(cols))]

        self.fig = make_subplots(specs=[[{"secondary_y":True}]])

        for ind, col in enumerate(cols):
            if ind >= len(cols)-2: secy = True
            else: secy = False

            self.fig.add_trace(
                go.Scatter(
                    x=self.timeser, y=dataobj[col].tolist(),
                    name=col), secondary_y=secy
                )

        # It works, it seems the x and y parameters in the function is
        # for choosing the columns from the dataframe and it was throwing
        # an error because there was no such column.
        # Here is an idea: recreate the entire dataframe and use the 
        # labels to retrieve the plots of it, then that would make things
        # faster as there is no need to choose the columns to turn into
        # lists.

        # Check: How to change the labels of axis
        # Check: How to scale the x-ticks to make them seconds
        # Check: Is there automatic scaling for multiple datasets
        # Check: How can there be multiple y-scales

    def update(self,
            fig_title, fig_xlabel, fig_ylabel, fig_ylabel2=None, ):

        self.fig.update_layout(title_text=fig_title)
        self.fig.update_xaxes(title_text=fig_xlabel)
        self.fig.update_yaxes(title_text=fig_ylabel, secondary_y=False)
        if fig_ylabel2 != None:
            self.fig.update_yaxes(title_text=fig_ylabel2, secondary_y=True)

    def _show_(self):
        self.fig.show()

def main(csv_file, ch_cols, figlabels):

    """
        Put the csv file in the same directory as the code.
        First run the code after writing the csv file to be opened.
        It will give an error as there are no appropriate columns in the
        parameters. Find the names of the data columns you want to use in
        the terminal output. Write these names into the source script and
        run it again. You should see the plot coming up in your browser.
    """

    csv_data= csvf(csv_file)
    print(csv_data.colnames)
    theplot = pltcls(csv_data.data, ch_cols)
    #theplot.update(figlabels[0], figlabels[1], figlabels[2], figlabels[3])
    # Its show time
    theplot._show_()
    pio.write_html(theplot.fig, file=theplot.name+'.html', auto_open=True)

# Example
#main("Test1_Kuzey_Platform_Esneme.csv",
#  ["Motorposx","Motorposy", "XactualDegree", "YactualDegree"],
#   ["Motor pozisyonu ve Inklinometre açısı",
#       "Zaman(s)","MotorPoz", "InklinometreDeg"])

"""
main("lasertracker.csv",
    ["A"],
    [".",
        "Zaman(s)","."])
main("lastrack2.csv",["LposfeedY"],[".",".","."])
""""""
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Plot serving at", PORT)
    httpd.serve_forever()

""" 

def get_data(csvobj, colname):
    datalst = csvobj.data[colname].tolist()
    return datalst

def get_error(dt1, dt2):
    # Match the data list lengths
    if len(dt1) >= len(dt2): dt1 = dt1[:len(dt2)]
    elif len(dt2) >= len(dt1): dt2 = dt2[:len(dt1)]

    errlst = [0 for x in range(len(dt1))] # Define the error dataset

    # Calculate the difference of datasets
    cnt = 0
    for d1, d2 in zip(dt1, dt2):
        errlst[cnt] = (d1-d2)
        cnt += 1

    return errlst

timeser = []
def adtrc(figobj,datalst,strname,secondy=False):
    # Add a graph to the figure

    timeser = [*range(0,len(datalst))]  # Timeseries is the data number
    timeser = [x/100 for x in timeser] # SamplingPeriod=10ms

    figobj.add_trace(go.Scatter(x=timeser, y=datalst, name=strname),
            secondary_y=secondy)

# -----------------------------------------------------------------------------

# CSV Files to be read, get the column names from the outputs
csvd1 = csvf("lasertracker22.csv")
csvd2 = csvf("test2_son.csv")

# Data lists
lposfeedy = get_data(csvd1, "LposfeedY")
lasery = get_data(csvd2, "LaserY")
lposfeedyext = get_data(csvd1, "LposfeedYext")
lposrefy = get_data(csvd1, "LposrefY")

# Error lists
las_inc =get_error(lasery, lposfeedy)
las_ext = get_error(lasery, lposfeedyext)
las_ref = get_error(lasery, lposrefy)
ref_inc = get_error(lposrefy, lposfeedy)

fig = make_subplots(specs=[[{"secondary_y":True}]]) # Add a second Y-axis
fig.update_layout(plot_bgcolor="#eee") # Background Color

adtrc(fig, lposfeedy, "lposfeedY", secondy=False)
adtrc(fig, lasery, "laserY", secondy=False)
adtrc(fig, lposfeedyext, "lposFeedYext", secondy=False)
adtrc(fig, lposrefy, "lPosRefY", secondy=False)

adtrc(fig, las_inc, "LaserY-lPosFeedY", secondy=True)
adtrc(fig, las_ext, "LaserY-lPosFeedYext", secondy=True)
adtrc(fig, las_ref, "LaserY-lPosRefY", secondy=True)
adtrc(fig, ref_inc, "lPosRefY-lposFeedY", secondy=True)

fig.show()
pio.write_html(fig, file='LaserTrackerError.html', auto_open=True)
