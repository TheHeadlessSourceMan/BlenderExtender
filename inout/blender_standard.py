# This file is ONLY for all the importers and exporters that normally
# ship with Blender.  If you want to add your own import script,
# please create a new file for it.

from k_importExport import *
from Blender import *

# ---------- Blender built-in importer
class BlenderFileImporter(ObjectImporter):
    def listTypes(self):
        return [FileType(self,"Blender 3D","blend")]
    def importFile(self,filename):
        """
        You can do like "foo.blend" or "foo.blend:myObject1:myObject2"
        """
        filename,ext,objs=self.separate(filename)
        if ext!="blend":
            return None
        print "linking "+filename
        Library.Open(filename)
        groups = Library.LinkableGroups()
        if 'Object' in groups:
            for obname in Library.Datablocks('Object'):
                if len(objs)<1 or (obname in objs):
                    Library.Load(obname,'Object',0)
            Library.Update()
            Library.Close()

importers.add(BlenderFileImporter())


# ---------- 3d object importers
try:
    m=__import__("3ds_import", globals(), locals())
    class Blender3DSImporter(ObjectImporter):
        def listTypes(self):
            return [FileType(self,"3DS Max","3ds")]
        def importFile(self,filename):
            filename,ext,_=self.separate(filename)
            m.load_3ds(filename, False)
    importers.add(Blender3DSImporter())
except ImportError:
    pass


##try:
##    import ac3d_import
##    class BlenderAC3DImporter(ObjectImporter):
##        def listTypes(self):
##            return [FileType(self,"AC3D","ac")]
##        def importFile(self,filename):
##            filename,ext,_=self.separate(filename)
##            ac3d_import.AC3DImport(filename)
##    importers.add(BlenderAC3DImporter())
##except ImportError:
##    pass


#try:
#    import collada_import
#    class BlenderColladaImporter(ObjectImporter):
#        def listTypes(self):
#            return [FileType(self,"Collada 3D","dae")]
#        def importFile(self,filename):
#            filename,ext,_=self.separate(filename)
#            collada_import.main(filename)
#    importers.add(BlenderColladaImporter())
#except ImportError:
#    pass


##try:
##    import DirectX8Importer
##    class BlenderDirectXImporter(ObjectImporter):
##        def listTypes(self):
##            return [FileType(self,"DirectX 3D (v8)","x")]
##        def importFile(self,filename):
##            filename,ext,_=self.separate(filename)
##            DirectX8Importer.my_callback(filename)
##    importers.add(BlenderDirectXImporter())
##except ImportError:
##    pass


try:
    import flt_import
    class BlenderFLTImporter(ObjectImporter):
        def listTypes(self):
            return [FileType(self,"Open Flight","flt")]
        def importFile(self,filename):
            filename,ext,_=self.separate(filename)
            grr=flt_import.GlobalResourceRepository()
            flt_import.select_file(grr,filename)
    importers.add(BlenderFLTImporter())
except ImportError:
    pass


##try:
##    import import_dxf
##    class BlenderDXFImporter(ObjectImporter):
##        def listTypes(self):
##            return [FileType(self,"Audodesk (Drawing eXchange Format)","dxf")]
##        def importFile(self,filename):
##            """If you specify a directory, it can import everything!"""
##            filename,ext,_=self.separate(filename)
##            import_dxf.multi_import(filename)
##    importers.add(BlenderDXFImporter())
##except ImportError:
##    pass


try:
    import import_obj
    class BlenderOBJImporter(ObjectImporter):
        def listTypes(self):
            return [FileType(self,"Alias Wavefront 3D","obj")]
        def importFile(self,filename):
            filename,ext,_=self.separate(filename)
            import_obj.load_obj_ui(filename)
    importers.add(BlenderOBJImporter())
except ImportError:
    pass


try:
    import import_web3d
    class BlenderOBJImporter(ObjectImporter):
        def listTypes(self):
            return [FileType(self,"X3D","x3d"),FileType(self,"VRML97","vrml")]
        def importFile(self,filename):
            filename,ext,_=self.separate(filename)
            import_web3d.load_ui(filename)
            # load_web3d(path)
    importers.add(BlenderOBJImporter())
except ImportError:
    pass


try:
    import slp_import
    class BlenderSLPImporter(ObjectImporter):
        def listTypes(self):
            return [FileType(self,"Pro Engineer","slp")]
        def importFile(self,filename):
            filename,ext,_=self.separate(filename)
            slp_import.read(filename)
    importers.add(BlenderSLPImporter())
except ImportError:
    pass


try:
    import raw_import
    class BlenderRAWImporter(ObjectImporter):
        def listTypes(self):
            return [FileType(self,"Raw Triangles",["raw","tri"])]
        def importFile(self,filename):
            filename,ext,_=self.separate(filename)
            raw_import.read(filename)
    importers.add(BlenderRAWImporter())
except ImportError:
    pass


try:
    import ply_import
    class BlenderPLYImporter(ObjectImporter):
        def listTypes(self):
            return [FileType(self,"Stanford PLY","ply")]
        def importFile(self,filename):
            filename,ext,_=self.separate(filename)
            ply_import.load_ply(filename)
    importers.add(BlenderPLYImporter())
