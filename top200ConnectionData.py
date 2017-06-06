#this code takes a large dataset and finds the profiles that are ranked in the top 200, then adds the connection data for the top 200 profiles to a new Excel sheet

import pandas as pd
import numpy as np

#import data from Excel
connectionData = pd.read_excel("C:\\Users\\UserName\\Desktop\\ConnectionDataFull.xlsx",sheetname="Sheet1")
profileData = pd.read_excel("C:\\Users\\UserName\\Desktop\\top200Profiles.xlsx", sheetname="Sheet1",parse_cols="A,B,C")

#create a list for IDs
topIDs = profileData["voxx_id"].tolist()
#create a dictionary that matches ID with name
dictionary = profileData.set_index("voxx_id")["name"].to_dict()

#create a blank list
rowData = []

#finds the IDs in the connectionData DataFrame that are also in the topID list
for index, row in connectionData.iterrows():
    for i in topIDs:
            #checks if there is a match in either the source or target columns
            if row.iloc[0] == i or row.iloc[1] == i:
                rowInfo = row.iloc[0],row.iloc[1],row.iloc[2]
                #if it is not a duplicate, add to the rowData list
                if rowInfo not in rowData:
                    rowData.append(rowInfo)

#create a new DataFrame
columns = ["sourceVoxxID","targetVoxxID","origin"]
data = pd.DataFrame.from_records(rowData, columns=columns)

#add blank columns to the new DataFrame
data.insert(1,"source",np.nan)
data.insert(3,"target",np.nan)

#adds names for the sourceID column data
x = 0
for row1 in data["sourceVoxxID"]:
    for k, v in dictionary.items():
        if row1 == k:
            data["source"].iloc[x] = v
    x = x + 1

#adds names for the targetID column data
y = 0
for row2 in data["targetVoxxID"]:
    for k, v in dictionary.items():
        if row2 == k:
            data["target"].iloc[y] = v
    y = y + 1

#adds the DataFrame to a new Excel sheet
data.to_excel("C:\\Users\\UserName\\Desktop\\top200RankData.xlsx", index=False, sheet_name="top200Data")
