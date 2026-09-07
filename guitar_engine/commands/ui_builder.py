"""Functions to build each tab of the Guitar Engine dialog."""

from typing import Dict

import adsk.core

from ..constants import IMAGE_PATH
from ..geometry import fret_position, fretboard_length_from_frets


def build_general_tab(
    inputs: adsk.core.CommandInputs,
    values: Dict[str, str],
    units: str,
    ui_refs: Dict,
) -> None:
    """Build the General tab with core guitar parameters."""
    tab = inputs.addTabCommandInput('general', 'General')
    children = tab.children

    try:
        img = children.addImageCommandInput('fretboardImage', '', IMAGE_PATH)
        img.isFullWidth = True
    except Exception:
        # Image may not load if path is incorrect - continue without it
        pass

    ui_refs['standard'] = _add_dropdown(
        children, 'standard', 'Standard',
        ['Imperial', 'Metric'],
        values.get('standard', 'Imperial'),
    )

    ui_refs['error_message'] = children.addTextBoxCommandInput('errorMessage', '', '', 1, True)
    ui_refs['error_message'].isFullWidth = True

    ui_refs['fret_number'] = children.addIntegerSpinnerCommandInput(
        'fretNumber', 'Number of Frets', 12, 36, 1, int(values['fretNumber']))

    ui_refs['string_count'] = children.addIntegerSpinnerCommandInput(
        'stringCount', 'Number of Strings', 4, 12, 1, int(values['stringCount']))

    ui_refs['scale_length'] = children.addValueInput(
        'scaleLength', 'Scale Length', units,
        adsk.core.ValueInput.createByReal(float(values['scaleLength'])))

    ui_refs['guitar_length'] = children.addValueInput(
        'guitarLength', 'Guitar Length', units,
        adsk.core.ValueInput.createByReal(float(values['guitarLength'])))

    ui_refs['body_length'] = children.addValueInput(
        'bodyLength', 'Body Length', units,
        adsk.core.ValueInput.createByReal(float(values['bodyLength'])))

    ui_refs['body_width'] = children.addValueInput(
        'bodyWidth', 'Body Width', units,
        adsk.core.ValueInput.createByReal(float(values['bodyWidth'])))

    ui_refs['body_thickness'] = children.addValueInput(
        'bodyThickness', 'Body Thickness', units,
        adsk.core.ValueInput.createByReal(float(values['bodyThickness'])))

    ui_refs['neck_thickness'] = children.addValueInput(
        'neckThickness', 'Neck Thickness', units,
        adsk.core.ValueInput.createByReal(float(values['neckThickness'])))

    ui_refs['first_fret_thickness'] = children.addValueInput(
        'firstFretThickness', 'First Fret Thickness', units,
        adsk.core.ValueInput.createByReal(float(values['firstFretThickness'])))

    ui_refs['twelfth_fret_thickness'] = children.addValueInput(
        'twelfthfretThickness', 'Twelfth Fret Thickness', units,
        adsk.core.ValueInput.createByReal(float(values['twelfthfretThickness'])))

    children.addTextBoxCommandInput('fullWidth_textBox', '', '<hr>', 1, True)

    ui_refs['only_fretboard'] = children.addBoolValueInput(
        'onlyFretboard', 'Generate Fretboard Only?', True, '', False)

    ui_refs['create_blanks'] = children.addBoolValueInput(
        'blanks', 'Generate Guitar Blanks?', True, '', True)

    ui_refs['create_dimensions'] = children.addBoolValueInput(
        'dimensions', 'Generate Guitar Dimensions?', True, '', False)


