import os
import pandas as pd
from shutil import copyfile

path = "C:\\Users\\UserName\\Desktop\\New folder"
file = "C:\\Users\\UserName\\Desktop\\Sample.xlsx"
for filename in os.listdir(path):
    name = filename.zfill(13)
    new_filename = name + ".jpg"


exceldata = pd.read_excel(file,sheetname="Sheet1")
exceldata["ID"] = exceldata["ID"].astype(str)
ids = exceldata["ID"].tolist()

for idnum in ids:
    paddednum = idnum.zfill(10)
    new_filename = paddednum + ".jpg"
    newimage = path + "\\Newimage.png"
    copyfile("C:\\Users\\UserName\\Desktop\\New folder\\No image available.png",newimage)
    os.rename(os.path.join(path, newimage), os.path.join(path, new_filename))