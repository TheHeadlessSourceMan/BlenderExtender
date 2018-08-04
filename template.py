import os
import sys
try:
    import _winreg
    hasWindowsRegistry=True
except ImportError:
    hasWindowsRegistry=False

if hasWindowsRegistry:
    def registerMenu(key,menuName,command):
        """
        Registers a given context menu command with a certain file type
        """
        hkcr=_winreg.CreateKey(_winreg.HKEY_CLASSES_ROOT,None)
        while key[0]==".":
            try:
                val=_winreg.QueryValue(hkcr,key)
            except WindowsError:
                val=None 
            if val==None or val=="" or val==key:
                break
            key=val
        print "Registering \""+key+"\" menu \""+menuName+"\""
        reg=_winreg.CreateKey(hkcr,key)
        reg=_winreg.CreateKey(reg,"shell")
        shortName=""
        for c in menuName:
            if c!=' ':
                shortName=shortName+c
        reg1=_winreg.CreateKey(reg,shortName)
        _winreg.SetValue(reg,shortName,_winreg.REG_SZ,menuName);
        reg=_winreg.CreateKey(reg1,"command")
        _winreg.SetValue(reg1,"command",_winreg.REG_SZ,command)
            
else:
    def registerMenu(key,menuName,command):
        print "ERR: Unable to register file extension with this OS!"

def register(filenames=None):
    """
    registers the given template(s) or all the templates in the "templates"
    directory if unspecified
    """
    class MT():pass
    def breakout(key,val,context):
        if val!="":
            setattr(context,"break",0)
        return context
    def savekey(key,val,context):
        setattr(context,key,fixString(val))
        return context
    def savearray(key,val,context):
        setattr(context,key,stringArray(val))
        return context
    fns={}
    fns["*"]=breakout
    fns["template_name"]=savekey
    fns["sources"]=savearray
    # figure out path
    path=os.path.abspath(__file__)
    path=path[0:path.rfind(os.sep)+1]+"templates"+os.sep
    if filenames==None:
        # list everything in the templates folder
        files=os.listdir(path)
        filenames=[]
        for filename in files:
            filenames.append(path+filename)
    if type(filenames).__name__!='list':
        filenames=[filenames]
    for filename in filenames:
        context=MT()
        processTemplate(filename, fns, context)
        if hasattr(context,"template_name")==False:
            print "File \"",filename,"\" missing $(template_name).  Skipping."
        elif hasattr(context,"sources")==False:
            print "File \"",filename,"\" missing $(sources).  Skipping."
        else:
            # register it for all sources and "folder"
            cmd="python \""+path+"template.py\" --template=\""+filename+"\" \"%1\""
            registerMenu("folder",context.template_name,cmd)
            for extn in context.sources:
                if extn!=None and extn!="":
                    if extn[0]!=".":
                        extn="."+extn
                    registerMenu(extn,context.template_name,cmd)


def template(templateFile, files, outDir=None):
    """
    runs the given template on the given list of files
    (any directories in with the files will start a recursive template)
    """
    class MT():pass
    if outDir==None:
        outDir=""
    else:
        os.makedirs(outDir)

    def generate(key,var,context):
        print "generate(",key,var,context,")"
        print "\tgenerating "+var
        params=stringArray(var)
        fileMappings={}
        for filename in context.files:
            if os.path.isfile(filename):
                # TODO: if this file is one of the applicable sources, generate
                resultFilename=""
                fileMappings[filename]=resultFilename
        context.mappings[params[3]]=fileMappings
        return context
    def sources(key,var,context):
        print "sources(",key,var,context,")"
        setattr(context,"sources",stringArray(var))
        return context
    def printout(key,var,context):
        print "printout(",key,var,context,")"
        if context.out==None:
            outFilename=outDir+filename[filename.rfind(os.sep):]
            context.out=open(outFilename,"w")
        context.out.write(var)
        return context
    def count(key,var,context):
        print "count(",key,var,context,")"
        if context.out==None:
            outFilename=outDir+context.filename[context.filename.rfind(os.sep):]
            context.out=open(outFilename,"w")
        context.out.write(str(len(files)))
        return context
    def switchFile(key,var,context):
        print "switchFile(",key,var,context,")"
        if context.out!=None:
            context.out.close()
            context.out=None
        context.filename=var
        return context
    def foreach(key,var,context):
        print "foreach(",key,var,context,")"
        if context.out==None:
            outFilename=outDir+context.filename[context.filename.rfind(os.sep):]
            context.out=open(outFilename,"w")
        var=var.split("$(")
        context.out.write(var[0])
        for i in range(1,len(var)):
            column=var[i]
            pos=column.find(")")
            sub=column[0:pos-1]
not exactly sure what I was going for here...
            if sub==currentSource:
                context.out.write(currentSource)
            else:
                context.out.write(context.mappings[sub][currentSource])
            context.out.write(column[pos+1:])
        return context

    fns={}
    fns["*"]=printout
    fns["generate"]=generate
    fns["sources"]=sources
    fns["count"]=count
    fns["foreach"]=foreach

    context=MT()
    setattr(context,"mappings",{})
    setattr(context,"out",None)
    setattr(context,"filename",templateFile)

    if type(files).__name__!='list':
        files=[files]
    
    # first thing, recurse (aka depth-first recursion)
    context.files=[]
    context.subdirs=[]
    for filename in files:
        if os.path.isdir(filename):
            # generate subdirs
            template(templateFile, os.listdir(filename), outDir)
            context.subdirs.append(filename)
        else:
            context.files.append(filename)
                             
    # now generate the template for this dir
    processTemplate(templateFile, fns, context)

    # shut things down
    if context.out!=None:
        context.out.close()

