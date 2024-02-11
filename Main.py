import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askyesno
from Workers.DataImporter import ImportWorker
from Workers.DataProcessor import DataHandler
from Workers.StatisticsGenerator import Generator
from Utils.StatEnum import StatType

class Main(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Data Processing App")
        self.geometry("1200x600")

        label = ttk.Label(self, text="Follow the steps to process the data", font= ('Arial 14 bold'), padding='20')
        label.pack()

        labelStep1 = ttk.Label(self, text="Step 1 - Import the CSV files in database", font= ('Arial 12'))
        labelStep1.pack()
        ttk.Button(self, text= "Execute Step 1", command=self.stepOne).pack(expand=True)

        labelStep2 = ttk.Label(self, text="Step 2 - Prepare data and export to JSON", font= ('Arial 12'))
        labelStep2.pack()
        ttk.Button(self, text= "Execute Step 2", command=self.stepTwo).pack(expand=True)

        labelStep3 = ttk.Label(self, text="Step 3 - Generate Stats and Graphs", font= ('Arial 12'))
        labelStep3.pack()
        ttk.Button(self, text= "Execute Step 3", command=self.stepThree).pack(expand=True)

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
            
            
            print(meanByPowr)
            print(modeByPowr)
            print(medianByPowr)


            
            print(meanByStart)
            print(modeByStart)
            print(medianByStart)

        return

if __name__ == "__main__":
    app = Main()
    app.mainloop()