except ImportError:
    pass


try:
    import off_import
    class BlenderOFFImporter(ObjectImporter):
        def listTypes(self):
            return [FileType(self,"DEC Object File Format","off")]
        def importFile(self,filename):
            filename,ext,_=self.separate(filename)
            off_import.read(filename)
    importers.add(BlenderOFFImporter())
except ImportError:
    pass


try:
    import md2_import
    class BlenderMD2Importer(ObjectImporter):
        def listTypes(self):
            return [FileType(self,"Quake format","md2")]
        def importFile(self,filename):
            filename,ext,_=self.separate(filename)
            obj=md2_import.md2_obj()
            obj.load(filename)
    importers.add(BlenderMD2Importer())
except ImportError:
    pass


try:
    import lightwave_import
    class BlenderLWOImporter(ObjectImporter):
        def listTypes(self):
            return [FileType(self,"LightWave Object","lwo")]
        def importFile(self,filename):
            filename,ext,_=self.separate(filename)
            lightwave_import.read(filename)
    importers.add(BlenderLWOImporter())
except ImportError:
    pass


try:
    import ms3d_import
    class BlenderMS3DImporter(ObjectImporter):
        def listTypes(self):
            return [FileType(self,"MilkShape3D","ms3d")]
        def importFile(self,filename):
            filename,ext,_=self.separate(filename)
            ms3d_import.import_ms3d_ascii(filename)
    importers.add(BlenderMS3DImporter())
except ImportError:
    pass


try:
    import ms3d_import_ascii
    class BlenderMS3DTXTImporter(ObjectImporter):
        def listTypes(self):
            return [FileType(self,"MilkShape3D ASCII","txt")]
        def importFile(self,filename):
            filename,ext,_=self.separate(filename)
            ms3d_import.import_ms3d(filename)
    importers.add(BlenderMS3DTXTImporter())
except ImportError:
    pass


# ---------- path/motion importers
try:
    import bvh_import
    class BlenderBVHImporter(PathImporter):
        def listTypes(self):
            return [FileType(self,"BioVision motion capture","bvh")]
        def importFile(self,filename):
            filename,ext,_=self.separate(filename)
            bvh_import.load_bvh_ui(filename,False)
    importers.add(BlenderBVHImporter())
except ImportError:
    pass


try:
    import c3d_import
    class BlenderC3DImporter(PathImporter):
        def listTypes(self):
            return [FileType(self,"Graphics Lab Motion Capture","c3d")]
        def importFile(self,filename):
            filename,ext,_=self.separate(filename)
            c3d_import.load_c3d(filename)
    importers.add(BlenderC3DImporter())
except ImportError:
    pass


try:
    import import_lightwave_motion
    class BlenderLightwaveMotionImporter(PathImporter):
        def listTypes(self):
            return [FileType(self,"Lightwave Motion","mot")]
        def importFile(self,filename):
            filename,ext,_=self.separate(filename)
            # TODO: fix. This will load into whatever object is selected.
            import_lightwave_motion.FuncionPrincipal(filename)
    importers.add(BlenderLightwaveMotionImporter())
except ImportError:
    pass


try:
    import import_mdd
    class BlenderMDDImporter(PathImporter):
        def listTypes(self):
            return [FileType(self,"Lightwave MotionDesigner motion","mdd")]
        def importFile(self,filename):
            filename,ext,_=self.separate(filename)
            import_mdd.mdd_import_ui(filename)
    importers.add(BlenderMDDImporter())
except ImportError:
    pass


try:
    import paths_eps2obj
    class BlenderPSImporter(PathImporter):
        def listTypes(self):
            return [FileType(self,"PostScript",["ps","eps"])]
        def importFile(self,filename):
            filename,ext,_=self.separate(filename)
            paths_eps2obj.fonctionSELECT(filename)
    importers.add(BlenderPSImporter())
except ImportError:
    pass


try:
    import paths_svg2obj
    class BlenderSVGImporter(PathImporter):
        def listTypes(self):
            return [ \
                FileType(self,"Scalable Vector Graphic","svg"), \
                FileType(self,"Gimp 2.0 path","xsf") \
                ]
        def importFile(self,filename):
            filename,ext,_=self.separate(filename)
            paths_svg2obj.functionSELECT(filename)
    importers.add(BlenderSVGImporter())
except ImportError:
    pass


try:
    import paths_gimp2obj
    class BlenderOldGimpPathImporter(PathImporter):
        def listTypes(self):
            return [FileType(self,"Gimp 1.0 path","xsf")]
        def importFile(self,filename):
            filename,ext,_=self.separate(filename)
            paths_gimp2obj.fonctionSELECT(filename)
    importers.add(BlenderOldGimpPathImporter())
except ImportError:
    pass


try:
    import paths_ai2obj
    class BlenderIllustratorPathImporter(PathImporter):
        def listTypes(self):
            return [FileType(self,"Adobe illustrator","ai")]
        def importFile(self,filename):
            filename,ext,_=self.separate(filename)
            paths_ai2obj.fonctionSELECT(filename)
    importers.add(BlenderIllustratorPathImporter())
except ImportError:
    pass
