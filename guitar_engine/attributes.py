"""Data-driven attribute load/save for design persistence.

Replaces the ~200 lines of repetitive 4-line blocks in the original code
with a single registry that drives both loading and saving.
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Optional

import adsk.fusion

from .config import GuitarDefaults
from .constants import ATTRIBUTE_GROUP_FRETBOARD, ATTRIBUTE_GROUP_PICKUPS


@dataclass
class AttributeDef:
    """Definition of one design attribute."""

    group: str
    name: str
    default_field: str  # field name on GuitarDefaults (snake_case)
    needs_unit_conv: bool = True
    is_int: bool = False
    is_dropdown: bool = False
    dropdown_default: str = ''


# Complete registry of all attributes to persist.
# The 'name' must match the original attribute names exactly for backward compatibility.
ATTRIBUTE_REGISTRY: List[AttributeDef] = [
    # Fretboard group - value parameters
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'fretNumber', 'fret_number',
                 needs_unit_conv=False, is_int=True),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'scaleLength', 'scale_length'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'fretboardLength', '',
                 needs_unit_conv=False),  # computed, no default field
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'nutLength', 'nut_length'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'endLength', 'end_length'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'radius', 'radius'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'nutRadius', 'nut_radius'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'endRadius', 'end_radius'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'fretboardHeight', 'fretboard_height'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'filletRadius', 'fillet_radius'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'endCurve', 'end_curve'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'tangWidth', 'tang_width'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'tangDepth', 'tang_depth'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'blindFrets', 'blind_frets'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'nutSlotWidth', 'nut_slot_width'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'nutSlotDepth', 'nut_slot_depth'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'markerDiameter', 'marker_diameter'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'markerDepth', 'marker_depth'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'markerSpacing', 'marker_spacing'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'guitarLength', 'guitar_length'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'bodyWidth', 'body_width'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'bodyThickness', 'body_thickness'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'bodyLength', 'body_length'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'firstFretThickness', 'first_fret_thickness'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'twelfthfretThickness', 'twelfth_fret_thickness'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'neckThickness', 'neck_thickness'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'headstockLength', 'headstock_length'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'headstockWidth', 'headstock_width'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'headstockThickness', 'headstock_thickness'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'bridgeStringSpacing', 'bridge_string_spacing'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'nutStringSpacing', 'nut_string_spacing'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'nutToPost', 'nut_to_post'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'stringCount', 'string_count',
                 needs_unit_conv=False, is_int=True),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'machinePostHoleDiameter', 'machine_post_hole_diameter'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'machinePostDiameter', 'machine_post_diameter'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'machinePostHoleSpacing', 'machine_post_hole_spacing'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'neckSpacing', 'neck_spacing'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'bridgeSpacing', 'bridge_spacing'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'singleCoilLength', 'single_coil_length'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'singleCoilWidth', 'single_coil_width'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'singleCoilDepth', 'single_coil_depth'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'humbuckerLength', 'humbucker_length'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'humbuckerWidth', 'humbucker_width'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'humbuckerDepth', 'humbucker_depth'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'humbuckerFillet', 'humbucker_fillet'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'pickupCavityMountLength', 'pickup_cavity_mount_length'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'pickupCavityMountTabWidth', 'pickup_cavity_mount_tab_width'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'bridgePickupAngle', 'bridge_pickup_angle',
                 needs_unit_conv=False),
    # Dropdown attributes
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'standard', '',
                 needs_unit_conv=False, is_dropdown=True, dropdown_default='Imperial'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'fretboardStyle', '',
                 needs_unit_conv=False, is_dropdown=True, dropdown_default='Straight Radius'),
    AttributeDef(ATTRIBUTE_GROUP_FRETBOARD, 'headstockStyle', '',
                 needs_unit_conv=False, is_dropdown=True, dropdown_default='Straight In-line'),
    # Pickup dropdowns (stored in 'pickups' group)
    AttributeDef(ATTRIBUTE_GROUP_PICKUPS, 'pickupNeck', '',
                 needs_unit_conv=False, is_dropdown=True, dropdown_default='Single-Coil'),
    AttributeDef(ATTRIBUTE_GROUP_PICKUPS, 'pickupMiddle', '',
                 needs_unit_conv=False, is_dropdown=True, dropdown_default='Single-Coil'),
    AttributeDef(ATTRIBUTE_GROUP_PICKUPS, 'pickupBridge', '',
                 needs_unit_conv=False, is_dropdown=True, dropdown_default='Single-Coil'),
]


def load_attributes(
    design: adsk.fusion.Design,
    defaults: GuitarDefaults,
) -> Dict[str, str]:
    """Load all attributes from a design, falling back to defaults.

    Returns a dict of {attribute_name: string_value} for all registered attributes.
    """
    values: Dict[str, str] = {}

    for attr_def in ATTRIBUTE_REGISTRY:
        # Compute default value
        if attr_def.is_dropdown:
            default_str = attr_def.dropdown_default
        elif attr_def.default_field:
            raw = getattr(defaults, attr_def.default_field)
            if attr_def.needs_unit_conv:
                default_str = str(raw * defaults.user_unit)
            else:
                default_str = str(raw)
        else:
            default_str = ''

        # Try to load from design attributes
        attrib = design.attributes.itemByName(attr_def.group, attr_def.name)
        if attrib:
            values[attr_def.name] = attrib.value
        else:
            values[attr_def.name] = default_str

    return values


def save_attributes(
    design: adsk.fusion.Design,
    values: Dict[str, str],
) -> None:
    """Save all parameter values as design attributes."""
    attribs = design.attributes
    for attr_def in ATTRIBUTE_REGISTRY:
        value = values.get(attr_def.name)
        if value is not None:
            attribs.add(attr_def.group, attr_def.name, str(value))
