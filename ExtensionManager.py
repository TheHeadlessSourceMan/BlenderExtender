import copy
try:
    from Tkinter import *
    haveTk=True
except ImportError:
    haveTk=False

try:
    import _winreg
    usingWindows=True
except ImportError:
    usingWindows=False

import os,sys

origin,_=os.path.split(sys.argv[0]);origin=os.path.abspath(origin)
scriptsDir=os.sep.join(origin.split(os.sep)[0:-1])+os.sep+".blender"+os.sep+"scripts"
sys.path.append(scriptsDir)
from k_settings import *


# ------------------- Windows registry tools

if usingWindows:
    def getKey(path,start=None):
        """
        Gets a given registry key

        Path is a /-separated path

        Currenly only the top-levels HKCR and HKLM are supported.

        Returns the value string or None if non-existant
        """
        tmp=path
        path=path.split("/")
        while path[0]=="":
            path=path[1:]
        if start==None:
            if path[0]=="HKCR" or path[0]=="HKEY_CLASSES_ROOT":
                reg=_winreg.CreateKey(_winreg.HKEY_CLASSES_ROOT,None)
            elif path[0]=="HKLM" or path[0]=="HKEY_LOCAL_MACHINE":
                reg=_winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE,None)
            else:
                print "Bad registry path: "+"/".join(path)
                return
            path=path[1:]
        else:
            reg=start
        val=None
        for i in range(0,len(path)):
            try:
                val=_winreg.QueryValue(reg,path[i])
            except WindowsError:
                reg=None
                val=None
                break
            reg=_winreg.CreateKey(reg,path[i])
        #if start!=None:
        #    print "  ",
        #print "  ",tmp,"=",val
        return reg,val


if usingWindows:
    def removeKey(path,ifEq=None,start=None):
        """
        Removes a given registry key, possibly only if it is a certain value

        Path is a /-separated path

        Currenly only the top-levels HKCR and HKLM are supported.
        """
        path=path.split("/")
        while path[0]=="":
            path=path[1:]
        if start==None:
            if path[0]=="HKCR" or path[0]=="HKEY_CLASSES_ROOT":
                reg=_winreg.CreateKey(_winreg.HKEY_CLASSES_ROOT,None)
            elif path[0]=="HKLM" or path[0]=="HKEY_LOCAL_MACHINE":
                reg=_winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE,None)
            else:
                print "Bad registry path: "+path
        else:
            reg=start
        for i in range(1,len(path)):
            try:
                val=_winreg.QueryValue(reg,path[i])
            except WindowsError:
                reg=None
                parent=None
                break
            parent=reg
            reg=_winreg.CreateKey(parent,path[i])
        if reg!=None and (ifEq==None or val==ifEq):
            print "deleting registry key "+path[i]
            _winreg.DeleteKey(parent,path[i])

if usingWindows:
    def createKey(path,default=None,start=None):
        """
        Creates a given registry key, possibly setting it's (default) value

        Path is a /-separated path

        Currenly only the top-levels HKCR and HKLM are supported.

        Returns the newly-created key
        """
        path=path.split("/")
        while path[0]=="":
            path=path[1:]
        if start==None:
            if path[0]=="HKCR" or path[0]=="HKEY_CLASSES_ROOT":
                reg=_winreg.CreateKey(_winreg.HKEY_CLASSES_ROOT,None)
            elif path[0]=="HKLM" or path[0]=="HKEY_LOCAL_MACHINE":
                reg=_winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE,None)
            else:
                print "Bad registry path: "+path
        else:
            reg=start
        for i in range(1,len(path)):
            parent=reg
            reg=_winreg.CreateKey(parent,path[i])
        if default!=None:
            _winreg.SetValue(parent,path[-1],_winreg.REG_SZ,default)
        return reg


# ------------------- The FileTypeInfo object