def build_fretboard_tab(
    inputs: adsk.core.CommandInputs,
    values: Dict[str, str],
    units: str,
    ui_refs: Dict,
) -> None:
    """Build the Fretboard tab with surface, fret, and marker settings."""
    tab = inputs.addTabCommandInput('fretboard', 'Fretboard')
    tab_children = tab.children

    # --- Fretboard group ---
    group1 = tab_children.addGroupCommandInput('fretboard', 'Fretboard')
    group1.isExpanded = True
    group1.isEnabledCheckBoxDisplayed = False
    g1 = group1.children

    ui_refs['fretboard_style'] = _add_dropdown(
        g1, 'fretboardStyle', 'Fretboard Style',
        ['Straight Radius', 'Compound Radius', 'Flat/No Radius'],
        values.get('fretboardStyle', 'Straight Radius'),
    )

    ui_refs['radius'] = g1.addValueInput(
        'radius', 'Radius', units,
        adsk.core.ValueInput.createByReal(float(values['radius'])))

    ui_refs['nut_radius'] = g1.addValueInput(
        'nutRadius', 'Nut Radius', units,
        adsk.core.ValueInput.createByReal(float(values['nutRadius'])))

    ui_refs['end_radius'] = g1.addValueInput(
        'endRadius', 'End Radius', units,
        adsk.core.ValueInput.createByReal(float(values['endRadius'])))

    g1.addTextBoxCommandInput('fullWidth_textBox', '', '<hr>', 1, True)

    ui_refs['fretboard_length'] = g1.addValueInput(
        'fretboardLength', 'Fretboard Length', units,
        adsk.core.ValueInput.createByReal(float(values['fretboardLength'])))

    ui_refs['fretboard_height'] = g1.addValueInput(
        'fretboardHeight', 'Fretboard Height', units,
        adsk.core.ValueInput.createByReal(float(values['fretboardHeight'])))

    ui_refs['bridge_string_spacing'] = g1.addValueInput(
        'bridgeStringSpacing', 'Bridge String Spacing', units,
        adsk.core.ValueInput.createByReal(float(values['bridgeStringSpacing'])))

    ui_refs['nut_string_spacing'] = g1.addValueInput(
        'nutStringSpacing', 'Nut String Spacing', units,
        adsk.core.ValueInput.createByReal(float(values['nutStringSpacing'])))

    ui_refs['nut_length'] = g1.addValueInput(
        'nutLength', 'Nut Length', units,
        adsk.core.ValueInput.createByReal(float(values['nutLength'])))

    ui_refs['end_length'] = g1.addValueInput(
        'endLength', 'End Length', units,
        adsk.core.ValueInput.createByReal(float(values['endLength'])))

    ui_refs['nut_slot_width'] = g1.addValueInput(
        'nutSlotWidth', 'Nut Slot Width', units,
        adsk.core.ValueInput.createByReal(float(values['nutSlotWidth'])))

    ui_refs['nut_slot_depth'] = g1.addValueInput(
        'nutSlotDepth', 'Nut Slot Depth', units,
        adsk.core.ValueInput.createByReal(float(values['nutSlotDepth'])))

    ui_refs['create_fillet_radius'] = g1.addBoolValueInput(
        'filletRadius', 'Create Fillet Radius?', True, '', True)

    ui_refs['fillet_radius_value'] = g1.addValueInput(
        'filletRadiusValue', 'Fillet Radius', units,
        adsk.core.ValueInput.createByReal(float(values['filletRadius'])))

    ui_refs['create_end_curve'] = g1.addBoolValueInput(
        'endCurve', 'Create End Curve?', True, '', True)

    ui_refs['end_curve_value'] = g1.addValueInput(
        'endCurveValue', 'End Curve', units,
        adsk.core.ValueInput.createByReal(float(values['endCurve'])))

    ui_refs['extension_visible'] = g1.addBoolValueInput(
        'extensionVisibility', 'Extension Visible?', True, '', True)

    # --- Fret Cuts group ---
    group2 = tab_children.addGroupCommandInput('fretCuts', 'Fret Cuts')
    group2.isExpanded = True
    g2 = group2.children

    ui_refs['create_fret_cuts'] = g2.addBoolValueInput(
        'fretCuts', 'Create Fret Cuts?', True, '', True)

    ui_refs['tang_width'] = g2.addValueInput(
        'tangWidth', 'Tang Width', units,
        adsk.core.ValueInput.createByReal(float(values['tangWidth'])))

    ui_refs['tang_depth'] = g2.addValueInput(
        'tangDepth', 'Tang Depth', units,
        adsk.core.ValueInput.createByReal(float(values['tangDepth'])))

    ui_refs['create_blind_frets'] = g2.addBoolValueInput(
        'blindFrets', 'Create Blind Frets?', True, '', True)

    if ui_refs['create_fret_cuts'].value:
        ui_refs['create_blind_frets'].isEnabled = True
    else:
        ui_refs['create_blind_frets'].isEnabled = False

    ui_refs['blind_frets_value'] = g2.addValueInput(
        'blindFretsValue', 'Blind Fret Inset', units,
        adsk.core.ValueInput.createByReal(float(values['blindFrets'])))

    # --- Fret Markers group ---
    group3 = tab_children.addGroupCommandInput('markerCuts', 'Fret Marker Cuts')
    group3.isExpanded = True
    g3 = group3.children

    ui_refs['create_fret_markers'] = g3.addBoolValueInput(
        'fretMarkers', 'Create Fret Markers?', True, '', True)

    ui_refs['marker_diameter'] = g3.addValueInput(
        'markerDiameter', 'Marker Diameter', units,
        adsk.core.ValueInput.createByReal(float(values['markerDiameter'])))

    ui_refs['marker_depth'] = g3.addValueInput(
        'markerDepth', 'Marker Depth', units,
        adsk.core.ValueInput.createByReal(float(values['markerDepth'])))

    ui_refs['marker_spacing'] = g3.addValueInput(
        'markerSpacing', 'Marker Spacing', units,
        adsk.core.ValueInput.createByReal(float(values['markerSpacing'])))


