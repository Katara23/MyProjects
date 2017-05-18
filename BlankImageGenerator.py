from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror
from tkinter import messagebox
import os
import pandas as pd
from shutil import copyfile

class BlankImageGen:
    def __init__(self, master):
        self.master = master
        master.title("Image Generator")

        self.message = "Please select an Excel file to open."
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
        msg = Message(top, text="""There may be an error if the sheet in the Excel file does not have the default name "Sheet1".""")
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
                                           ("All files", "*.*") ),
                                           title = "Select an Excel file")
        if file:
            try:
                self.message = "Running..."
                self.label_text.set(self.message)
                
                noimage = askopenfilename(title = "Select an image file to duplicate")
                if noimage == "":
                    self.message = "Error. Please try again."
                    self.label_text.set(self.message)
                    showerror("Open Image File", "Failed to open file")
                    return
                
                path = askdirectory(title = "Select a directory")
                if path == "":
                    self.message = "Error. Please try again."
                    self.label_text.set(self.message)
                    showerror("Select Directory", "Failed to select directory")
                    return
                
                exceldata = pd.read_excel(file,sheetname="Sheet1")
                exceldata["ID"] = exceldata["ID"].astype(str)
                ids = exceldata["ID"].tolist()
                for idnum in ids:
                    paddednum = idnum.zfill(10)
                    new_filename = paddednum + ".jpg"
                    newimage = path + "\\Newimage.png"
                    copyfile(noimage,newimage)
                    os.rename(os.path.join(path, newimage), os.path.join(path, new_filename))
                self.message = "Complete"
                self.label_text.set(self.message)
            except:
                self.message = "Error. Please try again."
                self.label_text.set(self.message)
            return
         
root=Tk()
my_gui = BlankImageGen(root)
root.mainloop()