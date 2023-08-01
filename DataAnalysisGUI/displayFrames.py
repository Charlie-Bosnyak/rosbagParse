import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from PIL import ImageTk, Image


def displayTopics(root,frame,filterTopic,updateSelectedTopic,forwardTopicPage,backTopicPage,selectedTopic,topicFilter):
    #Entry box for filtering topics
    #Translate

    pageIndicator=tk.Label(frame,text=f'Page {root.topicPageNum+1} of {root.filteredTopicCount//root.topicsPerPage+1}')
    pageIndicator.grid(row=1000,column=2)

    #Display rows of radio buttons with text corresponding to that topic
    if not root.filteredTopicList  == []:
        topicFilterLabel=tk.Label(frame,text="Enter a search term")
        topicFilterLabel.grid(row=0,column=1,columnspan=2,sticky='w')

        filterEntry=tk.Entry(frame,textvariable=topicFilter)
        filterEntry.grid(row=1,column=1,columnspan=2,sticky='w')


        topicFilterButton=tk.Button(frame,text='Filter',command=filterTopic)
        topicFilterButton.grid(row=2,column=1,columnspan=2,sticky='w')
      

def displayTopicInfo(root,frame):

    #Remove all previous topic info labels
    for label in root.topicInfoLabelList:
        label.grid_forget()

    root.topicInfoLabelList=[]

    #If a topic is selected, display the info about that topic(name, type, msg count, frequency)
    if not root.currTopicIndex == -1:
        topicNameLabel=tk.Label(frame,text=root.topicTable.T[root.currTopicIndex][0],padx=10,pady=10)
        topicNameLabel.grid(row=0,column=1,sticky='w')

        
        root.topicInfoLabelList.append(topicNameLabel)
        
        topicTypesLabel=tk.Label(frame,text=root.topicTable.T[root.currTopicIndex][1],padx=10,pady=10)
        topicTypesLabel.grid(row=1,column=1,sticky='w')

        root.topicInfoLabelList.append(topicTypesLabel)

        topicMsgCountLabel=tk.Label(frame,text=root.topicTable.T[root.currTopicIndex][2],padx=10,pady=10)
        topicMsgCountLabel.grid(row=2,column=1,sticky='w')

    
        root.topicInfoLabelList.append(topicMsgCountLabel)

        topicFreqLabel=tk.Label(frame,text=root.topicTable.T[root.currTopicIndex][3],padx=10,pady=10)
        topicFreqLabel.grid(row=3,column=1,sticky='w')

    
        root.topicInfoLabelList.append(topicFreqLabel)

#Opens a browser window to look for CSV files
def findCSVbrowser(bagFolder):
    return filedialog.askopenfilename(initialdir=bagFolder,title="select a CSV file",filetypes=(('csv files','*.csv'),('all files','*.*')))

#Creates the CSV file
def createCSVbutton(root,frame,writeCSV):
    createCSVbutton=tk.Button(frame,text='Create CSV File',padx=10,pady=5,command=writeCSV)
    createCSVbutton.grid(row=0,column=0,sticky='w')


def overWriteCSVfile(CSVpath):
    return messagebox.askyesno("Overwrite?",f"A file at \n {CSVpath} \n already exists.\n Do you want to overwrite?")

#Reads the data columns from the CSV file previously selected and puts them in a data table
def readCSVbutton(root,frame,readCSV):
    readCSVbutton=tk.Button(frame,text='Read CSV with above path',padx=10,pady=10,command=readCSV)
    readCSVbutton.grid(row=0,column=0,sticky='nw')

#Reads the data from the table into a 2D list
def confirmHeaderButton(root,frame,confirmHeaders):
    confirmHeadersButton=tk.Button(frame,text="Confirm selection",padx=10,pady=10,command=confirmHeaders)
    confirmHeadersButton.grid(row=3,column=0,sticky='w')

#Subtract all entries of a data column by its first entry. 
#Useful for data columns that correspond to time, so that time can be read as time since start of recording
def normalizeTimePopup(root,column):
    return messagebox.askyesno("Normalize time?",f"""Data stream {root.focusHeaderList[column]} has keyword 'time' \n
Subtract entries of {root.focusHeaderList[column]} by the first entry such that it represents
time since rosbag start?""")
def chooseTopicPopup(root):
    messagebox.showwarning("Choose a topic","Choose a topic in order to create a CSV file")


