from dataclasses import dataclass


@dataclass
class GuitarDefaults:
    """Default parameter values for guitar generation.

    All length values are in user units (inches by default).
    The user_unit factor converts to centimeters (Fusion 360 internal unit).
    """

    user_unit: float = 2.54  # 2.54 = inches to cm, 0.1 = mm to cm, 1 = cm

    # Fretboard
    scale_length: float = 25.5
    fret_number: int = 22
    nut_length: float = 1.6527
    end_length: float = 2.1875
    radius: float = 7.25
    nut_radius: float = 10.0
    end_radius: float = 16.0
    fretboard_height: float = 0.25
    fillet_radius: float = 0.2
    end_curve: float = 10.0
    tang_width: float = 0.023
    tang_depth: float = 0.073
    blind_frets: float = 0.0625
    nut_slot_width: float = 0.127
    nut_slot_depth: float = 0.1
    marker_diameter: float = 0.1
    marker_depth: float = 0.05
    marker_spacing: float = 0.875

    # Body
    guitar_length: float = 38.5
    body_width: float = 12.5
    body_thickness: float = 1.75
    body_length: float = 16.75

    # Neck
    first_fret_thickness: float = 0.8
    twelfth_fret_thickness: float = 0.85
    neck_thickness: float = 1.0

    # Headstock
    headstock_length: float = 7.5
    headstock_width: float = 3.5
    headstock_thickness: float = 0.5625

    # Strings
    bridge_string_spacing: float = 2.08
    nut_string_spacing: float = 1.388
    nut_to_post: float = 1.5
    string_count: int = 6
    machine_post_hole_diameter: float = 0.4
    machine_post_diameter: float = 0.2
    machine_post_hole_spacing: float = 1.0

    # Pickups
    neck_spacing: float = 0.25
    bridge_spacing: float = 0.5
    single_coil_length: float = 2.75
    single_coil_width: float = 0.7
    single_coil_depth: float = 1.0
    humbucker_length: float = 2.75
    humbucker_width: float = 1.5
    humbucker_depth: float = 1.0
    humbucker_fillet: float = 0.125
    pickup_cavity_mount_length: float = 3.28
    pickup_cavity_mount_tab_width: float = 0.5
    bridge_pickup_angle: float = 10.0

    def to_internal(self, value: float) -> float:
        """Convert a user-unit value to cm (Fusion 360 internal)."""
        return value * self.user_unit


DEFAULTS = GuitarDefaults()
