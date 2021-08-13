import adsk.core

class UIElements:

    tabGeneral: adsk.core.TabCommandInput
    tabFretboard: adsk.core.TabCommandInput
    tabHeadstock: adsk.core.TabCommandInput
    tabPickups: adsk.core.TabCommandInput
    tabInfo: adsk.core.TabCommandInput
    
    floatValueControls = {}
    boolValueControls = {}
    intSpinnerControls = {}
    floatSpinnerControls = {}
    dropdownControls = {}