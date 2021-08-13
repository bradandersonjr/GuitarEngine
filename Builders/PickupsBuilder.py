import os, sys
import adsk.core, adsk.fusion, adsk.cam, traceback, math
from math import sqrt
from ..ParameterValues import ParameterValues

class PickupsBuilder:

    def __init__(self, app):
        self.app = app
        self.design = app.activeProduct

    def buildPickups(self, parameters: ParameterValues):

        rootComp = self.design.rootComponent
        pickupsOccs = rootComp.occurrences
        pickupsOcc = pickupsOccs.addNewComponent(adsk.core.Matrix3D.create())
        pickupsComp = adsk.fusion.Component.cast(pickupsOcc.component)

        guitarLength = parameters.guitarLength
        headstockLength = parameters.headstockLength
        scaleLength = parameters.scaleLength
        fretboardLength = parameters.fretboardLength + parameters.fretboardLengthOffset
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

        # Create a new sketch.
        sketches = pickupsComp.sketches
        xzPlane = pickupsComp.xYConstructionPlane
        neckDistance = guitarLength - headstockLength - fretboardLength - neckSpacing
        bridgeDistance = guitarLength - headstockLength - scaleLength + bridgeSpacing
        middleDistance = bridgeDistance + (neckDistance - bridgeDistance)/2

        if pickupNeck == "None":
            neckPickupType = ''
        else:
            #Create sketch for bridge spacing
            sketch1 = sketches.add(xzPlane)
            neckLines = sketch1.sketchCurves.sketchLines
            cavityNeckLines = sketch1.sketchCurves.sketchLines

            # Get sketch points
            sketchPoints = sketch1.sketchPoints
            sketch1.isComputeDeferred = True
            sketch1.areConstraintsShown = False
            sketch1.arePointsShown = False

            if pickupNeck == "Single-Coil":
                # Create sketch lines
                pickupNeck1 = neckLines.addCenterPointRectangle(adsk.core.Point3D.create((neckDistance-singleCoilWidth/2), 0, 0), adsk.core.Point3D.create((neckDistance-singleCoilWidth/2)+singleCoilWidth/2, (singleCoilLength/2), 0))
                pickupNeck2 = neckLines.addByTwoPoints(adsk.core.Point3D.create((neckDistance-singleCoilWidth/2), (-pickupCavityMountLength/2), 0), adsk.core.Point3D.create((neckDistance-singleCoilWidth/2), (pickupCavityMountLength/2), 0))
                pickupNeck2.isConstruction = True
                pickupNeckFillet1 = sketch1.sketchCurves.sketchArcs.addFillet(pickupNeck1[0], pickupNeck1[0].endSketchPoint.geometry, pickupNeck1[1], pickupNeck1[1].startSketchPoint.geometry, singleCoilWidth/2)
                pickupNeckFillet2 = sketch1.sketchCurves.sketchArcs.addFillet(pickupNeck1[1], pickupNeck1[1].endSketchPoint.geometry, pickupNeck1[2], pickupNeck1[2].startSketchPoint.geometry, singleCoilWidth/2)
                pickupNeckFillet3 = sketch1.sketchCurves.sketchArcs.addFillet(pickupNeck1[2], pickupNeck1[2].endSketchPoint.geometry, pickupNeck1[3], pickupNeck1[3].startSketchPoint.geometry, singleCoilWidth/2)
                pickupNeckFillet4 = sketch1.sketchCurves.sketchArcs.addFillet(pickupNeck1[3], pickupNeck1[3].endSketchPoint.geometry, pickupNeck1[0], pickupNeck1[0].startSketchPoint.geometry, singleCoilWidth/2)
                cavityNeck1 = cavityNeckLines.addCenterPointRectangle(adsk.core.Point3D.create((neckDistance-singleCoilWidth/2), 0, 0), adsk.core.Point3D.create((neckDistance-singleCoilWidth/2)+singleCoilWidth/2, (pickupCavityMountLength/2), 0))
                cavityNeckFillet1 = sketch1.sketchCurves.sketchArcs.addFillet(cavityNeck1[0], cavityNeck1[0].endSketchPoint.geometry, cavityNeck1[1], cavityNeck1[1].startSketchPoint.geometry, singleCoilWidth/2)
                cavityNeckFillet2 = sketch1.sketchCurves.sketchArcs.addFillet(cavityNeck1[1], cavityNeck1[1].endSketchPoint.geometry, cavityNeck1[2], cavityNeck1[2].startSketchPoint.geometry, singleCoilWidth/2)
                cavityNeckFillet3 = sketch1.sketchCurves.sketchArcs.addFillet(cavityNeck1[2], cavityNeck1[2].endSketchPoint.geometry, cavityNeck1[3], cavityNeck1[3].startSketchPoint.geometry, singleCoilWidth/2)
                cavityNeckFillet4 = sketch1.sketchCurves.sketchArcs.addFillet(cavityNeck1[3], cavityNeck1[3].endSketchPoint.geometry, cavityNeck1[0], cavityNeck1[0].startSketchPoint.geometry, singleCoilWidth/2)
                sketch1.name = 'Neck Pickup [Single-Coil]'
                neckPickupType = 'S'
            elif pickupNeck == "Humbucker":
                pickupNeck1 = neckLines.addCenterPointRectangle(adsk.core.Point3D.create((neckDistance-humbuckerWidth/2), 0, 0), adsk.core.Point3D.create((neckDistance-humbuckerWidth/2)+humbuckerWidth/2, (humbuckerLength/2), 0))
                pickupNeck2 = neckLines.addByTwoPoints(adsk.core.Point3D.create((neckDistance-humbuckerWidth/2), (-pickupCavityMountLength/2), 0), adsk.core.Point3D.create((neckDistance-humbuckerWidth/2), (pickupCavityMountLength/2), 0))
                pickupNeck2.isConstruction = True
                pickupNeckFillet1 = sketch1.sketchCurves.sketchArcs.addFillet(pickupNeck1[0], pickupNeck1[0].endSketchPoint.geometry, pickupNeck1[1], pickupNeck1[1].startSketchPoint.geometry, humbuckerFillet)
                pickupNeckFillet2 = sketch1.sketchCurves.sketchArcs.addFillet(pickupNeck1[1], pickupNeck1[1].endSketchPoint.geometry, pickupNeck1[2], pickupNeck1[2].startSketchPoint.geometry, humbuckerFillet)
                pickupNeckFillet3 = sketch1.sketchCurves.sketchArcs.addFillet(pickupNeck1[2], pickupNeck1[2].endSketchPoint.geometry, pickupNeck1[3], pickupNeck1[3].startSketchPoint.geometry, humbuckerFillet)
                pickupNeckFillet4 = sketch1.sketchCurves.sketchArcs.addFillet(pickupNeck1[3], pickupNeck1[3].endSketchPoint.geometry, pickupNeck1[0], pickupNeck1[0].startSketchPoint.geometry, humbuckerFillet)
                cavityNeck1 = cavityNeckLines.addCenterPointRectangle(adsk.core.Point3D.create((neckDistance-humbuckerWidth/2), 0, 0), adsk.core.Point3D.create((neckDistance-humbuckerWidth/2)-pickupCavityMountTabWidth/2, (pickupCavityMountLength/2), 0))
                cavityNeckFillet1 = sketch1.sketchCurves.sketchArcs.addFillet(cavityNeck1[0], cavityNeck1[0].endSketchPoint.geometry, cavityNeck1[1], cavityNeck1[1].startSketchPoint.geometry, humbuckerFillet/2)
                cavityNeckFillet2 = sketch1.sketchCurves.sketchArcs.addFillet(cavityNeck1[1], cavityNeck1[1].endSketchPoint.geometry, cavityNeck1[2], cavityNeck1[2].startSketchPoint.geometry, humbuckerFillet/2)
                cavityNeckFillet3 = sketch1.sketchCurves.sketchArcs.addFillet(cavityNeck1[2], cavityNeck1[2].endSketchPoint.geometry, cavityNeck1[3], cavityNeck1[3].startSketchPoint.geometry, humbuckerFillet/2)
                cavityNeckFillet4 = sketch1.sketchCurves.sketchArcs.addFillet(cavityNeck1[3], cavityNeck1[3].endSketchPoint.geometry, cavityNeck1[0], cavityNeck1[0].startSketchPoint.geometry, humbuckerFillet/2)
                sketch1.name = 'Neck Pickup [Humbucker]'
                neckPickupType = 'H'
            else:
                pass

        if pickupMiddle == "None":
            middlePickupType = ''
        else:
            #Create sketch for bridge spacing
            sketch2 = sketches.add(xzPlane)
            middleLines = sketch2.sketchCurves.sketchLines
            cavitymiddleLines = sketch2.sketchCurves.sketchLines

            # Get sketch points
            sketchPoints = sketch2.sketchPoints
            sketch2.isComputeDeferred = True
            sketch2.areConstraintsShown = False
            sketch2.arePointsShown = False

            if pickupMiddle == "Single-Coil":
                # Create sketch lines
                pickupMiddle1 = middleLines.addCenterPointRectangle(adsk.core.Point3D.create((middleDistance), 0, 0), adsk.core.Point3D.create((middleDistance+singleCoilWidth/2), (singleCoilLength/2), 0))
                pickupMiddle2 = middleLines.addByTwoPoints(adsk.core.Point3D.create((middleDistance), (-pickupCavityMountLength/2), 0), adsk.core.Point3D.create((middleDistance), (pickupCavityMountLength/2), 0))
                pickupMiddle2.isConstruction = True
                pickupMiddleFillet1 = sketch2.sketchCurves.sketchArcs.addFillet(pickupMiddle1[0], pickupMiddle1[0].endSketchPoint.geometry, pickupMiddle1[1], pickupMiddle1[1].startSketchPoint.geometry, singleCoilWidth/2)
                pickupMiddleFillet2 = sketch2.sketchCurves.sketchArcs.addFillet(pickupMiddle1[1], pickupMiddle1[1].endSketchPoint.geometry, pickupMiddle1[2], pickupMiddle1[2].startSketchPoint.geometry, singleCoilWidth/2)
                pickupMiddleFillet3 = sketch2.sketchCurves.sketchArcs.addFillet(pickupMiddle1[2], pickupMiddle1[2].endSketchPoint.geometry, pickupMiddle1[3], pickupMiddle1[3].startSketchPoint.geometry, singleCoilWidth/2)
                pickupMiddleFillet4 = sketch2.sketchCurves.sketchArcs.addFillet(pickupMiddle1[3], pickupMiddle1[3].endSketchPoint.geometry, pickupMiddle1[0], pickupMiddle1[0].startSketchPoint.geometry, singleCoilWidth/2)
                cavityMiddle1 = cavitymiddleLines.addCenterPointRectangle(adsk.core.Point3D.create((middleDistance), 0, 0), adsk.core.Point3D.create((middleDistance+singleCoilWidth/2), (pickupCavityMountLength/2), 0))
                cavityMiddleFillet1 = sketch2.sketchCurves.sketchArcs.addFillet(cavityMiddle1[0], cavityMiddle1[0].endSketchPoint.geometry, cavityMiddle1[1], cavityMiddle1[1].startSketchPoint.geometry, singleCoilWidth/2)
                cavityMiddleFillet2 = sketch2.sketchCurves.sketchArcs.addFillet(cavityMiddle1[1], cavityMiddle1[1].endSketchPoint.geometry, cavityMiddle1[2], cavityMiddle1[2].startSketchPoint.geometry, singleCoilWidth/2)
                cavityMiddleFillet3 = sketch2.sketchCurves.sketchArcs.addFillet(cavityMiddle1[2], cavityMiddle1[2].endSketchPoint.geometry, cavityMiddle1[3], cavityMiddle1[3].startSketchPoint.geometry, singleCoilWidth/2)
                cavityMiddleFillet4 = sketch2.sketchCurves.sketchArcs.addFillet(cavityMiddle1[3], cavityMiddle1[3].endSketchPoint.geometry, cavityMiddle1[0], cavityMiddle1[0].startSketchPoint.geometry, singleCoilWidth/2)
                sketch2.name = 'Middle Pickup [Single-Coil]'
                middlePickupType = 'S'
            elif pickupMiddle == "Humbucker":
                # Create sketch lines
                pickupMiddle1 = middleLines.addCenterPointRectangle(adsk.core.Point3D.create((middleDistance), 0, 0), adsk.core.Point3D.create((middleDistance+humbuckerWidth/2), (humbuckerLength/2), 0))
                pickupMiddle2 = middleLines.addByTwoPoints(adsk.core.Point3D.create((middleDistance), (-pickupCavityMountLength/2), 0), adsk.core.Point3D.create((middleDistance), (pickupCavityMountLength/2), 0))
                pickupMiddle2.isConstruction = True
                pickupMiddleFillet1 = sketch2.sketchCurves.sketchArcs.addFillet(pickupMiddle1[0], pickupMiddle1[0].endSketchPoint.geometry, pickupMiddle1[1], pickupMiddle1[1].startSketchPoint.geometry, humbuckerFillet)
                pickupMiddleFillet2 = sketch2.sketchCurves.sketchArcs.addFillet(pickupMiddle1[1], pickupMiddle1[1].endSketchPoint.geometry, pickupMiddle1[2], pickupMiddle1[2].startSketchPoint.geometry, humbuckerFillet)
                pickupMiddleFillet3 = sketch2.sketchCurves.sketchArcs.addFillet(pickupMiddle1[2], pickupMiddle1[2].endSketchPoint.geometry, pickupMiddle1[3], pickupMiddle1[3].startSketchPoint.geometry, humbuckerFillet)
                pickupMiddleFillet4 = sketch2.sketchCurves.sketchArcs.addFillet(pickupMiddle1[3], pickupMiddle1[3].endSketchPoint.geometry, pickupMiddle1[0], pickupMiddle1[0].startSketchPoint.geometry, humbuckerFillet)
                cavityMiddle1 = cavitymiddleLines.addCenterPointRectangle(adsk.core.Point3D.create((middleDistance), 0, 0), adsk.core.Point3D.create((middleDistance+pickupCavityMountTabWidth/2), (pickupCavityMountLength/2), 0))
                cavityMiddleFillet1 = sketch2.sketchCurves.sketchArcs.addFillet(cavityMiddle1[0], cavityMiddle1[0].endSketchPoint.geometry, cavityMiddle1[1], cavityMiddle1[1].startSketchPoint.geometry, humbuckerFillet/2)
                cavityMiddleFillet2 = sketch2.sketchCurves.sketchArcs.addFillet(cavityMiddle1[1], cavityMiddle1[1].endSketchPoint.geometry, cavityMiddle1[2], cavityMiddle1[2].startSketchPoint.geometry, humbuckerFillet/2)
                cavityMiddleFillet3 = sketch2.sketchCurves.sketchArcs.addFillet(cavityMiddle1[2], cavityMiddle1[2].endSketchPoint.geometry, cavityMiddle1[3], cavityMiddle1[3].startSketchPoint.geometry, humbuckerFillet/2)
                cavityMiddleFillet4 = sketch2.sketchCurves.sketchArcs.addFillet(cavityMiddle1[3], cavityMiddle1[3].endSketchPoint.geometry, cavityMiddle1[0], cavityMiddle1[0].startSketchPoint.geometry, humbuckerFillet/2)
                sketch2.name = 'Middle Pickup [Humbucker]'
                middlePickupType = 'H'
            else:
                pass

        #Create sketch for bridge spacing
        sketch3 = sketches.add(xzPlane)
        bridgeLines = sketch3.sketchCurves.sketchLines
        cavitybridgeLines = sketch3.sketchCurves.sketchLines

        # Get sketch points
        sketchPoints = sketch3.sketchPoints
        if parameters.generateBlanks:
            sketch3.isComputeDeferred = False
        else:
            sketch3.isComputeDeferred = True

        sketch3.areConstraintsShown = True
        sketch3.arePointsShown = False

        if pickupBridge == "Single-Coil":
            # Create sketch lines
            pickupBridge1 = bridgeLines.addCenterPointRectangle(adsk.core.Point3D.create((bridgeDistance+singleCoilWidth/2), 0, 0), adsk.core.Point3D.create((bridgeDistance+singleCoilWidth/2)+singleCoilWidth/2, (singleCoilLength/2), 0))
            pickupBridge2 = bridgeLines.addByTwoPoints(adsk.core.Point3D.create((bridgeDistance+singleCoilWidth/2), (-pickupCavityMountLength/2), 0), adsk.core.Point3D.create((bridgeDistance+singleCoilWidth/2), (pickupCavityMountLength/2), 0))
            pickupBridge2.isConstruction = True
            pickupBridgeAngle = bridgeLines.addByTwoPoints(adsk.core.Point3D.create(bridgeDistance, 0, 0), adsk.core.Point3D.create((bridgeDistance+singleCoilWidth), 0, 0))
            pickupBridgeAngle.isConstruction = True
            # Create sketch point
            point1 = adsk.core.Point3D.create((bridgeDistance+singleCoilWidth/2), 0, 0)
            sketchPoint1 = sketchPoints.add(point1)
            sketchPoint1.isFixed = True
            pickupBridgeFillet1 = sketch3.sketchCurves.sketchArcs.addFillet(pickupBridge1[0], pickupBridge1[0].endSketchPoint.geometry, pickupBridge1[1], pickupBridge1[1].startSketchPoint.geometry, singleCoilWidth/2)
            pickupBridgeFillet2 = sketch3.sketchCurves.sketchArcs.addFillet(pickupBridge1[1], pickupBridge1[1].endSketchPoint.geometry, pickupBridge1[2], pickupBridge1[2].startSketchPoint.geometry, singleCoilWidth/2)
            pickupBridgeFillet3 = sketch3.sketchCurves.sketchArcs.addFillet(pickupBridge1[2], pickupBridge1[2].endSketchPoint.geometry, pickupBridge1[3], pickupBridge1[3].startSketchPoint.geometry, singleCoilWidth/2)
            pickupBridgeFillet4 = sketch3.sketchCurves.sketchArcs.addFillet(pickupBridge1[3], pickupBridge1[3].endSketchPoint.geometry, pickupBridge1[0], pickupBridge1[0].startSketchPoint.geometry, singleCoilWidth/2)
            cavityBridge1 = cavitybridgeLines.addCenterPointRectangle(adsk.core.Point3D.create((bridgeDistance+singleCoilWidth/2), 0, 0), adsk.core.Point3D.create((bridgeDistance+singleCoilWidth/2)+singleCoilWidth/2, (pickupCavityMountLength/2), 0))
            cavityBridgeFillet1 = sketch3.sketchCurves.sketchArcs.addFillet(cavityBridge1[0], cavityBridge1[0].endSketchPoint.geometry, cavityBridge1[1], cavityBridge1[1].startSketchPoint.geometry, singleCoilWidth/2)
            cavityBridgeFillet2 = sketch3.sketchCurves.sketchArcs.addFillet(cavityBridge1[1], cavityBridge1[1].endSketchPoint.geometry, cavityBridge1[2], cavityBridge1[2].startSketchPoint.geometry, singleCoilWidth/2)
            cavityBridgeFillet3 = sketch3.sketchCurves.sketchArcs.addFillet(cavityBridge1[2], cavityBridge1[2].endSketchPoint.geometry, cavityBridge1[3], cavityBridge1[3].startSketchPoint.geometry, singleCoilWidth/2)
            cavityBridgeFillet4 = sketch3.sketchCurves.sketchArcs.addFillet(cavityBridge1[3], cavityBridge1[3].endSketchPoint.geometry, cavityBridge1[0], cavityBridge1[0].startSketchPoint.geometry, singleCoilWidth/2)
            # Constrain the Rectangle to stay rectangular
            constraints = sketch3.geometricConstraints
            constraints.addMidPoint(sketchPoint1, bridgeLines.item(4))
            constraints.addMidPoint(sketchPoint1, bridgeLines.item(5))
            constraints.addMidPoint(bridgeLines.item(5).startSketchPoint, bridgeLines.item(3))
            constraints.addMidPoint(bridgeLines.item(5).endSketchPoint, bridgeLines.item(1))
            constraints.addMidPoint(bridgeLines.item(5).startSketchPoint, cavitybridgeLines.item(9))
            constraints.addMidPoint(bridgeLines.item(5).endSketchPoint, cavitybridgeLines.item(7))
            constraints.addPerpendicular(bridgeLines.item(5), bridgeLines.item(4))
            all = adsk.core.ObjectCollection.create()
            for curves in sketch3.sketchCurves:
                all.add(curves)
            for points in sketch3.sketchPoints:
                all.add(points)
            normal = sketch3.xDirection.crossProduct(sketch3.yDirection)
            normal.transformBy(sketch3.transform)
            origin = sketch3.origin
            origin.transformBy(sketch3.transform)
            matrix = adsk.core.Matrix3D.create()
            matrix.setToRotation(-bridgePickupAngle, normal, origin)
            sketch3.move(all, matrix)
            sketch3.name = 'Bridge Pickup [Single-Coil]'
            bridgePickupType = 'S'
        elif pickupBridge == "Humbucker":
            pickupBridge1 = bridgeLines.addCenterPointRectangle(adsk.core.Point3D.create((bridgeDistance+humbuckerWidth/2), 0, 0), adsk.core.Point3D.create((bridgeDistance), (humbuckerLength/2), 0))
            pickupBridge2 = bridgeLines.addByTwoPoints(adsk.core.Point3D.create((bridgeDistance+humbuckerWidth/2), (-pickupCavityMountLength/2), 0), adsk.core.Point3D.create((bridgeDistance+humbuckerWidth/2), (pickupCavityMountLength/2), 0))
            pickupBridge2.isConstruction = True
            pickupBridgeFillet1 = sketch3.sketchCurves.sketchArcs.addFillet(pickupBridge1[0], pickupBridge1[0].endSketchPoint.geometry, pickupBridge1[1], pickupBridge1[1].startSketchPoint.geometry, humbuckerFillet)
            pickupBridgeFillet2 = sketch3.sketchCurves.sketchArcs.addFillet(pickupBridge1[1], pickupBridge1[1].endSketchPoint.geometry, pickupBridge1[2], pickupBridge1[2].startSketchPoint.geometry, humbuckerFillet)
            pickupBridgeFillet3 = sketch3.sketchCurves.sketchArcs.addFillet(pickupBridge1[2], pickupBridge1[2].endSketchPoint.geometry, pickupBridge1[3], pickupBridge1[3].startSketchPoint.geometry, humbuckerFillet)
            pickupBridgeFillet4 = sketch3.sketchCurves.sketchArcs.addFillet(pickupBridge1[3], pickupBridge1[3].endSketchPoint.geometry, pickupBridge1[0], pickupBridge1[0].startSketchPoint.geometry, humbuckerFillet)
            cavityBridge1 = cavitybridgeLines.addCenterPointRectangle(adsk.core.Point3D.create((bridgeDistance+humbuckerWidth/2), 0, 0), adsk.core.Point3D.create((bridgeDistance+humbuckerWidth/2)-pickupCavityMountTabWidth/2, (pickupCavityMountLength/2), 0))
            cavityBridgeFillet1 = sketch3.sketchCurves.sketchArcs.addFillet(cavityBridge1[0], cavityBridge1[0].endSketchPoint.geometry, cavityBridge1[1], cavityBridge1[1].startSketchPoint.geometry, humbuckerFillet/2)
            cavityBridgeFillet2 = sketch3.sketchCurves.sketchArcs.addFillet(cavityBridge1[1], cavityBridge1[1].endSketchPoint.geometry, cavityBridge1[2], cavityBridge1[2].startSketchPoint.geometry, humbuckerFillet/2)
            cavityBridgeFillet3 = sketch3.sketchCurves.sketchArcs.addFillet(cavityBridge1[2], cavityBridge1[2].endSketchPoint.geometry, cavityBridge1[3], cavityBridge1[3].startSketchPoint.geometry, humbuckerFillet/2)
            cavityBridgeFillet4 = sketch3.sketchCurves.sketchArcs.addFillet(cavityBridge1[3], cavityBridge1[3].endSketchPoint.geometry, cavityBridge1[0], cavityBridge1[0].startSketchPoint.geometry, humbuckerFillet/2)
            sketch3.name = 'Bridge Pickup [Humbucker]'
            bridgePickupType = 'H'
        else:
            pass

        if parameters.generateBlanks:
            #Get extrude features
            extrudes = pickupsComp.features.extrudeFeatures

            # Get the profiles of the pickups
            if pickupNeck == "Single-Coil":
                #Create an object collection to use an input.
                neckProfs = adsk.core.ObjectCollection.create()
                for prof in sketch1.profiles:
                    neckProfs.add(prof)
            elif pickupNeck == "Humbucker":
                #Create an object collection to use an input.
                neckProfs = adsk.core.ObjectCollection.create()
                for prof in sketch1.profiles:
                    neckProfs.add(prof)
            else:
                pass
            
            if pickupMiddle == "Single-Coil":
                #Create an object collection to use an input.
                middleProfs = adsk.core.ObjectCollection.create()
                for prof in sketch2.profiles:
                    middleProfs.add(prof)
            elif pickupMiddle == "Humbucker":
                #Create an object collection to use an input.
                middleProfs = adsk.core.ObjectCollection.create()
                for prof in sketch2.profiles:
                    middleProfs.add(prof)
            else:
                pass
            
            if pickupBridge == "Single-Coil":
                #Create an object collection to use an input.
                bridgeProfs = adsk.core.ObjectCollection.create()
                for prof in sketch3.profiles:
                    bridgeProfs.add(prof)
            elif pickupBridge == "Humbucker":
                #Create an object collection to use an input.
                bridgeProfs = adsk.core.ObjectCollection.create()
                for prof in sketch3.profiles:
                    bridgeProfs.add(prof)
            else:
                pass
            
            if pickupNeck == "Single-Coil":
                neckExtrude = extrudes.addSimple(neckProfs, adsk.core.ValueInput.createByReal(-singleCoilDepth), adsk.fusion.FeatureOperations.CutFeatureOperation)
                # Get the extrusion body
                neckPickupBody = neckExtrude.bodies.item(0)
                neckExtrude.name = "Extrusion: Neck Pickup [Single-Coil]"
                # bneckPickupBody.name = "Neck Pickup [Single-Coil]"
            elif pickupNeck == "Humbucker":
                neckExtrude = extrudes.addSimple(neckProfs, adsk.core.ValueInput.createByReal(-humbuckerDepth), adsk.fusion.FeatureOperations.CutFeatureOperation)
                # Get the extrusion body
                neckPickupBody = neckExtrude.bodies.item(0)
                neckExtrude.name = "Extrusion: Neck Pickup [Humbucker]"
                # bneckPickupBody.name = "Neck Pickup [Humbucker]"
            else:
                pass
            
            if pickupMiddle == "Single-Coil":
                middleExtrude = extrudes.addSimple(middleProfs, adsk.core.ValueInput.createByReal(-singleCoilDepth), adsk.fusion.FeatureOperations.CutFeatureOperation)
                # Get the extrusion body
                middlePickupBody = middleExtrude.bodies.item(0)
                middleExtrude.name = "Extrusion: Middle Pickup [Single-Coil]"
                # bmiddlePickupBody.name = "Middle Pickup [Single-Coil]"
            elif pickupMiddle == "Humbucker":
                middleExtrude = extrudes.addSimple(middleProfs, adsk.core.ValueInput.createByReal(-humbuckerDepth), adsk.fusion.FeatureOperations.CutFeatureOperation)
                # Get the extrusion body
                middlePickupBody = middleExtrude.bodies.item(0)
                middleExtrude.name = "Extrusion: Middle Pickup [Humbucker]"
                # bmiddlePickupBody.name = "Middle Pickup [Humbucker]"
            else:
                pass
            
            if pickupBridge == "Single-Coil":
                bridgeExtrude = extrudes.addSimple(bridgeProfs, adsk.core.ValueInput.createByReal(-singleCoilDepth), adsk.fusion.FeatureOperations.CutFeatureOperation)
                # Get the extrusion body
                bridgePickupBody = bridgeExtrude.bodies.item(0)
                bridgeExtrude.name = "Extrusion: Bridge Pickup [Single-Coil]"
                # bbridgePickupBody.name = "Bridge Pickup [Single-Coil]"
            elif pickupBridge == "Humbucker":
                bridgeExtrude = extrudes.addSimple(bridgeProfs, adsk.core.ValueInput.createByReal(-humbuckerDepth), adsk.fusion.FeatureOperations.CutFeatureOperation)
                # Get the extrusion body
                bridgePickupBody = bridgeExtrude.bodies.item(0)
                bridgeExtrude.name = "Extrusion: Bridge Pickup [Humbucker]"
                # bridgePickupBody.name = "Bridge Pickup [Humbucker]"
            else:
                pass
        else:
            pass

        #Centers the camera to fit the entire fretboard
        cam = self.app.activeViewport.camera
        cam.isFitView = True
        cam.isSmoothTransition = False
        self.app.activeViewport.camera = cam
        
        # Group everything used to create the fretboard in the timeline.
        timelineGroupspickups = self.design.timeline.timelineGroups
        pickupsOccIndex = pickupsOcc.timelineObject.index
        
        if parameters.generateBlanks:
            pickupsEndIndex = bridgeExtrude.timelineObject.index
        else:
            pickupsEndIndex = sketch3.timelineObject.index
        
        timelineGroupPickups = timelineGroupspickups.add(pickupsOccIndex, pickupsEndIndex)
        timelineGroupPickups.name = 'Pickups [' + bridgePickupType + middlePickupType + neckPickupType + ']'
        pickupsComp.name = 'Pickups [' + bridgePickupType + middlePickupType + neckPickupType + ']'
        
        return pickupsComp
