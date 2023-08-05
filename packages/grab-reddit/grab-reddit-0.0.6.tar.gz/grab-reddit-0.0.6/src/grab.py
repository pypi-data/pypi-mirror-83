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

# variables
import vars
# modules
import modules

###########
#variables#
###########

#colors for terminal output
CRED = '\033[91m'
CYEL = '\033[33m'
CGRE = '\033[92m'
CEND = '\033[0m'
#define config and read subs
vars.config = configparser.ConfigParser()
#choose default path
pathdef = str(os.path.join(Path.home(), "Downloads", "grab-bot"))

############
#Initialise#
############

try:
    vars.config.read('grab.ini')
    vars.config['CONFIG']['category']
except KeyError:
    vars.config['CONFIG'] = {'limit': '10',
                        'category': 'hot',
                        'subs': '.empty.;',
                        'path': pathdef,
                        'theme': 'light'}
    with open('grab.ini', 'w') as configfile:
        vars.config.write(configfile)
    print("Created default configuration file")
finally:
    modules.readconf()

#################
#Argument parser#
#################

parser = argparse.ArgumentParser(description='CLI-options for grab.py.', formatter_class=argparse.RawDescriptionHelpFormatter)
g = parser.add_argument_group(title='information options',
description =
'''-s, --sub <subreddit>        Add subreddits (Multiple allowed)
-r, --remove <subreddit>    Remove subreddits (Multiple allowed). Program will exit
-l, --lim <limit>           Set the limit of posts  
-c, --category <category>   Set the category
-p, --path <path>           Set the download path
-v, --variables             Shows the configuration file. Program will exit''')

parser.add_help
g.add_argument("-s", "--sub", dest="subreddit", type=str, nargs='+', required=False, help=argparse.SUPPRESS)
g.add_argument("-l", "--lim", dest="limit", type=int, required=False, help=argparse.SUPPRESS)
g.add_argument("-c", "--category", dest="category", type=str, required=False, help=argparse.SUPPRESS)
g.add_argument("-p", "--path", dest="path", type=str, required=False, help=argparse.SUPPRESS)
g.add_argument("-v", "--variables", action="store_true", dest="variables", required=False, help=argparse.SUPPRESS)
g.add_argument("-r", "--remove", dest="removesub", type=str, nargs='+', required=False, help=argparse.SUPPRESS)

args = parser.parse_args()
# print(args.subreddits)

# NOTE Make output of this more beautiful instead of just pasting the config. (Especially subreddits section)
argvars = args.variables
# if this is set, show the config file and exit
if (argvars == True):
    try:
        conffile = open("grab.ini")
        readbackfile = conffile.read()
        print(readbackfile)
        conffile.close()
        exitprog = True
    except:
        print("Could not read grab.ini")
    sys.exit(0)

# Argument for removing subs. Quits after execution.
# TODO Make case insensitive
argrem = args.removesub
if argrem is not None:
    returnsubs = "Removed "
    for s in range(len(argrem)):
        vars.sublist = vars.sublist.replace(";" + argrem[s], '')
        returnsubs = returnsubs + argrem[s] + ", "
    modules.writeconf()
    print(returnsubs)
    sys.exit(0)

argsubs = args.subreddit
#try getting an argument and add that to the list
if argsubs is not None:
    for s in range(len(argsubs)):
        # check if the subreddit is already in the array
        if (argsubs[s] in vars.sublist):
            print(argsubs[s] + " has already been added")
        else:
            try:
                #reddit stuff
                reddit = praw.Reddit(client_id="48VCokBQkKDsEg",
                                     client_secret=None,
                                     user_agent="grab, a Reddit download bot by /u/RealStickman_")

                subreddit = reddit.subreddit(argsubs[s])
                subreddit.title

                #add entered subreddit
                vars.sublist += subreddit.display_name + ";"
                #that's were we're gonna put it
                print("Added " + subreddit.display_name)
            #if the subreddit can't be found
            except prawcore.exceptions.Redirect:
                print("Wrong Subreddit", subreddit.display_name + " does not exist")
else:
    print("No subreddit given")

arglim = args.limit
#try getting a limit
if arglim is not None:
    vars.lim = args.limit
else:
    print("No limit given")

argcategory = args.category
#try getting a category
if argcategory is not None:
    vars.category = args.category
else:
    print("No category given")

argpath = args.path
#try getting a path
if argpath is not None:
    vars.path = args.path
else:
    print("No path given")

modules.writeconf()

modules.readconf()

#number of subreddits that have been specified in the config
#numsubs = len(vars.sublf)

def main():
    #global numsubs
    #global dl
    # number of subreddits
    vars.numsubs = len(vars.sublf)
    #creates a pool of processes
    try:
        p = multiprocessing.Pool(vars.numsubs)
        #processes are started with the arguments contained in the list
        p.map(modules.dl, vars.sublf)
    except ValueError:
        print(vars.CRED + "Please specify a subreddit." + vars.CEND)
    exit(0)

if __name__ == '__main__':
    #main()
    modules.multiprocdl()
