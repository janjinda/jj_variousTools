import os
import sys
from random import randint



# Asks user to input a path to desired directory.
if len(sys.argv) <= 2:
    raise IndexError("Missing file path!!!") 

if not os.path.exists(sys.argv[2]):
    raise RuntimeError("File path not valid!!!")
else:
    path = sys.argv[2]
    
# If path is draged and dropped it has '', this command removes them.
path = path if not path.startswith("'") else path[1:-2]

# If user does not include slash at the end, this command adds it.
path = path + "/" if not path.endswith("/") else path + ""

# Lists files in directory and removes all hidden files
directory = os.listdir(path)
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

user = sys.argv[1]
udimConvert.convertUV(type=user)
