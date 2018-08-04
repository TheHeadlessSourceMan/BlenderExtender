Overview:
=========

::: {.indent}
BlenderExtender is a tool for using Blender to automatically generate
thumbnails for the Windows file explorer. The need is, like 2D images,
you can sometimes find the file you\'re looking for faster if you can
see what its contents are.\
\

Requirements:
-------------

Blender (duh).

Python 2.5 full install.

More Blender plugins to import other data types. (Optional. See
\"Extending\", below.)

\

This system consists of:
------------------------

An ExtensionManager.py app that lets you change settings of which files
are given to Blender to render and what Blender\'s render settings
should be.

A windows \"shell extension\" that feeds the file explorer whatever
thumbnails it needs.

A render tool that can start a hidden Blender app and render a
thumbnail.

A complimentary Blender script to manage that rendering.

A tool to add a context menu to folders such that we can automatically
generate a template. (For instance, auto-generate a \"download\" webpage
with thumbnails for all Blender content)
:::

Settings
========

All the settings for these applications are held in common and are taken
in the preferred order (high to low):

Stored inside active blender file.

Passed in on the command line.

Stored in settings.ini.

Best guess.

There are many, many things that can be specified, including:

::: {.indent}
frame=\[First,Middle,Last,Current\] (untested)\
osa=\[specified,0,5,8,11,16\]\
ao=\[specified,on,off\] (TODO)\
gi=\[specified,on,off\] (TODO)\
w=\[specified,\#\]\
h=\[specified,\#\]\
out=\[filename\]\
listTypes\
filename=\[filename\] (this can also be an unnamed input, but this
syntax is recommended for all but .blend files)\
:::

If you want to take some common action on an event, do:

::: {.indent}
onRenderSuccess=\[common\_event(s)\]\
onRenderFail=\[common\_event(s)\]\
onRenderDone=\[common\_event(s)\]\
:::

Example:

::: {.indent}
\--onRenderSuccess=close \--onRenderSuccess=hibernate
\--onRenderFail=\"email://gmail.com:user:passwd:myself@gmail.com,myself@gmail.com:OOPS!:Your
render of \$(filename) died.\"
:::

These other ones are irrelevent outside of the .ini file:

::: {.indent}
shellex=\[uuid of Blender shell extention\]
blender=\[location\_of\_blender\] renderThis=\[location\_of\_script\]
openThis=\[location\_of\_script\] outdir=\[location\_for\_output\]
icon=\[icon\_file\]
:::

Troubleshooting:
================

::: {.indent}
FAQ:
----

**I get an error that it can\'t find the blender.exe, even though it
says the right path.**\
This is probably because you are running with a cygwin python. This is
lame and not supported. Install the real win32 python instead.
:::

ExtensionManager.py:
====================

::: {.indent}
This utility will give you a menu list of available extensions and what
their settings are. This was written in Python because Python is already
requierd to run the thing, plus it makes dynamic menus much easier.\

It will look roughly like:
--------------------------

  -------------------- ------------------------ ----------------------- ----------------------------------
  **File Extension**   **Generate Thumbnail**   **Open with Blender**   **Full Name**
  .blend               X                        X                       blender 3d scene
  .ts3                 X                                                truespace 3d scene
  .obj                 X                        X                       alias 3d object
  .jpg                                                                  jpeg image
  .exr                 X                                                openexr high dynamic range image
  -------------------- ------------------------ ----------------------- ----------------------------------

\
This will manage the windows registry as needed, but be warned: This is
non-warranty code meddling with your system settings! BACKUP THE
REGISTRY OFTEN!!!
:::

Shell Extension:
================

::: {.indent}
The shell extension uses the render tool to render images for all
thumbnails that are out-of-date.\
\

It will also:
-------------

Show a \"dead monkey\" image for anything that was not renderable. This
image is customizable.
:::

Render Tool:
============

::: {.indent}
Renders a given file with the Blender command line in conjunction with a
python script that changes the render settings once the file is open.\
\
For info on the Blender command line see:\
<http://wiki.blender.org/index.php/Doc:Manual/Render/Command_Line_Options>\
\
See:
http://www.blender.org/documentation/246PythonDoc/Registry-module.html\
:::

Blender Rendering Script:
=========================

::: {.indent}
Though minimal support exists for causing Blender to render via the
command line, we need more control than that. Instead, we will start
Blender normally and send in extra parameters to our render managment
script.
:::

Templates:
==========

::: {.indent}
This is a simple, yet powerful python template-based file generating
system. It can also register those templates as file context menus.

Registering a Context Menu:
---------------------------

::: {.indent}
To register a template simply run:\
**python template.py \--register \--template=\[your template\]**\
If your template is in the templates directory then it\'s even easier.
Just say:\
**python template.py \--register**\
You can now right-click on any kind of file(s) that the template
supports and let \'er rip!
:::

Manually Running a Template:
----------------------------

::: {.indent}
If you\'re testing a problematic template or using a specialty template
as part of a larger project, you may want to run your template manually.
Fortunately, it\'s quite easy: **python template.py \--template=\[your
template\] \[files\_and\_directories\]**\
:::

Writing Your Own:
-----------------

::: {.indent}
The template files generally all live in the \"templates\" directory
immediately under your BlenderExtender install location.\
\
The template format is just the file you want output, plus\...\
\
There are settings MUST BE at the very top that specify how the template
is to be registered and used:\

::: {.indent}
\$(template\_name=\"Generate Something\") \-- file browser menu name\
\$(sources=\"blend\",\"obj\",\"3ds\") \-- acceptable types of input
files\
\$(generate=100,100,\"png\",\"png\_100x100\_image\") \-- generated
output \[width,height,type,name to refer to result as\]. You can have
more than one.\
:::

\
There are some values that are good everywhere:\

::: {.indent}
\$(count) \-- the number of files processed\
\$(foreach=\...) \-- a loop of template code added once for each of the
input items processed\
\$(file=file\_name) \-- start writing to a new output file. Notice that
if you\'re outputting stuff and you haven\'t specified an output file,
it\'s just the name of this template file.\
:::

\
These are good only inside the foreach:\

::: {.indent}
\$(source) \-- the source file name\
\$(\...) \-- one of the names you specified in a \$(generate=\...), for
example if you added the generate above, you could then use
\$(png\_100x100\_image)\
:::

\
Note that since all template things are like \$() that you could
possibly mess things up with your template. Some examples:\

::: {.indent}
**\$(foreach=I am happy :)-) \-- fail\
\$(foreach=I am happy :)-) \-- pass\
\
\$(foreach=You owe \$4.50) \-- pass\
\$(foreach=You owe \$(US)4.50) \-- fail\
\
\$(foreach=hi) \-- pass\
\$( foreach=hi) \-- fail\
\
\$(foreach=\$(image)) \-- pass\
\$(foreach=\$(image) \-- fail\
\
\$(foreach=\
hello, this is an image\
\$(image)\
) \-- pass\
\$(foreach=\
hello, this is an image\
\$(image\
) \-- fail\
**
:::
:::
:::

Extending:
==========

::: {.indent}
Extending for new file types is easy and requires only minimal Python
knowledge. Here\'s how\...\
TODO: Write this.
:::

Programming Notes:
==================

This program is intended to be installed with [spoon
installer](http://sourceforge.net/projects/spoon-installer/). To create
the install, run \"manual install.bat\" to get all the assets in the
correct place and then fire up the \".spi\" file in spoon.

If you build and register the shell extension, then rebuild,
VisualStudio won\'t be able to save the .dll \-- cuz explorer is still
using it. One way around this is to open the task manager and kill
explorer.exe as you build. Then when you\'re done you can restart it in
task manager by going File-\>Run and typing \"explorer\". Kindof a pain,
but it works.

For info on writing a completely new non-Blender windows thumbnail shell
extension, see:\
<http://www.codeproject.com/KB/shell/thumbextract.aspx>

This extension was only implemented for thumbnail view, which is a great
way to keep directory browsing nice and fast. However, if you wish to
extend this add support for custom icons as well, check out:\
<http://www.codeproject.com/KB/shell/shellextguide9.aspx>

Status:
=======

::: {.indent}
Done:
-----

windows shell extension

render script

settings system

template system

generic event system (for like things to call when render is done)

transparent render

a generic way to load file types from the command line

settings.ini can contain info on managing extensions (undo history, etc)

extension manager ui is successfully managing extensions

\"failed\" image customizable

rudimentary \"run hidden\" functionality

In Progress:
------------

shell extension is re-rendering every time

extension manager is not presently working

extension manager should autodetect what types \"Open\" can open

Next Items:
-----------

save per-file settings inside the .blend file as metadata

Create a saver tool on par with the universal loader.

template system is not generating any output

setup a default scene for loading/rendering images

write up some examples on how to do stuff

Devise a way of re-using Blender instance to eliminate app startup
times. (this will probably require intercommunicating with the spawned
program vis stdin/stdout)

obsoletes the plugins k\_uberLoadImg and k\_uberLoadModel and stuff in
k\_lib like \"BLENDER\_LOAD\_MODELS\". These need to be gone through and
revamped.

Eventually, Maybe:
------------------

opener for PIL python library

opener for ImageMagick python library

opener for VTK python library

opener for OpnCV python library

opener for Processing python library

figure out which standard blender importers are being stoopid and fix
them -OR- \...

Blender is supposedly coming out with a smarter import/export scheme.
When they do, change over to that.

Show a \"progress\" thumbnail for anything that is busy rendering.

bust out some math and figure out how to auto-recenter an scene and hide
the ground plane

implement flag \--ao=\[specified,on,off\]

implement flag \--gi=\[specified,on,off\]

implement the maths to re-center the camera on an object

extension manager ui should manage filetype icons and descriptions

when using the \"script to open itsself\" model, we should not be
sending the .ini settings on the command line
:::