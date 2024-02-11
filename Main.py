import tkinter as tk
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askyesno
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from Workers.DataImporter import ImportWorker
from Workers.DataProcessor import DataHandler
from Workers.StatisticsGenerator import Generator
from Utils.StatEnum import StatType

class Main(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Data Processing App")
        self.attributes('-fullscreen',False)

        label = Label(self, text="Follow the steps to process the data", font= ('Arial 14 bold'))
        label.pack()

        labelStep1 = Label(self, text="Step 1 - Import the CSV files in database", font= ('Arial 12'))
        labelStep1.pack()
        Button(self, text= "Execute Step 1", command=self.stepOne).pack(expand=True)

        labelStep2 = Label(self, text="Step 2 - Prepare data and export to JSON", font= ('Arial 12'))
        labelStep2.pack()
        Button(self, text= "Execute Step 2", command=self.stepTwo).pack(expand=True)

        labelStep3 = Label(self, text="Step 3 - Generate Stats and Graphs", font= ('Arial 12'))
        labelStep3.pack()
        Button(self, text= "Execute Step 3", command=self.stepThree).pack(expand=True)
        
        

    def stepOne(self):
        answer = askyesno(title='Step 1 Confirmation', message='Are you sure you want to import data in database?')
        if answer:
            ImportWorker.databaseCleanUp()

            directoryName = askdirectory()

            ImportWorker.importAdmin(directoryName)
            ImportWorker.importAnt(directoryName)
            ImportWorker.importBroadcaster(directoryName)
            ImportWorker.importHfSchedule(directoryName)
            ImportWorker.importLanguage(directoryName)
            ImportWorker.importLocation(directoryName)

    def stepTwo(self):
        answer = askyesno(title='Step 2 Confirmation', message='Are you sure you want to start processing the data?')
        if answer:
            DataHandler.PrepareData()
            return
        
    def stepThree(self):
        answer = askyesno(title='Step 3 Confirmation', message='Are you sure you want to load the JSON and generate the Stats?')
        if answer:
            dataFrame = Generator.PrepareJsonData()

            filteredDfByPowr = Generator.filterDatabyPowr(dataFrame, 90)
            meanByPowr =  Generator.calculateStats(filteredDfByPowr, StatType.MEAN)
            modeByPowr =  Generator.calculateStats(filteredDfByPowr, StatType.MODE)
            medianByPowr = Generator.calculateStats(filteredDfByPowr, StatType.MEDIAN)
            
            
            filteredDfByStart = Generator.filterDatabyStart(dataFrame, 1100)
            meanByStart =  Generator.calculateStats(filteredDfByStart, StatType.MEAN)
            modeByStart =  Generator.calculateStats(filteredDfByStart, StatType.MODE)
            medianByStart = Generator.calculateStats(filteredDfByStart, StatType.MEDIAN)
                        
            # Displays Mean, Mode and Median for Power More than 90
            labelPowerMoreThan90 = Label(self, text='Mean, Mode, and Median for CirafZones for "Powr" more than 90', font= ('Arial 10 bold'))
            labelPowerMoreThan90.pack()
            
            labelMeanByPower = Label(self, text=f'Mean: {meanByPowr}', font= ('Arial 10'))
            labelMeanByPower.pack()
            labelModeByPower = Label(self, text=f'Mode: {modeByPowr}', font= ('Arial 10'))
            labelModeByPower.pack()
            labelMedianByPower = Label(self, text=f'Median: {medianByPowr}', font= ('Arial 10'))
            labelMedianByPower.pack()
            
            # Displays Mean, Mode and Median for Start Onwards 110
            labelStartOnwards110 = Label(self, text='Mean, Mode, and Median for CirafZones for "Powr" more than 90', font= ('Arial 10 bold'))
            labelStartOnwards110.pack()
            
            labelMeanByStart = Label(self, text=f'Mean: {meanByStart}', font= ('Arial 10'))
            labelMeanByStart.pack()
            labelModeByStart = Label(self, text=f'Mode: {modeByStart}', font= ('Arial 10'))
            labelModeByStart.pack()
            labelMedianByStart = Label(self, text=f'Median: {medianByStart}', font= ('Arial 10'))
            labelMedianByStart.pack()

            # Generate First Graph - Information for All shortwave frequencies
            self.f = Generator.GenerateGraph()
            self.canvas = FigureCanvasTkAgg(self.f)
            self.canvas.get_tk_widget().pack()
            self.canvas.draw()

            # Generate Second Graph - Output Correlation between 'Freq' and 'CirafZones'
            # self.g = Generator.GenerateCorrelation()
            # self.canvas = FigureCanvasTkAgg(self.g)
            # self.canvas.get_tk_widget().pack()
            # self.canvas.draw()            

        return

if __name__ == "__main__":
    app = Main()
    app.mainloop()
