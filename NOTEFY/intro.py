from tkinter.ttk import Progressbar
from tkinter import *
from tkinter import ttk
import time
from PIL import Image, ImageTk
class Intro:
    def __init__(self) -> None:
        self.root = Tk()

        self.width_window=427
        self.height_window=250
        self.screen_width=self.root.winfo_screenwidth()
        self.screen_height=self.root.winfo_screenheight()
        self.x_coordinate=(self.screen_width/2)-(self.width_window/2)
        self.y_coordinate=(self.screen_height/2)-(self.height_window/2)
        self.root.geometry('%dx%d+%d+%d'%(self.width_window, self.height_window, self.x_coordinate, self.y_coordinate))
        self.root.overrideredirect(1)

        self.intro_bell = ImageTk.PhotoImage(Image.open("intro_icon.png").resize((116,108)))
        self.black_line = ImageTk.PhotoImage(Image.open("intro_black_line.png").resize((50,70)))
        self.brown_line = ImageTk.PhotoImage(Image.open("intro_brown_line.png").resize((80, 60)))
        self.black_line2 = ImageTk.PhotoImage(Image.open("intro_black_line.png").resize((110,70)))

        self.bar_style= ttk.Style()
        self.bar_style.theme_use('clam')
        self.bar_style.configure('red.horizontal.TProgressbar', foreground='black', background='black')
        self.progress=Progressbar(self.root, orient=HORIZONTAL, length=500, mode='determinate')
        self.splash_screen()
        self.root.mainloop()

    def loading_bar(self):    
        value=0
        for _ in range(100):
            self.progress['value']=value
            self.root.update_idletasks()
            time.sleep(0.03)
            value= value+1
        self.root.destroy()

    def splash_screen(self):
        self.progress.place(x=-10,y=235)
        Frame(self.root, width=427, height=241, bg='#D5A113').place(x=0, y=0)
        
        self.proceed_font= ('Calibri (Body)', 9)
        Button(self.root, width=15, height=1, text='GET NOTEFIED', font= self.proceed_font, command=self.loading_bar, border=0, bg='black', fg='white', activebackground='brown', activeforeground='white').place(x=158, y=200)
        
        self.title_font= ('Calibri (Body)', 42, 'bold')

        Label(self.root, text='NOTEFY', fg='black', bg='#D5A113', font=self.title_font).place(x=40, y=80)
        Label(self.root, image=self.intro_bell, border=0, bg='#D5A113').place(x=285, y=46)
        Label(self.root, image=self.black_line, border=0, bg='#D5A113', height=15).place(x=45, y=46) 
        Label(self.root, image=self.brown_line, border=0, bg='#D5A113', height=13).place(x=45, y=56)
        Label(self.root, image=self.black_line2, border=0, bg='#D5A113', height=15).place(x=45, y=70)
        tagline_font= ('Arial', 11)    
        Label(self.root, text="Note em' all down to never miss an event!", fg='black', bg='#D5A113', font=tagline_font).place(x=44, y=140)