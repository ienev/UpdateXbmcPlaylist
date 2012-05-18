"""
Watches for new/changed or deleted files in a given directory.
If found a function is called to handle them.

Parameters (paths:[str], func:callable, delay:float)

"""


from __future__ import nested_scopes
import os, time, sys
from os.path import join, getsize


def watch_directories (path, func, delay=1.0):
    
    # "snapshot" of the given directory containing file names 
    # as keys  and modification times as values 
    dir_snapshot = {}

    # populate the snapshot with initial values
    def init (path):
        for root, dirs, files in os.walk(path):
            for filename in files:
              file = os.path.join(root, filename)
              try:
                  t = os.stat(file)
              except os.error:
                continue
              dir_snapshot[file] =  t.st_mtime

    # compare the the current snapshot of the directory with the
    # previous one to find any new/changed or deleted files
    def check_files (dirname, files):
        for filename in files:
            path = os.path.join(dirname, filename)
            try:
                t = os.stat(path)
            except os.error:
                continue
            mtime = old_snapshot.get(path)
            if mtime is not None:
                # remove files from the old snapshot; only deleted files will remain in it
                del old_snapshot[path]
                # if the file has been changed/re-uploaded then the modification time is newer
                if t.st_mtime > mtime:
                    changed_list.append(path)
            else:
                # if no modification time then this is a new file
                changed_list.append(path)
            # replace the old snapshot with the current one
            dir_snapshot[path] = t.st_mtime

    # Main loop
    rescan = False
    init(path)
    while True:
        time.sleep(delay)
        changed_list = []
        deleted_list = []
        old_snapshot = dir_snapshot.copy()
        dir_snapshot = {}
        for root, dirs, files in os.walk(path):
            check_files(root, files)
        deleted_list = old_snapshot.keys()
        if rescan:
            rescan = False
        elif changed_list or deleted_list:
            rescan = func(changed_list, deleted_list)

