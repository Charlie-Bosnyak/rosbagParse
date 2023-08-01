import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from PIL import Image, ImageTk


def displayTopics(root,frame,filterTopic,updateSelectedTopic,forwardTopicPage,backTopicPage,selectedTopic,topicFilter):
    #Entry box for filtering topics
    #Translate

    pageIndicator=tk.Label(frame,text=f'第{root.topicPageNum+1}页(总共{root.filteredTopicCount//root.topicsPerPage+1}页）')
    pageIndicator.grid(row=1000,column=2)

    #Display rows of radio buttons with text corresponding to that topic
    if not root.filteredTopicList  == []:
        topicFilterLabel=tk.Label(frame,text="搜关键词")
        topicFilterLabel.grid(row=0,column=1,columnspan=2,sticky='w')

        filterEntry=tk.Entry(frame,textvariable=topicFilter)
        filterEntry.grid(row=1,column=1,columnspan=2,sticky='w')


        topicFilterButton=tk.Button(frame,text='搜索',command=filterTopic)
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
    return filedialog.askopenfilename(initialdir=bagFolder,title="选CSV文件",filetypes=(('CSV文件','*.csv'),('所有文件','*.*')))

#Creates the CSV file
def createCSVbutton(root,frame,writeCSV):
    createCSVbutton=tk.Button(frame,text='写CSV文件',padx=10,pady=5,command=writeCSV)
    createCSVbutton.grid(row=0,column=0,sticky='w')


def overWriteCSVfile(CSVpath):
    return messagebox.askyesno("重写CSV文件?",f"CSV文件已经被创始,路径是 \n {CSVpath} \n 重写CSV文件?")

#Reads the data columns from the CSV file previously selected and puts them in a data table
def readCSVbutton(root,frame,readCSV):
    readCSVbutton=tk.Button(frame,text='读已选择的CSV文件',padx=10,pady=10,command=readCSV)
    readCSVbutton.grid(row=0,column=0,sticky='nw')

#Reads the data from the table into a 2D list
def confirmHeaderButton(root,frame,confirmHeaders):
    confirmHeadersButton=tk.Button(frame,text="确认选择",padx=10,pady=10,command=confirmHeaders)
    confirmHeadersButton.grid(row=3,column=0,sticky='w')

#Subtract all entries of a data column by its first entry. 
#Useful for data columns that correspond to time, so that time can be read as time since start of recording
def normalizeTimePopup(root,column):
    return messagebox.askyesno("改变时间尺度?",f"""数据流{root.focusHeaderList[column]}有关键词时间(time) \n
把{root.focusHeaderList[column]}里面的数据减掉最早的数据吗？\n
减掉之后每一数据会代表从Rosbag录音开始已过的时间。""")

def chooseTopicPopup(root):
    messagebox.showwarning("选话题","写CSV之前先选要看重的话题")

#If there are errors when float-ing values of a data column or cells of that column are blank
def datalistConstructionError(root,column):
    messagebox.showerror("数据流有错",f"""存数据流时出现问题\n
确认{root.focusHeaderList[column]}数据流是否全部从数值搭建的""")

#Displays the number of lines in the data lines that were written to the 2d list
def linesProcessedLabel(root,frame,lineCount):
    linesProcessedLabel=tk.Label(frame,text=f"存了{lineCount}条数据",padx=10,pady=10)
    linesProcessedLabel.grid(row=3,column=1,sticky='w')

def twinGraphWarning(root,name):
    messagebox.showwarning("已选的图标已经被结合其俩了",f"""{name}图标已经是个结合图\n
为了防止出错跳过了{name}的结合过程""")

def twinGraphXAxisWarning(root,currPlot,twinPlot):
    
    response=messagebox.askokcancel("不同的X尺度",f"""图标{currPlot.name}用X轴:{currPlot.xDataLabel}但图标{twinPlot.name}用X轴:{twinPlot.xDataLabel}\n
产生结合图时用不同的X轴可能会创造尺度错误\n
继续产生结合图?""")
    return response

#Create the display name for the twinned plot
def combinePlotsName(name1,name2):
    combinedName=name1+ ' and '+name2
    return combinedName

