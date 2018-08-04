#!/usr/bin/python
#!BPY

""" Registration info for Blender menus:
Name: 'k+) Render This'
Blender: 242
Group: 'Object'
Tip: 'Generate an image based on any Blender-loadable image or 3d object.'
"""

__author__ = "Kurt"
__url__ = ""
__version__ = "1.0"
__bpydoc__ = """
Generate an image based on any Blender-loadable image or 3d object.
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
    from Blender import *
    inBlender=True
except ImportError:
    inBlender=False

try:
    from Tkinter import *
    import tkFileDialog
    haveTk=True
except ImportError:
    haveTk=False

origin,_=os.path.split(sys.argv[0]);origin=os.path.abspath(origin)
if inBlender:
    nxt=False
    for arg in sys.argv:
        if nxt:
            origin,_=os.path.split(arg);origin=os.path.abspath(origin)
            break
        elif arg=="-P":
            nxt=True
sys.path.append(origin)

try:
    import k_runner
except ImportError:
    print "Unable to find k_runner.py"
    print origin
    print sys.path
from k_settings import *
from k_openThis import *
from k_commonEvent import *


def renderInNewInstance(settings):
    """This can still be used from within Blender"""
    if not pythonProper:
        print "Python is not installed.  You cannot call renderInNewInstance()"
        return -1
    settings.showUI=False
    if settings.showUI:
        backgroundFlag=''
    else:
         backgroundFlag=' -W -p 0 0 0 0 -noaudio -nojoystick -noglsl'
    def fixup(longpath):
        try:
            import win32api
            return win32api.GetShortPathName(longpath)
        except ImportError:
            return '"'+longpath+'"'
    if settings.filename[-6:]==".blend":
        blenderFile='"'+settings.filename+'"'
    else:
        blenderFile=""
    cmdline=fixup(settings.blender)+backgroundFlag+' '+blenderFile+' -P "'+settings.renderThis+'" --filename="'+settings.filename+'"'
    cmdline=addParam(cmdline,"--frame=",settings,"frame")
    cmdline=addParam(cmdline,"--w=",settings,"w")
    cmdline=addParam(cmdline,"--h=",settings,"h")
    cmdline=addParam(cmdline,'--out="',settings,"out",'"')
    cmdline=addParam(cmdline,"--osa=",settings,"osa")
    cmdline=addParam(cmdline,"--ao=",settings,"ao")
    cmdline=addParam(cmdline,"--gi=",settings,"gi")
    
    print "Launching Blender:\n"+cmdline
    print "--------------------------------\n\n"
    result=k_runner.Application().run(cmdline,hideWindows=(settings.showUI==False),wDogLifetime=settings.killRenderAfter)
    print str(result)+"\n--------------------------------\n\n"
    return result


def tkGui(settings):
    """This can still be used from within Blender"""
    tkApp=Tk()
    tkApp.doit=False
    tkApp.title('Render File with Blender')
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
    def getImageType(filename):
        extension=filename.split(".")[-1]
        imageType=Scene.Render.JPEG
        if extension=="png":
            imageType=Scene.Render.PNG
        elif extension=="bmp":
            imageType=Scene.Render.BMP
        elif extension=="tga" or extension=="tiff":
            imageType=Scene.Render.TARGA
        elif extension=="iris":
            imageType=Scene.Render.IRIS
        elif extension=="iriz":
            imageType=Scene.Render.IRIZ
        return imageType
            
    
    def renderInThisInstance(settings):
        if settings.filename[-6:]==".blend":
            # crass assumption: it was already opened via the cmdline
            pass
        elif openInThisInstance(settings)==False:
            return False

        try:
            scene=Scene.GetCurrent()
            if scene.objects.camera==None:
                print "ERR: No camera.  What now??"
            context=scene.getRenderingContext()
            
            context.setImageType(getImageType(settings.out))
            if context.imageType==Scene.Render.PNG or context.imageType==Scene.Render.TARGA:
                context.alphaMode=1
            else:
                context.alphaMode=0
            
            if settings.frame=="first":
                context.currentFrame(context.sFrame)
            elif settings.frame=="middle":
                context.currentFrame((context.eFrame-context.sFrame)/2+context.sFrame)
            elif settings.frame=="last":
                context.currentFrame(context.eFrame)
            context.sFrame=context.currentFrame()
            context.eFrame=context.currentFrame()
            context.extensions=False

            if settings.osa!="specified":
                if int(settings.osa)>0:
                    context.enableOversampling(1);
                    context.setOversamplingLevel(int(settings.osa));
                else:
                    context.enableOversampling(0);

            context.imageSizeX(int(settings.w))
            context.imageSizeY(int(settings.h))
            context.crop=0

            # may someday want to specify some of these via cmdline
            context.partsX(1)
            context.partsY(1)
            context.enableMotionBlur(0)
            context.enablePanorama(0)
            context.enableRadiosityRender(0)
            context.enableFieldRendering(0)
            #context.setRenderer(Scene.Render.INTERN)
            context.displayMode=0
            context.imagePlanes=32
            
            print "rendering "+settings.out+"..."
            context.render()
            context.setRenderPath(Blender.sys.dirname(settings.out)+Blender.sys.sep)
            context.saveRenderedImage(Blender.sys.basename(settings.out))
            #context.renderAnim()
            print "done!"
            bWorked=True
	except Exception:
            bWorked=False
        if bWorked:
            if hasattr(settings,"onRenderSuccess")==True and settings.onRenderSuccess!="":
                doCommonEvent(settings.onRenderSuccess,settings)
        else:
            if hasattr(settings,"onRenderFail")==True and settings.onRenderFail!="":
                doCommonEvent(settings.onRenderFail,settings)
        if hasattr(settings,"onRenderDone")==True and settings.onRenderDone!="":
            doCommonEvent(settings.onRenderDone,settings)
	return bWorked

    def blenderGui(settings):
        print "displaying the ui"


if __name__ == '__main__':
    """
    This will either render with the settings given via the command line or
    start an appropriate gui to enter in settings.
    """ 
    if inBlender:
        filename=""
    else:
        filename=os.path.abspath(__file__)
        
    if filename[0:10]=="/cygdrive/":
        print "ERR>> Cygwin python won't work.  Install real windows python!"
    else:
        
        # play fill in the blanks
        settings=readSettingsCmdline()
        settings=readSettingsINI("../../Blender Extender/settings.ini",settings,False) # must be AFTER cmdline to find script directory
        default(settings,"blender","c:\\Program Files\\Blender Foundation\\Blender\\blender.exe")
        default(settings,"renderThis","C:\\volitile\\coding\\BlenderExtender\\k_renderThis.py")
        default(settings,"frame","current")
        default(settings,"osa","specified")
        default(settings,"ao","specified")
        default(settings,"gi","specified")
        default(settings,"opencmd","")
        default(settings,"shellex","")
        default(settings,"showUI","False")
        default(settings,"extensions",[".blend"])
        default(settings,"w","100")
        default(settings,"h","100")
        default(settings,"killRenderAfter",30)

        if hasattr(settings,"onRenderDone"):
            print settings.onRenderDone
        if hasattr(settings,"onRenderSuccess")==False and hasattr(settings,"onRenderFail")==False:
            default(settings,"onRenderDone","close")

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

            # if we have no output, assume it's filename.png
            if hasattr(settings,"out")==False or settings.out==None:
                setattr(settings,"out",settings.filename.split(".")[0]+".png");
            else:
                # default path
                path=settings.out.split(os.sep)
                if len(path)<=1:
                    settings.out=os.getcwd()+os.sep+settings.out
                        
            # Let's roll!        
            if inBlender:
                settings=readSettingsBlender(settings)
                renderInThisInstance(settings)
            else:
                renderInNewInstance(settings)
