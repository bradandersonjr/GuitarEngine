import os, sys
import adsk.core, adsk.fusion, adsk.cam, traceback, math
from math import sqrt
from ..ParameterValues import ParameterValues

class StringsBuilder:

    def __init__(self, app):
        self.app = app
        self.design = app.activeProduct

    def buildStrings(self, parameters):

        rootComp = self.design.rootComponent
        stringsOccs = rootComp.occurrences
        stringsOcc = stringsOccs.addNewComponent(adsk.core.Matrix3D.create())
        stringsComp = adsk.fusion.Component.cast(stringsOcc.component)

        stringCount = parameters.stringCount
        bridgeStringSpacing = parameters.bridgeStringSpacing
        nutStringSpacing = parameters.nutStringSpacing
        guitarLength = parameters.guitarLength
        headstockLength = parameters.headstockLength
        scaleLength = parameters.scaleLength
        nutLength = parameters.nutLength
        fretboardHeight = parameters.fretboardHeight
        machinePostHoleSpacing = parameters.machinePostHoleSpacing
        machinePostHoleDiameter = parameters.machinePostHoleDiameter
        machinePostDiameter = parameters.machinePostDiameter
        nutToPost = parameters.nutToPost
        headstockStyle = parameters.headstockStyle
        headstockThickness = parameters.headstockThickness

        # Create a new sketch.
        sketches = stringsComp.sketches
        xzPlane = stringsComp.xYConstructionPlane

        #Get extrude features
        extrudes = stringsComp.features.extrudeFeatures
        stringInset = (nutLength - nutStringSpacing)/2
        nutDistance = guitarLength - headstockLength

        if headstockStyle == 'Straight In-line':
            #Create sketch for bridge spacing
            sketch1 = sketches.add(xzPlane)
            sketch1.isComputeDeferred = True
            sketch1.arePointsShown = False
            sketch1.name = 'Strings [ ' + str((int(stringCount))) + ' strings ]'
            stringSketch = sketch1.sketchCurves.sketchLines

            for string in range(int(stringCount)):
                spacing = bridgeStringSpacing/2 - (bridgeStringSpacing/((int(stringCount))-1))*string
                nutSpacing = (nutLength-stringInset*2)/2 - ((nutLength-stringInset*2)/((int(stringCount))-1))*string
                holeSpacingHor = string*machinePostHoleSpacing
                stringsSketch = stringSketch.addByTwoPoints(adsk.core.Point3D.create(nutDistance-scaleLength, spacing, fretboardHeight+0.125), adsk.core.Point3D.create(nutDistance, nutSpacing, fretboardHeight+0.125))
                stringsSketch = stringSketch.addByTwoPoints(adsk.core.Point3D.create(nutDistance, nutSpacing, fretboardHeight+0.125), adsk.core.Point3D.create(nutDistance+nutToPost+holeSpacingHor, nutSpacing, 0))

            #Create sketch for bridge spacing
            sketch2 = sketches.add(xzPlane)
            sketch2.isComputeDeferred = True
            sketch2.arePointsShown = False
            sketch2.name = 'Machine Post Holes'
            machinePost = sketch2.sketchCurves.sketchCircles

            for spacing in range(int(stringCount)):
                holeSpacingVert = ((nutLength-stringInset*2)/2 - ((nutLength-stringInset*2)/((int(stringCount))-1))*spacing)
                holeSpacingHor = spacing*machinePostHoleSpacing
                machinePostHoles = machinePost.addByCenterRadius(adsk.core.Point3D.create(nutDistance+nutToPost+holeSpacingHor, holeSpacingVert+machinePostDiameter/2, 0), machinePostHoleDiameter/2)

        else:
            #Create sketch for bridge spacing
            sketch1 = sketches.add(xzPlane)
            sketch1.isComputeDeferred = True
            sketch1.arePointsShown = False
            sketch1.name = 'Strings [ ' + str((int(stringCount))) + ' strings ]'
            stringSketch = sketch1.sketchCurves.sketchLines

            for string in range(int(stringCount)):
                spacing = bridgeStringSpacing/2 - (bridgeStringSpacing/((int(stringCount))-1))*string
                nutSpacing = (nutLength-stringInset*2)/2 - ((nutLength-stringInset*2)/((int(stringCount))-1))*string
                holeSpacingHor = string*machinePostHoleSpacing
                stringsSketch = stringSketch.addByTwoPoints(adsk.core.Point3D.create(nutDistance-scaleLength, spacing, fretboardHeight+0.125), adsk.core.Point3D.create(nutDistance, nutSpacing, fretboardHeight+0.125))

            stringsSketch1 = stringSketch.addByTwoPoints(adsk.core.Point3D.create(nutDistance, nutStringSpacing/2, fretboardHeight+0.125), adsk.core.Point3D.create(nutDistance+nutToPost, nutStringSpacing/2, 0))
            stringsSketch2 = stringSketch.addByTwoPoints(adsk.core.Point3D.create(nutDistance, nutStringSpacing/2-(nutStringSpacing/5), fretboardHeight+0.125), adsk.core.Point3D.create(nutDistance+nutToPost+machinePostHoleSpacing, nutStringSpacing/2, 0))
            stringsSketch3 = stringSketch.addByTwoPoints(adsk.core.Point3D.create(nutDistance, nutStringSpacing/2-(nutStringSpacing/5*2), fretboardHeight+0.125), adsk.core.Point3D.create(nutDistance+nutToPost+machinePostHoleSpacing*2, nutStringSpacing/2, 0))
            stringsSketch4 = stringSketch.addByTwoPoints(adsk.core.Point3D.create(nutDistance, -nutStringSpacing/2+(nutStringSpacing/5*2), fretboardHeight+0.125), adsk.core.Point3D.create(nutDistance+nutToPost+machinePostHoleSpacing*2, -nutStringSpacing/2, 0))
            stringsSketch5 = stringSketch.addByTwoPoints(adsk.core.Point3D.create(nutDistance, -nutStringSpacing/2+(nutStringSpacing/5), fretboardHeight+0.125), adsk.core.Point3D.create(nutDistance+nutToPost+machinePostHoleSpacing, -nutStringSpacing/2, 0))
            stringsSketch6 = stringSketch.addByTwoPoints(adsk.core.Point3D.create(nutDistance, -nutStringSpacing/2, fretboardHeight+0.125), adsk.core.Point3D.create(nutDistance+nutToPost, -nutStringSpacing/2, 0))

            #Create sketch for bridge spacing
            sketch2 = sketches.add(xzPlane)
            sketch2.isComputeDeferred = True
            sketch2.arePointsShown = False
            sketch2.name = 'Machine Post Holes'
            machinePost = sketch2.sketchCurves.sketchCircles
            machinePostHole1 = machinePost.addByCenterRadius(adsk.core.Point3D.create(nutDistance+nutToPost, (nutStringSpacing/2)+(machinePostDiameter/2), 0), machinePostHoleDiameter/2)
            machinePostHole2 = machinePost.addByCenterRadius(adsk.core.Point3D.create(nutDistance+nutToPost+machinePostHoleSpacing, (nutStringSpacing/2)+(machinePostDiameter/2), 0), machinePostHoleDiameter/2)
            machinePostHole3 = machinePost.addByCenterRadius(adsk.core.Point3D.create(nutDistance+nutToPost+machinePostHoleSpacing*2, (nutStringSpacing/2)+(machinePostDiameter/2), 0), machinePostHoleDiameter/2)
            machinePostHole4 = machinePost.addByCenterRadius(adsk.core.Point3D.create(nutDistance+nutToPost+machinePostHoleSpacing*2, (-nutStringSpacing/2)-(machinePostDiameter/2), 0), machinePostHoleDiameter/2)
            machinePostHole5 = machinePost.addByCenterRadius(adsk.core.Point3D.create(nutDistance+nutToPost+machinePostHoleSpacing, (-nutStringSpacing/2)-(machinePostDiameter/2), 0), machinePostHoleDiameter/2)
            machinePostHole6 = machinePost.addByCenterRadius(adsk.core.Point3D.create(nutDistance+nutToPost, (-nutStringSpacing/2)-(machinePostDiameter/2), 0), machinePostHoleDiameter/2)

        tuningHoles = adsk.core.ObjectCollection.create()

        for holes in sketch2.profiles:
            tuningHoles.add(holes)

        #Get extrude features
        extrudes = stringsComp.features.extrudeFeatures

        if parameters.generateBlanks:
            #Extrusion for fret markers
            holesExtrude = extrudes.addSimple(tuningHoles, adsk.core.ValueInput.createByReal(-headstockThickness*2), adsk.fusion.FeatureOperations.CutFeatureOperation)
            holesExtrude.name = 'Extrusion: Tuning Machine Holes'

        # Group everything used to create the fretboard in the timeline.
        timelineGroupsStrings = self.design.timeline.timelineGroups
        stringsOccIndex = stringsOcc.timelineObject.index

        if parameters.generateBlanks:
            stringsEndIndex = holesExtrude.timelineObject.index
        else:
            stringsEndIndex = sketch2.timelineObject.index

        timelineGroupStrings = timelineGroupsStrings.add(stringsOccIndex, stringsEndIndex)
        timelineGroupStrings.name = 'Strings [ ' + str((int(stringCount))) + ' strings ]'
        stringsComp.name = 'Strings [ ' + str((int(stringCount))) + ' strings ]'

        return stringsComp