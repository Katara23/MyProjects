import os 
import pandas as pd
import requests
from datetime import date

dir_path = os.path.dirname(os.path.realpath(__file__))

file = dir_path + "\\Sample.xlsx"
date = date.today().strftime("%b %d ")
new_folder = dir_path + "\\" + date + "User Profile Images"
try:
    os.makedirs(new_folder)
except OSError:
    pass

data = pd.read_excel(file,sheetname="Sheet")
column_names = ["user_id","user_profile_image_url"]
data = data.loc[:,column_names]

data["user_id"] = data["user_id"].astype(str)
z = 0
for idnum in data["user_id"]:
    paddedidnum = idnum.zfill(18)
    data["user_id"].iloc[z] = paddedidnum
    z = z + 1

y = 0
for s in data["user_profile_image_url"]:
    new_str = s.replace("_normal","")
    data["user_profile_image_url"].iloc[y] = new_str
    y = y + 1
    
x = 0
for i in data["user_profile_image_url"]:
    screen_name = data["user_id"].iloc[x]
    img_data = requests.get(i).content
    with open(new_folder + "\\" + screen_name + '.jpg', 'wb') as handler:
        handler.write(img_data)
    x = x + 1