def build_headstock_tab(
    inputs: adsk.core.CommandInputs,
    values: Dict[str, str],
    units: str,
    ui_refs: Dict,
) -> None:
    """Build the Headstock tab."""
    tab = inputs.addTabCommandInput('headstock', 'Headstock')
    children = tab.children

    ui_refs['headstock_style'] = _add_dropdown(
        children, 'headstockStyle', 'Headstock Style',
        ['Straight In-line', 'Symmetrical'],
        values.get('headstockStyle', 'Straight In-line'),
    )

    children.addTextBoxCommandInput(
        'fullWidth_textBox', '',
        '<div align="center"><b>Notice:</b> Symmetrical only supports 6 strings.</div>',
        1, True,
    )

    ui_refs['headstock_length'] = children.addValueInput(
        'headstockLength', 'Headstock Length', units,
        adsk.core.ValueInput.createByReal(float(values['headstockLength'])))

    ui_refs['headstock_width'] = children.addValueInput(
        'headstockWidth', 'Headstock Width', units,
        adsk.core.ValueInput.createByReal(float(values['headstockWidth'])))

    ui_refs['headstock_thickness'] = children.addValueInput(
        'headstockThickness', 'Headstock Thickness', units,
        adsk.core.ValueInput.createByReal(float(values['headstockThickness'])))

    ui_refs['nut_to_post'] = children.addValueInput(
        'nutToPost', 'Nut To Post', units,
        adsk.core.ValueInput.createByReal(float(values['nutToPost'])))

    ui_refs['machine_post_hole_diameter'] = children.addValueInput(
        'machinePostHoleDiameter', 'Machine Post Hole Diameter', units,
        adsk.core.ValueInput.createByReal(float(values['machinePostHoleDiameter'])))

    ui_refs['machine_post_diameter'] = children.addValueInput(
        'machinePostDiameter', 'Machine Post Diameter', units,
        adsk.core.ValueInput.createByReal(float(values['machinePostDiameter'])))

    ui_refs['machine_post_hole_spacing'] = children.addValueInput(
        'machinePostHoleSpacing', 'Machine Post Hole Spacing', units,
        adsk.core.ValueInput.createByReal(float(values['machinePostHoleSpacing'])))