#Pop up that lets the user enter a self-selected name for the saved plot
def savePlotWindow(root):
    plotName=simpledialog.askstring('保存图标',"给图标取个名字:")
    while True:
        if plotName=="":
            
            plotName=simpledialog.askstring('保存图标',"给图标取个名字:")
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

    setYaxesLabel=tk.Label(frame,text="选要显示的数据流")
    setYaxesLabel.grid(row=999,column=0,sticky='w')
    root.yAxisListbox.grid(row=1000,column=0,rowspan=2,sticky='w')

#Additional info about finding the bag file
def filepathHelp():
    messagebox.showinfo("数据包更多信息","""按了 "确认" 之后,一个文件夹会在数据包的路径出现\n
CSV文件会保存在这里""")

#Additional info about creating or finding a CSV
def CSVhelp():
    messagebox.showinfo("CSV路径更多信息","""用已选择的话题产生CSV或找已经存在的CSV""")

#Additional info about configurating the multi-plot
def plotsHelp():
    global plotInfoImg
    plotInfo=tk.Toplevel()
    plotInfo.title('多图设置指南')
    plotInfoImg= ImageTk.PhotoImage(Image.open("GUI_Images/PlotsHelpCN.png"))
    plotInfoLabel=tk.Label(plotInfo,image=plotInfoImg)
    plotInfoLabel.pack()


