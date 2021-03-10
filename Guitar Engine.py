#import system modules
import os, sys 
import adsk.core, adsk.fusion, adsk.cam, traceback

from .GuitarEngineUI import UIElements, UIManager
from .ParameterValues import ParameterValues
from .DesignParameters import DesignParameters
from .Builders import FretboardBuilder, BodyBlankBuilder, StringsBuilder, DimensionsBuilder, PickupsBuilder

handlers = []
commandHandlers = []
parameters: ParameterValues = None
uiManager: UIManager

def run(context):
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        createPanel = ui.allToolbarPanels.itemById('SolidCreatePanel')

        fretboardButton = createPanel.controls.itemById('adskFretboardPythonAddIn2')

        if fretboardButton:
            fretboardButton.deleteMe()

        cmdDef = ui.commandDefinitions.itemById('adskFretboardPythonAddIn2')

        if cmdDef:
            cmdDef.deleteMe()

        # Create a command definition and add a button to the CREATE panel.
        cmdDef = ui.commandDefinitions.addButtonDefinition('adskFretboardPythonAddIn2', 'Guitar Engine', 'Creates a guitar component\n\n', 'Resources/Icons')
        fretboardButton = createPanel.controls.addCommand(cmdDef)

        # Connect to the command created event.
        onCommandCreated = GuitarEngineClickCommandHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        handlers.append(onCommandCreated)

        # Make the button available in the panel.
        fretboardButton.isPromotedByDefault = True
        fretboardButton.isPromoted = True
        if context['IsApplicationStartup'] == False:
            ui.messageBox('<b>Guitar Engine [has been added to the <i>SOLID</i> tab of the <i>DESIGN</i> workspace.')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        createPanel = ui.allToolbarPanels.itemById('SolidCreatePanel')
        fretboardButton = createPanel.controls.itemById('adskFretboardPythonAddIn2')

        if fretboardButton:
            fretboardButton.deleteMe()

        cmdDef = ui.commandDefinitions.itemById('adskFretboardPythonAddIn2')

        if cmdDef:
            cmdDef.deleteMe()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class GuitarEngineClickCommandHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            
            app = adsk.core.Application.get()
            ui  = app.userInterface
            eventArgs = adsk.core.CommandCreatedEventArgs.cast(args)

            # Verify that a Fusion design is active.
            design = adsk.fusion.Design.cast(app.activeProduct)

            if not design:
                ui.messageBox('A Fusion design must be active when invoking this command.')
                return()

            cmd = eventArgs.command
            cmd.isExecutedWhenPreEmpted = False

            cmd.helpFile = 'help.html'
            cmd.setDialogInitialSize(300, 800)
            cmd.setDialogMinimumSize(300, 800)
            cmd.okButtonText = 'Create Guitar'

            global parameters
            
            designParameters = DesignParameters(app)
            designStoredParameters = designParameters.getStoredParameters()

            if (designStoredParameters is not None):
                parameters = designStoredParameters
            else:
                if (parameters is None):
                    parameters = ParameterValues()            

                    defaultUnits = design.unitsManager.defaultLengthUnits

                    # Determine whether to use inches or millimeters as the initial default.
                    if defaultUnits == 'in' or defaultUnits == 'ft':
                        parameters.units = 'in'
                    else:
                        parameters.units = 'mm'
            
            global uiManager
            uiManager = UIManager(app, ui, parameters)

            uiManager.createUIElements(cmd.commandInputs)
            
            onInputChanged = GuitarEngineInputChangedCommandHandler()
            cmd.inputChanged.add(onInputChanged)
            commandHandlers.append(onInputChanged)

            onExecute = GuitarEngineCommandExecuteHandler()
            cmd.execute.add(onExecute)
            commandHandlers.append(onExecute)

            onDestroy = GuitarEngineDestroyHandler()
            cmd.destroy.add(onDestroy)
            commandHandlers.append(onDestroy)

        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class GuitarEngineCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            eventArgs = adsk.core.CommandEventArgs.cast(args)
            app = adsk.core.Application.get()
            ui = app.userInterface            

            designParameters = DesignParameters(app)

            designParameters.setAndStoreParameterValues(parameters)

            fretboardBuilder = FretboardBuilder(app)

            if parameters.generateOnlyFretboard:
                fretboardBuilder.buildFretboard(parameters)
            else:
            
                stepsRequired = self.getStepsRequired()

                progressDialog = ui.createProgressDialog()
                progressDialog.isBackgroundTranslucent = False
                progressDialog.isCancelButtonShown = False
                progressDialog.show('Generating Guitar', 'Generation %p percent complete, completed %v of %m steps', 0, stepsRequired, 1)

                stringsBuilder = StringsBuilder(app)
                pickupsBuilder = PickupsBuilder(app)
                
                fretboardBuilder.buildFretboard(parameters)
                progressDialog.progressValue += 1
                
                if parameters.generateBlanks:
                    bodyBlankBuilder = BodyBlankBuilder(app)
                    blanksComponent = bodyBlankBuilder.buildBodyBlank(parameters)
                    progressDialog.progressValue += 1

                # Create the strings.
                stringsComponent = stringsBuilder.buildStrings(parameters)
                progressDialog.progressValue += 1

                # Create the pickup cavities.
                pickupsComponent = pickupsBuilder.buildPickups(parameters)
                progressDialog.progressValue += 1

                # Create dimension sketches
                if parameters.generateDimensions:
                    dimensionsBuilder = DimensionsBuilder(app)
                    dimensionsComponent = dimensionsBuilder.buildDimensions(parameters)
                    progressDialog.progressValue += 1

                progressDialog.hide()
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

    def getStepsRequired(self):
        return 3 + (1 if parameters.generateBlanks else 0) + (1 if parameters.generateDimensions else 0)


class GuitarEngineDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        eventArgs = adsk.core.CommandEventArgs.cast(args)

        commandHandlers.clear()
        uiManager.resetControls()

class GuitarEngineInputChangedCommandHandler(adsk.core.InputChangedEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        eventArgs = adsk.core.InputChangedEventArgs.cast(args)
        
        # Check the value of the check box.
        changedInput = eventArgs.input

        if (changedInput.id == "fretboardStyle"):
            uiManager.onFretboardStyleChanged()
        elif (changedInput.id == "createFretCuts"):
            uiManager.onCreateFretCutsChanged()
        elif (changedInput.id == 'createFilletRadius'):
            uiManager.onCreateFilletRadiusChanged()
        elif (changedInput.id == 'createEndCurve'):
            uiManager.onCreateEndCurveChanged()
        elif (changedInput.id == 'createBlindFrets'):
            uiManager.onCreateBlindFretsChanged()
        elif (changedInput.id == 'createFretMarkers'):
            uiManager.onCreateFretMarkersChanged()
        elif (changedInput.id == 'pickupBridge'):
            uiManager.onPickupBridgeChanged()
        elif (changedInput.id == 'generateOnlyFretboard'):
            uiManager.onGenerateOnlyFretboardChanged()            
        else:
            pass