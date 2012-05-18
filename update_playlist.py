"""
Watches a XBMC player playlist directory and  
adds any new or changed files to the playlist.

"""

import os.path, string
import glob, random
import xbmc, xbmcgui
from file_watcher import *

playlist_dir =  '/path/to/playlist/'

def changePlaylist (changed_files, removed_files):
    if (changed_files): 
        filename = changed_files[0]
        file_length = len(filename)
        if file_length > 0: 
           pls = xbmc.PlayList(0)
           pls.load(filename)
           xbmc.Player().play(pls)

watch_directories(playlist_dir, changePlaylist, 5.0)

