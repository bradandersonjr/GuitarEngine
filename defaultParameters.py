"""Backward-compatible wrapper for default parameters.

Users can modify values here and they will be picked up by Guitar Engine.
After making changes, restart the add-in via Scripts and Add-ins window.

The canonical defaults are now in guitar_engine/config.py (GuitarDefaults).
This file provides the legacy defaultParameters class interface.
"""

from .guitar_engine.config import DEFAULTS


class defaultParameters:
    """Default parameter values for Guitar Engine.

    Unit of measure for length values:
      userUnit = 2.54  -> Inches (default)
      userUnit = 0.1   -> Millimeters
      userUnit = 1     -> Centimeters
    """

    userUnit = DEFAULTS.user_unit

    scaleLength = DEFAULTS.scale_length
    fretNumber = DEFAULTS.fret_number
    nutLength = DEFAULTS.nut_length
    endLength = DEFAULTS.end_length
    radius = DEFAULTS.radius
    nutRadius = DEFAULTS.nut_radius
    endRadius = DEFAULTS.end_radius
    fretboardHeight = DEFAULTS.fretboard_height
    filletRadius = DEFAULTS.fillet_radius
    endCurve = DEFAULTS.end_curve
    tangWidth = DEFAULTS.tang_width
    tangDepth = DEFAULTS.tang_depth
    blindFrets = DEFAULTS.blind_frets
    nutSlotWidth = DEFAULTS.nut_slot_width
    nutSlotDepth = DEFAULTS.nut_slot_depth
    markerDiameter = DEFAULTS.marker_diameter
    markerDepth = DEFAULTS.marker_depth
    markerSpacing = DEFAULTS.marker_spacing
    guitarLength = DEFAULTS.guitar_length
    bodyWidth = DEFAULTS.body_width
    bodyThickness = DEFAULTS.body_thickness
    bodyLength = DEFAULTS.body_length
    firstFretThickness = DEFAULTS.first_fret_thickness
    twelfthfretThickness = DEFAULTS.twelfth_fret_thickness
    neckThickness = DEFAULTS.neck_thickness
    headstockLength = DEFAULTS.headstock_length
    headstockWidth = DEFAULTS.headstock_width
    headstockThickness = DEFAULTS.headstock_thickness
    bridgeStringSpacing = DEFAULTS.bridge_string_spacing
    nutStringSpacing = DEFAULTS.nut_string_spacing
    nutToPost = DEFAULTS.nut_to_post
    stringCount = DEFAULTS.string_count
    machinePostHoleDiameter = DEFAULTS.machine_post_hole_diameter
    machinePostDiameter = DEFAULTS.machine_post_diameter
    machinePostHoleSpacing = DEFAULTS.machine_post_hole_spacing
    neckSpacing = DEFAULTS.neck_spacing
    bridgeSpacing = DEFAULTS.bridge_spacing
    singleCoilLength = DEFAULTS.single_coil_length
    singleCoilWidth = DEFAULTS.single_coil_width
    singleCoilDepth = DEFAULTS.single_coil_depth
    humbuckerLength = DEFAULTS.humbucker_length
    humbuckerWidth = DEFAULTS.humbucker_width
    humbuckerDepth = DEFAULTS.humbucker_depth
    humbuckerFillet = DEFAULTS.humbucker_fillet
    pickupCavityMountLength = DEFAULTS.pickup_cavity_mount_length
    pickupCavityMountTabWidth = DEFAULTS.pickup_cavity_mount_tab_width
    bridgePickupAngle = DEFAULTS.bridge_pickup_angle
