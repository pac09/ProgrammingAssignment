import pyodbc
import pandas as pd

class Loader:

    def LoadAdminData(directoryName, fileName, sqlTable):
        # Some other example server values are
        # server = 'localhost\sqlexpress' # for a named instance
        # server = 'myserver,port' # to specify an alternate port
        server = 'servername' 
        database = 'AdventureWorks' 
        username = 'yourusername' 
        password = 'databasename'  
        cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()
        # select 26 rows from SQL table to insert in dataframe.
        query = "SELECT [CountryRegionCode], [Name] FROM Person.CountryRegion;"
        df = pd.read_sql(query, cnxn)
        print(df.head(26))
        return