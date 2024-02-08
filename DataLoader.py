import pyodbc
import pandas as pd

class Loader:

    def LoadAdminData():
        conn = pyodbc.connect('DRIVER={SQL Server};'
                        'SERVER=localhost,1433;'
                        'DATABASE=RadioBroadcasts;'
                        'UID=sa;'
                        'PWD=DevMode2024')
        conn.setdecoding(pyodbc.SQL_CHAR, encoding='latin1')
        conn.setencoding('latin1')
        # cursor = conn.cursor()
        query = "SELECT * FROM [dbo].[TBL_ADMIN];"
        df = pd.read_sql(query, conn)
        
        print(df)
        return