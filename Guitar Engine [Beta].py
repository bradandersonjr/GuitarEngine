#Author-Brad Anderson Jr
#Description - Generates a guitar
import adsk.core, adsk.fusion, traceback, math
from math import sqrt
from .defaultParameters import defaultParameters

# Globals
app = adsk.core.Application.cast(None)
ui = adsk.core.UserInterface.cast(None)
units = ''

#Default Inputs
defaultStandard = adsk.core.DropDownCommandInput.cast(None)
defaultFretboardStyle = adsk.core.DropDownCommandInput.cast(None)
defaultPickupNeck = adsk.core.DropDownCommandInput.cast(None)
defaultPickupMiddle = adsk.core.DropDownCommandInput.cast(None)
defaultPickupBridge = adsk.core.DropDownCommandInput.cast(None)
defaultFretNumber = adsk.core.ValueCommandInput.cast(None)
defaultScaleLength = adsk.core.ValueCommandInput.cast(None)
defaultNutLength = adsk.core.ValueCommandInput.cast(None)
defaultEndLength = adsk.core.ValueCommandInput.cast(None)
defaultRadius = adsk.core.ValueCommandInput.cast(None)
defaultNutRadius = adsk.core.ValueCommandInput.cast(None)
defaultEndRadius = adsk.core.ValueCommandInput.cast(None)
defaultEndCurve = adsk.core.ValueCommandInput.cast(None)
defaultfretboardHeight = adsk.core.ValueCommandInput.cast(None)
defaultFilletRadius = adsk.core.ValueCommandInput.cast(None)
defaultTangWidth = adsk.core.ValueCommandInput.cast(None)
defaultTangDepth = adsk.core.ValueCommandInput.cast(None)
defaultBlindFrets = adsk.core.ValueCommandInput.cast(None)
defaultNutSlotWidth = adsk.core.ValueCommandInput.cast(None)
defaultNutSlotDepth = adsk.core.ValueCommandInput.cast(None)
defaultMarkerDiameter = adsk.core.ValueCommandInput.cast(None)
defaultMarkerDepth = adsk.core.ValueCommandInput.cast(None)
defaultMarkerSpacing = adsk.core.ValueCommandInput.cast(None)
defaultFretboardLength = adsk.core.ValueCommandInput.cast(None)
defaultGuitarLength = adsk.core.ValueCommandInput.cast(None)
defaultBodyWidth = adsk.core.ValueCommandInput.cast(None)
defaultBodyThickness = adsk.core.ValueCommandInput.cast(None)
defaultBodyLength = adsk.core.ValueCommandInput.cast(None)
defaultNeckLength = adsk.core.ValueCommandInput.cast(None)
defaultNeckWidth = adsk.core.ValueCommandInput.cast(None)
defaultNeckThickness = adsk.core.ValueCommandInput.cast(None)
defaultHeadstockLength = adsk.core.ValueCommandInput.cast(None)
defaultHeadstockWidth = adsk.core.ValueCommandInput.cast(None)
defaultHeadstockThickness = adsk.core.ValueCommandInput.cast(None)
defaultBridgeStringSpacing = adsk.core.ValueCommandInput.cast(None)
defaultNutStringSpacing = adsk.core.ValueCommandInput.cast(None)
defaultNutToPost = adsk.core.ValueCommandInput.cast(None)
defaultMachinePostHoleDiameter = adsk.core.ValueCommandInput.cast(None)
defaultMachinePostDiameter = adsk.core.ValueCommandInput.cast(None)
defaultMachinePostHoleSpacing = adsk.core.ValueCommandInput.cast(None)
defaultStringCount = adsk.core.ValueCommandInput.cast(None)
defaultfirstFretThickness = adsk.core.ValueCommandInput.cast(None)
defaulttwelfthfretThickness = adsk.core.ValueCommandInput.cast(None)
defaultHeadstockStyle = adsk.core.DropDownCommandInput.cast(None)
defaultNeckSpacing = adsk.core.ValueCommandInput.cast(None)
defaultBridgeSpacing = adsk.core.ValueCommandInput.cast(None)
defaultSingleCoilLength = adsk.core.ValueCommandInput.cast(None)
defaultSingleCoilWidth = adsk.core.ValueCommandInput.cast(None)
defaultSingleCoilDepth = adsk.core.ValueCommandInput.cast(None)
defaultHumbuckerLength = adsk.core.ValueCommandInput.cast(None)
defaultHumbuckerWidth = adsk.core.ValueCommandInput.cast(None)
defaultHumbuckerDepth = adsk.core.ValueCommandInput.cast(None)
defaultHumbuckerFillet = adsk.core.ValueCommandInput.cast(None)
defaultPickupCavityMountLength = adsk.core.ValueCommandInput.cast(None)
defaultPickupCavityMountTabWidth = adsk.core.ValueCommandInput.cast(None)
defaultBridgePickupAngle = adsk.core.ValueCommandInput.cast(None)

handlers = []