class FileTypeInfo():
    def __init__(self,settings,extension,preFetch=False):
        """
        You can either fetch the values you need on demand, or prefetch them
        all at startup.
        """
        self.settings=settings
        self.fileTypeName=extension
        self.extension=extension
        if preFetch:
            self.getThumbnailRenderer()
            self.getPrimaryOpener()
            self.getOpenWith()
            self.getIcon()
    def _getKey(self):
        if usingWindows:
            key,val=getKey("HKCR/"+self.fileTypeName)
            while val!="" and self.fileTypeName[0]==".":
                self.fileTypeName=val
                key,val=getKey("HKCR/"+self.fileTypeName)
            self.description=val
        else:
            print "Unable to register file extensions on this system."
        return key
    def setIcon(self,description):
        print "I don't think we want to do this."
    def getIcon(self):
        if not hasattr(self,"icon"):
            reg=self._getKey()
            _,self.icon=getKey("DefaultIcon",reg)
        return self.icon
    def setDescription(self,description):
        print "I don't think we want to do this."
    def getDescription(self):
        """
        Gets the description name of a given file type
        """
        if not hasattr(self,"description"):
            self._getKey()
        return self.description
    def getThumbnailRenderer(self):
        """
        Is Blender the thumbnail generator of a given file type?
        """
        if not hasattr(self,"thumbnailRenderer"):
            iThumbnailRendererClassID="{BB2E617C-0920-11d1-9A0B-00C04FC2D6C1}"
            reg=self._getKey()
            self.thumbnailRenderer=getKey("shellex/"+iThumbnailRendererClassID,reg)[1]==self.settings.thumbobj
        return self.thumbnailRenderer
    def setThumbnailRenderer(self,useBlenderThumbnail):
        """
        Sets the thumbnail renderer for a given file type

        This maintains a cookie-crumb trail in the .ini file for undo purposes
        """
	global origin
        if self.thumbnailRenderer==useBlenderThumbnail:
            return
        reg=self._getKey()
        if useBlenderThumbnail:
            # save old thumbnail viewer
            if self.thumbnailRenderer!=None:
                backup=createEmptyObject()
                setattr(backup,"oldthumbobj",self.thumbnailRenderer)
                writeINI(self.fileTypeName,backup,True,origin+os.sep+"settings.ini")
            createKey("ShellEx/"+self.settings.thumbobj,self.settings.thumbobj,reg)
            self.thumbnailRenderer=useBlenderThumbnail
        else:
            removeKey("ShellEx/"+self.settings.thumbobj,self.settings.thumbobj,reg)
            # revert to old thumbnail viewer
            if hasattr(self.settings,self.fileTypeName):
                old=getattr(self.settings,self.fileTypeName)
                if old!=None and hasattr(old,"oldthumbobj"):
                    old=getattr(old,self.fileTypeName)
                    if len(old)>0:
                        createKey("ShellEx/"+old[-1],old[-1],reg)
                        backup=createEmptyObject()
                        setattr(backup,"oldthumbobj",old[0:-1])
                        writeINI(self.fileTypeName,backup,False,origin+os.sep+"settings.ini")
                        self.thumbnailRenderer=useBlenderThumbnail
    def getOpenWith(self):
        """
        Is Blender in the "openWith" menu of a given file type?
        """
        if not hasattr(self,"openWith"):
            reg=self._getKey()
            self.openWith=getKey("shell/blender",reg)[1]!=None
        return self.openWith
    def setOpenWith(self,setBlenderInOpenWith):
        """
        Sets the "openWith" menu for a given file type
        """
        if self.openWith==setBlenderInOpenWith:
            return
        self.openWith=setBlenderInOpenWith
        reg=self._getKey()
        if setBlenderInOpenWith==True:
            createKey("shell/blender",self.settings.openWithreg)
        else:
            removeKey("shell/blender",None,reg)
    def getPrimaryOpener(self):
        """
        Is Blender the primary opener of a given file type?
        """
        if not hasattr(self,"primaryOpener"):
            reg=self._getKey()
            self.primaryOpener=getKey("shell/open/command",reg)[1]==self.settings.openWith
        return self.primaryOpener
    def setPrimaryOpener(self,primaryOpenerBlender):
        if primaryOpenerBlender==self.primaryOpener:
            return
        primaryOpenerBlender=self.primaryOpener
        reg=self._getKey()
        if primaryOpenerBlender:
            createKey("shell/open/command",self.settings.openWith,reg)
        else:
            removeKey("shell/open/command",self.settings.openWith,reg)


def getAvailableFileTypes(settings,preFetch=False):
    """returns array where each element is a FileTypeInfo object"""
    retval=[]

    #try:
    if True:
        # try and determine everything that k_openThis can currently open
        import k_openThis
        types=k_openThis.listAvailableTypes(settings)
        for t in types:
            if hasattr(settings.cats,t[0])==False:
                settings.cats[t]=createEmptyObject()
    #except:
    #    print "WARN: k_openThis failed.  Retrieving last known list instead..."
        
    for cat in settings.cats:
        if cat[0]==".":
            retval.append(FileTypeInfo(settings,cat,preFetch))

    return retval