def build_pickups_tab(
    inputs: adsk.core.CommandInputs,
    values: Dict[str, str],
    units: str,
    ui_refs: Dict,
) -> None:
    """Build the Pickups tab."""
    tab = inputs.addTabCommandInput('pickups', 'Pickups')
    children = tab.children

    ui_refs['pickup_neck'] = _add_dropdown(
        children, 'pickupNeck', 'Neck Pickup',
        ['Single-Coil', 'Humbucker', 'None'],
        values.get('pickupNeck', 'Single-Coil'),
    )

    ui_refs['pickup_middle'] = _add_dropdown(
        children, 'pickupMiddle', 'Middle Pickup',
        ['Single-Coil', 'Humbucker', 'None'],
        values.get('pickupMiddle', 'Single-Coil'),
    )

    ui_refs['pickup_bridge'] = _add_dropdown(
        children, 'pickupBridge', 'Bridge Pickup',
        ['Single-Coil', 'Humbucker'],
        values.get('pickupBridge', 'Single-Coil'),
    )

    ui_refs['bridge_pickup_angle'] = children.addFloatSpinnerCommandInput(
        'bridgePickupAngle', 'Bridge Pickup Angle', 'deg', 0, 20, 1,
        float(values.get('bridgePickupAngle', '10')))

    ui_refs['neck_spacing'] = children.addValueInput(
        'neckSpacing', 'Neck Spacing', units,
        adsk.core.ValueInput.createByReal(float(values['neckSpacing'])))

    ui_refs['bridge_spacing'] = children.addValueInput(
        'bridgeSpacing', 'Bridge Spacing', units,
        adsk.core.ValueInput.createByReal(float(values['bridgeSpacing'])))

    # Single-Coil group
    sc_group = children.addGroupCommandInput('singleCoilGroup', 'Single-Coil')
    sc_group.isExpanded = True
    sc = sc_group.children

    ui_refs['single_coil_length'] = sc.addValueInput(
        'singleCoilLength', 'Single-Coil Length', units,
        adsk.core.ValueInput.createByReal(float(values['singleCoilLength'])))

    ui_refs['single_coil_width'] = sc.addValueInput(
        'singleCoilWidth', 'Single-Coil Width', units,
        adsk.core.ValueInput.createByReal(float(values['singleCoilWidth'])))

    ui_refs['single_coil_depth'] = sc.addValueInput(
        'singleCoilDepth', 'Single-Coil Depth', units,
        adsk.core.ValueInput.createByReal(float(values['singleCoilDepth'])))

    # Humbucker group
    hb_group = children.addGroupCommandInput('humbuckerGroup', 'Humbucker')
    hb_group.isExpanded = True
    hb = hb_group.children

    ui_refs['humbucker_length'] = hb.addValueInput(
        'humbuckerLength', 'Humbucker Length', units,
        adsk.core.ValueInput.createByReal(float(values['humbuckerLength'])))

    ui_refs['humbucker_width'] = hb.addValueInput(
        'humbuckerWidth', 'Humbucker Width', units,
        adsk.core.ValueInput.createByReal(float(values['humbuckerWidth'])))

    ui_refs['humbucker_depth'] = hb.addValueInput(
        'humbuckerDepth', 'Humbucker Depth', units,
        adsk.core.ValueInput.createByReal(float(values['humbuckerDepth'])))

    ui_refs['humbucker_fillet'] = hb.addValueInput(
        'humbuckerFillet', 'Humbucker Corner Radius', units,
        adsk.core.ValueInput.createByReal(float(values['humbuckerFillet'])))

    ui_refs['pickup_cavity_mount_length'] = hb.addValueInput(
        'pickupCavityMountLength', 'Length of pickup cavity', units,
        adsk.core.ValueInput.createByReal(float(values['pickupCavityMountLength'])))

    ui_refs['pickup_cavity_mount_tab_width'] = hb.addValueInput(
        'pickupCavityMountTabWidth', 'Width of pickup cavity rout', units,
        adsk.core.ValueInput.createByReal(float(values['pickupCavityMountTabWidth'])))


def build_info_tab(inputs: adsk.core.CommandInputs) -> None:
    """Build the Info tab with author and support links."""
    tab = inputs.addTabCommandInput('info', 'Info')
    children = tab.children

    children.addTextBoxCommandInput(
        'fullWidth_textBox', '',
        '<div align="center"><font size="6"><br><b>Guitar Engine</b><br>'
        'by Brad Anderson Jr<br><br>'
        '<a href="https://www.facebook.com/groups/Fusion360Luthiers/" '
        'style="text-decoration: none">Fusion 360 Luthiers Facebook Group'
        '</font></a></div>',
        10, True,
    )

    children.addTextBoxCommandInput(
        'fullWidth_textBox', '',
        '<div align="center"><font size="4">Please report any issues to the<br>'
        '<a href="https://github.com/BradAndersonJr/GuitarEngine/" '
        'style="text-decoration: none">Guitar Engine Github Repository'
        '</font></a></div>',
        10, True,
    )

    children.addTextBoxCommandInput(
        'fullWidth_textBox', '',
        '<div align="center"><a href="https://www.paypal.com/cgi-bin/webscr?'
        'cmd=_s-xclick&hosted_button_id=WP8D4HECT42G8&source=url" '
        'style="text-decoration: none">If you would like to support the '
        'development of <b>Guitar Engine</b><br> please follow this link. '
        '<b><i>Thank you!</b></i></a></div>',
        3, True,
    )


def _add_dropdown(
    parent: adsk.core.CommandInputs,
    input_id: str,
    label: str,
    items: list,
    selected_name: str,
) -> adsk.core.DropDownCommandInput:
    """Add a dropdown with the given items, selecting the matching one."""
    dropdown = parent.addDropDownCommandInput(
        input_id, label, adsk.core.DropDownStyles.TextListDropDownStyle,
    )
    for item_name in items:
        dropdown.listItems.add(item_name, item_name == selected_name)
    return dropdown
