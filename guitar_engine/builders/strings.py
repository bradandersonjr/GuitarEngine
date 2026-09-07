"""Builds string layout sketches and machine post holes."""

import adsk.core
import adsk.fusion

from ..parameters import StringsParams, HeadstockStyle
from ..sketch_helpers import create_timeline_group


def build_strings(
    app: adsk.core.Application,
    design: adsk.fusion.Design,
    params: StringsParams,
) -> adsk.fusion.Component:
    """Create string line sketches and machine post hole circles."""
    root_comp = design.rootComponent
    strings_occ = root_comp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    strings_comp = adsk.fusion.Component.cast(strings_occ.component)

    sketches = strings_comp.sketches
    xy_plane = strings_comp.xYConstructionPlane
    extrudes = strings_comp.features.extrudeFeatures

    string_count = int(params.string_count)
    string_inset = (params.nut_length - params.nut_string_spacing) / 2
    nut_distance = params.guitar_length - params.headstock_length
    nut_span = params.nut_length - string_inset * 2

    label = f'Strings [ {string_count} strings ]'

    if params.headstock_style == HeadstockStyle.STRAIGHT_INLINE:
        _build_straight_inline(
            sketches, xy_plane, params, string_count, string_inset,
            nut_distance, nut_span, label,
        )
    else:
        _build_symmetrical(
            sketches, xy_plane, params, string_count, string_inset,
            nut_distance, nut_span, label,
        )

    # Collect all tuning hole profiles for extrusion
    sketch2 = sketches.itemByName('Machine Post Holes')
    tuning_holes = adsk.core.ObjectCollection.create()
    for prof in sketch2.profiles:
        tuning_holes.add(prof)

    # Extrude tuning holes through headstock
    last_timeline_item = sketch2
    if params.create_blanks:
        holes_extrude = extrudes.addSimple(
            tuning_holes,
            adsk.core.ValueInput.createByReal(-params.headstock_thickness * 2),
            adsk.fusion.FeatureOperations.CutFeatureOperation,
        )
        holes_extrude.name = 'Extrusion: Tuning Machine Holes'
        last_timeline_item = holes_extrude

    # Timeline group
    create_timeline_group(
        design,
        strings_occ.timelineObject.index,
        last_timeline_item.timelineObject.index,
        label,
    )
    strings_comp.name = label

    return strings_comp


def _build_straight_inline(
    sketches, xy_plane, params: StringsParams,
    string_count: int, string_inset: float,
    nut_distance: float, nut_span: float, label: str,
) -> None:
    """Build strings and machine posts for straight in-line headstock."""
    # String lines sketch
    sketch1 = sketches.add(xy_plane)
    sketch1.isComputeDeferred = True
    sketch1.arePointsShown = False
    sketch1.name = label
    string_lines = sketch1.sketchCurves.sketchLines

    for s in range(string_count):
        bridge_y = (params.bridge_string_spacing / 2
                    - (params.bridge_string_spacing / (string_count - 1)) * s)
        nut_y = nut_span / 2 - (nut_span / (string_count - 1)) * s
        hole_x_offset = s * params.machine_post_hole_spacing
        z_top = params.fretboard_height + 0.125

        # String from bridge to nut
        string_lines.addByTwoPoints(
            adsk.core.Point3D.create(nut_distance - params.scale_length, bridge_y, z_top),
            adsk.core.Point3D.create(nut_distance, nut_y, z_top),
        )
        # String from nut to tuning post
        string_lines.addByTwoPoints(
            adsk.core.Point3D.create(nut_distance, nut_y, z_top),
            adsk.core.Point3D.create(nut_distance + params.nut_to_post + hole_x_offset, nut_y, 0),
        )

    # Machine post holes sketch
    sketch2 = sketches.add(xy_plane)
    sketch2.isComputeDeferred = True
    sketch2.arePointsShown = False
    sketch2.name = 'Machine Post Holes'
    circles = sketch2.sketchCurves.sketchCircles

    for s in range(string_count):
        nut_y = nut_span / 2 - (nut_span / (string_count - 1)) * s
        hole_x = nut_distance + params.nut_to_post + s * params.machine_post_hole_spacing
        circles.addByCenterRadius(
            adsk.core.Point3D.create(hole_x, nut_y + params.machine_post_diameter / 2, 0),
            params.machine_post_hole_diameter / 2,
        )