def run(context):
    try:
        global app, ui
        app = adsk.core.Application.get()
        ui  = app.userInterface

        # Create a command definition and add a button to the CREATE panel.
        cmdDef = ui.commandDefinitions.addButtonDefinition('adskFretboardPythonAddIn', 'Guitar Engine [Beta] (v2020.06.13)', 'Creates a fretboard component\n\n', 'Resources/Icons')
        createPanel = ui.allToolbarPanels.itemById('SolidCreatePanel')
        fretboardButton = createPanel.controls.addCommand(cmdDef)

        # Connect to the command created event.
        onCommandCreated = FretboardCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        handlers.append(onCommandCreated)

        # Make the button available in the panel.
        fretboardButton.isPromotedByDefault = True
        fretboardButton.isPromoted = True
        if context['IsApplicationStartup'] == False:
            ui.messageBox('<b>Guitar Engine [Beta] (v2020.06.13)</b> has been added to the <i>SOLID</i> tab of the <i>DESIGN</i> workspace.<br><br><div align="center"><b>This is a beta version.</div>')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    try:
        createPanel = ui.allToolbarPanels.itemById('SolidCreatePanel')
        fretboardButton = createPanel.controls.itemById('adskFretboardPythonAddIn')

        if fretboardButton:
            fretboardButton.deleteMe()

        cmdDef = ui.commandDefinitions.itemById('adskFretboardPythonAddIn')

        if cmdDef:
            cmdDef.deleteMe()
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def getCommandInputValue(commandInput, unitType):
    try:
        valCommandInput = adsk.core.ValueCommandInput.cast(commandInput)

        if not valCommandInput:
            return (False, 0)

        # Verify that the expression is valid.
        design = adsk.fusion.Design.cast(app.activeProduct)
        unitsMgr = design.unitsManager
        userParams = design.userParameters

        if unitsMgr.isValidExpression(valCommandInput.expression, unitType):
            value = unitsMgr.evaluateExpression(valCommandInput.expression, unitType)
            return (True, value)
        else:
            return (False, 0)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class FretboardCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            eventArgs = adsk.core.CommandCreatedEventArgs.cast(args)

            # Verify that a Fusion design is active.
            design = adsk.fusion.Design.cast(app.activeProduct)

            if not design:
                ui.messageBox('A Fusion design must be active when invoking this command.')
                return()

            defaultUnits = design.unitsManager.defaultLengthUnits
            userParams = design.userParameters

            # Determine whether to use inches or millimeters as the initial default.
            global units
            if defaultUnits == 'in' or defaultUnits == 'ft':
                units = 'in'
            else:
                units = 'mm'

            # Define the default values and get the previous values from the attributes.
            if units == 'in':
                standard = 'Imperial'
            else:
                standard = 'Metric'

            standardAttrib = design.attributes.itemByName('Fretboard', 'standard')

            if standardAttrib:
                standard = standardAttrib.value
            if standard == 'Imperial':
                units = 'in'
            else:
                units = 'mm'

            fretNumber = str(defaultParameters.fretNumber)
            fretNumberAttrib = design.attributes.itemByName('Fretboard', 'fretNumber')
            if fretNumberAttrib:
                fretNumber = fretNumberAttrib.value

            scaleLength = str(defaultParameters.scaleLength * defaultParameters.userUnit)
            scaleLengthAttrib = design.attributes.itemByName('Fretboard', 'scaleLength')
            if scaleLengthAttrib:
                scaleLength = scaleLengthAttrib.value

            #Equation for fret spacing
            for fretNum in range(1,int((fretNumber))+2):
                fretDistance = (float(scaleLength))-((float(scaleLength))/(2**(fretNum/12.0)))

            fretboardLength = str(math.ceil(float(fretDistance)*8)/8)
            fretboardLengthAttrib = design.attributes.itemByName('Fretboard', 'fretboardLength')
            if fretboardLengthAttrib:
                fretboardLength = fretboardLengthAttrib.value

            nutLength = str(defaultParameters.nutLength * defaultParameters.userUnit)
            nutLengthAttrib = design.attributes.itemByName('Fretboard', 'nutLength')
            if nutLengthAttrib:
                nutLength = nutLengthAttrib.value

            endLength = str(defaultParameters.endLength * defaultParameters.userUnit)
            endLengthAttrib = design.attributes.itemByName('Fretboard', 'endLength')
            if endLengthAttrib:
                endLength = endLengthAttrib.value

            radius = str(defaultParameters.radius * defaultParameters.userUnit)
            radiusAttrib = design.attributes.itemByName('Fretboard', 'radius')
            if radiusAttrib:
                radius = radiusAttrib.value

            nutRadius = str(defaultParameters.nutRadius * defaultParameters.userUnit)
            nutRadiusAttrib = design.attributes.itemByName('Fretboard', 'nutRadius')
            if nutRadiusAttrib:
                nutRadius = nutRadiusAttrib.value

            endRadius = str(defaultParameters.endRadius * defaultParameters.userUnit)
            endRadiusAttrib = design.attributes.itemByName('Fretboard', 'endRadius')
            if endRadiusAttrib:
                endRadius = nutRadiusAttrib.value

            fretboardHeight = str(defaultParameters.fretboardHeight * defaultParameters.userUnit)
            fretboardHeightAttrib = design.attributes.itemByName('Fretboard', 'fretboardHeight')
            if fretboardHeightAttrib:
                fretboardHeight = fretboardHeightAttrib.value

            filletRadius = str(defaultParameters.filletRadius * defaultParameters.userUnit)
            filletRadiusAttrib = design.attributes.itemByName('Fretboard', 'filletRadius')
            if filletRadiusAttrib:
                filletRadius = filletRadiusAttrib.value

            endCurve = str(defaultParameters.endCurve * defaultParameters.userUnit)
            endCurveAttrib = design.attributes.itemByName('Fretboard', 'endCurve')
            if endCurveAttrib:
                endCurve = endCurveAttrib.value

            tangWidth = str(defaultParameters.tangWidth * defaultParameters.userUnit)
            tangWidthAttrib = design.attributes.itemByName('Fretboard', 'tangWidth')
            if tangWidthAttrib:
                tangWidth = tangWidthAttrib.value

            tangDepth = str(defaultParameters.tangDepth * defaultParameters.userUnit)
            tangDepthAttrib = design.attributes.itemByName('Fretboard', 'tangDepth')
            if tangDepthAttrib:
                tangDepth = tangDepthAttrib.value

            blindFrets = str(defaultParameters.blindFrets * defaultParameters.userUnit)
            blindFretsAttrib = design.attributes.itemByName('Fretboard', 'blindFrets')
            if blindFretsAttrib:
                blindFrets = blindFretsAttrib.value

            nutSlotWidth = str(defaultParameters.nutSlotWidth * defaultParameters.userUnit)
            nutSlotWidthAttrib = design.attributes.itemByName('Fretboard', 'nutSlotWidth')
            if nutSlotWidthAttrib:
                nutSlotWidth = nutSlotWidthAttrib.value

            nutSlotDepth = str(defaultParameters.nutSlotDepth * defaultParameters.userUnit)
            nutSlotDepthAttrib = design.attributes.itemByName('Fretboard', 'nutSlotDepth')
            if nutSlotDepthAttrib:
                nutSlotDepth = nutSlotDepthAttrib.value

            markerDiameter = str(defaultParameters.markerDiameter * defaultParameters.userUnit)
            markerDiameterAttrib = design.attributes.itemByName('Fretboard', 'markerDiameter')
            if markerDiameterAttrib:
                markerDiameter = markerDiameterAttrib.value

            markerDepth = str(defaultParameters.markerDepth * defaultParameters.userUnit)
            markerDepthAttrib = design.attributes.itemByName('Fretboard', 'markerDepth')
            if markerDepthAttrib:
                markerDepth = markerDepthAttrib.value

            markerSpacing = str(defaultParameters.markerSpacing * defaultParameters.userUnit)
            markerSpacingAttrib = design.attributes.itemByName('Fretboard', 'markerSpacing')
            if markerSpacingAttrib:
                markerSpacing = markerSpacingAttrib.value

            guitarLength = str(defaultParameters.guitarLength * defaultParameters.userUnit)
            guitarLengthAttrib = design.attributes.itemByName('Fretboard', 'guitarLength')
            if guitarLengthAttrib:
                guitarLength = guitarLengthAttrib.value

            bodyWidth = str(defaultParameters.bodyWidth * defaultParameters.userUnit)
            bodyWidthAttrib = design.attributes.itemByName('Fretboard', 'bodyWidth')
            if bodyWidthAttrib:
                bodyWidth = bodyWidthAttrib.value

            bodyThickness = str(defaultParameters.bodyThickness * defaultParameters.userUnit)
            bodyThicknessAttrib = design.attributes.itemByName('Fretboard', 'bodyThickness')
            if bodyThicknessAttrib:
                bodyThickness = bodyThicknessAttrib.value

            bodyLength = str(defaultParameters.bodyLength * defaultParameters.userUnit)
            bodyLengthAttrib = design.attributes.itemByName('Fretboard', 'bodyLength')
            if bodyLengthAttrib:
                bodyLength = bodyLengthAttrib.value

            firstFretThickness = str(defaultParameters.firstFretThickness * defaultParameters.userUnit)
            firstFretThicknessAttrib = design.attributes.itemByName('Fretboard', 'firstFretThickness')
            if firstFretThicknessAttrib:
                firstFretThickness = firstFretThicknessAttrib.value

            twelfthfretThickness = str(defaultParameters.twelfthfretThickness * defaultParameters.userUnit)
            twelfthfretThicknessAttrib = design.attributes.itemByName('Fretboard', 'twelfthfretThickness')
            if twelfthfretThicknessAttrib:
                twelfthfretThickness = twelfthfretThicknessAttrib.value

            neckThickness = str(defaultParameters.neckThickness * defaultParameters.userUnit)
            neckThicknessAttrib = design.attributes.itemByName('Fretboard', 'neckThickness')
            if neckThicknessAttrib:
                neckThickness = neckThicknessAttrib.value

            headstockLength = str(defaultParameters.headstockLength * defaultParameters.userUnit)
            headstockLengthAttrib = design.attributes.itemByName('Fretboard', 'headstockLength')
            if headstockLengthAttrib:
                headstockLength = headstockLengthAttrib.value

            headstockWidth = str(defaultParameters.headstockWidth * defaultParameters.userUnit)
            headstockWidthAttrib = design.attributes.itemByName('Fretboard', 'headstockWidth')
            if headstockWidthAttrib:
                headstockWidth = headstockWidthAttrib.value

            headstockThickness = str(defaultParameters.headstockThickness * defaultParameters.userUnit)
            headstockThicknessAttrib = design.attributes.itemByName('Fretboard', 'headstockThickness')
            if headstockThicknessAttrib:
                headstockThickness = headstockThicknessAttrib.value

            bridgeStringSpacing = str(defaultParameters.bridgeStringSpacing * defaultParameters.userUnit)
            bridgeStringSpacingAttrib = design.attributes.itemByName('Fretboard', 'bridgeStringSpacing')
            if bridgeStringSpacingAttrib:
                bridgeStringSpacing = bridgeStringSpacingAttrib.value

            nutStringSpacing = str(defaultParameters.nutStringSpacing * defaultParameters.userUnit)
            nutStringSpacingAttrib = design.attributes.itemByName('Fretboard', 'nutStringSpacing')
            if nutStringSpacingAttrib:
                nutStringSpacing = nutStringSpacingAttrib.value

            nutToPost = str(defaultParameters.nutToPost * defaultParameters.userUnit)
            nutToPostAttrib = design.attributes.itemByName('Fretboard', 'nutToPost')
            if nutToPostAttrib:
                nutToPost = nutToPostAttrib.value

            stringCount = str(defaultParameters.stringCount)
            stringCountAttrib = design.attributes.itemByName('Fretboard', 'stringCount')
            if stringCountAttrib:
                stringCount = stringCountAttrib.value

            machinePostHoleDiameter = str(defaultParameters.machinePostHoleDiameter * defaultParameters.userUnit)
            machinePostHoleDiameterAttrib = design.attributes.itemByName('Fretboard', 'machinePostHoleDiameter')
            if machinePostHoleDiameterAttrib:
                machinePostHoleDiameter = machinePostHoleDiameterAttrib.value

            machinePostDiameter = str(defaultParameters.machinePostDiameter * defaultParameters.userUnit)
            machinePostDiameterAttrib = design.attributes.itemByName('Fretboard', 'machinePostDiameter')
            if machinePostDiameterAttrib:
                machinePostDiameter = machinePostDiameterAttrib.value

            machinePostHoleSpacing = str(defaultParameters.machinePostHoleSpacing * defaultParameters.userUnit)
            machinePostHoleSpacingAttrib = design.attributes.itemByName('Fretboard', 'machinePostHoleSpacing')
            if machinePostHoleSpacingAttrib:
                machinePostHoleSpacing = machinePostHoleSpacingAttrib.value

            headstockStyle = 'Straight In-line'
            headstockStyleAttrib = design.attributes.itemByName('Fretboard', 'headstockStyle')
            if headstockStyleAttrib:
                headstockStyle = headstockStyleAttrib.value

            fretboardStyle = 'Straight Radius'
            fretboardStyleAttrib = design.attributes.itemByName('Fretboard', 'fretboardStyle')
            if fretboardStyleAttrib:
                fretboardStyle = fretboardStyleAttrib.value

            pickupNeck = 'Single-Coil'
            pickupNeckAttrib = design.attributes.itemByName('pickups', 'pickupNeck')
            if pickupNeckAttrib:
                pickupNeck = pickupNeckAttrib.value

            pickupMiddle = 'Single-Coil'
            pickupMiddleAttrib = design.attributes.itemByName('pickups', 'pickupMiddle')
            if pickupMiddleAttrib:
                pickupMiddle = pickupMiddleAttrib.value

            pickupBridge = 'Single-Coil'
            pickupBridgeAttrib = design.attributes.itemByName('pickups', 'pickupBridge')
            if pickupBridgeAttrib:
                pickupBridge = pickupBridgeAttrib.value

            neckSpacing = str(defaultParameters.neckSpacing * defaultParameters.userUnit)
            neckSpacingAttrib = design.attributes.itemByName('Fretboard', 'neckSpacing')
            if neckSpacingAttrib:
                neckSpacing = neckSpacingAttrib.value

            bridgeSpacing = str(defaultParameters.bridgeSpacing * defaultParameters.userUnit)
            bridgeSpacingAttrib = design.attributes.itemByName('Fretboard', 'bridgeSpacing')
            if bridgeSpacingAttrib:
                bridgeSpacing = bridgeSpacingAttrib.value

            singleCoilLength = str(defaultParameters.singleCoilLength * defaultParameters.userUnit)
            singleCoilLengthAttrib = design.attributes.itemByName('Fretboard', 'singleCoilLength')
            if singleCoilLengthAttrib:
                singleCoilLength = singleCoilLengthAttrib.value

            singleCoilWidth = str(defaultParameters.singleCoilWidth * defaultParameters.userUnit)
            singleCoilWidthAttrib = design.attributes.itemByName('Fretboard', 'singleCoilWidth')
            if singleCoilWidthAttrib:
                singleCoilWidth = singleCoilWidthAttrib.value

            singleCoilDepth = str(defaultParameters.singleCoilDepth * defaultParameters.userUnit)
            singleCoilDepthAttrib = design.attributes.itemByName('Fretboard', 'singleCoilDepth')
            if singleCoilDepthAttrib:
                singleCoilDepth = singleCoilDepthAttrib.value

            humbuckerLength = str(defaultParameters.humbuckerLength * defaultParameters.userUnit)
            humbuckerLengthAttrib = design.attributes.itemByName('Fretboard', 'humbuckerLength')
            if humbuckerLengthAttrib:
                humbuckerLength = humbuckerLengthAttrib.value

            humbuckerWidth = str(defaultParameters.humbuckerWidth * defaultParameters.userUnit)
            humbuckerWidthAttrib = design.attributes.itemByName('Fretboard', 'humbuckerWidth')
            if humbuckerWidthAttrib:
                humbuckerWidth = humbuckerWidthAttrib.value

            humbuckerDepth = str(defaultParameters.humbuckerDepth * defaultParameters.userUnit)
            humbuckerDepthAttrib = design.attributes.itemByName('Fretboard', 'humbuckerDepth')
            if humbuckerDepthAttrib:
                humbuckerDepth = humbuckerDepthAttrib.value

            humbuckerFillet = str(defaultParameters.humbuckerFillet * defaultParameters.userUnit)
            humbuckerFilletAttrib = design.attributes.itemByName('Fretboard', 'humbuckerFillet')
            if humbuckerFilletAttrib:
                humbuckerFillet = humbuckerFilletAttrib.value

            pickupCavityMountLength = str(defaultParameters.pickupCavityMountLength * defaultParameters.userUnit)
            pickupCavityMountLengthAttrib = design.attributes.itemByName('Fretboard', 'pickupCavityMountLength')
            if pickupCavityMountLengthAttrib:
                pickupCavityMountLength = pickupCavityMountLengthAttrib.value

            pickupCavityMountTabWidth = str(defaultParameters.pickupCavityMountTabWidth * defaultParameters.userUnit)
            pickupCavityMountTabWidthAttrib = design.attributes.itemByName('Fretboard', 'pickupCavityMountTabWidth')
            if pickupCavityMountTabWidthAttrib:
                pickupCavityMountTabWidth = pickupCavityMountTabWidthAttrib.value

            bridgePickupAngle = str(defaultParameters.bridgePickupAngle)
            bridgePickupAngleAttrib = design.attributes.itemByName('Fretboard', 'bridgePickupAngle')
            if bridgePickupAngleAttrib:
                bridgePickupAngle = bridgePickupAngleAttrib.value

            global defaultStandard, defaultFretNumber, defaultScaleLength, defaultNutLength, defaultEndLength, createFlatFretboard, defaultRadius, defaultNutRadius, defaultEndRadius, defaultfretboardHeight, \
                createFilletRadius, defaultFilletRadius, createEndCurve, extensionVisibility, defaultEndCurve, createFretCuts, defaultTangWidth, defaultTangDepth, createBlindFrets, defaultBlindFrets, \
                defaultNutSlotWidth, defaultPickupNeck, defaultPickupMiddle, defaultPickupBridge, defaultNutSlotDepth, createFretMarkers, defaultMarkerDiameter, defaultMarkerDepth, defaultMarkerSpacing, \
                defaultFretboardLength, defaultFretboardStyle, defaultGuitarLength, defaultBodyWidth, defaultBodyThickness, defaultBodyLength, defaultNeckLength, defaultNeckWidth, defaultNeckThickness, \
                defaultHeadstockLength, defaultHeadstockWidth, defaultHeadstockThickness, defaultBridgeStringSpacing, defaultNutStringSpacing, defaultNutToPost, defaultMachinePostHoleDiameter, createBlanks, \
                defaultMachinePostDiameter, defaultMachinePostHoleSpacing, defaultStringCount, defaultfirstFretThickness, defaulttwelfthfretThickness, createDimensions, defaultHeadstockStyle, defaultNeckSpacing, \
                defaultBridgeSpacing, defaultSingleCoilLength, defaultSingleCoilWidth, defaultSingleCoilDepth, defaultHumbuckerLength, defaultHumbuckerWidth, defaultHumbuckerDepth, defaultHumbuckerFillet, \
                defaultPickupCavityMountLength, defaultPickupCavityMountTabWidth, defaultBridgePickupAngle, createOnlyFretboard, errorMessage

            cmd = eventArgs.command
            cmd.isExecutedWhenPreEmpted = False
            inputs = cmd.commandInputs
            cmd.helpFile = 'help.html'
            cmd.okButtonText = 'Create Fretboard'

            # Set the size of the dialog.
            cmd.setDialogInitialSize(275, 800)
            cmd.setDialogMinimumSize(275, 800)
            cmd.okButtonText = 'Create Guitar'

            # Create a tab input.
            tabCmdInput1 = inputs.addTabCommandInput('general', 'General')
            tab1ChildInputs = tabCmdInput1.children
            imgInput = tab1ChildInputs.addImageCommandInput('fretboardImage', '', 'Resources/guitarEngine.png')
            imgInput.isFullWidth = True

            defaultStandard = tab1ChildInputs.addDropDownCommandInput('standard', 'Standard', adsk.core.DropDownStyles.TextListDropDownStyle)
            if standard == "Imperial":
                defaultStandard.listItems.add('Imperial', True)
                defaultStandard.listItems.add('Metric', False)
            else:
                defaultStandard.listItems.add('Imperial', False)
                defaultStandard.listItems.add('Metric', True)

            errorMessage = tab1ChildInputs.addTextBoxCommandInput('errorMessage', '', '', 1, True)
            errorMessage.isFullWidth = True

            defaultFretNumber = tab1ChildInputs.addIntegerSpinnerCommandInput('fretNumber', 'Number of Frets', 12, 36, 1, int(fretNumber))


            defaultStringCount = tab1ChildInputs.addIntegerSpinnerCommandInput('stringCount', 'Number of Strings', 4, 12, 1, int(stringCount))


            defaultScaleLength = tab1ChildInputs.addValueInput('scaleLength', 'Scale Length', units, adsk.core.ValueInput.createByReal(float(scaleLength)))


            defaultGuitarLength = tab1ChildInputs.addValueInput('guitarLength', 'Guitar Length', units, adsk.core.ValueInput.createByReal(float(guitarLength)))


            defaultBodyLength = tab1ChildInputs.addValueInput('bodyLength', 'Body Length', units, adsk.core.ValueInput.createByReal(float(bodyLength)))


            defaultBodyWidth = tab1ChildInputs.addValueInput('bodyWidth', 'Body Width', units, adsk.core.ValueInput.createByReal(float(bodyWidth)))


            defaultBodyThickness = tab1ChildInputs.addValueInput('bodyThickness', 'Body Thickness', units, adsk.core.ValueInput.createByReal(float(bodyThickness)))


            defaultNeckThickness = tab1ChildInputs.addValueInput('neckThickness', 'Neck Thickness', units, adsk.core.ValueInput.createByReal(float(neckThickness)))


            defaultfirstFretThickness = tab1ChildInputs.addValueInput('firstFretThickness', 'First Fret Thickness', units, adsk.core.ValueInput.createByReal(float(firstFretThickness)))


            defaulttwelfthfretThickness = tab1ChildInputs.addValueInput('twelfthfretThickness', 'Twelfth Fret Thickness', units, adsk.core.ValueInput.createByReal(float(twelfthfretThickness)))


            message = '<hr>'
            tab1ChildInputs.addTextBoxCommandInput('fullWidth_textBox', '', message, 1, True)
            createOnlyFretboard = tab1ChildInputs.addBoolValueInput('onlyFretboard', 'Generate Fretboard Only?', True, '', False)


            createBlanks = tab1ChildInputs.addBoolValueInput('blanks', 'Generate Guitar Blanks?', True, '', True)


            createDimensions = tab1ChildInputs.addBoolValueInput('dimensions', 'Generate Guitar Dimensions?', True, '', False)


            # Create a tab input.
            tabCmdInput2 = inputs.addTabCommandInput('fretboard', 'Fretboard')
            tab2ChildInputs = tabCmdInput2.children

            # Create group input.
            groupCmdInput1 = tab2ChildInputs.addGroupCommandInput('fretboard', 'Fretboard')
            groupCmdInput1.isExpanded = True
            groupCmdInput1.isEnabledCheckBoxDisplayed = False
            groupChildInputs1 = groupCmdInput1.children

            defaultFretboardStyle = groupChildInputs1.addDropDownCommandInput('fretboardStyle', 'Fretboard Style', adsk.core.DropDownStyles.TextListDropDownStyle)
            if fretboardStyle == "Straight Radius":
                defaultFretboardStyle.listItems.add('Straight Radius', True)
                defaultFretboardStyle.listItems.add('Compound Radius', False)
                defaultFretboardStyle.listItems.add('Flat/No Radius', False)
            elif fretboardStyle == "Compound Radius":
                defaultFretboardStyle.listItems.add('Straight Radius', False)
                defaultFretboardStyle.listItems.add('Compound Radius', True)
                defaultFretboardStyle.listItems.add('Flat/No Radius', False)
            elif fretboardStyle == "Flat/No Radius":
                defaultFretboardStyle.listItems.add('Straight Radius', False)
                defaultFretboardStyle.listItems.add('Compound Radius', False)
                defaultFretboardStyle.listItems.add('Flat/No Radius', True)
            else:
                pass

            defaultRadius = groupChildInputs1.addValueInput('radius', 'Radius', units, adsk.core.ValueInput.createByReal(float(radius)))


            defaultNutRadius = groupChildInputs1.addValueInput('nutRadius', 'Nut Radius', units, adsk.core.ValueInput.createByReal(float(nutRadius)))


            defaultEndRadius = groupChildInputs1.addValueInput('endRadius', 'End Radius', units, adsk.core.ValueInput.createByReal(float(endRadius)))


            message = '<hr>'
            groupChildInputs1.addTextBoxCommandInput('fullWidth_textBox', '', message, 1, True)
            defaultFretboardLength = groupChildInputs1.addValueInput('fretboardLength', 'Fretboard Length', units, adsk.core.ValueInput.createByReal(float(fretboardLength)))


            defaultfretboardHeight = groupChildInputs1.addValueInput('fretboardHeight', 'Fretboard Height', units, adsk.core.ValueInput.createByReal(float(fretboardHeight)))


            defaultBridgeStringSpacing = groupChildInputs1.addValueInput('bridgeStringSpacing', 'Bridge String Spacing', units, adsk.core.ValueInput.createByReal(float(bridgeStringSpacing)))


            defaultNutStringSpacing = groupChildInputs1.addValueInput('nutStringSpacing', 'Nut String Spacing', units, adsk.core.ValueInput.createByReal(float(nutStringSpacing)))


            defaultNutLength = groupChildInputs1.addValueInput('nutLength', 'Nut Length', units, adsk.core.ValueInput.createByReal(float(nutLength)))


            defaultEndLength = groupChildInputs1.addValueInput('endLength', 'End Length', units, adsk.core.ValueInput.createByReal(float(endLength)))


            defaultNutSlotWidth = groupChildInputs1.addValueInput('nutSlotWidth', 'Nut Slot Width', units, adsk.core.ValueInput.createByReal(float(nutSlotWidth)))


            defaultNutSlotDepth = groupChildInputs1.addValueInput('nutSlotDepth', 'Nut Slot Depth', units, adsk.core.ValueInput.createByReal(float(nutSlotDepth)))


            createFilletRadius = groupChildInputs1.addBoolValueInput('filletRadius', 'Create Fillet Radius?', True, '', True)


            defaultFilletRadius = groupChildInputs1.addValueInput('filletRadius', 'Fillet Radius', units, adsk.core.ValueInput.createByReal(float(filletRadius)))


            createEndCurve = groupChildInputs1.addBoolValueInput('endCurve', 'Create End Curve?', True, '', True)


            defaultEndCurve = groupChildInputs1.addValueInput('endCurve', 'End Curve', units, adsk.core.ValueInput.createByReal(float(endCurve)))


            extensionVisibility = groupChildInputs1.addBoolValueInput('extensionVisibility', 'Extension Visible?', True, '', True)


            # Create group input.
            groupCmdInput2 = tab2ChildInputs.addGroupCommandInput('fretCuts', 'Fret Cuts')
            groupCmdInput2.isExpanded = True
            groupChildInputs2 = groupCmdInput2.children
            createFretCuts = groupChildInputs2.addBoolValueInput('fretCuts', 'Create Fret Cuts?', True, '', True)


            defaultTangWidth = groupChildInputs2.addValueInput('tangWidth', 'Tang Width', units,adsk.core.ValueInput.createByReal(float(tangWidth)))


            defaultTangDepth = groupChildInputs2.addValueInput('tangDepth', 'Tang Depth', units, adsk.core.ValueInput.createByReal(float(tangDepth)))


            createBlindFrets = groupChildInputs2.addBoolValueInput('blindFrets', 'Create Blind Frets?', True, '', True)


            if createFretCuts.value:
                createBlindFrets.isEnabled = True
            else:
                createBlindFrets.isEnabled = False

            defaultBlindFrets = groupChildInputs2.addValueInput('blindFrets', 'Blind Fret Inset', units, adsk.core.ValueInput.createByReal(float(blindFrets)))


            # Create group input.
            groupCmdInput3 = tab2ChildInputs.addGroupCommandInput('markerCuts', 'Fret Marker Cuts')
            groupCmdInput3.isExpanded = True
            groupChildInputs3 = groupCmdInput3.children
            createFretMarkers = groupChildInputs3.addBoolValueInput('fretMarkers', 'Create Fret Markers?', True, '', True)


            defaultMarkerDiameter = groupChildInputs3.addValueInput('markerDiameter', 'Marker Diameter', units, adsk.core.ValueInput.createByReal(float(markerDiameter)))


            defaultMarkerDepth = groupChildInputs3.addValueInput('markerDepth', 'Marker Depth', units, adsk.core.ValueInput.createByReal(float(markerDepth)))


            defaultMarkerSpacing = groupChildInputs3.addValueInput('markerSpacing', 'Marker Spacing', units, adsk.core.ValueInput.createByReal(float(markerSpacing)))


            # Create a tab input.
            tabCmdInput3 = inputs.addTabCommandInput('headstock', 'Headstock')
            tab3ChildInputs = tabCmdInput3.children
            defaultHeadstockStyle = tab3ChildInputs.addDropDownCommandInput('headstockStyle', 'Headstock Style', adsk.core.DropDownStyles.TextListDropDownStyle)


            if headstockStyle == "Straight In-line":
                defaultHeadstockStyle.listItems.add('Straight In-line', True)
                defaultHeadstockStyle.listItems.add('Symmetrical', False)
            else:
                defaultHeadstockStyle.listItems.add('Straight In-line', False)
                defaultHeadstockStyle.listItems.add('Symmetrical', True)

            message = '<div align="center"><b>Notice:</b> Symmetrical only supports 6 strings.</div>'

            tab3ChildInputs.addTextBoxCommandInput('fullWidth_textBox', '', message, 1, True)

            defaultHeadstockLength = tab3ChildInputs.addValueInput('headstockLength', 'Headstock Length', units, adsk.core.ValueInput.createByReal(float(headstockLength)))


            defaultHeadstockWidth = tab3ChildInputs.addValueInput('headstockWidth', 'Headstock Width', units, adsk.core.ValueInput.createByReal(float(headstockWidth)))


            defaultHeadstockThickness = tab3ChildInputs.addValueInput('headstockThickness', 'Headstock Thickness', units, adsk.core.ValueInput.createByReal(float(headstockThickness)))


            defaultNutToPost = tab3ChildInputs.addValueInput('nutToPost', 'Nut To Post', units, adsk.core.ValueInput.createByReal(float(nutToPost)))


            defaultMachinePostHoleDiameter = tab3ChildInputs.addValueInput('machinePostHoleDiameter', 'Machine Post Hole Diameter', units, adsk.core.ValueInput.createByReal(float(machinePostHoleDiameter)))


            defaultMachinePostDiameter = tab3ChildInputs.addValueInput('machinePostDiameter', 'Machine Post Diameter', units, adsk.core.ValueInput.createByReal(float(machinePostDiameter)))


            defaultMachinePostHoleSpacing = tab3ChildInputs.addValueInput('machinePostHoleSpacing', 'Machine Post Hole Spacing', units, adsk.core.ValueInput.createByReal(float(machinePostHoleSpacing)))


            # Create a tab input.
            tabCmdInput4 = inputs.addTabCommandInput('pickups', 'Pickups')
            tab4ChildInputs = tabCmdInput4.children
            defaultPickupNeck = tab4ChildInputs.addDropDownCommandInput('pickups', 'Neck Pickup', adsk.core.DropDownStyles.TextListDropDownStyle)


            if pickupNeck == "Single-Coil":
                defaultPickupNeck.listItems.add('Single-Coil', True)
                defaultPickupNeck.listItems.add('Humbucker', False)
                defaultPickupNeck.listItems.add('None', False)
            elif pickupNeck == "Humbucker":
                defaultPickupNeck.listItems.add('Single-Coil', False)
                defaultPickupNeck.listItems.add('Humbucker', True)
                defaultPickupNeck.listItems.add('None', False)
            elif pickupNeck == "None":
                defaultPickupNeck.listItems.add('Single-Coil', False)
                defaultPickupNeck.listItems.add('Humbucker', False)
                defaultPickupNeck.listItems.add('None', True)
            else:
                pass

            defaultPickupMiddle = tab4ChildInputs.addDropDownCommandInput('pickups', 'Middle Pickup', adsk.core.DropDownStyles.TextListDropDownStyle)


            if pickupMiddle == "Single-Coil":
                defaultPickupMiddle.listItems.add('Single-Coil', True)
                defaultPickupMiddle.listItems.add('Humbucker', False)
                defaultPickupMiddle.listItems.add('None', False)
            elif pickupMiddle == "Humbucker":
                defaultPickupMiddle.listItems.add('Single-Coil', False)
                defaultPickupMiddle.listItems.add('Humbucker', True)
                defaultPickupMiddle.listItems.add('None', False)
            elif pickupMiddle == "None":
                defaultPickupMiddle.listItems.add('Single-Coil', False)
                defaultPickupMiddle.listItems.add('Humbucker', False)
                defaultPickupMiddle.listItems.add('None', True)
            else:
                pass

            defaultPickupBridge = tab4ChildInputs.addDropDownCommandInput('pickups', 'Bridge Pickup', adsk.core.DropDownStyles.TextListDropDownStyle)


            if pickupBridge == "Single-Coil":
                defaultPickupBridge.listItems.add('Single-Coil', True)
                defaultPickupBridge.listItems.add('Humbucker', False)
                # defaultPickupBridge.listItems.add('None', False)
            elif pickupBridge == "Humbucker":
                defaultPickupBridge.listItems.add('Single-Coil', False)
                defaultPickupBridge.listItems.add('Humbucker', True)
            else:
                pass

            # defaultBridgePickupAngle = tab4ChildInputs.addValueInput('pickups', 'Bridge Pickup Angle', 'deg', adsk.core.ValueInput.createByReal(math.radians(float(bridgePickupAngle))))
            defaultBridgePickupAngle = tab4ChildInputs.addFloatSpinnerCommandInput('pickups', 'Bridge Pickup Angle', 'deg', 0, 20, 1, float(bridgePickupAngle))


            defaultNeckSpacing = tab4ChildInputs.addValueInput('pickups', 'Neck Spacing', units, adsk.core.ValueInput.createByReal(float(neckSpacing)))


            defaultBridgeSpacing = tab4ChildInputs.addValueInput('pickups', 'Bridge Spacing', units, adsk.core.ValueInput.createByReal(float(bridgeSpacing)))


            groupCmdInput4 = tab4ChildInputs.addGroupCommandInput('pickUps', 'Single-Coil')
            groupCmdInput4.isExpanded = True
            groupChildInputs4 = groupCmdInput4.children
            defaultSingleCoilLength = groupChildInputs4.addValueInput('pickups', 'Single-Coil Length', units, adsk.core.ValueInput.createByReal(float(singleCoilLength)))


            defaultSingleCoilWidth = groupChildInputs4.addValueInput('pickups', 'Single-Coil Width', units, adsk.core.ValueInput.createByReal(float(singleCoilWidth)))


            defaultSingleCoilDepth = groupChildInputs4.addValueInput('pickups', 'Single-Coil Depth', units, adsk.core.ValueInput.createByReal(float(singleCoilDepth)))


            groupCmdInput5 = tab4ChildInputs.addGroupCommandInput('pickUps', 'Humbucker')
            groupCmdInput5.isExpanded = True
            groupChildInputs5 = groupCmdInput5.children
            defaultHumbuckerLength = groupChildInputs5.addValueInput('pickups', 'Humbucker Length', units, adsk.core.ValueInput.createByReal(float(humbuckerLength)))


            defaultHumbuckerWidth = groupChildInputs5.addValueInput('pickups', 'Humbucker Width', units, adsk.core.ValueInput.createByReal(float(humbuckerWidth)))


            defaultHumbuckerDepth = groupChildInputs5.addValueInput('pickups', 'Humbucker Depth', units, adsk.core.ValueInput.createByReal(float(humbuckerDepth)))


            defaultHumbuckerFillet = groupChildInputs5.addValueInput('pickups', 'Humbucker Corner Radius', units, adsk.core.ValueInput.createByReal(float(humbuckerFillet)))


            defaultPickupCavityMountLength = groupChildInputs5.addValueInput('pickups', 'Length of pickup cavity', units, adsk.core.ValueInput.createByReal(float(pickupCavityMountLength)))


            defaultPickupCavityMountTabWidth = groupChildInputs5.addValueInput('pickups', 'Width of pickup cavity rout', units, adsk.core.ValueInput.createByReal(float(pickupCavityMountTabWidth)))


            # Create a tab input.
            tabCmdInput5 = inputs.addTabCommandInput('info', 'Info')
            tab5ChildInputs = tabCmdInput5.children

            message = '<div align="center"><font size="6"><br><b>Guitar Engine</b><br>by Brad Anderson Jr<br><br><a href="https://www.facebook.com/groups/Fusion360Luthiers/" style="text-decoration: none">Fusion 360 Luthiers Facebook Group</font></a></div>'
            tab5ChildInputs.addTextBoxCommandInput('fullWidth_textBox', '', message, 10, True)

            message = '<div align="center"><font size="4">Please report any issues to the<br><a href="https://github.com/BradAndersonJr/GuitarEngine/" style="text-decoration: none">Guitar Engine Github Repository</font></a></div>'
            tab5ChildInputs.addTextBoxCommandInput('fullWidth_textBox', '', message, 10, True)

            message = '<div align="center"><a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=WP8D4HECT42G8&source=url" style="text-decoration: none">If you would like to support the development of <b>Guitar Engine</b><br> please follow this link. <b><i>Thank you!</b></i></a></div>'
            tab5ChildInputs.addTextBoxCommandInput('fullWidth_textBox', '', message, 3, True)

            # Connect to the command related events.
            onExecute = FretboardCommandExecuteHandler()
            cmd.execute.add(onExecute)
            handlers.append(onExecute)
            onInputChanged = FretboardCommandInputChangedHandler()
            cmd.inputChanged.add(onInputChanged)
            handlers.append(onInputChanged)
            onValidateInputs = FretboardCommandValidateInputsHandler()
            cmd.validateInputs.add(onValidateInputs)
            handlers.append(onValidateInputs)
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
# Event handler for the execute event.
class FretboardCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            eventArgs = adsk.core.CommandEventArgs.cast(args)

            # Save the current values as attributes.
            design = adsk.fusion.Design.cast(app.activeProduct)
            attribs = design.attributes
            attribs.add('Fretboard', 'standard', defaultStandard.selectedItem.name)
            attribs.add('Fretboard', 'headstockStyle', defaultHeadstockStyle.selectedItem.name)
            attribs.add('Fretboard', 'fretNumber', str(defaultFretNumber.value))
            attribs.add('Fretboard', 'stringCount', str(defaultStringCount.value))
            attribs.add('Fretboard', 'scaleLength', str(defaultScaleLength.value))
            attribs.add('Fretboard', 'fretboardLength', str(defaultFretboardLength.value))
            attribs.add('Fretboard', 'nutLength', str(defaultNutLength.value))
            attribs.add('Fretboard', 'endLength', str(defaultEndLength.value))
            attribs.add('Fretboard', 'radius', str(defaultRadius.value))
            attribs.add('Fretboard', 'nutRadius', str(defaultNutRadius.value))
            attribs.add('Fretboard', 'endRadius', str(defaultEndRadius.value))
            attribs.add('Fretboard', 'fretboardHeight', str(defaultfretboardHeight.value))
            attribs.add('Fretboard', 'filletRadius', str(defaultFilletRadius.value))
            attribs.add('Fretboard', 'endCurve', str(defaultEndCurve.value))
            attribs.add('Fretboard', 'tangWidth', str(defaultTangWidth.value))
            attribs.add('Fretboard', 'tangDepth', str(defaultTangDepth.value))
            attribs.add('Fretboard', 'blindFrets', str(defaultBlindFrets.value))
            attribs.add('Fretboard', 'nutSlotWidth', str(defaultNutSlotWidth.value))
            attribs.add('Fretboard', 'nutSlotDepth', str(defaultNutSlotWidth.value))
            attribs.add('Fretboard', 'markerDiameter', str(defaultMarkerDiameter.value))
            attribs.add('Fretboard', 'markerDepth', str(defaultMarkerDepth.value))
            attribs.add('Fretboard', 'markerSpacing', str(defaultMarkerSpacing.value))
            attribs.add('Fretboard', 'guitarLength', str(defaultGuitarLength.value))
            attribs.add('Fretboard', 'bodyWidth', str(defaultBodyWidth.value))
            attribs.add('Fretboard', 'bodyLength', str(defaultBodyLength.value))
            attribs.add('Fretboard', 'bodyThickness', str(defaultBodyThickness.value))
            attribs.add('Fretboard', 'headstockLength', str(defaultHeadstockLength.value))
            attribs.add('Fretboard', 'firstFretThickness', str(defaultfirstFretThickness.value))
            attribs.add('Fretboard', 'twelfthfretThickness', str(defaulttwelfthfretThickness.value))
            attribs.add('Fretboard', 'bridgeStringSpacing', str(defaultBridgeStringSpacing.value))
            attribs.add('Fretboard', 'nutStringSpacing', str(defaultNutStringSpacing.value))
            attribs.add('Fretboard', 'nutToPost', str(defaultNutToPost.value))
            attribs.add('Fretboard', 'machinePostHoleDiameter', str(defaultMachinePostHoleDiameter.value))
            attribs.add('Fretboard', 'machinePostDiameter', str(defaultMachinePostDiameter.value))
            attribs.add('Fretboard', 'machinePostHoleSpacing', str(defaultMachinePostHoleSpacing.value))
            attribs.add('Fretboard', 'neckThickness', str(defaultNeckThickness.value))
            attribs.add('Fretboard', 'headstockWidth', str(defaultHeadstockWidth.value))
            attribs.add('Fretboard', 'headstockThickness', str(defaultHeadstockThickness.value))
            attribs.add('Fretboard', 'neckSpacing', str(defaultNeckSpacing.value))
            attribs.add('Fretboard', 'bridgeSpacing', str(defaultBridgeSpacing.value))
            attribs.add('Fretboard', 'singleCoilLength', str(defaultSingleCoilLength.value))
            attribs.add('Fretboard', 'singleCoilWidth', str(defaultSingleCoilWidth.value))
            attribs.add('Fretboard', 'singleCoilDepth', str(defaultSingleCoilDepth.value))
            attribs.add('Fretboard', 'humbuckerLength', str(defaultHumbuckerLength.value))
            attribs.add('Fretboard', 'humbuckerWidth', str(defaultHumbuckerWidth.value))
            attribs.add('Fretboard', 'humbuckerDepth', str(defaultHumbuckerDepth.value))
            attribs.add('Fretboard', 'humbuckerFillet', str(defaultHumbuckerFillet.value))
            attribs.add('Fretboard', 'pickupCavityMountLength', str(defaultPickupCavityMountLength.value))
            attribs.add('Fretboard', 'pickupCavityMountTabWidth', str(defaultPickupCavityMountTabWidth.value))
            attribs.add('Fretboard', 'bridgePickupAngle', str(defaultBridgePickupAngle.value))

            if defaultHeadstockStyle.selectedItem.name == "Straight In-line":
                headstockStyle = 'Straight In-line'
            else:
                headstockStyle = 'Symmetrical'

            if defaultFretboardStyle.selectedItem.name == "Straight Radius":
                fretboardStyle = 'Straight Radius'
            elif defaultFretboardStyle.selectedItem.name == "Compound Radius":
                fretboardStyle = 'Compound Radius'
            elif defaultFretboardStyle.selectedItem.name == "Flat/No Radius":
                fretboardStyle = 'Flat/No Radius'
            else:
                pass

            if defaultPickupNeck.selectedItem.name == "Single-Coil":
                pickupNeck = 'Single-Coil'
            elif defaultPickupNeck.selectedItem.name == "Humbucker":
                pickupNeck = 'Humbucker'
            elif defaultPickupNeck.selectedItem.name == "None":
                pickupNeck = 'None'
            else:
                pass

            if defaultPickupMiddle.selectedItem.name == "Single-Coil":
                pickupMiddle = 'Single-Coil'
            elif defaultPickupMiddle.selectedItem.name == "Humbucker":
                pickupMiddle = 'Humbucker'
            elif defaultPickupMiddle.selectedItem.name == "None":
                pickupMiddle = 'None'
            else:
                pass

            if defaultPickupBridge.selectedItem.name == "Single-Coil":
                pickupBridge = 'Single-Coil'
            elif defaultPickupBridge.selectedItem.name == "Humbucker":
                pickupBridge = 'Humbucker'
            elif defaultPickupBridge.selectedItem.name == "None":
                pickupBridge = 'None'
            else:
                pass

            fretNumber = defaultFretNumber.value
            stringCount = defaultStringCount.value
            scaleLength = defaultScaleLength.value
            fretboardLength = defaultFretboardLength.value
            nutLength = defaultNutLength.value
            endLength = defaultEndLength.value
            radius = defaultRadius.value
            nutRadius = defaultNutRadius.value
            endRadius = defaultEndRadius.value
            fretboardHeight = defaultfretboardHeight.value
            filletRadius = defaultFilletRadius.value
            endCurve = defaultEndCurve.value
            tangWidth = defaultTangWidth.value
            tangDepth = defaultTangDepth.value
            blindFrets = defaultBlindFrets.value
            nutSlotWidth = defaultNutSlotWidth.value
            nutSlotDepth = defaultNutSlotWidth.value
            markerDiameter = defaultMarkerDiameter.value
            markerDepth = defaultMarkerDepth.value
            markerSpacing = defaultMarkerSpacing.value
            guitarLength = defaultGuitarLength.value
            bodyWidth = defaultBodyWidth.value
            bodyLength = defaultBodyLength.value
            bodyThickness = defaultBodyThickness.value
            headstockLength = defaultHeadstockLength.value
            firstFretThickness = defaultfirstFretThickness.value
            twelfthfretThickness = defaulttwelfthfretThickness.value
            bridgeStringSpacing = defaultBridgeStringSpacing.value
            nutStringSpacing = defaultNutStringSpacing.value
            nutToPost = defaultNutToPost.value
            machinePostHoleDiameter = defaultMachinePostHoleDiameter.value
            machinePostDiameter = defaultMachinePostDiameter.value
            machinePostHoleSpacing = defaultMachinePostHoleSpacing.value
            neckThickness = defaultNeckThickness.value
            headstockWidth = defaultHeadstockWidth.value
            headstockThickness = defaultHeadstockThickness.value
            neckSpacing = defaultNeckSpacing.value
            bridgeSpacing = defaultBridgeSpacing.value
            singleCoilLength = defaultSingleCoilLength.value
            singleCoilWidth = defaultSingleCoilWidth.value
            singleCoilDepth = defaultSingleCoilDepth.value
            humbuckerLength = defaultHumbuckerLength.value
            humbuckerWidth = defaultHumbuckerWidth.value
            humbuckerDepth = defaultHumbuckerDepth.value
            humbuckerFillet = defaultHumbuckerFillet.value
            pickupCavityMountLength = defaultPickupCavityMountLength.value
            pickupCavityMountTabWidth = defaultPickupCavityMountTabWidth.value
            bridgePickupAngle = defaultBridgePickupAngle.value

            if createOnlyFretboard.value:
                # Create the fretboard.
                fretboardComp = buildFretboard(design, fretNumber, scaleLength, nutLength, endLength, radius, nutRadius, endRadius, fretboardHeight, filletRadius, endCurve, tangWidth, tangDepth, blindFrets,
                    nutSlotWidth, nutSlotDepth, markerDiameter, markerDepth, markerSpacing, guitarLength, headstockLength, fretboardLength, firstFretThickness, twelfthfretThickness, neckThickness,
                    headstockWidth, headstockThickness)
            elif createOnlyFretboard.value == False:
                # Create the fretboard.
                fretboardComp = buildFretboard(design, fretNumber, scaleLength, nutLength, endLength, radius, nutRadius, endRadius, fretboardHeight, filletRadius, endCurve, tangWidth, tangDepth, blindFrets,
                    nutSlotWidth, nutSlotDepth, markerDiameter, markerDepth, markerSpacing, guitarLength, headstockLength, fretboardLength, firstFretThickness, twelfthfretThickness, neckThickness,
                    headstockWidth, headstockThickness)

                # Create blanks for body and headstock
                if createBlanks.value:
                    blanksComp = buildBlanks(design, bodyLength, bodyWidth, bodyThickness, headstockLength, headstockWidth, headstockThickness, guitarLength)
                else:
                    pass

                # Create the strings.
                stringsComp = buildStrings(design, stringCount, bridgeStringSpacing, nutStringSpacing, guitarLength, headstockLength, scaleLength, nutLength, fretboardHeight, machinePostHoleSpacing,
                        machinePostHoleDiameter, machinePostDiameter, nutToPost, headstockStyle, headstockThickness)

                # Create the pickup cavities.
                pickupsComp = buildPickups(design, guitarLength, headstockLength, scaleLength, fretboardLength, neckSpacing, bridgeSpacing, singleCoilLength, singleCoilWidth, singleCoilDepth, humbuckerLength,
                        humbuckerWidth, humbuckerDepth, humbuckerFillet, pickupNeck, pickupMiddle, pickupBridge, pickupCavityMountLength, pickupCavityMountTabWidth, bridgePickupAngle)

                # Create dimension sketches
                if createDimensions.value:
                    dimsComp = guitarDimensions(design, fretNumber, scaleLength, nutLength, endLength, nutRadius, endRadius, fretboardHeight, filletRadius, endCurve, tangWidth, bridgeStringSpacing, tangDepth,
                                            nutSlotWidth, nutSlotDepth, markerDiameter, markerDepth, markerSpacing, guitarLength, bodyWidth, headstockLength, bodyLength, stringCount, nutToPost,
                                            machinePostHoleSpacing, machinePostHoleDiameter, machinePostDiameter, nutStringSpacing, fretboardLength, headstockStyle, neckSpacing, bridgeSpacing,
                                            singleCoilLength, singleCoilWidth, singleCoilDepth, humbuckerLength, humbuckerWidth, humbuckerDepth, humbuckerFillet, pickupNeck, pickupMiddle,
                                            pickupBridge, pickupCavityMountLength, pickupCavityMountTabWidth, bridgePickupAngle)
                else:
                    pass

            # Create a list of usable paramters
            parameters = buildParameters(design, fretboardHeight, headstockLength, firstFretThickness, twelfthfretThickness, neckThickness, headstockWidth, headstockThickness, machinePostHoleSpacing,
                    machinePostHoleDiameter, machinePostDiameter, nutToPost, bodyLength, bodyWidth, bodyThickness)

        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

