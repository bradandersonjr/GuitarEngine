#Author-Brad Anderson
#Description-Generates a fretboard

import adsk.core, adsk.fusion, traceback, math
from math import sqrt

# Globals
app = adsk.core.Application.cast(None)
ui = adsk.core.UserInterface.cast(None)
units = ''

#Default Inputs
defaultStandard = adsk.core.DropDownCommandInput.cast(None)
defaultFretNumber = adsk.core.ValueCommandInput.cast(None) #Number of Frets
defaultScaleLength = adsk.core.ValueCommandInput.cast(None) #scale length
defaultNutLength = adsk.core.ValueCommandInput.cast(None) #Neck length at nut
defaultEndLength = adsk.core.ValueCommandInput.cast(None) #Neck length at end
defaultNutRadius = adsk.core.ValueCommandInput.cast(None) #Neck Radius
defaultEndRadius = adsk.core.ValueCommandInput.cast(None) #End Radius
defaultEndCurve = adsk.core.ValueCommandInput.cast(None) #Fretboard end curve
defaultHeight = adsk.core.ValueCommandInput.cast(None) #Overall height of the fretboard
defaultFilletRadius = adsk.core.ValueCommandInput.cast(None) #radius of the end of fretboard corners
defaultTangWidth = adsk.core.ValueCommandInput.cast(None) #width of the fret tangs
defaultTangDepth = adsk.core.ValueCommandInput.cast(None) #depth of the fret tangs
defaultCrownWidth = adsk.core.ValueCommandInput.cast(None) #depth of the fret tangs
defaultCrownHeight = adsk.core.ValueCommandInput.cast(None) #depth of the fret tangs
defaultBlindFrets = adsk.core.ValueCommandInput.cast(None) #edge distance for the blind frets
defaultNutSlotWidth = adsk.core.ValueCommandInput.cast(None) #this is the width of the nut cut
defaultNutSlotDepth = adsk.core.ValueCommandInput.cast(None) #this is the width of the nut cut
defaultMarkerDiameter = adsk.core.ValueCommandInput.cast(None)
defaultMarkerDepth = adsk.core.ValueCommandInput.cast(None)
defaultMarkerSpacing = adsk.core.ValueCommandInput.cast(None)
defaultFretboardLength = adsk.core.ValueCommandInput.cast(None)
defaultGuitarLength = adsk.core.ValueCommandInput.cast(None)
defaultGuitarWidth = adsk.core.ValueCommandInput.cast(None)
defaultGuitarThickness = adsk.core.ValueCommandInput.cast(None)
defaultBodyLength = adsk.core.ValueCommandInput.cast(None)
defaultNeckLength = adsk.core.ValueCommandInput.cast(None)
defaultNeckWidth = adsk.core.ValueCommandInput.cast(None)
defaultNeckThickness = adsk.core.ValueCommandInput.cast(None)
defaultHeadstockLength = adsk.core.ValueCommandInput.cast(None)
defaultHeadstockWidth = adsk.core.ValueCommandInput.cast(None)
defaultHeadstockThickness = adsk.core.ValueCommandInput.cast(None)
defaultFirstFretThickness = adsk.core.ValueCommandInput.cast(None)
defaultTwelfthFretThickness = adsk.core.ValueCommandInput.cast(None)
defaultBridgeStringSpacing = adsk.core.ValueCommandInput.cast(None)
defaultNutStringSpacing = adsk.core.ValueCommandInput.cast(None)
defaultNutToPost = adsk.core.ValueCommandInput.cast(None)
defaultMachinePostHoleDiameter = adsk.core.ValueCommandInput.cast(None)
defaultMachinePostDiameter = adsk.core.ValueCommandInput.cast(None)
defaultMachinePostHoleSpacing = adsk.core.ValueCommandInput.cast(None)
defaultStringCount = adsk.core.ValueCommandInput.cast(None)
defaultFirstFretHeight = adsk.core.ValueCommandInput.cast(None)
defaultTwelfthFretHeight = adsk.core.ValueCommandInput.cast(None)

defaultneckHumGap = adsk.core.ValueCommandInput.cast(None)
defaultbridgeHumGap = adsk.core.ValueCommandInput.cast(None)
defaultHumbuckerCavityLength = adsk.core.ValueCommandInput.cast(None)
defaultHumbuckerCavityWidth = adsk.core.ValueCommandInput.cast(None)
defaultHumbuckerCavityDepth = adsk.core.ValueCommandInput.cast(None)
defaultHumbuckerCavityMountDepth = adsk.core.ValueCommandInput.cast(None)
defaultHumbuckerCavityFillet = adsk.core.ValueCommandInput.cast(None)
defaultHumbuckerCavityMountLength = adsk.core.ValueCommandInput.cast(None)
defaultHumbuckerCavityMountWidth = adsk.core.ValueCommandInput.cast(None)



neckHumGap = 0.25 * 2.54
bridgeHumGap = 0.5 * 2.54

humbuckerCavityLength = 2.81375 * 2.54 #2.7825 + 1/32
humbuckerCavityWidth = 1.55875 * 2.54 #1.5275 + 1/32
humbuckerCavityDepth = 0.8 * 2.54
humbuckerCavityMountDepth = 0.9 * 2.54
humbuckerCavityFillet = 0.125 * 2.54
humbuckerCavityMountLength = 0.625 * 2.54
humbuckerCavityMountWidth = 0.785 * 2.54

handlers = []

def run(context):
    try:
        global app, ui
        app = adsk.core.Application.get()
        ui  = app.userInterface

        # Create a command definition and add a button to the CREATE panel.
        cmdDef = ui.commandDefinitions.addButtonDefinition('adskFretboardPythonAddIn', 'Guitar Engine [Beta] (v2019.04.07)', 'Creates a fretboard component\n\n', 'Resources/Icons')        
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
            ui.messageBox('<b>Guitar Engine [Beta] (v2019.04.07)</b> has been added to the <i>SOLID</i> tab of the <i>DESIGN</i> workspace.<br><br><div align="center"><b>This is a beta version.</div>')
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
                
            # Determine whether to use inches or millimeters as the intial default.
            global units
            if defaultUnits == 'in' or defaultUnits == 'ft':
                units = 'in'
            else:
                units = 'mm'
                        
            # Define the default values and get the previous values from the attributes.
            if units == 'in':
                standard = 'English'
            else:
                standard = 'Metric'
            standardAttrib = design.attributes.itemByName('Fretboard', 'standard')
            if standardAttrib:
                standard = standardAttrib.value
                
            if standard == 'English':
                units = 'in'
            else:
                units = 'mm'

            fretNumber = '22'
            fretNumberAttrib = design.attributes.itemByName('Fretboard', 'fretNumber')
            if fretNumberAttrib:
                fretNumber = fretNumberAttrib.value

            scaleLength = str(25.5 * 2.54)
            scaleLengthAttrib = design.attributes.itemByName('Fretboard', 'scaleLength')
            if scaleLengthAttrib:
                scaleLength = scaleLengthAttrib.value
                
            fretboardLength = str(18.75 * 2.54)
            fretboardLengthAttrib = design.attributes.itemByName('Fretboard', 'fretboardLength')
            if fretboardLengthAttrib:
                fretboardLength = fretboardLengthAttrib.value                
                
            nutLength = str(1.6527 * 2.54)
            nutLengthAttrib = design.attributes.itemByName('Fretboard', 'nutLength')
            if nutLengthAttrib:
                nutLength = nutLengthAttrib.value

            endLength = str(2.1875 * 2.54)
            endLengthAttrib = design.attributes.itemByName('Fretboard', 'endLength')
            if endLengthAttrib:
                endLength = endLengthAttrib.value

            nutRadius = str(9.5 * 2.54)
            nutRadiusAttrib = design.attributes.itemByName('Fretboard', 'nutRadius')
            if nutRadiusAttrib:
                nutRadius = nutRadiusAttrib.value

            endRadius = str(12.0 * 2.54)
            endRadiusAttrib = design.attributes.itemByName('Fretboard', 'endRadius')
            if endRadiusAttrib:
                endRadius = nutRadiusAttrib.value

            height = str(0.125 * 2.54)
            heightAttrib = design.attributes.itemByName('Fretboard', 'height')
            if heightAttrib:
                height = heightAttrib.value

            filletRadius = str(0.2 * 2.54)
            filletRadiusAttrib = design.attributes.itemByName('Fretboard', 'filletRadius')
            if filletRadiusAttrib:
                filletRadius = filletRadiusAttrib.value
                
            endCurve = str(10.0 * 2.54)
            endCurveAttrib = design.attributes.itemByName('Fretboard', 'endCurve')
            if endCurveAttrib:
                endCurve = endCurveAttrib.value

            tangWidth = str(0.023 * 2.54)
            tangWidthAttrib = design.attributes.itemByName('Fretboard', 'tangWidth')
            if tangWidthAttrib:
                tangWidth = tangWidthAttrib.value

            tangDepth = str(0.073 * 2.54)
            tangDepthAttrib = design.attributes.itemByName('Fretboard', 'tangDepth')
            if tangDepthAttrib:
                tangDepth = tangDepthAttrib.value
                
            crownWidth = str(0.084 * 2.54)
            crownWidthAttrib = design.attributes.itemByName('Fretboard', 'crownWidth')
            if crownWidthAttrib:
                crownWidth = crownWidthAttrib.value
                
            crownHeight = str(0.039 * 2.54)
            crownHeightAttrib = design.attributes.itemByName('Fretboard', 'crownHeight')
            if crownHeightAttrib:
                crownHeight = crownWidthAttrib.value

            blindFrets = str(0.0625 * 2.54)
            blindFretsAttrib = design.attributes.itemByName('Fretboard', 'blindFrets')
            if blindFretsAttrib:
                blindFrets = blindFretsAttrib.value

            nutSlotWidth = str(0.127 * 2.54)
            nutSlotWidthAttrib = design.attributes.itemByName('Fretboard', 'nutSlotWidth')
            if nutSlotWidthAttrib:
                nutSlotWidth = nutSlotWidthAttrib.value

            nutSlotDepth = str(0.1 * 2.54)
            nutSlotDepthAttrib = design.attributes.itemByName('Fretboard', 'nutSlotDepth')
            if nutSlotDepthAttrib:
                nutSlotDepth = nutSlotDepthAttrib.value

            markerDiameter = str(0.1 * 2.54)
            markerDiameterAttrib = design.attributes.itemByName('Fretboard', 'markerDiameter')
            if markerDiameterAttrib:
                markerDiameter = markerDiameterAttrib.value

            markerDepth = str(0.05 * 2.54)
            markerDepthAttrib = design.attributes.itemByName('Fretboard', 'markerDepth')
            if markerDepthAttrib:
                markerDepth = markerDepthAttrib.value
                
            markerSpacing = str(0.875 * 2.54)
            markerSpacingAttrib = design.attributes.itemByName('Fretboard', 'markerSpacing')
            if markerSpacingAttrib:
                markerSpacing = markerSpacingAttrib.value

            guitarLength = str(38.5 * 2.54)
            guitarLengthAttrib = design.attributes.itemByName('Fretboard', 'guitarLength')
            if guitarLengthAttrib:
                guitarLength = guitarLengthAttrib.value

            guitarWidth = str(12.5 * 2.54)
            guitarWidthAttrib = design.attributes.itemByName('Fretboard', 'guitarWidth')
            if guitarWidthAttrib:
                guitarWidth = guitarWidthAttrib.value

            guitarThickness = str(1.25 * 2.54)
            guitarThicknessAttrib = design.attributes.itemByName('Fretboard', 'guitarThickness')
            if guitarThicknessAttrib:
                guitarThickness = guitarThicknessAttrib.value

            bodyLength = str(16.75 * 2.54)
            bodyLengthAttrib = design.attributes.itemByName('Fretboard', 'bodyLength')
            if bodyLengthAttrib:
                bodyLength = bodyLengthAttrib.value

