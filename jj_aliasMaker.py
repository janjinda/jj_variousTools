"""JJ Alias Maker (janjinda@janjinda.com)

Simple script for creating aliases inside your system. It asks you for
a name for your alias and for a command which you would like to run 
with it.

Example:
    Type this in your terminal to launch the script::

        $ python /u/jj/Scripts/jj_aliasMaker.py

Todo:
    * add automatic system check
    * import platform   
    * print platform.system()
    * macos returns "Darwin"

"""

import sys
import getpass
w
# Asks user to input desired alias and it's command.
alias = raw_input("Give me alias: ")
command = raw_input("Give me command: ")

    
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
    pathLinux = "/u/%s/.bashcshrc" % (user)
    pathMac = "/Users/%s/.profile" % (user)
    path = pathLinux if not os == 'macos' else pathMac
    
    # Defines what to look for in opened file.
    lookup = '### Aliases'
    
    # Defines format of a line, which will be added to file. 
    insertLinux = 'alias %s "%s"' % (alias, command)
    insertMac = 'alias %s="%s"' % (alias, command)
    insert = insertLinux if not os == 'macos' else insertMac

    # Reads content of file and assigns it to variable.
    with open(path, "r") as in_file:
        content = in_file.readlines()

    # Adds line into stored content and writes the file with new content.
    with open(path, "w") as out_file:
        for line in content:
            if line == lookup + "\n":
                line = line + insert + "\n"
            out_file.write(line)
    
    # Printing addition result.
    print (insert + "-- CREATED SUCCESSFULY.")
    
    return insert

# Calling function.
makeAlias(os='linux')
