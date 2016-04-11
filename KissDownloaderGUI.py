from KissDownloader import *
from tkinter import *
from tkinter.ttk import *

class App(Frame):

    def __init__(self):
        Frame.__init__(self)
        self.master.title("KissDownloader")
        self.grid()
        self.master.geometry("585x320")


    # create label for site select
        self.site_select_label = Label(self, text="Select Site to download from: ").grid(row=1, column=1)
    # create a Combobox with site to choose from
    # currently not in effect
        self.available_sites = ['kissanime.to']
        self.site_select = Combobox(self, values=self.available_sites)
        self.site_select.grid(row=1, column=2, padx=32, pady=8)
    # create username label and field
        self.user_name_label = Label(self, text="Enter Username for Kiss: ").grid(row=2, column=1)
        self.user_name = Entry(self, width=30)
        self.user_name.grid(row=2, column=2)
    # create password label and field
        self.user_password_label = Label(self, text="Enter Password for Kiss: ").grid(row=3, column=1)
        self.user_password = Entry(self, show="*", width=30)
        self.user_password.grid(row=3, column=2)
    # create kissanime url label and field
        self.url_label = Label(self, text="Enter URL for season: ").grid(row=4, column=1)
        self.url = Entry(self, width=30)
        self.url.grid(row=4, column=2)
    # create season name label and field
        self.title_label = Label(self, text="Enter anime Title: ").grid(row=5, column=1)
        self.title = Entry(self, width=30)
        self.title.grid(row=5, column=2)
    # create season number label and field
        self.season_num_label = Label(self, text="Enter Season number: ").grid(row=6, column=1)
        self.season_num = Entry(self, width=30)
        self.season_num.grid(row=6, column=2)
    # create episode min label and field
        self.episode_min_label = Label(self, text="Enter Episode Min: ").grid(row=7, column=1)
        self.episode_min = Entry(self, width=30)
        self.episode_min.grid(row=7, column=2)
    # create episode max label and field
        self.episode_max_label = Label(self, text="Enter Episode Max: ").grid(row=8, column=1)
        self.episode_max = Entry(self, width=30)
        self.episode_max.grid(row=8, column=2)
    # create root destination label and field
        self.destination_label = Label(self, text="Enter Root Destination: ").grid(row=9, column=1)
        self.destination = Entry(self, width=30)
        self.destination.grid(row=9, column=2)
    # create label for quality select
        self.site_select_label = Label(self, text="Select Quality to download: ").grid(row=10, column=1)
    # create a Combobox with quality to choose from
        self.available_quality = ["1920x1080.mp4", "1280x720.mp4", "640x360.mp4", "320x180.3pg", "960x720.mp4", "480x360.mp4", "320x240.3pg"]
        self.quality_select = Combobox(self, values=self.available_quality)
        self.quality_select.grid(row=10, column=2, padx=32, pady=8)
    # import config button
        self.download_button = Button(self, text='Import Config')
        self.download_button['command'] = self.fill_gui_from_config
        self.download_button.grid(row=11, column=2)
    # download button
        self.download_button = Button(self, text='Download')
        self.download_button['command'] = self.run_download
        self.download_button.grid(row=11, column=3)

    def fill_gui_from_config(self):
        global config
        # create a configparser instance and open config.ini
        config = configparser.ConfigParser()
        config.read("config.ini", encoding='utf-8')

        # fill gui from what is in the config
        site_select = config["Website"]
        if len(site_select["subsite"]) != 0:
            self.site_select.select_clear()
            self.site_select.set(site_select["subsite"])

        auth = config["login"]
        if len(auth["username"]) != 0:
            self.user_name.delete(0, END)
            self.user_name.insert(0, auth["username"])

        if len(auth["password"]) != 0:
            self.user_password.delete(0, END)
            self.user_password.insert (0, auth["password"])

        show = config["show"]
        if len(show["title"]) != 0:
            self.title.delete(0, END)
            self.title.insert(0, show["title"])

        if len(show["anime"]) != 0:
            self.url.delete(0, END)
            self.url.insert(0, show["anime"])

        if len(show["Season"]) != 0:
            self.season_num.delete(0, END)
            self.season_num.insert(0, show["Season"])

        if len(show["episodeMin"]) != 0:
            self.episode_min.delete(0, END)
            self.episode_min.insert(0, show["episodeMin"])

        if len(show["episodeMax"]) != 0:
            self.episode_max.delete(0, END)
            self.episode_max.insert(0, show["episodeMax"])

        if len(show["destination"]) != 0:
            self.destination.delete(0, END)
            self.destination.insert(0, show["destination"])

        if len(show["quality"]) != 0:
            self.quality_select.select_clear()
            self.quality_select.set(show["quality"])

    def run_download(self):
        if self.destination.get().endswith('\\'):
            destination = self.destination.get() + self.title.get() + "\\"
        else:
            destination = self.destination.get() + "\\" + self.title.get() + "\\"
        params = [self.user_name.get(), self.user_password.get(), self.title.get(), self.url.get(), str(self.season_num.get()), str(self.episode_min.get()), str(self.episode_max.get()), destination, self.quality_select.get()]
        print(params)
        KissDownloader(params)


root = Tk() 
app = App()
root.mainloop()
