import Blender
from Blender import Scene


class FileOperator:
    def listTypes(self):
        pass
    def findTypes(self,filename):
        """
        returns all possible file types for a given filename
        """
        _,ext,_=self.separate(filename)
        foundTypes=[]
        types=self.listTypes()
        for t in types:
            if ext in t.extensions:
                foundTypes.append(t)
        return foundTypes
    def separate(self,filename):
        """
        separates a filename like myfile.foo:myobj1:myobj2
        into an undecorated filename, extension, and objects array
        """
        objs=[]
        pos=filename.rfind(".")
        ext=""
        if pos>-1:
            objs=filename[pos+1:].split(":")
            ext=objs[0]
            objs=objs[1:]
            filename=filename[0:pos+4] # cull off any :... junk
        return filename, ext, objs
    def __str__(self):
        result=self.__class__.__name__+":\n"
        types=self.listTypes()
        for t in types:
            result=result+"\t"+t.__str__()+"\n"
        return result
    

class FileImporter(FileOperator):
    def importFile(self,filename):
        pass
    def listTypes(self):
        pass


class FileExporter(FileOperator):
    def exportFile(self,filename):
        pass
    def listTypes(self):
        pass


class FileImporterSet(FileImporter):
    """
    a fileImporter capable of containing other fileImporters
    """
    def __init__(self):
        self.subImporters=[]
    def importFile(self,filename):
        """
        Imports the filename and returns the object or None.
        
        Also, this will use the first available importer.  For better control,
        use findTypes(filename), select one, then to selectedType.owner.importFile(filename)
        """
        types=self.findTypes(filename)
        if len(types)>0:
            return types[0].owner.importFile(filename)
        return None
    def add(self,importer):
        """
        adds a sub-importer to this importer
        """
        self.subImporters.append(importer)
    def listTypes(self):
        """
        Lists all acceptable types for this importer
        """
        allTypes=[]
        for sub in self.subImporters:
            types=sub.listTypes()
            if len(types)>0:
                allTypes=allTypes+types
        return allTypes


class FileExporterSet(FileExporter):
    """
    a fileExporter capable of containing other fileExporters
    """
    def __init__(self):
        subExporters=[]
    def exportFile(self,filename):
        """
        Imports the filename and returns the object or None.
        
        Also, this will use the first available exporter.  For better control,
        use findTypes(filename), select one, then to selectedType.owner.exportFile(filename)
        """
        types=self.findTypes(filename)
        if len(types)>0:
            return types[0].owner.importFile(filename)
        return None
    def add(self,exporter):
        """
        adds a sub-importer to this exporter
        """
        self.subExporters.append(exporter)
    def listTypes(self):
        """
        Lists all acceptable types for this exporter
        """
        allTypes=[]
        for sub in self.subExporters:
            types=sub.listTypes()
            if len(types)>0:
                allTypes=allTypes+types
        return allTypes


class ImageImporter(FileImporter):
    def importFile(self,filename):
        pass
    def listTypes(self):
        pass
    def importAsPlane(self,filename,w=None,h=None):
        pass
    def importAsTerrain(self,filename,w=None,h=None):
        pass


class ObjectImporter(FileImporter):
    def importFile(self,filename):
        pass
    def listTypes(self):
        pass


class PathImporter(FileImporter):
    def importFile(self,filename):
        pass
    def listTypes(self):
        pass
    def importAsMotion(self,filename,obj):
        pass
    def importAsIpo(self,filename,obj,curveName):
        pass


class FileType:
    def __init__(self, owner, name, extensions):
        self.name=name
        self.owner=owner
        if type(extensions).__name__!='list':
            self.extensions=[]
            self.extensions.append(extensions)
        else:
            self.extensions=extensions
    def __str__(self):
        result=self.name+" using "+self.owner.__class__.__name__+" ["
        for x in self.extensions:
            result=result+" ."+x
        return result+" ]"


# Create default lists
importers=FileImporterSet()
exporters=FileExporterSet()


# Import whatever is available
def loadAll():
    try:
        import os, glob, sys
        fullPython=True
    except ImportError:
        fullPython=False

    if fullPython==True:
        sys.path.append("inout")
        for inout in glob.glob("inout"+os.path.sep+"*"):
            inout=inout.split(os.path.sep)[-1][0:-3]
            m=__import__(inout, globals(), locals())
    else:
        import sys
        sys.path.append("inout")
        import blender_standard

def main():
    loadAll()