# ------------------  The application

def readSettings(settings=None):
    global origin
    settings=createEmptyObject(settings)
    settings=readSettingsCmdline(None,settings)
    settings=readSettingsINI(origin+os.sep+"settings.ini",settings,False) # must be AFTER cmdline to find script directory
    default(settings,"blender","c:\\Program Files\\Blender Foundation\\Blender\\blender.exe")
    default(settings,"openThis","C:\\volitile\coding\\BlenderExtender\\k_openThis.py")
    setattr(settings,"openWith",'"'+settings.blender+'" -P "'+settings.openThis+'" --filename="%1"')
    default(settings,"icon",'"'+settings.blender+',1"')
    default(settings,"thumbobj","{AE7B2720-60D0-48FC-958A-7CAD029A7CF5}")
    return settings
    
def runTkGui(settings=None):
    global types
    if settings==None:
        settings=readSettings()
    if not haveTk:
        print "Must have TK installed to run this application"
        return
    tkApp=Tk()
    def onOK():
        global types
        for t in types:
            # set type info settings
            t.setThumbnailRenderer(t.thumbnailCtl.get()==1)
            if hasattr(t,"primaryOpenerCtl"):
                t.setPrimaryOpener(t.primaryOpenerCtl.get()==1)
            if hasattr(t,"openWithCtl"):
                t.setOpenWith(t.openWithCtl.get()==1)
        tkApp.quit()
    def onRecommend():
        global types
    def onCancel():
        tkApp.quit()
    tkApp.title('Blender File Extensions')
    # add controls for all extensions
    types=getAvailableFileTypes(settings,True)
    Label(tkApp,text='Extensions:').grid(row=0,sticky=W)
    extensionsArea=Frame(tkApp,relief=GROOVE,borderwidth=2)
    extensionsArea.grid(row=1,columnspan=4)
    Message(extensionsArea,text="EXT",width=50).grid(row=0,column=0,sticky=W)
    Message(extensionsArea,text="Thumb",width=50).grid(row=0,column=1,sticky=W)
    Message(extensionsArea,text="Open",width=50).grid(row=0,column=2,sticky=W)
    Message(extensionsArea,text="OpenWith",width=50).grid(row=0,column=3,sticky=W)
    Message(extensionsArea,text="Icon",width=100).grid(row=0,column=4,sticky=W)
    Message(extensionsArea,text="Description",width=100).grid(row=0,column=5,sticky=W)
    row=1
    for t in types:
        Message(extensionsArea,text=t.extension,width=50).grid(row=row,column=0,sticky=W)
        setattr(t,"thumbnailCtl",IntVar()); t.thumbnailCtl.set(t.thumbnailRenderer)
        Checkbutton(extensionsArea,text="",anchor=W,variable=t.thumbnailCtl).grid(row=row,column=1,sticky=W)
        if t.extension!=".blend":
            # it makes no sense to do all this for file types Blender can already open
            setattr(t,"primaryOpenerCtl",IntVar()); t.primaryOpenerCtl.set(t.primaryOpener)
            Checkbutton(extensionsArea,text="",anchor=W,variable=t.primaryOpenerCtl).grid(row=row,column=2,sticky=W)
            setattr(t,"openWithCtl",IntVar()); t.openWithCtl.set(t.openWith)
            Checkbutton(extensionsArea,text="",anchor=W,variable=t.openWithCtl).grid(row=row,column=3,sticky=W)
        setattr(t,"iconCtl",StringVar());
        if (t.icon==None)==False:
            t.iconCtl.set(t.icon)
        Entry(extensionsArea,textvariable=t.iconCtl,width=40).grid(row=row,column=4,sticky=W)
        setattr(t,"descriptionCtl",StringVar());
        if (t.description==None)==False:
            t.descriptionCtl.set(t.description)
        Entry(extensionsArea,textvariable=t.descriptionCtl,width=40).grid(row=row,column=5,sticky=W)
        row=row+1
    row=2
    Button(tkApp,text="Recommend",command=onRecommend,width=10).grid(row=row,column=0,sticky=W)
    row=3
    Button(tkApp,text="OK",command=onOK,width=20).grid(row=row,column=1,sticky=E)
    Button(tkApp,text="Cancel",command=onCancel,width=20).grid(row=row,column=2,sticky=W)
    row=row+1
    tkApp.mainloop()
    # run till done
                          
runTkGui()
