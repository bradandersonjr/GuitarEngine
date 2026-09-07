"""Execute event handler - extracts params from UI, saves attributes, and runs builders."""

import traceback
from typing import Dict

import adsk.core
import adsk.fusion

from ..parameters import (
    FretboardParams, BlanksParams, StringsParams, PickupsParams,
    DimensionsParams, UserParams, BuildOptions,
    FretboardStyle, HeadstockStyle, PickupType,
)
from ..attributes import save_attributes
from ..builders.fretboard import build_fretboard
from ..builders.blanks import build_blanks
from ..builders.strings import build_strings
from ..builders.pickups import build_pickups
from ..builders.dimensions import build_dimensions
from ..builders.user_parameters import build_user_parameters


class GuitarExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self, app: adsk.core.Application, ui_refs: Dict):
        super().__init__()
        self._app = app
        self._ui_refs = ui_refs

    def notify(self, args: adsk.core.CommandEventArgs):
        try:
            design = adsk.fusion.Design.cast(self._app.activeProduct)
            r = self._ui_refs

            # Save all values as design attributes for persistence
            self._save_all_attributes(design)

            # Extract enum values
            fretboard_style = FretboardStyle(r['fretboard_style'].selectedItem.name)
            headstock_style = HeadstockStyle(r['headstock_style'].selectedItem.name)
            pickup_neck = PickupType(r['pickup_neck'].selectedItem.name)
            pickup_middle = PickupType(r['pickup_middle'].selectedItem.name)
            pickup_bridge = PickupType(r['pickup_bridge'].selectedItem.name)

            # Build options
            options = BuildOptions(
                only_fretboard=r['only_fretboard'].value,
                create_blanks=r['create_blanks'].value,
                create_dimensions=r['create_dimensions'].value,
            )

            # Fretboard params
            fb_params = FretboardParams(
                fret_number=r['fret_number'].value,
                scale_length=r['scale_length'].value,
                fretboard_length=r['fretboard_length'].value,
                nut_length=r['nut_length'].value,
                end_length=r['end_length'].value,
                fretboard_height=r['fretboard_height'].value,
                fretboard_style=fretboard_style,
                radius=r['radius'].value,
                nut_radius=r['nut_radius'].value,
                end_radius=r['end_radius'].value,
                fillet_radius=r['fillet_radius_value'].value,
                end_curve=r['end_curve_value'].value,
                tang_width=r['tang_width'].value,
                tang_depth=r['tang_depth'].value,
                blind_frets=r['blind_frets_value'].value,
                nut_slot_width=r['nut_slot_width'].value,
                nut_slot_depth=r['nut_slot_depth'].value,
                marker_diameter=r['marker_diameter'].value,
                marker_depth=r['marker_depth'].value,
                marker_spacing=r['marker_spacing'].value,
                guitar_length=r['guitar_length'].value,
                headstock_length=r['headstock_length'].value,
                first_fret_thickness=r['first_fret_thickness'].value,
                twelfth_fret_thickness=r['twelfth_fret_thickness'].value,
                neck_thickness=r['neck_thickness'].value,
                headstock_width=r['headstock_width'].value,
                headstock_thickness=r['headstock_thickness'].value,
                create_fret_cuts=r['create_fret_cuts'].value,
                create_blind_frets=r['create_blind_frets'].value,
                create_fret_markers=r['create_fret_markers'].value,
                create_fillet_radius=r['create_fillet_radius'].value,
                create_end_curve=r['create_end_curve'].value,
                extension_visible=r['extension_visible'].value,
            )

            # Always build fretboard
            build_fretboard(self._app, design, fb_params)

            if not options.only_fretboard:
                # Blanks
                blanks_params = BlanksParams(
                    body_length=r['body_length'].value,
                    body_width=r['body_width'].value,
                    body_thickness=r['body_thickness'].value,
                    headstock_length=r['headstock_length'].value,
                    headstock_width=r['headstock_width'].value,
                    headstock_thickness=r['headstock_thickness'].value,
                    guitar_length=r['guitar_length'].value,
                )
                if options.create_blanks:
                    build_blanks(self._app, design, blanks_params)

                # Strings
                strings_params = StringsParams(
                    string_count=r['string_count'].value,
                    bridge_string_spacing=r['bridge_string_spacing'].value,
                    nut_string_spacing=r['nut_string_spacing'].value,
                    guitar_length=r['guitar_length'].value,
                    headstock_length=r['headstock_length'].value,
                    scale_length=r['scale_length'].value,
                    nut_length=r['nut_length'].value,
                    fretboard_height=r['fretboard_height'].value,
                    machine_post_hole_spacing=r['machine_post_hole_spacing'].value,
                    machine_post_hole_diameter=r['machine_post_hole_diameter'].value,
                    machine_post_diameter=r['machine_post_diameter'].value,
                    nut_to_post=r['nut_to_post'].value,
                    headstock_style=headstock_style,
                    headstock_thickness=r['headstock_thickness'].value,
                    create_blanks=options.create_blanks,
                )
                build_strings(self._app, design, strings_params)

                # Pickups
                pickups_params = PickupsParams(
                    guitar_length=r['guitar_length'].value,
                    headstock_length=r['headstock_length'].value,
                    scale_length=r['scale_length'].value,
                    fretboard_length=r['fretboard_length'].value,
                    neck_spacing=r['neck_spacing'].value,
                    bridge_spacing=r['bridge_spacing'].value,
                    single_coil_length=r['single_coil_length'].value,
                    single_coil_width=r['single_coil_width'].value,
                    single_coil_depth=r['single_coil_depth'].value,
                    humbucker_length=r['humbucker_length'].value,
                    humbucker_width=r['humbucker_width'].value,
                    humbucker_depth=r['humbucker_depth'].value,
                    humbucker_fillet=r['humbucker_fillet'].value,
                    pickup_neck=pickup_neck,
                    pickup_middle=pickup_middle,
                    pickup_bridge=pickup_bridge,
                    pickup_cavity_mount_length=r['pickup_cavity_mount_length'].value,
                    pickup_cavity_mount_tab_width=r['pickup_cavity_mount_tab_width'].value,
                    bridge_pickup_angle=r['bridge_pickup_angle'].value,
                    create_blanks=options.create_blanks,
                )
                build_pickups(self._app, design, pickups_params)

                # Dimensions
                if options.create_dimensions:
                    dims_params = DimensionsParams(
                        fretboard=fb_params,
                        strings=strings_params,
                        pickups=pickups_params,
                        body_width=r['body_width'].value,
                        body_length=r['body_length'].value,
                    )
                    build_dimensions(self._app, design, dims_params)

            # User parameters (always)
            user_params = UserParams(
                fretboard_height=r['fretboard_height'].value,
                headstock_length=r['headstock_length'].value,
                first_fret_thickness=r['first_fret_thickness'].value,
                twelfth_fret_thickness=r['twelfth_fret_thickness'].value,
                neck_thickness=r['neck_thickness'].value,
                headstock_width=r['headstock_width'].value,
                headstock_thickness=r['headstock_thickness'].value,
                machine_post_hole_spacing=r['machine_post_hole_spacing'].value,
                machine_post_hole_diameter=r['machine_post_hole_diameter'].value,
                machine_post_diameter=r['machine_post_diameter'].value,
                nut_to_post=r['nut_to_post'].value,
                body_length=r['body_length'].value,
                body_width=r['body_width'].value,
                body_thickness=r['body_thickness'].value,
            )
            build_user_parameters(self._app, design, user_params)

        except Exception:
            ui = self._app.userInterface
            if ui:
                ui.messageBox(f'Failed:\n{traceback.format_exc()}')

    def _save_all_attributes(self, design: adsk.fusion.Design) -> None:
        """Save all current UI values as design attributes."""
        r = self._ui_refs
        attribs = design.attributes

        # Dropdown attributes
        attribs.add('Fretboard', 'standard', r['standard'].selectedItem.name)
        attribs.add('Fretboard', 'headstockStyle', r['headstock_style'].selectedItem.name)
        attribs.add('Fretboard', 'fretboardStyle', r['fretboard_style'].selectedItem.name)
        attribs.add('pickups', 'pickupNeck', r['pickup_neck'].selectedItem.name)
        attribs.add('pickups', 'pickupMiddle', r['pickup_middle'].selectedItem.name)
        attribs.add('pickups', 'pickupBridge', r['pickup_bridge'].selectedItem.name)

        # Value attributes - map ui_refs key to attribute name
        value_attrs = {
            'fret_number': ('Fretboard', 'fretNumber'),
            'string_count': ('Fretboard', 'stringCount'),
            'scale_length': ('Fretboard', 'scaleLength'),
            'fretboard_length': ('Fretboard', 'fretboardLength'),
            'nut_length': ('Fretboard', 'nutLength'),
            'end_length': ('Fretboard', 'endLength'),
            'radius': ('Fretboard', 'radius'),
            'nut_radius': ('Fretboard', 'nutRadius'),
            'end_radius': ('Fretboard', 'endRadius'),
            'fretboard_height': ('Fretboard', 'fretboardHeight'),
            'fillet_radius_value': ('Fretboard', 'filletRadius'),
            'end_curve_value': ('Fretboard', 'endCurve'),
            'tang_width': ('Fretboard', 'tangWidth'),
            'tang_depth': ('Fretboard', 'tangDepth'),
            'blind_frets_value': ('Fretboard', 'blindFrets'),
            'nut_slot_width': ('Fretboard', 'nutSlotWidth'),
            'nut_slot_depth': ('Fretboard', 'nutSlotDepth'),
            'marker_diameter': ('Fretboard', 'markerDiameter'),
            'marker_depth': ('Fretboard', 'markerDepth'),
            'marker_spacing': ('Fretboard', 'markerSpacing'),
            'guitar_length': ('Fretboard', 'guitarLength'),
            'body_width': ('Fretboard', 'bodyWidth'),
            'body_length': ('Fretboard', 'bodyLength'),
            'body_thickness': ('Fretboard', 'bodyThickness'),
            'headstock_length': ('Fretboard', 'headstockLength'),
            'first_fret_thickness': ('Fretboard', 'firstFretThickness'),
            'twelfth_fret_thickness': ('Fretboard', 'twelfthfretThickness'),
            'bridge_string_spacing': ('Fretboard', 'bridgeStringSpacing'),
            'nut_string_spacing': ('Fretboard', 'nutStringSpacing'),
            'nut_to_post': ('Fretboard', 'nutToPost'),
            'machine_post_hole_diameter': ('Fretboard', 'machinePostHoleDiameter'),
            'machine_post_diameter': ('Fretboard', 'machinePostDiameter'),
            'machine_post_hole_spacing': ('Fretboard', 'machinePostHoleSpacing'),
            'neck_thickness': ('Fretboard', 'neckThickness'),
            'headstock_width': ('Fretboard', 'headstockWidth'),
            'headstock_thickness': ('Fretboard', 'headstockThickness'),
            'neck_spacing': ('Fretboard', 'neckSpacing'),
            'bridge_spacing': ('Fretboard', 'bridgeSpacing'),
            'single_coil_length': ('Fretboard', 'singleCoilLength'),
            'single_coil_width': ('Fretboard', 'singleCoilWidth'),
            'single_coil_depth': ('Fretboard', 'singleCoilDepth'),
            'humbucker_length': ('Fretboard', 'humbuckerLength'),
            'humbucker_width': ('Fretboard', 'humbuckerWidth'),
            'humbucker_depth': ('Fretboard', 'humbuckerDepth'),
            'humbucker_fillet': ('Fretboard', 'humbuckerFillet'),
            'pickup_cavity_mount_length': ('Fretboard', 'pickupCavityMountLength'),
            'pickup_cavity_mount_tab_width': ('Fretboard', 'pickupCavityMountTabWidth'),
            'bridge_pickup_angle': ('Fretboard', 'bridgePickupAngle'),
        }

        for ref_key, (group, attr_name) in value_attrs.items():
            attribs.add(group, attr_name, str(r[ref_key].value))
