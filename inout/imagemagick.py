try:
    # http://www.procoders.net/?p=39
    from PythonMagickWand import *
    hasImageMagick=PythonMagickWand
except ImportError:
    try:
        # http://www.imagemagick.org/download/python/
        from PythonMagick import *
        hasImageMagick=PythonMagick
    except ImportError:
        hasImageMagick=False


from k_importExport import *
        

if hasImageMagick!=False:
    class ImageMagickImporter(ImageImporter):
        def importFile(filename):
            pass
        def listTypes():
            # command line: convert -list format
            pass


if hasImageMagick!=False:
    importers.add(ImageMagickImporter())
    
