import pip
import time
import configparser
import os
try:
    pip.main(['install', '--upgrade', 'pip'])
except:
    pass
try:
    from bs4 import BeautifulSoup
except ImportError:
    pip.main(['install', 'BeautifulSoup4'])
    from bs4 import BeautifulSoup
try:
    import pySmartDL
except ImportError:
    pip.main(['install', 'pySmartDL'])
    import pySmartDL

try:
    pip.main(['install', '--upgrade', 'cfscrape'])
    import cfscrape
except:
    pip.main(['install', 'cfscrape'])
    import cfscrape




# stuff that I may do... eventually
# TODO error management
# TODO standalone package
# TODO confirm a successful login
# TODO fancy logging
# TODO edit config to keep track of downloaded episodes
# TODO filename customization, with config
# TODO a fancy gui
# TODO support for starting the script with command line args
# TODO maybe build downloader as a module? idk man
# TODO simultaneous downloads
# TODO pause downloads
# TODO get video src through video player to avoid the need to login and handle user data   - not possible to get 1080p this way
# TODO support for queueing downloads, will be easy once configs/console launching is supported
# TODO deal with reaching the end of a show


class KissDownloader:
    def __init__(self, params):
        for param in params:
            print(param)
        # create a webdriver instance with a lenient timeout duration
        self.scraper = cfscrape.create_scraper()

        self.rootPage = ""
        self.file_extension = ""
        self.debug_mode = False

        self.download(params)



    def login(self, user, pw, site):
        global config
        # define login page
        login_url = "http://" + str(site) + "/Login"

        #define user and pass
        username = user
        password = pw

        #define payload
        payload = {
            'username': username,
            'password': password
        }

        #login
        self.scraper.get(login_url)
        login = self.scraper.post(login_url, data=payload)

        if self.debug_mode:
            print(login.url)

        # confirm that login was successful and return a bool
        if str(login.url).lower() == "https://" + site + "/login" or str(login.url).lower() == "http://" + site + "/login":
            return False
        else:
            return True

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
                    elif "episode-" + str(episode).zfill(3) + "-" in currentlink.lower() or "episode-" + str(episode).zfill(2) + "-" in currentlink.lower():
                        return ["http://" + site + "" + currentlink.lower(), False]
            else:
                ###for special episodes
                episode = int(episode)
                # uncensored vvv
                for link in soup.findAll('a'):
                    currentlink = link.get('href')
                    if currentlink is None:
                        pass
                    elif "episode-" + str(episode).zfill(3) + "-5" in currentlink.lower() or "episode-" + str(episode).zfill(2) + "-5" in currentlink.lower():
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
                    elif "uncensored-episode-" + str(episode).zfill(3) + "?" in currentlink.lower() or "uncensored-episode-" + str(episode).zfill(2) + "?" in currentlink.lower() or "uncen-episode-" + str(episode).zfill(3) + "?" in currentlink.lower() or "uncen-episode-" + str(episode).zfill(2) + "?" in currentlink.lower() or "episode-" + str(episode).zfill(3) + "-uncensored?" in currentlink.lower() or "episode-" + str(episode).zfill(2) + "-uncensored?" in currentlink.lower() or "episode-" + str(episode).zfill(3) + "-uncen?" in currentlink.lower() or "episode-" + str(episode).zfill(2) + "-uncen?" in currentlink.lower():
                        return ["http://" + site + "" + currentlink.lower(), True]
                # censored vvv
                for link in soup.findAll('a'):
                    currentlink = link.get('href')
                    if currentlink is None:
                        pass
                    elif "episode-" + str(episode).zfill(3) + "?" in currentlink.lower() or "episode-" + str(episode).zfill(2) + "?" in currentlink.lower():
                        return ["http://" + site + "" + currentlink.lower(), False]
                # weird urls
                for link in soup.findAll('a'):
                    currentlink = link.get('href')
                    if currentlink is None:
                        pass
                    elif "episode-" + str(episode).zfill(3) + "-" in currentlink.lower() or "episode-" + str(episode).zfill(2) + "-" in currentlink.lower():
                        return ["http://" + site + "" + currentlink.lower(), False]
                # experimental urls
                for link in soup.findAll('a'):
                    currentlink = link.get('href')
                    if currentlink is None:
                        pass
                    else:
                        currentlinkx = currentlink.lower()
                        episodex = 0
                        # print(currentlink)
                        if ("/anime/" in currentlinkx):
                            currentlinkx = currentlinkx.replace("/anime/", "")
                            animetitle = currentlinkx.split("/", 1)
                            for item in animetitle:  # get last item
                                episodexx = item
                            if animetitle[0] + "-" in episodexx:
                                episodex = episodexx.replace(animetitle[0] + "-", "")
                                if self.debug_mode:
                                    print("found [" + episodex + "]")
                                episodex = episodex.split("-")[0]
                        try:
                            if (float(episodex) and float(episodex) > 0 and float(episodex) == float(episode)):
                                return ["http://" + site + "" + currentlink.lower(), False]
                            else:
                                pass
                        except ValueError:
                            print("invalid episode")
            else:
                ###for special episodes
                episode = int(episode)
                # uncensored vvv
                for link in soup.findAll('a'):
                    currentlink = link.get('href')
                    if currentlink is None:
                        pass
                    elif "uncensored-episode-" + str(episode).zfill(3) + "-5?" in currentlink.lower() or "uncensored-episode-" + str(episode).zfill(2) + "-5?" in currentlink.lower() or "uncen-episode-" + str(episode).zfill(3) + "-5?" in currentlink.lower() or "uncen-episode-" + str(episode).zfill(2) + "-5?" in currentlink.lower() or "episode-" + str(episode).zfill(3) + "-5-uncensored?" in currentlink.lower() or "episode-" + str(episode).zfill(2) + "-5-uncensored?" in currentlink.lower() or "episode-" + str(episode).zfill(3) + "-5-uncen?" in currentlink.lower() or "episode-" + str(episode).zfill(2) + "-5-uncen?" in currentlink.lower():
                        return ["http://" + site + "" + currentlink.lower(), True]
                # censored (normal) vvv
                for link in soup.findAll('a'):
                    currentlink = link.get('href')
                    if currentlink is None:
                        pass
                    elif "episode-" + str(episode).zfill(3) + "-5?" in currentlink.lower() or "episode-" + str(episode).zfill(2) + "-5?" in currentlink.lower():
                        return ["http://" + site + "" + currentlink.lower(), False]
                # weird urls
                for link in soup.findAll('a'):
                    currentlink = link.get('href')
                    if currentlink is None:
                        pass
                    elif "episode-" + str(episode).zfill(3) + "-5" in currentlink.lower() or "episode-" + str(episode).zfill(2) + "-5" in currentlink.lower():
                        return ["http://" + site + "" + currentlink.lower(), False]
        return ["", False]

    def get_video_src(self, episode_page, qual):
        # parses the video source link from the streaming page, currently chooses the highest available quality

        x = True
        while x:
            try:
                page = self.scraper.get(episode_page)
                if self.debug_mode:
                    pass
                    # print(page.url)
                    # print(page.text)
                scraper_url = page.url
                if "Special/AreYouHuman?" in str(scraper_url):
                    print("please click url and prove your human")
                    print(page.url)
                    input("Press Enter to continue...")
                    print("please wait for system to refresh")
                    time.sleep(10)
                else:
                    x = False
            # try again if the page times out
            except:
                print("loading " + episode_page + " timed out, trying again.")
                time.sleep(5)
        time.sleep(1)
        currentpage = page.content
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
            return ["false", ""]

    def download_video(self, url, name, destination):
        #makes sure the directory exists
        try:
            os.stat(destination)
        except:
            os.makedirs(destination)

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
            time.sleep(3)
            os.rename(location, path)
        else:
            print("Download of " + name + " failed")
        return path

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
        print("Logging in Please Wait")
        l = self.login(p[0], p[1], p[9])  # 0 are the indices of the username and password from get_params()
        login_count = 0
        while not l:
            if login_count > 3:
                print("Login Failed")
                break
            print("login failed, try again")
            l = self.login(p[0], p[1], p[9])
            login_count = login_count + 1

        time.sleep(3)
        self.rootPage = self.scraper.get(p[3]).content  # 3 is the index of the url
        time.sleep(3)


        print("Getting episode urls please wait")
        for e in self.frange(float(p[5]), int(p[6])+1, 0.5):  # 5 and 6 are episodes min and max
            if self.debug_mode:
                print("-----------------")
                print("trying to get link for episode " + str(e))

            page = self.get_episode_page(e, p[9])
            # page = [page_url, isUncensored]
            if page[0] == "":
                pass
            else:
                video = self.get_video_src(page[0], p[8]) #8 is the quality
                # video = [url, file_extension]
                if video[0] != 'false':
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
                else: print("Unable to link for episode " + str(e) + " trying increasing the quality")
        if self.debug_mode:
            print(episode_list)
            #logs url list
            f = open('log.txt', 'w')
            f.write(str(episode_list) + '\n')
            f.close()


        for tuple in episode_list:
            url = tuple[0]
            filename = tuple[1]
            destination = tuple[2]
            if self.debug_mode:
                print("Download:")
                print(filename, url, destination)
                self.download_video(url, filename, destination)
            else:
                self.download_video(url, filename, destination)
            print("downloaded ", filename)
        print("done downloading " + p[2] + " Season " + p[4])


if __name__ == "__main__":
    #params = [user, password, title, anime, season, episode_min, episode_max, destination, quality, site]
    print('please run from KissDownloaderGUI.py')
    KissDownloader
    episodes_list = []
    for tup in episodes_list:
        url = tup[0]
        filename = tup[1]
        destination = tup[2]
        KissDownloader.download_video(KissDownloader, url, filename, destination)