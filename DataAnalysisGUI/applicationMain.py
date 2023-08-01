import bagpy
from bagpy import bagreader
import pandas as pd
import seaborn as sea
import matplotlib.pyplot as plt
import numpy as np
import csv
from tabulate import tabulate
import tkinter as tk
from tkinter import filedialog,messagebox,simpledialog,ttk
import os.path
import copy

root=tk.Tk()

import graphGen

import displayFrames

import displayFramesCN

root.displayPkg=displayFrames

#root wide variables
root.bagpath=('Rosbag path not selected')
root.title('Rosbag visual parser')

root.frameDict={}

root.topicList=[]
root.topicCount=0
selectedTopic=tk.StringVar()
root.currTopicIndex=-1
root.filteredTopicList=[]
root.filteredTopicCount=0
topicFilter=tk.StringVar()

root.topicRadioButtons=[]
root.topicPageNum=0
root.topicsPerPage=15
root.atTopicPageLimit=False
root.topicTable=[]
root.topicInfoLabelList=[]



root.CSVpath=""

root.headerList=[]
currSelected=tk.StringVar() 

root.focusHeaderIndices=[]
root.focusHeaderList=[]
root.dataList=[]

root.lineCount=0

root.xAxisSelection=tk.IntVar()
root.XdataIndex=0
root.YdataIndices=[]

root.headerRadioButtons=[]

root.graphType= tk.StringVar()

#global frame that surrounds other frames
globalFrame=tk.LabelFrame(root,padx=10,pady=10)
globalFrame.grid(row=0,column=0)


root.frameDict.update({"globalFrame":globalFrame})

root.savedPlots=[]

root.buttonGrid=[["",""],["",""]]
root.plotGrid=[[""]]
root.plotGridHeight=1
root.plotGridWidth=1

root.removedButtons=[]
root.buttonGridSelect=[]

root.shareY=False
root.shareX=False

root.lang='EN'


#A class for saved plots that stores information to be used when creating multi plots
class plot:
    def __init__(self,name,xData,yData,graphType,xDataLabel,yDataLabels):
        self.name=name
        self.xData=xData
        self.yData=yData
        self.graphType=graphType
        self.xDataLabel=xDataLabel
        self.yDataLabels=yDataLabels

        self.isTwin=False
        self.twinXdata=[]
        self.twinYdata=[]

    def combine(self,baseName,twinName,newXdata,newYdata,xDataLabel,yDataLabels):
        #Function to store all of the twin data when called
        self.isTwin=True
        self.baseName=baseName
        self.twinName=twinName
        self.twinXdata=newXdata
        self.twinYdata=newYdata
        self.twinXlabel=xDataLabel
        self.twinYlabels=yDataLabels

#update topic info when another topic is selected
def updateSelectedTopic():
    buttonIndex=int(selectedTopic.get())
    index=buttonIndex+root.topicPageNum*root.topicsPerPage
    currTopic=root.filteredTopicList[index]
    root.currTopicIndex=root.topicList.index(currTopic)
    

    root.displayPkg.displayTopicInfo(root,root.frameDict['topicHighlight'])


def filterTopic():
    keyword=topicFilter.get()
    #print(keyword)
    root.filteredTopicList=[]

    #Loop through all of the topics in the bag files, if they contain the keyword,
    #Add to the listbox and an additional helper list
    for topic in root.topicList:
        if keyword in topic:
            root.filteredTopicList.append(topic)
        else:
            pass

    root.filteredTopicCount=len(root.filteredTopicList)
    root.topicPageNum=0
    root.currTopicIndex=-1
    root.displayPkg.displayTopicInfo(root,root.frameDict['topicHighlight'])
    clearTopicSelect()
    displayTopics()
    

