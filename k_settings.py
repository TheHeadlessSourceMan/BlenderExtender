#!/usr/bin/env python
#!BPY

"""
Reads settings from a .ini file, a command line, and/or an open Blender file.
"""

# $Id: k_settings.py,v 1.0 2007/12/25 23:14:48 kurt Exp $


try:
    import subprocess
    import re
    import sys
    import os
    pythonProper=True
except ImportError:
    pythonProper=False

try:
    # note: use namespace so Blender.sys doesn't override sys
    import Blender
    from Blender import Scene
    inBlender=True
except ImportError:
    inBlender=False


def default(obj,var,val):
    """
    Utility function to set default parameters in an object only if they do not already exist.
    """
    if hasattr(obj,var)==False:
        setattr(obj,var,val)


def writeINI(categoryName,obj,append=False,filename=None,clobberAll=False):
    """
    Works like writeCatsINI, but is more convenient for writing a single object category
    """
    cats={}
    cats[categoryName]=obj
    return writeCatsINI(cats,append,filename,clobberAll)


def writeCatsINI(cats,append=False,filename=None,clobberAll=False):
    """
    Writes a single setting to the .ini file.

    cats is a dictionary of objects where all object attrbutes should
    be written to file.

    If append =True, the new values will be added to the old ones
    as arrays.  If it is false, we'll save over the old values.

    if clobberAll=True, this will set the contents of the .ini file to exactly
    and only the cats given.  Generally, it's a better idea to change what you
    want and ignore what you don't.
    """
    def writeSettingsINI(settings,filename=None):
        """
        This WILL NOT work as a general-purpose settings writer.

        That's not a bad thing since settings can be .ini info, cmd line, etc
        all smooshed together.  Writing all that to the .ini could create a big mess.
        """
        if filename==None:
            filename="settings.ini"
        ini=sys.stdout #open(filename,"w+")
        if not ini:
            return False
        eol="\n"
        for catName,catObj in settings.cats.iteritems():
            ini.write("["+catName+"]"+eol)
            items=dir(catObj)
            for key in items:
                if key[0]!="_":
                    vals=getattr(catObj,key)
                    if type(vals).__name__=='list':
                        ini.write(key+"=")
                        c="["
                        for val in vals:
                            ini.write(c+str(val))
                            c=", "
                        ini.write("]")
                    elif type(vals).__name__=='builtin_function_or_method':
                        pass
                    else:
                        ini.write(key+"="+vals+eol)
            ini.write(""+eol)
        #ini.close()
        return True
    if clobberAll==False:
        settings=readSettingsINI(filename)
    else:
        settings=createEmptyObject()
    if hasattr(settings,"cats")==False:
        settings.cats={}
    for name, cat in cats.iteritems():
        if append==False:
            settings.cats[name]=cat
        else:
            # problem at this level
            items=dir(cat)
            for itemName in items:
                if itemName[0]!="_":
                    if hasattr(settings.cats[name],itemName)==False:
                        setattr(settings.cats[name],itemName,[])
                    elif type(settings.cats[name]).__name__!='list':
                        settings.cats[name]=[settings.cats[name]]
                    vals=getattr(cat,itemName)
                    if type(vals).__name__=='builtin_function_or_method':
                        pass
                    elif type(vals).__name__!='list':
                        getattr(settings.cats[name],itemName).append(vals)
                    else:
                        for val in vals:
                            getattr(settings.cats[name],itemName).append(val)
    return writeSettingsINI(settings,filename)


