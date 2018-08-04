#!BPY

""" Registration info for Blender menus:
Name: 'k+) Center'
Blender: 242
Group: 'Object'
Tooltip: 'Recenter the camera to look at object(s).'
"""

__author__ = "Kurt"
__url__ = ""
__version__ = "1.0"
__bpydoc__ = """
Recenter and then zoom the camera to frame the current object(s).

A good idea, but me and math are not getting along well.
"""

# $Id: k_center.py,v 1.0 2007/12/25 23:14:48 kurt Exp $

import Blender
from Blender import *
from math import *

def center(objs=None,camera=None):
        """
        Using the given camera, current camera (or new camera) frame the shot so the given object(s) are centered

        If no object(s) are specified, it will try to frame all existing objects.
        """
        scene=Scene.GetCurrent()
        if objs==None:
            objs=scene.objects
        if objs==None:
            return
        if type(objs).__name__!='list':
            objs = [objs]
        elif  len(objs)<1:
            return
        if camera==None:
            camera = scene.objects.camera
        if camera==None:
                camera = scene.objects.new (Blender.Camera.New())
                camera.setLocation (10.0, 10.0, 10.0)
                camera.setEuler (Euler(-45.0,0.0,45.0))
        # figure out the space occupied by everything togehter
        xmax=-65535;xmin=65535;ymax=-65535;ymin=65535;zmax=-65535;zmin=65535;
        for obj in objs:
            bb=obj.getBoundBox()
            if bb == None:
                print dir(obj)
                pass
            else:
                for pt in bb:
                    xmin=min(xmin,pt[0])
                    xmax=max(xmax,pt[0])
                    ymin=min(ymin,pt[1])
                    ymax=max(ymax,pt[1])
                    zmin=min(zmin,pt[2])
                    zmax=max(zmax,pt[2])
        if xmax == None:
            print "ERROR: No objects found to center to."
            return -1
        xspan=xmax-xmin
        yspan=ymax-ymin
        zspan=zmax-zmin
        xcenter=xmin+(xspan/2)
        ycenter=xmin+(yspan/2)
        zcenter=xmin+(zspan/2)
        camera.clearTrack()
        camx,camy,camz=camera.getLocation()
        # Rotate camera to face center point
        rx=cos((camy-ycenter)/(camz-zcenter))
        ry=cos((camz-zcenter)/(camx-xcenter))
        rz=cos((camx-xcenter)/(camy-ycenter))
        camera.RotX=rx
        camera.RotY=ry
        camera.RotZ=rz
        # TODO: Zoom in/out until we fill the frame

if __name__ == '__main__':
    print "-----------"
    center(Object.GetSelected())
