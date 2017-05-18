import pandas as pd
import requests
from bs4 import BeautifulSoup

data = pd.read_excel("C:\\Users\\UserName\\Desktop\\Sample.xlsx",sheetname="Sheet") 
results = pd.DataFrame(columns=["ID","Name","OtherID","Topic","URL","Articles"])
                
#create keyword/search terms DataFrame
keywords = pd.read_excel("C:\\Users\\UserName\\Desktop\\Sample.xlsx",sheetname="Keywords")
keywords_list = keywords["Keywords"].tolist()
#keywords_list = keywords["Keywords"].astype(str)
data["Search Name"] = data["First"] + "+" + data["Last"]
data["Name"] = data["First"] + " " + data["Last"]
name_list = data["Name"].tolist()
                
#create urls for each name and search terms
x = 0
n = 0
for sn in data["Search Name"]:
    name = name_list[n]
    for keyword in keywords_list:
        url = "https://www.ncbi.nlm.nih.gov/pubmed/?term=" + sn + "+" + "AND" + "+" + keyword
        results.loc[x] = ["",name,"",keyword,url,""]
        x = x + 1
    n = n + 1
                
#create dictionary for IDs
id = data["ID"].tolist()
id_column = {}
for i, name in enumerate(name_list):
    id_column[name] = id[i]
                
#add IDs to DataFrame
y = 0
for name in results["Name"]:
    for k, v in id_column.items():
        if results["Name"].iloc[y] == k:
            results["ID"].iloc[y] = v
    y = y + 1
                
#create dictionary for OtherIDs
otherid = data["OtherID"].tolist()
otherid_column = {}
for i, name in enumerate(name_list):
    otherid_column[name] = otherid[i]
                
#add OtherIDs to DataFrame
z = 0
for name in results["Name"]:
    for k, v in otherid_column.items():
        if results["Name"].iloc[z] == k:
            results["OtherID"].iloc[z] = v
    z = z + 1
                
#grab article number for each url
count = 0
for url in results["URL"]:
    r = requests.get(url)
    content = r.content
    parser = BeautifulSoup(content, "html.parser")
    article_number = parser.find("input", {"id": "resultcount"}).attrs["value"]
    results["Articles"].iloc[count] = article_number
    count = count + 1
                
#convert Number of Articles to int
results["Articles"] = results["Articles"].astype(int)

results.to_excel("C:\\Users\\UserName\\Desktop\\Results.xlsx", index=False, sheet_name="Results")