#            neckLength = str(25.5 * 2.54)
#            neckLengthAttrib = design.attributes.itemByName('Fretboard', 'neckLength')
#            if neckLengthAttrib:
#                neckLength = neckLengthAttrib.value
#
#            neckWidth = str(25.5 * 2.54)
#            neckWidthAttrib = design.attributes.itemByName('Fretboard', 'neckWidth')
#            if neckWidthAttrib:
#                neckWidth = neckWidthAttrib.value

            firstFretHeight = str(0.8 * 2.54)
            firstFretHeightAttrib = design.attributes.itemByName('Fretboard', 'firstFretHeight')
            if firstFretHeightAttrib:
                firstFretHeight = firstFretHeightAttrib.value

            twelfthFretHeight = str(0.85 * 2.54)
            twelfthFretHeightAttrib = design.attributes.itemByName('Fretboard', 'twelfthFretHeight')
            if twelfthFretHeightAttrib:
                twelfthFretHeight = twelfthFretHeightAttrib.value
                            
            neckThickness = str(1 * 2.54)
            neckThicknessAttrib = design.attributes.itemByName('Fretboard', 'neckThickness')
            if neckThicknessAttrib:
                neckThickness = neckThicknessAttrib.value
            
            headstockLength = str(7.5 * 2.54)
            headstockLengthAttrib = design.attributes.itemByName('Fretboard', 'headstockLength')
            if headstockLengthAttrib:
                headstockLength = headstockLengthAttrib.value

            headstockWidth = str(3.5 * 2.54)
            headstockWidthAttrib = design.attributes.itemByName('Fretboard', 'headstockWidth')
            if headstockWidthAttrib:
                headstockWidth = headstockWidthAttrib.value
                
            headstockThickness = str(0.5625 * 2.54)
            headstockThicknessAttrib = design.attributes.itemByName('Fretboard', 'headstockThickness')
            if headstockThicknessAttrib:
                headstockThickness = headstockThicknessAttrib.value

            firstFretThickness = str(0.8 * 2.54)
            firstFretThicknessAttrib = design.attributes.itemByName('Fretboard', 'firstFretThickness')
            if firstFretThicknessAttrib:
                firstFretThickness = firstFretThicknessAttrib.value

            twelfthFretThickness = str(0.85 * 2.54)
            twelfthFretThicknessAttrib = design.attributes.itemByName('Fretboard', 'twelfthFretThickness')
            if twelfthFretThicknessAttrib:
                twelfthFretThickness = twelfthFretThicknessAttrib.value
                
            bridgeStringSpacing = str(2.08 * 2.54)
            bridgeStringSpacingAttrib = design.attributes.itemByName('Fretboard', 'bridgeStringSpacing')
            if bridgeStringSpacingAttrib:
                bridgeStringSpacing = bridgeStringSpacingAttrib.value                

            nutStringSpacing = str(1.388 * 2.54)
            nutStringSpacingAttrib = design.attributes.itemByName('Fretboard', 'nutStringSpacing')
            if nutStringSpacingAttrib:
                nutStringSpacing = nutStringSpacingAttrib.value     
                
            nutToPost = str(1.5 * 2.54)
            nutToPostAttrib = design.attributes.itemByName('Fretboard', 'nutToPost')
            if nutToPostAttrib:
                nutToPost = nutToPostAttrib.value    

            stringCount = '6'
            stringCountAttrib = design.attributes.itemByName('Fretboard', 'stringCount')
            if stringCountAttrib:
                stringCount = stringCountAttrib.value
                
            machinePostHoleDiameter = str(0.4 * 2.54)
            machinePostHoleDiameterAttrib = design.attributes.itemByName('Fretboard', 'machinePostHoleDiameter')
            if machinePostHoleDiameterAttrib:
                machinePostHoleDiameter = machinePostHoleDiameterAttrib.value 

            machinePostDiameter = str(0.2 * 2.54)
            machinePostDiameterAttrib = design.attributes.itemByName('Fretboard', 'machinePostDiameter')
            if machinePostDiameterAttrib:
                machinePostDiameter = machinePostDiameterAttrib.value

            machinePostHoleSpacing = str(1 * 2.54)
            machinePostHoleSpacingAttrib = design.attributes.itemByName('Fretboard', 'machinePostHoleSpacing')
            if machinePostHoleSpacingAttrib:
                machinePostHoleSpacing = machinePostHoleSpacingAttrib.value


            global defaultStandard, defaultFretNumber, defaultScaleLength, defaultNutLength, defaultEndLength, createFlatFretboard, defaultNutRadius, defaultEndRadius, defaultHeight, \
                createFilletRadius, defaultFilletRadius, createEndCurve, defaultEndCurve, createFretCuts, defaultTangWidth, defaultTangDepth, defaultCrownWidth, defaultCrownHeight, \
                createBlindFrets, defaultBlindFrets, defaultNutSlotWidth, defaultNutSlotDepth, createFretMakers, defaultMarkerDiameter, defaultMarkerDepth, defaultMarkerSpacing, \
                defaultFretboardLength, defaultGuitarLength, defaultGuitarWidth, defaultGuitarThickness, defaultBodyLength, defaultNeckLength, defaultNeckWidth, defaultNeckThickness, \
                defaultHeadstockLength, defaultHeadstockWidth, defaultHeadstockThickness, defaultFirstFretThickness, defaultTwelfthFretThickness, defaultBridgeStringSpacing, \
                defaultNutStringSpacing, defaultNutToPost, defaultMachinePostHoleDiameter, defaultMachinePostDiameter, defaultMachinePostHoleSpacing, defaultStringCount, errorMessage, \
                createPreview, defaultFirstFretHeight, defaultTwelfthFretHeight 
              
            cmd = eventArgs.command
            cmd.isExecutedWhenPreEmpted = False
            inputs = cmd.commandInputs
            cmd.helpFile = 'help.html'
            cmd.okButtonText = 'Create Fretboard'
#
#            # Set the size of the dialog.
#            cmd.setDialogInitialSize(180, 800)
#            cmd.setDialogMinimumSize(180, 800)
            cmd.okButtonText = 'Create Guitar'

            # Create a tab input.
            tabCmdInput1 = inputs.addTabCommandInput('general', 'General')
            tab1ChildInputs = tabCmdInput1.children

            # Create a tab input.
            tabCmdInput2 = inputs.addTabCommandInput('fretboard', 'Fretboard')
            tab2ChildInputs = tabCmdInput2.children

            imgInput = tab1ChildInputs.addImageCommandInput('fretboardImage', '', 'Resources/guitarEngine.png')
            imgInput.isFullWidth = True

            defaultStandard = tab1ChildInputs.addDropDownCommandInput('standard', 'Standard', adsk.core.DropDownStyles.TextListDropDownStyle)
            defaultStandard.tooltip = 'This will set your values to either metric or imperial.'
            if standard == "English":
                defaultStandard.listItems.add('English', True)
                defaultStandard.listItems.add('Metric', False)
            else:
                defaultStandard.listItems.add('English', False)
                defaultStandard.listItems.add('Metric', True)

            defaultFretNumber = tab1ChildInputs.addStringValueInput('fretNumber', 'Number of frets', fretNumber)
            defaultFretNumber.tooltip = 'Input the number frets for your fretboard.'
            defaultFretNumber.tooltipDescription = 'This will only validate values between 10 and 36.'
            
            defaultScaleLength = tab1ChildInputs.addValueInput('scaleLength', 'Scale Length', units, adsk.core.ValueInput.createByReal(float(scaleLength)))
            defaultScaleLength.tooltip = 'This is the distance between the nut and the bridge.'

            errorMessage = tab1ChildInputs.addTextBoxCommandInput('errorMessage', '', '', 2, True)
            errorMessage.isFullWidth = True
            
            
            defaultGuitarLength = tab1ChildInputs.addValueInput('guitarLength', 'Guitar Length', units, adsk.core.ValueInput.createByReal(float(guitarLength)))
            
            defaultGuitarWidth = tab1ChildInputs.addValueInput('guitarWidth', 'Guitar Width', units, adsk.core.ValueInput.createByReal(float(guitarWidth)))
            
            defaultBodyLength = tab1ChildInputs.addValueInput('bodyLength', 'Body Length', units, adsk.core.ValueInput.createByReal(float(bodyLength)))
            
            defaultHeadstockLength = tab1ChildInputs.addValueInput('headstockLength', 'Headstock Length', units, adsk.core.ValueInput.createByReal(float(headstockLength)))
                        
            defaultStringCount = tab1ChildInputs.addStringValueInput('stringCount', 'Number of Strings', stringCount)
            defaultStringCount.tooltip = 'Input the number strings for your guitar.'
            defaultStringCount.tooltipDescription = '   '
            
            defaultFirstFretHeight = tab1ChildInputs.addValueInput('firstFretHeight', 'First Fret Height', units, adsk.core.ValueInput.createByReal(float(firstFretHeight)))

            defaultTwelfthFretHeight = tab1ChildInputs.addValueInput('twelfthFretHeight', 'Twelfth Fret Height', units, adsk.core.ValueInput.createByReal(float(twelfthFretHeight)))
            
            defaultBridgeStringSpacing = tab1ChildInputs.addValueInput('bridgeStringSpacing', 'Bridge String Spacing', units, adsk.core.ValueInput.createByReal(float(bridgeStringSpacing)))
            
            defaultNutStringSpacing = tab1ChildInputs.addValueInput('nutStringSpacing', 'Nut String Spacing', units, adsk.core.ValueInput.createByReal(float(nutStringSpacing)))
            
            defaultNutToPost = tab1ChildInputs.addValueInput('nutToPost', 'Nut To Post', units, adsk.core.ValueInput.createByReal(float(nutToPost)))
            
            defaultMachinePostHoleDiameter = tab1ChildInputs.addValueInput('machinePostHoleDiameter', 'Machine Post Hole Diameter', units, adsk.core.ValueInput.createByReal(float(machinePostHoleDiameter)))

            defaultMachinePostDiameter = tab1ChildInputs.addValueInput('machinePostDiameter', 'Machine Post Diameter', units, adsk.core.ValueInput.createByReal(float(machinePostDiameter)))            

            defaultMachinePostHoleSpacing = tab1ChildInputs.addValueInput('machinePostHoleSpacing', 'Machine Post Hole Spacing', units, adsk.core.ValueInput.createByReal(float(machinePostHoleSpacing)))

