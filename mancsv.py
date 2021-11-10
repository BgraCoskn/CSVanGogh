import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


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
                colname = colname.replace('_', '')
                colnames.append(colname)
            self.colnames = colnames
            self.data = self.data.set_axis(colnames, axis=1)
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
        self.timeser = [x/1000 for x in self.timeser] # Scaling down timeseries
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

csv_file= "Test1_Kuzey_Platform_Esneme.csv"
thedata = csvf(csv_file)
print(thedata.colnames)
chosen = ["Motorposx","Motorposy", "XactualDegree", "YactualDegree"]
figlabels = ["Motor pozisyonu ve Inklinometre açısı",
        "Zaman(s)","MotorPoz", "InklinometreDeg"]
theplot = pltcls(thedata.data, chosen)
theplot.update(figlabels[0], figlabels[1], figlabels[2], figlabels[3])
# Its show time
theplot._show_()


