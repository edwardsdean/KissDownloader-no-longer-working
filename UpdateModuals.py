__author__ = 'Dean'
import pip

try:
    pip.main(['install', '--upgrade', 'BeautifulSoup4'])

except:
    pip.main(['install', 'BeautifulSoup4'])
try:
    pip.main(['install', '--upgrade', 'selenium'])
except:
    pip.main(['install', 'selenium'])
try:
    pip.main(['install', '--upgrade', 'pySmartDL'])
except:
    pip.main(['install', 'pySmartDL'])
