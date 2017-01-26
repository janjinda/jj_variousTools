"""JJ Alias Maker (janjinda@janjinda.com)

Simple script for creating aliases inside your system. It takes two arguements
as an input for a name for your alias and for a command which you would like to run 
with it.

Example:
    Type this in your terminal to launch the script::

        $ python /u/jj/Scripts/jj_aliasMaker_argv.py alias 'command'

Todo:
    * add automatic system check
    * import platform   
    * print platform.system()

"""

import sys
import getpass
import platform

# Checks if there are correct arguments given in terminal.
try:
    if len(sys.argv) < 3:
        raise IndexError()
    
    elif len(sys.argv) > 3:
        raise ValueError()
        
    else:
        
        # If there are correct arguments, stores them to variables.
        alias = sys.argv[1]
        command = sys.argv[2]

# If there is wrong argument format raises an error based on a mistake.        
except IndexError:
    print ("Not enough arguments!")
    sys.exit()
except ValueError:
    print ("Please write command in 'quotes'.")
    sys.exit()


def makeAlias(os = None):

    """
    Function adds a line defining new alias into the system.

    Args:
        os (str): Operating system - 'linux' or 'macos'.
        
    Returns:
        str: Newly created alias.

    """
    
    # Finds current username to be passed as folder name.
    user = getpass.getuser()
    
    # Defining paths for saving aliases based on os.
    pathLinux = "/u/%s/.mycshrc" % (user)
    pathMac = "/Users/%s/.profile" % (user)
    path = pathLinux if os == "linux" else pathMac
    
    # Defines what to look for in opened file.
    lookup = '### Aliases'
    
    # Defines format of a line, which will be added to file. 
    insertLinux = 'alias %s "%s"' % (alias, command)
    insertMac = 'alias %s="%s"' % (alias, command)
    insert = insertLinux if os == "linux" else insertMac

    # Reads content of file and assigns it to variable.
    with open(path, "r") as in_file:
        content = in_file.readlines()

    # Adds line into stored content and writes the file with new content.

    if os == "linux":
        with open(path, "w") as out_file:
            for line in content:
                if line == lookup + "\n":
                    line = line + insert + "\n"
                out_file.write(line)
    else:
        with open(path, "a") as out_file:
            line = insert + "\n"
            out_file.write(line)

    # Printing addition result.
    print (insert + "-- CREATED SUCCESSFULY.")
    
    return insert

# Calling function.
os = platform.system()
makeAlias(os=os)
