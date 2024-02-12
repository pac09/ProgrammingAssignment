import csv
import pyodbc
import os
from utils.ServerCredentials import Credentials

class ImportWorker:

    def database_clean_up():    
        # Set up the SQL Server connection
        conn = pyodbc.connect(f'DRIVER=SQL Server;SERVER={Credentials._server};DATABASE={Credentials._database};UID={Credentials._user};PWD={Credentials._password}')

        cursor = conn.cursor()
        cleanupStoredProcedure = 'EXEC [dbo].[TablesCleanUp]'
        cursor.execute(cleanupStoredProcedure)
        cursor.commit()
        return 
    
    def generic_import(directoryName, fileName, sqlTable):
        format = 'csv'

        # Opens and reads the file in the directory
        with open(os.path.join(directoryName, fileName + "." + format), 'r', encoding="unicode_escape") as f:
            # Set up the SQL Server connection
            conn = pyodbc.connect(f'DRIVER=SQL Server;SERVER={Credentials._server};DATABASE={Credentials._database};UID={Credentials._user};PWD={Credentials._password}')
            conn.setdecoding(pyodbc.SQL_CHAR, encoding=Credentials._encoding)
            conn.setencoding(Credentials._encoding)

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
                ImportWorker.escape_language_commas(data, fileName)
                cursor.execute(query, data)

            cursor.commit()
                                
            # Commit the transaction and close the connection
            conn.commit()
            conn.close()
            return
        
    def escape_language_commas(data, fileName):
        if(len(data) == 3 and fileName == 'LANGUAGE'):
            data[0] = data[0]
            data[1] = data[1] + data[2]
            data[2] = ''
            data.remove('')
            
        return data
    
    def import_admin(directoryName):
        fileName = 'ADMIN'
        sqlTable = '[dbo].[TBL_ADMIN]'

        ImportWorker.generic_import(directoryName, fileName, sqlTable)
        return
    
    def import_ant(directoryName):
        fileName = 'ANT'
        sqlTable = '[dbo].[TBL_ANT]'

        ImportWorker.generic_import(directoryName, fileName, sqlTable)
        return
    
    def import_broadcaster(directoryName):
        fileName = 'BROADCASTER'
        sqlTable = '[dbo].[TBL_BROADCASTER]'

        ImportWorker.generic_import(directoryName, fileName, sqlTable)
        return

    def import_hf_schedule(directoryName):
        fileName = 'HF_SCHEDULE'
        sqlTable = '[dbo].[TBL_HF_SCHEDULE]'

        ImportWorker.generic_import(directoryName, fileName, sqlTable)
        return

    def import_language(directoryName):
        fileName = 'LANGUAGE'
        sqlTable = '[dbo].[TBL_LANGUAGE]'

        ImportWorker.generic_import(directoryName, fileName, sqlTable)
        return

    def import_location(directoryName):
        fileName = 'LOCATION'
        sqlTable = '[dbo].[TBL_LOCATION]'

        ImportWorker.generic_import(directoryName, fileName, sqlTable)
        return