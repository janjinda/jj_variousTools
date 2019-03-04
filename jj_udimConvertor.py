"""
JJ UDIM Convertor

Installation
============


Copy jj_objToolkit.py from the zip file to your scripts folder. Usually at these locations ():


Windows - \<user's directory>\My Documents/Maya\<version>\scripts

MacOs - /Users/<user's directory>/Library/Preferences/Autodesk/maya/<version>/scripts

Linux - $MAYA_APP_DIR/Maya/<version>/scripts


Run following script or make a shelf button with following script.


import jj_objToolkit
jj_objToolkit.showUI()

"""

__author__ = "Jan Jinda"
__version__ = "0.0.1"
__documentation__ = "https://janjinda.artstation.com/pages/jj-obj-toolkit-doc"
__email__ = "janjinda@janjinda.com"
__website__ = "http://janjinda.com"

import os
import re

while True:
    # Asks user to input a path to desired directory.
    path = raw_input("What directory do you want to convert? ")

    # If path is dragged and dropped it has '', this command removes them.
    path = path if not path.startswith("'") else path[1:-2]

    # If user does not include slash at the end, this command adds it.
    path = path + "/" if not path.endswith("/") else path + ""

    if not os.path.exists(path):
        print ("Path does not exist! Try again.")
        continue
    else:
        break

# Lists files in directory and removes all hidden files
directory = sorted((file for file in os.listdir(path)
            if os.path.isfile(os.path.join(path, file))))
directory = [filename for filename in directory if not filename.startswith(".")]


def convertUV(type=None):
    """Goes throught the directory list and runs other methods based on user input."""

    for fileOld in directory:
        suffix = fileOld.split(".")[-1]
        filename = fileOld.strip('.%s' % suffix)

        if type == 'from':
            # Finds UDIM value in last 4 characters at the end of filename.
            udim = filename[-4:]
            
            r = re.compile('\d{4}')
            if r.match(udim) is None:
                print ("%s ---> SKIPPED" % fileOld)
                continue
            
            else:
                # Generates u and v values from UDIM.
                u = int(udim[-1]) if int(udim[-1]) != 0 else 10
                v = (int(udim[0:3]) + 1 - 100) if u != 10 else (int(udim[0:3]) - 100)

                # Creates a new filename using previous variables and prints rename results.
             
                fileNew = ("%s_u%s_v%s.%s" % (filename.strip(udim)[:-1], u, v, suffix))
            
        elif type == 'to':

            r = re.compile('.+\_u\d+_v\d+$')
            if r.match(filename) is None:
                print ("%s ---> SKIPPED" % fileOld)
                continue

            else:
                # Finds u and v values in last two list items.         
                u = int((filename.split("_")[-2])[1:])
                v = int((filename.split("_")[-1])[1:])

                if u > 10:
                    print ("%s ---> SKIPPED" % fileOld)
                    continue

                else:
                    # Generates new u and v values.
                    udimU = u if u != 10 else 0
                    udimV = ('%02d' % (v - 1 + 100)) if udimU != 0 else (v + 100)

                    # Creates a new filename using previous variables and prints rename results.
                    fileNew = ("%s.%s%s.%s" % ((filename.strip("_u%s_v%s" % (u, v))), udimV, udimU, suffix))
            
        else:
            raise RuntimeError("Wrong conversion type given!")
        
        # Creates a new filename using previous variables and prints rename results.
        print ("%s ---> %s" % (fileOld, fileNew))

        # Finally renames files.
        os.rename(path + fileOld, path + fileNew)

while True:
    # Asks user about conversion type and passes it to convertUV method.
    user = raw_input("Do you want to convert 'from' or 'to' UDIM? ")

    if user not in ("from", "to"):
        print ("Please give me valid method!")
        continue
    else:
        break

convertUV(type=user)