def readSettingsINI(filename=None,settings=None,overwrite=True):
    """
    Utility function to convert all .ini file settings into a settings object.

    The settings object will be populated with all items under the first [category].
    If there is more than one, each [subcategory] will be its own object under the settings object.
    Additionally, these are linked up under the settings.cats{} dictionary

    You can also have arrays in the ini, ala: name=[a,b,c,d]
    """
    settings=createEmptyObject(settings)
    if filename==None:
        filename="settings.ini"
    if -1==filename.find(os.sep):
        if inBlender:
            # We passed the script path in the blender.exe command line
            if hasattr(settings,"P")==False:
                print "Warning: unknown Blender Extender path so settings.ini not available."
                return settings
            path=settings.P
            print settings.P
            print getattr(settings,"*")
        else:
            # figure out where we are being executed from
            path=os.path.abspath(__file__)
        filename=path[0:path.rfind(os.sep)+1]+filename
    ini=open(filename,"r")
    if not ini:
        print "File \"",filename,"\" not found!"
        return settings
    category=None
    defaultCategory=True
    def setValue(key,val):
        if defaultCategory:
            if overwrite or hasattr(settings,key)==False:
                setattr(settings,key,val)
        if category!=None:
            if overwrite or hasattr(category,key)==False:
                setattr(category,key,val)
    for line in ini:
        index=re.compile('=').search(line,1)
        if index==None:
            if line[0]=="[":
                defaultCategory=(category==None)
                line=line[1:].split("]")[0]
                if hasattr(settings,line)==False:
                    category=createEmptyObject()
                    setattr(settings,line,category)
                    if hasattr(settings,"cats")==False:
                        settings.cats={}
                    settings.cats[line]=category
                else:
                    category=getattr(settings,line)
        else:
            index=index.start()
            key=line[:index]
            val=line[index+1:-1]
            if val==None or len(val)<1:
                continue
            while val[-1]==" " or val[-1]=="\t" or val[-1]=="\n" or val[-1]=="\r":
                val=val[0:-1]
            while val[0]==" " or val[0]=="\t" or val[0]=='\n' or val[0]=='\r':
                val=val[1:]
            items=None
            if val[0]=='[':
                val=val[1,-1]
                items=val.split(',')
            if items!=None:
                setValue(key,items)
            else:
                while val[0]=='"' and val[-1]=='"':
                    val=val[1:-1]
                setValue(key,val)
    ini.close()
    return settings

if inBlender:
    def readSettingsBlender(settings=None):
        """
        Utility function to read parameters from the current .blend file.
        """
        settings=createEmptyObject(settings)
        # TODO: stuff
        return settings


def readSettingsCmdline(argv=None,settings=None,overwrite=False):
    """
    Utility function to convert all command-line parameters to a settings object.
    If no argv is specified, use sys.argv instead
    Anything not taken as a parameter gets added to "*"
    """
    settings=createEmptyObject(settings)
    if hasattr(settings,"*")==False:
        setattr(settings,"*",[]);
    if argv==None:
        if pythonProper:
            argv=sys.argv
        else:
            print "Warning: Unable to parse command line without full python install."
    needVal="*"
    for i in range(len(argv)):
        if len(argv[i])<2:
            pass
        elif argv[i][0]=='-':
            if argv[i][1]=='-':
                pair=argv[i][2:].split("=")
                if overwrite or hasattr(settings,pair[0])==False:
                    if len(pair)>1:
                        setattr(settings,pair[0],pair[1])
                    else:
                        setattr(settings,pair[0],"true")
                needVal="*"
            else:
                # Blender windows command line does things like "-t 1" for settings :P
                if overwrite or hasattr(settings,argv[i][1:])==False:
                    setattr(settings,argv[i][1:],"true")
                    needVal=argv[i][1:]
        elif needVal!="*":
            setattr(settings,needVal,argv[i])
            needVal="*"
        else:
            getattr(settings,needVal).append(argv[i])
    return settings


def createEmptyObject(orReturnThis=None):
    """
    Creates and empty object for adding settings to
    """
    if orReturnThis==None:
        class MT():pass
        orReturnThis=MT()
    return orReturnThis
    

def readSettings(settings=None):
    """
    Will read settings from:
        1) The settings.ini file
        2) The command line
        3) The open Blender file
    In that precedence order.
    """
    settings=readSettingsCmdline(None,settings)
    settings=readSettingsINI(None,settings,False) # must be AFTER cmdline to find script directory
    if inBlender:
        settings=readSettingsBlender(settings)
    return settings
