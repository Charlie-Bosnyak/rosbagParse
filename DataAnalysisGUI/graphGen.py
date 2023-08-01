import numpy as np
import matplotlib.pyplot as plt

#Create a matplotlib window with multiple subplots
def generateMultiPlot(root):
    colorIndex=0
    #Side by side subplots
    if root.plotGridWidth>1 and root.plotGridHeight>1:
        fig,axs=plt.subplots(root.plotGridHeight,root.plotGridWidth,sharex=root.shareX,sharey=root.shareY)
    elif root.plotGridWidth>1:
        fig,axs= plt.subplots(1,root.plotGridWidth,sharex=root.shareX,sharey=root.shareY)
    elif root.plotGridHeight>1:
        fig,axs= plt.subplots(root.plotGridHeight,sharex=root.shareX,sharey=root.shareY)
    else:
        fig,axs= plt.subplots(sharex=root.shareX,sharey=root.shareY)

    fig.set_figheight(8)
    fig.set_figwidth(12.8)

    for row in range(root.plotGridHeight):
        for col in range(root.plotGridWidth):
            if root.plotGridWidth>1 and root.plotGridHeight>1:
                currPlot=root.plotGrid[row][col]
                plotDisplay=axs[row,col]
            elif root.plotGridWidth>1:
                currPlot=root.plotGrid[0][col]
                plotDisplay=axs[col]
            elif root.plotGridHeight>1:
                currPlot=root.plotGrid[row][0]
                plotDisplay=axs[row]
            else:
                currPlot=root.plotGrid[0][0]
                plotDisplay=axs

            if currPlot=='':

                    continue
                #Get the data from the plot object
            xData=currPlot.xData
            yData=currPlot.yData
            currCol=0
            #Set up the plot

            for yDataCol in yData:
                
                if currPlot.graphType=='Line':
                    plotDisplay.plot(xData,yDataCol,label=currPlot.yDataLabels[currCol],color=f'C{colorIndex}')
                if currPlot.graphType=='Scatter':
                    plotDisplay.scatter(xData,yDataCol,label=currPlot.yDataLabels[currCol],color=f'C{colorIndex}')
                if currPlot.graphType=='Bar':
                    plotDisplay.bar(xData,yDataCol,label=currPlot.yDataLabels[currCol],color=f'C{colorIndex}')
                colorIndex+=1
                
                currCol+=1
            plotDisplay.set_title(currPlot.name)
            plotDisplay.set(xlabel=currPlot.xDataLabel)
            plotDisplay.xaxis.set_label_coords(0.9,-0.1)
            plotDisplay.legend()

            if root.shareX and root.shareY:
                for ax in fig.get_axes():
                    ax.label_outer()

            if currPlot.isTwin==True:
                currCol=0
                plotDisplay.set_title(currPlot.name)
                plotDisplay.set_ylabel(currPlot.baseName,color=f'C{colorIndex-1}')
                plotDisplay.tick_params(color=f'C{colorIndex-1}')
                plotDisplay.yaxis.set_label_coords(-0.05,0.95)

                newTwin=plotDisplay.twinx()
                newTwin.set_ylabel(currPlot.twinName,color=f'C{colorIndex}')
                newTwin.tick_params(color=f'C{colorIndex}')
                
                newTwin.yaxis.set_label_coords(1.05,0.95)
                for yDataCol in currPlot.twinYdata:
                    if currPlot.graphType=='Line':
                        newTwin.plot(currPlot.twinXdata,yDataCol,label=currPlot.twinYlabels[currCol],color=f'C{colorIndex}')
                    if currPlot.graphType=='Scatter':
                        newTwin.scatter(currPlot.twinXdata,yDataCol,label=currPlot.twinYlabels[currCol],color=f'C{colorIndex}')
                    if currPlot.graphType=='Bar':
                        newTwin.bar(currPlot.twinXdata,yDataCol,label=currPlot.twinYlabels[currCol],color=f'C{colorIndex}')
                    colorIndex+=1
                    currCol+=1
                newTwin.legend()
    plt.legend()            
    plt.show()

    #Generate the matplotlib graph
def generateGraph(root):
    #get the data from radiobuttons and listbox
    root.XdataIndex=root.xAxisSelection.get()
   
    root.YdataIndices=root.yAxisListbox.curselection()
   
    xData=root.dataList[root.XdataIndex]
    
    #Creating the graphs
    if root.graphType.get()=="Line":
        for i in root.YdataIndices:
            
            plt.plot(xData,root.dataList[i],label=f'{root.focusHeaderList[i]}')
    elif root.graphType.get()=="Scatter":
        for i in root.YdataIndices:
            plt.scatter(xData,root.dataList[i],label=f'{root.focusHeaderList[i]}')
    elif root.graphType.get()=="Bar":
        for i in root.YdataIndices:
            plt.bar(xData,root.dataList[i],label=f'{root.focusHeaderList[i]}')
    plt.xlabel(f'{root.focusHeaderList[root.XdataIndex]}')
    plt.legend()
    plt.show()