#If there are errors when float-ing values of a data column or cells of that column are blank
def datalistConstructionError(root,column):
    messagebox.showerror("Datalist construction error",f"""An error was encountered when writing the data stream's values into a numerical list \n
Check if there are non-numerical values in the data stream {root.focusHeaderList[column]}""")

#Displays the number of lines in the data lines that were written to the 2d list
def linesProcessedLabel(root,frame,lineCount):
    linesProcessedLabel=tk.Label(frame,text=f"Processed {lineCount} lines",padx=10,pady=10)
    linesProcessedLabel.grid(row=3,column=1,sticky='w')

def twinGraphWarning(root,name):
    messagebox.showwarning("Selected plot already twin",f"""The plot {name} already is a twin plot 
    \nSkipping the combining process for {name} to avoid errors
    """)

def twinGraphXAxisWarning(root,currPlot,twinPlot):
    
    response=messagebox.askokcancel("Differing X scales",f"""The plot {currPlot.name} uses X axis {currPlot.xDataLabel} while the plot {twinPlot.name} uses X axis {twinPlot.xDataLabel}
                                    \nUsing differing X axes may lead to scaling issues with the combined graph
                                    \nContinue with the combining process?
                                    """)
    return response

#Create the display name(for the displayed multi-plot) for the twinned plot
def combinePlotsName(name1,name2):
    combinedName=name1+ ' and '+name2
    return combinedName

#Pop up that lets the user enter a self-selected name for the saved plot
def savePlotWindow(root):
    plotName=simpledialog.askstring('Save plot',"Save plot as:")
    while True:
        if plotName=="":
            
            plotName=simpledialog.askstring('Save plot',"Plot name cannot be empty \n Save plot as:")
        else:
            break

    return plotName




def displayHeaderSelect(root,frame):
    root.yAxisListbox

    tk.Label(frame,text="                                                             ").grid(row=2,column=0,sticky="w")
    
    #Clear previous radio buttons
    

    root.headerRadioButtons.clear()

    #Create a radio button for each selected headder
    for index in range(len(root.focusHeaderList)):
        
        radiobutton=tk.Radiobutton(frame,text=root.focusHeaderList[index],variable=root.xAxisSelection,value=index)
        #List to track radio buttons to delete them later
        root.headerRadioButtons.append(radiobutton)
        radiobutton.grid(row=index+1,column=0,sticky='w')

    root.yAxisListbox.delete(0,len(root.focusHeaderList))
    #Create the entries for the listbox
    for index2 in range(len(root.focusHeaderList)):
        root.yAxisListbox.insert(index2,root.focusHeaderList[index2])

    setYaxesLabel=tk.Label(frame,text="Select the data stream(s) to plot")
    setYaxesLabel.grid(row=999,column=0,sticky='w')
    root.yAxisListbox.grid(row=1000,column=0,rowspan=2,sticky='w')

#Additional info about finding the bag file
def filepathHelp():
    messagebox.showinfo("Bag path additional info","""Clicking "Confirm" will create a data folder in the same folder as the .bag file
    \nThis is where CSV files generated later will be stored
    """)

#Additional info about creating or finding a CSV
def CSVhelp():
    messagebox.showinfo("CSV path additional info","""Either create a CSV from the selected topic or browse for an existing CSV file
    """)

#Additional info about configurating the multi-plot
def plotsHelp():
    global plotInfoImg
    plotInfo=tk.Toplevel()
    plotInfo.title('Multi-plot configuration guide')
    plotInfoImg= ImageTk.PhotoImage(Image.open("GUI_Images/PlotsHelpEN.png"))
    plotInfoLabel=tk.Label(plotInfo,image=plotInfoImg)
    plotInfoLabel.pack()
 