#            message = '<div align="center"><hr></a></div>'
#            tab1ChildInputs.addTextBoxCommandInput('fullWidth_textBox', '', message, 1, True)             
            
            # Create group input.
            groupCmdInput1 = tab2ChildInputs.addGroupCommandInput('fretboard', 'Fretboard')
            groupCmdInput1.isExpanded = True
            groupCmdInput1.isEnabledCheckBoxDisplayed = False
            groupChildInputs1 = groupCmdInput1.children      

            defaultFretboardLength = groupChildInputs1.addValueInput('fretboardLength', 'Fretboard Length', units, adsk.core.ValueInput.createByReal(float(fretboardLength)))
            defaultFretboardLength.tooltip = 'Tooltip'                        
                        
            defaultNutLength = groupChildInputs1.addValueInput('nutLength', 'Nut Length', units, adsk.core.ValueInput.createByReal(float(nutLength)))
            defaultNutLength.tooltip = 'Tooltip'
            
            defaultEndLength = groupChildInputs1.addValueInput('endLength', 'End Length', units, adsk.core.ValueInput.createByReal(float(endLength)))
            defaultEndLength.tooltip = 'Tooltip'
            
            createFlatFretboard = groupChildInputs1.addBoolValueInput('flatFretboard', 'Create Flat Fretboard?', True, '', False)            
            
            defaultNutRadius = groupChildInputs1.addValueInput('nutRadius', 'Nut Radius', units, adsk.core.ValueInput.createByReal(float(nutRadius)))
            defaultNutRadius.tooltip = 'Tooltip'
            
            defaultEndRadius = groupChildInputs1.addValueInput('endRadius', 'End Radius', units, adsk.core.ValueInput.createByReal(float(endRadius)))
            defaultEndRadius.tooltip = 'Tooltip'
            
            defaultHeight = groupChildInputs1.addValueInput('height', 'Height', units, adsk.core.ValueInput.createByReal(float(height)))
            defaultHeight.tooltip = 'Tooltip'
            
            createFilletRadius = groupChildInputs1.addBoolValueInput('filletRadius', 'Create Fillet Radius?', True, '', True)            
            
            defaultFilletRadius = groupChildInputs1.addValueInput('filletRadius', 'Fillet Radius', units, adsk.core.ValueInput.createByReal(float(filletRadius)))
            defaultFilletRadius.tooltip = 'Tooltip'

            createEndCurve = groupChildInputs1.addBoolValueInput('endCurve', 'Create End Curve?', True, '', True)

            defaultEndCurve = groupChildInputs1.addValueInput('endCurve', 'End Curve', units, adsk.core.ValueInput.createByReal(float(endCurve)))
            defaultEndCurve.tooltip = 'Tooltip'
            
#            # Create a tab input.
#            tabCmdInput3 = inputs.addTabCommandInput('bodyBlanks', 'Body Blanks')
#            tab3ChildInputs = tabCmdInput3.children            
            
            # Create group input.
            groupCmdInput2 = tab2ChildInputs.addGroupCommandInput('fretCuts', 'Fret Cuts')
            groupCmdInput2.isExpanded = False
            groupCmdInput2.isEnabledCheckBoxDisplayed = True
            groupCmdInput2.isEnabledCheckBoxChecked = False
            groupChildInputs2 = groupCmdInput2.children
            
            createFretCuts = groupChildInputs2.addBoolValueInput('fretCuts', 'Create Fret Cuts?', True, '', True)
                        
            defaultTangWidth = groupChildInputs2.addValueInput('tangWidth', 'Tang Width', units,adsk.core.ValueInput.createByReal(float(tangWidth)))
            
            defaultTangDepth = groupChildInputs2.addValueInput('tangDepth', 'Tang Depth', units, adsk.core.ValueInput.createByReal(float(tangDepth)))

            defaultCrownWidth = groupChildInputs2.addValueInput('crownWidth', 'Crown Width', units, adsk.core.ValueInput.createByReal(float(crownWidth)))
            
            defaultCrownHeight = groupChildInputs2.addValueInput('crownHeight', 'Crown Height', units, adsk.core.ValueInput.createByReal(float(crownHeight)))

            createBlindFrets = groupChildInputs2.addBoolValueInput('blindFrets', 'Create Blind Frets?', True, '', False)
            createBlindFrets.tooltip = 'This will create fret cuts that end before the edges of the fretboard'
            if createFretCuts.value:
                createBlindFrets.isEnabled = True
            else:
                createBlindFrets.isEnabled = False

            defaultBlindFrets = groupChildInputs2.addValueInput('blindFrets', 'Blind Frets', units, adsk.core.ValueInput.createByReal(float(blindFrets)))
                
            defaultNutSlotWidth = groupChildInputs2.addValueInput('nutSlotWidth', 'Nut Slot Width', units, adsk.core.ValueInput.createByReal(float(nutSlotWidth)))

            defaultNutSlotDepth = groupChildInputs2.addValueInput('nutSlotDepth', 'Nut Slot Depth', units, adsk.core.ValueInput.createByReal(float(nutSlotDepth)))
            
            # Create group input.
            groupCmdInput3 = tab2ChildInputs.addGroupCommandInput('markerCuts', 'Fret Marker Cuts')
            groupCmdInput3.isExpanded = False
            groupCmdInput3.isEnabledCheckBoxDisplayed = True
            groupCmdInput3.isEnabledCheckBoxChecked = False
            groupChildInputs3 = groupCmdInput3.children

            createFretMakers = groupChildInputs3.addBoolValueInput('fretMarkers', 'Create Fret Markers?', True, '', True)

            defaultMarkerDiameter = groupChildInputs3.addValueInput('markerDiameter', 'Marker Diameter', units, adsk.core.ValueInput.createByReal(float(markerDiameter)))

            defaultMarkerDepth = groupChildInputs3.addValueInput('markerDepth', 'Marker Depth', units, adsk.core.ValueInput.createByReal(float(markerDepth)))
            
            defaultMarkerSpacing = groupChildInputs3.addValueInput('markerSpacing', 'Marker Spacing', units, adsk.core.ValueInput.createByReal(float(markerSpacing)))   
            
            
            # Create a tab input.
            tabCmdInput3 = inputs.addTabCommandInput('pickups', 'Pickups')
            tab3ChildInputs = tabCmdInput3.children
                     
                     
            # Create a tab input.
            tabCmdInput4 = inputs.addTabCommandInput('info', 'Info')
            tab4ChildInputs = tabCmdInput4.children

            message = '<div align="center"><font size="6"><br><b>Guitar Engine</b><br>by Brad Anderson<br><a href="https://www.facebook.com/groups/Fusion360Luthiers/" style="text-decoration: none">Fusion 360 Luthiers Facebook Group.</font></a></div>'
            tab4ChildInputs.addTextBoxCommandInput('fullWidth_textBox', '', message, 10, True)
            
            message = '<div align="center"></a>Please report any issues or concerns to the Facebook Group above.</div>'
            tab4ChildInputs.addTextBoxCommandInput('fullWidth_textBox', '', message, 3, True)
            
            message = '<div align="center"><a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=WP8D4HECT42G8&source=url" style="text-decoration: none">If you would like to support the development of <b>Guitar Engine</b><br> please follow this link. <b><i>Thank you!</b></i></a></div>'
            tab4ChildInputs.addTextBoxCommandInput('fullWidth_textBox', '', message, 3, True)  
            
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
            attribs.add('Fretboard', 'fretNumber', str(defaultFretNumber.value))
            attribs.add('Fretboard', 'scaleLength', str(defaultScaleLength.value))
            attribs.add('Fretboard', 'fretboardLength', str(defaultFretboardLength.value))
            attribs.add('Fretboard', 'nutLength', str(defaultNutLength))
            attribs.add('Fretboard', 'endLength', str(defaultEndLength.value))
            attribs.add('Fretboard', 'nutRadius', str(defaultNutRadius.value))
            attribs.add('Fretboard', 'endRadius', str(defaultEndRadius.value))
            attribs.add('Fretboard', 'height', str(defaultHeight.value))
            attribs.add('Fretboard', 'filletRadius', str(defaultFilletRadius.value))
            attribs.add('Fretboard', 'endCurve', str(defaultEndCurve.value))
            attribs.add('Fretboard', 'tangWidth', str(defaultTangWidth.value))
            attribs.add('Fretboard', 'tangDepth', str(defaultTangDepth.value))
            attribs.add('Fretboard', 'crownWidth', str(defaultCrownWidth.value))
            attribs.add('Fretboard', 'crownHeight', str(defaultCrownHeight.value))
            attribs.add('Fretboard', 'blindFrets', str(defaultBlindFrets.value))
            attribs.add('Fretboard', 'nutSlotWidth', str(defaultNutSlotWidth.value))
            attribs.add('Fretboard', 'markerDiameter', str(defaultMarkerDiameter.value))
            attribs.add('Fretboard', 'markerDepth', str(defaultMarkerDepth.value))
            attribs.add('Fretboard', 'markerSpacing', str(defaultMarkerSpacing.value))

            attribs.add('Fretboard', 'guitarLength', str(defaultGuitarLength.value))
            attribs.add('Fretboard', 'guitarWidth', str(defaultGuitarWidth.value))
            attribs.add('Fretboard', 'bodyLength', str(defaultBodyLength.value))
            attribs.add('Fretboard', 'headstockLength', str(defaultHeadstockLength.value))
            attribs.add('Fretboard', 'firstFretHeight', str(defaultFirstFretHeight.value))            
            attribs.add('Fretboard', 'twelfthFretHeight', str(defaultTwelfthFretHeight.value))            
            attribs.add('Fretboard', 'bridgeStringSpacing', str(defaultBridgeStringSpacing.value))
            attribs.add('Fretboard', 'nutStringSpacing', str(defaultNutStringSpacing.value))
            attribs.add('Fretboard', 'nutToPost', str(defaultNutToPost.value))
            attribs.add('Fretboard', 'machinePostHoleDiameter', str(defaultMachinePostHoleDiameter.value))
            attribs.add('Fretboard', 'machinePostDiameter', str(defaultMachinePostDiameter.value))
            attribs.add('Fretboard', 'machinePostHoleSpacing', str(defaultMachinePostHoleSpacing.value))
            attribs.add('Fretboard', 'stringCount', str(defaultStringCount.value))            
            

            fretNumber = defaultFretNumber.value
            scaleLength = defaultScaleLength.value
            fretboardLength = defaultFretboardLength.value
            nutLength = defaultNutLength.value
            endLength = defaultEndLength.value
            nutRadius = defaultNutRadius.value
            endRadius = defaultEndRadius.value  
            height = defaultHeight.value
            filletRadius = defaultFilletRadius.value
            endCurve = defaultEndCurve.value
            tangWidth = defaultTangWidth.value
            tangDepth = defaultTangDepth.value
            crownWidth = defaultCrownWidth.value            
            crownHeight = defaultCrownHeight.value
            blindFrets = defaultBlindFrets.value
            nutSlotWidth = defaultNutSlotWidth.value
            nutSlotDepth = defaultNutSlotDepth.value
            markerDiameter = defaultMarkerDiameter.value
            markerDepth = defaultMarkerDepth.value
            markerSpacing = defaultMarkerSpacing.value
            guitarLength = defaultGuitarLength.value
            guitarWidth = defaultGuitarWidth.value
            bodyLength = defaultBodyLength.value            
            headstockLength = defaultHeadstockLength.value
            bridgeStringSpacing = defaultBridgeStringSpacing.value
            nutStringSpacing = defaultNutStringSpacing.value
            nutToPost = defaultNutToPost.value
            machinePostHoleDiameter = defaultMachinePostHoleDiameter.value
            machinePostDiameter = defaultMachinePostDiameter.value
            machinePostHoleSpacing = defaultMachinePostHoleSpacing.value
            stringCount = defaultStringCount.value
            firstFretHeight = defaultFirstFretHeight.value
            twelfthFretHeight = defaultTwelfthFretHeight.value

            # Create the fretboard.
            fretboardComp = buildFretboard(design, fretNumber, scaleLength, nutLength, endLength, nutRadius, endRadius, height, filletRadius, endCurve, tangWidth, tangDepth, crownWidth, 
                                           crownHeight, blindFrets, nutSlotWidth, nutSlotDepth, markerDiameter, markerDepth, markerSpacing, guitarLength,
                                           headstockLength, fretboardLength)
            neckComp = buildNeck(design, fretNumber, scaleLength, nutLength, endLength, height, guitarLength, headstockLength, firstFretHeight, twelfthFretHeight)

            # Create the strings.
            stringsComp = buildStrings(design, stringCount, bridgeStringSpacing, nutStringSpacing, guitarLength, headstockLength, scaleLength, nutLength, height, machinePostHoleSpacing,
                                       machinePostHoleDiameter, machinePostDiameter, nutToPost)

            dimsComp = guitarDimensions(design, fretNumber, scaleLength, nutLength, endLength, nutRadius, endRadius, height, filletRadius, endCurve, tangWidth, bridgeStringSpacing, tangDepth,
                                        nutSlotWidth, nutSlotDepth, markerDiameter, markerDepth, markerSpacing, guitarLength, guitarWidth, headstockLength, bodyLength, stringCount, nutToPost,
                                        machinePostHoleSpacing, machinePostHoleDiameter, machinePostDiameter, nutStringSpacing, fretboardLength)
                                        
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

            global units
            if changedInput.id == 'standard':
                if defaultStandard.selectedItem.name == 'English':
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
                
                defaultNutRadius.value = defaultNutRadius.value
                defaultNutRadius.unitType = units
                
                defaultEndRadius.value = defaultEndRadius.value
                defaultEndRadius.unitType = units
                
                defaultHeight.value = defaultHeight.value
                defaultHeight.unitType = units
                
                defaultFilletRadius.value = defaultFilletRadius.value
                defaultFilletRadius.unitType = units
                
                defaultEndCurve.value = defaultEndCurve.value
                defaultEndCurve.unitType = units
                
                defaultTangWidth.value = defaultTangWidth.value
                defaultTangWidth.unitType = units  

                defaultTangDepth.value = defaultTangDepth.value
                defaultTangDepth.unitType = units

                defaultCrownWidth.value = defaultCrownWidth.value
                defaultCrownWidth.unitType = units  
                
                defaultCrownHeight.value = defaultCrownHeight.value
                defaultCrownHeight.unitType = units                  
                
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
                
            # Update
            if not defaultFretNumber.value.isdigit():
                errorMessage.text = 'The number of frets must be a whole number.'
                eventArgs.areInputsValid = False
                return
            else:    
                fretNumber = int(defaultFretNumber.value)
            scaleLength = defaultScaleLength.value               

