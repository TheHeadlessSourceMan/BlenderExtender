try:
    import vtk
    import VTKBlender
    reload(VTKBlender)
    from VTKBlender import *
    from vtk import *
    from vtkpython import *
    hasVTK=True
except ImportError:
    print "vtk not installed."
    hasVTK=False


from k_importExport import *


if hasVTK!=False:
    class VtkFileType(FileType):
        loaderFn
        def __init__(self, name, loaderFn, extensions):
            FileType.__init__(self, name, extensions)
            self.loaderFn=loaderFn

            
if hasVTK!=False:
    class VtkModelImporter(FileImporter):
        types=[]
        def __init__(self):
            self.types.append(VtkFileType("3DS Max",vtk3DSImporter,["3ds","max"]))
            self.types.append(VtkFileType("BYU polygon files",vtkBYUReader,["g","d","t"]))
            self.types.append(VtkFileType("Chaco http://www.cs.sandia.gov/~bahendr/chaco.html",vtkChacoReader,"chaco"))
            self.types.append(VtkFileType("EnSight files",vtkEnSightReader,["ensight","ens"]))
            self.types.append(VtkFileType("ExodusII Files",vtkExodusReader,["ex","ex2"]))
            self.types.append(VtkFileType("ASCII Facet Files",vtkFacetReader,"facet"))
            self.types.append(VtkFileType("ASCII GAMBIT neutral format",vtkGambitReader,"gambit"))
            self.types.append(VtkFileType("ASCII Gaussian Cube format http://www.gaussian.com/00000430.htm",vtkGaussianCubeReader,"gaussian"))
            self.types.append(VtkFileType("Marching Cubes files",vtkMCubesReader,["mar","mcu"]))
            self.types.append(VtkFileType("binary or a text file of particles",vtkParticleReader,"part"))
            self.types.append(VtkFileType("Alias/Wavefront OBJ files",vtkOBJReader,"obj"))
            self.types.append(VtkFileType("Volume Images",vtkVolumeReader,"ximg"))
            self.types.append(VtkFileType("PDB Molecule file",vtkPDBReader,"pdb"))
            self.types.append(VtkFileType("PLOT3D Fluid Dynamics file",vtkPLOT3DReader,"plot3d"))
            self.types.append(VtkFileType("Stanford PLY polygonal file",vtkPLYReader,"ply"))
            self.types.append(VtkFileType("Simple XYZ points",vtkSimplePointsReader,"txt"))
            self.types.append(VtkFileType("SLC volume file",vtkSLCReader,"slc"))
            self.types.append(VtkFileType("STL (stereo lithography) file",vtkSTLReader,"stl"))
            self.types.append(VtkFileType("VRML Files",vtkVRMLImporter,"vrml"))
            self.types.append(VtkFileType("EDS Unigraphics facet file",vtkUGFacetReader,"eds"))
            self.types.append(VtkFileType("XYZMol Molecular Data files",vtkXYZMolReader,"xyzmol"))
        def importFile(self,filename):
            pipeline=[]
            pipeline.append(vtk.vtkDataReader())
            pipeline[0].SetFileName(filename)
            pipeline[0].SetMerging(1)
            return vtk2Blend(pipeline[0].GetOutput(),None)
        def listTypes(self):
            return self.types
            pass

                              
if hasVTK!=False:
    class VtkImageImporter(ImageImporter):
        types=[]
        def __init__(self):
            self.types.append(VtkFileType("USGS DEM File",vtkDEMReader,"dem"))
            self.types.append(VtkFileType("DICOM Medical Imageing File",vtkDICOMReader,"dicom"))
            self.types.append(VtkFileType("JPEG File",vtkJPEGReader,["jpeg","jpg","jpe"]))
            self.types.append(VtkFileType("PNG File",vtkPNGReader,"png"))
            self.types.append(VtkFileType("SLC volume File",vtkSLCReader,"slc"))
            self.types.append(VtkFileType("PNM File",vtkPNMReader,["pbm","pgm","ppm"]))
            self.types.append(VtkFileType("BMP File",vtkBMPReader,"bmp"))
            self.types.append(VtkFileType("GE Signa File",vtkGESignaReader,"ximg"))
            self.types.append(VtkFileType("UNC meta image data",vtkMetaImageReader,["mha","mhd"]))
            self.types.append(VtkFileType("TIFF File",vtkTIFFReader,["tiff","tif","tga","targa","iff"]))
        def importFile(self,filename):
            filename,ext,_=self.separate(self,filename)
            newFilename=filename+"_tmp.png"
            img=vtkLoadImage(filename+"."+ext)
            vtkSaveImage(img,newFilename)
            img=Image.Load(newFilename)
            # TODO: delete filename+"_tmp.png"
            return img
        def listTypes(self):
            return self.types


if hasVTK!=False:
    class VtkImageExporter(ImageExporter):
        types=[]
        def __init__(self):
            self.types.append(VtkFileType("PostScript File",vtkPostScriptWriter,"ps"))
            self.types.append(VtkFileType("JPEG File",vtkJPEGWriter,["jpeg","jpg","jpe"]))
            self.types.append(VtkFileType("PNG File",vtkPNGWriter,"png"))
            self.types.append(VtkFileType("PNM File",vtkPNMWriter,["pbm","pgm","ppm"]))
            self.types.append(VtkFileType("BMP File",vtkBMPWriter,"bmp"))
            self.types.append(VtkFileType("UNC meta image data",vtkMetaImageWriter,["mha","mhd"]))
            self.types.append(VtkFileType("TIFF File",vtkTIFFWriter,["tiff","tif","tga","targa"]))
        def exportFile(self,filename):
            pass
        def listTypes(self):
            return self.types


if hasVTK!=False:
    importers.add(VtkModelImporter())
    importers.add(VtkImageImporter())
    exporters.add(VtkImageExporter())
