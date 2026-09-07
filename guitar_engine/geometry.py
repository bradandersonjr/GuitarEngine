"""Guitar geometry calculations.

Contains the mathematical formulas for fret spacing, fret width,
radius sagitta, and inlay placement. These are extracted from the
original inline calculations and preserved exactly.
"""

import math
from math import sqrt
from typing import List


def fret_position(scale_length: float, fret_number: int) -> float:
    """Distance from nut to a specific fret using equal temperament.

    Formula: distance = scale_length - (scale_length / (2 ^ (fret / 12)))
    """
    return scale_length - (scale_length / (2 ** (fret_number / 12.0)))


def all_fret_positions(scale_length: float, num_frets: int) -> List[float]:
    """All fret positions from fret 1 through num_frets."""
    return [fret_position(scale_length, f) for f in range(1, num_frets + 1)]


def fret_width_at_position(
    fret_distance: float,
    nut_length: float,
    end_length: float,
    fretboard_length: float,
) -> float:
    """Width of the fretboard at a given distance from the nut.

    Uses trigonometry to account for the trapezoidal fretboard shape
    where the nut end is narrower than the bridge end.
    """
    L = fretboard_length
    half_width_diff = (end_length - nut_length) / 2
    hyp = sqrt(half_width_diff ** 2 + L ** 2)
    cos_arg = (L ** 2 + hyp ** 2 - half_width_diff ** 2) / (2 * L * hyp)
    angle_deg = math.acos(cos_arg) * (180 / math.pi)
    angle_rad = math.radians(angle_deg)
    projection = fret_distance / math.cos(angle_rad)
    offset = 2 * sqrt(projection ** 2 - fret_distance ** 2)
    return nut_length + offset


def radius_sagitta(radius: float, half_chord: float) -> float:
    """Height of the arc (sagitta) for a fretboard radius.

    sagitta = R - sqrt(R^2 - (chord/2)^2)
    """
    return radius - sqrt(radius ** 2 - half_chord ** 2)


def inlay_midpoints(fret_positions: List[float]) -> List[float]:
    """Midpoints between consecutive frets for inlay placement."""
    return [((y - x) / 2) + x for x, y in zip(fret_positions, fret_positions[1:])]


def single_dot_positions(inlays: List[float]) -> List[float]:
    """Single-dot inlay positions: frets 3, 5, 7, 9, 15, 17, 19, 21."""
    return list(inlays[1:9:2]) + list(inlays[13:21:2])


def small_dot_positions(inlays: List[float]) -> List[float]:
    """Small single-dot inlay positions: frets 27, 29, 31, 33."""
    return list(inlays[25:33:2])


def double_dot_positions(inlays: List[float]) -> List[float]:
    """Double-dot inlay positions: frets 12 and 24."""
    return list(inlays[10:24:12])


def fretboard_length_from_frets(scale_length: float, num_frets: int) -> float:
    """Calculate the fretboard length (rounded up to nearest 1/8 unit).

    Computes the position of the last fret + 1 and rounds up.
    """
    last_fret_plus_one = fret_position(scale_length, num_frets + 1)
    return math.ceil(last_fret_plus_one * 8) / 8
