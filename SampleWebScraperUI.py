from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import showerror
from tkinter import messagebox
import pandas as pd
import requests
from bs4 import BeautifulSoup

class MeshTerms:
    def __init__(self, master):
        self.master = master
        master.title("Web Scraper")

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
-The Excel file must contain the following sheets: "Sheet" and "Keywords" \n
-Make sure the "Sheet" contains the following columns: "First", "Last", "ID", and "OtherID" \n
-Make sure the "Keywords" sheet contains the column "Keywords" \n
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
                savefile = asksaveasfilename(filetypes=(("Excel files", "*.xlsx"),
                                                          ("All files", "*.*") ))
                if savefile == "":
                    self.message = "Error. Please try again."
                    self.label_text.set(self.message)
                    showerror("File Save Error", "Failed to save file")
                    return
                #Web scraper
                data = pd.read_excel(file,sheetname="Sheet") 
                results = pd.DataFrame(columns=["ID","Name","OtherID","Topic","URL","Articles"])
                
                #create keyword/search terms DataFrame
                keywords = pd.read_excel(file,sheetname="Keywords")
                keywords_list = keywords["Keywords"].tolist()
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
                
                #create dictionary for CRMIDs
                crmid = data["OtherID"].tolist()
                crmid_column = {}
                for i, name in enumerate(name_list):
                    crmid_column[name] = crmid[i]
                
                #add CRMIDs to DataFrame
                z = 0
                for name in results["Name"]:
                    for k, v in crmid_column.items():
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

                results.to_excel(savefile + ".xlsx", index=False, sheet_name="Results")         
                self.message = "Complete"
                self.label_text.set(self.message)
            except:
                self.message = "Error. Please try again."
                self.label_text.set(self.message)
                showerror("Open Excel File", "Failed to import file\n'%s'" % file)
            return

root=Tk()
my_gui = MeshTerms(root)
root.mainloop()