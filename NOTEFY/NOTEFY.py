# could have made a general class for the main frame
# and a class for each page (Add Note page, Notes/Events page)
# so we don't have a huge chunk of code that is hard to read, maintain, and revise
# there's also too many dependencies

from tkinter import *
from PIL import Image, ImageTk
from tkcalendar import *
from datetime import datetime
import sqlite3, pygame, threading, time, webbrowser, os
from tkinter import filedialog
from tkinter import ttk
import babel.numbers, speech_recognition, cv2, intro
from pytesseract import *
from tkinter import font
from plyer import notification
from abc import ABC, abstractmethod
pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class Notefy(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.root = Tk()
        self.root.geometry ('700x550+405+120')
        self.root.overrideredirect(True)
        self.root.config(bg="#f0f0f0")
        #images
        # img to text icon
        self.img2text = ImageTk.PhotoImage(Image.open("image_text.png").resize((37,17)))
        # mic icon
        self.mic_icon = ImageTk.PhotoImage(Image.open("mic_icon.png").resize((22,18)))
        #ringtone icon
        self.ringtone_icon = ImageTk.PhotoImage(Image.open("ringtone_icon.png").resize((32,27)))
        #datetime icon
        self.datetime_icon = ImageTk.PhotoImage(Image.open("Datetime_icon.png").resize((32,27)))
        # manual title
        self.light_manual_title = ImageTk.PhotoImage(Image.open("light_manual_title.png").resize((75,20)))
        self.dark_manual_title = ImageTk.PhotoImage(Image.open("dark_manual_title.png").resize((75,20)))
        #events bar title
        self.light_events_title = ImageTk.PhotoImage(Image.open("events_title.png").resize((75,20)))
        self.dark_events_title = ImageTk.PhotoImage(Image.open("dark_events_title.png").resize((75,20)))
        #notes bar title
        self.light_notes_title = ImageTk.PhotoImage(Image.open("notes_title.png").resize((70,20)))
        self.dark_notes_title = ImageTk.PhotoImage(Image.open("dark_notes_title.png").resize((70,20)))
        # trash title
        self.light_trash_title = ImageTk.PhotoImage(Image.open("trash_title.png").resize((70,20)))
        self.dark_trash_title = ImageTk.PhotoImage(Image.open("dark_trash_title.png").resize((70,20)))
        # abouts tittle
        self.light_about_title = ImageTk.PhotoImage(Image.open("about_title.png").resize((70,20)))
        self.dark_about_title= ImageTk.PhotoImage(Image.open("dark_about_title.png").resize((70,20)))
        # hamb menu title
        self.light_menu_title = ImageTk.PhotoImage(Image.open("menu_title.png").resize((65,25)))
        self.dark_menu_title = ImageTk.PhotoImage(Image.open("dark_menu_title.png").resize((65,25)))
        #hamburger button
        self.light_hamburger = ImageTk.PhotoImage(Image.open("hamburger.png").resize((48,25)))
        self.dark_hamburger = ImageTk.PhotoImage(Image.open("dark_hamburger.png").resize((48,25)))
        # hamb menu footer
        self.hamb_label = ImageTk.PhotoImage(Image.open("ham_label.png").resize((180,25)))
        # light top bar
        self.light_top_bar = Image.open("upper_bar.png").resize((686,40))
        self.light_top_bar = ImageTk.PhotoImage(self.light_top_bar)
        # dark top bar
        self.dark_top_bar = ImageTk.PhotoImage(Image.open("dark_upper_bar.png").resize((686,40)))
        # add button
        self.light_add_button = ImageTk.PhotoImage(Image.open("add_button.png").resize((60,60)))
        self.dark_add_button = ImageTk.PhotoImage(Image.open("dark_add_button.png").resize((60,60)))
        # delete/trash button
        self.trash = ImageTk.PhotoImage(Image.open("trash.png").resize((16,17)))
        # members' names
        self.light_members = ImageTk.PhotoImage(Image.open("members.png").resize((152,23)))
        self.dark_members = ImageTk.PhotoImage(Image.open("dark_members.png").resize((150,23)))
        # undo button
        self.undo_img = ImageTk.PhotoImage(Image.open("undo.png").resize((20,15)))
        # redo button
        self.redo_img = ImageTk.PhotoImage(Image.open("redo.png").resize((20,15)))
        # dark button frame
        self.dark_note_frame = ImageTk.PhotoImage(Image.open("dark_note_frame.png").resize((650,105)))
        # light button frame
        self.light_note_frame = ImageTk.PhotoImage(Image.open("data_frame.png").resize((650,105)))
        #light mode button
        self.on = ImageTk.PhotoImage(Image.open("light.png").resize((70, 30)))
        #dark mode button
        self.off = ImageTk.PhotoImage(Image.open("dark.png").resize((70, 30)))
        # restore button
        self.restore_bttn = ImageTk.PhotoImage(Image.open("restore.png").resize((18,13)))
        # x / remove button for note event
        self.close = ImageTk.PhotoImage(Image.open("close.png").resize((18,15)))
        # back button
        self.back_button = ImageTk.PhotoImage(Image.open("back_button.png").resize((23,13)))
        # about image
        self.light_about = ImageTk.PhotoImage(Image.open("about.png").resize((660,430)))
        self.dark_about = ImageTk.PhotoImage(Image.open("dark_about.png").resize((660,430)))
        # main frame image
        self.dark_main_frame = ImageTk.PhotoImage(Image.open("dark_main_frame.png").resize((660,430)))
        self.light_main_frame = ImageTk.PhotoImage(Image.open("light_main_frame.png").resize((660,430)))
        #------------------------
        self.connector = sqlite3.connect("Notes.db", check_same_thread=False, isolation_level=None)
        self.cursor = self.connector.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Notes (
                            title text,
                            notes text,
                            schedule text,
                            ringtone text,
                            last_edit text)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Trash (
                            title text,
                            notes text,
                            schedule text,
                            ringtone text,
                            last_edit text)""")
    @abstractmethod
    def display_notes(self):
        pass
    @abstractmethod
    def display_notif_pop_up(self):
        pass
    @abstractmethod
    def change_theme(self):
        pass
    @abstractmethod
    def display_digital_clock(self):
        pass
    @abstractmethod
    def close_notif_window(self):
        pass
    @abstractmethod
    def back_to_mainWindow(self):
        pass
    @abstractmethod
    def open_addNote_frame(self):
        pass
    @abstractmethod
    def open_ringtone_picker(self):
        pass
    @abstractmethod
    def open_img2text_frame(self):
        pass
    @abstractmethod
    def pick_ringtone(self):
        pass
    @abstractmethod
    def pick_image(self):
        pass
    @abstractmethod
    def open_schedPicker_frame(self):
        pass
    @abstractmethod
    def open_hamb_menu(self):
        pass

class Main(Notefy):
    def __init__(self):
        intro.Intro()
        super().__init__()
        self.manual_title = self.light_manual_title
        self.about = self.light_about
        self.menu_title = self.light_menu_title
        self.hamburger = self.light_hamburger
        self.titleEntry_bg = "#DCDCDC"
        self.__event_sched = 'None'
        self.ringtone = "Default Notification"
        self.all_scheds = self.__get_schedules()
        self.note_imgFrame = self.light_note_frame
        self.frame_bg = "#f0f0f0"
        self.notes_bg = "#fafafa"
        self.add_button = self.light_add_button
        self.hambMenu_bg = "#DCDCDC"
        self.hamb_fg = "black"
        self.notes_fg = "black"
        self.scroll_back_color = "#DCDCDC"
        self.events_title = self.light_events_title
        self.notes_title  = self.light_notes_title
        self.about_title = self.light_about_title
        self.trash_title = self.light_trash_title
        self.notesTitle_fg = "#808080"

        self.__event_checker = threading.Thread(target=self.__check_for_reminder, daemon=True)
        self.__event_checker.start()

        # make a frame for the title bar
        self.title_bar = Frame(self.root, bg='goldenrod', relief='raised', bd=0)
        # put a close button on the title bar
        self.close_button = Button(self.title_bar, text='  ✖ ', bg="goldenrod", bd=0, fg="black", command=self.root.destroy, activebackground="goldenrod")
        #label for the title bar
        self.title_label = Label(self.title_bar, text=" 🔔 NOTEFY", font=("Arial Black",10) ,bg="goldenrod")
        self.title_label.pack(side=LEFT, pady=2)
        # pack the widgets
        self.title_bar.pack(expand=0, fill=BOTH)
        self.close_button.pack(side=RIGHT)
        # upper bar
        self.upper_bar = Label(self.root, image=self.light_top_bar, text="notes", border=0)
        self.upper_bar.place(x=5, y=35)
        self.page_title= Label(self.root, border=0, bg=self.hambMenu_bg)
        # lower bar
        self.lower_bar = Frame(self.root, width = 700, height = 31, bg = "#DCDCDC", highlightbackground="light gray", highlightthickness=0)
        self.lower_bar.place(x= 0, y=519)
        self.member_names = Label(self.lower_bar, image=self.light_members, border=0, bg = "#DCDCDC", height=19)
        self.member_names.place(x=27, y=6)
        #dark button
        self.theme_bttn = Button(self.root, image=self.on, bd=0, bg="#DCDCDC", activebackground="#E1E1E1", command=self.change_theme)
        self.theme_bttn.place(x=610, y=40)
        #clock
        self.time_label = Label(self.root, font=("Arial", 13), fg= "black", bg="#DCDCDC", bd=2)
        self.time_label.place(x=533, y=45)

        self.display_digital_clock()
        self.display_notes(for_notes = True)
        self.root.mainloop()        

    def display_notif_pop_up(self):
        self.splash_root = Toplevel(self.root)
        self.splash_root.geometry('275x115+620+300')
        self.splash_root.overrideredirect(True) # turns off title bar, geometry
        self.splash_root.config(bg="gray")

        # make a frame for the title bar
        self.splsh_title = Frame(self.splash_root, bg='goldenrod', relief='flat', bd=0)
        self.splshclose_button = Button(self.splsh_title, text='  ✖ ', bg="goldenrod", bd=0, fg="black", command=self.close_notif_window, activebackground="goldenrod")
        #label for the title bar
        self.splshtitle_labl = Label(self.splsh_title, text=" 🔔 ALARM", font=("Arial Black",10) ,bg="goldenrod")
        self.splshtitle_labl.pack(side=LEFT, pady=2)
        self.splshclose_button.pack(side=RIGHT)
        self.splsh_title.pack(expand=0, fill=BOTH)

    def close_notif_window(self):
        self.splash_root.destroy()
        try: pygame.mixer.music.stop()
        except Exception as e: print(e)

    def change_theme(self):
        if self.root.cget("bg") == "#f0f0f0":
            self.notesTitle_fg = "#ffffff"
            self.about = self.dark_about
            self.member_names.config(image=self.dark_members)
            self.hamburger = self.dark_hamburger
            self.menu_title = self.dark_menu_title
            # for titles
            self.manual_title = self.dark_manual_title
            self.notes_title = self.dark_notes_title
            self.trash_title = self.dark_trash_title
            self.events_title = self.dark_events_title
            self.about_title = self.dark_about_title
            #-----
            self.titleEntry_bg = "#64666b"
            self.scroll_back_color = "black"
            self.notes_fg = "#DCDCDC"
            self.hamb_fg = "#808080"
            self.hambMenu_bg = "#363636"
            self.add_button = self.dark_add_button
            self.member_names.config(bg="#363636")
            self.lower_bar.config(bg="#363636")
            self.frame_bg = "black"
            self.notes_bg = "#262626"
            self.theme_bttn.config(image=self.off, bg="#363636", activebackground="#363636")
            self.root.config(bg="black")
            self.notes_canvas.config(bg="black")
            self.notes_canvas.pack_forget()
            self.note_imgFrame = self.dark_note_frame
            self.upper_bar.config(image=self.dark_top_bar)
            self.time_label.config(bg="#363636", fg="goldenrod")
            if self.page_title.cget("text") == "notes": self.display_notes(for_notes=True)
            elif self.page_title.cget("text") == "trash": self.display_notes(for_trash=True)
            elif self.page_title.cget("text") == "manual": self.display_notes(for_manual=True, display_manual = False)
            elif self.page_title.cget("text") == "about": self.display_notes(for_about=True)
            else: self.display_notes()
        else:
            self.notesTitle_fg = "#808080"
            self.about = self.light_about
            self.member_names.config(image=self.light_members)
            self.menu_title = self.light_menu_title
            #for titles
            self.manual_title = self.light_manual_title
            self.hamburger = self.light_hamburger
            self.notes_title = self.light_notes_title
            self.trash_title = self.light_trash_title
            self.events_title = self.light_events_title
            self.about_title = self.light_about_title
            #-----------
            self.titleEntry_bg = "#DCDCDC"
            self.scroll_back_color = "#DCDCDC"
            self.notes_fg = "black"
            self.hamb_fg = "black"
            self.hambMenu_bg = "#DCDCDC"
            self.add_button = self.light_add_button
            self.member_names.config(bg="#DCDCDC")
            self.lower_bar.config(bg="#DCDCDC")
            self.frame_bg = "#f0f0f0"
            self.notes_bg = "#fafafa"
            self.note_imgFrame = self.light_note_frame
            self.theme_bttn.config(image=self.on, bg="#DCDCDC", activebackground="#DCDCDC")
            self.root.config(bg="#f0f0f0")
            self.notes_canvas.config(bg="#f0f0f0")
            self.notes_canvas.pack_forget()
            self.upper_bar.config(image=self.light_top_bar)
            self.time_label.config(bg="#DCDCDC", fg="black")
            if self.page_title.cget("text") == "notes": self.display_notes(for_notes=True)
            elif self.page_title.cget("text") == "trash": self.display_notes(for_trash=True)
            elif self.page_title.cget("text") == "manual": self.display_notes(for_manual=True, display_manual = False)
            elif self.page_title.cget("text") == "about": self.display_notes(for_about=True)
            else: self.display_notes()

    def display_digital_clock(self):
        time_var = time.strftime("%I:%M %p")
        self.time_label.config(text = time_var)
        self.time_label.after(200, self.display_digital_clock )

    def display_notes(self, for_notes = False, for_trash = False, for_about = False, for_manual = False, display_manual = True):
        self.theme_bttn["state"] = NORMAL
        if for_notes: self.page_title.config(image=self.notes_title, text="notes")
        elif for_trash: self.page_title.config(image=self.trash_title, text="trash")
        elif for_about: self.page_title.config(image=self.about_title, text="about")
        elif for_manual: self.page_title.config(image=self.manual_title, text="manual")
        else: self.page_title.config(image=self.events_title, text = "events")
        self.page_title.place(x=63, y=45)
        # this try block's purpose is solely to remove all widgets before displaying new ones
        try:
            self.scroll_bar.destroy()
            self.addNote_button.destroy()
            try: self.about_label.place_forget()
            except: pass
            try: self.delete_all_bttn.place_forget()
            except: pass
            try: self.main_frame_label.place_forget()
            except: pass
            self.notes_canvas.destroy()
            self.close_hamb_menu()
            for note in self.notes:
                note.destroy()
        except: pass

        # Notes canvas w/ scrollbar
        self.notes_canvas = Canvas(self.root,  highlightthickness=0, border=0, bd=0, borderwidth=0, highlightbackground=self.root.cget("bg"), highlightcolor=self.root.cget("bg"))
        self.notes_canvas.pack(side=LEFT, fill='both', expand="yes", pady=47)
        # Scroll bar
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure("Vertical.TScrollbar", background="goldenrod", darkcolor="#806000", lightcolor="black",
                troughcolor=self.scroll_back_color, bordercolor="#806000", arrowcolor="black")

        self.scroll_bar = ttk.Scrollbar(self.notes_canvas, command=self.notes_canvas.yview)
        self.scroll_bar.pack(side=RIGHT, fill=Y, pady=3)

        self.notes_canvas.configure(yscrollcommand=self.scroll_bar.set)
        self.notes_canvas.bind('<Configure>', lambda e: self.notes_canvas.configure(scrollregion=self.notes_canvas.bbox('all')))
        self.notes_canvas.bind_all('<MouseWheel>', lambda event: self.notes_canvas.yview('scroll', int(-2*(event.delta/120)), 'units'))

        self.events_frame = Frame(self.notes_canvas, bg=self.frame_bg)
        self.notes_canvas.create_window((0,0), window=self.events_frame)

        if for_notes: self.cursor.execute("SELECT * FROM Notes WHERE schedule=:sched", {'sched': 'None'})
        elif for_trash: 
            self.cursor.execute("SELECT * FROM Trash")
            self.delete_all_bttn = Button(self.lower_bar, border=0, bg = self.hambMenu_bg, image=self.trash, command = self.__delete_all_trash, activebackground=self.lower_bar.cget("bg"))
            self.delete_all_bttn.place(x=13, y=6)
        elif for_about: pass
        elif for_manual: pass
        else: self.cursor.execute("SELECT * FROM Notes WHERE schedule!=:sched", {'sched': 'None'})

        with self.connector:
            self.events = self.cursor.fetchall()
        self.notes = []
        if self.events:
            if len(self.events) < 4:
                y_positions = [80, 194, 308]
                self.notes_canvas.pack_forget()
            for i, notes_details in enumerate(self.events):
                title, note, sched, ringtone, last_edited  = notes_details
                if sched != "None":
                    date, _, _ = sched.split()
                    passed_date = datetime.now().strftime("%Y-%m-%d") >= date
                    
                if for_notes:
                    note_preview = " ".join(note.split())[:50]+' . . .' if note else ''
                    button_text = f"\n   {title[:20] if title else 'Untitled'}\n      📝  {f'{note_preview}' if note_preview else 'Blank Note'}"
                elif for_trash:
                    if sched == "None":
                        note_preview = " ".join(note.split())[:50]+' . . .' if note else ''
                        button_text = f"\n   {title[:20] if title else 'Untitled'}\n      📝  {f'{note_preview}' if note_preview else 'Blank Note'}"
                    else:
                        button_text = f"\n   {title[:20] if title else 'Untitled'}\n      🔔  {sched}{' ✔' if passed_date else ''}"
                else:
                    button_text = f"\n   {title[:20] if title else 'Untitled'}\n      🔔  {sched}{' ✔' if passed_date else ''}"
                self.button_frame = Canvas(self.events_frame if len(self.events) > 3 else self.root, highlightthickness=0)
                self.notes.append(self.button_frame)
                if len(self.events) > 3: self.button_frame.pack(padx=15, pady=3)
                else: self.button_frame.place(x=22, y=y_positions[i])

                Label(self.button_frame, image=self.note_imgFrame, highlightthickness=0, bg=self.frame_bg).pack()

                Button(self.button_frame,background=self.notes_bg,border=0, activebackground=self.notes_bg, text=button_text, width=76, fg="goldenrod",height=5,justify="left", anchor="w",\
                    font=("Arial Rounded MT Bold", 9), command = lambda t = title, n = note, s = sched, r = ringtone, ls = last_edited: self.open_addNote_frame(t, n, s, r, ls, True, for_trash)).place(x=20, y=11.8)
        else:
            self.notes_canvas.pack_forget()
            if for_about:
                self.about_label = Label(self.root, image=self.about, bg="#dcdcdc", highlightbackground="#dcdcdc", highlightthickness=0)
                self.about_label.place(x=20, y=79)
            else:
                if for_manual and display_manual:
                    webbrowser.open("NOTEFY Manual.pdf")

                self.main_frame_label = Label(self.root, image=self.dark_main_frame if self.root.cget("bg")!="#f0f0f0" else self.light_main_frame, highlightthickness=0, border=0)
                self.main_frame_label.place(x=20, y=79)
        #Add Note/Event button
        self.addNote_button = Button(self.root, highlightthickness= 0, border=0, bd=0,command=self.open_addNote_frame, image = self.add_button, activebackground=self.root.cget("bg"))
        self.addNote_button.place(x= 587, y= 450)
        if for_about: self.addNote_button.place_forget()
        #Hamburger button
        self.hamburg_Button = Button(self.root, border=0, command=self.open_hamb_menu, background=self.hambMenu_bg, image = self.hamburger, activebackground=self.lower_bar.cget("bg"))
        self.hamburg_Button.place(x=12, y=41)

    def __delete_all_trash(self):
        with self.connector:
            self.cursor.execute("DELETE from Trash")
        self.display_notes(for_trash=True)

    def __get_schedules(self):
        with self.connector:
            self.cursor.execute("SELECT * FROM Notes")
        return [data[2] for data in self.cursor.fetchall()]

    def play_notif_sound(self, path):
        pygame.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

    def __check_for_reminder(self):
        while True:
            if f'{datetime.now().strftime("%Y-%m-%d")}  {time.strftime("%I:%M %p")}' in self.all_scheds:
                self.all_scheds = self.__get_schedules()
                self.cursor.execute("SELECT * FROM Notes WHERE schedule=:sched", {'sched': f'{datetime.now().strftime("%Y-%m-%d")}  {time.strftime("%I:%M %p")}'})
                title, _, _, ringtone, _ = self.cursor.fetchall()[0]

                self.display_notif_pop_up()
                message = Label(self.splash_root, text=title[:20] if title else "Untitled", fg="#f0f0f0", bg="gray",font=("Arial Rounded MT Bold", 10) )
                message.pack(pady=25, fill=X)

                alarmed_sched = f'{datetime.now().strftime("%Y-%m-%d")}  {time.strftime("%I:%M %p")}'
                
                if ringtone == "Default Notification":
                    notification.notify(title="NOTEFY", message = title[:20] if title else "Untitled", app_name="NOTEFY",timeout=10, app_icon = "icon.ico")
                elif ringtone == "Default Alarm": 
                    self.play_notif_sound("Default Alarm.mp3")
                else:
                    try:
                        self.play_notif_sound(ringtone)
                    except Exception as e:
                        print(e)
                        notification.notify(title="NOTEFY", message = title[:20] if title else "Untitled", app_name="NOTEFY",timeout=10, app_icon = "icon.ico")
                while alarmed_sched == f'{datetime.now().strftime("%Y-%m-%d")}  {time.strftime("%I:%M %p")}':
                    time.sleep(2)
            time.sleep(2)

    def __save_note(self, for_update = False, for_delete=False, for_trash=False):
        self.cursor.execute("SELECT * FROM Notes WHERE schedule=:sched", {'sched': self.__event_sched})
        blank_note = not (self.title_entry.get() or self.__note_entry.get(1.0, END).rstrip() or self.__event_sched != "None")
        try:
            if self.previous_sched == self.__event_sched:
                valid_time = True
            elif self.hour_entry.get().isnumeric() and self.minute_entry.get().isnumeric() and self.am_or_pm.get() in ["AM", 'PM']:
                valid_time = self.__event_sched == "None" or ( int(self.hour_entry.get()) in list(range(1,13)) and int(self.minute_entry.get()) in list(range(60)) )
            else:
                valid_time = self.__event_sched == "None" or False
        except AttributeError as e:
            print(e)
            valid_time = self.__event_sched=="None" or ( int(self.__event_sched.split()[1].split(":")[0]) in list(range(1,13)) and int(self.__event_sched.split()[1].split(":")[1]) in list(range(60)) )
        #check if sched is taken
        if not for_update: sched_is_taken = self.cursor.fetchall() and self.__event_sched !="None"
        else: sched_is_taken = (self.cursor.fetchall() and self.__event_sched != self.previous_sched) and self.__event_sched != "None"

        if for_update == "None":
            pass
        elif for_delete:
            if not for_trash:
                with self.connector:
                    self.cursor.execute("DELETE from Notes WHERE schedule=:s AND notes=:n AND schedule=:s AND ringtone=:r AND last_edit=:LE",\
                         {"s": self.previous_title, "n": self.previous_note, "s": self.previous_sched, "r": self.previous_ringtone, "LE": self.last_edited})
                    self.cursor.execute("INSERT INTO Trash VALUES (:title, :notes, :schedule, :ringtone, :last_edit)", \
                                        {'title': self.previous_title, 'notes': self.previous_note, 'schedule': self.previous_sched, 'ringtone': self.previous_ringtone, 'last_edit': self.last_edited})
            else:
                with self.connector:
                    self.cursor.execute("DELETE from Trash WHERE schedule=:s AND notes=:n AND schedule=:s AND ringtone=:r AND last_edit=:LE",\
                         {"s": self.previous_title, "n": self.previous_note, "s": self.previous_sched, "r": self.previous_ringtone, "LE": self.last_edited})
        elif sched_is_taken:
            self.display_notif_pop_up()
            self.splsh_title.config(bg="#bf0404")
            self.splshclose_button.config(bg="#bf0404", activebackground="#bf0404", fg="#f0f0f0")
            self.splshtitle_labl.config(text = " Oops!", bg="#bf0404", fg="#f0f0f0")
            self.splash_root.config(bg="#DCDCDC")
            self.play_notif_sound("Default Notification.mp3")
            
            title = Label(self.splash_root, text="Schedule Already Taken", fg="black",bg="#DCDCDC", font=("Arial Black",10))
            title.pack(pady=25, fill=X)
        elif not blank_note:
            if valid_time:
                self.__title = self.title_entry.get()
                self.cursor.execute("SELECT * FROM Notes")
                if not for_update:
                    last_edit = f'Edited {str(datetime.now().strftime("%Y-%m-%d"))} | {str(time.strftime("%I:%M %p"))}'
                    if self.__event_sched != "None":
                        self.__event_sched = f'{self.date_entry.get_date()}  {str(int(self.hour_entry.get())).rjust(2, "0")}:{str(int(self.minute_entry.get())).rjust(2, "0")} {self.am_or_pm.get()}'
                    with self.connector:
                        self.cursor.execute("INSERT INTO Notes VALUES (:title, :notes, :schedule, :ringtone, :last_edit)", \
                        {'title': self.__title, 'notes': self.__note_entry.get(1.0, END).rstrip(), 'schedule': self.__event_sched, 'ringtone': self.ringtone, 'last_edit': last_edit})
                else:
                    last_edit = self.last_edited if (self.__title == self.previous_title) and (self.__note_entry.get(1.0, END).rstrip() == self.previous_note) and (self.__event_sched == self.previous_sched) and self.ringtone == self.previous_ringtone \
                        else f'Edited {str(datetime.now().strftime("%Y-%m-%d"))} | {str(time.strftime("%I:%M %p"))}'
                    if self.previous_sched != self.__event_sched and self.__event_sched != "None":
                        self.__event_sched = f'{self.date_entry.get_date()}  {str(int(self.hour_entry.get())).rjust(2, "0")}:{str(int(self.minute_entry.get())).rjust(2, "0")} {self.am_or_pm.get()}'
                    with self.connector:
                        self.cursor.execute("UPDATE Notes SET title = :t, notes = :n, schedule = :s, ringtone = :r, last_edit = :LE WHERE title = :prev_title AND notes = :prev_notes AND schedule = :prev_sched AND ringtone = :prev_ringtone AND last_edit = :LE0", \
                        {'t': self.__title, 'n': self.__note_entry.get(1.0, END).rstrip(), "s": self.__event_sched, "r": self.ringtone, "LE": last_edit,\
                        "prev_title": self.previous_title, "prev_notes": self.previous_note, "prev_sched": self.previous_sched, "prev_ringtone": self.previous_ringtone, "LE0": self.last_edited})
            elif not valid_time:
                self.display_notif_pop_up()
                self.splsh_title.config(bg="#bf0404")
                self.splshclose_button.config(bg="#bf0404", activebackground="#bf0404", fg="#f0f0f0")
                self.splshtitle_labl.config(text = " Oops!", bg="#bf0404", fg="#f0f0f0")
                self.splash_root.config(bg="#DCDCDC")
                self.play_notif_sound("Default Notification.mp3")
                
                title = Label(self.splash_root, text="Invalid Datetime", fg="black",bg="#DCDCDC", font=("Arial Black",10))
                title.pack(pady=25, fill=X)
        elif blank_note and for_update:
            with self.connector:
                self.cursor.execute("DELETE from Notes WHERE schedule=:s AND notes=:n AND schedule=:s AND ringtone=:r AND last_edit=:LE", \
                                    {"s": self.previous_title, "n": self.previous_note, "s": self.previous_sched, "r": self.previous_ringtone, "LE": self.last_edited})
                self.cursor.execute("INSERT INTO Trash VALUES (:title, :notes, :schedule, :ringtone, :last_edit)", \
                                    {'title': self.previous_title, 'notes': self.previous_note, 'schedule': self.previous_sched, 'ringtone': self.previous_note, 'last_edit': self.last_edited})
    
    def back_to_mainWindow(self, for_update = False, for_delete=False, for_trash=False):
        # this try block's purpose is solely to remove a widget before displaying a new one
        try: self.delete_button.place_forget()
        except: pass
        self.textBox_scrollBar.pack_forget()
        self.theme_bttn.place(x=610, y=40)

        self.__save_note(for_update=for_update, for_delete=for_delete, for_trash=for_trash)

        blank_note = not (self.title_entry.get() or self.__note_entry.get(1.0, END).rstrip() or self.__event_sched != "None")
        if blank_note:
            if self.page_title.cget("text")=="notes": 
                self.page_title.config(image=self.notes_title, text="notes")
                self.display_notes(for_notes = True)
            elif self.page_title.cget("text")=="trash": 
                self.page_title.config(image=self.trash_title, text = "trash")
                self.display_notes(for_trash=True)
            elif self.page_title.cget("text")=="abouts":
                 self.display_notes(for_abouts=True)
            elif self.page_title.cget("text")=="manual":
                self.display_notes(for_manual=True, display_manual=False)
            else:
                self.page_title.config(image=self.events_title, text = "events") 
                self.display_notes()
        elif not for_trash:
            if self.__event_sched == "None": self.display_notes(for_notes = True)
            else: self.display_notes()
        else: 
            self.display_notes(for_trash=True)

        self.time_label.place_configure(x=533, y=45)
        self.__event_sched = "None"
        self.ringtone = "Default Notification"
        self.hamburg_Button["state"] = NORMAL
        self.addNote_frame.place_forget()
        self.all_scheds = self.__get_schedules()

    def open_addNote_frame(self, title="", note="", sched="",ringtone="", last_edit = "", for_update=False, for_trash = False):

        def create_roundEdged_rectangle(x1, y1, x2, y2, radius=25, **kwargs):
            points = [x1+radius, y1, x1+radius, y1,x2-radius, y1, x2-radius, y1, x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2, x2-radius, y2,
                        x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]

            return self.canvas.create_polygon(points, **kwargs, smooth=True, width=3, fill=self.root.cget("bg"), outline="goldenrod3" )

        self.theme_bttn["state"] = DISABLED
        # Note's previous data (before editing)
        self.previous_title, self.previous_note, self.previous_sched, self.previous_ringtone, self.last_edited = title, note, sched, ringtone, last_edit
        #delete button
        if for_update:
            self.delete_button = Button(self.lower_bar, border=0, bg = self.hambMenu_bg, image=self.trash, command= lambda: self.back_to_mainWindow(for_delete=True, for_trash=for_trash), activebackground=self.lower_bar.cget("bg"))
            self.delete_button.place(x=13, y=6)
        # this try block's purpose is solely to remove a widget before displaying a new one
        try: self.close_hamb_menu()
        except: pass
        self.notes_canvas.unbind_all('<MouseWheel>')
        self.events_frame.destroy()
        self.notes_canvas.destroy()
        self.hamburg_Button["state"] = DISABLED
        self.addNote_button.place_forget()
        #Add Event/Note Frame
        self.addNote_frame = Frame(self.root, bg = "#DCDCDC", height=451, width=675)
        self.addNote_frame.place(x= 5, y= 75)

        self.canvas = Canvas(self.addNote_frame,height=438,width=678,bg=self.root.cget("bg"), highlightthickness=0)
        self.canvas.pack()
        create_roundEdged_rectangle(10, 15, 670, 428, radius=130)

        self.canvas.create_line(30, 85, 650, 85,fill="goldenrod3", width=2)

        # back&save button
        back_button = Button(self.addNote_frame,activebackground=self.root.cget("bg"), image=self.back_button, borderwidth=0,\
             bg=self.root.cget("bg"), command=lambda : self.back_to_mainWindow(for_update = for_update if not for_trash else "None", for_trash=for_trash))
        back_button.place(x= 32, y=40)
        # ringtone button
        ringtone_button = Button(self.addNote_frame,activebackground=self.root.cget("bg"), image=self.ringtone_icon,borderwidth=0, bg=self.root.cget("bg"),command=self.open_ringtone_picker, fg="goldenrod3", activeforeground="goldenrod3")
        ringtone_button.place(x= 500, y=33)
        # alarm button
        alarm_button = Button(self.addNote_frame,borderwidth=0,activebackground=self.root.cget("bg"), bg=self.root.cget("bg"), image=self.datetime_icon, command=self.open_schedPicker_frame, fg="goldenrod3", activeforeground="goldenrod3")
        alarm_button.place(x= 533, y=33)
        # Title Entry
        Label(self.addNote_frame,fg=self.notesTitle_fg, text="TITLE:", font=("Arial Rounded MT Bold", 10), bg=self.root.cget("bg")).place(x=30, y=59)
        self.title_entry = Entry(self.addNote_frame,borderwidth=0, width=77, bg=self.root.cget("bg"), fg=self.notes_fg, font=("Times", 11), insertbackground="goldenrod")
        self.title_entry.place(x=90, y=61)
        self.title_entry.insert(0, title)
        # text box scrollbar
        self.textBox_scrollBar = ttk.Scrollbar(self.root)
        self.textBox_scrollBar.pack(fill=Y, side=RIGHT, pady=50)
        # Note Box
        Label(self.addNote_frame,fg=self.notesTitle_fg, text="NOTE", bg=self.root.cget("bg"), font=("Arial Rounded MT Bold", 10)).place(x=30, y=90)
        self.__note_entry = Text(self.addNote_frame,borderwidth=0,fg=self.notes_fg, bg=self.root.cget("bg"), height=14, width=85, font=("Times", 11),\
             undo=True, selectbackground="#bf8600", selectforeground="black", yscrollcommand=self.textBox_scrollBar.set, insertbackground="goldenrod")
        self.__note_entry.place(x=40, y=117)
        self.__note_entry.insert(END, note)
        self.textBox_scrollBar.config(command=self.__note_entry.yview)
        # Image to Text
        img2Text_button = Button(self.addNote_frame,activebackground=self.root.cget("bg"), image=self.img2text, borderwidth=0, bg=self.root.cget("bg"), command = self.open_img2text_frame)
        img2Text_button.place(x=570, y=35)
        # speech to text
        speech2text_button = Button(self.addNote_frame, activebackground=self.lower_bar.cget("bg"),image=self.mic_icon, borderwidth=0, bg=self.root.cget("bg"),command=self.__convert_speech)
        speech2text_button.place(x=613, y=35)
        # undo
        undo_button = Button(self.addNote_frame,activebackground=self.root.cget("bg"), image=self.undo_img, borderwidth=0, bg=self.root.cget("bg"),command=self.undo)
        undo_button.place(x=50, y=405)
        #redo button
        redo_button = Button(self.addNote_frame, activebackground=self.root.cget("bg"), image=self.redo_img, borderwidth=0, bg=self.root.cget("bg"),command=self.redo)
        redo_button.place(x=75, y=405)
        # last_edited
        self.lastEdited_label = Label(self.addNote_frame, text=last_edit, bg=self.root.cget("bg"),font=("Arial", 7),borderwidth=0, fg=self.notesTitle_fg)
        self.lastEdited_label.place(x=263, y=410)
        if sched !="None" and sched:  self.__save_note_sched(sched, for_trash=for_trash)
        if for_trash:
            Button(self.addNote_frame,image=self.restore_bttn,  borderwidth=0, bg=self.root.cget("bg"),activebackground=self.root.cget("bg"),command=self.__restore).place(x=623, y=30)
            self.textBox_scrollBar.pack_forget()
            undo_button.place_forget()
            redo_button.place_forget()
            speech2text_button.place_forget()
            img2Text_button.place_forget()
            alarm_button.place_forget()
            ringtone_button.place_forget()
            self.__note_entry["state"]  = DISABLED

    def __restore(self):
        self.delete_button.place_forget()
        self.addNote_frame.place_forget()
        with self.connector:
            self.cursor.execute("DELETE from Trash WHERE schedule=:s AND notes=:n AND schedule=:s AND ringtone=:r AND last_edit=:LE",\
                 {"s": self.previous_title, "n": self.previous_note, "s": self.previous_sched, "r": self.previous_ringtone, "LE": self.last_edited})
            self.cursor.execute("INSERT INTO Notes VALUES (:title, :notes, :schedule, :ringtone, :last_edit)", \
                 {'title': self.previous_title, 'notes': self.previous_note, 'schedule': self.previous_sched, 'ringtone': self.previous_ringtone, "last_edit": self.last_edited})
        self.display_notes(for_trash=True)

    def open_ringtone_picker(self):
        # frame that acts as border
        self.ringtone_frame = Frame(self.addNote_frame, bg = "goldenrod3", width = 226, height = 111)
        self.ringtone_frame.place(x=309, y=30)
        # top frame
        self.ringtone_topFrame = Frame(self.ringtone_frame, bg=self.notes_bg, width=220, height=105)
        self.ringtone_topFrame.place(x=3, y=3)
        Label(self.ringtone_topFrame, text="CHOOSE A RINGTONE",font=("Arial Rounded MT Bold", 10), fg=self.notes_fg,bg=self.notes_bg).place(x=37, y=12)
        # img path entry
        style = ttk.Style()
        style.configure('TCombobox', fieldbackground=self.titleEntry_bg)
        self.ringtone_entry = ttk.Combobox(self.ringtone_topFrame, values = ["Default Notification", "Default Alarm"], width=20, style="TCombobox")
        self.ringtone_entry.set("Default Notification" if not self.previous_ringtone else self.previous_ringtone)
        self.ringtone_entry.place(x=10, y=41)
        if self.ringtone or self.previous_ringtone:
            self.ringtone_entry.set(self.previous_ringtone if self.previous_ringtone else self.ringtone)
        # choose image button
        Button(self.ringtone_topFrame, text="CHOOSE", bg=self.hambMenu_bg,command=self.pick_ringtone, fg=self.notes_fg, activebackground="goldenrod").place(x=155, y=37)
        # Okay button
        Button(self.ringtone_topFrame, text="DONE",bg=self.hambMenu_bg, fg=self.notes_fg, command=self.save_ringtone, activebackground="goldenrod",width=23).place(x=25, y=70)
        # x butoon
        Button(self.ringtone_topFrame, text="X", bg=self.notes_bg, font=("Arial", 11),activebackground=self.notes_bg , command=self.save_ringtone, border=0, fg=self.notesTitle_fg).place(x=197, y=1)

    def save_ringtone(self):
        self.ringtone = self.ringtone_entry.get() if self.ringtone_entry.get() else "Default Notification"
        self.ringtone_frame.place_forget()
        
    def undo(self):
        try: self.__note_entry.edit_undo()
        except: pass

    def redo(self):
        try: self.__note_entry.edit_redo()
        except: pass

    def __convert_speech(self):
        try:
            __recognizer = speech_recognition.Recognizer()
            with speech_recognition.Microphone() as source:
                __recognizer.adjust_for_ambient_noise(source, duration=0.2)
                __audio = __recognizer.listen(source)
            try:
                __text = __recognizer.recognize_google(__audio)
                self.__note_entry.insert(END, " "+__text)
            except Exception as e:
                print(e)
                self.display_notif_pop_up()
                self.splsh_title.config(bg="#bf0404")
                self.splshclose_button.config(bg="#bf0404", activebackground="#bf0404", fg="#f0f0f0")
                self.splshtitle_labl.config(text = " Oops!", bg="#bf0404", fg="#f0f0f0")
                self.splash_root.config(bg="#DCDCDC")
                self.play_notif_sound("Default Notification.mp3")
                
                title = Label(self.splash_root, text="Sorry. Didn't get that.", fg="black",bg="#DCDCDC", font=("Arial Black",10))
                title.pack(pady=25, fill=X)
        except Exception as e:
            print(e) 
            self.display_notif_pop_up()
            self.splsh_title.config(bg="#bf0404")
            self.splshclose_button.config(bg="#bf0404", activebackground="#bf0404", fg="#f0f0f0")
            self.splshtitle_labl.config(text = " Oops!", bg="#bf0404", fg="#f0f0f0")
            self.splash_root.config(bg="#DCDCDC")
            self.play_notif_sound("Default Notification.mp3")
            
            title = Label(self.splash_root, text="Check your internet connection.", fg="black",bg="#DCDCDC", font=("Arial Black",10))
            title.pack(pady=25, fill=X)

    def open_img2text_frame(self):
        self.img2Text_frame = Frame(self.addNote_frame, bg = "goldenrod3", width = 220, height = 115)
        self.img2Text_frame.place(x=390, y=30)
        #top frame
        self.img2Text_topFrame = Frame(self.img2Text_frame, bg=self.notes_bg, width=214, height=110)
        self.img2Text_topFrame.place(x=3, y=3)
        # img path entry
        Label(self.img2Text_topFrame, text="CHOOSE THE IMAGE", font=("Arial Rounded MT Bold", 10), fg=self.notes_fg, bg=self.notes_bg).place(x=37, y=14)
        self.imgPath_entry = Entry(self.img2Text_topFrame, width=20, bg=self.titleEntry_bg, fg=self.notes_fg)
        self.imgPath_entry.place(x=15, y=45)
        # choose image button
        Button(self.img2Text_topFrame, text="CHOOSE",bg=self.hambMenu_bg, command=self.pick_image, fg=self.notes_fg, activebackground="goldenrod").place(x=143, y=41)
        # convert button
        self.convertImg_button = Button(self.img2Text_topFrame,bg=self.hambMenu_bg, text="CONVERT",command=self.__convert_img, width=20,fg=self.notes_fg, activebackground="goldenrod").place(x=33, y=75)
        # back button
        Button(self.img2Text_topFrame, text="X", bg=self.notes_bg, font=("Arial", 11),activebackground=self.notes_bg ,command= lambda: self.img2Text_frame.place_forget(), border=0, fg=self.notesTitle_fg).place(x=190, y=1)

    def pick_ringtone(self):
        self.ringtone_path = filedialog.askopenfile()
        try:
            self.ringtone = self.ringtone_path.name
        except Exception as e:
            print(e) 
            self.ringtone = "Default Notification"
        self.ringtone_frame.place_forget()

    def pick_image(self):
        try:
            self.image_path = filedialog.askopenfile()
            self.imgPath_entry.delete(0, END)
            self.imgPath_entry.insert(0, self.image_path.name)
        except Exception as e:
            print(e)

    def __convert_img(self):
        if self.imgPath_entry.get():
            try:
                self.__img = cv2.imread(self.image_path.name)
                self.__img = cv2.resize(self.__img, None, fx=2, fy=2)
                self.__img = cv2.cvtColor(self.__img, cv2.COLOR_BGR2GRAY)
                self.__txt = pytesseract.image_to_string(self.__img, config = '--oem 3 --psm 6')
                self.__note_entry.insert(END, " "+self.__txt)
                self.img2Text_frame.place_forget()
            except Exception as e:
                print(e) 
                self.display_notif_pop_up()
                self.splsh_title.config(bg="#bf0404")
                self.splshclose_button.config(bg="#bf0404", activebackground="#bf0404", fg="#f0f0f0")
                self.splshtitle_labl.config(text = " Oops!", bg="#bf0404", fg="#f0f0f0")
                self.splash_root.config(bg="#DCDCDC")
                self.play_notif_sound("Default Notification.mp3")
                
                title = Label(self.splash_root, text="Conversion Unsuccessful", fg="black",bg="#DCDCDC", font=("Arial Black",10))
                title.pack(pady=25, fill=X)
                self.img2Text_frame.place_forget()

    def open_schedPicker_frame(self):
        # Date and Time Selector Frame
        self.dateTime_setter_frame = Frame(self.addNote_frame, width = 221, height = 111, bg = "goldenrod3")
        self.dateTime_setter_frame.place(x=347, y=30)
        # top frame
        self.datetime_topFrame = Frame(self.dateTime_setter_frame, bg=self.notes_bg, width=215, height=105)
        self.datetime_topFrame.place(x=3, y=3)
        # Date selector
        style = ttk.Style(self.root)
        style.configure('my.DateEntry', fieldbackground=self.titleEntry_bg)
        Label(self.datetime_topFrame,  text="DATE: ",font=("Arial Rounded MT Bold", 10), bg=self.notes_bg, fg=self.notes_fg ).place(x=35, y=23)
        self.date_entry = DateEntry(self.datetime_topFrame, selectmode = "day", background='#bf8600', style="my.DateEntry")
        self.date_entry.place(x=85, y=23)
        #back button
        Button(self.datetime_topFrame,border=0, text= "X",font=("Arial", 11),bg=self.notes_bg,activebackground=self.notes_bg, command= self.__save_note_sched, fg=self.notesTitle_fg).place(x=193, y=1)
        #Time selector
        Label(self.datetime_topFrame,  text="TIME:",font=("Arial Rounded MT Bold", 10), bg=self.notes_bg, fg=self.notes_fg ).place(x=25, y=57)
        self.hour_entry = Spinbox(self.datetime_topFrame, from_=0, to=12, wrap=True , width=3,justify=CENTER, increment=-1, bg=self.titleEntry_bg)
        self.hour_entry.place(x=70, y=58)
        Label(self.datetime_topFrame, text=':',font=("Arial Rounded MT Bold", 10), bg=self.notes_bg, fg=self.notes_fg).place(x=100, y=55)
        self.minute_entry = Spinbox(self.datetime_topFrame, from_=0, to=59, wrap=True , width=3,justify=CENTER, increment=-1, bg=self.titleEntry_bg)
        self.minute_entry.place(x=110, y=58)
        self.am_or_pm = ttk.Combobox(self.datetime_topFrame, values = ["AM", "PM"], width=3, style="my.DateEntry")
        self.am_or_pm.set("AM")
        self.am_or_pm.place(x=150, y=57)

    def __save_note_sched(self, sched="", for_trash = False):
        if sched:
            self.__event_sched_popUp = Label (self.addNote_frame, text=sched, bg=self.root.cget("bg"),font=("Arial", 8),borderwidth=0, fg="goldenrod")
            self.__event_sched_popUp.place(x=525, y=405)
            self.remove_schedButton = Button(self.addNote_frame, image=self.close,borderwidth=0, bg=self.root.cget("bg"), command=self.__remove_event_reminder, activebackground=self.notes_bg)
            if not for_trash: self.remove_schedButton.place(x=502, y=405)
            self.__event_sched = sched
            
        else:
            if self.hour_entry.get() != "0" or self.minute_entry.get() != "0":
                self.__event_sched = f'{self.date_entry.get_date()}  {self.hour_entry.get().rjust(2, "0")[:2]}:{self.minute_entry.get().rjust(2, "0")[:2]} {self.am_or_pm.get()[:2]}'
                #picked schedule and its remove button
                self.__event_sched_popUp = Label (self.addNote_frame, text=self.__event_sched,font=("Arial", 8),borderwidth=0, bg=self.root.cget("bg"), fg="goldenrod")
                self.__event_sched_popUp.place(x=525, y=405)
                self.remove_schedButton = Button(self.addNote_frame, image=self.close,borderwidth=0, bg=self.root.cget("bg"), command=self.__remove_event_reminder, activebackground=self.notes_bg)
                if not for_trash: self.remove_schedButton.place(x=502, y=405)
            self.dateTime_setter_frame.place_forget()
            
    def __remove_event_reminder(self):
        self.__event_sched_popUp.place_forget()
        self.remove_schedButton.place_forget()
        self.__event_sched = "None"
        self.ringtone = "Default Notification"

    def open_hamb_menu(self):
        self.menu = Frame(self.root, width=200, height=492, bg =self.hambMenu_bg, highlightbackground="gray", highlightthickness=1)
        self.menu.place(x=0, y=27)

        self.menu_image = Label(self.menu, image=self.menu_title, border=0, bg = self.hambMenu_bg)
        self.menu_image.place(x=65, y=12)

        self.ham_label = Label(self.menu, image=self.hamb_label, border=0, bg =self.hambMenu_bg)
        self.ham_label.place(x=15, y=464)
        self.addNote_button.place_forget()
        #hamburger button
        Button(self.menu, border=0, background=self.hambMenu_bg, activebackground=self.hambMenu_bg, image=self.hamburger, command = self.close_hamb_menu).place(x=7, y=10)
        self.font = font.Font(family='Calibri', size=13)
        #Hamburger Menu Buttons
        #Events List
        self.events_bttn= Button(self.menu, border=0, width=21, fg = self.hamb_fg, height=1,  bg =self.hambMenu_bg, activebackground='gray', activeforeground='white', text=f"   📅  Events List      ", \
            font=self.font, command=self.display_notes )
        self.events_bttn.place(x= 1, y=57)
        self.events_bttn.bind('<Enter>', self.on_hover)
        self.events_bttn.bind('<Leave>', self.not_on_hover)
        #Notes List
        self.notes_bttn= Button(self.menu, border=0, width=21, fg = self.hamb_fg,height=1,  bg =self.hambMenu_bg, activebackground='#E9BF34', activeforeground='black', text=f"  🗒   Notes List{' '*6}", \
            font=self.font, command = lambda : self.display_notes(for_notes = True))
        self.notes_bttn.place(x= 1,y= 89)
        self.notes_bttn.bind('<Enter>', lambda _: self.on_hover(None, for_notes= True))
        self.notes_bttn.bind('<Leave>', lambda _ : self.not_on_hover(None, for_notes= True))
        #Trash
        self.trash_bttn= Button(self.menu, border=0, width=21, height=1, fg = self.hamb_fg,bg =self.hambMenu_bg, activebackground="#7D671C", activeforeground="white",  text=f" 🗑  Trash{' '*14}", \
            font=self.font, command = lambda: self.display_notes(for_trash = True))
        self.trash_bttn.place(x= 1,y= 119)
        self.trash_bttn.bind('<Enter>', lambda _: self.on_hover(None, for_trash= True))
        self.trash_bttn.bind('<Leave>', lambda _: self.not_on_hover(None, for_trash= True))
        #About
        self.about_bttn= Button(self.menu, border=0, width=21, height=1, fg = self.hamb_fg,bg =self.hambMenu_bg, activebackground="#3F330E", activeforeground="white",  text=f"   📌  About{' '*15}", font=self.font, command=lambda:self.display_notes(for_about=True))
        self.about_bttn.place(x= 1,y= 149)
        self.about_bttn.bind('<Enter>', lambda _: self.on_hover(None, for_about= True))
        self.about_bttn.bind('<Leave>', lambda _: self.not_on_hover(None, for_about= True))
        # Manual
        self.manual_bttn= Button(self.menu, border=0, width=21, height=1, fg = self.hamb_fg,bg =self.hambMenu_bg, activebackground="#3F330E", activeforeground="white",  text=f"     📚  Manual{' '*15}", font=self.font, command=lambda:self.display_notes(for_manual=True))
        self.manual_bttn.place(x= 1,y= 179)
        self.manual_bttn.bind('<Enter>', lambda _: self.on_hover(None, for_manual= True))
        self.manual_bttn.bind('<Leave>', lambda _ : self.not_on_hover(None,for_manual= True))

    def on_hover(self, _, for_manual = False, for_notes = False, for_trash = False, for_about = False):
        if for_manual:
            self.manual_bttn['background']= '#004d29'; self.manual_bttn['foreground']= 'white'
        elif for_notes: 
            self.notes_bttn['background']= '#E9BF34' ; self.notes_bttn['foreground']= 'black'
        elif for_trash:
            self.trash_bttn['background']= '#7D671C' ; self.trash_bttn['foreground']= 'white'
        elif for_about:
            self.about_bttn['background']= '#3F330E' ; self.about_bttn['foreground']= 'white'
        else:
            self.events_bttn['background']= 'gray'; self.events_bttn['foreground']= 'white'

    def not_on_hover(self, _, for_manual = False, for_notes = False, for_trash = False, for_about = False):
        if for_manual:
            self.manual_bttn['background']= self.hambMenu_bg; self.manual_bttn['foreground']= self.hamb_fg
        elif for_notes:
            self.notes_bttn['background']= self.hambMenu_bg ; self.notes_bttn['foreground']= self.hamb_fg
        elif for_trash:
            self.trash_bttn['background']= self.hambMenu_bg ; self.trash_bttn['foreground']= self.hamb_fg
        elif for_about:
            self.about_bttn['background']= self.hambMenu_bg ; self.about_bttn['foreground']= self.hamb_fg
        else:
            self.events_bttn['background']= self.hambMenu_bg; self.events_bttn['foreground']= self.hamb_fg

    def close_hamb_menu(self):
        try:
            self.menu.place_forget()
            self.addNote_button.place(x= 587, y= 450)
        except Exception as e:
                print(e)


def main():
    Main()

if __name__ == '__main__':
    main()