def _build_symmetrical(
    sketches, xy_plane, params: StringsParams,
    string_count: int, string_inset: float,
    nut_distance: float, nut_span: float, label: str,
) -> None:
    """Build strings and machine posts for symmetrical (3+3) headstock."""
    # String lines sketch
    sketch1 = sketches.add(xy_plane)
    sketch1.isComputeDeferred = True
    sketch1.arePointsShown = False
    sketch1.name = label
    string_lines = sketch1.sketchCurves.sketchLines

    z_top = params.fretboard_height + 0.125
    nss = params.nut_string_spacing
    ntp = params.nut_to_post
    mphs = params.machine_post_hole_spacing

    # Bridge to nut lines (same for all strings)
    for s in range(string_count):
        bridge_y = (params.bridge_string_spacing / 2
                    - (params.bridge_string_spacing / (string_count - 1)) * s)
        nut_y = nut_span / 2 - (nut_span / (string_count - 1)) * s
        string_lines.addByTwoPoints(
            adsk.core.Point3D.create(nut_distance - params.scale_length, bridge_y, z_top),
            adsk.core.Point3D.create(nut_distance, nut_y, z_top),
        )

    # Nut to post lines (symmetrical 3+3 layout)
    # Top 3 strings
    string_lines.addByTwoPoints(
        adsk.core.Point3D.create(nut_distance, nss / 2, z_top),
        adsk.core.Point3D.create(nut_distance + ntp, nss / 2, 0),
    )
    string_lines.addByTwoPoints(
        adsk.core.Point3D.create(nut_distance, nss / 2 - nss / 5, z_top),
        adsk.core.Point3D.create(nut_distance + ntp + mphs, nss / 2, 0),
    )
    string_lines.addByTwoPoints(
        adsk.core.Point3D.create(nut_distance, nss / 2 - nss / 5 * 2, z_top),
        adsk.core.Point3D.create(nut_distance + ntp + mphs * 2, nss / 2, 0),
    )
    # Bottom 3 strings
    string_lines.addByTwoPoints(
        adsk.core.Point3D.create(nut_distance, -nss / 2 + nss / 5 * 2, z_top),
        adsk.core.Point3D.create(nut_distance + ntp + mphs * 2, -nss / 2, 0),
    )
    string_lines.addByTwoPoints(
        adsk.core.Point3D.create(nut_distance, -nss / 2 + nss / 5, z_top),
        adsk.core.Point3D.create(nut_distance + ntp + mphs, -nss / 2, 0),
    )
    string_lines.addByTwoPoints(
        adsk.core.Point3D.create(nut_distance, -nss / 2, z_top),
        adsk.core.Point3D.create(nut_distance + ntp, -nss / 2, 0),
    )

    # Machine post holes sketch
    sketch2 = sketches.add(xy_plane)
    sketch2.isComputeDeferred = True
    sketch2.arePointsShown = False
    sketch2.name = 'Machine Post Holes'
    circles = sketch2.sketchCurves.sketchCircles
    mpd = params.machine_post_diameter
    r = params.machine_post_hole_diameter / 2

    # Top row (3 posts)
    circles.addByCenterRadius(
        adsk.core.Point3D.create(nut_distance + ntp, nss / 2 + mpd / 2, 0), r)
    circles.addByCenterRadius(
        adsk.core.Point3D.create(nut_distance + ntp + mphs, nss / 2 + mpd / 2, 0), r)
    circles.addByCenterRadius(
        adsk.core.Point3D.create(nut_distance + ntp + mphs * 2, nss / 2 + mpd / 2, 0), r)
    # Bottom row (3 posts)
    circles.addByCenterRadius(
        adsk.core.Point3D.create(nut_distance + ntp + mphs * 2, -nss / 2 - mpd / 2, 0), r)
    circles.addByCenterRadius(
        adsk.core.Point3D.create(nut_distance + ntp + mphs, -nss / 2 - mpd / 2, 0), r)
    circles.addByCenterRadius(
        adsk.core.Point3D.create(nut_distance + ntp, -nss / 2 - mpd / 2, 0), r)
