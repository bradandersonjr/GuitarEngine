import os, sys
import adsk.core, adsk.fusion, adsk.cam, traceback, math
from math import sqrt
from ..ParameterValues import ParameterValues

class BodyBlankBuilder:

    def __init__(self, app):
        self.app = app
        self.design = app.activeProduct

    def buildBodyBlank(self, parameters: ParameterValues):
        rootComp = self.design.rootComponent
        allOccs = rootComp.occurrences
        blanksOcc = allOccs.addNewComponent(adsk.core.Matrix3D.create())

        blanksComp = adsk.fusion.Component.cast(blanksOcc.component)
        
        bodyLength = parameters.bodyLength
        bodyWidth = parameters.bodyWidth
        bodyThickness = parameters.bodyThickness
        headstockLength = parameters.headstockLength
        headstockWidth = parameters.headstockWidth
        headstockThickness = parameters.headstockThickness
        guitarLength = parameters.guitarLength        

        # Create a new sketch.
        sketches = blanksComp.sketches
        xzPlane = blanksComp.xYConstructionPlane

        #Get extrude features
        extrudes = blanksComp.features.extrudeFeatures
        
        #Create sketch for bridge spacing
        sketch1 = sketches.add(xzPlane)
        sketch1.isComputeDeferred = False
        sketch1.name = 'Body Blank'
        bodyBlankSketch = sketch1.sketchCurves.sketchLines
        bodyBlank = bodyBlankSketch.addTwoPointRectangle(adsk.core.Point3D.create(0, -bodyWidth/2, 0), adsk.core.Point3D.create(bodyLength, bodyWidth/2, 0))
        
        #Create sketch for bridge spacing
        sketch2 = sketches.add(xzPlane)
        sketch2.isComputeDeferred = False
        sketch2.name = 'Headstock Blank'
        headstockBlankSketch = sketch2.sketchCurves.sketchLines
        headstockBlank = headstockBlankSketch.addTwoPointRectangle(adsk.core.Point3D.create(guitarLength-headstockLength, -headstockWidth/2, 0), adsk.core.Point3D.create(guitarLength, headstockWidth/2, 0))
        
        #Get extrude features
        extrudes = blanksComp.features.extrudeFeatures
        bodyProf = sketch1.profiles.item(0)
        headstockProf = sketch2.profiles.item(0)
        bodyExtrude = extrudes.addSimple(bodyProf, adsk.core.ValueInput.createByReal(-bodyThickness), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        # Get the extrusion body
        bodyBody = bodyExtrude.bodies.item(0)
        bodyExtrude.name = "Extrusion: Body Blank"
        bodyBody.name = "Body Blank"
        headstockExtrude = extrudes.addSimple(headstockProf, adsk.core.ValueInput.createByReal(-headstockThickness), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        
        # Get the extrusion body
        headstockBody = headstockExtrude.bodies.item(0)
        headstockExtrude.name = "Extrusion: Headstock Blank"
        headstockBody.name = "Headstock Blank"
        
        # Get a reference to an appearance in the library.
        lib = self.app.materialLibraries.itemByName('Fusion 360 Appearance Library')
        libAppear1 = lib.appearances.itemByName('Wax (White)')
        blanksAppearance1 = blanksComp.bRepBodies.item(0)
        blanksAppearance1.appearance = libAppear1
        blanksAppearance2 = blanksComp.bRepBodies.item(1)
        blanksAppearance2.appearance = libAppear1
        
        #Centers the camera to fit the entire fretboard
        cam = self.app.activeViewport.camera
        cam.isFitView = True
        cam.isSmoothTransition = False
        self.app.activeViewport.camera = cam
        
        # Group everything used to create the fretboard in the timeline.
        timelineGroupsBlanks = self.design.timeline.timelineGroups
        blanksOccIndex = blanksOcc.timelineObject.index
        blanksEndIndex = headstockExtrude.timelineObject.index
        timelineGroupBlanks = timelineGroupsBlanks.add(blanksOccIndex, blanksEndIndex)
        timelineGroupBlanks.name = 'Blanks'
        blanksComp.name = 'Blanks'
        
        return blanksComp