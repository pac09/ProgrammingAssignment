import pandas as pd
import numpy as np
from scipy import stats
from Utils.StatEnum import StatType
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class Generator:

    def PrepareJsonData():
        df = pd.read_json(r'OutputFiles\Data.json', orient=True)

        # Flatten the Arrays present in DataFrame from JSON file
        broadcasterSeries = df.Broadcaster.apply(Generator.flatten)
        broadcasterDf = pd.DataFrame(broadcasterSeries)
        
        adminSeries = df.Admin.apply(Generator.flatten)
        adminDf = pd.DataFrame(adminSeries)

        languageSeries = df.Language.apply(Generator.flatten)
        languageDf = pd.DataFrame(languageSeries)

        antSeries = df.Ant.apply(Generator.flatten)
        antDf = pd.DataFrame(antSeries)
        
        locationSeries = df.Location.apply(Generator.flatten)
        locationDf = pd.DataFrame(locationSeries)

        df = pd.concat([df.drop(['Broadcaster', 'Admin', 'Language', 'Ant', 'Location'], axis=1),
                broadcasterDf,
                adminDf,
                languageDf,
                antDf,
                locationDf], axis=1)

        return df
                
    def calculateStats(df, classification):
        cleanedDataFrame = Generator.cleanData(df)
        match classification:
            case StatType.MEAN:
                return np.mean(cleanedDataFrame)
            case StatType.MODE:
                return stats.mode(cleanedDataFrame)
            case StatType.MEDIAN:
                return np.median(cleanedDataFrame)

    def filterDatabyPowr(df, val):
        return df[(df.Powr > val)]
    
    def filterDatabyStart(df, val):
        return df[(df.Start >= val)]

    def cleanData(df):
        cirafZonesDf = (df['CirafZones']).to_frame()
        cirafZonesDf["Result"] = cirafZonesDf["CirafZones"].str.isnumeric().apply(lambda x: "No" if x == False else "Yes")
        dataToErasedf = cirafZonesDf[(cirafZonesDf['Result'] == 'No')].index
        cirafZonesDf.drop(dataToErasedf, inplace=True)
        cirafZonesDf = cirafZonesDf[cirafZonesDf.columns.drop('Result')]

        return cirafZonesDf['CirafZones'].astype(float)
    
    def flatten(js):
        return pd.DataFrame(js).squeeze()
    
    def GenerateGraph(df):
        # x = [1,2,3,4]
        # y = [20,21,20.5, 20.8]
        # fig = Figure()
        # axes = fig.add_subplot(111)
        # axes.plot(x,y)

        # Clean the data to have 
        cleanedDataFrame = Generator.cleanData(df)
        print(df)
        
        # set up the figure and axes
        fig = plt.figure(figsize=(8, 3))
        ax1 = fig.add_subplot(121, projection='3d')
        ax2 = fig.add_subplot(122, projection='3d')

        # fake data
        _x = np.arange(4)
        _y = np.arange(5)
        _xx, _yy = np.meshgrid(_x, _y)
        x, y = _xx.ravel(), _yy.ravel()

        top = x + y
        bottom = np.zeros_like(top)
        width = depth = 1

        ax1.bar3d(x, y, bottom, width, depth, top, shade=True)
        ax1.set_title('Shaded')

        ax2.bar3d(x, y, bottom, width, depth, top, shade=False)
        ax2.set_title('Not Shaded')

        plt.show()
        return fig
        
    def GenerateCorrelation():
        # x = [1,2,3,4]
        # y = [20,21,20.5, 20.8]
        # fig = Figure()
        # axes = fig.add_subplot(111)
        # axes.plot(x,y)

        # set up the figure and axes
        fig = plt.figure(figsize=(8, 3))
        ax1 = fig.add_subplot(121, projection='3d')
        ax2 = fig.add_subplot(122, projection='3d')

        # fake data
        _x = np.arange(4)
        _y = np.arange(5)
        _xx, _yy = np.meshgrid(_x, _y)
        x, y = _xx.ravel(), _yy.ravel()

        top = x + y
        bottom = np.zeros_like(top)
        width = depth = 1

        ax1.bar3d(x, y, bottom, width, depth, top, shade=True)
        ax1.set_title('Shaded')

        ax2.bar3d(x, y, bottom, width, depth, top, shade=False)
        ax2.set_title('Not Shaded')

        plt.show()
        return fig