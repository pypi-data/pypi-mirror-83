"""
@author: RealStickman
"""
import configparser
import multiprocessing
import sys
import praw
import prawcore
import requests
import os
from datetime import date
import argparse
from pathlib import Path
from PIL import Image

# import variables
import vars

# read the config file
def readconf():
    print("Reading Config file")
    vars.config.read('grab.ini')
    vars.lim = int(vars.config['CONFIG']['limit'])
    vars.category = vars.config['CONFIG']['category']
    vars.subl = vars.config['CONFIG']['subs']
    vars.sublist = vars.subl.replace('.empty.', '')
    vars.sublf = list(filter(None, vars.sublist.split(';')))
    vars.path = vars.config['CONFIG']['path']
    vars.seltheme = vars.config['CONFIG']['theme']

# Write the configuration file
def writeconf():
    print("Writing config file")
    vars.config['CONFIG'] = {'limit': vars.lim,
                        'category': vars.category,
                        'subs': vars.sublist,
                        'path': vars.path,
                        'theme': vars.seltheme}
    with open('grab.ini', 'w') as configfile:
        vars.config.write(configfile)

# Download stuff from reddit
def dl(subvar):
    # make path choosable
    pathdl = str(os.path.join(vars.path, subvar, vars.date))
    if not os.path.exists(pathdl):
        os.makedirs(pathdl)
    pathtxt = str(os.path.join(vars.path, subvar))
    os.chdir(pathtxt)

    reddit = praw.Reddit(client_id="48VCokBQkKDsEg",
                         client_secret=None,
                         user_agent="grab, a Reddit download bot by /u/RealStickman_")

    # setting subreddit and variable for the first few posts in the hot category of it
    subreddit = reddit.subreddit(subvar)

    if vars.category == 'controversial':
        print(vars.category)
        posts = subreddit.controversial(limit=vars.lim)
    elif vars.category == 'gilded':
        print(vars.category)
        posts = subreddit.gilded(limit=vars.lim)
    elif vars.category == 'hot':
        print(vars.category)
        posts = subreddit.hot(limit=vars.lim)
    elif vars.category == 'new':
        print(vars.category)
        posts = subreddit.new(limit=vars.lim)
    elif vars.category == 'rising':
        print(vars.category)
        posts = subreddit.rising(limit=vars.lim)
    elif vars.category == 'top':
        print(vars.category)
        posts = subreddit.top(limit=vars.lim)
    else:
        print('This category is not implemented or does not exist')

    #test whether the subreddit exists
    try:
        subreddit.title
    except prawcore.exceptions.Redirect:
        print(vars.CRED + subreddit.display_name + " is no subreddit" + vars.CEND)
        return

    #creates downloaded.txt in the subreddit's directory
    try:
        downloaded = open("downloaded.txt")
        print("File exists")
        print("Downloading from " + subreddit.display_name)
    except IOError:
        print("Creating file")
        downloaded = open("downloaded.txt", "w")
        downloaded.write("")
        print("Downloading from " + subreddit.display_name)
    finally:
        downloaded.close()

    #searches the specified number of posts
    for post in posts:
        url = post.url
        filename = post.author.name + " - " + post.title + ".png"
        filetest = post.title
        downloaded = open("downloaded.txt", "r")
        string = str(downloaded.read())
        downloaded.close()
        if filetest not in string:
            print(vars.CGRE + filename + vars.CEND)
            reddit = requests.get(url)
            #download files from reddit
            os.chdir(pathdl)
            try:
                with open(filename, "wb") as file:
                    file.write(reddit.content)
                try:
                    Image.open(filename)
                except:
                    os.remove(filename)
                    print("Removed " + filename + ", because it is not an image.")
            except IOError:
                print("Couldn't find any picture, skipping.")
            #appends the filenames
            os.chdir(pathtxt)
            with open("downloaded.txt", "a") as downloaded:
                downloaded.write(post.title)
                downloaded.write(" ")
        else:
            print(vars.CYEL + filename + " is already present in downloaded.txt" + vars.CEND)

def multiprocdl():
    # number of subreddits
    vars.numsubs = len(vars.sublf)
    #creates a pool of processes
    try:
        p = multiprocessing.Pool(vars.numsubs)
        #processes are started with the arguments contained in the list
        p.map(dl, vars.sublf)
    except ValueError:
        print(vars.CRED + "Please specify a subreddit." + vars.CEND)
    #exit(0)
