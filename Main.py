import tkinter as tk
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askyesno
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from workers.DataImporter import ImportWorker
from workers.DataProcessor import DataHandler
from workers.StatisticsGenerator import Generator
from utils.StatEnum import StatType

class Main(tk.Tk):
    button1: Button
    button2: Button
    button3: Button

    def __init__(self):
        super().__init__()

        self.title("Data Processing App")
        self.attributes('-fullscreen',False)

        label = Label(self, text="Follow the steps to process the data", font= ('Arial 14 bold'))
        label.pack()

        labelStep1 = Label(self, text="Step 1 - Import the CSV files in database", font= ('Arial 12'))
        labelStep1.pack()
        Main.button1 = Button(self, text= "Execute Step 1", command=self.step_one)
        Main.button1.pack(expand=True)

        labelStep2 = Label(self, text="Step 2 - Prepare data and export to JSON", font= ('Arial 12'))
        labelStep2.pack()
        Main.button2 = Button(self, text= "Execute Step 2", command=self.step_two, state='disabled')
        Main.button2.pack(expand=True)

        labelStep3 = Label(self, text="Step 3 - Generate Stats and Graphs", font= ('Arial 12'))
        labelStep3.pack()
        Main.button3 = Button(self, text= "Execute Step 3", command=self.step_three, state='disabled')
        Main.button3.pack(expand=True)

    def step_one(self):
        answer = askyesno(title='Step 1 Confirmation', message='Are you sure you want to import data in database?')
        if answer:
            ImportWorker.database_clean_up()

            directoryName = askdirectory()

            ImportWorker.import_admin(directoryName)
            ImportWorker.import_ant(directoryName)
            ImportWorker.import_broadcaster(directoryName)
            ImportWorker.import_hf_schedule(directoryName)
            ImportWorker.import_language(directoryName)
            ImportWorker.import_location(directoryName)
        
            print('Step 1 - Import Process finished!')
            Main.button2['state'] = 'normal'
        return 
    
    def step_two(self):
        answer = askyesno(title='Step 2 Confirmation', message='Are you sure you want to start processing the data?')
        if answer:
            DataHandler.prepare_data()
            print('Step 2 - Data Processing finished!')
            Main.button3['state'] = 'normal'
        return
        
    def step_three(self):
        answer = askyesno(title='Step 3 Confirmation', message='Are you sure you want to load the JSON and generate the Stats?')
        if answer:
            dataFrame = Generator.prepare_json_data()

            filteredDfByPowr = Generator.filter_data_by_powr(dataFrame, 90)
            meanByPowr =  Generator.calculate_stats(filteredDfByPowr, StatType.MEAN)
            modeByPowr =  Generator.calculate_stats(filteredDfByPowr, StatType.MODE)
            medianByPowr = Generator.calculate_stats(filteredDfByPowr, StatType.MEDIAN)
            
            filteredDfByStart = Generator.filter_data_by_start(dataFrame, 1100)
            meanByStart =  Generator.calculate_stats(filteredDfByStart, StatType.MEAN)
            modeByStart =  Generator.calculate_stats(filteredDfByStart, StatType.MODE)
            medianByStart = Generator.calculate_stats(filteredDfByStart, StatType.MEDIAN)
                        
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
            labelStartOnwards110 = Label(self, text='Mean, Mode, and Median for CirafZones for "Start" onwards 100 ', font= ('Arial 10 bold'))
            labelStartOnwards110.pack()
            
            labelMeanByStart = Label(self, text=f'Mean: {meanByStart}', font= ('Arial 10'))
            labelMeanByStart.pack()
            labelModeByStart = Label(self, text=f'Mode: {modeByStart}', font= ('Arial 10'))
            labelModeByStart.pack()
            labelMedianByStart = Label(self, text=f'Median: {medianByStart}', font= ('Arial 10'))
            labelMedianByStart.pack()

            # Generate First Graph - Information for All shortwave frequencies
            self.f = Generator.generate_graph(dataFrame)
            self.canvas = FigureCanvasTkAgg(self.f)
            self.canvas.get_tk_widget().pack()
            self.canvas.draw()

            # Generate Second Graph - Output Correlation between 'Freq' and 'CirafZones'
            self.f = Generator.generate_correlation(dataFrame)
            self.canvas = FigureCanvasTkAgg(self.f)
            self.canvas.get_tk_widget().pack()
            self.canvas.draw()

            print('Step 3 - Stats were generated!')

        return

if __name__ == "__main__":

    app = Main()
    app.mainloop()
