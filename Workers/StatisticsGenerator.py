import pandas as pd
import numpy as np
from scipy import stats
from utils.StatEnum import StatType
import matplotlib
matplotlib.use('TkAgg')
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

class Generator:

    def prepare_json_data():
        df = pd.read_json(r'outputfiles\Data.json', orient=True)

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
                
    def calculate_stats(df, classification):
        cleanedDataFrame = Generator.clean_data(df)
        match classification:
            case StatType.MEAN:
                return np.mean(cleanedDataFrame)
            case StatType.MODE:
                return stats.mode(cleanedDataFrame)
            case StatType.MEDIAN:
                return np.median(cleanedDataFrame)

    def filter_data_by_powr(df, val):
        return df[(df.Powr > val)]
    
    def filter_data_by_start(df, val):
        return df[(df.Start >= val)]

    def clean_data(df):
        cirafZonesDf = (df['CirafZones']).to_frame()
        cirafZonesDf["Result"] = cirafZonesDf["CirafZones"].str.isnumeric().apply(lambda x: "No" if x == False else "Yes")
        dataToErasedf = cirafZonesDf[(cirafZonesDf['Result'] == 'No')].index
        cirafZonesDf.drop(dataToErasedf, inplace=True)
        cirafZonesDf = cirafZonesDf[cirafZonesDf.columns.drop('Result')]

        return cirafZonesDf['CirafZones'].astype(float)

    def clean_data_for_plotting(df):
        df["Result"] = df["CirafZones"].str.isnumeric().apply(lambda x: "No" if x == False else "Yes")
        dataToErasedf = df[(df['Result'] == 'No')].index
        df.drop(dataToErasedf, inplace=True)
        df = df[df.columns.drop('Result')]
        df['CirafZones'] = df['CirafZones'].astype(float)
        
        return df
    
    def flatten(js):
        return pd.DataFrame(js).squeeze()
    
    def generate_graph(df):
        # Clean the data to have 
        cleanedDataFrame = Generator.clean_data_for_plotting(df)
        
        dfForPlotting = cleanedDataFrame.groupby(['Freq', 'BroadcasterCode', 'LanguageCode', 'CirafZones'])['Days'].sum().reset_index().rename(columns={'Days':'SummedDays'})
        dfForPlotting['Grouped'] = dfForPlotting['Freq'].astype(str)  + ' ' + dfForPlotting['BroadcasterCode'] + ' ' + dfForPlotting['LanguageCode'] + ' ' + dfForPlotting['CirafZones'].astype(str)
        dfForPlotting = dfForPlotting[dfForPlotting.columns.drop(['Freq', 'BroadcasterCode', 'LanguageCode', 'CirafZones'])]

        np.random.seed(19680801)

        fig, ax = plt.subplots()
        groupedFreqAndCiraf = tuple(dfForPlotting.Grouped)

        y_pos = np.arange(len(groupedFreqAndCiraf))
        summedDays = dfForPlotting['SummedDays'].values
        
        error = np.random.rand(len(groupedFreqAndCiraf))

        ax.barh(y_pos, summedDays, xerr=error, align='center')
        ax.set_yticks(y_pos, labels=groupedFreqAndCiraf)
        ax.invert_yaxis() 

        ax.set_xlabel('Summed Days')
        ax.set_title('Days for instances of shortwave frequencies grouped by: Freq, BroadcasterCode, LanguageCode & CirafZones')

        plt.show()
        return fig
        
    def generate_correlation(df):
        # Clean the data to have 
        cleanedDataFrame = Generator.clean_data_for_plotting(df)

        dfForPlotting = cleanedDataFrame.filter(['Freq','CirafZones'], axis=1)

        print(dfForPlotting)

        # plot the data
        figure, ax = plt.subplots()
        sns.heatmap(dfForPlotting.corr(), annot=True, square=True, cbar=True, ax=ax)

        cor = dfForPlotting['Freq'].corr(df['CirafZones'])
        print(f'The correlation coeficient is: {cor}')

        plt.show()        
        return figure