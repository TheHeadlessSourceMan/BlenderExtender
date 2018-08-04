#!/usr/bin/python
#!BPY

""" Registration info for Blender menus:
Name: 'k+) Open This'
Blender: 242
Group: 'Import'
Tip: 'Open any Blender-loadable image or 3d object.'
"""

__author__ = "Kurt"
__url__ = ""
__version__ = "1.0"
__bpydoc__ = """
Open any Blender-loadable image or 3d object.
"""

# $Id: k_renderThis.py,v 1.0 2007/12/25 23:14:48 kurt Exp $


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
    inBlender=True
except ImportError:
    inBlender=False

try:
    from Tkinter import *
    import tkFileDialog
    haveTk=True
except ImportError:
    haveTk=False
    
if inBlender:
    import k_importExport
    import k_center

import k_runner
from k_settings import *


def addParam(cmdline,prefix,obj,value,affix=""):
    """
    Utility function to add a parameter to a command line if its value exists.
    """
    if hasattr(obj,value) and getattr(obj,value)!=None:
        return cmdline+" "+prefix+getattr(obj,value)+affix
    return cmdline


def openInNewInstance(settings):
    """This can still be used from within Blender"""
    if not pythonProper:
        print "Python is not installed.  You cannot call openInNewInstance()"
        return -1
    if settings.showUI:
        backgroundFlag=''
    else:
         backgroundFlag=' -W -p 0 0 0 0 -noaudio -nojoystick -noglsl'
    def fixup(longpath):
        try:
            import win32api
            return win32api.GetShortPathName(longpath)
        except ImportError:
            return ' "'+longpath+'"'
    if hasattr(settings,"listTypes"):
        filename=" --filename=\"n/a\" --listTypes"
        blenderFile=""
    elif settings.filename[-6:]==".blend":
        blenderFile=' "'+settings.filename+'"'
        filename=' --filename="'+settings.filename+'"'
    else:
        blenderFile=""
        filename=' --filename="'+settings.filename+'"'

    cmdline=fixup(settings.blender)+backgroundFlag+blenderFile+' -P "'+settings.openThis+'"'+filename
    cmdline=addParam(cmdline,"--frame=",settings,"frame")
    cmdline=addParam(cmdline,"--w=",settings,"w")
    cmdline=addParam(cmdline,"--h=",settings,"h")
    
    print "Launching Blender:\n"+cmdline
    print "--------------------------------\n\n"
    result=k_runner.Application().run(cmdline)
    print str(result)+"\n--------------------------------\n\n"
    return result


def listAvailableTypes(settings):
    """
    returns an array of all available types where each element is
    [file_extn, description]
    """
    global availables
    def fixup(longpath):
        try:
            import win32api
            return win32api.GetShortPathName(longpath)
        except ImportError:
            return ' "'+longpath+'"'
    availables=[]
    def onOut(app,out):
        global availables
        print "out>> ",out
        out=out.split("[")
        if len(out)==2:
            while out[1][-1]==' ' or out[1][-1]==']' or out[1][-1]=='\n':
                out[1]=out[1][0:-1]
            while out[1][0]==' ':
                out[1]=out[1][1:]
            out[1]=out[1].split(" ")
            for extn in out[1]:
                availables.append([extn,out[0]])
        return None
    backgroundFlag=' -W -p 0 0 0 0 -noaudio -nojoystick -noglsl'
    cmdline=fixup(settings.blender)+backgroundFlag+' -P "'+settings.openThis+'" --listTypes'
    print "Launching Blender:\n"+cmdline
    print "--------------------------------\n\n"
    result=k_runner.Application().run(cmdline,onOutputCB=onOut,hideWindows=True,wDogLifetime=5)
    print str(result)+"\n--------------------------------\n\n"
    return availables
    


def tkGui(settings):
    """
    This can still be used from within Blender
    """
    tkApp=Tk()
    tkApp.doit=False
    tkApp.title('Open File in Blender')
    fileField=None
    def onBrowse():
        settings.filename=tkFileDialog.askopenfilename()
        # for some annoying reason this returns "/" separators even in windoze
        if os.sep!="/":
            settings.filename=os.sep.join(settings.filename.split("/"))
        fileField.delete(0, END)
        fileField.insert(0, settings.filename) 
    def onOK():
        tkApp.doit=True
        tkApp.quit()
    def onCancel():
        tkApp.doit=False
        tkApp.quit()
    row=0
    settings.filename=""
    filenameEntry=Frame(tkApp)
    filenameEntry.grid(row=row,columnspan=4)
    Message(filenameEntry,text="File:").grid(row=0,column=0,sticky=E)
    fileField=Entry(filenameEntry,textvariable=settings.filename,width=75)
    fileField.grid(row=0,column=1,sticky=W)
    Button(filenameEntry,text="...",command=onBrowse).grid(row=0,column=2,sticky=W)
    row=row+1
    Button(tkApp,text="OK",command=onOK,width=10).grid(row=row,column=1,sticky=E)
    Button(tkApp,text="Cancel",command=onCancel,width=10).grid(row=row,column=2,sticky=W)
    tkApp.mainloop()
    if hasattr(settings,"filename")==False:
        print "Missing filename!"
        return False
    return tkApp.doit
    