#display the list of topics to choose from and update it
def displayTopics():

    root.topicRadioButtons.clear()

    #If the current page is the last, then set limit = true
    if (root.filteredTopicCount//root.topicsPerPage)==root.topicPageNum:
        root.atTopicPageLimit=True
    else:
        root.atTopicPageLimit=False

    #Entry box for filtering topics
    root.displayPkg.displayTopics(root,root.frameDict['topicFrame'],filterTopic,updateSelectedTopic,forwardTopicPage,backTopicPage,selectedTopic,topicFilter)
    
    
    
    #Display rows of radio buttons with text corresponding to that topic 
    if not root.atTopicPageLimit:
        for topicPageIndex in range(root.topicsPerPage):
            #Label with text of corresponding topic

            buttonText=root.filteredTopicList[root.topicPageNum*root.topicsPerPage+topicPageIndex]
            
            radiobutton=tk.Radiobutton(root.frameDict['topicFrame'],text= buttonText, variable=selectedTopic,value=topicPageIndex,command=updateSelectedTopic)
            root.topicRadioButtons.append(radiobutton)
            radiobutton.grid(row=topicPageIndex,column=0,sticky='w')
    else:
        #If it is the last page, autofill the unfilled rows with whitespace
        for topicPageIndex in range(root.topicsPerPage):
            if topicPageIndex<root.filteredTopicCount%root.topicsPerPage:
                
                buttonText=root.filteredTopicList[root.topicPageNum*root.topicsPerPage+topicPageIndex]
                radiobutton=tk.Radiobutton(root.frameDict['topicFrame'],text= buttonText, variable=selectedTopic,value=topicPageIndex,command=updateSelectedTopic)
                root.topicRadioButtons.append(radiobutton)
                radiobutton.grid(row=topicPageIndex,column=0,sticky='w')
                
            else:
                tk.Label(root.frameDict['topicFrame'],text="        ").grid(row=topicPageIndex,column=1,sticky='')
        
    #Buttons to go forward and back pages
    if root.atTopicPageLimit:
        #Forward button disabled if at page limit
        forwardTopic=tk.Button(root.frameDict['topicFrame'],text=">>",anchor='e',command=forwardTopicPage,state=tk.DISABLED)
        forwardTopic.grid(row=999,column=1,sticky=tk.S)
    else:
        forwardTopic=tk.Button(root.frameDict['topicFrame'],text=">>",anchor='e',command=forwardTopicPage)
        forwardTopic.grid(row=999,column=1,sticky=tk.S)

    if root.topicPageNum==0:
        #Backward button disabled if at page 0
        backTopic=tk.Button(root.frameDict['topicFrame'],text='<<',anchor='w',command=backTopicPage,state=tk.DISABLED)
        backTopic.grid(row=999,column=0,sticky=tk.S)
    else:
        backTopic=tk.Button(root.frameDict['topicFrame'],text='<<',anchor='w',command=backTopicPage)
        backTopic.grid(row=999,column=0,sticky=tk.S)
    


#Clear topic radio button selection
def clearTopicSelect():
    for radiobutton in root.topicRadioButtons:
        radiobutton.deselect()
        radiobutton.grid_forget()
        radiobutton.destroy()

    root.topicRadioButtons.clear()

#Helper function to make csv path
def getCSVpath(topicName,bagPath):
    topicNameNew=topicName.replace('/','-')
    bagPath=bagPath[0:-4]
    csvPath=bagPath+'/'+topicNameNew+'.csv'
    return csvPath

#Writes CSV file from contents of selected topic
def writeCSV():

    if root.currTopicIndex==-1:
        root.displayPkg.chooseTopicPopup(root)
        return

    topicName=root.topicList[root.currTopicIndex]
    
    csvfiles = []
    CSVpath=getCSVpath(topicName[1:],root.bagpath)
    root.CSVpath=CSVpath
    if os.path.isfile(CSVpath):
        #Translate
        overwriteResponse=root.displayPkg.overWriteCSVfile(CSVpath)
        #print(overwriteResponse)
        if overwriteResponse:
            data=b.message_by_topic(topicName)
        else:
            pass
    else:
        data=b.message_by_topic(topicName)

    #Split the CSV path onto multiple lines to avoid extending the frame    
    newCSVpath=root.CSVpath
    CSVlineLength=40
    for i in range(len(newCSVpath)//CSVlineLength):
        newCSVpath=newCSVpath[:(i+1)*CSVlineLength]+"\n"+newCSVpath[(i+1)*CSVlineLength:]

    root.CSVpathLabel2.destroy()
    root.CSVpathLabel2=tk.Label(root.frameDict['createCSVframe'],text=newCSVpath)
    root.CSVpathLabel2.grid(row=1,column=1,columnspan=2,sticky='w')

    root.displayPkg.readCSVbutton(root,root.frameDict['createHeaderFrame'],readCSV)
    


#Reads CSV to give a list of headers
def readCSV():
    with open(root.CSVpath, mode = 'r') as csv_file:
        root.headerList=[]
        csv_reader=csv.DictReader(csv_file)
        
        root.headersListbox.delete(0,tk.END)
        #Scan the first row to get the name of each header
        for row in csv_reader:
            for header in row:
                root.headerList.append(header)
                
            break
        #Add each header to the listbox selection
        for index in range(len(root.headerList)):
            header=root.headerList[index]
            root.headersListbox.insert(index,header)
        
        
        root.displayPkg.confirmHeaderButton(root,root.frameDict['createHeaderFrame'],confirmHeaders)
        

def findCSV():
    #Translate
    #Create prompt window to browse for CSV file
    if not root.bagpath==('Rosbag path not selected'):
        bagFolder=root.bagpath[0:-4]
    else:
        bagFolder="~/"

    #Translate
    root.CSVpath=root.displayPkg.findCSVbrowser(bagFolder)
    
    
    newCSVpath=root.CSVpath
    #Breaking up the filepath name to multiple lines if it is too long
    CSVlineLength=40
    for i in range(len(newCSVpath)//CSVlineLength):
        newCSVpath=newCSVpath[:(i+1)*CSVlineLength]+"\n"+newCSVpath[(i+1)*CSVlineLength:]

    
    root.CSVpathLabel2.destroy()
    root.CSVpathLabel2=tk.Label(root.frameDict['createCSVframe'],text=newCSVpath)
    root.CSVpathLabel2.grid(row=1,column=1,columnspan=2,sticky='w')

    
    root.displayPkg.readCSVbutton(root,root.frameDict['createHeaderFrame'],readCSV)
    



#Constructs the 2d Datalist where each column is the data stream of a selected header
def constructDataList():
    root.lineCount=0
    lineCount=0
    normalizedCols=[]
    normalizedColStarts=[]
    normalizeStart=0
    with open(root.CSVpath,mode='r') as csv_file:
        csv_reader=csv.DictReader(csv_file)
        for row in csv_reader:
            #Pass over the first row to let user select any cols they want to normalize
            if lineCount==0:

                for column in range(len(root.focusHeaderList)):
                    
                    if 'time' in root.focusHeaderList[column].lower():
                        
                        
                        normalizeCol= root.displayPkg.normalizeTimePopup(root,column)
                        
                        if normalizeCol:
                            root.focusHeaderList[column]=root.focusHeaderList[column]
                            normalizeStart=row[root.focusHeaderList[column]]
                            normalizedCols.append(column)
                            normalizedColStarts.append(normalizeStart)
                            
            #Raster through the rest of the csv file, adding numbers to data list
            for column in range(len(root.focusHeaderList)):
                
                try:
                    if column in normalizedCols:
                        root.dataList[column].append(float(row[root.focusHeaderList[column]])-float(normalizedColStarts[column]))
                    else:
                        root.dataList[column].append(float(row[root.focusHeaderList[column]]))
                except:

                   
                    root.displayPkg.datalistConstructionError(root,column)
                    root.focusHeaderList=[]

            lineCount+=1

        #Change the name of the normalized cols for indication
        for column in range(len(root.focusHeaderList)):
            if column in normalizedCols:
                root.focusHeaderList[column]=root.focusHeaderList[column]+"(T+)"

        root.lineCount=lineCount
        root.displayPkg.linesProcessedLabel(root,root.frameDict['createHeaderFrame'],lineCount)
        

#Display the radio buttons to select an x-axis dataset and the datasets to plot against it
def displayHeaderSelect():
    root.displayPkg.displayHeaderSelect(root,root.frameDict['headerAnalyzeFrame'])


#after selecting headers on the listbox, write the DataList and display the choices for x and y axis selection
def confirmHeaders():
    root.dataList.clear()
    root.focusHeaderList=[]
    root.focusHeaderIndices=[]
    for selection in root.headersListbox.curselection():
        root.focusHeaderIndices.append(selection)
        root.focusHeaderList.append(root.headerList[selection])
        root.dataList.append([])


    constructDataList()
    displayHeaderSelect()

#adding a button that represents a subplot's position on the grid
def addPlot(pressedButton,newName):

    #j corresponds to col number
    #i corresponds to row number
    pressedButton.updateText(newName)
    
    width=len(root.buttonGrid[0])
    height=len(root.buttonGrid)
    
    #Expanding down if a button is added on the bottom row
    if pressedButton.i == height-1:
        
        newButtonRow=[]
        for j in range(width):
            plotButton=gridButton(root.frameDict['savedPlotsFrame'],'',height,j)
            newButtonRow.append(plotButton)
        root.buttonGrid.append(newButtonRow)
        root.plotGridHeight+=1
        root.plotGrid.append([""]*root.plotGridWidth)

    #updating width and height
    width=len(root.buttonGrid[0])
    height=len(root.buttonGrid)

    #Expanding right if a button is added on the rightmost col
    if pressedButton.j == width-1:
       
        for i in range(height):
            plotButton=gridButton(root.frameDict['savedPlotsFrame'],'',i,width)
            root.buttonGrid[i].append(plotButton)

        root.plotGridWidth+=1
        for row in range(root.plotGridHeight):
            root.plotGrid[row].append("")

    for newPlot in root.savedPlots:
        if newPlot.name==pressedButton.text:
            root.plotGrid[pressedButton.i][pressedButton.j]=newPlot
    displaySavedPlots()
    #print(root.plotGrid)

#remove a button from the button grid and remove the corresponding plot
def removePlot():
    
    #Remove all buttons in the button select list
    for row in root.buttonGrid:
        for button in row:
            if button in root.buttonGridSelect:
                button.updateText("")
                root.buttonGridSelect.remove(button)
                root.plotGrid[button.i][button.j]=""


    root.buttonGridSelect=[]

    #Add auto collapse to rows and cols later     
    
    #Auto collapse for rows
    rowNum=0
    for row in root.buttonGrid:
        deleteRow=True
        #If a row is all empty, remove it
        for button in row:
            if button.text=="":
                continue
            else:
                deleteRow=False
        if deleteRow:
            #except for the last row
            if rowNum<len(root.buttonGrid)-1:
                #set the text of the removed row to the one below it
                button.text=root.buttonGrid[button.i+1][button.j].text
          
                root.plotGridHeight-=1
                

                #For the rows under the removed row, move the text one row up 
                for nextRows in range(len(root.buttonGrid)-1):
                    if nextRows>=rowNum:
                        for nextButton in root.buttonGrid[nextRows]:
                            nextButton.text=root.buttonGrid[nextButton.i+1][nextButton.j].text
                            
                #for the last row, remove the buttons from the grid
                for removedButton in root.buttonGrid[len(root.buttonGrid)-1]:
                    if removedButton.i>root.plotGridHeight:
                        removedButton.destroyed=True
                        root.removedButtons.append(removedButton)
                root.buttonGrid.pop(-1)
                #Update the plot grid by popping the rowNum that was removed
                root.plotGrid.pop(rowNum)

                break
        rowNum+=1    

    colNum=0
    #Loop through columns to find empty ones to remove
    for colNum in range(len(root.buttonGrid[0])):
        deleteCol=True
        for row in root.buttonGrid:
            if colNum<len(row):
                currButton=row[colNum]
    
                if currButton.text=="":
                    continue
                else:
                    deleteCol=False
        #If an empty row is found
        if deleteCol:
            if colNum<len(root.buttonGrid[0])-1:
                root.plotGridWidth-=1
               
                #Move the text to the left
                for indexingRow in root.buttonGrid:
                
                    button=indexingRow[colNum]
                    button.text=indexingRow[colNum+1].text
                
                for nextCols in range(len(root.buttonGrid[0])-1):
                    if nextCols>=colNum:
                        for indexingRow in root.buttonGrid:
                            nextButton=indexingRow[nextCols]
                            
                            nextButton.text=root.buttonGrid[nextButton.i][nextButton.j+1].text
 
                #Remove the rightmost column of buttons
                for indexingRow in root.buttonGrid:
                    for button in indexingRow:
                        if button.j>root.plotGridWidth:
                            button.destroyed=True
                            root.removedButtons.append(button)
                            indexingRow.remove(button)

                #Update the plot grid to reflect the missing column
                for row in root.plotGrid:
                    row.pop(colNum)

    displaySavedPlots()


#Create a twin x plot on the selected buttons    
def combinePlots():
    if root.plotsListbox.curselection==():
        return
    #print('combining plots')
    plotIndex=root.plotsListbox.curselection()
    twinPlot=root.savedPlots[plotIndex[0]]
    twinPlotName=twinPlot.name
    for currButton in root.buttonGridSelect:
        currPlot=root.plotGrid[currButton.i][currButton.j]
        #Popup a warning when trying to twin plot a already twinned plot
        if currPlot.isTwin:
            root.displayPkg.twinGraphWarning(root,currPlot.name)
            
            continue
        
        #Warning when the two plots have different X axis labels
        if not currPlot.xDataLabel==twinPlot.xDataLabel:
            response=root.displayPkg.twinGraphXAxisWarning(root,currPlot,twinPlot)
            if response == 1:
                pass
            elif response == 0:
                continue

        combinedName=root.displayPkg.combinePlotsName(currPlot.name,twinPlot.name)
        combinedPlot=plot(combinedName,currPlot.xData,currPlot.yData,currPlot.graphType,currPlot.xDataLabel,currPlot.yDataLabels)
        combinedPlot.combine(currPlot.name,twinPlot.name,twinPlot.xData,twinPlot.yData,twinPlot.xDataLabel,twinPlot.yDataLabels)

        root.plotGrid[currButton.i][currButton.j]=combinedPlot
        #Name for the button in the button grid(not the plot name in the multi-plot)
        newButtonName=currPlot.name+"+"+twinPlotName
        currButton.updateText(newButtonName)
        root.buttonGridSelect.remove(currButton)


    displaySavedPlots()

#Main function that will identify the coordinate of the button pressed, then interpret what function needs to be called
def plotButtonMain(pressedButton):
    #print(f'i={pressedButton.i}')
    #print(f'j={pressedButton.j}')
    plotIndex=root.plotsListbox.curselection()
    
    #If the button text is an empty string, then add a new button with the currently selected plot to that grid spot, and expand the grid
    if pressedButton.text=='':
        if plotIndex==():
            pass
        else:
            currPlot=root.savedPlots[plotIndex[0]]
            plotName=currPlot.name
            addPlot(pressedButton,plotName)
    #If the button text is not empty, add that button to a list
    else:
        if pressedButton in root.buttonGridSelect:
            root.buttonGridSelect.remove(pressedButton)
            #pressedButton.toggleHighlight()
        else:
            root.buttonGridSelect.append(pressedButton)
            #pressedButton.toggleHighlight()

    displaySavedPlots()
    

    #If the button text isn't empty:
        #If the remove button is then pressed, remove that button and resize the grid
        #If the combine button is pressed, if the listbox has a selection, then create a twin graph with those two plots

    
    
#A wrapper object for the grid buttons that allow its coordinates to be passed into the command lambda function
class gridButton:
    def __init__(self,frame,text,i,j):
        self.frame=frame
        self.i=i
        self.j=j
        self.text=text
        self.bg='light grey'
        self.button=tk.Button(self.frame,text=self.text,width=10,bg=self.bg,command=lambda: plotButtonMain(self))
        self.destroyed=False
        

    def display(self):
        #Erase all the previous layers of buttons
        self.button.grid_forget()
        self.button.destroy()
        offset=6
        #If the button is not destroyed, create it and grid it
        if not self.destroyed:
            
            self.button=tk.Button(self.frame,text=self.text,width=10,bg=self.bg,command=lambda: plotButtonMain(self))
            self.button.grid(row=self.i+offset,column=self.j,sticky='w')

    #change text of button to new text
    def updateText(self,newText):
        self.text=newText

    def create(self):
        self.button=tk.Button(self.frame,text=self.text,width=10,bg=self.bg,command=lambda: plotButtonMain(self))
        self.destroyed=False

    #toggle the color of the button to signal if it is selected or not
    def toggleHighlight(self):
        if self.bg=='light grey':
            self.bg='grey'
        elif self.bg=='grey':
            self.bg='light grey'

def shareXtoggle():
    root.shareX= not root.shareX
    displaySavedPlots()

def shareYtoggle():
    root.shareY= not root.shareY
    displaySavedPlots()


#Function to update the saved plots window
def displaySavedPlots():

    
    #root.displayPkg.displaySavedPlots(root,root.frameDict['savedPlotsFrame'],removePlot,combinePlots,shareXtoggle,shareYtoggle,generateMultiPlot)

    root.plotsListbox=tk.Listbox(root.frameDict['savedPlotsFrame'])
    root.plotsListbox.grid(row=1,column=0,columnspan=3,rowspan=5,sticky='w')
    index=0
    #Creating the listbox with all of the saved plots
    for currPlot in root.savedPlots:
        root.plotsListbox.insert(index,currPlot.name)
        index +=1
    root.plotsListbox.grid(row=1,column=0)

    root.displayPkg.displaySavedPlots(root,root.frameDict['savedPlotsFrame'],removePlot,combinePlots,shareXtoggle,shareYtoggle,generateMultiPlot)
    root.displayPkg.displayPlotbuttonGrid(root,root.frameDict['savedPlotsFrame'])


#Create a matplotlib window with multiple subplots
def generateMultiPlot():
    graphGen.generateMultiPlot(root)
    
    

#Generate the matplotlib graph
def generateGraph():
    graphGen.generateGraph(root)

#Save the current plot to be used in a multi-plot
def savePlot():
    #Each plot has a list of x axis data, a 2d list of all the data to be plotted, and the graph type
    root.XdataIndex=root.xAxisSelection.get()
    root.YdataIndices=root.yAxisListbox.curselection()
    xData=root.dataList[root.XdataIndex]
    yData=[]
    xDataLabel=f'{root.focusHeaderList[root.XdataIndex]}'
    yDataLabels=[]
    for i in root.YdataIndices:
        yData.append(root.dataList[i])
        yDataLabels.append(f'{root.focusHeaderList[i]}')

    #def __init__(self,name,xData,yData,graphType):
    #dialog box to prompt the user to create a name for that plot

    
    plotName=root.displayPkg.savePlotWindow(root)
    
    #Creating the object
    savedPlot=plot(plotName,xData,yData,root.graphType.get(),xDataLabel,yDataLabels)
    #List of all the saved plot objects
    root.savedPlots.append(savedPlot)

    displaySavedPlots()


#Functions to scroll back and forward through the page of topics
def forwardTopicPage():
    root.topicPageNum +=1
    clearTopicSelect()
    displayTopics()

def backTopicPage():
    root.topicPageNum -=1
    clearTopicSelect()
    displayTopics()


#--------------------------------------------------------------Filepath Frame for selecting the filepath of the bag files--------------------
filepathFrame=tk.LabelFrame(globalFrame, text='Search for Rosbag path',padx=10,pady=10)
filepathFrame.grid(row=0,column=0,sticky='w')

root.frameDict.update({"filepathFrame":filepathFrame})

#Function to display a window to choose a file path
#Translate
def displayFilepath():
    root.displayPkg.displayFilepath(root,root.frameDict['filepathFrame'],setFilepath)


#Confirming filepath
def setFilepath():
    global b
    b=bagreader(root.bagpath)
    root.topicList=list(b.topic_table.Topics)
    
    root.topicTable=b.topic_table

    root.filteredTopicList=copy.deepcopy(root.topicList)

    root.topicCount=len(root.topicList)

    root.filteredTopicCount=len(root.filteredTopicList)

    clearTopicSelect()

    root.displayPkg.createCSVbutton(root,root.frameDict['createCSVframe'],writeCSV)
    
    displayTopics()
    

#--------------------------------------------------------------------------Find Bagpath frame

def createFindBagpathFrame():
    root.displayPkg.createFindBagpathFrame(root,root.frameDict['filepathFrame'],displayFilepath,setFilepath)

createFindBagpathFrame()

#---------------------------------------------------------------------------Topic selection frame
topicFrame=tk.LabelFrame(globalFrame,text='Select a topic to analyze',padx=10,pady=10)
topicFrame.grid(row=1,column=0,rowspan=4,sticky=tk.N+tk.S+tk.E+tk.W)

root.frameDict.update({"topicFrame":topicFrame})

def createTopicSelectFrame():
    
    root.displayPkg.createTopicSelectFrame(root,root.frameDict['topicFrame'],backTopicPage,forwardTopicPage)
createTopicSelectFrame()



#----------------------------------------------------------------------------------Topic Highlight Frame
topicHighlight=tk.LabelFrame(globalFrame,text='Info about the selected topic',padx=10,pady=10)
topicHighlight.grid(row=5,column=0,sticky=tk.W+tk.E)

root.frameDict.update({"topicHighlight":topicHighlight})

def createTopicHighlightFrame():
  
    root.displayPkg.createTopicHighlightFrame(root,root.frameDict['topicHighlight'])

createTopicHighlightFrame()

#----------------------------------------------------------------------------------CSV Write Frame
createCSVframe=tk.LabelFrame(globalFrame,text='Create or load a CSV file',padx=10,pady=10)
createCSVframe.grid(row=0,column=1,sticky=tk.S+tk.E+tk.W+tk.N)

root.frameDict.update({"createCSVframe":createCSVframe})

def createCSVwriteFrame():
    
    root.displayPkg.createCSVwriteFrame(root,root.frameDict['createCSVframe'],writeCSV,findCSV)

createCSVwriteFrame()

#---------------------------------------------------------------------------------Header Select Frame

createHeaderFrame=tk.LabelFrame(globalFrame,text='Select data streams to analyze',padx=10,pady=10)
createHeaderFrame.grid(row=1,column=1,rowspan=2,sticky='nw')

root.frameDict.update({"createHeaderFrame":createHeaderFrame})


root.headersListbox=tk.Listbox(root.frameDict['createHeaderFrame'],width=30,selectmode=tk.MULTIPLE)
#root.headersListbox=tk.Listbox(root.frameDict['createHeaderFrame'],width=30,selectmode=tk.MULTIPLE)
def createHeaderSelectFrame():
    root.displayPkg.createHeaderSelectFrame(root,root.frameDict['createHeaderFrame'],readCSV,confirmHeaders)
    
    root.headersListbox=tk.Listbox(root.frameDict['createHeaderFrame'],width=30,selectmode=tk.MULTIPLE)
    root.headersListbox.grid(row=2,column=0,sticky='w')
  

createHeaderSelectFrame()

#-------------------------------------------------------------------------------Header Analyze Frame
headerAnalyzeFrame=tk.LabelFrame(globalFrame,text='Plotting Config',padx=10,pady=10)
headerAnalyzeFrame.grid(row=3,column=1,rowspan=3,sticky='nw')

root.frameDict.update({"headerAnalyzeFrame":headerAnalyzeFrame})

def createHeaderAnalyzeFrame():
    root.displayPkg.createHeaderAnalyzeFrame(root,root.frameDict['headerAnalyzeFrame'],generateGraph,savePlot)

createHeaderAnalyzeFrame()

#----------------------------------------------------------------------------------Saved plots frame

savedPlotsFrame=tk.LabelFrame(globalFrame,text='Saved Plots',padx=10,pady=10)
savedPlotsFrame.grid(row=0,column=2,rowspan=2,sticky=tk.S+tk.E+tk.W+tk.N)

root.frameDict.update({"savedPlotsFrame":savedPlotsFrame})

def createSavedPlotsFrame():


    root.displayPkg.createSavedPlotsFrame(root,root.frameDict['savedPlotsFrame'],removePlot,combinePlots,generateMultiPlot,shareXtoggle,shareYtoggle)

    #iterate through the initial grid size and create button wrapper objects
    for i in range(root.plotGridHeight+1):
        for j in range(root.plotGridWidth+1):
            plotButton=gridButton(root.frameDict['savedPlotsFrame'],"",i,j)
            plotButton.display()

            #Button dict has is button object: coordinate tuple
            #Button grid is 2D list of plot button objects in their respective positions
            root.buttonGrid[i][j]=plotButton
    

 
createSavedPlotsFrame()

#----------------------------------------------------------------------------------Settings frame

settingsFrame=tk.LabelFrame(globalFrame,text='Window settings',padx=10,pady=10)
settingsFrame.grid(row=3,column=2,sticky='nw')

root.frameDict.update({"settingsFrame":settingsFrame})

#Function to redraw all of the frames- to be used for language toggle or data reset
def redrawAll():

    for frame in root.frameDict:
        if not frame == "globalFrame":
            
            frameObj=root.frameDict[frame]

            #Delete all of the widgets in current frames to redraw them
            for widget in frameObj.winfo_children():
                widget.grid_forget()
                widget.destroy()
            
    #Code in displayFrames that redraws widgets

    root.displayPkg.updateFrames(root,globalFrame)

    root.displayPkg.createFindBagpathFrame(root,root.frameDict['filepathFrame'],displayFilepath,setFilepath)

    root.displayPkg.createTopicSelectFrame(root,root.frameDict['topicFrame'],backTopicPage,forwardTopicPage)

    root.displayPkg.createTopicHighlightFrame(root,root.frameDict['topicHighlight'])

    displayTopics()

    root.displayPkg.displayTopicInfo(root,root.frameDict['topicHighlight'])

    root.displayPkg.createCSVwriteFrame(root,root.frameDict['createCSVframe'],writeCSV,findCSV)

    root.displayPkg.createHeaderSelectFrame(root,root.frameDict['createHeaderFrame'],readCSV,confirmHeaders)

    root.displayPkg.createHeaderAnalyzeFrame(root,root.frameDict['headerAnalyzeFrame'],generateGraph,savePlot)

    root.displayPkg.displayHeaderSelect(root,root.frameDict['headerAnalyzeFrame'])
    
    root.displayPkg.createSavedPlotsFrame(root,root.frameDict['savedPlotsFrame'],removePlot,combinePlots,generateMultiPlot,shareXtoggle,shareYtoggle)

    #Buttons were already destroyed, but recreate them with the new frame defined
    for row in root.buttonGrid:
        for button in row:
            button.frame=root.frameDict['savedPlotsFrame']
            button.create()
    
    root.displayPkg.displayPlotbuttonGrid(root,root.frameDict["savedPlotsFrame"])

    root.displayPkg.createSettingsFrame(root,root.frameDict["settingsFrame"],redrawAll,toggleLanguage)

def toggleLanguage():
    #Toggle between the 2 languages
    if root.lang=='EN':
        root.lang='CN'
    elif root.lang=='CN':
        root.lang='EN'

    #Change the package used based on the toggle
    if root.lang=='EN':
        root.displayPkg=displayFrames
        
    elif root.lang=='CN':
        root.displayPkg=displayFramesCN
    
    redrawAll()

def createSettingsFrame():
    root.displayPkg.createSettingsFrame(root,root.frameDict['settingsFrame'],redrawAll,toggleLanguage)

createSettingsFrame()

'''
def createScrollbar():
    scroll = ttk.Scrollbar(root.frameDict['globalFrame'])
    scroll.grid(row=0, column=3,rowspan=5, sticky=tk.E)

    scroll.config(command=root.frameDict['globalFrame'].yview)
    root.frameDict['globalFrame'].configure(yscrollcommand=scroll.set)

createScrollbar()
'''
#-----------------------------------------------------------------------------------MAIN LOOP--------------------------------------
root.mainloop()