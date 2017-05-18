from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror
from tkinter import messagebox
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os 
from datetime import date


class Scraper:
    def __init__(self, master):
        self.master = master
        master.title("Image Scraper")

        self.message = "Please select an Excel file to import."
        self.label_text = StringVar()
        self.label_text.set(self.message)
        self.label = Label(master, textvariable=self.label_text)
        self.label.pack()
        
        menubar = Menu(root)
        menu_file = Menu(menubar, tearoff=False)
        menu_help = Menu(menubar, tearoff=False)
        menubar.add_cascade(menu=menu_file, label='File')
        menubar.add_cascade(menu=menu_help, label='Help')
        menu_file.add_command(label="Open", command=self.load_file)
        menu_file.add_command(label="Quit", command=self.on_closing)
        menu_help.add_command(label="Help", command=self.help_text)
        menu_help.add_command(label="About", command=self.about_text)
        root.config(menu=menubar)
        
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            root.destroy()
            
    def help_text(self):
        top = Toplevel()
        top.title("Help")
        msg = Message(top, text="""Here are some tips to avoid errors: \n
-The Excel file must contain the following sheets: "Sheet" \n
-Sheet and column names are case sensitive \n""")
        msg.pack()
        button = Button(top, text="Close", command=top.destroy)
        button.pack()
        
    def about_text(self):
        top = Toplevel()
        top.title("About")
        msg = Message(top, text="Made by noob programmer \n Christelle Williams.")
        msg.pack(fill=X)
        button = Button(top, text="Close", command=top.destroy)
        button.pack()
        
    
    def load_file(self):
        file = askopenfilename(filetypes=(("Excel files", "*.xlsx"),
                                           ("All files", "*.*") ))
        if file:
            try:
                self.message = "Running..."
                self.label_text.set(self.message)
                savedir = askdirectory()
                if savedir == "":
                    self.message = "Error. Please try again."
                    self.label_text.set(self.message)
                    showerror("Folder Save Error", "Failed to save")
                    return
                
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
                    with open(savedir + "\\" + screen_name + '.jpg', 'wb') as handler:
                        handler.write(img_data)
                    x = x + 1
                self.message = "Complete"
                self.label_text.set(self.message)

            except:
                self.message = "Error. Please try again."
                self.label_text.set(self.message)
                showerror("Open Excel File", "Failed to import file\n'%s'" % file)
            return
                    
                    
root=Tk()
my_gui = Scraper(root)
root.mainloop()