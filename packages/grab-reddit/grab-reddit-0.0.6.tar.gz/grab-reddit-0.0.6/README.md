# grab - a Reddit download bot

This is a simple Python script to download submissions containing images from any specified subreddit.  
All images are placed in the ~/Downloads/grab-bot/[subreddit]/[date] by default. The download path however can be changed through the GUI or config file.  
"grab.ini" is the configuration file used by the program. It will be generated with default values in case it is not present when the program is run. This file will be created in your home directory.  
"downloaded.txt" lists all previously downloaded images from their subreddit. This was done to avoid downloading images multiple times in an effort to save bandwidth and make subsequent executions of the program faster.  

*This program is currently Linux-only. Windows has not yet been tested, but support is planned for the future.*  

## Table of Contents

1. [TODO](#todo)
2. [How to use](#howto)
3. [Installation](#install)
    1. [Arch](#instarch)
    2. [Debian](#instdeb)
    3. [Fedora](#instfed)
4. [Known Bugs](#bugs)
5. [Cron](#cron)

## TODO <a name="todo"></a>

- [X] GUI for selecting subreddits
- [X] Change download location through GUI
- [X] Change the download limit
- [X] Change the category
- [X] CLI option for launching the gui. Done through grab-reddit-gui.
- [ ] Make the GUI look better
- [X] Create CLI options for grab.py to create config files in the terminal 
- [ ] Automatically schedule program execution (Can be done manually with cron)


## How to use <a name="howto"></a>

Follow the [installation instructions](#install).  
To add subreddits open the gui, click on the "+" Button and type in the subreddit you want to add.  
To remove a subreddit, select one from the list and click on the "-" in the top right. Click yes in the following dialog.  
Clicking ">" will expand the window to change the category, limit and download path. Clicking "Run" in the GUI will execute grab.py.  
The theme can be changed by clicking on "light" or "dark". The dark theme is still work in progress.  

To run the program in the terminal use `grab-reddit <args>`. If you want the gui version, run `grab-reddit-gui`.  
Help for arguments taken by `grab-reddit` can be found by executing `grab-reddit -h`.  

Setting up cron for repeated executions is [covered below](#cron).

## Installation <a name="install"></a>

To install all requirements follow the instructions for your distribution shown below.  

### Arch <a name="instarch"></a>

`sudo pacman -S python-pip tk`  
`sudo pip install grab-reddit`  

Installing locally to the user does not work currently, as the directory is not inside of PATH.  
`pip install --user grab-reddit`  

### Debian <a name="instdeb"></a>

`sudo apt-get install python3-pip python3-tk`  
`pip3 install grab-reddit`  

### Fedora <a name="instfed"></a>

`sudo dnf install python3 python3-wheel python3-tkinter`  
`pip install --user grab-reddit`  

To use the CLI run `grab-reddit <args>`. For the gui version use `grab-reddit-gui`.  

## Known Bugs <a name="bugs"></a>

1. ~~Some images can't be opened.~~ Fixed by using Pillow to check images after the download.
2. ~~Can't currently click "Run" in the GUI and have the program work in Debian. Launching grab.py directly works.~~ Fixed in Commit 2538a8fefe17755868b2fbd0e01d43aa7411b58f
3. After changing the theme the exit button does not return the command prompt.

## Cron <a name="cron"></a>

*Outdated*

Change the directory to the location where the grab.py file is located and execute it with python. In Debian you have to specify python3 instead of python. The change of location is done to make sure the program is initialized with the working directory where the .subr files are located.  
`cd /<directory> && python grab.py`  

Example setup for hourly execution  
`0 * * * * cd /home/<user>/scripts && python grab.py`
