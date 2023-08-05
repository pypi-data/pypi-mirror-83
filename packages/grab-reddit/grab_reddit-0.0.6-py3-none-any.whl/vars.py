"""
@author: RealStickman
"""
from datetime import date
import configparser

#colors for terminal output
CRED = '\033[91m'
CYEL = '\033[33m'
CGRE = '\033[92m'
CEND = '\033[0m'

# variable for configparser
config = ''

# limit
lim = ''
# category
category = ''
# array as read from the config. Used only after first creating the config.
subl = ''
# removed .empty. from subl. This will be written into the config file again.
sublist = ''
# splitting the sublist on ;
sublf = ''
# download path
path = ''
# selected theme for gui
seltheme = ''

# used in download function
# date
date = str(date.today())

# numsubs
numsubs = ''
