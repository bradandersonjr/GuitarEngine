"""Validate inputs event handler - controls UI field visibility and enabled state."""

from typing import Dict

import adsk.core


class GuitarValidateInputsHandler(adsk.core.ValidateInputsEventHandler):
    def __init__(self, ui_refs: Dict):
        super().__init__()
        self._ui_refs = ui_refs

    def notify(self, args: adsk.core.ValidateInputsEventArgs):
        r = self._ui_refs

        r['error_message'].text = ''

        # Show/hide radius inputs based on fretboard style
        style = r['fretboard_style'].selectedItem.name
        r['radius'].isVisible = (style == 'Straight Radius')
        r['nut_radius'].isVisible = (style == 'Compound Radius')
        r['end_radius'].isVisible = (style == 'Compound Radius')

        # Fret cuts toggles
        fret_cuts_on = r['create_fret_cuts'].value
        r['tang_width'].isEnabled = fret_cuts_on
        r['tang_depth'].isEnabled = fret_cuts_on

        # Fillet radius toggle
        r['fillet_radius_value'].isEnabled = r['create_fillet_radius'].value

        # End curve toggle
        r['end_curve_value'].isEnabled = r['create_end_curve'].value

        # Blind frets toggle
        r['blind_frets_value'].isEnabled = r['create_blind_frets'].value

        # Fret markers toggles
        markers_on = r['create_fret_markers'].value
        r['marker_diameter'].isEnabled = markers_on
        r['marker_depth'].isEnabled = markers_on
        r['marker_spacing'].isEnabled = markers_on

        # Bridge pickup angle only for single-coil
        r['bridge_pickup_angle'].isVisible = (
            r['pickup_bridge'].selectedItem.name == 'Single-Coil'
        )

        # Fretboard-only mode disables blanks and dimensions
        only_fb = r['only_fretboard'].value
        r['create_blanks'].isEnabled = not only_fb
        r['create_dimensions'].isEnabled = not only_fb
