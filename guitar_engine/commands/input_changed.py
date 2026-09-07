"""Input changed event handler - handles unit switching.

Note: In Fusion 360, you cannot recreate tabs/inputs after the dialog is open.
The unitType property is read-only. However, we can still convert the numeric
values when the standard changes, and the user can close/reopen the dialog to
see the values displayed with the correct unit labels.
"""

import traceback
from typing import Dict

import adsk.core
import adsk.fusion


class GuitarInputChangedHandler(adsk.core.InputChangedEventHandler):
    def __init__(self, app: adsk.core.Application, ui_refs: Dict):
        super().__init__()
        self._app = app
        self._ui_refs = ui_refs

    def notify(self, args: adsk.core.InputChangedEventArgs):
        try:
            event_args = adsk.core.InputChangedEventArgs.cast(args)
            changed = event_args.input

            if changed.id == 'standard':
                # Standard (Imperial/Metric) dropdown changed
                new_standard = self._ui_refs['standard'].selectedItem.name
                new_units = 'in' if new_standard == 'Imperial' else 'mm'

                # Conversion factor: 1 inch = 25.4 mm
                if new_units == 'in':
                    conversion = 1.0 / 25.4  # mm to in
                else:
                    conversion = 25.4  # in to mm

                # Update all length input values in place
                # Note: The display unit labels won't change (they're based on the
                # original unitType), but the values will be converted
                length_inputs = [
                    'scale_length', 'fretboard_length', 'nut_length', 'end_length',
                    'radius', 'nut_radius', 'end_radius', 'fretboard_height',
                    'fillet_radius_value', 'end_curve_value', 'tang_width', 'tang_depth',
                    'blind_frets_value', 'nut_slot_width', 'nut_slot_depth',
                    'marker_diameter', 'marker_depth', 'marker_spacing',
                    'guitar_length', 'body_width', 'body_length', 'body_thickness',
                    'headstock_length', 'first_fret_thickness', 'twelfth_fret_thickness',
                    'headstock_width', 'headstock_thickness',
                    'bridge_string_spacing', 'nut_string_spacing', 'nut_to_post',
                    'machine_post_hole_diameter', 'machine_post_diameter',
                    'machine_post_hole_spacing', 'neck_spacing', 'bridge_spacing',
                    'single_coil_length', 'single_coil_width', 'single_coil_depth',
                    'humbucker_length', 'humbucker_width', 'humbucker_depth',
                    'humbucker_fillet', 'pickup_cavity_mount_length',
                    'pickup_cavity_mount_tab_width', 'neck_thickness',
                ]

                for key in length_inputs:
                    if key in self._ui_refs and hasattr(self._ui_refs[key], 'value'):
                        self._ui_refs[key].value = self._ui_refs[key].value * conversion

        except Exception:
            ui = self._app.userInterface
            if ui:
                ui.messageBox(f'Failed:\n{traceback.format_exc()}')
