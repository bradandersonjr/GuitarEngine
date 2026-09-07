"""Guitar Engine - generates a parametric guitar component in Fusion.

Builds fretboard, blanks, strings, pickups and dimension geometry from a single
five-tab dialog, so an instrument starts as a fully driven model rather than a
blank sketch. Fret spacing follows equal temperament from the scale length.

Dialog values persist in the design's attributes, so reopening a document
restores the settings it was built with.

Requires Autodesk Fusion (the adsk modules only exist inside Fusion's Python).
"""

__author__ = 'brad anderson jr.'
__copyright__ = 'Copyright (c) 2026 brad anderson jr.'
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = 'brad anderson jr.'
__email__ = 'brad@bradandersonjr.com'
__status__ = 'Production'

import adsk.core
import adsk.fusion
import traceback

from .guitar_engine.constants import ADDIN_ID, ADDIN_NAME, ADDIN_VERSION, PANEL_ID, ICON_PATH
from .guitar_engine.commands.created_handler import GuitarCommandCreatedHandler

app = adsk.core.Application.cast(None)
ui = adsk.core.UserInterface.cast(None)
handlers = []


def run(context):
    try:
        global app, ui
        app = adsk.core.Application.get()
        ui = app.userInterface

        cmd_def = ui.commandDefinitions.addButtonDefinition(
            ADDIN_ID,
            f'{ADDIN_NAME} ({ADDIN_VERSION})',
            'Creates a guitar component\n\n',
            ICON_PATH,
        )

        panel = ui.allToolbarPanels.itemById(PANEL_ID)
        button = panel.controls.addCommand(cmd_def)

        on_created = GuitarCommandCreatedHandler(app)
        cmd_def.commandCreated.add(on_created)
        handlers.append(on_created)

        button.isPromotedByDefault = True
        button.isPromoted = True

        if not context['IsApplicationStartup']:
            ui.messageBox(
                f'<b>{ADDIN_NAME} ({ADDIN_VERSION})</b> has been added to the '
                f'<i>SOLID</i> tab of the <i>DESIGN</i> workspace.'
            )

    except Exception:
        if ui:
            ui.messageBox(f'Failed:\n{traceback.format_exc()}')


def stop(context):
    try:
        panel = ui.allToolbarPanels.itemById(PANEL_ID)
        button = panel.controls.itemById(ADDIN_ID)
        if button:
            button.deleteMe()

        cmd_def = ui.commandDefinitions.itemById(ADDIN_ID)
        if cmd_def:
            cmd_def.deleteMe()
    except Exception:
        if ui:
            ui.messageBox(f'Failed:\n{traceback.format_exc()}')
