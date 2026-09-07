from dataclasses import dataclass
from enum import Enum


class FretboardStyle(Enum):
    STRAIGHT_RADIUS = 'Straight Radius'
    COMPOUND_RADIUS = 'Compound Radius'
    FLAT = 'Flat/No Radius'


class HeadstockStyle(Enum):
    STRAIGHT_INLINE = 'Straight In-line'
    SYMMETRICAL = 'Symmetrical'


class PickupType(Enum):
    SINGLE_COIL = 'Single-Coil'
    HUMBUCKER = 'Humbucker'
    NONE = 'None'


@dataclass
class FretboardParams:
    fret_number: int
    scale_length: float
    fretboard_length: float
    nut_length: float
    end_length: float
    fretboard_height: float
    fretboard_style: FretboardStyle
    radius: float
    nut_radius: float
    end_radius: float
    fillet_radius: float
    end_curve: float
    tang_width: float
    tang_depth: float
    blind_frets: float
    nut_slot_width: float
    nut_slot_depth: float
    marker_diameter: float
    marker_depth: float
    marker_spacing: float
    guitar_length: float
    headstock_length: float
    first_fret_thickness: float
    twelfth_fret_thickness: float
    neck_thickness: float
    headstock_width: float
    headstock_thickness: float
    create_fret_cuts: bool
    create_blind_frets: bool
    create_fret_markers: bool
    create_fillet_radius: bool
    create_end_curve: bool
    extension_visible: bool


@dataclass
class BlanksParams:
    body_length: float
    body_width: float
    body_thickness: float
    headstock_length: float
    headstock_width: float
    headstock_thickness: float
    guitar_length: float


@dataclass
class StringsParams:
    string_count: int
    bridge_string_spacing: float
    nut_string_spacing: float
    guitar_length: float
    headstock_length: float
    scale_length: float
    nut_length: float
    fretboard_height: float
    machine_post_hole_spacing: float
    machine_post_hole_diameter: float
    machine_post_diameter: float
    nut_to_post: float
    headstock_style: HeadstockStyle
    headstock_thickness: float
    create_blanks: bool


@dataclass
class PickupsParams:
    guitar_length: float
    headstock_length: float
    scale_length: float
    fretboard_length: float
    neck_spacing: float
    bridge_spacing: float
    single_coil_length: float
    single_coil_width: float
    single_coil_depth: float
    humbucker_length: float
    humbucker_width: float
    humbucker_depth: float
    humbucker_fillet: float
    pickup_neck: PickupType
    pickup_middle: PickupType
    pickup_bridge: PickupType
    pickup_cavity_mount_length: float
    pickup_cavity_mount_tab_width: float
    bridge_pickup_angle: float
    create_blanks: bool


@dataclass
class DimensionsParams:
    fretboard: FretboardParams
    strings: StringsParams
    pickups: PickupsParams
    body_width: float
    body_length: float


@dataclass
class UserParams:
    fretboard_height: float
    headstock_length: float
    first_fret_thickness: float
    twelfth_fret_thickness: float
    neck_thickness: float
    headstock_width: float
    headstock_thickness: float
    machine_post_hole_spacing: float
    machine_post_hole_diameter: float
    machine_post_diameter: float
    nut_to_post: float
    body_length: float
    body_width: float
    body_thickness: float


@dataclass
class BuildOptions:
    only_fretboard: bool
    create_blanks: bool
    create_dimensions: bool
