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
__version__ = "1.0.0"
__documentation__ = "https://janjinda.artstation.com/pages/jj-obj-toolkit-doc"
__email__ = "janjinda@janjinda.com"
__website__ = "http://janjinda.com"

import os

while True:
    # Asks user to input a path to desired directory.
    path = raw_input("What directory do you want to convert? ")

    # If path is draged and dropped it has '', this command removes them.
    path = path if not path.startswith("'") else path[1:-2]

    # If user does not include slash at the end, this command adds it.
    path = path + "/" if not path.endswith("/") else path + ""

    if not os.path.exists(path):
        print ("Path does not exist! Try again.")
        continue
    else:
        break

# Lists files in directory and removes all hidden files
directory = (file for file in os.listdir(path) 
             if os.path.isfile(os.path.join(path, file)))
directory = [filename for filename in directory if not filename.startswith(".")]

class UdimConvert(object):
    """Simple set of methods for renaming file between two udim standards."""
    
    
    
    def uvToUdim(self):
        """Takes u#_v# values and converts them to UDIM."""
        
        # Finds u and v values in last two list items.
        u = (self.filename.split("_")[-2])[1:]
        v = (self.filename.split("_")[-1])[1:]
        
        # Generates new u and v values.
        newU = int(u) if int(u) != 10 else 0
        newV = "%02d" % ((int(v) - 1) if newU != 0 else int(v))
        
        # Puts new u and v together to get UDIM.
        udim = ("1%s%s" % (newV, newU))
        
        # Finds correct file name by removing u#_v# from filename.
        
        filename = self.filename.strip("_u%s_v%s" % (u, v))
        
        # Creates a new filename using previous variables and prints rename results.
        fileNew = ("%s.%s.%s" % (filename, udim, self.suffix))
        print ("%s -> %s" % (self.fileOld, fileNew))

        # Finally renames files.
        os.rename(path + self.fileOld, path + fileNew)
        
    def udimToUv(self):
        """Takes UDIM value and converts it to u#_v#."""
        
        # Finds UDIM value in last 4 characters at the end of filename.
        udim = (self.fileOld.split(".")[-2])[-4:]
        
        # Generates u and v values from UDIM.
        newU = int(udim[-1]) if int(udim[-1]) != 0 else 10
        newV = int(udim[1:3]) + 1 if newU !=10 else int(udim[1:3])

        # Puts new u and v together to form a string.
        uv = ("u%s_v%s" % (newU, newV))
        
        # Finds correct file name by removing UDIM from filename.
        filename = self.filename.strip("_%s" % udim)
        
        # Creates a new filename using previous variables and prints rename results.
        fileNew = ("%s_%s.%s" % (filename, uv, self.suffix))
        print ("%s -> %s" % (self.fileOld, fileNew))
       
        # Finally renames files.
        os.rename(path + self.fileOld, path + fileNew)

    def convertUV(self, type=None):
        """Goes throught the directory list and runs other methods based on user input."""
        
        
        for self.fileOld in directory:
            self.filename = self.fileOld.split(".")[0]
            self.suffix = self.fileOld.split(".")[-1]
            
            if type == 'from':
                self.udimToUv()
            elif type == 'to':
                self.uvToUdim()
            else:
                raise RuntimeError("Wrong conversion type given!")

# Assigns the class to variable.
udimConvert = UdimConvert()

while True:
    # Asks user about conversion type and passes it to convertUV method.
    user = raw_input("Do you want to convert 'from' or 'to' UDIM? ")
    
    if user not in ("from", "to"):
        print ("Please give me valid method!")
        continue
    else:    
        break
udimConvert.convertUV(type=user)