def fixString(string):
    """
    Takes a string, trims it, and un-quotes it as necessary
    """
    while string[-1]==" " or string[-1]=="\t" or string[-1]=="\r" or string[-1]=="\n":
        string=string[:-1]
    while string[0]==" " or string[0]=="\t":
        string=string[1:]
    while string[0]=='"' and string[-1]=='"':
        string=string[1:-1]
    return string

def stringArray(string):
    """
    Takes a string that looks anything like " a",b, c,47 and parses it into a viable array
    of strings like [" a","b","c","47"]

    TODO: currently "a", "b" yields ["a", "", "b"] and I can't see why??
    """
    result=[]
    start=-1
    for i in range(len(string)):
        if string[i]=='"':
            if start!=-1:
                result.append(string[start:i])
                while i<len(string) and string[i]!=',':
                    i=i+1
                if i<len(string):
                    i=i+1
                start=-1
            else:
                start=i+1
        elif string[i]==',':
            if start!=-1:
                result.append(string[start:i])
                start=-1
            else:
                start=i+1
        elif string[i]==' ':
            pass
        elif start==-1:
            start=i
    if start!=-1 and start<len(string):
        result.append(string[start:])

    return result
            


def processTemplate(filename, fns, context=None):
    """
    This reads a filename and for each $(key=val) item it will call fn["key"](key,val,context).
    For text outside of $() it will call fn["*"]("*",val,context).
    Finally, the $() can span multiple lines and can include $()'s within it. (Though these
        will be ignored at this level and must be processed manually by the called function.
    If the context object contains the special variable "break", after a fn[] call,
        we will break with the exit code given.
    """
    template=open(filename,"r")
    if template==None:
        print "Template file \"",filename,"\" not found!"
        return -1
    leftover=""
    lineOffs=0
    lineNo=0
    stack=0
    while True:
        lineNo=lineNo+1
        line=template.readline()
        print lineNo,": ",line
        if line==None or line=="": # should at least have a newline character
            template.close()
            return 0
        
        # trim trailing characters
        while line!="" and (line[-1]=="\n" or line[-1]=="\r" or line[-1]=="\t" or line[-1]==" "):
            line=line[:-1]
            
        if line=="":
            continue
            
        while True:
            pos = line.find("$(")
            if pos!=-1:
                if fns.has_key("*"):
                    context=fns["*"]("*",line[0:pos],context)
                    if hasattr(context,"break"):
                        return getattr(context,"break")
                line=line[pos+2:]
                next=line.find("=")
                close=line.find(")")
                if close<next and close!=-1:
                    key=line[0:close]
                    line=line[close+1:]
                    if fns.has_key(key):
                        context=fns[key](key,"",context)
                        if hasattr(context,"break"):
                            return getattr(context,"break")
                    else:
                        print "Unknown key $("+key+")"
                        # skip unknown keys
                        pass
                    continue
                key=line[0:next]
                line=line[next+1:]
                stack=stack+1
                while True:
                    for i in range(len(line)):
                        c=line[i]
                        if c==")":
                            stack=stack-1
                        elif c=="(":
                            stack=stack+1
                        if stack<=0:
                            break
                    if stack<=0:
                        print "Calling "+key
                        if fns.has_key(key):
                            context=fns[key](key,leftover+line[0:i],context)
                            if hasattr(context,"break"):
                                return getattr(context,"break")
                        else:
                            print "Unknown key $("+key+")"
                            # skip unknown keys
                            pass
                        leftover=""
                        lineNo=lineNo+lineOffs
                        line=line[i+1:]
                        lineOffs=0
                        break
                    else:
                        leftover=leftover+line
                        line=template.readline()
                        lineOffs=lineOffs+1
                        if line==None or line=="":
                            template.close()
                            print "Template error unterminated \"$(\" in \"",filename,"\" line ",str(lineNo)
                            return -1
                        while line!="" and (line[-1]=="\n" or line[-1]=="\r" or line[-1]=="\t" or line[-1]==" "):
                            line=line[:-1]
            else:
                if fns.has_key("*"):
                    context=fns["*"]("*",line,context)
                    if hasattr(context,"break"):
                        return getattr(context,"break")
                break

if __name__ == '__main__':
    """
    This will generate a webpage based on images in this directory from a template.
    """
    unknownArg=None
    templateName=None
    registerFlag=False
    outDir=None
    
    files=[]
    for i in range(1,len(sys.argv)):
        arg=sys.argv[i]
        if arg[0]=="-":
            while arg[0]=="-":
                arg=arg[1:]
            arg=arg.split("=")
            if arg[0]=="register":
                registerFlag=True
            elif arg[0]=="template":
                templateName=arg[1]
            elif arg[0]=="outdir":
                outDir=arg[1]
            else:
                unknownArg=True
        else:
            files.append(arg)

    if unknownArg!=None or (templateName==None and registerFlag==None):
        print "USAGE: python template.py [--register] [--template=template] [--outdir=dir] [filename(s)]"
    else:
        if registerFlag:
            register (templateName)
        else:
            template (templateName, files, outDir)

