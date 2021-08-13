import adsk.core, adsk.fusion, adsk.cam, traceback, math
from math import sqrt
from .ParameterValues import ParameterValues
from .UIElements import UIElements

class UIManager:

    def __init__(self, app, ui, parameters: ParameterValues):
        self.app = app
        self.ui = ui
        self.parameters = parameters

    def createUIElements(self, inputs: adsk.core.CommandInputs):
                
        self.createTabs(inputs)
        self.addGeneralControls()
        self.addFretboardControls()
        self.addHeadstockControls()
        self.addPickupControls()
        self.addInfoControls()
        self.setInitialVisibility()

    def createTabs(self, inputs: adsk.core.CommandInputs):
        UIElements.tabGeneral = inputs.addTabCommandInput('general', 'General')
        UIElements.tabFretboard = inputs.addTabCommandInput('fretboard', 'Fretboard')
        UIElements.tabHeadstock = inputs.addTabCommandInput('headstock', 'Headstock')
        UIElements.tabPickups = inputs.addTabCommandInput('pickups', 'Pickups')
        UIElements.tabInfo = inputs.addTabCommandInput('info', 'Info')

    def addFloatValueControl(self, name: str, description: str, tab: adsk.core.TabCommandInput):
        UIElements.floatValueControls[name] = tab.addValueInput(name, description, self.parameters.units, adsk.core.ValueInput.createByReal(float(getattr(self.parameters, name))))

    def addBoolValueControl(self, name: str, description: str, tab: adsk.core.TabCommandInput):
        UIElements.boolValueControls[name] = tab.addBoolValueInput(name, description, True, '', bool(getattr(self.parameters, name)))

    def addIntSpinnerControl(self, name: str, description: str, min: int, max: int, tab: adsk.core.TabCommandInput):
        UIElements.intSpinnerControls[name] = tab.addIntegerSpinnerCommandInput(name, description, min, max, 1, int(getattr(self.parameters, name)))

    def addFloatSpinnerControl(self, name: str, description: str, type: str, min: float, max: float, step: float, tab: adsk.core.TabCommandInput):
        UIElements.floatSpinnerControls[name] = tab.addFloatSpinnerCommandInput(name, description, type, min, max, step, float(getattr(self.parameters, name)))

    def addDropdownControl(self, name: str, description: str,  tab: adsk.core.TabCommandInput):
        newControl = tab.addDropDownCommandInput(name, description, adsk.core.DropDownStyles.TextListDropDownStyle)
        UIElements.dropdownControls[name] = newControl
        return newControl

    def addGeneralControls(self):

        tabInputs = UIElements.tabGeneral.children

        imgInput = tabInputs.addImageCommandInput('fretboardImage', '', 'Resources/guitarEngine.png')

        self.addIntSpinnerControl('stringCount', 'Number of Strings', 4, 12, tabInputs)
        self.addIntSpinnerControl('fretNumber', 'Number of Frets', 12, 36, tabInputs)
        self.addFloatValueControl('scaleLength', 'Scale Length', tabInputs)
        self.addFloatValueControl('neckPocketLength', 'Neck Pocket Length', tabInputs)
        self.addFloatValueControl('bodyLength', 'Body Length', tabInputs)
        self.addFloatValueControl('bodyWidth', 'Body Width', tabInputs)
        self.addFloatValueControl('bodyThickness', 'Body Thickness', tabInputs)
        self.addFloatValueControl('neckThickness', 'Neck Thickness', tabInputs)
        self.addFloatValueControl('firstFretThickness', 'First Fret Thickness', tabInputs)
        self.addFloatValueControl('twelfthfretThickness', 'Twelfth Fret Thickness', tabInputs)

        tabInputs.addTextBoxCommandInput('fullWidth_textBox', '', "<hr>", 1, True)
        
        self.addBoolValueControl('generateOnlyFretboard', 'Generate Fretboard Only?', tabInputs)
        self.addBoolValueControl('generateBlanks', 'Generate Guitar Blanks?', tabInputs)
        self.addBoolValueControl('generateDimensions', 'Generate Guitar Dimensions?', tabInputs)

    def addFretboardControls(self):        

        tabInputs = UIElements.tabFretboard.children

        fretboardStyle = self.addDropdownControl('fretboardStyle', 'Fretboard Style', tabInputs)
        fretboardStyle.listItems.add('Straight Radius', (self.parameters.fretboardStyle == "Straight Radius"))
        fretboardStyle.listItems.add('Compound Radius', (self.parameters.fretboardStyle == "Compound Radius"))
        fretboardStyle.listItems.add('Flat/No Radius', (self.parameters.fretboardStyle == "Flat/No Radius"))

        self.addFloatValueControl('radius', 'Radius', tabInputs)
        self.addFloatValueControl('nutRadius', 'Nut Radius', tabInputs)
        self.addFloatValueControl('endRadius', 'End Radius', tabInputs)

        tabInputs.addTextBoxCommandInput('fullWidth_textBox', '', "<hr>", 1, True)
        
        #Fretboard length is calculated on change of fret number, we still want to show the value though.
        self.addFloatValueControl('fretboardLength', 'Fretboard Length', tabInputs)
        UIElements.floatValueControls['fretboardLength'].isEnabled = False

        self.addFloatValueControl('fretboardLengthOffset', 'Fretboard Length Offset', tabInputs)        
        self.addFloatValueControl('fretboardHeight', 'Fretboard Height', tabInputs)
        self.addFloatValueControl('bridgeStringSpacing', 'Bridge String Spacing', tabInputs)
        self.addFloatValueControl('nutStringSpacing', 'Nut String Spacing', tabInputs)
        self.addFloatValueControl('nutLength', 'Nut Length', tabInputs)
        self.addFloatValueControl('endLength', 'End Length', tabInputs)
        self.addFloatValueControl('nutSlotWidth', 'Nut Slot Width', tabInputs)
        self.addFloatValueControl('nutSlotDepth', 'Nut Slot Depth', tabInputs)
        self.addBoolValueControl('createFilletRadius', 'Create Fillet Radius?', tabInputs)
        self.addFloatValueControl('filletRadius', 'Fillet Radius', tabInputs)
        self.addBoolValueControl('createEndCurve', 'Create End Curve?', tabInputs)
        self.addFloatValueControl('endCurve', 'End Curve', tabInputs)
        self.addBoolValueControl('extensionVisible', 'Extension Visible?', tabInputs)

        fretCutsGroup = tabInputs.addGroupCommandInput('fretCuts', 'Fret Cuts')
        fretCutsGroup.isExpanded = True
        fretCutsInputs = fretCutsGroup.children

        self.addBoolValueControl('createFretCuts', 'Create Fret Cuts?', fretCutsInputs)
        self.addFloatValueControl('tangWidth', 'Tang Width', fretCutsInputs)
        self.addFloatValueControl('tangDepth', 'Tang Depth', fretCutsInputs)
        self.addBoolValueControl('createBlindFrets', 'Create Blind Frets?', fretCutsInputs)
        self.addFloatValueControl('blindFretInset', 'Blind Fret Inset', fretCutsInputs)

        markerCutsGroup = tabInputs.addGroupCommandInput('markerCuts', 'Fret Marker Cuts')
        markerCutsGroup.isExpanded = True
        markerCutsInputs = markerCutsGroup.children

        self.addBoolValueControl('createFretMarkers', 'Create Fret Markers?', markerCutsInputs)
        self.addFloatValueControl('markerDiameter', 'Marker Diameter', markerCutsInputs)
        self.addFloatValueControl('markerDepth', 'Marker Depth', markerCutsInputs)
        self.addFloatValueControl('markerSpacing', 'Marker Spacing', markerCutsInputs)

    def addHeadstockControls(self):        

        tabInputs = UIElements.tabHeadstock.children

        headstockStyle = self.addDropdownControl('headstockStyle', 'Headstock Style', tabInputs)
        headstockStyle.listItems.add('Straight In-line', (self.parameters.headstockStyle == "Straight In-line"))
        headstockStyle.listItems.add('Symmetrical', (self.parameters.headstockStyle == "Symmetrical"))

        tabInputs.addTextBoxCommandInput('fullWidth_textBox', '', '<div align="center"><b>Notice:</b> Symmetrical only supports 6 strings.</div>', 1, True)

        self.addFloatValueControl('headstockLength', 'Headstock Length', tabInputs)
        self.addFloatValueControl('headstockWidth', 'Headstock Width', tabInputs)
        self.addFloatValueControl('headstockThickness', 'Headstock Thickness', tabInputs)
        self.addFloatValueControl('nutToPost', 'Nut To Post', tabInputs)
        self.addFloatValueControl('machinePostHoleDiameter', 'Machine Post Hole Diameter', tabInputs)
        self.addFloatValueControl('machinePostDiameter', 'Machine Post Diameter', tabInputs)
        self.addFloatValueControl('machinePostHoleSpacing', 'Machine Post Hole Spacing', tabInputs)

    def addPickupControls(self):

        tabInputs = UIElements.tabPickups.children

        pickupNeck = self.addDropdownControl('pickupNeck', 'Neck Pickup', tabInputs)
        pickupNeck.listItems.add('Single-Coil', (self.parameters.pickupNeck == "Single-Coil"))
        pickupNeck.listItems.add('Humbucker', (self.parameters.pickupNeck == "Humbucker"))
        pickupNeck.listItems.add('None', (self.parameters.pickupNeck == "None"))

        pickupMiddle = self.addDropdownControl('pickupMiddle', 'Middle Pickup', tabInputs)
        pickupMiddle.listItems.add('Single-Coil', (self.parameters.pickupMiddle == "Single-Coil"))
        pickupMiddle.listItems.add('Humbucker', (self.parameters.pickupMiddle == "Humbucker"))
        pickupMiddle.listItems.add('None', (self.parameters.pickupMiddle == "None"))

        pickupBridge = self.addDropdownControl('pickupBridge', 'Bridge Pickup', tabInputs)
        pickupBridge.listItems.add('Single-Coil', (self.parameters.pickupBridge == "Single-Coil"))
        pickupBridge.listItems.add('Humbucker', (self.parameters.pickupBridge == "Humbucker"))

        self.addFloatSpinnerControl('bridgePickupAngle', 'Bridge Pickup Angle', 'deg', 0, 20, 1, tabInputs)
        self.addFloatValueControl('neckSpacing', 'Neck Spacing', tabInputs)
        self.addFloatValueControl('bridgeSpacing', 'Bridge Spacing', tabInputs)

        singleCoilGroup = tabInputs.addGroupCommandInput('singleCoilGroup', 'Single-Coil')
        singleCoilGroup.isExpanded = True
        singleCoilGroupInputs = singleCoilGroup.children
        self.addFloatValueControl('singleCoilLength', 'Single-Coil Length', singleCoilGroupInputs)
        self.addFloatValueControl('singleCoilWidth', 'Single-Coil Width', singleCoilGroupInputs)
        self.addFloatValueControl('singleCoilDepth', 'Single-Coil Depth', singleCoilGroupInputs)

        humbuckerGroup = tabInputs.addGroupCommandInput('humbuckerGroup', 'Humbucker')
        humbuckerGroup.isExpanded = True
        humbuckerGroupInputs = humbuckerGroup.children

        self.addFloatValueControl('humbuckerLength', 'Humbucker Length', humbuckerGroupInputs)
        self.addFloatValueControl('humbuckerWidth', 'Humbucker Width', humbuckerGroupInputs)
        self.addFloatValueControl('humbuckerDepth', 'Humbucker Depth', humbuckerGroupInputs)
        self.addFloatValueControl('humbuckerFillet', 'Humbucker Corner Radius', humbuckerGroupInputs)
        self.addFloatValueControl('pickupCavityMountLength', 'Length of pickup cavity', humbuckerGroupInputs)
        self.addFloatValueControl('pickupCavityMountTabWidth', 'Width of pickup cavity rout', humbuckerGroupInputs)

    def addInfoControls(self):
        tabInputs = UIElements.tabInfo.children

        message = '<div align="center"><font size="6"><br><b>Guitar Engine</b><br>by Brad Anderson Jr<br><br><a href="https://www.facebook.com/groups/Fusion360Luthiers/" style="text-decoration: none">Fusion 360 Luthiers Facebook Group</font></a></div>'
        tabInputs.addTextBoxCommandInput('fullWidth_textBox', '', message, 10, True)

        message = '<div align="center"><font size="4">Please report any issues to the<br><a href="https://github.com/BradAndersonJr/GuitarEngine/" style="text-decoration: none">Guitar Engine Github Repository</font></a></div>'
        tabInputs.addTextBoxCommandInput('fullWidth_textBox', '', message, 10, True)

        message = '<div align="center"><a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=WP8D4HECT42G8&source=url" style="text-decoration: none">If you would like to support the development of <b>Guitar Engine</b><br> please follow this link. <b><i>Thank you!</b></i></a></div>'
        tabInputs.addTextBoxCommandInput('fullWidth_textBox', '', message, 3, True)

    def setInitialVisibility(self):

        self.onFretboardStyleChanged()
        self.onCreateFretCutsChanged()
        self.onCreateFilletRadiusChanged()
        self.onCreateEndCurveChanged()
        self.onCreateBlindFretsChanged()
        self.onCreateFretMarkersChanged()
        self.onPickupBridgeChanged()
        self.onGenerateOnlyFretboardChanged()

    def onFretboardStyleChanged(self):
        UIElements.floatValueControls['radius'].isVisible = (UIElements.dropdownControls['fretboardStyle'].selectedItem.name == "Straight Radius")
        UIElements.floatValueControls['nutRadius'].isVisible = (UIElements.dropdownControls['fretboardStyle'].selectedItem.name == "Compound Radius")
        UIElements.floatValueControls['endRadius'].isVisible = (UIElements.dropdownControls['fretboardStyle'].selectedItem.name == "Compound Radius")

    def onCreateFretCutsChanged(self):
        UIElements.floatValueControls['tangWidth'].isEnabled = UIElements.boolValueControls['createFretCuts'].value
        UIElements.floatValueControls['tangDepth'].isEnabled = UIElements.boolValueControls['createFretCuts'].value

    def onCreateFilletRadiusChanged(self):
        UIElements.floatValueControls['filletRadius'].isEnabled = UIElements.boolValueControls['createFilletRadius'].value

    def onCreateEndCurveChanged(self):
        UIElements.floatValueControls['endCurve'].isEnabled = UIElements.boolValueControls['createEndCurve'].value

    def onCreateBlindFretsChanged(self):
        UIElements.floatValueControls['blindFretInset'].isEnabled = UIElements.boolValueControls['createBlindFrets'].value

    def onCreateFretMarkersChanged(self):
        UIElements.floatValueControls['markerDiameter'].isEnabled = UIElements.boolValueControls['createFretMarkers'].value
        UIElements.floatValueControls['markerDepth'].isEnabled = UIElements.boolValueControls['createFretMarkers'].value
        UIElements.floatValueControls['markerSpacing'].isEnabled = UIElements.boolValueControls['createFretMarkers'].value

    def onPickupBridgeChanged(self):        
        UIElements.floatSpinnerControls['bridgePickupAngle'].isVisible = (UIElements.dropdownControls['pickupBridge'].selectedItem.name == "Single-Coil")

    def recalculateFretboardLength(self):
         
        fretCount = UIElements.intSpinnerControls['fretNumber'].value + 1 #Leave a full frets worth of space at the end of the fretboard
        scaleLength = UIElements.floatValueControls['scaleLength'].value

        newFretboardLength = round(scaleLength - (scaleLength/(2**(fretCount/12))), 3) 

        UIElements.floatValueControls['fretboardLength'].value = newFretboardLength

    def onGenerateOnlyFretboardChanged(self):
        if UIElements.boolValueControls['generateOnlyFretboard'].value:
            UIElements.boolValueControls['generateBlanks'].isEnabled = False
            UIElements.boolValueControls['generateBlanks'].value = False
            UIElements.boolValueControls['generateDimensions'].isEnabled = False
            UIElements.boolValueControls['generateDimensions'].value = False
        else:
            UIElements.boolValueControls['generateBlanks'].isEnabled = True
            UIElements.boolValueControls['generateDimensions'].isEnabled = True

    def resetControls(self):
        UIElements.tabGeneral = None
        UIElements.tabFretboard = None
        UIElements.tabHeadstock = None
        UIElements.tabPickups = None
        UIElements.tabInfo = None

        UIElements.floatValueControls = {}
        UIElements.boolValueControls = {}
        UIElements.intSpinnerControls = {}
        UIElements.floatSpinnerControls = {}
        UIElements.dropdownControls = {}