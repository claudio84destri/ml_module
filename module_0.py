# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
|                       About This Module:                                    |
-------------------------------------------------------------------------------
|   Created on Tue Jan 30 10:50:05 2018                                       |
|                                                                             |
|   @author: [Nespoli Claudio; Swarup Selvaraj]                               |
|                                                                             |
|   Subject : Object Oriented Programming Module using PANDAS Dataframe.      |
-------------------------------------------------------------------------------
"""
#=============================================================================#
# Import Libraries
#=============================================================================#
import pandas as pd                       #  1
import datetime as dt                     #  2

print("Welcome to version 0 of Module 0 ")

#=============================================================================#
# Function Definitions
#=============================================================================#

#-----------------------------------------------------------------------------#
# Drop Columns from Dataframe
def dropColumns(dataframe, varstokeep=""):
    return dataframe.drop( list( set(dataframe.columns.tolist()) - set(varstokeep) ), axis=1 )       

#=============================================================================#
# Class Definitions
#=============================================================================#

#-----------------------------------------------------------------------------#
# Data Manipulation Class
class dataManipulate:
    def __init__(self, aggregateRecords=0, inputData=[]):
        self.aggregaterecords = aggregateRecords
        self.inputdata = inputData
    def __del__(self):
        print("dataManipulate Object Deleted.")
    def genFeatures(self):
        self.outputdata = pd.DataFrame(columns = self.inputdata.columns.tolist()*self.aggregaterecords)
        for i in range(0,int(len(self.inputdata)/self.aggregaterecords),1):
            self.outputdata.loc[self.inputdata.index[i*self.aggregaterecords]] = self.inputdata[i*self.aggregaterecords:i*self.aggregaterecords+self.aggregaterecords][:].values.flatten()
#-----------------------------------------------------------------------------#
# Excel Dataframe Class
class xlDataFrame:
    def __init__(self, xlParam):
        self.xlparams = xlParam
        self.xvar = ""
        self.yvar = ""
        self.pfilename = ""
        self.ptitle = ""
        self.pallette = ['#d32f2f','#ff6090','#df78ef','#7e57c2','#3f51b5','#1e88e5','#4fc3f7','#88ffff','#26a69a','#4caf50','#9ccc65','#dce775','#fff176','#ffd54f','#ffb74d','#ff8a65','#a1887f','#e0e0e0','#90a4ae']
        self.importvars()
    def __del__(self):
        print("xlDataFrame Object Deleted.")
    def printInstance(self):
        temp=[self.textmode,self.syncmode,self.indepvar,self.depvar,[self.forecast,self.syncronise],self.statistics]
        print(str(dt.datetime.now()) + "\n   xlDataFrame Instance : \n   " + str(temp))
    def importvars(self):
        print(str(dt.datetime.now()) + "\n   Importing Independent Variable..")
        for i in range(0,len(self.xlparams.indepvar),1):
            self.xlparams.indepvar[i].getIndColumn()
            if self.xlparams.indepvar[i].filetype == "excel":
                excel_workbook = pd.ExcelFile(self.xlparams.indepvar[i].filename)
                temp = excel_workbook.parse(self.xlparams.indepvar[i].sheetname, self.xlparams.indepvar[i].headerrow - 1, index_col=self.xlparams.indepvar[i].indexcol)
            else:
                temp = pd.read_csv(filepath_or_buffer  = self.xlparams.indepvar[i].filename, delimiter = self.xlparams.indepvar[i].filedel, header = self.xlparams.indepvar[i].headerrow - 1, index_col = self.xlparams.indepvar[i].indexcol)
                print(temp.columns.tolist())
            temp = dropColumns(temp, self.xlparams.indepvar[i].datalist)
            if i==0:
                self.xvar = temp
            else:
                self.xvar = pd.concat([self.xvar, temp], axis=1)
        print(str(dt.datetime.now()) + "\n   Importing Dependent Variable..")
        for i in range(0,len(self.xlparams.depvar),1):
            self.xlparams.depvar[i].getIndColumn()
            if self.xlparams.depvar[i].filetype == "excel":
                excel_workbook = pd.ExcelFile(self.xlparams.depvar[i].filename)
                temp = excel_workbook.parse(self.xlparams.depvar[i].sheetname, self.xlparams.depvar[i].headerrow - 1, index_col=self.xlparams.depvar[i].indexcol)
            else:
                temp = pd.read_csv(filepath_or_buffer  = self.xlparams.depvar[i].filename, delimiter = self.xlparams.depvar[i].filedel, header = self.xlparams.depvar[i].headerrow - 1, index_col = self.xlparams.depvar[i].indexcol)
            temp = dropColumns(temp, self.xlparams.depvar[i].datalist)
            if i==0:
                self.yvar = temp
            else:
                self.yvar = pd.concat([self.yvar, temp], axis=1)
            self.sortindex()
        print(str(dt.datetime.now()) + "\n   Importing Completed..")
    def sortindex(self):
        self.xvar = self.xvar.sort_index(axis=0, ascending=True)
        self.yvar = self.yvar.sort_index(axis=0, ascending=True)
    def genHTMLPlt(self, dataframe , plotmode=[""]):
#        dataframe = dropColumns(dataframe, varstoplot)
        print(str(dataframe.columns))
        print(str(dt.datetime.now()) + "\n   Plotting HTML")

        import requests
        r = requests.get("https://drive.google.com/uc?id=1KtdSkNXQiMglikyR6RIeKL1VSf_LrqZ7&export=download", allow_redirects=True)
        open(self.pfilename, 'wb').write(r.content)        
        file = open(self.pfilename, "a")
        temp = "\n\t\t\t\tPlotly.plot(gd, {\n\t\t\t\t\tdata: ["
        file.write(temp)
        cols = dataframe.columns.tolist()
        xx = dataframe.index.astype(str).tolist()
        counter = 0
        temp = '{"opacity" : 0.8, "name": "' + cols[0] + '", "y": ' + str(dataframe[cols[0]].tolist()) + ', "x": ' + str(xx) + ', "line": {"color": "' + self.pallette[counter] + '"}, "type": "scatter"}'
        file.write(temp)
        for i in range(1,len(cols),1):
            if counter + 1 == len(self.pallette):
                counter = 0
            else:
                counter += 1
            temp = ',{"opacity" : 0.8, "name": "' + cols[i] + '", "y": ' + str(dataframe[cols[i]].tolist()) + ', "x": ' + str(xx) + ', "line": {"color": "' + self.pallette[counter] + '"}, "type": "scatter"}'
            file.write(temp)
        temp = '],\n\t\t\t\t\tlayout: {"xaxis": {"rangeselector": {"buttons": [{"step": "all"}]}, "type": "date", "rangeslider": {}}, "title": "' + self.ptitle + '"}, frames: []});  }());\n\t\t</script>\n\t</body>\n</html>'
        file.write(temp)
        file.close()
        print(str(dt.datetime.now()) + "\n   Plot Completed")
#-----------------------------------------------------------------------------#
# Import Parameter Class
class xlImportParameter:
    'Class for storing Excel Import Parameters and Statistics of Imported Data'
    instance_Count = 0
    def __init__(self, textMode = True, syncMode = True, indepVars = "List of xlWorksheet Objects", depVars = "List of xlWorksheet Objects", forecastInterval = pd.Timestamp('00:00:00') - pd.Timestamp('00:00:00'), syncInterval = pd.Timestamp('00:00:00') - pd.Timestamp('00:00:00'), statParams = []):
        self.textmode = textMode
        self.syncmode = syncMode
        self.indepvar = indepVars
        self.depvar = depVars
        self.forecast = forecastInterval
        self.syncronise = syncInterval
        self.statistics = statParams
        xlImportParameter.instance_Count += 1
    def __del__(self):
        print("xlImportParameter Object Deleted.")
    def printInstance(self):
        temp=[self.textmode,self.syncmode,self.indepvar,self.depvar,[self.forecast,self.syncronise],self.statistics]
        print("xlImportParameter Instance : \n" + str(temp))
#-----------------------------------------------------------------------------#
# Worksheet Class
class xlWorkSheet:
    'Class for storing Excel Sheet Names and Variables'
    def __init__(self, fileType="excel", fileDel = "," , fileName = "", sheetName = "", timeSeries = True, dataFrequency = 0, headerRow = 0, timeStamp = 0, dataList = []):
        self.filetype = fileType
        self.filedel = fileDel
        self.filename = fileName
        self.sheetname = sheetName
        self.frequency = dataFrequency
        self.headerrow = headerRow
        self.timestamp = timeStamp
        self.datalist = dataList
        self.timeseries =timeSeries
        self.indexcol = None
    def __del__(self):
        print("xlWorkSheet Object Deleted.")
    def printInstance(self):
        temp=[self.filename,self.sheetname,self.frequency,self.headerrow,self.timestamp,self.datalist]
        print("xlWorkSheet Instance : \n" + str(temp))
    def printHeaders(self):
        if self.filetype == "excel":
            excel_workbook = pd.ExcelFile(self.filename)
            temp = str(excel_workbook.parse(self.sheetname, self.headerrow - 1).columns.tolist())
        else:
            temp = str(pd.read_csv(filepath_or_buffer = self.filename, delimiter = self.filedel, header = self.headerrow - 1).columns.tolist())
        print(temp)
    def getIndColumn(self):
        if self.timeseries:
            if self.filetype == "excel":
                excel_workbook = pd.ExcelFile(self.filename)
                temp=excel_workbook.parse(self.sheetname, self.headerrow - 1).columns.tolist()
            else:
                temp = pd.read_csv(filepath_or_buffer = self.filename, delimiter = self.filedel, header = self.headerrow - 1).columns.tolist()
            self.indexcol = temp.index(self.timestamp)
#=============================================================================#

