import os, sys
import adsk.core, adsk.fusion, adsk.cam, traceback, math
from math import sqrt
from ..ParameterValues import ParameterValues

class FretboardBuilder:

    def __init__(self, app):
        self.app = app
        self.design = app.activeProduct

    def buildFretboard(self, parameters: ParameterValues):
        rootComp = self.design.rootComponent
        allOccs = rootComp.occurrences
        newOcc = allOccs.addNewComponent(adsk.core.Matrix3D.create())

        # Set local variables from parameters object to preserve existing code, refactor at some point..
        fretboardStyle = parameters.fretboardStyle
        fretNumber = parameters.fretNumber
        scaleLength = parameters.scaleLength
        nutLength = parameters.nutLength
        endLength = parameters.endLength
        radius = parameters.radius
        nutRadius = parameters.nutRadius
        endRadius = parameters.endRadius
        fretboardHeight = parameters.fretboardHeight
        filletRadius = parameters.filletRadius
        endCurve = parameters.endCurve
        tangWidth = parameters.tangWidth
        tangDepth = parameters.tangDepth
        blindFrets = parameters.blindFretInset
        nutSlotWidth = parameters.nutSlotWidth
        nutSlotDepth = parameters.nutSlotDepth
        markerDiameter = parameters.markerDiameter
        markerDepth = parameters.markerDepth
        markerSpacing = parameters.markerSpacing
        guitarLength = parameters.guitarLength
        headstockLength = parameters.headstockLength
        fretboardLength = parameters.fretboardLength
        firstFretThickness = parameters.firstFretThickness
        twelfthfretThickness = parameters.twelfthfretThickness
        neckThickness = parameters.neckThickness
        headstockWidth = parameters.headstockWidth
        headstockThickness = parameters.headstockThickness

        
        fretboardComp = adsk.fusion.Component.cast(newOcc.component)
        fretboardComp.description = 'Fretboard'
        
        #Equation for fret spacing
        for fretNum in range(1,int((fretNumber))+1):
            fretDistance = (scaleLength)-((scaleLength)/(2**(fretNum/12.0)))
        
        nutDistance = guitarLength - headstockLength
        
        #This calculates and rounds the total length of the fretboard using the scale length and number of frets
        L = fretboardLength

        if fretboardStyle == "Straight Radius":
            endRadius = nutRadius = radius
        else:
            pass

        #Equation for defining the proper radii
        endR = endRadius-sqrt(endRadius**2-(endLength/2)**2)
        nutR = nutRadius-sqrt(nutRadius**2-(nutLength/2)**2)
        endC = endCurve-sqrt(endCurve**2-(endLength/2)**2)

        # Points defined for curves
        if fretboardStyle == "Flat/No Radius":
            endTopL = adsk.core.Point3D.create(nutDistance+endC-L, (endLength/-2), fretboardHeight)            
            endTopC = adsk.core.Point3D.create(nutDistance-L, 0, fretboardHeight)
            endTopR = adsk.core.Point3D.create(nutDistance+endC-L, (endLength/2), fretboardHeight)
        else:
            endTopL = adsk.core.Point3D.create(nutDistance+endC-L, (endLength/-2), fretboardHeight-endR)
            endTopC = adsk.core.Point3D.create(nutDistance-L, 0, fretboardHeight)
            endTopR = adsk.core.Point3D.create(nutDistance+endC-L, (endLength/2), fretboardHeight-endR)

        endBotL = adsk.core.Point3D.create(nutDistance+endC-L, (endLength/-2), 0)
        endBotC = adsk.core.Point3D.create(nutDistance-L, 0, 0)
        endBotR = adsk.core.Point3D.create(nutDistance+endC-L, (endLength/2), 0)
        nutTopL = adsk.core.Point3D.create(nutDistance, (nutLength/-2), fretboardHeight-nutR)
        nutTopC = adsk.core.Point3D.create(nutDistance, 0, fretboardHeight)
        nutTopR = adsk.core.Point3D.create(nutDistance, (nutLength/2), fretboardHeight-nutR)
        
        # Create a new sketch.
        sketches = fretboardComp.sketches
        xyPlane = fretboardComp.xYConstructionPlane
        xzPlane = fretboardComp.xZConstructionPlane
        yzPlane = fretboardComp.yZConstructionPlane

        #create curve for bridge-end top arc
        sketch1 = sketches.add(xyPlane)
        sketch1.isComputeDeferred = True
        sketchArc1 = sketch1.sketchCurves.sketchArcs
        line1 = sketch1.sketchCurves.sketchLines

        if parameters.createEndCurve and fretboardStyle == "Flat/No Radius":
            path1 =  sketchArc1.addByThreePoints(adsk.core.Point3D.create(nutDistance+endC-L, (endLength/2), fretboardHeight), adsk.core.Point3D.create(nutDistance-L, 0, fretboardHeight),
                                                adsk.core.Point3D.create(nutDistance+endC-L, (endLength/-2), fretboardHeight))
        elif parameters.createEndCurve:
            path1 = sketchArc1.addByThreePoints(endTopL, endTopC, endTopR)
        else:
            path1 = sketchArc1.addByThreePoints(adsk.core.Point3D.create(nutDistance-L, (endLength/2), fretboardHeight-endR), adsk.core.Point3D.create(nutDistance-L, 0, fretboardHeight),
                                                adsk.core.Point3D.create(nutDistance-L, (endLength/-2), fretboardHeight-endR))

        openProfile1 = adsk.fusion.Path.create(path1.createForAssemblyContext(newOcc), adsk.fusion.ChainedCurveOptions.noChainedCurves)
        
        if parameters.createEndCurve:
            path2 = sketchArc1.addByThreePoints(endBotL, endBotC, endBotR)
        else:
            path2 = line1.addByTwoPoints(adsk.core.Point3D.create(nutDistance-L, (endLength/2), 0), adsk.core.Point3D.create(nutDistance-L, (endLength/-2), 0))
        
        openProfile2 = adsk.fusion.Path.create(path2.createForAssemblyContext(newOcc), adsk.fusion.ChainedCurveOptions.noChainedCurves)

        if fretboardStyle == "Flat/No Radius":
            path3 = line1.addByTwoPoints(adsk.core.Point3D.create(nutDistance, (nutLength/-2), fretboardHeight), adsk.core.Point3D.create(nutDistance, (nutLength/2), fretboardHeight))
        else:
            path3 = sketchArc1.addByThreePoints(nutTopL, nutTopC, nutTopR)
        
        openProfile3 = adsk.fusion.Path.create(path3.createForAssemblyContext(newOcc), adsk.fusion.ChainedCurveOptions.noChainedCurves)
        
        path4 = line1.addByTwoPoints(adsk.core.Point3D.create(nutDistance, (nutLength/-2), 0), adsk.core.Point3D.create(nutDistance, (nutLength/2), 0))
        
        openProfile4 = adsk.fusion.Path.create(path4.createForAssemblyContext(newOcc), adsk.fusion.ChainedCurveOptions.noChainedCurves)
        
        line1.addByTwoPoints(path1.startSketchPoint, path3.startSketchPoint)
        line1.addByTwoPoints(path2.startSketchPoint, path4.endSketchPoint)
        line1.addByTwoPoints(path1.endSketchPoint, path3.endSketchPoint)
        line1.addByTwoPoints(path2.endSketchPoint, path4.startSketchPoint)
        
        sketch1.name = 'Fretboard curves'
        sketch1.arePointsShown = False
        sketch1.isVisible = False
        
        #Create sketch for fret lines
        sketch5 = sketches.add(xyPlane)
        sketch5.isComputeDeferred = True
        frets = sketch5.sketchCurves.sketchLines
        sketch5.name = 'Fret Lines (Reference)'
        sketch5.isVisible = False

        #Create sketch for fret cuts
        sketch6 = sketches.add(xyPlane)
        sketch6.isComputeDeferred = False
        cuts = sketch6.sketchCurves.sketchLines
        sketch6.name = 'Fret slots [ ' + str(fretNumber) + ' frets ]'
        sketch6.isVisible = False
        
        #create sketch for nut cut
        sketch7 = sketches.add(xyPlane)
        sketch7.isComputeDeferred = False
        nutSketch = sketch7.sketchCurves.sketchLines
        nutSlotsketch = nutSketch.addTwoPointRectangle(adsk.core.Point3D.create(nutDistance, nutLength, fretboardHeight),
                                                adsk.core.Point3D.create(nutDistance+nutSlotWidth, -nutLength, fretboardHeight))
        nutProfile = sketch7.profiles.item(0)
        sketch7.name = 'Nut slot profile'
        sketch7.isVisible = False

        #create sketch for nut cut
        sketch9 = sketches.add(xyPlane)
        sketch9.isComputeDeferred = False
        fretMarker = sketch9.sketchCurves.sketchCircles
        sketch9.name = 'Inlays'
        sketch9.isVisible = False
        sketch10 = sketches.add(xyPlane)
        sketch10.isComputeDeferred = True
        inplayPoints = sketch10.sketchPoints
        sketch10.name = 'Default Marker Positions'
        sketch10.isVisible = False
        
        # Create surface for bridge-end of fretboard
        loftFeats = fretboardComp.features.loftFeatures
        loftInput1 = loftFeats.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        loftSections1 = loftInput1.loftSections
        loftSections1.add(openProfile2)
        loftSections1.add(openProfile1)
        loftInput1.isSolid = False
        loft1 = loftFeats.add(loftInput1)
        l1 = loft1.faces[0]
        loft1.name = 'Loft: Fretboard End'
        
        # Create surface for nut-end of fretboard
        loftInput2 = loftFeats.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        loftSections2 = loftInput2.loftSections
        loftSections2.add(openProfile3)
        loftSections2.add(openProfile4)
        loftInput2.isSolid = False
        loft2 = loftFeats.add(loftInput2)
        l2 = loft2.faces[0]
        loft2.name = 'Loft: Fretboard Start'
        
        # Create new surface using previous surfaces
        loftInput3 = loftFeats.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        loftSections3 = loftInput3.loftSections
        loftSections3.add(l1)
        loftSections3.add(l2)
        loftInput3.isSolid = False
        loft3 = loftFeats.add(loftInput3)
        l3 = loft3.faces[0]
        loft3.name = 'Loft: Fretboard'
        
        # Get surface bodies and add them to object collection
        surface1 = loft1.bodies.item(0)
        surface2 = loft2.bodies.item(0)
        surface3 = loft3.bodies.item(0)
        surfaces = adsk.core.ObjectCollection.create()
        surfaces.add(surface1)
        surfaces.add(surface2)
        surfaces.add(surface3)
        
        # Define tolerance        
        tolerance = adsk.core.ValueInput.createByString('0.001 in')

        # Create a stitch input to be able to define the input needed for an stitch.
        stitches = fretboardComp.features.stitchFeatures
        stitchInput = stitches.createInput(surfaces, tolerance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        
        # Create a stitch feature.
        stitch = stitches.add(stitchInput)
        stitch.name = 'Stitch: Fretboard'
        
        #Select edges of bridge-end of fretboard to make fillets
        fretboardEndFace = stitch.bodies.item(0)
        fretboardEndEdge1 = fretboardEndFace.edges.item(1)
        fretboardEndEdge2 = fretboardEndFace.edges.item(3)
        
        #Create collection
        endEdges = adsk.core.ObjectCollection.create()
        endEdges.add(fretboardEndEdge1)
        endEdges.add(fretboardEndEdge2)
        
        if parameters.createFilletRadius:
            #Creating fillets
            fillets = fretboardComp.features.filletFeatures
            filletInput = fillets.createInput()
            filletInput.addConstantRadiusEdgeSet(endEdges, adsk.core.ValueInput.createByReal(filletRadius), True)
            filletInput.isG2 = False
            filletInput.isRollingBallCorner = True
            fillet = fillets.add(filletInput)
            fillet.name = 'Rounded Corners'
        else:
            pass
        
        # Get the body created by the stitch
        face = stitch.bodies.item(0)
        if parameters.createFilletRadius:
            topFace = face.faces.item(6)
        else:
            topFace = face.faces.item(4)
        
        # Create input entities for offset feature
        inputEntities = adsk.core.ObjectCollection.create()
        inputEntities.add(topFace)
        
        # Create an input for offset feature
        offsetFeature = fretboardComp.features.offsetFeatures
        offsetInput = offsetFeature.createInput(inputEntities, adsk.core.ValueInput.createByReal(-tangDepth),
                                                adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        
        #Get the surface body.
        extrudeFeature = offsetFeature.add(offsetInput)
        extrudeFeature.name = 'Offset: Fret Projections'
        offSurf = extrudeFeature.bodies.item(0)
        offSurf.name = 'Reference for fret cuts'
        offSurf.isVisible = False
        
        #Get an edge from surface, and add it to object collection.
        extend = offSurf.edges
        ext1 = extend.item(0)
        ext2 = extend.item(1)
        ext3 = extend.item(2)
        ext4 = extend.item(3)
        inputEdges = adsk.core.ObjectCollection.create()
        inputEdges.add(ext1)
        inputEdges.add(ext2)
        inputEdges.add(ext3)
        inputEdges.add(ext4)
        
        #Define a distance to extend.
        distance = adsk.core.ValueInput.createByString('0.5 in')
        
        #Create an extend input to be able to define the input needed for an extend.
        extendFeatures = fretboardComp.features.extendFeatures
        extendFeatureInput1 = extendFeatures.createInput(inputEdges, distance, adsk.fusion.SurfaceExtendTypes.NaturalSurfaceExtendType)
        
        #Create an extend feature.
        extendFeature1 = extendFeatures.add(extendFeatureInput1)
        extendFeature1.name = 'Extend: Fret Projections'

        #Create loop for fret spacing and creation
        fretSpacing = []
        for fret in range(1,int(fretNumber)+1):
            fretDistance = scaleLength-(scaleLength/(2**(fret/12.0)))
            fretSpacing.append(fretDistance)
            fretLength = nutLength + 2*sqrt(((fretDistance/(math.cos(math.radians(math.acos((L**2+(sqrt((((endLength-nutLength)/2)**2) +(L**2)))**2-
                                                ((endLength-nutLength)/2)**2)/(2*L*(sqrt((((endLength-nutLength)/2)**2)+(L**2)))))*((180)/math.pi)))))**2)
                                                -(fretDistance**2))
            if parameters.createBlindFrets:
                #Create fret lines for fret spacing reference
                fretLines = frets.addByTwoPoints(adsk.core.Point3D.create((nutDistance-fretDistance), ((fretLength/2)-(blindFrets/2)), fretboardHeight),
                                                adsk.core.Point3D.create((nutDistance-fretDistance), ((-fretLength/2)+(blindFrets/2)), fretboardHeight))
                #Create fret cuts
                cutLines = cuts.addTwoPointRectangle(adsk.core.Point3D.create((nutDistance-fretDistance-(tangWidth/2)), ((-fretLength/2)+(blindFrets/2)), fretboardHeight),
                                                    adsk.core.Point3D.create((nutDistance-fretDistance+(tangWidth/2)), ((fretLength/2)-(blindFrets/2)), fretboardHeight))
            else:
                #Create fret lines for fret spacing reference
                fretLines = frets.addByTwoPoints(adsk.core.Point3D.create((nutDistance-fretDistance), ((fretLength/2)+(1)), fretboardHeight),
                                                adsk.core.Point3D.create((nutDistance-fretDistance), ((-fretLength/2)-(1)), fretboardHeight))
                #Create fret cuts
                cutLines = cuts.addTwoPointRectangle(adsk.core.Point3D.create((nutDistance-fretDistance-(tangWidth/2)), ((-fretLength/2)-(1)), fretboardHeight),
                                                    adsk.core.Point3D.create((nutDistance-fretDistance+(tangWidth/2)), ((fretLength/2)+(1)), fretboardHeight))
        
        inlays = [((y-x)/2)+x for x, y in zip(fretSpacing,fretSpacing[1:])]
        
        for inlayOdd in inlays[1:9:2] + inlays[13:21:2]:
            fretMarker.addByCenterRadius(adsk.core.Point3D.create(nutDistance-inlayOdd, 0, fretboardHeight), markerDiameter)
            points = adsk.core.Point3D.create(nutDistance-inlayOdd, 0, fretboardHeight)
            sketch10 = inplayPoints.add(points)
        
        for inlayOdd in inlays[25:33:2]:
            fretMarker.addByCenterRadius(adsk.core.Point3D.create(nutDistance-inlayOdd, 0, fretboardHeight), markerDiameter/2)
            points = adsk.core.Point3D.create(nutDistance-inlayOdd, 0, fretboardHeight)
            sketch10 = inplayPoints.add(points)
        
        for inlayEven in inlays[10:24:12]:
            fretMarker.addByCenterRadius(adsk.core.Point3D.create(nutDistance-inlayEven, markerSpacing/2, fretboardHeight), markerDiameter)
            fretMarker.addByCenterRadius(adsk.core.Point3D.create(nutDistance-inlayEven, -markerSpacing/2, fretboardHeight), markerDiameter)
            points = adsk.core.Point3D.create(nutDistance-inlayEven, 0, fretboardHeight)
            sketch10 = inplayPoints.add(points)
        
        fretMarkers = adsk.core.ObjectCollection.create()
        
        for markers in sketch9.profiles:
            fretMarkers.add(markers)
        
        fretboard = stitch.bodies.item(0)
        fretboard.name = 'Fretboard' + ' [ ' + str(fretNumber) + ' frets ]'
        fretboardFaces = [face for face in fretboard.faces]
        
        if parameters.createFilletRadius:
            fretboardSurf = fretboardFaces[6::2]
        else:
            fretboardSurf = fretboardFaces[4::2]
        
        fretCurves = [curve for curve in sketch5.sketchCurves]
        sketch8 = sketches.add(xyPlane)
        sketch8.isComputeDeferred = True
        fretProj = sketch8.projectToSurface(fretboardSurf, fretCurves, adsk.fusion.SurfaceProjectTypes.AlongVectorSurfaceProjectType,
                                            fretboardComp.zConstructionAxis)
        sketch8.name = 'Fret Lines [ ' + str(fretNumber) + ' frets ]'
        sketch8.isVisible = False
        
        #Create an object collection to use an input.
        profs = adsk.core.ObjectCollection.create()
        
        #Add all of the profiles to the collection.
        for prof in sketch6.profiles:
            profs.add(prof)
        
        #Get extrude features
        extrudes = fretboardComp.features.extrudeFeatures
        
        if parameters.createFretMarkers:
            #Extrusion for fret markers
            markerExtrude = extrudes.addSimple(fretMarkers, adsk.core.ValueInput.createByReal(-markerDepth), adsk.fusion.FeatureOperations.CutFeatureOperation)
            markerExtrude.name = 'Extrusion: Fret Markers'
        else:
            pass
        
        # Extrude Sample 4: Create an extrusion that goes from the profile plane to a specified entity.
        extrudeInput1 = extrudes.createInput(profs, adsk.fusion.FeatureOperations.CutFeatureOperation)
        extentToEntity = adsk.fusion.ToEntityExtentDefinition.create(extrudeFeature.faces.item(0), True)
        
        # Set the one side extent with the to-entity-extent-definition, and with a taper angle of 0 degree
        extrudeInput1.setOneSideExtent(extentToEntity, adsk.fusion.ExtentDirections.PositiveExtentDirection)
        
        #Extrusion for adding material to the nut-end of the fretboard
        if parameters.createFilletRadius:
            nutExtend = extrudes.addSimple(fretboardFaces[4], distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        else:
            nutExtend = extrudes.addSimple(fretboardFaces[1], distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        
        nutExt = nutExtend.bodies.item(0)
        nutExt.name = 'Extension'
        nutExtend.name = 'Extrusion: Extension'
        nutSlot = extrudes.addSimple(nutProfile, adsk.core.ValueInput.createByReal(-nutSlotDepth), adsk.fusion.FeatureOperations.CutFeatureOperation)
        nutSlot.name = 'Extrusion: Nut Slot'
        
        if parameters.createFretCuts:
            #Create the extrusion
            extrude1 = extrudes.add(extrudeInput1)
            extrude1.name = 'Extrusion: Cutting Frets'
        
        if parameters.extensionVisible:
            nutExt.isVisible = True
        else:
            nutExt.isVisible = False
        
        # Get a reference to an appearance in the library.
        lib = self.app.materialLibraries.itemByName('Fusion 360 Appearance Library')
        libAppear1 = lib.appearances.itemByName('Paint - Enamel Glossy (Yellow)')
        libAppear2 = lib.appearances.itemByName('Wax (White)')
        fretboardAppearance1 = fretboardComp.bRepBodies.item(0)
        fretboardAppearance1.appearance = libAppear1
        fretboardAppearance2 = fretboardComp.bRepBodies.item(1)
        fretboardAppearance2.appearance = libAppear1
        offSurf.appearance = libAppear2
        
        #Centers the camera to fit the entire fretboard
        cam = self.app.activeViewport.camera
        cam.isFitView = True
        cam.isSmoothTransition = False
        self.app.activeViewport.camera = cam
        
        # Group everything used to create the fretboard in the timeline.
        timelineGroups = self.design.timeline.timelineGroups
        newOccIndex = newOcc.timelineObject.index
        
        if parameters.createFretCuts:
            endIndex = extrude1.timelineObject.index
        else:
            endIndex = nutSlot.timelineObject.index
        
        timelineGroup = timelineGroups.add(newOccIndex, endIndex)
        timelineGroup.name = 'Fretboard [ ' + str(fretNumber) + ' Frets ]'
        fretboardComp.name = 'Fretboard' + ' [ ' + str(fretNumber) + ' Frets ]'
        
        return fretboardComp
