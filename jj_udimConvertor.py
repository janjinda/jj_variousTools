"""
JJ Obj Toolkit is a set of simple scripts tailored to provide clean, easier and more effective
workflow for handling OBJ files in Maya. Thanks to the Import as blend shape options it keeps all your scene
hierarchy, geometry UVs, shader assignments etc.

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
        filename = fileOld.split(".")[0]
        suffix = fileOld.split(".")[-1]

        if type == 'from':
            # Finds UDIM value in last 4 characters at the end of filename.
            udim = fileOld.strip(".%s" % suffix)[-4:]
            
            if not udim.isdigit():
                print ("%s ---> SKIPPED" % fileOld)
                continue
            
            else:
                # Generates u and v values from UDIM.
                u = int(udim[-1]) if int(udim[-1]) != 0 else 10
                v = int(udim[1:3]) + 1 if u != 10 else int(udim[1:3])

                # Puts new u and v together to form a string.
                uv = ("u%s_v%s" % (u, v))

                # Creates a new filename using previous variables and prints rename results.
             
                fileNew = ("%s_%s.%s" % (filename, uv, suffix))
            
        elif type == 'to':

            r = re.compile('^_u\d+_v\d+$')
            if r.match('_%s_%s' % (filename.split('_')[-2], filename.split('_')[-1])) is None:
                print ("%s ---> SKIPPED" % fileOld)
                continue

            else:
                # Finds u and v values in last two list items.         
                u = (filename.split("_")[-2])[1:]
                v = (filename.split("_")[-1])[1:]

                # Generates new u and v values.
                newU = int(u) if int(u) != 10 else 0
                newV = "%02d" % ((int(v) - 1) if newU != 0 else int(v))

                # Puts new u and v together to get UDIM.
                udim = ("1%s%s" % (newV, newU))

                # Creates a new filename using previous variables and prints rename results.
                fileNew = ("%s.%s.%s" % ((filename.strip("_u%s_v%s" % (u, v))), udim, suffix))
            
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
