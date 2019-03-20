"""
JJ UDIM Converter is a simple system shell script for batch renaming texture files
from _uU_vV sequence format (e.g. from Mudbox) to a more common UDIM format (e.g. ZBrush, Mari) and vice versa.

Installation
============
Copy the script to your own preffered location.


Windows - You have to install Python 2.7.x, if you don't have it on your system already (https://www.python.org/downloads)

macOS - No need of Python installation

Linux - No need of Python installation


Usage
=====
Run following commands and follow on screen instructions:


Windows (Command Line) - C:\Python27\python.exe <path to the script>\jj_udim_converter.py

macOS (Terminal) - python <path to the script>/jj_udim_converter.py

Linux (Terminal) - python <path to the script>/jj_udim_converter.py


"""

__author__ = "Jan Jinda"
__version__ = "1.0.0"
__documentation__ = "http://janjinda.artstation.com/pages/jj-udim-converter-doc"
__email__ = "janjinda@janjinda.com"
__website__ = "http://janjinda.com"

import os
import re

while True:
    # Asks user to input a path to desired directory
    path = raw_input("What directory do you want to convert? ")

    # If path is dragged and dropped it has '', this command removes them
    path = path if not path.startswith("'") else path[1:-2]

    # If user does not include slash at the end, this command adds it
    path = path + "/" if not path.endswith("/") else path + ""
    
    # If path does not exist ask again
    if not os.path.exists(path):
        print ("Path does not exist! Try again.")
        continue
    else:
        break

# Lists files in directory and removes all hidden files
directory = sorted((file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))))
directory = [filename for filename in directory if not filename.startswith(".")]


def convertUDIM(type=None):
    """Main function converts UDIM to _uU_vV and vice versa
    Parameters:
        type (string): type of conversion
       
    Returns:
        filesNew (string): name of renamed file
    """

    for fileOld in directory:
        # Creates variables for suffix and filename
        suffix = fileOld.split(".")[-1]
        filename = fileOld.strip('.%s' % suffix)
        filesNew = []
        separator = ' ---> '

        if type == 'from':
            # Conversion from UDIM format (e.g. 1001)
            # Finds UDIM value in last 4 characters at the end of filename
            udim = filename[-4:]

            # Checks if udim variable is a valid UDIM format
            r = re.compile('\d{4}')
            if r.match(udim) is None or int(udim) == 1000:
                print ("%s%sSKIPPED" % fileOld, separator)
                continue
                        
            else:
                # Generates u and v values from udim
                u = int(udim[-1]) if int(udim[-1]) != 0 else 10
                v = (int(udim[0:3]) + 1 - 100) if u != 10 else (int(udim[0:3]) - 100)

                # Creates a new filename using previous variables and prints rename results
                fileNew = ("%s_u%s_v%s.%s" % (filename.strip(udim)[:-1], u, v, suffix))
            
        elif type == 'to':
            # Conversion from _uU_vV format (e.g. _u1_v1)
            # Checks if the _uU_vV at the end of filename is valid
            r = re.compile('.+\_u\d+_v\d+$')
            if r.match(filename) is None:
                print ("%s%sSKIPPED" % fileOld, separator)
                continue

            else:
                # Finds u and v values in last two list items     
                u = int((filename.split("_")[-2])[1:])
                v = int((filename.split("_")[-1])[1:])
                # Checks if u,v values are valid
                if u == 0 or u > 10 or v==0:
                    print ("%s%sSKIPPED" % fileOld, separator)
                    continue

                else:
                    # Generates udimU and udimV values for UDIM format generation
                    udimU = u if u != 10 else 0
                    udimV = ('%02d' % (v - 1 + 100)) if udimU != 0 else (v + 100)

                    # Creates a new filename using given variables
                    fileNew = ("%s.%s%s.%s" % ((filename.strip("_u%s_v%s" % (u, v))), udimV, udimU, suffix))
            
        else:
            raise RuntimeError("Wrong conversion type given!")
        
        # Prints rename results
        print ("%s ---> %s" % (fileOld, fileNew))

        # Finally renames files
        os.rename(path + fileOld, path + fileNew)
        
        # Appends new filename to a list
        filesNew.append(fileNew)

    return filesNew

while True:
    # Asks user about conversion type and passes it to convertUV method
    user = raw_input("Do you want to convert 'from' or 'to' UDIM format? ")

    if user not in ("from", "to"):
        print ("Please give me valid method.")
        continue
    else:
        break

convertUV(type=user)