#            #Equation for fret spacing
#            if defaultFretNumber.value.isdigit(): 
#                for fretNum in range(1,int(fretNumber)+2):
#                    fretDistance = scaleLength-scaleLength/(2**(fretNum/12.0))
#            
#                    #
#                    design = adsk.fusion.Design.cast(app.activeProduct)
#                    fretboardLengthText = design.unitsManager.formatInternalValue((fretDistance + (0.25 * 2.54)), units, True)
#                    defaultFretboardLength.text = fretboardLengthText
#
#                if fretNumber < 10:
#                    defaultFretboardLength.text = 'Fret count must be between 10 and 36.'
#                if fretNumber > 36:
#                    defaultFretboardLength.text = 'WHAT ARE YOU DOING?!'
#            else:
#                defaultFretboardLength.text = ''                  

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
        
        # Verify that at lesat 4 teath are specified.
        if not defaultFretNumber.value.isdigit():
            errorMessage.text = 'The number of frets must be a whole number.'
            eventArgs.areInputsValid = False
            return
        else:    
            fretNumber = int(defaultFretNumber.value)
        
        if fretNumber < 10:
            eventArgs.areInputsValid = False
            return
        if fretNumber > 36:
            eventArgs.areInputsValid = False
            return

def buildFretboard(design, fretNumber, scaleLength, nutLength, endLength, nutRadius, endRadius, height, filletRadius, endCurve, tangWidth, tangDepth, crownWidth, crownHeight, blindFrets, 
                   nutSlotWidth, nutSlotDepth, markerDiameter, markerDepth, markerSpacing, guitarLength, headstockLength, fretboardLength):
    try:
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        rootComp = design.rootComponent
        allOccs = rootComp.occurrences
        newOcc = allOccs.addNewComponent(adsk.core.Matrix3D.create())
        fretboardComp = adsk.fusion.Component.cast(newOcc.component)   

        #Equation for fret spacing
        for fretNum in range(1,int((fretNumber))+1):
            fretDistance = (scaleLength)-((scaleLength)/(2**(fretNum/12.0)))
            
        nutDistance = guitarLength - headstockLength
        
        #This calculates and rounds the total length of the fretboard using the scale length and number of frets

        L = fretboardLength 

        print(L/2.54)
        

        #Equation for defining the proper radii
        endR = endRadius-sqrt(endRadius**2-(endLength/2)**2)
        nutR = nutRadius-sqrt(nutRadius**2-(nutLength/2)**2)
        endC = endCurve-sqrt(endCurve**2-(endLength/2)**2)        

        # Points defined for curves
        if createFlatFretboard.value:
            endTopL = adsk.core.Point3D.create((endLength/-2), height, nutDistance+endC-L)
        else:
            endTopL = adsk.core.Point3D.create((endLength/-2), height-endR, nutDistance+endC-L)
        if createFlatFretboard.value:
            endTopC = adsk.core.Point3D.create(0, height, nutDistance-L)
        else:
            endTopC = adsk.core.Point3D.create(0, height, nutDistance-L)
        if createFlatFretboard.value:
            endTopR = adsk.core.Point3D.create((endLength/2), height, nutDistance+endC-L)
        else:
            endTopR = adsk.core.Point3D.create((endLength/2), height-endR, nutDistance+endC-L)
            
        endBotL = adsk.core.Point3D.create((endLength/-2), 0, nutDistance+endC-L)
        endBotC = adsk.core.Point3D.create(0, 0, nutDistance-L)
        endBotR = adsk.core.Point3D.create((endLength/2), 0, nutDistance+endC-L)
                
        nutTopL = adsk.core.Point3D.create((nutLength/-2), height-nutR, nutDistance)
        nutTopC = adsk.core.Point3D.create(0, height, nutDistance)
        nutTopR = adsk.core.Point3D.create((nutLength/2), height-nutR, nutDistance) 
        
        # Create a new sketch.
        sketches = fretboardComp.sketches
        yzPlane = fretboardComp.yZConstructionPlane
        xzPlane = fretboardComp.xZConstructionPlane
        xyPlane = fretboardComp.xYConstructionPlane

        #create curve for bridge-end top arc
        sketch1 = sketches.add(yzPlane)
        sketchArc1 = sketch1.sketchCurves.sketchArcs
        line1 = sketch1.sketchCurves.sketchLines;

        if createEndCurve.value and createFlatFretboard.value:
            path1 =  sketchArc1.addByThreePoints(adsk.core.Point3D.create((endLength/2), height, nutDistance+endC-L), adsk.core.Point3D.create(0, height, nutDistance-L),
                                                adsk.core.Point3D.create((endLength/-2), height, nutDistance+endC-L))                                  
        elif createEndCurve.value:            
            path1 = sketchArc1.addByThreePoints(endTopL, endTopC, endTopR)
            
        else:
            path1 = sketchArc1.addByThreePoints(adsk.core.Point3D.create((endLength/2), height-endR, nutDistance-L), adsk.core.Point3D.create(0, height, nutDistance-L),
                                                adsk.core.Point3D.create((endLength/-2), height-endR, nutDistance-L))  
