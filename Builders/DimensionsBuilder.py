import os, sys
import adsk.core, adsk.fusion, adsk.cam, traceback, math
from math import sqrt
from ..ParameterValues import ParameterValues

class DimensionsBuilder:

    def __init__(self, app):
        self.app = app
        self.design = app.activeProduct

    def buildDimensions(self, parameters: ParameterValues):

        rootComp = self.design.rootComponent
        allOccs2 = rootComp.occurrences
        newOcc2 = allOccs2.addNewComponent(adsk.core.Matrix3D.create())
        dimsComp = adsk.fusion.Component.cast(newOcc2.component)

        fretNumber = parameters.fretNumber
        scaleLength = parameters.scaleLength
        nutLength = parameters.nutLength
        endLength = parameters.endLength
        nutRadius = parameters.nutRadius
        endRadius = parameters.endRadius
        fretboardHeight = parameters.fretboardHeight
        filletRadius = parameters.filletRadius
        endCurve = parameters.endCurve
        tangWidth = parameters.tangWidth
        bridgeStringSpacing = parameters.bridgeStringSpacing
        tangDepth = parameters.tangDepth
        nutSlotWidth = parameters.nutSlotWidth
        nutSlotDepth = parameters.nutSlotDepth
        markerDiameter = parameters.markerDiameter
        markerDepth = parameters.markerDepth
        markerSpacing = parameters.markerSpacing
        guitarLength = parameters.guitarLength
        bodyWidth = parameters.bodyWidth
        headstockLength = parameters.headstockLength
        bodyLength = parameters.bodyLength
        stringCount = parameters.stringCount
        nutToPost = parameters.nutToPost
        machinePostHoleSpacing = parameters.machinePostHoleSpacing
        machinePostHoleDiameter = parameters.machinePostHoleDiameter
        machinePostDiameter = parameters.machinePostDiameter
        nutStringSpacing = parameters.nutStringSpacing
        fretboardLength = parameters.fretboardLength
        headstockStyle = parameters.headstockStyle
        neckSpacing = parameters.neckSpacing
        bridgeSpacing = parameters.bridgeSpacing
        singleCoilLength = parameters.singleCoilLength
        singleCoilWidth = parameters.singleCoilWidth
        singleCoilDepth = parameters.singleCoilDepth
        humbuckerLength = parameters.humbuckerLength
        humbuckerWidth = parameters.humbuckerWidth
        humbuckerDepth = parameters.humbuckerDepth
        humbuckerFillet = parameters.humbuckerFillet
        pickupNeck = parameters.pickupNeck
        pickupMiddle = parameters.pickupMiddle
        pickupBridge = parameters.pickupBridge
        pickupCavityMountLength = parameters.pickupCavityMountLength
        pickupCavityMountTabWidth = parameters.pickupCavityMountTabWidth        
        bridgePickupAngle =  self.design.unitsManager.convert(parameters.bridgePickupAngle, 'deg', 'rad')

        #Equation for fret spacing
        for fretNum in range(1,int((fretNumber))+1):
            fretDistance = (scaleLength)-((scaleLength)/(2**(fretNum/12.0)))
        
        #This calculates and rounds the total length of the fretboard using the scale length and number of frets
        L = fretboardLength
        stringInset = (nutLength - nutStringSpacing)/2
        nutDistance = guitarLength - headstockLength
        width = (nutLength-(stringInset*2)) + (2*sqrt(((L/(math.cos(math.radians(math.acos((scaleLength**2+(sqrt((((bridgeStringSpacing-(nutLength-(stringInset*2)))/2)**2)+(scaleLength**2)))**2-
                                                ((bridgeStringSpacing-(nutLength-(stringInset*2)))/2)**2)/(2*scaleLength*(sqrt((((bridgeStringSpacing-(nutLength-(stringInset*2)))/2)**2)+(scaleLength**2)))))*((180)/math.pi)))))**2)
                                                -(L**2)))

        # Create a new sketch.
        sketches = dimsComp.sketches
        yzPlane = dimsComp.yZConstructionPlane
        xzPlane = dimsComp.xYConstructionPlane
        xyPlane = dimsComp.xYConstructionPlane

        #Create construction lines
        sketch1 = sketches.add(xzPlane)
        sketch1.isComputeDeferred = True
        lines = sketch1.sketchCurves.sketchLines
        sketch1.name = 'Boundary Dimensions'
        sketch1.isVisible = True
        sketch1.areDimensionsShown = True
        sketch1.areConstraintsShown = False
        sketch1.arePointsShown = False
        sketch1.areProfilesShown = False
        centerLine = lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(guitarLength, 0, 0))
        centerLine.isConstruction = True
        centerLine.isFixed = True
        originBoundary = lines.addByTwoPoints(adsk.core.Point3D.create(0, bodyWidth/2, 0), adsk.core.Point3D.create(0, -bodyWidth/2, 0))
        originBoundary.isConstruction = True
        endBoundary = lines.addByTwoPoints(adsk.core.Point3D.create(guitarLength, bodyWidth/2, 0), adsk.core.Point3D.create(guitarLength, -bodyWidth/2, 0))
        endBoundary.isConstruction = True
        topBoundary = lines.addByTwoPoints(adsk.core.Point3D.create(0, bodyWidth/2, 0), adsk.core.Point3D.create(guitarLength, bodyWidth/2, 0))
        topBoundary.isConstruction = True
        bottomBoundary = lines.addByTwoPoints(adsk.core.Point3D.create(0, -bodyWidth/2, 0), adsk.core.Point3D.create(guitarLength, -bodyWidth/2, 0))
        bottomBoundary.isConstruction = True
        bodyBoundary = lines.addByTwoPoints(adsk.core.Point3D.create(bodyLength, bodyWidth/2, 0), adsk.core.Point3D.create(bodyLength, -bodyWidth/2, 0))
        bodyBoundary.isConstruction = True
        nutBoundary = lines.addByTwoPoints(adsk.core.Point3D.create(nutDistance, bodyWidth/4, 0), adsk.core.Point3D.create(nutDistance, -bodyWidth/4, 0))
        nutBoundary.isConstruction = True
        bridgeBoundary = lines.addByTwoPoints(adsk.core.Point3D.create(nutDistance-scaleLength, bodyWidth/4, 0), adsk.core.Point3D.create(nutDistance-scaleLength, -bodyWidth/4, 0))
        bridgeBoundary.isConstruction = True
        fret12Boundary = lines.addByTwoPoints(adsk.core.Point3D.create(nutDistance-scaleLength/2, bodyWidth/4, 0), adsk.core.Point3D.create(nutDistance-scaleLength/2, -bodyWidth/4, 0))
        fret12Boundary.isConstruction = True

        #Create dimension lines
        sketch1.areDimensionsShown = True
        sketch1.sketchDimensions.addDistanceDimension(topBoundary.startSketchPoint, topBoundary.endSketchPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create((topBoundary.length/2), bodyWidth/2+4, 0), False)
        sketch1.sketchDimensions.addDistanceDimension(originBoundary.startSketchPoint, originBoundary.endSketchPoint,
                                                     adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                     adsk.core.Point3D.create(-4, 0, 0), False)
        sketch1.sketchDimensions.addDistanceDimension(bridgeBoundary.startSketchPoint, fret12Boundary.startSketchPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create((nutDistance-scaleLength+scaleLength/4), bodyWidth/4+2, 0), False)
        sketch1.sketchDimensions.addDistanceDimension(fret12Boundary.startSketchPoint, nutBoundary.startSketchPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create((nutDistance-scaleLength/4), bodyWidth/4+2, 0), False)
        sketch1.sketchDimensions.addDistanceDimension(topBoundary.startSketchPoint, bodyBoundary.startSketchPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create((bodyLength/2), bodyWidth/2+2, 0), False)
        sketch1.sketchDimensions.addDistanceDimension(bodyBoundary.startSketchPoint, topBoundary.endSketchPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create(((guitarLength+bodyLength)/2), bodyWidth/2+2, 0), False)
        sketch1.sketchDimensions.addDistanceDimension(topBoundary.startSketchPoint, centerLine.startSketchPoint,
                                                     adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                     adsk.core.Point3D.create(-2, bodyWidth/4, 0), False)
        sketch1.sketchDimensions.addDistanceDimension(centerLine.startSketchPoint, bottomBoundary.startSketchPoint,
                                                     adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                     adsk.core.Point3D.create(-2, -bodyWidth/4, 0), False)
        sketch1.sketchDimensions.addDistanceDimension(centerLine.startSketchPoint, bridgeBoundary.startSketchPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create(((guitarLength-headstockLength-scaleLength)/2), bodyWidth/4+2, 0), False)
        sketch1.sketchDimensions.addDistanceDimension(nutBoundary.startSketchPoint, centerLine.endSketchPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create((guitarLength-headstockLength/2), bodyWidth/4+2, 0), False)

        sketch2 = sketches.add(xzPlane)
        sketch2.isComputeDeferred = True
        dimensionFrets = sketch2.sketchCurves.sketchLines
        dimensionFrets2 = sketch2.sketchCurves.sketchLines
        dimensionCircles = sketch2.sketchCurves.sketchCircles
        dimensionCircles2 = sketch2.sketchCurves.sketchCircles
        dimensionLines = sketch2.sketchCurves.sketchLines
        humbuckerCavitySketch = sketch2.sketchCurves.sketchLines
        sketch2.name = 'Core Dimensions'
        sketch2.isVisible = True
        sketch2.areDimensionsShown = True
        sketch2.areConstraintsShown = False
        sketch2.arePointsShown = False
        sketch2.areProfilesShown = False

        for fret in range(int(fretNumber)+1):
            fretDistance = scaleLength-(scaleLength/(2**(fret/12.0)))
            fretLength = nutLength + 2*sqrt(((fretDistance/(math.cos(math.radians(math.acos((L**2+(sqrt((((endLength-nutLength)/2)**2) +(L**2)))**2-
                                    ((endLength-nutLength)/2)**2)/(2*L*(sqrt((((endLength-nutLength)/2)**2)+(L**2)))))*((180)/math.pi)))))**2)
                                    -(fretDistance**2))
            dimensioning = dimensionFrets.addByTwoPoints(adsk.core.Point3D.create((nutDistance-fretDistance), (fretLength/2), 0),
                                                         adsk.core.Point3D.create((nutDistance-fretDistance), (-fretLength/2), 0))
            dimensioning.isConstruction = True

        dimensioning2 = dimensionFrets2.addByTwoPoints(adsk.core.Point3D.create(nutDistance-L, (endLength/2), 0), adsk.core.Point3D.create(nutDistance-L, (-endLength/2), 0))
        dimensioning2.isConstruction = True
        bridgeLine2 = dimensionFrets2.addByTwoPoints(adsk.core.Point3D.create(nutDistance-scaleLength, (bridgeStringSpacing/2), 0), adsk.core.Point3D.create(nutDistance-scaleLength, (-bridgeStringSpacing/2), 0))
        bridgeLine2.isConstruction = True

        for dime in range(int(fretNumber)):
            sketchDime1 = sketch2.sketchDimensions.addDistanceDimension(dimensionFrets[0+dime].startSketchPoint, dimensionFrets[1+dime].startSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create((nutDistance-scaleLength-(scaleLength/(-2**((dime+0.5)/12.0)))), 5, 0), False);
        
        for dime in range(1, int(fretNumber)+1):
            sketchDime1 = sketch2.sketchDimensions.addDistanceDimension(dimensionFrets[0].endSketchPoint, dimensionFrets[0+dime].endSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create((nutDistance-scaleLength-(scaleLength/(-2**((dime-0.5)/12.0)))), -5-(dime/4), 0), False);
        
        sketchDime2 = sketch2.sketchDimensions.addDistanceDimension(dimensionFrets[0].startSketchPoint,
                                                       dimensionFrets[0].endSketchPoint, adsk.fusion.DimensionOrientations.VerticalDimensionOrientation, adsk.core.Point3D.create(nutDistance+2, 0, 0), False)
        sketchDime3 = sketch2.sketchDimensions.addDistanceDimension(dimensioning2.startSketchPoint,
                                                       dimensioning2.endSketchPoint, adsk.fusion.DimensionOrientations.VerticalDimensionOrientation, adsk.core.Point3D.create(nutDistance-L-1, 0, 0), False)
        sketchDime4 = sketch2.sketchDimensions.addDistanceDimension(dimensioning2.endSketchPoint,
                                                       dimensionFrets[0].endSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create(nutDistance-L/2, -12, 0), False)
        sketchDime5 = sketch2.sketchDimensions.addDistanceDimension(bridgeLine2.startSketchPoint,
                                                       dimensionFrets[0].startSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create(nutDistance-scaleLength/2, 8, 0), False)
        sketchDime6 = sketch2.sketchDimensions.addDistanceDimension(bridgeLine2.startSketchPoint,
                                                       bridgeLine2.endSketchPoint, adsk.fusion.DimensionOrientations.VerticalDimensionOrientation, adsk.core.Point3D.create(nutDistance-scaleLength-1, 0, 0), False)
                                                       
        if headstockStyle == 'Straight In-line':
            #Create sketch for bridge spacing
            for spacing in range(int(stringCount)):
                holeSpacingVert = (nutLength-stringInset*2)/2 - ((nutLength-stringInset*2)/(int(stringCount)-1))*spacing
                holeSpacingHor = spacing*machinePostHoleSpacing
                machinePosts = dimensionCircles.addByTwoPoints(adsk.core.Point3D.create(nutDistance+nutToPost+holeSpacingHor, holeSpacingVert, 0), adsk.core.Point3D.create(nutDistance+nutToPost+holeSpacingHor, holeSpacingVert+(machinePostDiameter), 0))
                machinePosts.isConstruction = True
            for dime in range(int(stringCount)-1):
                sketchDime7 = sketch2.sketchDimensions.addDistanceDimension(dimensionCircles[0+dime].centerSketchPoint, dimensionCircles[1+dime].centerSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                                            adsk.core.Point3D.create((nutDistance+nutToPost+machinePostHoleSpacing*dime)+machinePostHoleSpacing/2, 4, 0), False);
                sketchDime8 = sketch2.sketchDimensions.addDistanceDimension(dimensionCircles[0+dime].centerSketchPoint, dimensionCircles[1+dime].centerSketchPoint, adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                                            adsk.core.Point3D.create(guitarLength+2, (nutLength-stringInset*2)/2 - ((nutLength-stringInset*2)/(int(stringCount)-1))*dime, 0), False);
            sketchDime9 = sketch2.sketchDimensions.addDistanceDimension(dimensionFrets.item(0).startSketchPoint, dimensionCircles.item(0).centerSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create(nutDistance+nutToPost/2, 4, 0), False);
        else:
            pass
            machinePosts = sketch2.sketchCurves.sketchCircles            
            machinePostHole1 = machinePosts.addByCenterRadius(adsk.core.Point3D.create(nutDistance+nutToPost, (nutStringSpacing/2)+(machinePostDiameter/2), 0), machinePostDiameter/2)
            machinePostHole1.isConstruction = True
            machinePostHole2 = machinePosts.addByCenterRadius(adsk.core.Point3D.create(nutDistance+nutToPost+machinePostHoleSpacing, (nutStringSpacing/2)+(machinePostDiameter/2), 0), machinePostDiameter/2)
            machinePostHole2.isConstruction = True
            machinePostHole3 = machinePosts.addByCenterRadius(adsk.core.Point3D.create(nutDistance+nutToPost+machinePostHoleSpacing*2, (nutStringSpacing/2)+(machinePostDiameter/2), 0), machinePostDiameter/2)
            machinePostHole3.isConstruction = True
            machinePostHole4 = machinePosts.addByCenterRadius(adsk.core.Point3D.create(nutDistance+nutToPost+machinePostHoleSpacing*2, (-nutStringSpacing/2)-(machinePostDiameter/2), 0), machinePostDiameter/2)
            machinePostHole4.isConstruction = True
            machinePostHole5 = machinePosts.addByCenterRadius(adsk.core.Point3D.create(nutDistance+nutToPost+machinePostHoleSpacing, (-nutStringSpacing/2)-(machinePostDiameter/2), 0), machinePostDiameter/2)
            machinePostHole5.isConstruction = True
            machinePostHole6 = machinePosts.addByCenterRadius(adsk.core.Point3D.create(nutDistance+nutToPost, (-nutStringSpacing/2)-(machinePostDiameter/2), 0), machinePostDiameter/2)
            machinePostHole6.isConstruction = True
            sketchDime10 = sketch2.sketchDimensions.addDistanceDimension(dimensionFrets.item(0).startSketchPoint, machinePostHole1.centerSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create(nutDistance+nutToPost/2, 4, 0), False)
            sketchDime11 = sketch2.sketchDimensions.addDistanceDimension(machinePostHole1.centerSketchPoint, machinePostHole2.centerSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create(nutDistance+nutToPost+machinePostHoleSpacing/2, 4, 0), False)
            sketchDime12 = sketch2.sketchDimensions.addDistanceDimension(machinePostHole2.centerSketchPoint, machinePostHole3.centerSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create(nutDistance+nutToPost+machinePostHoleSpacing*1.5, 4, 0), False)
            sketchDime13 = sketch2.sketchDimensions.addDistanceDimension(machinePostHole3.centerSketchPoint, machinePostHole4.centerSketchPoint, adsk.fusion.DimensionOrientations.VerticalDimensionOrientation, adsk.core.Point3D.create(nutDistance+machinePostHoleSpacing*3+2, 0, 0), False)

        ### PICKUPS
        sketch3 = sketches.add(xzPlane)
        sketch3.isComputeDeferred = True
        sketch3.name = 'Pickup Dimensions'
        sketch3.isVisible = True
        sketch3.areDimensionsShown = True
        sketch3.areConstraintsShown = False
        sketch3.arePointsShown = False
        sketch3.areProfilesShown = False
        neckDistance = guitarLength - headstockLength - fretboardLength - neckSpacing
        bridgeDistance = guitarLength - headstockLength - scaleLength + bridgeSpacing
        middleDistance = bridgeDistance + (neckDistance - bridgeDistance)/2
        neckLines = sketch3.sketchCurves.sketchLines
        cavityNeckLines = sketch3.sketchCurves.sketchLines

        if pickupNeck == "Single-Coil":
            # Create sketch lines
            pickupNeck1 = neckLines.addCenterPointRectangle(adsk.core.Point3D.create((neckDistance-singleCoilWidth/2), 0, 0), adsk.core.Point3D.create((neckDistance-singleCoilWidth/2)+singleCoilWidth/2, (singleCoilLength/2), 0))
            pickupNeck1[0].isConstruction = True
            pickupNeck1[1].isConstruction = True
            pickupNeck1[2].isConstruction = True
            pickupNeck1[3].isConstruction = True
            pickupNeck2 = neckLines.addByTwoPoints(adsk.core.Point3D.create((neckDistance-singleCoilWidth/2), (-pickupCavityMountLength/2), 0), adsk.core.Point3D.create((neckDistance-singleCoilWidth/2), (pickupCavityMountLength/2), 0))
            pickupNeck2.isConstruction = True
            pickupNeckFillet1 = sketch3.sketchCurves.sketchArcs.addFillet(pickupNeck1[0], pickupNeck1[0].endSketchPoint.geometry, pickupNeck1[1], pickupNeck1[1].startSketchPoint.geometry, singleCoilWidth/2)
            pickupNeckFillet1.isConstruction = True
            pickupNeckFillet2 = sketch3.sketchCurves.sketchArcs.addFillet(pickupNeck1[1], pickupNeck1[1].endSketchPoint.geometry, pickupNeck1[2], pickupNeck1[2].startSketchPoint.geometry, singleCoilWidth/2)
            pickupNeckFillet2.isConstruction = True
            pickupNeckFillet3 = sketch3.sketchCurves.sketchArcs.addFillet(pickupNeck1[2], pickupNeck1[2].endSketchPoint.geometry, pickupNeck1[3], pickupNeck1[3].startSketchPoint.geometry, singleCoilWidth/2)
            pickupNeckFillet3.isConstruction = True
            pickupNeckFillet4 = sketch3.sketchCurves.sketchArcs.addFillet(pickupNeck1[3], pickupNeck1[3].endSketchPoint.geometry, pickupNeck1[0], pickupNeck1[0].startSketchPoint.geometry, singleCoilWidth/2)
            pickupNeckFillet4.isConstruction = True
            cavityNeck1 = cavityNeckLines.addCenterPointRectangle(adsk.core.Point3D.create((neckDistance-singleCoilWidth/2), 0, 0), adsk.core.Point3D.create((neckDistance-singleCoilWidth/2)+singleCoilWidth/2, (pickupCavityMountLength/2), 0))
            cavityNeck1[0].isConstruction = True
            cavityNeck1[1].isConstruction = True
            cavityNeck1[2].isConstruction = True
            cavityNeck1[3].isConstruction = True
            cavityNeckFillet1 = sketch3.sketchCurves.sketchArcs.addFillet(cavityNeck1[0], cavityNeck1[0].endSketchPoint.geometry, cavityNeck1[1], cavityNeck1[1].startSketchPoint.geometry, singleCoilWidth/2)
            cavityNeckFillet1.isConstruction = True
            cavityNeckFillet2 = sketch3.sketchCurves.sketchArcs.addFillet(cavityNeck1[1], cavityNeck1[1].endSketchPoint.geometry, cavityNeck1[2], cavityNeck1[2].startSketchPoint.geometry, singleCoilWidth/2)
            cavityNeckFillet2.isConstruction = True
            cavityNeckFillet3 = sketch3.sketchCurves.sketchArcs.addFillet(cavityNeck1[2], cavityNeck1[2].endSketchPoint.geometry, cavityNeck1[3], cavityNeck1[3].startSketchPoint.geometry, singleCoilWidth/2)
            cavityNeckFillet3.isConstruction = True
            cavityNeckFillet4 = sketch3.sketchCurves.sketchArcs.addFillet(cavityNeck1[3], cavityNeck1[3].endSketchPoint.geometry, cavityNeck1[0], cavityNeck1[0].startSketchPoint.geometry, singleCoilWidth/2)
            cavityNeckFillet4.isConstruction = True
        elif pickupNeck == "Humbucker":
            pickupNeck1 = neckLines.addCenterPointRectangle(adsk.core.Point3D.create((neckDistance-humbuckerWidth/2), 0, 0), adsk.core.Point3D.create((neckDistance-humbuckerWidth/2)+humbuckerWidth/2, (humbuckerLength/2), 0))
            pickupNeck1[0].isConstruction = True
            pickupNeck1[1].isConstruction = True
            pickupNeck1[2].isConstruction = True
            pickupNeck1[3].isConstruction = True
            pickupNeck2 = neckLines.addByTwoPoints(adsk.core.Point3D.create((neckDistance-humbuckerWidth/2), (-pickupCavityMountLength/2), 0), adsk.core.Point3D.create((neckDistance-humbuckerWidth/2), (pickupCavityMountLength/2), 0))
            pickupNeck2.isConstruction = True
            pickupNeckFillet1 = sketch3.sketchCurves.sketchArcs.addFillet(pickupNeck1[0], pickupNeck1[0].endSketchPoint.geometry, pickupNeck1[1], pickupNeck1[1].startSketchPoint.geometry, humbuckerFillet)
            pickupNeckFillet1.isConstruction = True
            pickupNeckFillet2 = sketch3.sketchCurves.sketchArcs.addFillet(pickupNeck1[1], pickupNeck1[1].endSketchPoint.geometry, pickupNeck1[2], pickupNeck1[2].startSketchPoint.geometry, humbuckerFillet)
            pickupNeckFillet2.isConstruction = True
            pickupNeckFillet3 = sketch3.sketchCurves.sketchArcs.addFillet(pickupNeck1[2], pickupNeck1[2].endSketchPoint.geometry, pickupNeck1[3], pickupNeck1[3].startSketchPoint.geometry, humbuckerFillet)
            pickupNeckFillet3.isConstruction = True
            pickupNeckFillet4 = sketch3.sketchCurves.sketchArcs.addFillet(pickupNeck1[3], pickupNeck1[3].endSketchPoint.geometry, pickupNeck1[0], pickupNeck1[0].startSketchPoint.geometry, humbuckerFillet)
            pickupNeckFillet4.isConstruction = True
            cavityNeck1 = cavityNeckLines.addCenterPointRectangle(adsk.core.Point3D.create((neckDistance-humbuckerWidth/2), 0, 0), adsk.core.Point3D.create((neckDistance-humbuckerWidth/2)-pickupCavityMountTabWidth/2, (pickupCavityMountLength/2), 0))
            cavityNeck1[0].isConstruction = True
            cavityNeck1[1].isConstruction = True
            cavityNeck1[2].isConstruction = True
            cavityNeck1[3].isConstruction = True
            cavityNeckFillet1 = sketch3.sketchCurves.sketchArcs.addFillet(cavityNeck1[0], cavityNeck1[0].endSketchPoint.geometry, cavityNeck1[1], cavityNeck1[1].startSketchPoint.geometry, humbuckerFillet/2)
            cavityNeckFillet1.isConstruction = True
            cavityNeckFillet2 = sketch3.sketchCurves.sketchArcs.addFillet(cavityNeck1[1], cavityNeck1[1].endSketchPoint.geometry, cavityNeck1[2], cavityNeck1[2].startSketchPoint.geometry, humbuckerFillet/2)
            cavityNeckFillet2.isConstruction = True
            cavityNeckFillet3 = sketch3.sketchCurves.sketchArcs.addFillet(cavityNeck1[2], cavityNeck1[2].endSketchPoint.geometry, cavityNeck1[3], cavityNeck1[3].startSketchPoint.geometry, humbuckerFillet/2)
            cavityNeckFillet3.isConstruction = True
            cavityNeckFillet4 = sketch3.sketchCurves.sketchArcs.addFillet(cavityNeck1[3], cavityNeck1[3].endSketchPoint.geometry, cavityNeck1[0], cavityNeck1[0].startSketchPoint.geometry, humbuckerFillet/2)
            cavityNeckFillet4.isConstruction = True
        else:
            pass

        middleLines = sketch3.sketchCurves.sketchLines
        cavitymiddleLines = sketch3.sketchCurves.sketchLines

        if pickupMiddle == "Single-Coil":
            # Create sketch lines
            pickupMiddle1 = middleLines.addCenterPointRectangle(adsk.core.Point3D.create((middleDistance), 0, 0), adsk.core.Point3D.create((middleDistance+singleCoilWidth/2), (singleCoilLength/2), 0))
            pickupMiddle1[0].isConstruction = True
            pickupMiddle1[1].isConstruction = True
            pickupMiddle1[2].isConstruction = True
            pickupMiddle1[3].isConstruction = True
            pickupMiddle2 = middleLines.addByTwoPoints(adsk.core.Point3D.create((middleDistance), (-pickupCavityMountLength/2), 0), adsk.core.Point3D.create((middleDistance), (pickupCavityMountLength/2), 0))
            pickupMiddle2.isConstruction = True
            pickupMiddleFillet1 = sketch3.sketchCurves.sketchArcs.addFillet(pickupMiddle1[0], pickupMiddle1[0].endSketchPoint.geometry, pickupMiddle1[1], pickupMiddle1[1].startSketchPoint.geometry, singleCoilWidth/2)
            pickupMiddleFillet1.isConstruction = True
            pickupMiddleFillet2 = sketch3.sketchCurves.sketchArcs.addFillet(pickupMiddle1[1], pickupMiddle1[1].endSketchPoint.geometry, pickupMiddle1[2], pickupMiddle1[2].startSketchPoint.geometry, singleCoilWidth/2)
            pickupMiddleFillet2.isConstruction = True
            pickupMiddleFillet3 = sketch3.sketchCurves.sketchArcs.addFillet(pickupMiddle1[2], pickupMiddle1[2].endSketchPoint.geometry, pickupMiddle1[3], pickupMiddle1[3].startSketchPoint.geometry, singleCoilWidth/2)
            pickupMiddleFillet3.isConstruction = True
            pickupMiddleFillet4 = sketch3.sketchCurves.sketchArcs.addFillet(pickupMiddle1[3], pickupMiddle1[3].endSketchPoint.geometry, pickupMiddle1[0], pickupMiddle1[0].startSketchPoint.geometry, singleCoilWidth/2)
            pickupMiddleFillet4.isConstruction = True
            cavityMiddle1 = cavitymiddleLines.addCenterPointRectangle(adsk.core.Point3D.create((middleDistance), 0, 0), adsk.core.Point3D.create((middleDistance+singleCoilWidth/2), (pickupCavityMountLength/2), 0))
            cavityMiddle1[0].isConstruction = True
            cavityMiddle1[1].isConstruction = True
            cavityMiddle1[2].isConstruction = True
            cavityMiddle1[3].isConstruction = True
            cavityMiddleFillet1 = sketch3.sketchCurves.sketchArcs.addFillet(cavityMiddle1[0], cavityMiddle1[0].endSketchPoint.geometry, cavityMiddle1[1], cavityMiddle1[1].startSketchPoint.geometry, singleCoilWidth/2)
            cavityMiddleFillet1.isConstruction = True
            cavityMiddleFillet2 = sketch3.sketchCurves.sketchArcs.addFillet(cavityMiddle1[1], cavityMiddle1[1].endSketchPoint.geometry, cavityMiddle1[2], cavityMiddle1[2].startSketchPoint.geometry, singleCoilWidth/2)
            cavityMiddleFillet2.isConstruction = True
            cavityMiddleFillet3 = sketch3.sketchCurves.sketchArcs.addFillet(cavityMiddle1[2], cavityMiddle1[2].endSketchPoint.geometry, cavityMiddle1[3], cavityMiddle1[3].startSketchPoint.geometry, singleCoilWidth/2)
            cavityMiddleFillet3.isConstruction = True
            cavityMiddleFillet4 = sketch3.sketchCurves.sketchArcs.addFillet(cavityMiddle1[3], cavityMiddle1[3].endSketchPoint.geometry, cavityMiddle1[0], cavityMiddle1[0].startSketchPoint.geometry, singleCoilWidth/2)
            cavityMiddleFillet4.isConstruction = True
        elif pickupMiddle == "Humbucker":
            # Create sketch lines
            pickupMiddle1 = middleLines.addCenterPointRectangle(adsk.core.Point3D.create((middleDistance), 0, 0), adsk.core.Point3D.create((middleDistance+humbuckerWidth/2), (humbuckerLength/2), 0))
            pickupMiddle1[0].isConstruction = True
            pickupMiddle1[1].isConstruction = True
            pickupMiddle1[2].isConstruction = True
            pickupMiddle1[3].isConstruction = True
            pickupMiddle2 = middleLines.addByTwoPoints(adsk.core.Point3D.create((middleDistance), (-pickupCavityMountLength/2), 0), adsk.core.Point3D.create((middleDistance), (pickupCavityMountLength/2), 0))
            pickupMiddle2.isConstruction = True
            pickupMiddleFillet1 = sketch3.sketchCurves.sketchArcs.addFillet(pickupMiddle1[0], pickupMiddle1[0].endSketchPoint.geometry, pickupMiddle1[1], pickupMiddle1[1].startSketchPoint.geometry, humbuckerFillet)
            pickupMiddleFillet1.isConstruction = True
            pickupMiddleFillet2 = sketch3.sketchCurves.sketchArcs.addFillet(pickupMiddle1[1], pickupMiddle1[1].endSketchPoint.geometry, pickupMiddle1[2], pickupMiddle1[2].startSketchPoint.geometry, humbuckerFillet)
            pickupMiddleFillet2.isConstruction = True
            pickupMiddleFillet3 = sketch3.sketchCurves.sketchArcs.addFillet(pickupMiddle1[2], pickupMiddle1[2].endSketchPoint.geometry, pickupMiddle1[3], pickupMiddle1[3].startSketchPoint.geometry, humbuckerFillet)
            pickupMiddleFillet3.isConstruction = True
            pickupMiddleFillet4 = sketch3.sketchCurves.sketchArcs.addFillet(pickupMiddle1[3], pickupMiddle1[3].endSketchPoint.geometry, pickupMiddle1[0], pickupMiddle1[0].startSketchPoint.geometry, humbuckerFillet)
            pickupMiddleFillet4.isConstruction = True
            cavityMiddle1 = cavitymiddleLines.addCenterPointRectangle(adsk.core.Point3D.create((middleDistance), 0, 0), adsk.core.Point3D.create((middleDistance+pickupCavityMountTabWidth/2), (pickupCavityMountLength/2), 0))
            cavityMiddle1[0].isConstruction = True
            cavityMiddle1[1].isConstruction = True
            cavityMiddle1[2].isConstruction = True
            cavityMiddle1[3].isConstruction = True
            cavityMiddleFillet1 = sketch3.sketchCurves.sketchArcs.addFillet(cavityMiddle1[0], cavityMiddle1[0].endSketchPoint.geometry, cavityMiddle1[1], cavityMiddle1[1].startSketchPoint.geometry, humbuckerFillet/2)
            cavityMiddleFillet1.isConstruction = True
            cavityMiddleFillet2 = sketch3.sketchCurves.sketchArcs.addFillet(cavityMiddle1[1], cavityMiddle1[1].endSketchPoint.geometry, cavityMiddle1[2], cavityMiddle1[2].startSketchPoint.geometry, humbuckerFillet/2)
            cavityMiddleFillet2.isConstruction = True
            cavityMiddleFillet3 = sketch3.sketchCurves.sketchArcs.addFillet(cavityMiddle1[2], cavityMiddle1[2].endSketchPoint.geometry, cavityMiddle1[3], cavityMiddle1[3].startSketchPoint.geometry, humbuckerFillet/2)
            cavityMiddleFillet3.isConstruction = True
            cavityMiddleFillet4 = sketch3.sketchCurves.sketchArcs.addFillet(cavityMiddle1[3], cavityMiddle1[3].endSketchPoint.geometry, cavityMiddle1[0], cavityMiddle1[0].startSketchPoint.geometry, humbuckerFillet/2)
            cavityMiddleFillet4.isConstruction = True
        else:
            pass

        bridgeLines = sketch3.sketchCurves.sketchLines
        cavitybridgeLines = sketch3.sketchCurves.sketchLines
        sketchPoints = sketch3.sketchPoints

        # Create sketch point
        if pickupBridge == "Single-Coil":
            point1 = adsk.core.Point3D.create((bridgeDistance+singleCoilWidth/2), 0, 0)
        elif pickupBridge == "Humbucker":
            point1 = adsk.core.Point3D.create((bridgeDistance+humbuckerWidth/2), 0, 0)
        else:
            pass

        sketchPoint1 = sketchPoints.add(point1)
        sketchPoint1.isFixed = True

        if pickupBridge == "Single-Coil":
            # Create sketch lines
            pickupBridge1 = bridgeLines.addCenterPointRectangle(adsk.core.Point3D.create((bridgeDistance+singleCoilWidth/2), 0, 0), adsk.core.Point3D.create((bridgeDistance+singleCoilWidth/2)+singleCoilWidth/2, (singleCoilLength/2), 0))
            pickupBridge1[0].isConstruction = True
            pickupBridge1[1].isConstruction = True
            pickupBridge1[2].isConstruction = True
            pickupBridge1[3].isConstruction = True
            pickupBridge2 = bridgeLines.addByTwoPoints(adsk.core.Point3D.create((bridgeDistance+singleCoilWidth/2), (-pickupCavityMountLength/2), 0), adsk.core.Point3D.create((bridgeDistance+singleCoilWidth/2), (pickupCavityMountLength/2), 0))
            pickupBridge2.isConstruction = True
            pickupBridgeFillet1 = sketch3.sketchCurves.sketchArcs.addFillet(pickupBridge1[0], pickupBridge1[0].endSketchPoint.geometry, pickupBridge1[1], pickupBridge1[1].startSketchPoint.geometry, singleCoilWidth/2)
            pickupBridgeFillet1.isConstruction = True
            pickupBridgeFillet2 = sketch3.sketchCurves.sketchArcs.addFillet(pickupBridge1[1], pickupBridge1[1].endSketchPoint.geometry, pickupBridge1[2], pickupBridge1[2].startSketchPoint.geometry, singleCoilWidth/2)
            pickupBridgeFillet2.isConstruction = True
            pickupBridgeFillet3 = sketch3.sketchCurves.sketchArcs.addFillet(pickupBridge1[2], pickupBridge1[2].endSketchPoint.geometry, pickupBridge1[3], pickupBridge1[3].startSketchPoint.geometry, singleCoilWidth/2)
            pickupBridgeFillet3.isConstruction = True
            pickupBridgeFillet4 = sketch3.sketchCurves.sketchArcs.addFillet(pickupBridge1[3], pickupBridge1[3].endSketchPoint.geometry, pickupBridge1[0], pickupBridge1[0].startSketchPoint.geometry, singleCoilWidth/2)
            pickupBridgeFillet4.isConstruction = True
            cavityBridge1 = cavitybridgeLines.addCenterPointRectangle(adsk.core.Point3D.create((bridgeDistance+singleCoilWidth/2), 0, 0), adsk.core.Point3D.create((bridgeDistance+singleCoilWidth/2)+singleCoilWidth/2, (pickupCavityMountLength/2), 0))
            cavityBridge1[0].isConstruction = True
            cavityBridge1[1].isConstruction = True
            cavityBridge1[2].isConstruction = True
            cavityBridge1[3].isConstruction = True
            cavityBridgeFillet1 = sketch3.sketchCurves.sketchArcs.addFillet(cavityBridge1[0], cavityBridge1[0].endSketchPoint.geometry, cavityBridge1[1], cavityBridge1[1].startSketchPoint.geometry, singleCoilWidth/2)
            cavityBridgeFillet1.isConstruction = True
            cavityBridgeFillet2 = sketch3.sketchCurves.sketchArcs.addFillet(cavityBridge1[1], cavityBridge1[1].endSketchPoint.geometry, cavityBridge1[2], cavityBridge1[2].startSketchPoint.geometry, singleCoilWidth/2)
            cavityBridgeFillet2.isConstruction = True
            cavityBridgeFillet3 = sketch3.sketchCurves.sketchArcs.addFillet(cavityBridge1[2], cavityBridge1[2].endSketchPoint.geometry, cavityBridge1[3], cavityBridge1[3].startSketchPoint.geometry, singleCoilWidth/2)
            cavityBridgeFillet3.isConstruction = True
            cavityBridgeFillet4 = sketch3.sketchCurves.sketchArcs.addFillet(cavityBridge1[3], cavityBridge1[3].endSketchPoint.geometry, cavityBridge1[0], cavityBridge1[0].startSketchPoint.geometry, singleCoilWidth/2)
            cavityBridgeFillet4.isConstruction = True
            pickupBridgeAngle = bridgeLines.addByTwoPoints(adsk.core.Point3D.create(bridgeDistance, 0, 0), adsk.core.Point3D.create((bridgeDistance+singleCoilWidth), 0, 0))
            pickupBridgeAngle.isConstruction = True
            # Constrain the Rectangle to stay rectangular
            constraints = sketch3.geometricConstraints
            constraints.addMidPoint(sketchPoint1, bridgeLines.item(22))
            constraints.addMidPoint(sketchPoint1, bridgeLines.item(27))
            constraints.addMidPoint(bridgeLines.item(27).startSketchPoint, bridgeLines.item(19))
            constraints.addMidPoint(bridgeLines.item(27).endSketchPoint, bridgeLines.item(21))
            constraints.addMidPoint(bridgeLines.item(27).startSketchPoint, cavitybridgeLines.item(24))
            constraints.addMidPoint(bridgeLines.item(27).endSketchPoint, cavitybridgeLines.item(26))
            constraints.addPerpendicular(bridgeLines.item(27), bridgeLines.item(22))
            # all = adsk.core.ObjectCollection.create()
            # for lines in range(bridgeLines[19:]):
            #     all.add(lines)
            all = adsk.core.ObjectCollection.create()
            all.add(bridgeLines.item(19))
            all.add(bridgeLines.item(20))
            all.add(bridgeLines.item(21))
            all.add(bridgeLines.item(22))
            all.add(bridgeLines.item(23))
            all.add(bridgeLines.item(24))
            all.add(bridgeLines.item(25))
            all.add(bridgeLines.item(26))
            all.add(bridgeLines.item(27))
            all.add(sketchPoint1)
            normal = sketch3.xDirection.crossProduct(sketch3.yDirection)
            normal.transformBy(sketch3.transform)
            origin = sketch3.origin
            origin.transformBy(sketch3.transform)
            matrix = adsk.core.Matrix3D.create()
            matrix.setToRotation(-bridgePickupAngle, normal, origin)
            sketch3.move(all, matrix)
        elif pickupBridge == "Humbucker":
            pickupBridge1 = bridgeLines.addCenterPointRectangle(adsk.core.Point3D.create((bridgeDistance+humbuckerWidth/2), 0, 0), adsk.core.Point3D.create((bridgeDistance), (humbuckerLength/2), 0))
            pickupBridge1[0].isConstruction = True
            pickupBridge1[1].isConstruction = True
            pickupBridge1[2].isConstruction = True
            pickupBridge1[3].isConstruction = True
            pickupBridge2 = bridgeLines.addByTwoPoints(adsk.core.Point3D.create((bridgeDistance+humbuckerWidth/2), (-pickupCavityMountLength/2), 0), adsk.core.Point3D.create((bridgeDistance+humbuckerWidth/2), (pickupCavityMountLength/2), 0))
            pickupBridge2.isConstruction = True
            pickupBridgeFillet1 = sketch3.sketchCurves.sketchArcs.addFillet(pickupBridge1[0], pickupBridge1[0].endSketchPoint.geometry, pickupBridge1[1], pickupBridge1[1].startSketchPoint.geometry, humbuckerFillet)
            pickupBridgeFillet1.isConstruction = True
            pickupBridgeFillet2 = sketch3.sketchCurves.sketchArcs.addFillet(pickupBridge1[1], pickupBridge1[1].endSketchPoint.geometry, pickupBridge1[2], pickupBridge1[2].startSketchPoint.geometry, humbuckerFillet)
            pickupBridgeFillet2.isConstruction = True
            pickupBridgeFillet3 = sketch3.sketchCurves.sketchArcs.addFillet(pickupBridge1[2], pickupBridge1[2].endSketchPoint.geometry, pickupBridge1[3], pickupBridge1[3].startSketchPoint.geometry, humbuckerFillet)
            pickupBridgeFillet3.isConstruction = True
            pickupBridgeFillet4 = sketch3.sketchCurves.sketchArcs.addFillet(pickupBridge1[3], pickupBridge1[3].endSketchPoint.geometry, pickupBridge1[0], pickupBridge1[0].startSketchPoint.geometry, humbuckerFillet)
            pickupBridgeFillet4.isConstruction = True
            cavityBridge1 = cavitybridgeLines.addCenterPointRectangle(adsk.core.Point3D.create((bridgeDistance+humbuckerWidth/2), 0, 0), adsk.core.Point3D.create((bridgeDistance+humbuckerWidth/2)-pickupCavityMountTabWidth/2, (pickupCavityMountLength/2), 0))
            cavityBridge1[0].isConstruction = True
            cavityBridge1[1].isConstruction = True
            cavityBridge1[2].isConstruction = True
            cavityBridge1[3].isConstruction = True
            cavityBridgeFillet1 = sketch3.sketchCurves.sketchArcs.addFillet(cavityBridge1[0], cavityBridge1[0].endSketchPoint.geometry, cavityBridge1[1], cavityBridge1[1].startSketchPoint.geometry, humbuckerFillet/2)
            cavityBridgeFillet1.isConstruction = True
            cavityBridgeFillet2 = sketch3.sketchCurves.sketchArcs.addFillet(cavityBridge1[1], cavityBridge1[1].endSketchPoint.geometry, cavityBridge1[2], cavityBridge1[2].startSketchPoint.geometry, humbuckerFillet/2)
            cavityBridgeFillet2.isConstruction = True
            cavityBridgeFillet3 = sketch3.sketchCurves.sketchArcs.addFillet(cavityBridge1[2], cavityBridge1[2].endSketchPoint.geometry, cavityBridge1[3], cavityBridge1[3].startSketchPoint.geometry, humbuckerFillet/2)
            cavityBridgeFillet3.isConstruction = True
            cavityBridgeFillet4 = sketch3.sketchCurves.sketchArcs.addFillet(cavityBridge1[3], cavityBridge1[3].endSketchPoint.geometry, cavityBridge1[0], cavityBridge1[0].startSketchPoint.geometry, humbuckerFillet/2)
            cavityBridgeFillet4.isConstruction = True
        else:
            pass
        if pickupNeck == "Single-Coil":
            pickupNeckDims1 = sketch3.sketchDimensions.addDistanceDimension(pickupNeck1[3].startSketchPoint, pickupNeck1[1].endSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create((neckDistance-singleCoilWidth/2), -6, 0), False)
            pickupNeckDims2 = sketch3.sketchDimensions.addDistanceDimension(cavityNeck1[3].startSketchPoint, cavityNeck1[1].endSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create((neckDistance-singleCoilWidth/2), -5, 0), False)
        elif pickupNeck == "Humbucker":
            pickupNeckDims1 = sketch3.sketchDimensions.addDistanceDimension(pickupNeck1[3].startSketchPoint, pickupNeck1[1].endSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create((neckDistance-humbuckerWidth/2), -6, 0), False)
            pickupNeckDims2 = sketch3.sketchDimensions.addDistanceDimension(cavityNeck1[3].startSketchPoint, cavityNeck1[1].endSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create((neckDistance-humbuckerWidth/2), -5, 0), False)
        else:
            pass
        if pickupMiddle == "Single-Coil":
            pickupMiddleDims1 = sketch3.sketchDimensions.addDistanceDimension(pickupMiddle1[3].startSketchPoint, pickupMiddle1[1].endSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create((middleDistance), -6, 0), False)
            pickupMiddleDims2 = sketch3.sketchDimensions.addDistanceDimension(cavityMiddle1[3].startSketchPoint, cavityMiddle1[1].endSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create((middleDistance), -5, 0), False)
        elif pickupMiddle == "Humbucker":
            pickupMiddleDims1 = sketch3.sketchDimensions.addDistanceDimension(pickupMiddle1[3].startSketchPoint, pickupMiddle1[1].endSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create((middleDistance), -6, 0), False)
            pickupMiddleDims2 = sketch3.sketchDimensions.addDistanceDimension(cavityMiddle1[3].startSketchPoint, cavityMiddle1[1].endSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create((middleDistance), -5, 0), False)
        else:
            pass
        if pickupBridge == "Single-Coil":
            pickupMiddleDims1 = sketch3.sketchDimensions.addDistanceDimension(pickupBridge1[3].startSketchPoint, pickupBridge1[1].endSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create((bridgeDistance+singleCoilWidth/2), -6, 0), False)
            pickupMiddleDims2 = sketch3.sketchDimensions.addDistanceDimension(cavityBridge1[3].startSketchPoint, cavityBridge1[1].endSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create((bridgeDistance+singleCoilWidth/2), -5, 0), False)
        elif pickupBridge == "Humbucker":
            pickupMiddleDims1 = sketch3.sketchDimensions.addDistanceDimension(pickupBridge1[3].startSketchPoint, sketchPoint1, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create((bridgeDistance+humbuckerWidth/2), -6, 0), False)
            pickupMiddleDims2 = sketch3.sketchDimensions.addDistanceDimension(cavityBridge1[3].startSketchPoint, sketchPoint1, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create((bridgeDistance+humbuckerWidth/2), -5, 0), False)
        else:
            pass
        if pickupMiddle == "None":
            pickupGapDims1 = sketch3.sketchDimensions.addDistanceDimension(pickupNeck2.endSketchPoint, sketchPoint1, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create(bridgeDistance + (neckDistance - bridgeDistance)/2, 7, 0), False)
        else:
            pickupGapDims1 = sketch3.sketchDimensions.addDistanceDimension(pickupNeck2.endSketchPoint, sketchPoint1, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create(bridgeDistance + (neckDistance - bridgeDistance)/2, 7, 0), False)
            pickupGapDims2 = sketch3.sketchDimensions.addDistanceDimension(pickupNeck2.endSketchPoint, pickupMiddle2.endSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create(middleDistance + (neckDistance - middleDistance)/2, 6, 0), False)
            pickupGapDims2 = sketch3.sketchDimensions.addDistanceDimension(pickupMiddle2.endSketchPoint, sketchPoint1, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create(bridgeDistance + (middleDistance - bridgeDistance)/2, 6, 0), False)
        pickupDims1 = sketch3.sketchDimensions.addDistanceDimension(pickupBridge1[0].startSketchPoint, pickupBridge1[2].endSketchPoint, adsk.fusion.DimensionOrientations.VerticalDimensionOrientation, adsk.core.Point3D.create(bridgeDistance - 4, 0, 0), False)
        pickupDims2 = sketch3.sketchDimensions.addDistanceDimension(pickupBridge2.endSketchPoint, pickupBridge2.startSketchPoint, adsk.fusion.DimensionOrientations.VerticalDimensionOrientation, adsk.core.Point3D.create(bridgeDistance - 5, 0, 0), False)
        
        #Centers the camera to fit the entire fretboard
        cam = self.app.activeViewport.camera
        cam.isFitView = True
        cam.isSmoothTransition = True
        cam.viewOrientation = adsk.core.ViewOrientations.TopViewOrientation
        self.app.activeViewport.camera = cam

        # Group everything used to create the fretboard in the timeline.
        timelineGroups2 = self.design.timeline.timelineGroups
        newOccIndex2 = newOcc2.timelineObject.index
        endIndex2 = sketch3.timelineObject.index
        timelineGroup2 = timelineGroups2.add(newOccIndex2, endIndex2)
        timelineGroup2.name = 'Dimensions'
        dimsComp.name = 'Dimensions'

        return dimsComp