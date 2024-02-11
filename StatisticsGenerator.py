import pandas as pd
import numpy as np
from scipy import stats
from StatEnum import StatType

class Generator:

    def PrepareJsonData():
        df = pd.read_json(r'Output\Data.json', orient=True)

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
    