if inBlender:
    def deleteEverything(theseTypes=['Armature', 'Curve', 'Lattice', 'Mball', 'Mesh', 'Surf', 'Empty']):
        """
        Pass in an array of types to delete.
        Possible types are: 'Armature', 'Camera', 'Curve', 'Lamp', 'Lattice', 'Mball', 'Mesh', 'Surf', 'Empty'
        Default is ['Armature', 'Curve', 'Lattice', 'Mball', 'Mesh', 'Surf', 'Empty']
        If set to None, it will delete everything.
        """
        scene=Scene.GetCurrent()
        objs=scene.objects
        if objs==None:
            return
        for obj in objs:
            if theseTypes == None or obj.getType() in theseTypes:
                scene.objects.unlink(obj)
        
    def openInThisInstance(settings,inEmptyScene=True):
        k_importExport.loadAll()
        print "simprini"
        if hasattr(settings,"listTypes"):
            print "kalamazoo"
            print k_importExport.importers
            if inBlender:
                pass
                #Blender.Quit()
            return True
        filetypes=k_importExport.importers.findTypes(settings.filename)
        if len(filetypes)<1:
            print "Unable to find appropriate importer for "+settings.filename
            return False
        if inEmptyScene:
            deleteEverything(None)
        # TODO: Have user select instead of just assuming[0]?
        importer=filetypes[0].owner
        if isinstance(importer, k_importExport.ImageImporter):
            #TODO: Choose:
            obj=importer.importAsPlane(settings.filename,settings.w,settings.h)
            # obj=importer.importAsTerrain(settings.filename,settings.w,settings.h)
        else:
            if inEmptyScene:
                scene = Scene.GetCurrent()
                # top lamps
                l=Blender.Lamp.New(); l.col=[1.0,0.948,0.807]; o=scene.objects.new (l); o.setLocation( 10.0, 10.0, 10.0)
                l=Blender.Lamp.New(); l.col=[1.0,0.948,0.807]; o=scene.objects.new (l); o.setLocation( 10.0,-10.0, 10.0)
                l=Blender.Lamp.New(); l.col=[1.0,0.948,0.807]; o=scene.objects.new (l); o.setLocation(-10.0,-10.0, 10.0)
                l=Blender.Lamp.New(); l.col=[1.0,0.948,0.807]; o=scene.objects.new (l); o.setLocation(-10.0, 10.0, 10.0)
                # bottom lamps
                l=Blender.Lamp.New(); l.col=[0.751,0.810,1.0]; o=scene.objects.new (l); o.setLocation( 10.0, 10.0,-10.0)
                l=Blender.Lamp.New(); l.col=[0.751,0.810,1.0]; o=scene.objects.new (l); o.setLocation( 10.0,-10.0,-10.0)
                l=Blender.Lamp.New(); l.col=[0.751,0.810,1.0]; o=scene.objects.new (l); o.setLocation(-10.0,-10.0,-10.0)
                l=Blender.Lamp.New(); l.col=[0.751,0.810,1.0]; o=scene.objects.new (l); o.setLocation(-10.0, 10.0,-10.0)
                # camera
                camera = scene.objects.new (Blender.Camera.New())
                camera.setLocation (10.0, 10.0, 10.0)
                camera.RotX = 0.79
                camera.RotZ = 2.35
            obj=importer.importFile(settings.filename)
        if hasattr(settings,"reFrame") and settings.reFrame==True:
            center(obj)
        return True

    def blenderGui(settings):
        print "displaying the ui"
        def loaded(filename):
            setattr(settings, "filename", filename)
            default(settings, "reFrame", False)
            openInThisInstance(settings)
        Blender.Window.FileSelector(loaded,"Load")


if __name__ == '__main__':
    """
    This will either open the file given via the command line or
    start an appropriate gui to enter in settings.
    """
    print "hopscotch"
    settings=createEmptyObject()
    if inBlender:
        filename=""
    else:
        filename=os.path.abspath(__file__)
        
    if filename[0:10]=="/cygdrive/":
        print "ERR>> Cygwin python won't work.  Install real windows python!"
    else:
        print "jiggle"
        # play fill in the blanks
        settings=readSettingsCmdline(None,settings)
        settings=readSettingsINI("../../Blender Extender/settings.ini",settings,False) # must be AFTER cmdline to find script directory
        default(settings,"blender","c:\\Program Files\\Blender Foundation\\Blender\\blender.exe")
        default(settings,"openThis","C:\\volitile\\coding\\BlenderExtender\\k_openThis.py")
        default(settings,"frame","current")
        default(settings,"opencmd","")
        default(settings,"showUI","False")
        if hasattr(settings,"listTypes"):
            settings.filename="n/a"

        # if we dont have --filename= then it's -noglsl[space] or assume it's the last reasonable unqualified parameter
        if hasattr(settings,"filename")==False or settings.filename==None:
            if hasattr(settings,"noglsl")!=False and settings.noglsl!=None:
                ext=settings.noglsl.split(".")
                if len(ext)>1 and ext[-1]!="exe" and ext[-1]!="py":
                    setattr(settings,"filename",settings.noglsl)
            if hasattr(settings,"filename")==False or settings.filename==None: 
                filenames=getattr(settings,"*")
                for test in filenames:
                    ext=test.split(".")
                    if len(ext)>1 and ext[-1]!="exe" and ext[-1]!="py":
                        setattr(settings,"filename",test)

        if hasattr(settings,"filename")==False or settings.filename==None:
            if haveTk:
                doit=tkGui(settings)
            elif inBlender:
                blenderGui(settings)
                doit=True
            else:
                print "ERR: No acceptable UI found. :("
                doit=False
        else:
            doit=True
            
        if doit==True:
            # Set the filename default path
            path=settings.filename.split(os.sep)
            if len(path)<=1:
                settings.filename=os.getcwd()+os.sep+settings.filename
            print "spumoni"            
            # Let's roll!
            if inBlender:
                settings=readSettingsBlender(settings)
                openInThisInstance(settings)
            else:
                openInNewInstance(settings)
