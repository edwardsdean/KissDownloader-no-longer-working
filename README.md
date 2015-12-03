# KissDownloader
Downloads shows from Kissanime.to
Currently uses selenium to navigate the site,
beautifulsoup to parse the html,
and pySmartDL to download the files.

To use the script just run the .py file in the same directory as the config.
you need to have the following installed to run:


-python 3.4 and up [Download Here](https://www.python.org/downloads/)

-python modules Beautifulsoup, selenium, pySmartDL, configparser, pip
note: these modules should auto install if you have pip installed which is installed by default on python 3.4 and up

-firefox web browser [Download Here](https://www.mozilla.org/en-GB/firefox/desktop/)


The script may work on other platforms, but has been tested on windows 7 and windows 10, this has also been tested on Mac.

Note: This works best with your default player set to flash, and auto play turned off

For Mac users change the config file destination to look like 
```
destination = /Users/HomeUser/Desktop/Anime/
```