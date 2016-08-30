from tkinter import Tk, Menu, BOTH
from tkinter.ttk import Frame, Button, Style
from PIL import Image, ImageTk


class Application(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        
        
    def initUI(self):
        
        self.parent.title("Label Generator")
        self.style = Style()
        self.style.theme_use("clam")

        self.pack(fill=BOTH, expand=1)
        '''
        quitButton = Button(self, text="Quit",
            command=self.quit)
        quitButton.place(x=50, y=50)
        '''
        
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        
        fileMenu = Menu(menubar)       
        
        fileMenu.add_command(label="New", underline=0)
        fileMenu.add_command(label="Open", underline=0)
        fileMenu.add_command(label="Save", underline=0)
        '''
        submenu = Menu(fileMenu)
        submenu.add_command(label="New feed")
        submenu.add_command(label="Bookmarks")
        submenu.add_command(label="Mail")
        fileMenu.add_cascade(label='Import', menu=submenu, underline=0)
        '''
        fileMenu.add_separator()
        
        fileMenu.add_command(label="Exit", underline=0, command=self.onExit)
        menubar.add_cascade(label="File", underline=0, menu=fileMenu)
        
        editMenu = Menu(menubar)
        menubar.add_cascade(label="Edit", underline=0, menu=editMenu)
        
        settingsMenu = Menu(menubar)
        menubar.add_cascade(label="Options", underline=0, menu=settingsMenu)
        
        runMenu = Menu(menubar)
        menubar.add_cascade(label="Run", underline=0, menu=runMenu)
        
        helpMenu = Menu(menubar)
        menubar.add_cascade(label="Help", underline=0, menu=helpMenu)
        
        
        
    def onExit(self):
        self.quit()

def main():
  
    root = Tk()
    root.geometry("800x1000")
    
    app = Application(root)
    root.mainloop()  
    
if __name__ == '__main__':
    main()  

'''
import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
'''
