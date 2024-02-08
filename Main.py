import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askyesno
from DataImporter import ImportWorker
from DataLoader import Loader

class Main(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Data Processing App")
        self.geometry("700x350")

        label = ttk.Label(self, text="Follow the steps to process the data", font= ('Arial 14 bold'), padding='20')
        label.pack()

        labelStep1 = ttk.Label(self, text="Step 1 - Import the CSV files in database", font= ('Arial 12'))
        labelStep1.pack()
        ttk.Button(self, text= "Execute Step 1", command=self.stepOne).pack(expand=True)

        labelStep2 = ttk.Label(self, text="Step 2 - Load data in DataFrames", font= ('Arial 12'))
        labelStep2.pack()
        ttk.Button(self, text= "Execute Step 2", command=self.stepTwo).pack(expand=True)

        labelStep3 = ttk.Label(self, text="Step 3 - Clean data", font= ('Arial 12'))
        labelStep3.pack()
        ttk.Button(self, text= "Execute Step 3", command=self.stepOne).pack(expand=True)

        labelStep4 = ttk.Label(self, text="Step 4 - XXX XXX XXX", font= ('Arial 12'))
        labelStep4.pack()
        ttk.Button(self, text= "Execute Step 4", command=self.stepOne).pack(expand=True)

        labelStep5 = ttk.Label(self, text="Step 5 - XXX XXX XXX", font= ('Arial 12'))
        labelStep5.pack()
        ttk.Button(self, text= "Execute Step 5", command=self.stepOne).pack(expand=True)

    def stepOne(self):
        answer = askyesno(title='Step 1 Confirmation', message='Are you sure you want to import data in database?')
        if answer:
            directoryName = askdirectory()

            ImportWorker.importAdmin(directoryName)
            ImportWorker.importAnt(directoryName)
            ImportWorker.importBroadcaster(directoryName)
            ImportWorker.importHfSchedule(directoryName)
            ImportWorker.importLanguage(directoryName)
            ImportWorker.importLocation(directoryName)

    def stepTwo(self):
        answer = askyesno(title='Step 2 Confirmation', message='Are you sure you want to load the data?')
        if answer:
            adminData = Loader.LoadAdminData()
            return adminData

if __name__ == "__main__":
    app = Main()
    app.mainloop()
