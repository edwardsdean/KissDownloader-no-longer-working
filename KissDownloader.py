import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
#stuff that I might do... eventually
#TODO error management
#TODO standalone package
#TODO confirm a successful login
#TODO add support for kisscartoon.com
#TODO fancy logging
#TODO persistent config
#TODO filename customization, with persistent config
#TODO a fancy gui
#TODO us a hidden browser instead of firefox
#TODO support for initialization of the Downloader class with arguments or a config file instead of get_params
#TODO support for starting the script with command line args
#TODO support for choosing video quality instead of automatically downloading the highest quality
#TODO detect file type instead of asuming mp4
#TODO maybe build downloader as a module? idk man
#TODO simultaneous downloads
#TODO download progress
#TODO pause downloads
#TODO get video src through video player to avoid the need to login and handle user data
#TODO support for queueing downloads, will be easy once configs/console launching is supported
class Downloader():

    def __init__(self):
        #create a webdriver instance with a lenient timeout duration
        self.driver = webdriver.Firefox()
        self.driver.set_page_load_timeout(100)

    def login(self):
        self.driver.get("http://kissanime.com/Login")\

        #wait for cloudflare to figure itself out
        time.sleep(10)

        #locate username and password fields in the login page
        username = self.driver.find_element_by_id("username")
        password = self.driver.find_element_by_id("password")

        #get login info from user
        user = input("username:")
        pw = input("password:")

        #type login info into fields
        username.send_keys(user)
        password.send_keys(pw)

        #send the filled out login form
        password.send_keys(Keys.RETURN)
        time.sleep(5)

    def get_params(self):
        #get all these parameters from the user, will eventually support easier ways of setting these params
        self.anime = input("anime root url, ie http://kissanime.com/Anime/One-Piece : ")
        self.title = input("anime title: ")
        self.season = input("season to download, for filenames: ")
        self.episodeMin = int(input("episode to start downloading from: "))
        self.episodeMax = int(input("episode to download last: ")) + 1
        self.destination = input("path for file dowload: ")

    def get_episode_page(self, episode):
        #parses the streaming page of an episode from the root page
        soup = BeautifulSoup(self.rootPage, 'html.parser')
        for link in soup.findAll('a'):
            currentlink = link.get('href')
            if currentlink == None:
                pass
            elif "/Episode-"+str(episode).zfill(3) in currentlink:
                return "http://kissanime.com" + currentlink

    def get_video_src(self, page):
        #parses the video source link from the streaming page, currently chooses the highest available quality
        print("page is " + page)
        x = True
        while(x):
            try:
                self.driver.get(page)
                x = False
            except TimeoutException:
                pass
        time.sleep(10)
        self.currentPage = self.driver.page_source
        soup = BeautifulSoup(self.currentPage, 'html.parser')
        for link in soup.findAll('a'):
            currentlink = link.get('href')
            if currentlink == None:
                pass
            elif "https://redirector.googlevideo.com/videoplayback?" in currentlink:
                return currentlink

    def download_video(self, url, Name, destination):
            # downloads the episode, currently assumes it to be an mp4
        fileName = Name + ".mp4" #add the expected file type here
        path = destination + fileName
        r = requests.get(url, stream=True)
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        return path

    def close(self):
        #closes the browser window, may be used for other program-ending tasks later on
        self.driver.close()

    def download(self):
        #uses all the other functions to do the downloads
        self.login()
        self.get_params()
        self.driver.get(self.anime)
        time.sleep(10)
        self.rootPage = self.driver.page_source
        for e in range (self.episodeMin, self.episodeMax):
            page = self.get_episode_page(e)
            video = self.get_video_src(page)
            filename = self.title + " S" + str(self.season).zfill(2) + "E" + str(e).zfill(3)
            print("downloading " + filename)
            self.download_video(video, filename, self.destination)
            print("downloaded " + filename)
        print("done downloading " + self.title + " Season " + self.season)
        self.close()

DL = Downloader()
DL.download()


