"""Shared sketch helpers for Fusion 360 operations.

Eliminates the repeated "rectangle + 4 fillets" pattern used 12+ times
in the original code for pickup cavities and dimensions.
"""

from typing import List, Tuple

import adsk.core
import adsk.fusion


def create_rounded_rect(
    sketch_lines: adsk.fusion.SketchLines,
    sketch_arcs: adsk.fusion.SketchArcs,
    center_x: float,
    center_y: float,
    half_width: float,
    half_length: float,
    fillet_radius: float,
    z: float = 0.0,
    as_construction: bool = False,
) -> Tuple[List, List]:
    """Create a center-point rectangle with fillets on all 4 corners.

    Returns (rect_lines, fillet_arcs) tuple.
    """
    rect = sketch_lines.addCenterPointRectangle(
        adsk.core.Point3D.create(center_x, center_y, z),
        adsk.core.Point3D.create(center_x + half_width, center_y + half_length, z),
    )

    fillets = []
    for i in range(4):
        next_i = (i + 1) % 4
        fillet = sketch_arcs.addFillet(
            rect[i], rect[i].endSketchPoint.geometry,
            rect[next_i], rect[next_i].startSketchPoint.geometry,
            fillet_radius,
        )
        fillets.append(fillet)
        if as_construction:
            fillet.isConstruction = True

    if as_construction:
        for line in rect:
            line.isConstruction = True

    return rect, fillets


def create_pickup_sketch(
    sketch: adsk.fusion.Sketch,
    position_x: float,
    pickup_width: float,
    pickup_length: float,
    fillet_radius: float,
    cavity_mount_length: float,
    cavity_half_width: float,
    cavity_fillet_radius: float,
    as_construction: bool = False,
) -> Tuple:
    """Create a complete pickup cavity sketch with main rect, cavity rect, and center line.

    Args:
        position_x: X position of the pickup center
        pickup_width: Total width of the pickup opening
        pickup_length: Total length of the pickup opening
        fillet_radius: Corner radius for the pickup opening
        cavity_mount_length: Length of the cavity mount tabs
        cavity_half_width: Half-width of the cavity rectangle
        cavity_fillet_radius: Corner radius for the cavity rectangle
        as_construction: If True, mark all geometry as construction lines

    Returns:
        (main_rect, main_fillets, center_line, cavity_rect, cavity_fillets)
    """
    lines = sketch.sketchCurves.sketchLines
    arcs = sketch.sketchCurves.sketchArcs

    main_rect, main_fillets = create_rounded_rect(
        lines, arcs,
        position_x, 0,
        pickup_width / 2, pickup_length / 2,
        fillet_radius,
        as_construction=as_construction,
    )

    center_line = lines.addByTwoPoints(
        adsk.core.Point3D.create(position_x, -cavity_mount_length / 2, 0),
        adsk.core.Point3D.create(position_x, cavity_mount_length / 2, 0),
    )
    center_line.isConstruction = True

    cavity_rect, cavity_fillets = create_rounded_rect(
        lines, arcs,
        position_x, 0,
        cavity_half_width, cavity_mount_length / 2,
        cavity_fillet_radius,
        as_construction=as_construction,
    )

    return main_rect, main_fillets, center_line, cavity_rect, cavity_fillets


def get_pickup_dimensions(
    pickup_type_name: str,
    single_coil_width: float,
    single_coil_length: float,
    humbucker_width: float,
    humbucker_length: float,
    humbucker_fillet: float,
    pickup_cavity_mount_tab_width: float,
) -> Tuple[float, float, float, float, float]:
    """Get (width, length, fillet, cavity_half_width, cavity_fillet) for a pickup type."""
    if pickup_type_name == 'Single-Coil':
        return (
            single_coil_width,
            single_coil_length,
            single_coil_width / 2,
            single_coil_width / 2,
            single_coil_width / 2,
        )
    else:  # Humbucker
        return (
            humbucker_width,
            humbucker_length,
            humbucker_fillet,
            pickup_cavity_mount_tab_width / 2,
            humbucker_fillet / 2,
        )


def fit_camera(app: adsk.core.Application, smooth: bool = False,
               orientation: 'adsk.core.ViewOrientations' = None) -> None:
    """Center the camera to fit the entire model in view."""
    cam = app.activeViewport.camera
    cam.isFitView = True
    cam.isSmoothTransition = smooth
    if orientation is not None:
        cam.viewOrientation = orientation
    app.activeViewport.camera = cam


def create_timeline_group(
    design: adsk.fusion.Design,
    start_index: int,
    end_index: int,
    name: str,
) -> adsk.fusion.TimelineGroup:
    """Create a named timeline group spanning from start_index to end_index."""
    groups = design.timeline.timelineGroups
    group = groups.add(start_index, end_index)
    group.name = name
    return group
