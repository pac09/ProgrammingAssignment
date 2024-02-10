import pyodbc

class Generator:

    def PrepareData():
    
        return


# CirafZones
# cirafZonesDf = (finaldataFrame['CirafZones']).to_frame()

# cirafZonesDf["Result"] = cirafZonesDf["CirafZones"].str.isnumeric().apply(lambda x: "No" if x == False else "Yes")

# print(cirafZonesDf)

# dataToErasedf = cirafZonesDf[(cirafZonesDf['Result'] == 'No')].index
# cirafZonesDf.drop(dataToErasedf, inplace=True)
# cirafZonesDf = cirafZonesDf[cirafZonesDf.columns.drop('Result')]

# print(cirafZonesDf)
