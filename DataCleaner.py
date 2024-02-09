import pyodbc
import pandas as pd
import gc


class Cleaner:

    def CleanData():
        conn = pyodbc.connect('DRIVER={SQL Server};'
                        'SERVER=localhost,1433;'
                        'DATABASE=RadioBroadcasts;'
                        'UID=sa;'
                        'PWD=DevMode2024')
        conn.setdecoding(pyodbc.SQL_CHAR, encoding='latin1')
        conn.setencoding('latin1')

        # Removes 'BROADCASTER' code: ADM, DWL or KBS
        broadcasterQuery = "SELECT * FROM [dbo].[TBL_BROADCASTER];"
        broadcasterDf = pd.read_sql(broadcasterQuery, conn)
        shortwaveRadioCodesData = broadcasterDf[(broadcasterDf['Code'] == 'ADM') | (broadcasterDf['Code'] == 'DWL') | (broadcasterDf['Code'] == 'KBS')].index
        broadcasterDf.drop(shortwaveRadioCodesData, inplace=True)

        # Reshape 'FREQ' ... Extract this out for each instance of frequencies: 5890MHz, 6040MHz, 7220MHz, 9490MHz, 9510MHz
        scheduleQuery = "SELECT * FROM [dbo].[TBL_HF_SCHEDULE] WHERE Freq = '5890' OR Freq = '6040' OR Freq = '7220' OR Freq = '9490' OR Freq = '9510';"
        scheduleDf = pd.read_sql(scheduleQuery, conn)

        # Joins data frames between BROADCASTER and HF_SCHEDULE
        mergedDf = pd.merge(scheduleDf, broadcasterDf, left_on='BroadcasterCode', right_on='Code')
        
        # Drop Columns from BROADCASTER
        mergedDf = mergedDf[mergedDf.columns.drop('TblBroadcasterId')]
        mergedDf = mergedDf[mergedDf.columns.drop('Code')]

        # Load data from 'ADMIN'
        adminQuery = "SELECT * FROM [dbo].[TBL_ADMIN];"
        adminDf = pd.read_sql(adminQuery, conn)

        # Joins data frames between 'mergedDataFramev1' and ADMIN
        mergeDf2 = pd.merge(mergedDf, adminDf, left_on='AdminCode', right_on='Code')

        # Drop Columns from 'ADMIN'
        mergeDf2 = mergeDf2[mergeDf2.columns.drop('TblAdminId')]
        mergeDf2 = mergeDf2[mergeDf2.columns.drop('Code')]

        # Load data from 'LANGUAGE'
        languageQuery = "SELECT * FROM [dbo].[TBL_LANGUAGE];"
        languageDf = pd.read_sql(languageQuery, conn)

        # Joins data frames between 'mergedDataFramev2' and LANGUAGE
        mergeDf3 = pd.merge(mergeDf2, languageDf, left_on='LanguageCode', right_on='Code')
        
        # Drop Columns from 'ADMIN'
        mergeDf3 = mergeDf3[mergeDf3.columns.drop('TblLanguageId')]
        mergeDf3 = mergeDf3[mergeDf3.columns.drop('Code')]

        # Load data from 'ANT'
        antQuery = "SELECT * FROM [dbo].[TBL_ANT];"
        antDf = pd.read_sql(antQuery, conn)

        # Joins data frames between 'mergedDataFramev3' and ANT
        mergeDf4 = pd.merge(mergeDf3, antDf, left_on='AntCode', right_on='Code')

        # Drop Columns from 'ADMIN'
        mergeDf4 = mergeDf4[mergeDf4.columns.drop('TblAntId')]
        mergeDf4 = mergeDf4[mergeDf4.columns.drop('Code')]

        # Load data from 'LOCATION'
        locationQuery = "SELECT * FROM [dbo].[TBL_LOCATION];"
        locationDf = pd.read_sql(locationQuery, conn)

        # Joins data frames between 'mergedDataFramev4' and LOCATION
        finaldataFrame = pd.merge(mergeDf4, locationDf, left_on='LocCode', right_on='Code')

        # Drop Columns from 'LOCATION'
        finaldataFrame = finaldataFrame[finaldataFrame.columns.drop('TblLocationId')]
        finaldataFrame = finaldataFrame[finaldataFrame.columns.drop('Code')]

        # Deleting DataFrames to release memory
        del [[broadcasterDf, scheduleDf, mergedDf, adminDf, mergeDf2, languageDf, mergeDf3, antDf, mergeDf4, locationDf]]
        gc.collect()
        broadcasterDf = pd.DataFrame()
        scheduleDf = pd.DataFrame()
        mergedDf = pd.DataFrame()
        adminDf = pd.DataFrame()
        mergeDf2 = pd.DataFrame()
        languageDf = pd.DataFrame()
        mergeDf3 = pd.DataFrame()
        antDf = pd.DataFrame()
        mergeDf4 = pd.DataFrame()
        locationDf = pd.DataFrame()

        finaldataFrame.rename({'Ant': 'Antenna Type', 'Site': 'Transmitter'}, axis=1, inplace=True)

        print(finaldataFrame[['Freq', 'Start', 'Stop', 'CirafZones', 'Powr', 'AziMuth', 'Slew', 'Days', 'Sdate', 'Edate', 'Mod', 'Afrq', 'FmoCode', 'BroadcasterCode', 'Broadcaster', 'AdminCode', 'AdminName', 'LanguageCode', 'Language', 'AntCode', 'Antenna Type', 'LocCode', 'Transmitter', 'Adm', 'Lat', 'Long']])

        return