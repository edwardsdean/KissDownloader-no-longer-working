import platform
from utils import *
try:
    import tkinter as tk
except Exception as e:
    utils.log(e)
    if platform.system() == "Linux":
        utils.log("Linux systems require installing the tk package")
        utils.log("Ubuntu: sudo apt-get install python-tk")
        utils.log("Arch Linux: sudo pacman -S tk")
    else:
        utils.log("=E Tkinter not found in python (requires python 3.1+)")
from tkinter.ttk import *
import tkinter.ttk as ttk
import os
import csv
from collections import defaultdict

queued = False

try:
    from KissDownloader import *
except Exception as e:
    utils.log(e)
    utils.log("=E Critical error KissDownloader.py")
    os.system('pause')
    sys.exit()

class OneVoltTen(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne):
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        if 'PageOne' in str(cont):
            queued = True
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        controller.title("KissDownloader")

        Label(self, text="Enter series URL: ").pack()
        self.url = Entry(self, width=30)
        self.url.pack()

        Label(self, text="Enter series name: ").pack()
        self.title = Entry(self, width=30)
        self.title.pack()

        #Label(self, text="Enter series episode count: ").pack()
        #self.episode_count = Entry(self, width=30)
        #self.episode_count.pack()

        Label(self, text="Download from episode (min): ").pack()
        self.episode_min = Entry(self, width=30)
        self.episode_min.pack()

        Label(self, text="Download to episode (max): ").pack()
        self.episode_max = Entry(self, width=30)
        self.episode_max.pack()

        Label(self, text="Select maximum resolution: ").pack()
        self.quality_select = Combobox(self, values=["1080p", "720p", "480p", "360p"], width=27)
        self.quality_select.pack()

        self.queue_button = Button(self, text='Queue', width=14, command=self.queue_download).pack()

        if(int(demo_data) == 1):
            self.url.insert(0, "http://kissanime.ru/Anime/Re-Zero-kara-Hajimeru-Isekai-Seikatsu")
            self.title.insert(0, "Re_Zero")
            #self.episode_count.insert(0, "25")
            self.episode_min.insert(0, "0")
            self.episode_max.insert(0, "0")
        self.quality_select.set("1080p")


        Label(self, text="Once queued series: ").pack()
        button = tk.Button(self, text="Next", width=12, command=lambda: controller.show_frame(PageOne))
        button.pack()

    def queue_download(self):
        if("https://" in str(self.url.get()) \
            or "http://" in str(self.url.get()) \
            or "www." in str(self.url.get())):
            valid = 0
            for checkint in ["episode_min","episode_max"]:
                try_this = "self." + checkint + ".get()"
                if not eval(try_this).isdigit():
                    utils.log(checkint + " must be number!")
                    valid = 1
            if(valid == 0):
                with open( dir_path + '/resolved.csv', 'a') as csvfile:
                    thewriter = csv.writer(csvfile, delimiter=',')
                    #print(str(params))
                    params = [str(self.title.get()), str(self.url.get()), '0', '9999', str(self.episode_min.get()), str(self.episode_max.get()), str(self.quality_select.get()[:-1])]
                    thewriter.writerow(params)
                utils.log("Queued " + str(self.title.get()))
        else:
            utils.log('URL invalid')

class PageOne(tk.Frame):

    # TODO add list with scrollbar for queued items

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.back = tk.Button(self, text="Back", command=self.btnRestart)
        self.back.pack()
        self.controller=controller
        self.dir_path = dir_path=os.path.dirname(os.path.realpath(__file__))
        while queued: # wait for frame change
            pass
        self.readCSV()


    def readCSV(self):
        valid = 0
        columns = defaultdict(list) # each value in each column is appended to a list
        with open('resolved.csv','r') as f:
          reader = csv.reader(f,delimiter=',')
          message = 0
          for row in reader:
            try:
                if row[0]:
                    if valid == 0:
                        Label(self, text="Queued items:").pack()
                        valid = 1
                    new_btn = Button(self, text=row[0], command=self.btnClick(row[1]))
                    new_btn.pack()
                    message += 1
                    if message > 5:
                        Label(self, text="Additional queued items hidden.").pack()
                        break
            except IndexError as e:
                pass

        if valid == 1:
            button3 = tk.Button(self, text="Start Download", command=self.initiate)
            button3.pack()
        else:
            Label(self, text="No queued items :(").pack()

    def btnClick(self, row_url):
        # print(row_url)
        # csv where row_url in row, delete row
        pass

    def btnRestart(self):
        self.controller.destroy()
        app = OneVoltTen()
        app.mainloop()

    def initiate(self):
        self.controller.destroy()

        try:
            KissDownloader.init()
        except Exception as e:
            utils.log(e)
            utils.log("=E Critical error KissDownloader.py")

app = OneVoltTen()
app.mainloop()
