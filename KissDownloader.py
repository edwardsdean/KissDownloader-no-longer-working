import pip
import time
import configparser
import os
try:
    from bs4 import BeautifulSoup
except ImportError:
    pip.main(['install', 'BeautifulSoup4'])
try:
    from selenium import webdriver
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.common.keys import Keys
except ImportError:
    pip.main(['install', 'selenium'])
try:
    import pySmartDL
except ImportError:
    pip.main(['install', 'pySmartDL'])




# stuff that I may do... eventually
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
# TODO maybe build downloader as a module? idk man
# TODO simultaneous downloads
# TODO pause downloads
# TODO get video src through video player to avoid the need to login and handle user data   - not possible to get 1080p this way
# TODO support for queueing downloads, will be easy once configs/console launching is supported
#TODO deal with reaching the end of a show


class KissDownloader:
    def __init__(self, params):
        for param in params:
            print(param)
        # create a webdriver instance with a lenient timeout duration
        self.driver = webdriver.Firefox()
        self.driver.set_page_load_timeout(100)
        self.rootPage = ""
        self.file_extension = ""
        self.download(params)

    def login(self, user, pw, site):
        global config
        # go to the site login page
        self.driver.get("http://" + str(site) + "/Login")

        # wait for cloudflare to figure itself out
        time.sleep(10)

        # locate username and password fields in the login page
        username = self.driver.find_element_by_id("username")
        password = self.driver.find_element_by_id("password")

        # type login info into fields
        username.send_keys(user)
        password.send_keys(pw)

        # send the filled out login form and wait
        password.send_keys(Keys.RETURN)
        time.sleep(5)

        # confirm that login was successful and return a bool
        if self.driver.current_url == "http://" + site + "/":
            return True
        else:
            # clear failed login info from config
            config = configparser.ConfigParser()
            config.read("config.ini")
            config["Login"]["username"] = ""
            config["Login"]["password"] = ""

            with open("config.ini", "w") as configfile:
                config.write(configfile)

            return False

    def get_episode_page(self, episode, site):
        # parses the streaming page of an episode from the root page
        soup = BeautifulSoup(self.rootPage, 'html.parser')
        ###for kisscartoon.me

        if site == "kisscartoon.me":
            if episode % 1 == 0:
                ###for non special episodes
                episode = int(episode)
                for link in soup.findAll('a'):
                    currentlink = link.get('href')
                    if currentlink is None:
                        pass
                    elif "/episode-" + str(episode).zfill(3) + "-" in currentlink.lower() or "/episode-" + str(episode).zfill(2) + "-" in currentlink.lower():
                        return ["http://" + site + "" + currentlink.lower(), False]
            else:
                ###for special episodes
                episode = int(episode)
                # uncensored vvv
                for link in soup.findAll('a'):
                    currentlink = link.get('href')
                    if currentlink is None:
                        pass
                    elif "/episode-" + str(episode).zfill(3) + "-5" in currentlink.lower() or "/episode-" + str(episode).zfill(2) + "-5" in currentlink.lower():
                        return ["http://" + site + "" + currentlink.lower(), False]
        else:

            #vvvvvv for kissanime.to / kissasian.com - might seperate if needed
            if episode % 1 == 0:
                ###for non special episodes
                episode = int(episode)
                # uncensored vvv
                for link in soup.findAll('a'):
                    currentlink = link.get('href')
                    if currentlink is None:
                        pass
                    elif "/uncensored-episode-" + str(episode).zfill(3) + "?" in currentlink.lower() or "/uncensored-episode-" + str(episode).zfill(2) + "?" in currentlink.lower() or "/uncen-episode-" + str(episode).zfill(3) + "?" in currentlink.lower() or "/uncen-episode-" + str(episode).zfill(2) + "?" in currentlink.lower() or "/episode-" + str(episode).zfill(3) + "-uncensored?" in currentlink.lower() or "/episode-" + str(episode).zfill(2) + "-uncensored?" in currentlink.lower() or "/episode-" + str(episode).zfill(3) + "-uncen?" in currentlink.lower() or "/episode-" + str(episode).zfill(2) + "-uncen?" in currentlink.lower():
                        return ["http://" + site + "" + currentlink.lower(), True]
                # censored vvv
                for link in soup.findAll('a'):
                    currentlink = link.get('href')
                    if currentlink is None:
                        pass
                    elif "/episode-" + str(episode).zfill(3) + "?" in currentlink.lower() or "/episode-" + str(episode).zfill(2) + "?" in currentlink.lower():
                        return ["http://" + site + "" + currentlink.lower(), False]
            else:
                ###for special episodes
                episode = int(episode)
                # uncensored vvv
                for link in soup.findAll('a'):
                    currentlink = link.get('href')
                    if currentlink is None:
                        pass
                    elif "/uncensored-episode-" + str(episode).zfill(3) + "-5?" in currentlink.lower() or "/uncensored-episode-" + str(episode).zfill(2) + "-5?" in currentlink.lower() or "/uncen-episode-" + str(episode).zfill(3) + "-5?" in currentlink.lower() or "/uncen-episode-" + str(episode).zfill(2) + "-5?" in currentlink.lower() or "/episode-" + str(episode).zfill(3) + "-5-uncensored?" in currentlink.lower() or "/episode-" + str(episode).zfill(2) + "-5-uncensored?" in currentlink.lower() or "/episode-" + str(episode).zfill(3) + "-5-uncen?" in currentlink.lower() or "/episode-" + str(episode).zfill(2) + "-5-uncen?" in currentlink.lower():


                    ############    "/uncensored-episode-" + str(episode).zfill(3) + "-5?" in currentlink.lower() or "/uncensored-episode-" + str(episode).zfill(2) + "-5?" in currentlink.lower() or "/episode-" + str(episode).zfill(3) + "-5-uncensored?" in currentlink.lower() or "/episode-" + str(episode).zfill(2) + "-5-uncensored?" in currentlink.lower():
                        return ["http://" + site + "" + currentlink.lower(), True]
                # censored (normal) vvv
                for link in soup.findAll('a'):
                    currentlink = link.get('href')
                    if currentlink is None:
                        pass
                    elif "/episode-" + str(episode).zfill(3) + "-5?" in currentlink.lower() or "/episode-" + str(episode).zfill(2) + "-5?" in currentlink.lower():
                        return ["http://" + site + "" + currentlink.lower(), False]
        return ["", False]

    def get_video_src(self, page, qual):
        # parses the video source link from the streaming page, currently chooses the highest available quality

        x = True
        while x:
            try:
                self.driver.get(page)
                x = False
            # try again if the page times out
            except TimeoutException:
                print("loading " + page + " timed out, trying again.")
        time.sleep(10)

        currentpage = self.driver.page_source
        soup = BeautifulSoup(currentpage, 'html.parser')