# Event handler for the inputChanged event.
class FretboardCommandInputChangedHandler(adsk.core.InputChangedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            eventArgs = adsk.core.InputChangedEventArgs.cast(args)
            changedInput = eventArgs.input
            design = adsk.fusion.Design.cast(app.activeProduct)
            unitsMgr = design.unitsManager
            defaultUnits = design.unitsManager.defaultLengthUnits

            fretNumber = defaultFretNumber.value
            stringCount = defaultStringCount.value
            scaleLength = defaultScaleLength.value
            fretboardLength = defaultFretboardLength.value
            nutLength = defaultNutLength.value
            endLength = defaultEndLength.value
            radius = defaultRadius.value
            nutRadius = defaultNutRadius.value
            endRadius = defaultEndRadius.value
            fretboardHeight = defaultfretboardHeight.value
            filletRadius = defaultFilletRadius.value
            endCurve = defaultEndCurve.value
            tangWidth = defaultTangWidth.value
            tangDepth = defaultTangDepth.value
            blindFrets = defaultBlindFrets.value
            nutSlotWidth = defaultNutSlotWidth.value
            nutSlotDepth = defaultNutSlotWidth.value
            markerDiameter = defaultMarkerDiameter.value
            markerDepth = defaultMarkerDepth.value
            markerSpacing = defaultMarkerSpacing.value
            guitarLength = defaultGuitarLength.value
            bodyWidth = defaultBodyWidth.value
            bodyLength = defaultBodyLength.value
            bodyThickness = defaultBodyThickness.value
            headstockLength = defaultHeadstockLength.value
            firstFretThickness = defaultfirstFretThickness.value
            twelfthfretThickness = defaulttwelfthfretThickness.value
            bridgeStringSpacing = defaultBridgeStringSpacing.value
            nutStringSpacing = defaultNutStringSpacing.value
            nutToPost = defaultNutToPost.value
            machinePostHoleDiameter = defaultMachinePostHoleDiameter.value
            machinePostDiameter = defaultMachinePostDiameter.value
            machinePostHoleSpacing = defaultMachinePostHoleSpacing.value
            neckThickness = defaultNeckThickness.value
            headstockWidth = defaultHeadstockWidth.value
            headstockThickness = defaultHeadstockThickness.value
            neckSpacing = defaultNeckSpacing.value
            bridgeSpacing = defaultBridgeSpacing.value
            singleCoilLength = defaultSingleCoilLength.value
            singleCoilWidth = defaultSingleCoilWidth.value
            singleCoilDepth = defaultSingleCoilDepth.value
            humbuckerLength = defaultHumbuckerLength.value
            humbuckerWidth = defaultHumbuckerWidth.value
            humbuckerDepth = defaultHumbuckerDepth.value
            humbuckerFillet = defaultHumbuckerFillet.value
            pickupCavityMountLength = defaultPickupCavityMountLength.value
            pickupCavityMountTabWidth = defaultPickupCavityMountTabWidth.value
            bridgePickupAngle = defaultBridgePickupAngle.value

            global units
            if changedInput.id == 'standard':
                if defaultStandard.selectedItem.name == 'Imperial':
                    units = 'in'
                elif defaultStandard.selectedItem.name == 'Metric':
                    units = 'mm'

                defaultScaleLength.value = defaultScaleLength.value
                defaultScaleLength.unitType = units

                defaultFretboardLength.value = defaultFretboardLength.value
                defaultFretboardLength.unitType = units

                defaultNutLength.value = defaultNutLength.value
                defaultNutLength.unitType = units

                defaultEndLength.value = defaultEndLength.value
                defaultEndLength.unitType = units

                defaultRadius.value = defaultRadius.value
                defaultRadius.unitType = units

                defaultNutRadius.value = defaultNutRadius.value
                defaultNutRadius.unitType = units

                defaultEndRadius.value = defaultEndRadius.value
                defaultEndRadius.unitType = units

                defaultfretboardHeight.value = defaultfretboardHeight.value
                defaultfretboardHeight.unitType = units

                defaultFilletRadius.value = defaultFilletRadius.value
                defaultFilletRadius.unitType = units

                defaultEndCurve.value = defaultEndCurve.value
                defaultEndCurve.unitType = units

                defaultTangWidth.value = defaultTangWidth.value
                defaultTangWidth.unitType = units

                defaultTangDepth.value = defaultTangDepth.value
                defaultTangDepth.unitType = units

                defaultBlindFrets.value = defaultBlindFrets.value
                defaultBlindFrets.unitType = units

                defaultNutSlotWidth.value = defaultNutSlotWidth.value
                defaultNutSlotWidth.unitType = units

                defaultNutSlotDepth.value = defaultNutSlotDepth.value
                defaultNutSlotDepth.unitType = units

                defaultMarkerDiameter.value = defaultMarkerDiameter.value
                defaultMarkerDiameter.unitType = units

                defaultMarkerDepth.value = defaultMarkerDepth.value
                defaultMarkerDepth.unitType = units

                defaultMarkerSpacing.value = defaultMarkerSpacing.value
                defaultMarkerSpacing.unitType = units

                defaultGuitarLength.value = defaultGuitarLength.value
                defaultGuitarLength.unitType = units

                defaultBodyWidth.value = defaultBodyWidth.value
                defaultBodyWidth.unitType = units

                defaultBodyLength.value = defaultBodyLength.value
                defaultBodyLength.unitType = units

                defaultBodyThickness.value = defaultBodyThickness.value
                defaultBodyThickness.unitType = units

                defaultHeadstockLength.value = defaultHeadstockLength.value
                defaultHeadstockLength.unitType = units

                defaultfirstFretThickness.value = defaultfirstFretThickness.value
                defaultfirstFretThickness.unitType = units

                defaulttwelfthfretThickness.value = defaulttwelfthfretThickness.value
                defaulttwelfthfretThickness.unitType = units

                defaultBridgeStringSpacing.value = defaultBridgeStringSpacing.value
                defaultBridgeStringSpacing.unitType = units

                defaultNutStringSpacing.value = defaultNutStringSpacing.value
                defaultNutStringSpacing.unitType = units

                defaultNutToPost.value = defaultNutToPost.value
                defaultNutToPost.unitType = units

                defaultMachinePostDiameter.value = defaultMachinePostDiameter.value
                defaultMachinePostDiameter.unitType = units

                defaultMachinePostHoleDiameter.value = defaultMachinePostHoleDiameter.value
                defaultMachinePostHoleDiameter.unitType = units

                defaultMachinePostHoleSpacing.value = defaultMachinePostHoleSpacing.value
                defaultMachinePostHoleSpacing.unitType = units

                defaultNeckThickness.value = defaultNeckThickness.value
                defaultNeckThickness.unitType = units

                defaultHeadstockWidth.value = defaultHeadstockWidth.value
                defaultHeadstockWidth.unitType = units

                defaultHeadstockThickness.value = defaultHeadstockThickness.value
                defaultHeadstockThickness.unitType = units

                defaultNeckSpacing.value = defaultNeckSpacing.value
                defaultNeckSpacing.unitType = units

                defaultBridgeSpacing.value = defaultBridgeSpacing.value
                defaultBridgeSpacing.unitType = units

                defaultSingleCoilLength.value = defaultSingleCoilLength.value
                defaultSingleCoilLength.unitType = units

                defaultSingleCoilWidth.value = defaultSingleCoilWidth.value
                defaultSingleCoilWidth.unitType = units

                defaultSingleCoilDepth.value = defaultSingleCoilDepth.value
                defaultSingleCoilDepth.unitType = units

                defaultHumbuckerLength.value = defaultHumbuckerLength.value
                defaultHumbuckerLength.unitType = units

                defaultHumbuckerWidth.value = defaultHumbuckerWidth.value
                defaultHumbuckerWidth.unitType = units

                defaultHumbuckerDepth.value = defaultHumbuckerDepth.value
                defaultHumbuckerDepth.unitType = units

                defaultHumbuckerFillet.value = defaultHumbuckerFillet.value
                defaultHumbuckerFillet.unitType = units

                defaultPickupCavityMountLength.value = defaultPickupCavityMountLength.value
                defaultPickupCavityMountLength.unitType = units

                defaultPickupCavityMountTabWidth.value = defaultPickupCavityMountTabWidth.value
                defaultPickupCavityMountTabWidth.unitType = units

                defaultBridgePickupAngle.value = defaultBridgePickupAngle.value
                defaultBridgePickupAngle.unitType = 'deg'

        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

# Event handler for the validateInputs event.
class FretboardCommandValidateInputsHandler(adsk.core.ValidateInputsEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.ValidateInputsEventArgs.cast(args)

        errorMessage.text = ''

        if defaultFretboardStyle.selectedItem.name == "Straight Radius":
            defaultRadius.isVisible = True
            defaultNutRadius.isVisible = False
            defaultEndRadius.isVisible = False
        elif defaultFretboardStyle.selectedItem.name == "Compound Radius":
            defaultRadius.isVisible = False
            defaultNutRadius.isVisible = True
            defaultEndRadius.isVisible = True
        elif defaultFretboardStyle.selectedItem.name == "Flat/No Radius":
            defaultRadius.isVisible = False
            defaultNutRadius.isVisible = False
            defaultEndRadius.isVisible = False
        else:
            pass

        if createFretCuts.value:
            defaultTangWidth.isEnabled = True
            defaultTangDepth.isEnabled = True
        else:
            defaultTangWidth.isEnabled = False
            defaultTangDepth.isEnabled = False

        if createFilletRadius.value:
            defaultFilletRadius.isEnabled = True
        else:
            defaultFilletRadius.isEnabled = False

        if createEndCurve.value:
            defaultEndCurve.isEnabled = True
        else:
            defaultEndCurve.isEnabled = False

        if createBlindFrets.value:
            defaultBlindFrets.isEnabled = True
        else:
            defaultBlindFrets.isEnabled = False

        if createFretMarkers.value:
            defaultMarkerDiameter.isEnabled = True
            defaultMarkerDepth.isEnabled = True
            defaultMarkerSpacing.isEnabled = True
        else:
            defaultMarkerDiameter.isEnabled = False
            defaultMarkerDepth.isEnabled = False
            defaultMarkerSpacing.isEnabled = False

        if defaultPickupBridge.selectedItem.name == "Single-Coil":
            defaultBridgePickupAngle.isVisible = True
        elif defaultPickupBridge.selectedItem.name == "Humbucker":
            defaultBridgePickupAngle.isVisible = False

        if createOnlyFretboard.value:
            createBlanks.isEnabled = False
            createDimensions.isEnabled = False
        else:
            createBlanks.isEnabled = True
            createDimensions.isEnabled = True

def buildParameters(design, fretboardHeight, headstockLength, firstFretThickness, twelfthfretThickness, neckThickness, headstockWidth, headstockThickness, machinePostHoleSpacing,
                    machinePostHoleDiameter, machinePostDiameter, nutToPost, bodyLength, bodyWidth, bodyThickness):
    try:
        design = adsk.fusion.Design.cast(app.activeProduct)
        unitsMgr = design.unitsManager
        defaultUnits = design.unitsManager.defaultLengthUnits
        userParams = design.userParameters
        bodyLengthParam = userParams.add('BodyLength', adsk.core.ValueInput.createByReal(float(bodyLength)), defaultUnits, '')
        bodyWidthParam = userParams.add('BodyWidth', adsk.core.ValueInput.createByReal(float(bodyWidth)), defaultUnits, '')
        bodyThicknessParam = userParams.add('BodyThickness', adsk.core.ValueInput.createByReal(float(bodyThickness)), defaultUnits, '')
        fretboardHeightParam = userParams.add('FretboardHeight', adsk.core.ValueInput.createByReal(float(fretboardHeight)), defaultUnits, '')
        neckThicknessParam = userParams.add('NeckThickness', adsk.core.ValueInput.createByReal(float(neckThickness)), defaultUnits, '')
        firstFretThicknessParam = userParams.add('FirstFretThickness', adsk.core.ValueInput.createByReal(float(firstFretThickness)), defaultUnits, '')
        twelfthfretThicknessParam = userParams.add('TwelfthfretThickness', adsk.core.ValueInput.createByReal(float(twelfthfretThickness)), defaultUnits, '')
        headstockLengthParam = userParams.add('HeadstockLength', adsk.core.ValueInput.createByReal(float(headstockLength)), defaultUnits, '')
        headstockWidthParam = userParams.add('HeadstockWidth', adsk.core.ValueInput.createByReal(float(headstockWidth)), defaultUnits, '')
        headstockThicknessParam = userParams.add('HeadstockThickness', adsk.core.ValueInput.createByReal(float(headstockThickness)), defaultUnits, '')
        headstockAngleParam = userParams.add('HeadstockAngle', adsk.core.ValueInput.createByString('10'), 'deg', '')
        hyoidDistanceParam = userParams.add('HyoidDistance', adsk.core.ValueInput.createByReal(1.5*2.54), defaultUnits, '')
        hyoidAngleParam = userParams.add('HyoidAngle', adsk.core.ValueInput.createByString('90'), 'deg', '')
        nutToPostParam = userParams.add('PutToPost', adsk.core.ValueInput.createByReal(float(nutToPost)), defaultUnits, '')
        machinePostHoleSpacingParam = userParams.add('MachinePostHoleSpacing', adsk.core.ValueInput.createByReal(float(machinePostHoleSpacing)), defaultUnits, '')
        machinePostHoleDiameterParam = userParams.add('MachinePostHoleDiameter', adsk.core.ValueInput.createByReal(float(machinePostHoleDiameter)), defaultUnits, '')
        machinePostDiameterParam = userParams.add('MachinePostDiameter', adsk.core.ValueInput.createByReal(float(machinePostDiameter)), defaultUnits, '')
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def buildFretboard(design, fretNumber, scaleLength, nutLength, endLength, radius, nutRadius, endRadius, fretboardHeight, filletRadius, endCurve, tangWidth, tangDepth, blindFrets,
                   nutSlotWidth, nutSlotDepth, markerDiameter, markerDepth, markerSpacing, guitarLength, headstockLength, fretboardLength, firstFretThickness, twelfthfretThickness, neckThickness,
                   headstockWidth, headstockThickness):
    try:
        design = adsk.fusion.Design.cast(app.activeProduct)
        rootComp = design.rootComponent
        allOccs = rootComp.occurrences
        newOcc = allOccs.addNewComponent(adsk.core.Matrix3D.create())
        fretboardComp = adsk.fusion.Component.cast(newOcc.component)
        fretboardComp.description = 'Fretboard'
        #Equation for fret spacing
        for fretNum in range(1,int((fretNumber))+1):
            fretDistance = (scaleLength)-((scaleLength)/(2**(fretNum/12.0)))
        nutDistance = guitarLength - headstockLength
        #This calculates and rounds the total length of the fretboard using the scale length and number of frets
        L = fretboardLength
        print(L/2.54)
        if defaultFretboardStyle.selectedItem.name == "Straight Radius":
            endRadius = nutRadius = radius
        else:
            pass
        #Equation for defining the proper radii
        endR = endRadius-sqrt(endRadius**2-(endLength/2)**2)
        nutR = nutRadius-sqrt(nutRadius**2-(nutLength/2)**2)
        endC = endCurve-sqrt(endCurve**2-(endLength/2)**2)
        # Points defined for curves
        if defaultFretboardStyle.selectedItem.name == "Flat/No Radius":
            endTopL = adsk.core.Point3D.create(nutDistance+endC-L, (endLength/-2), fretboardHeight)
        else:
            endTopL = adsk.core.Point3D.create(nutDistance+endC-L, (endLength/-2), fretboardHeight-endR)
        if defaultFretboardStyle.selectedItem.name == "Flat/No Radius":
            endTopC = adsk.core.Point3D.create(nutDistance-L, 0, fretboardHeight)
        else:
            endTopC = adsk.core.Point3D.create(nutDistance-L, 0, fretboardHeight)
        if defaultFretboardStyle.selectedItem.name == "Flat/No Radius":
            endTopR = adsk.core.Point3D.create(nutDistance+endC-L, (endLength/2), fretboardHeight)
        else:
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
        line1 = sketch1.sketchCurves.sketchLines;
        if createEndCurve.value and defaultFretboardStyle.selectedItem.name == "Flat/No Radius":
            path1 =  sketchArc1.addByThreePoints(adsk.core.Point3D.create(nutDistance+endC-L, (endLength/2), fretboardHeight), adsk.core.Point3D.create(nutDistance-L, 0, fretboardHeight),
                                                adsk.core.Point3D.create(nutDistance+endC-L, (endLength/-2), fretboardHeight))
        elif createEndCurve.value:
            path1 = sketchArc1.addByThreePoints(endTopL, endTopC, endTopR)
        else:
            path1 = sketchArc1.addByThreePoints(adsk.core.Point3D.create(nutDistance-L, (endLength/2), fretboardHeight-endR), adsk.core.Point3D.create(nutDistance-L, 0, fretboardHeight),
                                                adsk.core.Point3D.create(nutDistance-L, (endLength/-2), fretboardHeight-endR))
        # else:
        #     path1 = line1.addByTwoPoints(adsk.core.Point3D.create((endLength/2), fretboardHeight, nutDistance-L), adsk.core.Point3D.create((endLength/-2), fretboardHeight, nutDistance-L))
        openProfile1 = adsk.fusion.Path.create(path1.createForAssemblyContext(newOcc), adsk.fusion.ChainedCurveOptions.noChainedCurves)
        if createEndCurve.value:
            path2 = sketchArc1.addByThreePoints(endBotL, endBotC, endBotR)
        else:
            path2 = line1.addByTwoPoints(adsk.core.Point3D.create(nutDistance-L, (endLength/2), 0), adsk.core.Point3D.create(nutDistance-L, (endLength/-2), 0))
        openProfile2 = adsk.fusion.Path.create(path2.createForAssemblyContext(newOcc), adsk.fusion.ChainedCurveOptions.noChainedCurves)
        if defaultFretboardStyle.selectedItem.name == "Flat/No Radius":
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
        frets = sketch5.sketchCurves.sketchLines;
        sketch5.name = 'Fret Lines (Reference)'
        sketch5.isVisible = False
        #Create sketch for fret cuts
        sketch6 = sketches.add(xyPlane)
        sketch6.isComputeDeferred = False
        cuts = sketch6.sketchCurves.sketchLines;
        sketch6.name = 'Fret slots [ ' + str(fretNumber) + ' frets ]'
        sketch6.isVisible = False
        #create sketch for nut cut
        sketch7 = sketches.add(xyPlane)
        sketch7.isComputeDeferred = False
        nutSketch = sketch7.sketchCurves.sketchLines;
        nutSlotsketch = nutSketch.addTwoPointRectangle(adsk.core.Point3D.create(nutDistance, nutLength, fretboardHeight),
                                                adsk.core.Point3D.create(nutDistance+nutSlotWidth, -nutLength, fretboardHeight))
        nutProfile = sketch7.profiles.item(0)
        sketch7.name = 'Nut slot profile'
        sketch7.isVisible = False
        #create sketch for nut cut
        sketch9 = sketches.add(xyPlane)
        sketch9.isComputeDeferred = False
        fretMarker = sketch9.sketchCurves.sketchCircles;
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
        if createFilletRadius.value:
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
        if createFilletRadius.value:
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
            if createBlindFrets.value:
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
        if createFilletRadius.value:
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
        if createFretMarkers.value:
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
        if createFilletRadius.value:
            nutExtend = extrudes.addSimple(fretboardFaces[4], distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        else:
            nutExtend = extrudes.addSimple(fretboardFaces[1], distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        nutExt = nutExtend.bodies.item(0)
        nutExt.name = 'Extension'
        nutExtend.name = 'Extrusion: Extension'
        nutSlot = extrudes.addSimple(nutProfile, adsk.core.ValueInput.createByReal(-nutSlotDepth), adsk.fusion.FeatureOperations.CutFeatureOperation)
        nutSlot.name = 'Extrusion: Nut Slot'
        if createFretCuts.value:
            #Create the extrusion
            extrude1 = extrudes.add(extrudeInput1)
            extrude1.name = 'Extrusion: Cutting Frets'
        if extensionVisibility.value:
            nutExt.isVisible = True
        else:
            nutExt.isVisible = False
        # Get a reference to an appearance in the library.
        lib = app.materialLibraries.itemByName('Fusion 360 Appearance Library')
        libAppear1 = lib.appearances.itemByName('Paint - Enamel Glossy (Yellow)')
        libAppear2 = lib.appearances.itemByName('Wax (White)')
        fretboardAppearance1 = fretboardComp.bRepBodies.item(0)
        fretboardAppearance1.appearance = libAppear1
        fretboardAppearance2 = fretboardComp.bRepBodies.item(1)
        fretboardAppearance2.appearance = libAppear1
        offSurf.appearance = libAppear2
        #Centers the camera to fit the entire fretboard
        cam = app.activeViewport.camera
        cam.isFitView = True
        cam.isSmoothTransition = False
        app.activeViewport.camera = cam
        # Group everything used to create the fretboard in the timeline.
        timelineGroups = design.timeline.timelineGroups
        newOccIndex = newOcc.timelineObject.index
        if createFretCuts.value:
            endIndex = extrude1.timelineObject.index
        else:
            endIndex = nutSlot.timelineObject.index
        timelineGroup = timelineGroups.add(newOccIndex, endIndex)
        timelineGroup.name = 'Fretboard [ ' + str(fretNumber) + ' Frets ]'
        fretboardComp.name = 'Fretboard' + ' [ ' + str(fretNumber) + ' Frets ]'
        return fretboardComp
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def buildBlanks(design, bodyLength, bodyWidth, bodyThickness, headstockLength, headstockWidth, headstockThickness, guitarLength):
    try:
        design = adsk.fusion.Design.cast(app.activeProduct)
        rootComp = design.rootComponent
        blanksOccs = rootComp.occurrences
        blanksOcc = blanksOccs.addNewComponent(adsk.core.Matrix3D.create())
        blanksComp = adsk.fusion.Component.cast(blanksOcc.component)
        # Create a new sketch.
        sketches = blanksComp.sketches
        xzPlane = blanksComp.xYConstructionPlane
        #Get extrude features
        extrudes = blanksComp.features.extrudeFeatures
        #Create sketch for bridge spacing
        sketch1 = sketches.add(xzPlane)
        sketch1.isComputeDeferred = False
        sketch1.name = 'Body Blank'
        bodyBlankSketch = sketch1.sketchCurves.sketchLines;
        bodyBlank = bodyBlankSketch.addTwoPointRectangle(adsk.core.Point3D.create(0, -bodyWidth/2, 0), adsk.core.Point3D.create(bodyLength, bodyWidth/2, 0))
        #Create sketch for bridge spacing
        sketch2 = sketches.add(xzPlane)
        sketch2.isComputeDeferred = False
        sketch2.name = 'Headstock Blank'
        headstockBlankSketch = sketch2.sketchCurves.sketchLines;
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
        lib = app.materialLibraries.itemByName('Fusion 360 Appearance Library')
        libAppear1 = lib.appearances.itemByName('Wax (White)')
        blanksAppearance1 = blanksComp.bRepBodies.item(0)
        blanksAppearance1.appearance = libAppear1
        blanksAppearance2 = blanksComp.bRepBodies.item(1)
        blanksAppearance2.appearance = libAppear1
        #Centers the camera to fit the entire fretboard
        cam = app.activeViewport.camera
        cam.isFitView = True
        cam.isSmoothTransition = False
        app.activeViewport.camera = cam
        # Group everything used to create the fretboard in the timeline.
        timelineGroupsBlanks = design.timeline.timelineGroups
        blanksOccIndex = blanksOcc.timelineObject.index
        blanksEndIndex = headstockExtrude.timelineObject.index
        timelineGroupBlanks = timelineGroupsBlanks.add(blanksOccIndex, blanksEndIndex)
        timelineGroupBlanks.name = 'Blanks'
        blanksComp.name = 'Blanks'
        return blanksComp
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def buildStrings(design, stringCount, bridgeStringSpacing, nutStringSpacing, guitarLength, headstockLength, scaleLength, nutLength, fretboardHeight, machinePostHoleSpacing,
                                       machinePostHoleDiameter, machinePostDiameter, nutToPost, headstockStyle, headstockThickness):
    try:
        design = adsk.fusion.Design.cast(app.activeProduct)
        rootComp = design.rootComponent
        stringsOccs = rootComp.occurrences
        stringsOcc = stringsOccs.addNewComponent(adsk.core.Matrix3D.create())
        stringsComp = adsk.fusion.Component.cast(stringsOcc.component)
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
            stringSketch = sketch1.sketchCurves.sketchLines;
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
            machinePost = sketch2.sketchCurves.sketchCircles;
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
            stringSketch = sketch1.sketchCurves.sketchLines;
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
            machinePost = sketch2.sketchCurves.sketchCircles;
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
        if createBlanks.value:
            #Extrusion for fret markers
            holesExtrude = extrudes.addSimple(tuningHoles, adsk.core.ValueInput.createByReal(-headstockThickness*2), adsk.fusion.FeatureOperations.CutFeatureOperation)
            holesExtrude.name = 'Extrusion: Tuning Machine Holes'
        else:
            pass
        # Group everything used to create the fretboard in the timeline.
        timelineGroupsStrings = design.timeline.timelineGroups
        stringsOccIndex = stringsOcc.timelineObject.index
        if createBlanks.value:
            stringsEndIndex = holesExtrude.timelineObject.index
        else:
            stringsEndIndex = sketch2.timelineObject.index
        timelineGroupStrings = timelineGroupsStrings.add(stringsOccIndex, stringsEndIndex)
        timelineGroupStrings.name = 'Strings [ ' + str((int(stringCount))) + ' strings ]'
        stringsComp.name = 'Strings [ ' + str((int(stringCount))) + ' strings ]'
        return stringsComp
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def buildPickups(design, guitarLength, headstockLength, scaleLength, fretboardLength, neckSpacing, bridgeSpacing, singleCoilLength, singleCoilWidth, singleCoilDepth, humbuckerLength,
                    humbuckerWidth, humbuckerDepth, humbuckerFillet, pickupNeck, pickupMiddle, pickupBridge, pickupCavityMountLength, pickupCavityMountTabWidth, bridgePickupAngle):
    try:
        design = adsk.fusion.Design.cast(app.activeProduct)
        rootComp = design.rootComponent
        pickupsOccs = rootComp.occurrences
        pickupsOcc = pickupsOccs.addNewComponent(adsk.core.Matrix3D.create())
        pickupsComp = adsk.fusion.Component.cast(pickupsOcc.component)
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
            neckLines = sketch1.sketchCurves.sketchLines;
            cavityNeckLines = sketch1.sketchCurves.sketchLines;
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
            middleLines = sketch2.sketchCurves.sketchLines;
            cavitymiddleLines = sketch2.sketchCurves.sketchLines;
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
        bridgeLines = sketch3.sketchCurves.sketchLines;
        cavitybridgeLines = sketch3.sketchCurves.sketchLines;
        # Get sketch points
        sketchPoints = sketch3.sketchPoints
        if createBlanks.value:
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
        if createBlanks.value:
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
        cam = app.activeViewport.camera
        cam.isFitView = True
        cam.isSmoothTransition = False
        app.activeViewport.camera = cam
        # Group everything used to create the fretboard in the timeline.
        timelineGroupspickups = design.timeline.timelineGroups
        pickupsOccIndex = pickupsOcc.timelineObject.index
        if createBlanks.value:
            pickupsEndIndex = bridgeExtrude.timelineObject.index
        else:
            pickupsEndIndex = sketch3.timelineObject.index
        timelineGroupPickups = timelineGroupspickups.add(pickupsOccIndex, pickupsEndIndex)
        timelineGroupPickups.name = 'Pickups [' + bridgePickupType + middlePickupType + neckPickupType + ']'
        pickupsComp.name = 'Pickups [' + bridgePickupType + middlePickupType + neckPickupType + ']'
        return pickupsComp
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def guitarDimensions(design, fretNumber, scaleLength, nutLength, endLength, nutRadius, endRadius, fretboardHeight, filletRadius, endCurve, tangWidth, bridgeStringSpacing, tangDepth,
                                        nutSlotWidth, nutSlotDepth, markerDiameter, markerDepth, markerSpacing, guitarLength, bodyWidth, headstockLength, bodyLength, stringCount, nutToPost,
                                        machinePostHoleSpacing, machinePostHoleDiameter, machinePostDiameter, nutStringSpacing, fretboardLength, headstockStyle, neckSpacing, bridgeSpacing,
                                        singleCoilLength, singleCoilWidth, singleCoilDepth, humbuckerLength, humbuckerWidth, humbuckerDepth, humbuckerFillet, pickupNeck, pickupMiddle,
                                        pickupBridge, pickupCavityMountLength, pickupCavityMountTabWidth, bridgePickupAngle):
    try:
        design = adsk.fusion.Design.cast(app.activeProduct)
        rootComp = design.rootComponent
        allOccs2 = rootComp.occurrences
        newOcc2 = allOccs2.addNewComponent(adsk.core.Matrix3D.create())
        dimsComp = adsk.fusion.Component.cast(newOcc2.component)
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
        lines = sketch1.sketchCurves.sketchLines;
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
                                                     adsk.core.Point3D.create((topBoundary.length/2), bodyWidth/2+4, 0), False);
        sketch1.sketchDimensions.addDistanceDimension(originBoundary.startSketchPoint, originBoundary.endSketchPoint,
                                                     adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                     adsk.core.Point3D.create(-4, 0, 0), False);
        sketch1.sketchDimensions.addDistanceDimension(bridgeBoundary.startSketchPoint, fret12Boundary.startSketchPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create((nutDistance-scaleLength+scaleLength/4), bodyWidth/4+2, 0), False);
        sketch1.sketchDimensions.addDistanceDimension(fret12Boundary.startSketchPoint, nutBoundary.startSketchPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create((nutDistance-scaleLength/4), bodyWidth/4+2, 0), False);
        sketch1.sketchDimensions.addDistanceDimension(topBoundary.startSketchPoint, bodyBoundary.startSketchPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create((bodyLength/2), bodyWidth/2+2, 0), False);
        sketch1.sketchDimensions.addDistanceDimension(bodyBoundary.startSketchPoint, topBoundary.endSketchPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create(((guitarLength+bodyLength)/2), bodyWidth/2+2, 0), False);
        sketch1.sketchDimensions.addDistanceDimension(topBoundary.startSketchPoint, centerLine.startSketchPoint,
                                                     adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                     adsk.core.Point3D.create(-2, bodyWidth/4, 0), False);
        sketch1.sketchDimensions.addDistanceDimension(centerLine.startSketchPoint, bottomBoundary.startSketchPoint,
                                                     adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                     adsk.core.Point3D.create(-2, -bodyWidth/4, 0), False);
        sketch1.sketchDimensions.addDistanceDimension(centerLine.startSketchPoint, bridgeBoundary.startSketchPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create(((guitarLength-headstockLength-scaleLength)/2), bodyWidth/4+2, 0), False);
        sketch1.sketchDimensions.addDistanceDimension(nutBoundary.startSketchPoint, centerLine.endSketchPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create((guitarLength-headstockLength/2), bodyWidth/4+2, 0), False);
        sketch2 = sketches.add(xzPlane)
        sketch2.isComputeDeferred = True
        dimensionFrets = sketch2.sketchCurves.sketchLines;
        dimensionFrets2 = sketch2.sketchCurves.sketchLines;
        dimensionCircles = sketch2.sketchCurves.sketchCircles;
        dimensionCircles2 = sketch2.sketchCurves.sketchCircles;
        dimensionLines = sketch2.sketchCurves.sketchLines;
        humbuckerCavitySketch = sketch2.sketchCurves.sketchLines;
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
                                                       dimensionFrets[0].endSketchPoint, adsk.fusion.DimensionOrientations.VerticalDimensionOrientation, adsk.core.Point3D.create(nutDistance+2, 0, 0), False);
        sketchDime3 = sketch2.sketchDimensions.addDistanceDimension(dimensioning2.startSketchPoint,
                                                       dimensioning2.endSketchPoint, adsk.fusion.DimensionOrientations.VerticalDimensionOrientation, adsk.core.Point3D.create(nutDistance-L-1, 0, 0), False);
        sketchDime4 = sketch2.sketchDimensions.addDistanceDimension(dimensioning2.endSketchPoint,
                                                       dimensionFrets[0].endSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create(nutDistance-L/2, -12, 0), False);
        sketchDime5 = sketch2.sketchDimensions.addDistanceDimension(bridgeLine2.startSketchPoint,
                                                       dimensionFrets[0].startSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create(nutDistance-scaleLength/2, 8, 0), False);
        sketchDime6 = sketch2.sketchDimensions.addDistanceDimension(bridgeLine2.startSketchPoint,
                                                       bridgeLine2.endSketchPoint, adsk.fusion.DimensionOrientations.VerticalDimensionOrientation, adsk.core.Point3D.create(nutDistance-scaleLength-1, 0, 0), False);
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
            machinePosts = sketch2.sketchCurves.sketchCircles;
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
            sketchDime10 = sketch2.sketchDimensions.addDistanceDimension(dimensionFrets.item(0).startSketchPoint, machinePostHole1.centerSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create(nutDistance+nutToPost/2, 4, 0), False);
            sketchDime11 = sketch2.sketchDimensions.addDistanceDimension(machinePostHole1.centerSketchPoint, machinePostHole2.centerSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create(nutDistance+nutToPost+machinePostHoleSpacing/2, 4, 0), False);
            sketchDime12 = sketch2.sketchDimensions.addDistanceDimension(machinePostHole2.centerSketchPoint, machinePostHole3.centerSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create(nutDistance+nutToPost+machinePostHoleSpacing*1.5, 4, 0), False);
            sketchDime13 = sketch2.sketchDimensions.addDistanceDimension(machinePostHole3.centerSketchPoint, machinePostHole4.centerSketchPoint, adsk.fusion.DimensionOrientations.VerticalDimensionOrientation, adsk.core.Point3D.create(nutDistance+machinePostHoleSpacing*3+2, 0, 0), False);
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
        neckLines = sketch3.sketchCurves.sketchLines;
        cavityNeckLines = sketch3.sketchCurves.sketchLines;
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
        middleLines = sketch3.sketchCurves.sketchLines;
        cavitymiddleLines = sketch3.sketchCurves.sketchLines;
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
        bridgeLines = sketch3.sketchCurves.sketchLines;
        cavitybridgeLines = sketch3.sketchCurves.sketchLines;
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
            pickupNeckDims1 = sketch3.sketchDimensions.addDistanceDimension(pickupNeck1[3].startSketchPoint, pickupNeck1[1].endSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create((neckDistance-singleCoilWidth/2), -6, 0), False);
            pickupNeckDims2 = sketch3.sketchDimensions.addDistanceDimension(cavityNeck1[3].startSketchPoint, cavityNeck1[1].endSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create((neckDistance-singleCoilWidth/2), -5, 0), False);
        elif pickupNeck == "Humbucker":
            pickupNeckDims1 = sketch3.sketchDimensions.addDistanceDimension(pickupNeck1[3].startSketchPoint, pickupNeck1[1].endSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create((neckDistance-humbuckerWidth/2), -6, 0), False);
            pickupNeckDims2 = sketch3.sketchDimensions.addDistanceDimension(cavityNeck1[3].startSketchPoint, cavityNeck1[1].endSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create((neckDistance-humbuckerWidth/2), -5, 0), False);
        else:
            pass
        if pickupMiddle == "Single-Coil":
            pickupMiddleDims1 = sketch3.sketchDimensions.addDistanceDimension(pickupMiddle1[3].startSketchPoint, pickupMiddle1[1].endSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create((middleDistance), -6, 0), False);
            pickupMiddleDims2 = sketch3.sketchDimensions.addDistanceDimension(cavityMiddle1[3].startSketchPoint, cavityMiddle1[1].endSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create((middleDistance), -5, 0), False);
        elif pickupMiddle == "Humbucker":
            pickupMiddleDims1 = sketch3.sketchDimensions.addDistanceDimension(pickupMiddle1[3].startSketchPoint, pickupMiddle1[1].endSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create((middleDistance), -6, 0), False);
            pickupMiddleDims2 = sketch3.sketchDimensions.addDistanceDimension(cavityMiddle1[3].startSketchPoint, cavityMiddle1[1].endSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create((middleDistance), -5, 0), False);
        else:
            pass
        if pickupBridge == "Single-Coil":
            pickupMiddleDims1 = sketch3.sketchDimensions.addDistanceDimension(pickupBridge1[3].startSketchPoint, pickupBridge1[1].endSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create((bridgeDistance+singleCoilWidth/2), -6, 0), False);
            pickupMiddleDims2 = sketch3.sketchDimensions.addDistanceDimension(cavityBridge1[3].startSketchPoint, cavityBridge1[1].endSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create((bridgeDistance+singleCoilWidth/2), -5, 0), False);
        elif pickupBridge == "Humbucker":
            pickupMiddleDims1 = sketch3.sketchDimensions.addDistanceDimension(pickupBridge1[3].startSketchPoint, sketchPoint1, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create((bridgeDistance+humbuckerWidth/2), -6, 0), False);
            pickupMiddleDims2 = sketch3.sketchDimensions.addDistanceDimension(cavityBridge1[3].startSketchPoint, sketchPoint1, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create((bridgeDistance+humbuckerWidth/2), -5, 0), False);
        else:
            pass
        if pickupMiddle == "None":
            pickupGapDims1 = sketch3.sketchDimensions.addDistanceDimension(pickupNeck2.endSketchPoint, sketchPoint1, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create(bridgeDistance + (neckDistance - bridgeDistance)/2, 7, 0), False);
        else:
            pickupGapDims1 = sketch3.sketchDimensions.addDistanceDimension(pickupNeck2.endSketchPoint, sketchPoint1, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create(bridgeDistance + (neckDistance - bridgeDistance)/2, 7, 0), False);
            pickupGapDims2 = sketch3.sketchDimensions.addDistanceDimension(pickupNeck2.endSketchPoint, pickupMiddle2.endSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create(middleDistance + (neckDistance - middleDistance)/2, 6, 0), False);
            pickupGapDims2 = sketch3.sketchDimensions.addDistanceDimension(pickupMiddle2.endSketchPoint, sketchPoint1, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.core.Point3D.create(bridgeDistance + (middleDistance - bridgeDistance)/2, 6, 0), False);
        pickupDims1 = sketch3.sketchDimensions.addDistanceDimension(pickupBridge1[0].startSketchPoint, pickupBridge1[2].endSketchPoint, adsk.fusion.DimensionOrientations.VerticalDimensionOrientation, adsk.core.Point3D.create(bridgeDistance - 4, 0, 0), False);
        pickupDims2 = sketch3.sketchDimensions.addDistanceDimension(pickupBridge2.endSketchPoint, pickupBridge2.startSketchPoint, adsk.fusion.DimensionOrientations.VerticalDimensionOrientation, adsk.core.Point3D.create(bridgeDistance - 5, 0, 0), False);
        #Centers the camera to fit the entire fretboard
        cam = app.activeViewport.camera
        cam.isFitView = True
        cam.isSmoothTransition = True
        cam.viewOrientation = adsk.core.ViewOrientations.TopViewOrientation
        app.activeViewport.camera = cam
        # Group everything used to create the fretboard in the timeline.
        timelineGroups2 = design.timeline.timelineGroups
        newOccIndex2 = newOcc2.timelineObject.index
        endIndex2 = sketch3.timelineObject.index
        timelineGroup2 = timelineGroups2.add(newOccIndex2, endIndex2)
        timelineGroup2.name = 'Dimensions'
        dimsComp.name = 'Dimensions'
        return dimsComp
    # except:
    #     pass
    except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))