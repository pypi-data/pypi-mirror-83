"""
FILE: mayaviviewergiasscan.py
LAST MODIFIED: 24-12-2015 
DESCRIPTION: Container class for Scan instances in a mayavi scene.

===============================================================================
This file is part of GIAS2. (https://bitbucket.org/jangle/gias2)

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
===============================================================================
"""
import logging

from mayavi import mlab

from gias2.mappluginutils.mayaviviewer import MayaviViewerSceneObject, MayaviViewerObject

log = logging.getLogger(__name__)


class MayaviViewerGiasScanSceneObject(MayaviViewerSceneObject):
    typeName = 'giasscan'

    def __init__(self, name, slicerWidget, ISrc):
        self.name = name
        self.slicerWidget = slicerWidget
        self.ISrc = ISrc

    def setVisibility(self, visible):
        if self.slicerWidget:
            self.slicerWidget.visible = visible

    def remove(self):
        if self.slicerWidget:
            self.slicerWidget.remove()
            self.slicerWidget = None

        if self.ISrc:
            self.ISrc.remove()
            self.ISrc = None


class MayaviViewerGiasScan(MayaviViewerObject):
    typeName = 'giasscan'
    _vmax = 1800
    _vmin = -200
    _colourMap = 'black-white'
    _slicePlane = 'y_axes'

    def __init__(self, name, scan, renderArgs=None):
        self.name = name
        self.scan = scan
        self.sceneObject = None

        if renderArgs == None:
            self.renderArgs = {'vmin': self._vmin, 'vmax': self._vmax}
        else:
            self.renderArgs = renderArgs
            if 'vmax' not in list(self.renderArgs.keys()):
                self.renderArgs['vmax'] = self._vmax
            if 'vmin' not in list(self.renderArgs.keys()):
                self.renderArgs['vmin'] = self._vmin
            if 'colormap' not in list(self.renderArgs.keys()):
                self.renderArgs['colormap'] = self._colourMap

    def setScalarSelection(self, fieldName):
        pass

    def setVisibility(self, visible):
        self.sceneObject.setVisibility(visible)

    def remove(self):
        self.sceneObject.remove()
        self.sceneObject = None
        self.scan = None

    def draw(self, scene):
        scene.disable_render = True

        try:
            I = self.scan.I
        except AttributeError:
            log.debug('scan is None:', self.name)

        ISrc = mlab.pipeline.scalar_field(I, colormap=self.renderArgs['colormap'])
        slicerWidget = scene.mlab.pipeline.image_plane_widget(ISrc,
                                                              plane_orientation=self._slicePlane,
                                                              slice_index=0,
                                                              **self.renderArgs
                                                              )
        mlab.outline()
        self.sceneObject = MayaviViewerGiasScanSceneObject(self.name, slicerWidget, ISrc)
        scene.disable_render = False

        return self.sceneObject

    def changeSlicePlane(self, plane):
        self.sceneObject.slicerWidget.widgets[0].set(plane_orientation=plane)
        self._slicePlane = plane