# 16:9 vvv
        if qual in ["1920x1080.mp4"] and soup.findAll('a', string="1920x1080.mp4") != []:
            for link in soup.findAll('a', string="1920x1080.mp4"):
                return [link.get('href'), ".mp4"]
        elif qual in ["1920x1080.mp4", "1280x720.mp4"] and soup.findAll('a', string="1280x720.mp4") != []:
            for link in soup.findAll('a', string="1280x720.mp4"):
                return [link.get('href'), ".mp4"]
        elif qual in ["1920x1080.mp4", "1280x720.mp4", "640x360.mp4"] and soup.findAll('a', string="640x360.mp4") != []:
            for link in soup.findAll('a', string="640x360.mp4"):
                return [link.get('href'), ".mp4"]
        elif qual in ["1920x1080.mp4", "1280x720.mp4", "640x360.mp4", "320x180.3gp"] and soup.findAll('a', string="320x180.3gp") != []:
            for link in soup.findAll('a', string="320x180.3gp"):
                return [link.get('href'), ".3pg"]
# 4:3 vvv
        elif qual in ["1920x1080.mp4", "1280x720.mp4", "640x360.mp4", "320x180.3pg", "960x720.mp4"] and soup.findAll('a', string="960x720.mp4") != []:
            for link in soup.findAll('a', string="960x720.mp4"):
                return [link.get('href'), ".mp4"]
        elif qual in ["1920x1080.mp4", "1280x720.mp4", "640x360.mp4", "320x180.3pg", "960x720.mp4", "480x360.mp4"] and soup.findAll('a', string="480x360.mp4") != []:
            for link in soup.findAll('a', string="480x360.mp4"):
                return [link.get('href'), ".mp4"]
        elif qual in ["1920x1080.mp4", "1280x720.mp4", "640x360.mp4", "320x180.3pg", "960x720.mp4", "480x360.mp4", "320x240.3pg"] and soup.findAll('a', string="320x240.3pg") != []:
            for link in soup.findAll('a', string="320x240.3pg"):
                return [link.get('href'), ".3pg"]
        else:
            return False

    def download_video(self, url, name, destination):
        #makes sure the directory exists
        try:
            os.stat(destination)
        except:
            os.mkdir(destination)

        filename = name
        path = destination + filename
        obj = pySmartDL.SmartDL(url, destination, progress_bar=False, fix_urls=True)
        obj.start(blocking=False)
        location = obj.get_dest()

        while True:
            if obj.isFinished():
                break
            print(name + "\t " + str(float("{0:.2f}".format((float(obj.get_progress())*100)))) + "% done at " + pySmartDL.utils.sizeof_human(obj.get_speed(human=False)) + "/s")
            #*epiode name* 0.38% done at 2.9 MB/s
            time.sleep(1)
        if obj.isFinished():
            os.rename(location, path)
        else:
            print("Download of " + name + " failed")
        return path

    def close(self):
        # closes the browser window, may be used for other program-ending tasks later on
        self.driver.close()

    def frange(self, start, stop, step):
        i = start
        while i < stop:
            yield i
            i += step

    def zpad(self, val, n):
        bits = val.split('.')
        return "%s.%s" % (bits[0].zfill(n), bits[1])

    def download(self, p):
        episode_list = []

        #p = [user, password, title, anime, season, episode_min, episode_max, destination, quality, site]
        # takes a list of parameters and uses them to download the show
        l = self.login(p[0], p[1], p[9])  # 0 are the indices of the username and password from get_params()
        while not l:
            print("login failed, try again")
            l = self.login(p[0], p[1])

        self.driver.get(p[3])  # 3 is the index of the url
        time.sleep(10)

        self.rootPage = self.driver.page_source
        print("Getting episode urls please wait")
        for e in self.frange(float(p[5]), int(p[6])+1, 0.5):  # 5 and 6 are episodes min and max
            page = self.get_episode_page(e, p[9])
            # page = [page_url, isUncensored]
            if page[0] == "":
                pass
            else:
                video = self.get_video_src(page[0], p[8]) #8 is the quality
                # video = [url, file_extension]
                if isinstance(video[0], str):
                    if page[1]:  # if episode is called uncensored
                        if e % 1 == 0:
                            e = int(e)
                            filename = p[2] + " S" + str(p[4].zfill(2)) + "E" + str(e).zfill(3) + " Uncensored" + video[1]  # 2 is the title, 4 is the season
                        else:
                            filename = p[2] + " S" + str(p[4].zfill(2)) + "E" + self.zpad(str(e), 3) + " Uncensored" + video[1]  # 2 is the title, 4 is the season
                    else:
                        if e % 1 == 0:
                            e = int(e)
                            filename = p[2] + " S" + str(p[4].zfill(2)) + "E" + str(e).zfill(3) + video[1]  # 2 is the title, 4 is the season
                        else:
                            filename = p[2] + " S" + str(p[4].zfill(2)) + "E" + self.zpad(str(e), 3) + video[1]  # 2 is the title, 4 is the season
                    print("Got link for " + filename)
                    episode_list.append((video[0], filename, p[7]))
                else: ("no link for episode " + str(e))
        self.driver.close()
        for tuple in episode_list:
            url = tuple[0]
            filename = tuple[1]
            destination = tuple[2]
            self.download_video(url, filename, destination)
            print("downloaded ", filename)
        print("done downloading " + p[2] + " Season " + p[4])


if __name__ == "__main__":
    #params = [user, password, title, anime, season, episode_min, episode_max, destination, quality, site]
    print('please run from KissDownloaderGUI.py')