def displayFilepath(root,frame,setFilepath):
    root.bagpath=filedialog.askopenfilename(initialdir="~/",title="select a rosbag file",filetypes=(('rosbag files','*.bag'),('all files','*.*'))) 
    newBagpath=root.bagpath
    BagpathLineLength=50
    #Split the label into multiple lines
    for i in range(len(newBagpath)//BagpathLineLength):
        newBagpath=newBagpath[:(i+1)*BagpathLineLength]+"\n"+newBagpath[(i+1)*BagpathLineLength:]

    
    
    filenameLabel=tk.Label(frame,text=newBagpath)
    filenameLabel.grid(row=1,column=0,sticky='E')
    
    

    confirmFilepath=tk.Button(frame,text='Confirm',command=setFilepath)
    confirmFilepath.grid(row=0,column=1,sticky='NE')

    if root.bagpath[-4:]!='.bag' and root.bagpath  != 'Rosbag path not selected':
        messagebox.showwarning("File type caution","The file you have selected is not of type .bag \n This may cause errors when parsing")



def createFindBagpathFrame(root,frame,displayFilepath,setFilepath):
    #Button to pop up path selection window
    openFilepath=tk.Button(frame,text='Select',command=displayFilepath)
    openFilepath.grid(row=0,column=0,sticky='NW')

    #Button to confirm bag path
    if root.bagpath  == 'Rosbag path not selected':
        confirmFilepath=tk.Button(frame,text='Confirm',command=setFilepath,state=tk.DISABLED)
        confirmFilepath.grid(row=0,column=1,sticky='NE')
    else:
        confirmFilepath=tk.Button(frame,text='Confirm',command=setFilepath)
        confirmFilepath.grid(row=0,column=1,sticky='NE')

    #Label to display currently selected path

    newBagpath=root.bagpath
    BagpathLineLength=50
    #Split the label into multiple lines
    for i in range(len(newBagpath)//BagpathLineLength):
        newBagpath=newBagpath[:(i+1)*BagpathLineLength]+"\n"+newBagpath[(i+1)*BagpathLineLength:]

    
    
    filenameLabel=tk.Label(frame,text=newBagpath)
    filenameLabel.grid(row=1,column=0,sticky='E')

    #Button for extra info
    filepathInfo=tk.Button(frame,text="?",command=filepathHelp)
    filepathInfo.grid(row=1,column=1)

def createTopicSelectFrame(root,frame,backTopicPage,forwardTopicPage):
    

    #Vertical padding with whitespace
    for topicPageIndex in range(root.topicsPerPage):
                tk.Label(frame,text="                                                                                         ",anchor='w').grid(row=topicPageIndex,column=0,sticky='w')

    #Back and forward buttons, greyed out at start
    backTopic=tk.Button(frame,text='<<',anchor='w',command=backTopicPage,state=tk.DISABLED)
    backTopic.grid(row=999,column=0,sticky=tk.S)

    forwardTopic=tk.Button(frame,text=">>",anchor='e',command=forwardTopicPage,state=tk.DISABLED)
    forwardTopic.grid(row=999,column=1,sticky=tk.S)

    pageIndicator=tk.Label(frame,text=f'Page {root.topicPageNum+1} of {root.filteredTopicCount//root.topicsPerPage+1}')
    pageIndicator.grid(row=1000,column=2,sticky=tk.S)

def createTopicHighlightFrame(root,frame):
    
    root.topicInfoLabelList=[]

    #Different headers and labels
    topicNameHeader=tk.Label(frame,text="Topic Name:",padx=10,pady=10)
    topicNameHeader.grid(row=0,column=0,sticky='w')

    topicNameLabel=tk.Label(frame,text=" ",padx=10,pady=10)
    topicNameLabel.grid(row=0,column=1,sticky='w')

    topicTypesHeader=tk.Label(frame,text="Topic messages type:",padx=10,pady=10)
    topicTypesHeader.grid(row=1,column=0,sticky='w')

    topicTypesLabel=tk.Label(frame,text=" ",padx=10,pady=10)
    topicTypesLabel.grid(row=1,column=1,sticky='w')

    topicMsgCountHeader=tk.Label(frame,text="Message count:",padx=10,pady=10)
    topicMsgCountHeader.grid(row=2,column=0,sticky='w')

    topicMsgCountLabel=tk.Label(frame,text=" ",padx=10,pady=10)
    topicMsgCountLabel.grid(row=2,column=1,sticky='w')

    topicFreqHeader=tk.Label(frame,text="Frequency:",padx=10,pady=10)
    topicFreqHeader.grid(row=3,column=0,sticky='w')

    topicFreqLabel=tk.Label(frame,text=" ",padx=10,pady=10)
    topicFreqLabel.grid(row=3,column=1,sticky='w')

def createCSVwriteFrame(root,frame,writeCSV,findCSV):
    
    #Button to write CSV from selected topic, disabled if no topic is selected
    if root.filteredTopicCount<1:
        createCSVbutton=tk.Button(frame,text='Create CSV File',padx=10,pady=5,command=writeCSV,state=tk.DISABLED)
        createCSVbutton.grid(row=0,column=0,sticky='w')
    else:
        createCSVbutton=tk.Button(frame,text='Create CSV File',padx=10,pady=5,command=writeCSV)
        createCSVbutton.grid(row=0,column=0,sticky='w')

    findCSVbutton=tk.Button(frame,text='Browse for CSV',padx=10,pady=5,command=findCSV)
    findCSVbutton.grid(row=0,column=1)

    helpButtonCSV=tk.Button(frame,text="?",padx=10,pady=5,command=CSVhelp)
    helpButtonCSV.grid(row=0,column=2,sticky='e')

    CSVpathLabel1=tk.Label(frame,text=f'Path:',padx=10,pady=5)
    CSVpathLabel1.grid(row=1,column=0,sticky='w')

    #Create the label that displays the current CSV path
    newCSVpath=root.CSVpath
    CSVlineLength=40
    #Split the label into multiple lines
    for i in range(len(newCSVpath)//CSVlineLength):
        newCSVpath=newCSVpath[:(i+1)*CSVlineLength]+"\n"+newCSVpath[(i+1)*CSVlineLength:]

    #If the current CSV path is empty, then display a message
    if root.CSVpath=="":

        root.CSVpathLabel2=tk.Label(frame,text="CSV file currently not created")
        root.CSVpathLabel2.grid(row=1,column=1,columnspan=2)

    else:
        newCSVpath=root.CSVpath
        CSVlineLength=40
        for i in range(len(newCSVpath)//CSVlineLength):
            newCSVpath=newCSVpath[:(i+1)*CSVlineLength]+"\n"+newCSVpath[(i+1)*CSVlineLength:]
        root.CSVpathLabel2=tk.Label(frame,text=newCSVpath)
        root.CSVpathLabel2.grid(row=1,column=1,columnspan=2,sticky='w')

def createHeaderSelectFrame(root,frame,readCSV,confirmHeaders):

    root.headersListbox=tk.Listbox(frame,width=30,selectmode=tk.MULTIPLE)
    root.headersListbox.grid(row=2,column=0,sticky='w')

    for index in range(len(root.headerList)):
            header=root.headerList[index]
            root.headersListbox.insert(index,header)

    if root.CSVpath=="":
    
        readCSVbutton=tk.Button(frame,text='Read CSV with above path',padx=10,pady=10,command=readCSV,state=tk.DISABLED)
        readCSVbutton.grid(row=0,column=0,sticky='nw')
    else:
        readCSVbutton=tk.Button(frame,text='Read CSV with above path',padx=10,pady=10,command=readCSV)
        readCSVbutton.grid(row=0,column=0,sticky='nw')

    selectHeadersPrompt=tk.Label(frame,text='Select the datastreams to focus on from the options below',padx=10,pady=10)
    selectHeadersPrompt.grid(row=1,column=0,columnspan=2,sticky='w')
    
    #If the selection has been made, enable the buttons that allow confirmation
    if root.headersListbox.size()>0:
        confirmHeadersButton=tk.Button(frame,text="Confirm selection",padx=10,pady=10,command=confirmHeaders)
        confirmHeadersButton.grid(row=3,column=0,sticky='w')
    else:

        confirmHeadersButton=tk.Button(frame,text="Confirm selection",padx=10,pady=10,command=confirmHeaders,state=tk.DISABLED)
        confirmHeadersButton.grid(row=3,column=0,sticky='w')

    

    linesProcessedLabel=tk.Label(frame,text=f"Processed {root.lineCount} lines",padx=10,pady=10)
    linesProcessedLabel.grid(row=3,column=1,sticky='w')

    

def createHeaderAnalyzeFrame(root,frame,generateGraph,savePlot):
    setXaxisLabel=tk.Label(frame,text="Select the data stream to be the X axis")
    setXaxisLabel.grid(row=0,column=0,sticky='w')

    
    
    #Listbox for all of the headers that can be plotted
    root.yAxisListbox=tk.Listbox(frame,width=30,selectmode=tk.MULTIPLE)

    root.yAxisListbox.grid(row=1000,column=0,rowspan=2,sticky='w')

    setYaxesLabel=tk.Label(frame,text="Select the data stream(s) to plot")
    setYaxesLabel.grid(row=2,column=0,sticky='w')

    root.graphType.set("Line")
    typeOptions=["Line","Scatter","Bar"]

    
    graphTypeLabel=tk.Label(frame,text="Select a graph type",padx=10,pady=5)
    graphTypeLabel.grid(row=0,column=1,sticky='sw')

    graphTypeDrop=tk.OptionMenu(frame,root.graphType,*typeOptions)
    graphTypeDrop.grid(row=1,column=1)

    generateGraphButton=tk.Button(frame,text="Generate \n Single Graph",command=generateGraph,relief=tk.RAISED)
    generateGraphButton.grid(row=1000,column=1)

    savePlotButton=tk.Button(frame,text='Save Plot',command=savePlot,relief=tk.RAISED)
    savePlotButton.grid(row=1001,column=1)

def createSavedPlotsFrame(root,frame,removePlot,combinePlots,generateMultiPlot,shareXtoggle,shareYtoggle):

    root.plotsListbox=tk.Listbox(frame)
    root.plotsListbox.grid(row=1,column=0,columnspan=3,rowspan=5,sticky='w')

    #Index is a temporary value to determine what the listbox will output when that option is selected
    index=0
    #Creating the listbox with all of the saved plots
    for currPlot in root.savedPlots:
        root.plotsListbox.insert(index,currPlot.name)
        index +=1


    plotsLabel=tk.Label(frame,text='Choose plots to display')
    plotsLabel.grid(row=0,column=0,columnspan=3,sticky='w')

    #Open the remove and combine buttons if plot buttons have been selected
    if len(root.buttonGridSelect)>0:

        removePlotButton=tk.Button(frame,text='Remove selected plot',command=removePlot)
        removePlotButton.grid(row=1,column=4)

        combinePlotsButton=tk.Button(frame,text='Combine selected plots',command=combinePlots)
        combinePlotsButton.grid(row=2,column=4)
    else:

        removePlotButton=tk.Button(frame,text='Remove selected plot',command=removePlot,state=tk.DISABLED)
        removePlotButton.grid(row=1,column=4)

        combinePlotsButton=tk.Button(frame,text='Combine selected plots',command=combinePlots,state=tk.DISABLED)
        combinePlotsButton.grid(row=2,column=4)

    #If plots have been saved, enable the share x and share y toggles
    
    if root.plotsListbox.size()>0:

        if root.shareX:
            shareXbutton=tk.Button(frame,text='▣ Share X axis scale',command=shareXtoggle)
            shareXbutton.grid(row=3,column=4)
        else:
            shareXbutton=tk.Button(frame,text='▢ Share X axis scale',command=shareXtoggle)
            shareXbutton.grid(row=3,column=4)
            
        if root.shareY:
            shareYbutton=tk.Button(frame,text='▣ Share Y axis scale',command=shareYtoggle)
            shareYbutton.grid(row=4,column=4)
        else: 
            shareYbutton=tk.Button(frame,text='▢ Share Y axis scale',command=shareYtoggle)
            shareYbutton.grid(row=4,column=4)

    else:
        
        shareXbutton=tk.Button(frame,text='▢ Share X axis scale',state=tk.DISABLED)
        shareXbutton.grid(row=3,column=4)

        shareYbutton=tk.Button(frame,text='▢ Share Y axis scale',state=tk.DISABLED)
        shareYbutton.grid(row=4,column=4)

    plotsHelpButton=tk.Button(frame,text='?',command=plotsHelp,width=10)
    plotsHelpButton.grid(row=0,column=4)

    createMultiPlotButton=tk.Button(frame,text='Create Multi-Plot',command=generateMultiPlot,pady=20)
    createMultiPlotButton.grid(row=999,column=0,columnspan=2,sticky='w')



def displaySavedPlots(root,frame,removePlot,combinePlots,shareXtoggle,shareYtoggle,generateMultiPlot):

    #Translate

    #Activate the combine and remove buttons if buttons have been selected

    
    if len(root.buttonGridSelect)>0:
        removePlotButton=tk.Button(frame,text='Remove selected plot',command=removePlot)
        
        combinePlotsButton=tk.Button(frame,text='Combine selected plots',command=combinePlots)
        
    else:
        removePlotButton=tk.Button(frame,text='Remove selected plot',command=removePlot,state=tk.DISABLED)
        
        combinePlotsButton=tk.Button(frame,text='Combine selected plots',command=combinePlots,state=tk.DISABLED)

    combinePlotsButton.grid(row=2,column=4)
    removePlotButton.grid(row=1,column=4)

    #toggle buttons for sharing of the x or y axes
    if root.shareX:
        shareXbutton=tk.Button(frame,text='▣ Share X axis scale',command=shareXtoggle)
        
    else:
        shareXbutton=tk.Button(frame,text='▢ Share X axis scale',command=shareXtoggle)
    shareXbutton.grid(row=3,column=4)

    if root.shareY:
        shareYbutton=tk.Button(frame,text='▣ Share Y axis scale',command=shareYtoggle)
        
    else:
        shareYbutton=tk.Button(frame,text='▢ Share Y axis scale',command=shareYtoggle)
    shareYbutton.grid(row=4,column=4)

    plotsHelpButton=tk.Button(frame,text='?',command=plotsHelp,width=10)
    plotsHelpButton.grid(row=0,column=4)

    createMultiPlotButton=tk.Button(frame,text='Create Multi-Plot',command=generateMultiPlot,pady=20)
    createMultiPlotButton.grid(row=999,column=0,columnspan=2,sticky='w')

def displayPlotbuttonGrid(root,frame):
    for row in root.buttonGrid:
        for button in row:

            #Highlight the button in grey if it has been selected
                if button in root.buttonGridSelect:
                    button.bg='grey'
                else:
                    button.bg='light grey'
                #Rastor across the button grid and call .display() on them
                button.display()
    
    #This will grid_forget the removed buttons in .display()
    for button in root.removedButtons:
        button.display()
        
    root.removedButtons=[]


def updateFrames(root,globalFrame):
    #Forget previous frames
    for frame in root.frameDict:
        frameObj=root.frameDict[frame]
        frameObj.grid_forget()
        

        #If statements to draw the correct frame depending on the dict key
        if frame=="globalFrame":
            #frameObj=tk.LabelFrame(root,padx=10,pady=10)
            #root.frameDict['globalFrame']=frameObj
            frameObj.grid(row=0,column=0)

        elif frame=="filepathFrame":
            frameObj=tk.LabelFrame(globalFrame, text='Search for Rosbag path',padx=10,pady=10)
            root.frameDict['filepathFrame']=frameObj
            frameObj.grid(row=0,column=0,sticky='w')

        elif frame=="topicFrame":
            frameObj=tk.LabelFrame(globalFrame,text='Select a topic to analyze',padx=10,pady=10)
            root.frameDict['topicFrame']=frameObj
            frameObj.grid(row=1,column=0,rowspan=4,sticky=tk.N+tk.S+tk.E+tk.W)

        elif frame=="topicHighlight":
            frameObj=tk.LabelFrame(globalFrame,text='Info about the selected topic',padx=10,pady=10)
            root.frameDict['topicHighlight']=frameObj
            frameObj.grid(row=5,column=0,sticky=tk.W+tk.E)

        elif frame=="createCSVframe":
            frameObj=tk.LabelFrame(globalFrame,text='Create or load a CSV file',padx=10,pady=10)
            root.frameDict['createCSVframe']=frameObj
            frameObj.grid(row=0,column=1,sticky=tk.S+tk.E+tk.W+tk.N)

        elif frame=="createHeaderFrame":
            frameObj=tk.LabelFrame(globalFrame,text='Select data streams to analyze',padx=10,pady=10)
            root.frameDict['createHeaderFrame']=frameObj
            frameObj.grid(row=1,column=1,rowspan=2,sticky='nw')

        elif frame=="headerAnalyzeFrame":
            frameObj=tk.LabelFrame(globalFrame,text='Plotting Config',padx=10,pady=10)
            root.frameDict['headerAnalyzeFrame']=frameObj
            frameObj.grid(row=3,column=1,rowspan=3,sticky='nw')

        elif frame=="savedPlotsFrame":
            frameObj=tk.LabelFrame(globalFrame,text='Saved Plots',padx=10,pady=10)
            root.frameDict['savedPlotsFrame']=frameObj
            frameObj.grid(row=0,column=2,rowspan=2,sticky=tk.S+tk.E+tk.W+tk.N)

        elif frame=="settingsFrame":
            frameObj=tk.LabelFrame(globalFrame,text='Window settings',padx=10,pady=10)
            root.frameDict["settingsFrame"]=frameObj
            frameObj.grid(row=3,column=2,sticky='nw')


def createSettingsFrame(root,frame,redrawAll,toggleLanguage):
    testButton=tk.Button(frame,text='Redraw all',command = redrawAll)
    testButton.grid(row=0,column=0,pady=10,sticky='w')

    if root.lang=='EN':
        langToggle=tk.Button(frame,text='▣ English | ▢ 中文',command=toggleLanguage)
        langToggle.grid(row=1,column=0,pady=10,sticky='w')
    elif root.lang=='CN':
        langToggle=tk.Button(frame,text='▢ English | ▣ 中文',command=toggleLanguage)
        langToggle.grid(row=1,column=0,pady=10,sticky='w')

