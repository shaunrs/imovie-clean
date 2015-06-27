#!/usr/bin/env python

# Clean iMovie
# Copyright (c)2015 Shaun Smith.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


#

import os
import sys
import time

# If we can use psutil, great. If not, fall back to subprocess 'ps'
try:
    import psutil
except ImportError:
    import subprocess
    import re

try:
    from os import scandir, walk
except ImportError:
    try:
        from scandir import scandir, walk
    except ImportError:
        print "\033[93;1mWARNING: Using os.walk() because scandir() is not available, this will be much slower.\033[0m"
        from os import walk


def main():


    _start_time = time.time()

    MoviesFolder = "~/Movies/"
    iTunesLibrary = "~/Music/iTunes/iTunes Media/Music"
    iMovieLibrary = "~/Movies/iMovie Library.imovielibrary/"

    # Make sure we are using absolute paths, and expand our home directory
    MoviesFolder = os.path.expanduser(MoviesFolder)
    MoviesFolder = os.path.abspath(MoviesFolder)

    iTunesLibrary = os.path.expanduser(iTunesLibrary)
    iTunesLibrary = os.path.abspath(iTunesLibrary)

    iMovieLibrary = os.path.expanduser(iMovieLibrary)
    iMovieLibrary = os.path.abspath(iMovieLibrary)


    # Get a list of Movie files at the source
    sys.stdout.write("Building Source Movie file list..")
    _x=time.time()
    srcMoviesList = getSrcDirList(MoviesFolder)
    _y=time.time()
    print "  [Done] - " + str(round(_y-_x,2)) + " seconds"


    # Get a list of Music files in iTunes
    _x=time.time()
    sys.stdout.write("Building Source Music file list..")
    srcMusicList = getSrcDirList(iTunesLibrary)
    _y=time.time()
    print "  [Done] - " + str(round(_y-_x,2)) + " seconds"

    # Merge Movies and Music for parsing
    srcFileList = srcMoviesList + srcMusicList


    #for _f in srcFileList:
    #    print _f


    #sys.exit()
    # Parse the iMovie directory
    print "\nProcessing iMovie Library.."
    #parseIMovieDirectory(iMovieLibrary, srcFileList)
    parseIMovieDirectory(iMovieLibrary, srcMoviesList)

    _end_time = time.time()

    print "\n[Finished] in " + str(round(_end_time-_start_time,2)) + " seconds"


def iMovieRunning():
    # First, try with psutil
    try:
        for _p in psutil.process_iter():
            if _p.name() == 'iMovie':
                return True
    # then use Popen using ps command
    except NameError:
        s = subprocess.Popen(["ps", "awx"], stdout=subprocess.PIPE)

        for _line in s.stdout:
            if re.search('iMovie$', _line):
                return True

    return False


def printError(msg):
    print "\033[91;1mERROR: " + msg + "\033[0m"



def getSrcDirList(directory):

    # Ensure we can read this directory
    if not os.path.exists(directory):
        printError("The directory " + directory + " could not be read")
        sys.exit(10)

    _filelist = []

    # For each file in the source directory..
    for root, dirs, files in os.walk(directory, followlinks=True):

        # If the directory is our iMovie Library, skip it - we don't want circular links
        # This also catches iMovie Theater
        if "iMovie " in root:
            #print "SRC Scan - Skipping " + root
            continue

        for _filename in files:
            if _filename.lower().endswith(filetypes):

                # Append this file to the list
                _index = _filename

                _temp = {}
                _temp['filename'] = _filename
                _temp['fqpath'] = os.path.join(root, _filename)

                _temp['size'] = os.path.getsize(os.path.join(root, _filename))

                _filelist.append(_temp)

    #for _entry in _filelist:
    #    print str(_entry)

    return _filelist



def parseIMovieDirectory(directory, _rawFileList):

    # Ensure we can access this directory
    if not os.path.exists(directory):
        printError("The directory " + directory + " could not be read")
        sys.exit(10)

    # For each directory
    for root, dirs, files in os.walk(directory, followlinks=False):

        # If this is an 'original media' directory, we should process files
        if root.endswith('Original Media'):

            # For each file in this directory..
            for _filename in files:

                # Make sure it is an actual file (i.e. we haven't already symlinked it)
                if not os.path.islink(os.path.join(root, _filename)):

                    # Get the 'event' name from iMovie project (for display only)
                    _root_parts = root.split('/')
                    _imovie_event_name = _root_parts[-2]

                    print "  Searching for source: " + _imovie_event_name + " // " + _filename

                    # Find the filesize, to verify we are linking to the correct source
                    _filesize = os.path.getsize(os.path.join(root, _filename))

                    # Iterate over each source file info..
                    for _rawFile in _rawFileList:
                        # Check the filename, and size to match
                        if _rawFile['filename'].lower() == _filename.lower() and _rawFile['size'] == _filesize:
                            print "    Found link to: " + _rawFile['fqpath']

                            # Delete the iMovie file
                            #os.remove(os.path.join(root, _filename))

                            # Symlink the rawfile in
                            #os.symlink(_rawFile['fqpath'], os.path.join(root, _filename))

                            break
                    else:
                        print "    Source file not found!"




if __name__ == "__main__":

    if iMovieRunning():
        print "Cannot run, please close iMovie first.."

        sys.exit(50)

    filetypes = ('mp4', 'mov', 'mp3')

    main()