def displayFilepath(root,frame,setFilepath):
    root.bagpath=filedialog.askopenfilename(initialdir="~/",title="选Rosbag文件",filetypes=(('Rosbag文件','*.bag'),('所有文件','*.*'))) 
    newBagpath=root.bagpath
    BagpathLineLength=50
    #Split the label into multiple lines
    for i in range(len(newBagpath)//BagpathLineLength):
        newBagpath=newBagpath[:(i+1)*BagpathLineLength]+"\n"+newBagpath[(i+1)*BagpathLineLength:]

    
    
    filenameLabel=tk.Label(frame,text=newBagpath)
    filenameLabel.grid(row=1,column=0,sticky='E')
    

    confirmFilepath=tk.Button(frame,text='确认',command=setFilepath)
    confirmFilepath.grid(row=0,column=1,sticky='NE')

    if root.bagpath[-4:]!='.bag' and root.bagpath  != 'Rosbag path not selected':
        messagebox.showwarning("文件类型警告","已选的文件不是 .bag 类型\n 分析时会出错")



def createFindBagpathFrame(root,frame,displayFilepath,setFilepath):
    #Button to pop up path selection window
    openFilepath=tk.Button(frame,text='找Rosbag',command=displayFilepath)
    openFilepath.grid(row=0,column=0,sticky='NW')

    #Button to confirm bag path
    if root.bagpath  == 'Rosbag path not selected':
        confirmFilepath=tk.Button(frame,text='确认',command=setFilepath,state=tk.DISABLED)
        confirmFilepath.grid(row=0,column=1,sticky='NE')
    else:
        confirmFilepath=tk.Button(frame,text='确认',command=setFilepath)
        confirmFilepath.grid(row=0,column=1,sticky='NE')

    #Label to display currently selected path

    newBagpath=root.bagpath
    BagpathLineLength=50
    #Split the label into multiple lines
    for i in range(len(newBagpath)//BagpathLineLength):
        newBagpath=newBagpath[:(i+1)*BagpathLineLength]+"\n"+newBagpath[(i+1)*BagpathLineLength:]

    
    
    filenameLabel=tk.Label(frame,text=newBagpath)
    filenameLabel.grid(row=1,column=0,sticky='E')


    #filenameLabel=tk.Label(frame,text=root.bagpath,width=50)
    #filenameLabel.grid(row=1,column=0,sticky='E')

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

    pageIndicator=tk.Label(frame,text=f'第{root.topicPageNum+1}页（总共{root.filteredTopicCount//root.topicsPerPage+1}页）')
    pageIndicator.grid(row=1000,column=2,sticky=tk.S)

def createTopicHighlightFrame(root,frame):
    
    root.topicInfoLabelList=[]

    #Different headers and labels
    topicNameHeader=tk.Label(frame,text="话题名字:",padx=10,pady=10)
    topicNameHeader.grid(row=0,column=0,sticky='w')

    topicNameLabel=tk.Label(frame,text=" ",padx=10,pady=10)
    topicNameLabel.grid(row=0,column=1,sticky='w')

    topicTypesHeader=tk.Label(frame,text="话题信息类型:",padx=10,pady=10)
    topicTypesHeader.grid(row=1,column=0,sticky='w')

    topicTypesLabel=tk.Label(frame,text=" ",padx=10,pady=10)
    topicTypesLabel.grid(row=1,column=1,sticky='w')

    topicMsgCountHeader=tk.Label(frame,text="信息数量:",padx=10,pady=10)
    topicMsgCountHeader.grid(row=2,column=0,sticky='w')

    topicMsgCountLabel=tk.Label(frame,text=" ",padx=10,pady=10)
    topicMsgCountLabel.grid(row=2,column=1,sticky='w')

    topicFreqHeader=tk.Label(frame,text="信息频率:",padx=10,pady=10)
    topicFreqHeader.grid(row=3,column=0,sticky='w')

    topicFreqLabel=tk.Label(frame,text=" ",padx=10,pady=10)
    topicFreqLabel.grid(row=3,column=1,sticky='w')

def createCSVwriteFrame(root,frame,writeCSV,findCSV):
    
    #Button to write CSV from selected topic, disabled if no topic is selected
    if root.filteredTopicCount<1:
        createCSVbutton=tk.Button(frame,text='写CSV文件',padx=10,pady=5,command=writeCSV,state=tk.DISABLED)
        createCSVbutton.grid(row=0,column=0,sticky='w')
    else:
        createCSVbutton=tk.Button(frame,text='写CSV文件',padx=10,pady=5,command=writeCSV)
        createCSVbutton.grid(row=0,column=0,sticky='w')

    findCSVbutton=tk.Button(frame,text='找CSV文件',padx=10,pady=5,command=findCSV)
    findCSVbutton.grid(row=0,column=1)

    helpButtonCSV=tk.Button(frame,text="?",padx=10,pady=5,command=CSVhelp)
    helpButtonCSV.grid(row=0,column=2,sticky='e')

    CSVpathLabel1=tk.Label(frame,text=f'文件路径:',padx=10,pady=5)
    CSVpathLabel1.grid(row=1,column=0,sticky='w')

    #Create the label that displays the current CSV path
    newCSVpath=root.CSVpath
    CSVlineLength=40
    #Split the label into multiple lines
    for i in range(len(newCSVpath)//CSVlineLength):
        newCSVpath=newCSVpath[:(i+1)*CSVlineLength]+"\n"+newCSVpath[(i+1)*CSVlineLength:]

    #If the current CSV path is empty, then display a message
    if root.CSVpath=="":

        root.CSVpathLabel2=tk.Label(frame,text="CSV未产生")
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
    
        readCSVbutton=tk.Button(frame,text='读已选择的CSV文件',padx=10,pady=10,command=readCSV,state=tk.DISABLED)
        readCSVbutton.grid(row=0,column=0,sticky='nw')
    else:
        readCSVbutton=tk.Button(frame,text='读已选择的CSV文件',padx=10,pady=10,command=readCSV)
        readCSVbutton.grid(row=0,column=0,sticky='nw')

    selectHeadersPrompt=tk.Label(frame,text='从以下的数据流选择要注重的',padx=10,pady=10)
    selectHeadersPrompt.grid(row=1,column=0,columnspan=2,sticky='w')
    
    #If the selection has been made, enable the buttons that allow confirmation
    if root.headersListbox.size()>0:
        confirmHeadersButton=tk.Button(frame,text="确认选择",padx=10,pady=10,command=confirmHeaders)
        confirmHeadersButton.grid(row=3,column=0,sticky='w')
    else:

        confirmHeadersButton=tk.Button(frame,text="确认选择",padx=10,pady=10,command=confirmHeaders,state=tk.DISABLED)
        confirmHeadersButton.grid(row=3,column=0,sticky='w')

    

    linesProcessedLabel=tk.Label(frame,text=f"存了{root.lineCount}条数据",padx=10,pady=10)
    linesProcessedLabel.grid(row=3,column=1,sticky='w')

    

def createHeaderAnalyzeFrame(root,frame,generateGraph,savePlot):
    setXaxisLabel=tk.Label(frame,text="选择当X轴的数据流")
    setXaxisLabel.grid(row=0,column=0,sticky='w')

    
    
    #Listbox for all of the headers that can be plotted
    root.yAxisListbox=tk.Listbox(frame,width=30,selectmode=tk.MULTIPLE)

    root.yAxisListbox.grid(row=1000,column=0,rowspan=2,sticky='w')

    setYaxesLabel=tk.Label(frame,text="选择要画的数据流")
    setYaxesLabel.grid(row=2,column=0,sticky='w')

    root.graphType.set("Line")
    typeOptions=["Line","Scatter","Bar"]

    
    graphTypeLabel=tk.Label(frame,text="选择图标类型",padx=10,pady=5)
    graphTypeLabel.grid(row=0,column=1,sticky='sw')

    graphTypeDrop=tk.OptionMenu(frame,root.graphType,*typeOptions)
    graphTypeDrop.grid(row=1,column=1)

    generateGraphButton=tk.Button(frame,text="显示 \n 图标",command=generateGraph,relief=tk.RAISED)
    generateGraphButton.grid(row=1000,column=1)

    savePlotButton=tk.Button(frame,text='保存图标',command=savePlot,relief=tk.RAISED)
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


    plotsLabel=tk.Label(frame,text='选择想要同时显示的图标')
    plotsLabel.grid(row=0,column=0,columnspan=3,sticky='w')

    #Open the remove and combine buttons if plot buttons have been selected
    if len(root.buttonGridSelect)>0:

        removePlotButton=tk.Button(frame,text='清除图标',command=removePlot)
        removePlotButton.grid(row=1,column=4)

        combinePlotsButton=tk.Button(frame,text='产生结合图标',command=combinePlots)
        combinePlotsButton.grid(row=2,column=4)
    else:

        removePlotButton=tk.Button(frame,text='清除图标',command=removePlot,state=tk.DISABLED)
        removePlotButton.grid(row=1,column=4)

        combinePlotsButton=tk.Button(frame,text='产生结合图标',command=combinePlots,state=tk.DISABLED)
        combinePlotsButton.grid(row=2,column=4)

    #If plots have been saved, enable the share x and share y toggles
    if root.plotsListbox.size()>0:

        if root.shareX:
            shareXbutton=tk.Button(frame,text='▣ 保持一致的X轴尺度',command=shareXtoggle)
            shareXbutton.grid(row=3,column=4)
        else:
            shareXbutton=tk.Button(frame,text='▢ 保持一致的X轴尺度',command=shareXtoggle)
            shareXbutton.grid(row=3,column=4)
            
        if root.shareY:
            shareYbutton=tk.Button(frame,text='▣ 保持一致的Y轴尺度',command=shareYtoggle)
            shareYbutton.grid(row=4,column=4)
        else: 
            shareYbutton=tk.Button(frame,text='▢ 保持一致的Y轴尺度',command=shareYtoggle)
            shareYbutton.grid(row=4,column=4)

    else:
        
        shareXbutton=tk.Button(frame,text='▢ 保持一致的X轴尺度',state=tk.DISABLED)
        shareXbutton.grid(row=3,column=4)

        shareYbutton=tk.Button(frame,text='▢ 保持一致的Y轴尺度',state=tk.DISABLED)
        shareYbutton.grid(row=4,column=4)

    plotsHelpButton=tk.Button(frame,text='?',command=plotsHelp,width=10)
    plotsHelpButton.grid(row=0,column=4)

    createMultiPlotButton=tk.Button(frame,text='用网格显示以上的图标',command=generateMultiPlot,pady=20)
    createMultiPlotButton.grid(row=999,column=0,columnspan=2,sticky='w')



def displaySavedPlots(root,frame,removePlot,combinePlots,shareXtoggle,shareYtoggle,generateMultiPlot):

    #Translate

    #Activate the combine and remove buttons if buttons have been selected

    
    if len(root.buttonGridSelect)>0:
        removePlotButton=tk.Button(frame,text='清除图标',command=removePlot)
        
        combinePlotsButton=tk.Button(frame,text='产生结合图标',command=combinePlots)
        
    else:
        removePlotButton=tk.Button(frame,text='清除图标',command=removePlot,state=tk.DISABLED)
        
        combinePlotsButton=tk.Button(frame,text='产生结合图标',command=combinePlots,state=tk.DISABLED)

    combinePlotsButton.grid(row=2,column=4)
    removePlotButton.grid(row=1,column=4)

    #toggle buttons for sharing of the x or y axes
    if root.shareX:
        shareXbutton=tk.Button(frame,text='▣ 保持一致的X轴尺度',command=shareXtoggle)
        
    else:
        shareXbutton=tk.Button(frame,text='▢ 保持一致的X轴尺度',command=shareXtoggle)
    shareXbutton.grid(row=3,column=4)

    if root.shareY:
        shareYbutton=tk.Button(frame,text='▣ 保持一致的Y轴尺度',command=shareYtoggle)
        
    else:
        shareYbutton=tk.Button(frame,text='▢ 保持一致的Y轴尺度',command=shareYtoggle)
    shareYbutton.grid(row=4,column=4)

    plotsHelpButton=tk.Button(frame,text='?',command=plotsHelp,width=10)
    plotsHelpButton.grid(row=0,column=4)

    createMultiPlotButton=tk.Button(frame,text='用网格显示以上的图标',command=generateMultiPlot,pady=20)
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
            frameObj=tk.LabelFrame(globalFrame, text='搜Rosbag路径',padx=10,pady=10)
            root.frameDict['filepathFrame']=frameObj
            frameObj.grid(row=0,column=0,sticky='w')

        elif frame=="topicFrame":
            frameObj=tk.LabelFrame(globalFrame,text='选注重的话题',padx=10,pady=10)
            root.frameDict['topicFrame']=frameObj
            frameObj.grid(row=1,column=0,rowspan=4,sticky=tk.N+tk.S+tk.E+tk.W)

        elif frame=="topicHighlight":
            frameObj=tk.LabelFrame(globalFrame,text='话题信息',padx=10,pady=10)
            root.frameDict['topicHighlight']=frameObj
            frameObj.grid(row=5,column=0,sticky=tk.W+tk.E)

        elif frame=="createCSVframe":
            frameObj=tk.LabelFrame(globalFrame,text='创始或找CSV文件',padx=10,pady=10)
            root.frameDict['createCSVframe']=frameObj
            frameObj.grid(row=0,column=1,sticky=tk.S+tk.E+tk.W+tk.N)

        elif frame=="createHeaderFrame":
            frameObj=tk.LabelFrame(globalFrame,text='选关键的数据流',padx=10,pady=10)
            root.frameDict['createHeaderFrame']=frameObj
            frameObj.grid(row=1,column=1,rowspan=2,sticky='nw')

        elif frame=="headerAnalyzeFrame":
            frameObj=tk.LabelFrame(globalFrame,text='图表设置',padx=10,pady=10)
            root.frameDict['headerAnalyzeFrame']=frameObj
            frameObj.grid(row=3,column=1,rowspan=3,sticky='nw')

        elif frame=="savedPlotsFrame":
            frameObj=tk.LabelFrame(globalFrame,text='保存的数据流',padx=10,pady=10)
            root.frameDict['savedPlotsFrame']=frameObj
            frameObj.grid(row=0,column=2,rowspan=2,sticky=tk.S+tk.E+tk.W+tk.N)

        elif frame=="settingsFrame":
            frameObj=tk.LabelFrame(globalFrame,text='设置',padx=10,pady=10)
            root.frameDict["settingsFrame"]=frameObj
            frameObj.grid(row=3,column=2,sticky='nw')


def createSettingsFrame(root,frame,redrawAll,toggleLanguage):
    #testButton=tk.Button(frame,text='Redraw all',command = redrawAll)
    #testButton.grid(row=0,column=0,pady=10,sticky='w')

    if root.lang=='EN':
        langToggle=tk.Button(frame,text='▣ English | ▢ 中文',command=toggleLanguage)
        langToggle.grid(row=1,column=0,pady=10,sticky='w')
    elif root.lang=='CN':
        langToggle=tk.Button(frame,text='▢ English | ▣ 中文',command=toggleLanguage)
        langToggle.grid(row=1,column=0,pady=10,sticky='w')

