import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import configparser


# stuff that I might do... eventually
# TODO error management
# TODO standalone package
# TODO confirm a successful login
# TODO add support for kisscartoon.com
# TODO fancy logging
# TODO edit config to keep track of downloaded episodes
# TODO filename customization, with config
# TODO a fancy gui
# TODO us a hidden browser instead of firefox
# TODO support for initialization of the Downloader class with arguments or a config file instead of get_params
# TODO support for starting the script with command line args
# TODO support for choosing video quality instead of automatically downloading the highest quality
# TODO detect file type instead of assuming mp4
# TODO maybe build downloader as a module? idk man
# TODO simultaneous downloads
# TODO download progress
# TODO pause downloads
# TODO get video src through video player to avoid the need to login and handle user data
# TODO support for queueing downloads, will be easy once configs/console launching is supported
class Downloader():
    def __init__(self):
        # create a webdriver instance with a lenient timeout duration
        self.driver = webdriver.Firefox()
        self.driver.set_page_load_timeout(100)

    def login(self, user, pw):
        self.driver.get("http://kissanime.com/Login") \
 \
            # wait for cloudflare to figure itself out
        time.sleep(10)

        # locate username and password fields in the login page
        username = self.driver.find_element_by_id("username")
        password = self.driver.find_element_by_id("password")

        # type login info into fields
        username.send_keys(user)
        password.send_keys(pw)

        # send the filled out login form
        password.send_keys(Keys.RETURN)
        time.sleep(5)

    def get_episode_page(self, episode):
        # parses the streaming page of an episode from the root page
        soup = BeautifulSoup(self.rootPage, 'html.parser')
        for link in soup.findAll('a'):
            currentlink = link.get('href')
            if currentlink == None:
                pass
            elif "/Episode-" + str(episode).zfill(3) in currentlink:
                return "http://kissanime.com" + currentlink

    def get_video_src(self, page):
        # parses the video source link from the streaming page, currently chooses the highest available quality
        print("page is " + page)
        x = True
        while (x):
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
        fileName = Name + ".mp4"  # add the expected file type here
        path = destination + fileName
        r = requests.get(url, stream=True)
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        return path

    def close(self):
        # closes the browser window, may be used for other program-ending tasks later on
        self.driver.close()

    def download(self, p):
        # uses all the other functions to do the downloads
        self.login(p[0], p[1])  # 0 are the indices of the username and password from get_params()
        self.driver.get(p[3])  # 3 is the index of the url
        time.sleep(10)
        self.rootPage = self.driver.page_source
        for e in range(p[5], p[6]):  # 5 and 6 are episodes min and max
            page = self.get_episode_page(e)
            video = self.get_video_src(page)
            filename = p[2] + " S" + str(p[4].zfill(2)) + "E" + str(e).zfill(3)  # 2 is the title, 4 is the season
            print("downloading " + filename)
            self.download_video(video, filename, p[7])  # 7 is the destination
            print("downloaded " + filename)
        print("done downloading " + p[2] + " Season " + p[4])
        self.close()


def get_params():
    # create a configparser instance and open config.ini
    config = configparser.ConfigParser()
    config.read("config.ini")

    # check if each parameter is present in the config file
    # if not, get it from the user
    auth = config["Login"]
    if len(auth["username"]) != 0:
        user = auth["username"]
    else:
        user = input("input username: ")

    if len(auth["password"]) != 0:
        password = auth["password"]
    else:
        password = input("input password: ")

    show = config["show"]
    if len(show["title"]) != 0:
        title = show["title"]
    else:
        title = input("input show title: ")

    if len(show["anime"]) != 0:
        anime = show["anime"]
    else:
        anime = input("input show url: ")

    if len(show["Season"]) != 0:
        season = show["Season"]
    else:
        season = input("input show season number: ")

    if len(show["episodeMin"]) != 0:
        episodeMin = show["episodeMin"]
    else:
        episodeMin = input("input episodeMin: ")
    episodeMin = int(episodeMin) #episode numbers are used to iterate a range, so int()

    if len(show["episodeMax"]) != 0:
        episodeMax = show["episodeMax"]
    else:
        episodeMax = input("input episodeMax: ")
    episodeMax =  int(episodeMax)

    if len(show["destination"]) != 0:
        destination = show["destination"]
    else:
        destination = input("input show destination: ")

    params = [user, password, title, anime, season, episodeMin, episodeMax, destination]
    return params


config = get_params()
print(config)
DL = Downloader()
DL.download(config)
