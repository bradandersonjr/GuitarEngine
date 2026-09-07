"""Command created event handler - sets up the dialog UI and wires event handlers."""

import traceback

import adsk.core
import adsk.fusion

from ..config import DEFAULTS
from ..attributes import load_attributes
from ..geometry import fretboard_length_from_frets
from .ui_builder import (
    build_general_tab,
    build_fretboard_tab,
    build_headstock_tab,
    build_pickups_tab,
    build_info_tab,
)
from .execute_handler import GuitarExecuteHandler
from .input_changed import GuitarInputChangedHandler
from .validate_inputs import GuitarValidateInputsHandler


class GuitarCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self, app: adsk.core.Application):
        super().__init__()
        self._app = app
        self._handlers = []

    def notify(self, args: adsk.core.CommandCreatedEventArgs):
        try:
            event_args = adsk.core.CommandCreatedEventArgs.cast(args)
            design = adsk.fusion.Design.cast(self._app.activeProduct)

            if not design:
                self._app.userInterface.messageBox(
                    'A Fusion design must be active when invoking this command.')
                return

            # Determine units
            units = self._resolve_units(design)

            # Load all saved attributes (or defaults)
            values = load_attributes(design, DEFAULTS)

            # Compute fretboard length if not saved
            if not values.get('fretboardLength'):
                fret_number = int(values.get('fretNumber', str(DEFAULTS.fret_number)))
                scale_length = float(values.get('scaleLength',
                                    str(DEFAULTS.scale_length * DEFAULTS.user_unit)))
                values['fretboardLength'] = str(fretboard_length_from_frets(
                    scale_length, fret_number))

            # Configure command
            cmd = event_args.command
            cmd.isExecutedWhenPreEmpted = False
            cmd.helpFile = 'help.html'
            cmd.okButtonText = 'Create Guitar'
            cmd.setDialogInitialSize(275, 800)
            cmd.setDialogMinimumSize(275, 800)

            inputs = cmd.commandInputs
            ui_refs = {}

            # Build all tabs
            build_general_tab(inputs, values, units, ui_refs)
            build_fretboard_tab(inputs, values, units, ui_refs)
            build_headstock_tab(inputs, values, units, ui_refs)
            build_pickups_tab(inputs, values, units, ui_refs)
            build_info_tab(inputs)

            # Wire up event handlers
            on_execute = GuitarExecuteHandler(self._app, ui_refs)
            cmd.execute.add(on_execute)
            self._handlers.append(on_execute)

            on_changed = GuitarInputChangedHandler(self._app, ui_refs)
            cmd.inputChanged.add(on_changed)
            self._handlers.append(on_changed)

            on_validate = GuitarValidateInputsHandler(ui_refs)
            cmd.validateInputs.add(on_validate)
            self._handlers.append(on_validate)

        except Exception:
            ui = self._app.userInterface
            if ui:
                ui.messageBox(f'Failed:\n{traceback.format_exc()}')

    def _resolve_units(self, design: adsk.fusion.Design) -> str:
        """Determine whether to use inches or mm based on design settings."""
        default_units = design.unitsManager.defaultLengthUnits
        units = 'in' if default_units in ('in', 'ft') else 'mm'

        standard_attrib = design.attributes.itemByName('Fretboard', 'standard')
        if standard_attrib:
            units = 'in' if standard_attrib.value == 'Imperial' else 'mm'

        return units