#        else:
#            path1 = line1.addByTwoPoints(adsk.core.Point3D.create((endLength/2), height, nutDistance-L), adsk.core.Point3D.create((endLength/-2), height, nutDistance-L))
            
        openProfile1 = adsk.fusion.Path.create(path1.createForAssemblyContext(newOcc), adsk.fusion.ChainedCurveOptions.noChainedCurves)
        
        if createEndCurve.value:
            path2 = sketchArc1.addByThreePoints(endBotL, endBotC, endBotR)
        else:
            path2 = line1.addByTwoPoints(adsk.core.Point3D.create((endLength/2), 0, nutDistance-L), adsk.core.Point3D.create((endLength/-2), 0, nutDistance-L))
        openProfile2 = adsk.fusion.Path.create(path2.createForAssemblyContext(newOcc), adsk.fusion.ChainedCurveOptions.noChainedCurves)
        
        if createFlatFretboard.value:
            path3 = line1.addByTwoPoints(adsk.core.Point3D.create((nutLength/2), height, nutDistance), adsk.core.Point3D.create((nutLength/-2), height, nutDistance))
        else:
            path3 = sketchArc1.addByThreePoints(nutTopL, nutTopC, nutTopR)
        openProfile3 = adsk.fusion.Path.create(path3.createForAssemblyContext(newOcc), adsk.fusion.ChainedCurveOptions.noChainedCurves)

        path4 = line1.addByTwoPoints(adsk.core.Point3D.create((nutLength/-2), 0, nutDistance), adsk.core.Point3D.create((nutLength/2), 0, nutDistance))
        openProfile4 = adsk.fusion.Path.create(path4.createForAssemblyContext(newOcc), adsk.fusion.ChainedCurveOptions.noChainedCurves)
        
        line1.addByTwoPoints(path1.startSketchPoint, path3.startSketchPoint) 
        line1.addByTwoPoints(path2.startSketchPoint, path4.endSketchPoint)
        line1.addByTwoPoints(path1.endSketchPoint, path3.endSketchPoint)
        line1.addByTwoPoints(path2.endSketchPoint, path4.startSketchPoint)        
        sketch1.name = 'Fretboard curves'
        sketch1.isVisible = False
        
        #Create sketch for fret lines
        sketch5 = sketches.add(xzPlane)
        frets = sketch5.sketchCurves.sketchLines;
        sketch5.name = 'Fret Lines (Reference)'
        sketch5.isVisible = False
    
        #Create sketch for fret cuts
        sketch6 = sketches.add(xzPlane)
        cuts = sketch6.sketchCurves.sketchLines;
        sketch6.name = 'Fret slots [ ' + str(fretNumber) + ' frets ]'
        sketch6.isVisible = False
        
        #create sketch for nut cut
        sketch7 = sketches.add(xzPlane)
        nutSketch = sketch7.sketchCurves.sketchLines;
        nutSlotsketch = nutSketch.addTwoPointRectangle(adsk.core.Point3D.create(nutDistance, nutLength/2, height),
                                                adsk.core.Point3D.create(nutDistance+nutSlotWidth, -nutLength/2, height))
                                                
        nutProfile = sketch7.profiles.item(0)
        sketch7.name = 'Nut slot profile'
        sketch7.isVisible = False
        
        #create sketch for nut cut
        sketch9 = sketches.add(xzPlane)
        fretMarker = sketch9.sketchCurves.sketchCircles;
        sketch9.name = 'Inlays'
        sketch9.isVisible = False
    
        sketch10 = sketches.add(xzPlane)
        inplayPoints = sketch10.sketchPoints
        sketch10.name = 'Default Marker Positions'
        
        # Create surface for bridge-end of fretboard
        loftFeats = fretboardComp.features.loftFeatures
        loftInput1 = loftFeats.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        loftSections1 = loftInput1.loftSections
        loftSections1.add(openProfile2)
        loftSections1.add(openProfile1)
        loftInput1.isSolid = False

        loft1 = loftFeats.add(loftInput1)
        l1 = loft1.faces[0]

        # Create surface for nut-end of fretboard
        loftInput2 = loftFeats.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        loftSections2 = loftInput2.loftSections
        loftSections2.add(openProfile3)
        loftSections2.add(openProfile4)
        loftInput2.isSolid = False

        loft2 = loftFeats.add(loftInput2)
        l2 = loft2.faces[0]

        # Create new surface using previous surfaces
        loftInput3 = loftFeats.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        loftSections3 = loftInput3.loftSections
        loftSections3.add(l1)
        loftSections3.add(l2)
        loftInput3.isSolid = False

        loft3 = loftFeats.add(loftInput3)
        l3 = loft3.faces[0]

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
        offsetFeatures = fretboardComp.features.offsetFeatures
        offsetInput = offsetFeatures.createInput(inputEntities, adsk.core.ValueInput.createByReal(-tangDepth),
                                                 adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        #Get the surface body.
        extrudeFeature = offsetFeatures.add(offsetInput)
        extrudeFeature.name = 'Offset'
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

        sketch12 = sketches.add(xyPlane)
        sketchArc2 = sketch12.sketchCurves.sketchArcs;
        fretWire = sketch12.sketchCurves.sketchLines;
        sketch12.name = 'Frets ' + ' [' + str(fretNumber) + ']'
        sketch12.isVisible = False

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
                fretLines = frets.addByTwoPoints(adsk.core.Point3D.create((nutDistance-fretDistance), ((fretLength/2)-(blindFrets/2)), height),
                                                 adsk.core.Point3D.create((nutDistance-fretDistance), ((-fretLength/2)+(blindFrets/2)), height))
    
                #Create fret cuts
                cutLines = cuts.addTwoPointRectangle(adsk.core.Point3D.create((nutDistance-fretDistance-(tangWidth/2)), ((-fretLength/2)+(blindFrets/2)), height), 
                                                     adsk.core.Point3D.create((nutDistance-fretDistance+(tangWidth/2)), ((fretLength/2)-(blindFrets/2)), height))
            else:
                #Create fret lines for fret spacing reference            
                fretLines = frets.addByTwoPoints(adsk.core.Point3D.create((nutDistance-fretDistance), ((fretLength/2)+(1)), height),
                                                 adsk.core.Point3D.create((nutDistance-fretDistance), ((-fretLength/2)-(1)), height))
    
                #Create fret cuts
                cutLines = cuts.addTwoPointRectangle(adsk.core.Point3D.create((nutDistance-fretDistance-(tangWidth/2)), ((-fretLength/2)-(1)), height), 
                                                     adsk.core.Point3D.create((nutDistance-fretDistance+(tangWidth/2)), ((fretLength/2)+(1)), height))
    
            # Points defined for curves
            fretCrownL = adsk.core.Point3D.create((nutDistance-fretDistance-(crownWidth/2)), height, 0)
            fretCrownC = adsk.core.Point3D.create(nutDistance-fretDistance, height+crownHeight, 0)
            fretCrownR = adsk.core.Point3D.create((nutDistance-fretDistance+(crownWidth/2)), height, 0)
    
            fretWireArc = sketchArc2.addByThreePoints(fretCrownL, fretCrownC, fretCrownR)
    
            # Draw two connected lines.
            fretWire1 = fretWire.addByTwoPoints(fretCrownL, adsk.core.Point3D.create((nutDistance-fretDistance-(tangWidth/2)), height, 0))
            fretWire2 = fretWire.addByTwoPoints(fretWire1.endSketchPoint, adsk.core.Point3D.create((nutDistance-fretDistance-(tangWidth/2)), height-tangDepth, 0))
            fretWire3 = fretWire.addByTwoPoints(fretWire2.endSketchPoint, adsk.core.Point3D.create((nutDistance-fretDistance+(tangWidth/2)), height-tangDepth, 0))
            fretWire4 = fretWire.addByTwoPoints(fretWire3.endSketchPoint, adsk.core.Point3D.create((nutDistance-fretDistance+(tangWidth/2)), height, 0))
            fretWire5 = fretWire.addByTwoPoints(fretWire4.endSketchPoint, fretCrownR)
            
#            wireFilletR = sketch12.sketchCurves.sketchArcs.addFillet(fretWireArc, fretWireArc.startSketchPoint.geometry, fretWire5, fretWire5.endSketchPoint.geometry, 0.005)            
            
            
#            profs = sketch12.profiles.item(0)
#            
#            paths = adsk.core.ObjectCollection.create()            
#        
#            for path in sketch12.profiles:
#                paths.add(path)
#            
#
#            sweeps = fretboardComp.features.sweepFeatures
#
#            # Create a sweep input
#            sweepInput = sweeps.createInput(profs, paths, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
#            sweep = sweeps.add(sweepInput)

        inlays = [((y-x)/2)+x for x, y in zip(fretSpacing,fretSpacing[1:])]
            
        for inlayOdd in inlays[1:9:2] + inlays[13:21:2]:
            fretMarker.addByCenterRadius(adsk.core.Point3D.create(nutDistance-inlayOdd, 0, height), markerDiameter)
            points = adsk.core.Point3D.create(nutDistance-inlayOdd, 0, height)
            sketch10 = inplayPoints.add(points)
        for inlayOdd in inlays[25:33:2]:
            fretMarker.addByCenterRadius(adsk.core.Point3D.create(nutDistance-inlayOdd, 0, height), markerDiameter/2)
            points = adsk.core.Point3D.create(nutDistance-inlayOdd, 0, height)
            sketch10 = inplayPoints.add(points)
        for inlayEven in inlays[10:24:12]:
            fretMarker.addByCenterRadius(adsk.core.Point3D.create(nutDistance-inlayEven, markerSpacing/2, height), markerDiameter)
            fretMarker.addByCenterRadius(adsk.core.Point3D.create(nutDistance-inlayEven, -markerSpacing/2, height), markerDiameter)
            points = adsk.core.Point3D.create(nutDistance-inlayEven, 0, height)
            sketch10 = inplayPoints.add(points)
        
        fretMarkers = adsk.core.ObjectCollection.create()
        
        for markers in sketch9.profiles:
            fretMarkers.add(markers)
#
        fretboard = stitch.bodies.item(0)
        fretboard.name = 'Fretboard' + ' [ ' + str(fretNumber) + ' frets ]'

        fretboardFaces = [face for face in fretboard.faces]
        if createFilletRadius.value:
            fretboardSurf = fretboardFaces[6::2]
        else:
            fretboardSurf = fretboardFaces[4::2]
#            
        fretCurves = [curve for curve in sketch5.sketchCurves]   
    
        sketch8 = sketches.add(xzPlane)
        fretProj = sketch8.projectToSurface(fretboardSurf, fretCurves, adsk.fusion.SurfaceProjectTypes.AlongVectorSurfaceProjectType,
                                            fretboardComp.yConstructionAxis)
        sketch8.name = 'Fret Lines [ ' + str(fretNumber) + ' frets ]'
        sketch8.isVisible = False

#        
        #Create an object collection to use an input.
        profs = adsk.core.ObjectCollection.create()
    
        #Add all of the profiles to the collection.
        for prof in sketch6.profiles:
            profs.add(prof)
    
        #Get extrude features
        extrudes = fretboardComp.features.extrudeFeatures

        if createFretMakers.value:
            #Extrusion for fret markers            
            markerExtrude = extrudes.addSimple(fretMarkers, adsk.core.ValueInput.createByReal(-markerDepth), adsk.fusion.FeatureOperations.CutFeatureOperation)
            markerExtrude.name = 'Extrusion: Fret Makers'  
            
    
        #Create an extrusion that starts from an entity and goes the specified distance.
        extrudeInput1 = extrudes.createInput(profs, adsk.fusion.FeatureOperations.CutFeatureOperation)
        #Create a distance extent definition
        extent_distance = adsk.fusion.DistanceExtentDefinition.create(distance)
        #Create a start extent that starts from a brep face with an offset of 10 mm.
        start_from = adsk.fusion.FromEntityStartDefinition.create(extendFeature1.faces.item(0), adsk.core.ValueInput.createByReal(0))
        #taperAngle should be 0 because extrude start face is not a planar face in this case
        extrudeInput1.setOneSideExtent(extent_distance, adsk.fusion.ExtentDirections.PositiveExtentDirection)        
        extrudeInput1.startExtent = start_from
    
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
            
#        #Centers the camera to fit the entire fretboard
#        cam = app.activeViewport.camera
#        cam.isFitView = True
#        cam.isSmoothTransition = False
#        app.activeViewport.camera = cam

        # Get a reference to an appearance in the library.
        lib = app.materialLibraries.itemByName('Fusion 360 Appearance Library')
        libAppear1 = lib.appearances.itemByName('Paint - Enamel Glossy (Yellow)')
        libAppear2 = lib.appearances.itemByName('Wax (White)')

        fretboardAppearance1 = fretboardComp.bRepBodies.item(0)
        fretboardAppearance1.appearance = libAppear1
        fretboardAppearance2 = fretboardComp.bRepBodies.item(1)
        fretboardAppearance2.appearance = libAppear1
        offSurf.appearance = libAppear2
        
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
            
            
def buildNeck(design, fretNumber, scaleLength, nutLength, endLength, height, guitarLength, headstockLength, firstFretHeight, twelfthFretHeight):
    try:
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        rootComp = design.rootComponent
        neckOccs = rootComp.occurrences
        neckOcc = neckOccs.addNewComponent(adsk.core.Matrix3D.create())
        neckComp = adsk.fusion.Component.cast(neckOcc.component)
        
        #Equation for fret spacing
        for fretNum in range(1,int((fretNumber))+1):
            fretDistance = (scaleLength)-((scaleLength)/(2**(fretNum/12.0)))
        
        #This calculates and rounds the total length of the fretboard using the scale length and number of frets
        L = round(fretDistance+(0.35 * 2.54), 3)  
        nutDistance = guitarLength - headstockLength        
        
        # Create a new sketch.
        sketches = neckComp.sketches
        yzPlane = neckComp.yZConstructionPlane
        xzPlane = neckComp.xZConstructionPlane
        xyPlane = neckComp.xYConstructionPlane

        #create neck profiles
        sketch1 = sketches.add(yzPlane)
        neckProfiles = sketch1.sketchCurves.sketchLines;

        firstFretDistance = scaleLength-(scaleLength/(2**(1/12.0)))
        firstFretLength = nutLength + 2*sqrt(((firstFretDistance/(math.cos(math.radians(math.acos((L**2+(sqrt((((endLength-nutLength)/2)**2) +(L**2)))**2-
                                ((endLength-nutLength)/2)**2)/(2*L*(sqrt((((endLength-nutLength)/2)**2)+(L**2)))))*((180)/math.pi)))))**2)
                                -(firstFretDistance**2))
        firstFretPoint1 = adsk.core.Point3D.create(firstFretLength/2, 0, (nutDistance-firstFretDistance))
        firstFretPoint2 = adsk.core.Point3D.create(0, height-firstFretHeight, nutDistance-firstFretDistance)
        firstFretPoint3 = adsk.core.Point3D.create(-firstFretLength/2, 0, (nutDistance-firstFretDistance))
        firstFretPoints = adsk.core.ObjectCollection.create()
        firstFretPoints.add(firstFretPoint1)
        firstFretPoints.add(firstFretPoint2)
        firstFretPoints.add(firstFretPoint3)
        firstProfile = sketch1.sketchCurves.sketchFittedSplines.add(firstFretPoints)
        firstFretLine = neckProfiles.addByTwoPoints(firstFretPoint1, firstFretPoint3)
        firstFretTan1 = neckProfiles.addByTwoPoints(firstFretPoint1, adsk.core.Point3D.create(firstFretLength/2, height/2, (nutDistance-firstFretDistance)))
        firstFretTan2 = neckProfiles.addByTwoPoints(firstFretPoint3, adsk.core.Point3D.create(-firstFretLength/2, height/2, (nutDistance-firstFretDistance)))
        sketch1.geometricConstraints.addTangent(firstProfile, firstFretTan1)
        sketch1.geometricConstraints.addTangent(firstProfile, firstFretTan2)
        firstFretProfile = sketch1.profiles.item(0) 
        
        twelfthFretDistance = scaleLength-(scaleLength/(2**(12/12.0)))
        twelfthFretLength = nutLength + 2*sqrt(((twelfthFretDistance/(math.cos(math.radians(math.acos((L**2+(sqrt((((endLength-nutLength)/2)**2) +(L**2)))**2-
                                ((endLength-nutLength)/2)**2)/(2*L*(sqrt((((endLength-nutLength)/2)**2)+(L**2)))))*((180)/math.pi)))))**2)
                                -(twelfthFretDistance**2))            
        twelfthFretPoint1 = adsk.core.Point3D.create(twelfthFretLength/2, 0, (nutDistance-twelfthFretDistance))
        twelfthFretPoint2 = adsk.core.Point3D.create(0, height-twelfthFretHeight, nutDistance-twelfthFretDistance)
        twelfthFretPoint3 = adsk.core.Point3D.create(-twelfthFretLength/2, 0, (nutDistance-twelfthFretDistance))
        twelfthFretPoints = adsk.core.ObjectCollection.create()
        twelfthFretPoints.add(twelfthFretPoint1)
        twelfthFretPoints.add(twelfthFretPoint2)
        twelfthFretPoints.add(twelfthFretPoint3)
        twelfthProfile = sketch1.sketchCurves.sketchFittedSplines.add(twelfthFretPoints)        
        twelfthFretLine = neckProfiles.addByTwoPoints(twelfthFretPoint1, twelfthFretPoint3)  
        twelfthFretTan1 = neckProfiles.addByTwoPoints(twelfthFretPoint1, adsk.core.Point3D.create(twelfthFretLength/2, height/2, (nutDistance-twelfthFretDistance)))
        twelfthFretTan2 = neckProfiles.addByTwoPoints(twelfthFretPoint3, adsk.core.Point3D.create(-twelfthFretLength/2, height/2, (nutDistance-twelfthFretDistance)))
        sketch1.geometricConstraints.addTangent(twelfthProfile, twelfthFretTan1)
        sketch1.geometricConstraints.addTangent(twelfthProfile, twelfthFretTan2)
        sketch1.geometricConstraints.addHorizontalPoints
        twelfthFretProfile = sketch1.profiles.item(0)         
        sketch1.name = 'Neck profiles'
        sketch1.isVisible = False   

        # Create new surface using previous surfaces
        loftFeats = neckComp.features.loftFeatures
        loftInput1 = loftFeats.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        loftSections1 = loftInput1.loftSections
        loftSections1.add(firstFretProfile)
        loftSections1.add(twelfthFretProfile)
        loftInput1.isSolid = True

        neckLoft = loftFeats.add(loftInput1)
        neckLoft.name = 'Neck'
        neck = neckLoft.bodies.item(0)
        neck.name = 'Neck'        

        # Get a reference to an appearance in the library.
        lib = app.materialLibraries.itemByName('Fusion 360 Appearance Library')
        libAppear = lib.appearances.itemByName('Paint - Enamel Glossy (Yellow)')

        neckAppearance = neckComp.bRepBodies.item(0)
        neckAppearance.appearance = libAppear

        # Group everything used to create the fretboard in the timeline.
        timelineGroupsNeck = design.timeline.timelineGroups
        neckOccIndex = neckOcc.timelineObject.index
        neckEndIndex = neckLoft.timelineObject.index
        timelineGroupNeck = timelineGroupsNeck.add(neckOccIndex, neckEndIndex)
        timelineGroupNeck.name = 'Neck'

        neckComp.name = 'Neck'
        return neckComp
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            
def buildStrings(design, stringCount, bridgeStringSpacing, nutStringSpacing, guitarLength, headstockLength, scaleLength, nutLength, height, machinePostHoleSpacing,
                                       machinePostHoleDiameter, machinePostDiameter, nutToPost):
    try:
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        rootComp = design.rootComponent
        stringsOccs = rootComp.occurrences
        stringsOcc = stringsOccs.addNewComponent(adsk.core.Matrix3D.create())
        stringsComp = adsk.fusion.Component.cast(stringsOcc.component)
        
        # Create a new sketch.
        sketches = stringsComp.sketches
        xzPlane = stringsComp.xZConstructionPlane
        
        #Get extrude features
        extrudes = stringsComp.features.extrudeFeatures
        
        stringInset = (nutLength - nutStringSpacing)/2
        nutDistance = guitarLength - headstockLength

        #Create sketch for bridge spacing
        sketch1 = sketches.add(xzPlane)
        sketch1.name = 'Strings [ ' + str((int(stringCount))) + ' strings ]'   
        stringSketch = sketch1.sketchCurves.sketchLines;
        for string in range(int(stringCount)):
            spacing = bridgeStringSpacing/2 - (bridgeStringSpacing/((int(stringCount))-1))*string
            nutSpacing = (nutLength-stringInset*2)/2 - ((nutLength-stringInset*2)/((int(stringCount))-1))*string
            holeSpacingHor = string*machinePostHoleSpacing
            stringsSketch = stringSketch.addByTwoPoints(adsk.core.Point3D.create(nutDistance-scaleLength, spacing, height+0.125), adsk.core.Point3D.create(nutDistance, nutSpacing, height+0.125))
            stringsSketch = stringSketch.addByTwoPoints(adsk.core.Point3D.create(nutDistance, nutSpacing, height+0.125), adsk.core.Point3D.create(nutDistance+nutToPost+holeSpacingHor, nutSpacing, 0))

        #Create sketch for bridge spacing
        sketch2 = sketches.add(xzPlane)
        sketch2.name = 'Machine Post Holes'
        machinePost = sketch2.sketchCurves.sketchCircles;
        for spacing in range(int(stringCount)):
            holeSpacingVert = ((nutLength-stringInset*2)/2 - ((nutLength-stringInset*2)/((int(stringCount))-1))*spacing)
            holeSpacingHor = spacing*machinePostHoleSpacing
            machinePostHoles = machinePost.addByCenterRadius(adsk.core.Point3D.create(nutDistance+nutToPost+holeSpacingHor, holeSpacingVert+machinePostDiameter/2, 0), machinePostHoleDiameter/2)

        #Centers the camera to fit the entire fretboard
        cam = app.activeViewport.camera
        cam.isFitView = True
        cam.isSmoothTransition = False
        app.activeViewport.camera = cam

        # Group everything used to create the fretboard in the timeline.
        timelineGroupsStrings = design.timeline.timelineGroups
        stringsOccIndex = stringsOcc.timelineObject.index
        stringsEndIndex = sketch2.timelineObject.index
        timelineGroupStrings = timelineGroupsStrings.add(stringsOccIndex, stringsEndIndex)
        timelineGroupStrings.name = 'Strings [ ' + str((int(stringCount))) + ' strings ]'

        stringsComp.name = 'Strings [ ' + str((int(stringCount))) + ' strings ]'
        return stringsComp
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            
            
def guitarDimensions(design, fretNumber, scaleLength, nutLength, endLength, nutRadius, endRadius, height, filletRadius, endCurve, tangWidth, bridgeStringSpacing, tangDepth,
                                        nutSlotWidth, nutSlotDepth, markerDiameter, markerDepth, markerSpacing, guitarLength, guitarWidth, headstockLength, bodyLength, stringCount, nutToPost,
                                        machinePostHoleSpacing, machinePostHoleDiameter, machinePostDiameter, nutStringSpacing, fretboardLength):
                         
    try:
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
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
        xzPlane = dimsComp.xZConstructionPlane
        xyPlane = dimsComp.xYConstructionPlane
        
        #Create construction lines
        sketch1 = sketches.add(xzPlane)
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

        originBoundary = lines.addByTwoPoints(adsk.core.Point3D.create(0, guitarWidth/2, 0), adsk.core.Point3D.create(0, -guitarWidth/2, 0))
        originBoundary.isConstruction = True

        endBoundary = lines.addByTwoPoints(adsk.core.Point3D.create(guitarLength, guitarWidth/2, 0), adsk.core.Point3D.create(guitarLength, -guitarWidth/2, 0))
        endBoundary.isConstruction = True
        
        topBoundary = lines.addByTwoPoints(adsk.core.Point3D.create(0, guitarWidth/2, 0), adsk.core.Point3D.create(guitarLength, guitarWidth/2, 0))
        topBoundary.isConstruction = True
        
        bottomBoundary = lines.addByTwoPoints(adsk.core.Point3D.create(0, -guitarWidth/2, 0), adsk.core.Point3D.create(guitarLength, -guitarWidth/2, 0))
        bottomBoundary.isConstruction = True

        bodyBoundary = lines.addByTwoPoints(adsk.core.Point3D.create(bodyLength, guitarWidth/2, 0), adsk.core.Point3D.create(bodyLength, -guitarWidth/2, 0))
        bodyBoundary.isConstruction = True

        nutBoundary = lines.addByTwoPoints(adsk.core.Point3D.create(nutDistance, guitarWidth/4, 0), adsk.core.Point3D.create(nutDistance, -guitarWidth/4, 0))
        nutBoundary.isConstruction = True
        
        bridgeBoundary = lines.addByTwoPoints(adsk.core.Point3D.create(nutDistance-scaleLength, guitarWidth/4, 0), adsk.core.Point3D.create(nutDistance-scaleLength, -guitarWidth/4, 0))
        bridgeBoundary.isConstruction = True

        fret12Boundary = lines.addByTwoPoints(adsk.core.Point3D.create(nutDistance-scaleLength/2, guitarWidth/4, 0), adsk.core.Point3D.create(nutDistance-scaleLength/2, -guitarWidth/4, 0))
        fret12Boundary.isConstruction = True
        
        #Create dimension lines
        sketch1.areDimensionsShown = True
        sketch1.sketchDimensions.addDistanceDimension(topBoundary.startSketchPoint, topBoundary.endSketchPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create((topBoundary.length/2), guitarWidth/2+4, 0), False);
                                                     
        sketch1.sketchDimensions.addDistanceDimension(originBoundary.startSketchPoint, originBoundary.endSketchPoint,
                                                     adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                     adsk.core.Point3D.create(-4, 0, 0), False);
                                                     
        sketch1.sketchDimensions.addDistanceDimension(bridgeBoundary.startSketchPoint, fret12Boundary.startSketchPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create((nutDistance-scaleLength+scaleLength/4), guitarWidth/4+2, 0), False);
                                                     
        sketch1.sketchDimensions.addDistanceDimension(fret12Boundary.startSketchPoint, nutBoundary.startSketchPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create((nutDistance-scaleLength/4), guitarWidth/4+2, 0), False);
                                                     
        sketch1.sketchDimensions.addDistanceDimension(topBoundary.startSketchPoint, bodyBoundary.startSketchPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create((bodyLength/2), guitarWidth/2+2, 0), False);
                                                     
        sketch1.sketchDimensions.addDistanceDimension(bodyBoundary.startSketchPoint, topBoundary.endSketchPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create(((guitarLength+bodyLength)/2), guitarWidth/2+2, 0), False);
                                                     
        sketch1.sketchDimensions.addDistanceDimension(topBoundary.startSketchPoint, centerLine.startSketchPoint,
                                                     adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                     adsk.core.Point3D.create(-2, guitarWidth/4, 0), False);
                                                     
        sketch1.sketchDimensions.addDistanceDimension(centerLine.startSketchPoint, bottomBoundary.startSketchPoint,
                                                     adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                     adsk.core.Point3D.create(-2, -guitarWidth/4, 0), False);
                                                     
        sketch1.sketchDimensions.addDistanceDimension(centerLine.startSketchPoint, bridgeBoundary.startSketchPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create(((guitarLength-headstockLength-scaleLength)/2), guitarWidth/4+2, 0), False);
                                                     
        sketch1.sketchDimensions.addDistanceDimension(nutBoundary.startSketchPoint, centerLine.endSketchPoint, 
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create((guitarLength-headstockLength/2), guitarWidth/4+2, 0), False);

        sketch2 = sketches.add(xzPlane)
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
        sketch2.areProfilesShown = True
                
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

#        for dime in range(int(stringCount)):
#            holeSpacingVert = (nutLength-stringInset*2)/2 - ((nutLength-stringInset*2)/(int(stringCount)-1))*dime
#            holeSpacingHor = dime*machinePostHoleSpacing
#            sketchDime10 = sketch2.sketchDimensions.addRadialDimension(dimensionCircles[0+dime], adsk.core.Point3D.create(nutDistance+nutToPost+holeSpacingHor+1, holeSpacingVert+1, 0), False);
#        for dime in range(int(stringCount)):
#            holeSpacingVert = (nutLength-stringInset*2)/2 - ((nutLength-stringInset*2)/(int(stringCount)-1))*dime
#            holeSpacingHor = dime*machinePostHoleSpacing
#            sketchDime1 = sketch2.sketchDimensions.addRadialDimension(dimensionCircles2[0+dime], adsk.core.Point3D.create(nutDistance+nutToPost+holeSpacingHor+1, holeSpacingVert+1, 0), False);  
        

        ###  ALL FOR NECK HUMBUCKER!! 
        
        humbuckerNeck1 = humbuckerCavitySketch.addByTwoPoints(adsk.core.Point3D.create(nutDistance-L-neckHumGap-humbuckerCavityWidth, -humbuckerCavityLength/2, 0),
                                                              adsk.core.Point3D.create(nutDistance-L-neckHumGap-humbuckerCavityWidth, humbuckerCavityLength/2, 0))
        humbuckerNeck1.isConstruction = True
        humbuckerNeck2 = humbuckerCavitySketch.addByTwoPoints(humbuckerNeck1.endSketchPoint, adsk.core.Point3D.create(nutDistance-L-neckHumGap, humbuckerCavityLength/2, 0))
        humbuckerNeck2.isConstruction = True
        humbuckerNeck3 = humbuckerCavitySketch.addByTwoPoints(humbuckerNeck2.endSketchPoint, adsk.core.Point3D.create(nutDistance-L-neckHumGap, -humbuckerCavityLength/2, 0))
        humbuckerNeck3.isConstruction = True
        humbuckerNeck4 = humbuckerCavitySketch.addByTwoPoints(humbuckerNeck3.endSketchPoint, humbuckerNeck1.startSketchPoint)
        humbuckerNeck4.isConstruction = True

        humbuckerNeckFillet1 = sketch2.sketchCurves.sketchArcs.addFillet(humbuckerNeck1, humbuckerNeck1.endSketchPoint.geometry, humbuckerNeck2, humbuckerNeck2.startSketchPoint.geometry, humbuckerCavityFillet)
        humbuckerNeckFillet2 = sketch2.sketchCurves.sketchArcs.addFillet(humbuckerNeck2, humbuckerNeck2.endSketchPoint.geometry, humbuckerNeck3, humbuckerNeck3.startSketchPoint.geometry, humbuckerCavityFillet)
        humbuckerNeckFillet3 = sketch2.sketchCurves.sketchArcs.addFillet(humbuckerNeck3, humbuckerNeck3.endSketchPoint.geometry, humbuckerNeck4, humbuckerNeck4.startSketchPoint.geometry, humbuckerCavityFillet)
        humbuckerNeckFillet4 = sketch2.sketchCurves.sketchArcs.addFillet(humbuckerNeck4, humbuckerNeck4.endSketchPoint.geometry, humbuckerNeck1, humbuckerNeck1.startSketchPoint.geometry, humbuckerCavityFillet)
        
        humbuckerNeckMountTop1 = humbuckerCavitySketch.addByTwoPoints(adsk.core.Point3D.create(nutDistance-L-neckHumGap-humbuckerCavityWidth/2-humbuckerCavityMountWidth/2, -humbuckerCavityLength/2-humbuckerCavityMountLength/2, 0),
                                                                      adsk.core.Point3D.create(nutDistance-L-neckHumGap-humbuckerCavityWidth/2-humbuckerCavityMountWidth/2, -humbuckerCavityLength/2+humbuckerCavityMountLength/2, 0))
        humbuckerNeckMountTop1.isConstruction = True
        
        humbuckerNeckMountTop2 = humbuckerCavitySketch.addByTwoPoints(humbuckerNeckMountTop1.endSketchPoint,
                                                                      adsk.core.Point3D.create(nutDistance-L-neckHumGap-humbuckerCavityWidth/2+humbuckerCavityMountWidth/2, -humbuckerCavityLength/2+humbuckerCavityMountLength/2, 0))
        humbuckerNeckMountTop2.isConstruction = True
        
        humbuckerNeckMountTop3 = humbuckerCavitySketch.addByTwoPoints(humbuckerNeckMountTop2.endSketchPoint,
                                                                      adsk.core.Point3D.create(nutDistance-L-neckHumGap-humbuckerCavityWidth/2+humbuckerCavityMountWidth/2, -humbuckerCavityLength/2-humbuckerCavityMountLength/2, 0))
        humbuckerNeckMountTop3.isConstruction = True
        
        humbuckerNeckMountTop4 = humbuckerCavitySketch.addByTwoPoints(humbuckerNeckMountTop3.endSketchPoint, humbuckerNeckMountTop1.startSketchPoint)
        humbuckerNeckMountTop4.isConstruction = True

        humbuckerNeckMountTopFillet1 = sketch2.sketchCurves.sketchArcs.addFillet(humbuckerNeckMountTop1, humbuckerNeckMountTop1.endSketchPoint.geometry, humbuckerNeckMountTop2, humbuckerNeckMountTop2.startSketchPoint.geometry, humbuckerCavityFillet)
        humbuckerNeckMountTopFillet2 = sketch2.sketchCurves.sketchArcs.addFillet(humbuckerNeckMountTop2, humbuckerNeckMountTop2.endSketchPoint.geometry, humbuckerNeckMountTop3, humbuckerNeckMountTop3.startSketchPoint.geometry, humbuckerCavityFillet)
        humbuckerNeckMountTopFillet3 = sketch2.sketchCurves.sketchArcs.addFillet(humbuckerNeckMountTop3, humbuckerNeckMountTop3.endSketchPoint.geometry, humbuckerNeckMountTop4, humbuckerNeckMountTop4.startSketchPoint.geometry, humbuckerCavityFillet)
        humbuckerNeckMountTopFillet4 = sketch2.sketchCurves.sketchArcs.addFillet(humbuckerNeckMountTop4, humbuckerNeckMountTop4.endSketchPoint.geometry, humbuckerNeckMountTop1, humbuckerNeckMountTop1.startSketchPoint.geometry, humbuckerCavityFillet)

        humbuckerNeckMountBottom1 = humbuckerCavitySketch.addByTwoPoints(adsk.core.Point3D.create(nutDistance-L-neckHumGap-humbuckerCavityWidth/2-humbuckerCavityMountWidth/2, humbuckerCavityLength/2-humbuckerCavityMountLength/2, 0),
                                                                      adsk.core.Point3D.create(nutDistance-L-neckHumGap-humbuckerCavityWidth/2-humbuckerCavityMountWidth/2, humbuckerCavityLength/2+humbuckerCavityMountLength/2, 0))
        humbuckerNeckMountBottom1.isConstruction = True
        
        humbuckerNeckMountBottom2 = humbuckerCavitySketch.addByTwoPoints(humbuckerNeckMountBottom1.endSketchPoint,
                                                                      adsk.core.Point3D.create(nutDistance-L-neckHumGap-humbuckerCavityWidth/2+humbuckerCavityMountWidth/2, humbuckerCavityLength/2+humbuckerCavityMountLength/2, 0))
        humbuckerNeckMountBottom2.isConstruction = True
        
        humbuckerNeckMountBottom3 = humbuckerCavitySketch.addByTwoPoints(humbuckerNeckMountBottom2.endSketchPoint,
                                                                      adsk.core.Point3D.create(nutDistance-L-neckHumGap-humbuckerCavityWidth/2+humbuckerCavityMountWidth/2, humbuckerCavityLength/2-humbuckerCavityMountLength/2, 0))
        humbuckerNeckMountBottom3.isConstruction = True
        
        humbuckerNeckMountBottom4 = humbuckerCavitySketch.addByTwoPoints(humbuckerNeckMountBottom3.endSketchPoint, humbuckerNeckMountBottom1.startSketchPoint)
        humbuckerNeckMountBottom4.isConstruction = True

        humbuckerNeckMountBottomFillet1 = sketch2.sketchCurves.sketchArcs.addFillet(humbuckerNeckMountBottom1, humbuckerNeckMountBottom1.endSketchPoint.geometry, humbuckerNeckMountBottom2, humbuckerNeckMountBottom2.startSketchPoint.geometry, humbuckerCavityFillet)
        humbuckerNeckMountBottomFillet2 = sketch2.sketchCurves.sketchArcs.addFillet(humbuckerNeckMountBottom2, humbuckerNeckMountBottom2.endSketchPoint.geometry, humbuckerNeckMountBottom3, humbuckerNeckMountBottom3.startSketchPoint.geometry, humbuckerCavityFillet)
        humbuckerNeckMountBottomFillet3 = sketch2.sketchCurves.sketchArcs.addFillet(humbuckerNeckMountBottom3, humbuckerNeckMountBottom3.endSketchPoint.geometry, humbuckerNeckMountBottom4, humbuckerNeckMountBottom4.startSketchPoint.geometry, humbuckerCavityFillet)
        humbuckerNeckMountBottomFillet4 = sketch2.sketchCurves.sketchArcs.addFillet(humbuckerNeckMountBottom4, humbuckerNeckMountBottom4.endSketchPoint.geometry, humbuckerNeckMountBottom1, humbuckerNeckMountBottom1.startSketchPoint.geometry, humbuckerCavityFillet)

        ###  ALL FOR BRIDGE HUMBUCKER!! 

        humbuckerBridge1 = humbuckerCavitySketch.addByTwoPoints(adsk.core.Point3D.create(nutDistance-scaleLength+bridgeHumGap, -humbuckerCavityLength/2, 0),
                                                              adsk.core.Point3D.create(nutDistance-scaleLength+bridgeHumGap, humbuckerCavityLength/2, 0))
        humbuckerBridge1.isConstruction = True
        
        humbuckerBridge2 = humbuckerCavitySketch.addByTwoPoints(humbuckerBridge1.endSketchPoint, adsk.core.Point3D.create(nutDistance-scaleLength+bridgeHumGap+humbuckerCavityWidth, humbuckerCavityLength/2, 0))
        humbuckerBridge2.isConstruction = True

        humbuckerBridge3 = humbuckerCavitySketch.addByTwoPoints(humbuckerBridge2.endSketchPoint, adsk.core.Point3D.create(nutDistance-scaleLength+bridgeHumGap+humbuckerCavityWidth, -humbuckerCavityLength/2, 0))
        humbuckerBridge3.isConstruction = True

        humbuckerBridge4 = humbuckerCavitySketch.addByTwoPoints(humbuckerBridge3.endSketchPoint, humbuckerBridge1.startSketchPoint)
        humbuckerBridge4.isConstruction = True

        humbuckerBridgeFillet1 = sketch2.sketchCurves.sketchArcs.addFillet(humbuckerBridge1, humbuckerBridge1.endSketchPoint.geometry, humbuckerBridge2, humbuckerBridge2.startSketchPoint.geometry, humbuckerCavityFillet)
        humbuckerBridgeFillet2 = sketch2.sketchCurves.sketchArcs.addFillet(humbuckerBridge2, humbuckerBridge2.endSketchPoint.geometry, humbuckerBridge3, humbuckerBridge3.startSketchPoint.geometry, humbuckerCavityFillet)
        humbuckerBridgeFillet3 = sketch2.sketchCurves.sketchArcs.addFillet(humbuckerBridge3, humbuckerBridge3.endSketchPoint.geometry, humbuckerBridge4, humbuckerBridge4.startSketchPoint.geometry, humbuckerCavityFillet)
        humbuckerBridgeFillet4 = sketch2.sketchCurves.sketchArcs.addFillet(humbuckerBridge4, humbuckerBridge4.endSketchPoint.geometry, humbuckerBridge1, humbuckerBridge1.startSketchPoint.geometry, humbuckerCavityFillet)

        humbuckerBridgeMountTop1 = humbuckerCavitySketch.addByTwoPoints(adsk.core.Point3D.create(nutDistance-scaleLength+bridgeHumGap+humbuckerCavityWidth/2-humbuckerCavityMountWidth/2, -humbuckerCavityLength/2-humbuckerCavityMountLength/2, 0),
                                                                      adsk.core.Point3D.create(nutDistance-scaleLength+bridgeHumGap+humbuckerCavityWidth/2-humbuckerCavityMountWidth/2, -humbuckerCavityLength/2+humbuckerCavityMountLength/2, 0))
        humbuckerBridgeMountTop1.isConstruction = True
        
        humbuckerBridgeMountTop2 = humbuckerCavitySketch.addByTwoPoints(humbuckerBridgeMountTop1.endSketchPoint,
                                                                      adsk.core.Point3D.create(nutDistance-scaleLength+bridgeHumGap+humbuckerCavityWidth/2+humbuckerCavityMountWidth/2, -humbuckerCavityLength/2+humbuckerCavityMountLength/2, 0))
        humbuckerBridgeMountTop2.isConstruction = True
        
        humbuckerBridgeMountTop3 = humbuckerCavitySketch.addByTwoPoints(humbuckerBridgeMountTop2.endSketchPoint,
                                                                      adsk.core.Point3D.create(nutDistance-scaleLength+bridgeHumGap+humbuckerCavityWidth/2+humbuckerCavityMountWidth/2, -humbuckerCavityLength/2-humbuckerCavityMountLength/2, 0))
        humbuckerBridgeMountTop3.isConstruction = True
        
        humbuckerBridgeMountTop4 = humbuckerCavitySketch.addByTwoPoints(humbuckerBridgeMountTop3.endSketchPoint, humbuckerBridgeMountTop1.startSketchPoint)
        humbuckerBridgeMountTop4.isConstruction = True


        humbuckerBridgeMountTopFillet1 = sketch2.sketchCurves.sketchArcs.addFillet(humbuckerBridgeMountTop1, humbuckerBridgeMountTop1.endSketchPoint.geometry, humbuckerBridgeMountTop2, humbuckerBridgeMountTop2.startSketchPoint.geometry, humbuckerCavityFillet)
        humbuckerBridgeMountTopFillet2 = sketch2.sketchCurves.sketchArcs.addFillet(humbuckerBridgeMountTop2, humbuckerBridgeMountTop2.endSketchPoint.geometry, humbuckerBridgeMountTop3, humbuckerBridgeMountTop3.startSketchPoint.geometry, humbuckerCavityFillet)
        humbuckerBridgeMountTopFillet3 = sketch2.sketchCurves.sketchArcs.addFillet(humbuckerBridgeMountTop3, humbuckerBridgeMountTop3.endSketchPoint.geometry, humbuckerBridgeMountTop4, humbuckerBridgeMountTop4.startSketchPoint.geometry, humbuckerCavityFillet)
        humbuckerBridgeMountTopFillet4 = sketch2.sketchCurves.sketchArcs.addFillet(humbuckerBridgeMountTop4, humbuckerBridgeMountTop4.endSketchPoint.geometry, humbuckerBridgeMountTop1, humbuckerBridgeMountTop1.startSketchPoint.geometry, humbuckerCavityFillet)

        humbuckerBridgeMountBottom1 = humbuckerCavitySketch.addByTwoPoints(adsk.core.Point3D.create(nutDistance-scaleLength+bridgeHumGap+humbuckerCavityWidth/2-humbuckerCavityMountWidth/2, humbuckerCavityLength/2-humbuckerCavityMountLength/2, 0),
                                                                      adsk.core.Point3D.create(nutDistance-scaleLength+bridgeHumGap+humbuckerCavityWidth/2-humbuckerCavityMountWidth/2, humbuckerCavityLength/2+humbuckerCavityMountLength/2, 0))
        humbuckerBridgeMountBottom1.isConstruction = True
        
        humbuckerBridgeMountBottom2 = humbuckerCavitySketch.addByTwoPoints(humbuckerBridgeMountBottom1.endSketchPoint,
                                                                      adsk.core.Point3D.create(nutDistance-scaleLength+bridgeHumGap+humbuckerCavityWidth/2+humbuckerCavityMountWidth/2, humbuckerCavityLength/2+humbuckerCavityMountLength/2, 0))
        humbuckerBridgeMountBottom2.isConstruction = True
        
        humbuckerBridgeMountBottom3 = humbuckerCavitySketch.addByTwoPoints(humbuckerBridgeMountBottom2.endSketchPoint,
                                                                      adsk.core.Point3D.create(nutDistance-scaleLength+bridgeHumGap+humbuckerCavityWidth/2+humbuckerCavityMountWidth/2, humbuckerCavityLength/2-humbuckerCavityMountLength/2, 0))
        humbuckerBridgeMountBottom3.isConstruction = True
        
        humbuckerBridgeMountBottom4 = humbuckerCavitySketch.addByTwoPoints(humbuckerBridgeMountBottom3.endSketchPoint, humbuckerBridgeMountBottom1.startSketchPoint)
        humbuckerBridgeMountBottom4.isConstruction = True

        humbuckerBridgeMountBottomFillet1 = sketch2.sketchCurves.sketchArcs.addFillet(humbuckerBridgeMountBottom1, humbuckerBridgeMountBottom1.endSketchPoint.geometry, humbuckerBridgeMountBottom2, humbuckerBridgeMountBottom2.startSketchPoint.geometry, humbuckerCavityFillet)
        humbuckerBridgeMountBottomFillet2 = sketch2.sketchCurves.sketchArcs.addFillet(humbuckerBridgeMountBottom2, humbuckerBridgeMountBottom2.endSketchPoint.geometry, humbuckerBridgeMountBottom3, humbuckerBridgeMountBottom3.startSketchPoint.geometry, humbuckerCavityFillet)
        humbuckerBridgeMountBottomFillet3 = sketch2.sketchCurves.sketchArcs.addFillet(humbuckerBridgeMountBottom3, humbuckerBridgeMountBottom3.endSketchPoint.geometry, humbuckerBridgeMountBottom4, humbuckerBridgeMountBottom4.startSketchPoint.geometry, humbuckerCavityFillet)
        humbuckerBridgeMountBottomFillet4 = sketch2.sketchCurves.sketchArcs.addFillet(humbuckerBridgeMountBottom4, humbuckerBridgeMountBottom4.endSketchPoint.geometry, humbuckerBridgeMountBottom1, humbuckerBridgeMountBottom1.startSketchPoint.geometry, humbuckerCavityFillet)
        
        humbuckerNeckCenter = humbuckerCavitySketch.addByTwoPoints(adsk.core.Point3D.create(nutDistance-L-neckHumGap-humbuckerCavityWidth/2, -humbuckerCavityLength, 0),
                                                              adsk.core.Point3D.create(nutDistance-L-neckHumGap-humbuckerCavityWidth/2, humbuckerCavityLength, 0))
        humbuckerNeckCenter.isConstruction = True
       
        humbuckerBridgeCenter = humbuckerCavitySketch.addByTwoPoints(adsk.core.Point3D.create(nutDistance-scaleLength+bridgeHumGap+humbuckerCavityWidth/2, -humbuckerCavityLength, 0),
                                                              adsk.core.Point3D.create(nutDistance-scaleLength+bridgeHumGap+humbuckerCavityWidth/2, humbuckerCavityLength, 0))        
        humbuckerBridgeCenter.isConstruction = True
        
        sketchDime12 = sketch2.sketchDimensions.addDistanceDimension(humbuckerNeckCenter.startSketchPoint, humbuckerBridgeCenter.startSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, 
                                                                      adsk.core.Point3D.create(((guitarLength-headstockLength-scaleLength+(1/4*2.54)+humbuckerCavityWidth/2)+(guitarLength-headstockLength-L-(1/4*2.54)-humbuckerCavityWidth/2))/2, -humbuckerCavityLength-2, 0), True);

        # Group everything used to create the fretboard in the timeline.
        timelineGroups2 = design.timeline.timelineGroups
        newOccIndex2 = newOcc2.timelineObject.index
        endIndex2 = sketch2.timelineObject.index
        timelineGroup2 = timelineGroups2.add(newOccIndex2, endIndex2)
        timelineGroup2.name = 'Dimensions'

        dimsComp.name = 'Dimensions'
        return dimsComp
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
