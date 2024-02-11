import csv
import pyodbc
import os
from Utils.ServerCredentials import Credentials

class ImportWorker:

    def databaseCleanUp():    
        # Set up the SQL Server connection
        conn = pyodbc.connect(f'DRIVER=SQL Server;SERVER={Credentials.server};DATABASE={Credentials.database};UID={Credentials.user};PWD={Credentials.password}')

        cursor = conn.cursor()
        cleanupStoredProcedure = 'EXEC [dbo].[TablesCleanUp]'
        cursor.execute(cleanupStoredProcedure)
        cursor.commit()
        return 
    
    def genericImport(directoryName, fileName, sqlTable):
        format = 'csv'

        # Opens and reads the file in the directory
        with open(os.path.join(directoryName, fileName + "." + format), 'r', encoding="unicode_escape") as f:
            # Set up the SQL Server connection
            conn = pyodbc.connect(f'DRIVER=SQL Server;SERVER={Credentials.server};DATABASE={Credentials.database};UID={Credentials.user};PWD={Credentials.password}')
            conn.setdecoding(pyodbc.SQL_CHAR, encoding=Credentials.encoding)
            conn.setencoding(Credentials.encoding)

            reader = csv.reader(f, delimiter=',')
            columns = next(reader) 
            
            # Tentativo
            cleanedColumns = [x.replace(' ','') for x in columns]

            # Cleans up the last added Empty string element in the List if there was a delimiter at the end of line
            cleanedColumns = list(filter(None, cleanedColumns))

            query = f'INSERT INTO {sqlTable}' + '({0}) VALUES ({1})'
            query = query.format(','.join(cleanedColumns), ','.join('?' * len(cleanedColumns)))
            
            cursor = conn.cursor()

            for data in reader:
                ImportWorker.escapeLanguageCommas(data, fileName)
                cursor.execute(query, data)

            cursor.commit()
                                
            # Commit the transaction and close the connection
            conn.commit()
            conn.close()
            return
        
    def escapeLanguageCommas(data, fileName):
        if(len(data) == 3 and fileName == 'LANGUAGE'):
            data[0] = data[0]
            data[1] = data[1] + data[2]
            data[2] = ''
            data.remove('')
            
        return data
    
    def importAdmin(directoryName):
        fileName = 'ADMIN'
        sqlTable = '[dbo].[TBL_ADMIN]'

        ImportWorker.genericImport(directoryName, fileName, sqlTable)
        return
    
    def importAnt(directoryName):
        fileName = 'ANT'
        sqlTable = '[dbo].[TBL_ANT]'

        ImportWorker.genericImport(directoryName, fileName, sqlTable)
        return
    
    def importBroadcaster(directoryName):
        fileName = 'BROADCASTER'
        sqlTable = '[dbo].[TBL_BROADCASTER]'

        ImportWorker.genericImport(directoryName, fileName, sqlTable)
        return

    def importHfSchedule(directoryName):
        fileName = 'HF_SCHEDULE'
        sqlTable = '[dbo].[TBL_HF_SCHEDULE]'

        ImportWorker.genericImport(directoryName, fileName, sqlTable)
        return

    def importLanguage(directoryName):
        fileName = 'LANGUAGE'
        sqlTable = '[dbo].[TBL_LANGUAGE]'

        ImportWorker.genericImport(directoryName, fileName, sqlTable)
        return

    def importLocation(directoryName):
        fileName = 'LOCATION'
        sqlTable = '[dbo].[TBL_LOCATION]'

        ImportWorker.genericImport(directoryName, fileName, sqlTable)
        return