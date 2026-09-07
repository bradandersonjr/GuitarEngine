"""Builds pickup cavity sketches and extrusions."""

import math

import adsk.core
import adsk.fusion

from ..parameters import PickupsParams, PickupType
from ..sketch_helpers import (
    create_pickup_sketch,
    get_pickup_dimensions,
    fit_camera,
    create_timeline_group,
)


def build_pickups(
    app: adsk.core.Application,
    design: adsk.fusion.Design,
    params: PickupsParams,
) -> adsk.fusion.Component:
    """Create pickup cavity sketches and optional extrusions."""
    root_comp = design.rootComponent
    pickups_occ = root_comp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    pickups_comp = adsk.fusion.Component.cast(pickups_occ.component)

    sketches = pickups_comp.sketches
    xy_plane = pickups_comp.xYConstructionPlane

    neck_distance = (params.guitar_length - params.headstock_length
                     - params.fretboard_length - params.neck_spacing)
    bridge_distance = (params.guitar_length - params.headstock_length
                       - params.scale_length + params.bridge_spacing)
    middle_distance = bridge_distance + (neck_distance - bridge_distance) / 2

    neck_pickup_type = ''
    middle_pickup_type = ''
    bridge_pickup_type = ''

    # --- Neck pickup ---
    sketch1 = None
    if params.pickup_neck != PickupType.NONE:
        sketch1 = sketches.add(xy_plane)
        sketch1.isComputeDeferred = True
        sketch1.areConstraintsShown = False
        sketch1.arePointsShown = False
        _create_position_pickup(
            sketch1, neck_distance - _half_width(params, params.pickup_neck),
            params, params.pickup_neck,
        )
        type_label = params.pickup_neck.value
        sketch1.name = f'Neck Pickup [{type_label}]'
        neck_pickup_type = 'H' if params.pickup_neck == PickupType.HUMBUCKER else 'S'

    # --- Middle pickup ---
    sketch2 = None
    if params.pickup_middle != PickupType.NONE:
        sketch2 = sketches.add(xy_plane)
        sketch2.isComputeDeferred = True
        sketch2.areConstraintsShown = False
        sketch2.arePointsShown = False
        _create_position_pickup(
            sketch2, middle_distance,
            params, params.pickup_middle,
        )
        type_label = params.pickup_middle.value
        sketch2.name = f'Middle Pickup [{type_label}]'
        middle_pickup_type = 'H' if params.pickup_middle == PickupType.HUMBUCKER else 'S'

    # --- Bridge pickup ---
    sketch3 = sketches.add(xy_plane)
    if params.create_blanks:
        sketch3.isComputeDeferred = False
    else:
        sketch3.isComputeDeferred = True
    sketch3.areConstraintsShown = True
    sketch3.arePointsShown = False

    if params.pickup_bridge == PickupType.SINGLE_COIL:
        _create_bridge_single_coil(sketch3, bridge_distance, params)
        bridge_pickup_type = 'S'
    elif params.pickup_bridge == PickupType.HUMBUCKER:
        _create_bridge_humbucker(sketch3, bridge_distance, params)
        bridge_pickup_type = 'H'

    # --- Extrusions (only if blanks are being created) ---
    last_timeline_item = sketch3
    if params.create_blanks:
        extrudes = pickups_comp.features.extrudeFeatures
        last_timeline_item = _extrude_pickups(
            extrudes, sketch1, sketch2, sketch3, params,
        )

    fit_camera(app)

    comp_label = f'Pickups [{bridge_pickup_type}{middle_pickup_type}{neck_pickup_type}]'
    create_timeline_group(
        design,
        pickups_occ.timelineObject.index,
        last_timeline_item.timelineObject.index,
        comp_label,
    )
    pickups_comp.name = comp_label

    return pickups_comp


def _half_width(params: PickupsParams, pickup_type: PickupType) -> float:
    """Get half-width offset for neck pickup positioning."""
    if pickup_type == PickupType.SINGLE_COIL:
        return params.single_coil_width / 2
    return params.humbucker_width / 2


def _create_position_pickup(
    sketch: adsk.fusion.Sketch,
    position_x: float,
    params: PickupsParams,
    pickup_type: PickupType,
) -> None:
    """Create a pickup sketch at the given position."""
    width, length, fillet, cavity_hw, cavity_fillet = get_pickup_dimensions(
        pickup_type.value,
        params.single_coil_width, params.single_coil_length,
        params.humbucker_width, params.humbucker_length,
        params.humbucker_fillet, params.pickup_cavity_mount_tab_width,
    )
    create_pickup_sketch(
        sketch, position_x, width, length, fillet,
        params.pickup_cavity_mount_length, cavity_hw, cavity_fillet,
    )


def _create_bridge_single_coil(
    sketch: adsk.fusion.Sketch,
    bridge_distance: float,
    params: PickupsParams,
) -> None:
    """Create bridge single-coil pickup with rotation angle."""
    sc_w = params.single_coil_width
    center_x = bridge_distance + sc_w / 2
    lines = sketch.sketchCurves.sketchLines
    arcs = sketch.sketchCurves.sketchArcs
    sketch_points = sketch.sketchPoints

    width, length, fillet, cavity_hw, cavity_fillet = get_pickup_dimensions(
        'Single-Coil',
        params.single_coil_width, params.single_coil_length,
        params.humbucker_width, params.humbucker_length,
        params.humbucker_fillet, params.pickup_cavity_mount_tab_width,
    )

    main_rect, main_fillets, center_line, cavity_rect, cavity_fillets = create_pickup_sketch(
        sketch, center_x, width, length, fillet,
        params.pickup_cavity_mount_length, cavity_hw, cavity_fillet,
    )

    # Construction angle line
    angle_line = lines.addByTwoPoints(
        adsk.core.Point3D.create(bridge_distance, 0, 0),
        adsk.core.Point3D.create(bridge_distance + sc_w, 0, 0),
    )
    angle_line.isConstruction = True

    # Fixed center point
    point1 = adsk.core.Point3D.create(center_x, 0, 0)
    sk_point = sketch_points.add(point1)
    sk_point.isFixed = True

    # Geometric constraints
    constraints = sketch.geometricConstraints
    constraints.addMidPoint(sk_point, lines.item(2))
    constraints.addMidPoint(sk_point, lines.item(3))
    constraints.addMidPoint(lines.item(3).startSketchPoint, lines.item(1))
    constraints.addMidPoint(lines.item(3).endSketchPoint, lines.item(0))
    constraints.addMidPoint(lines.item(3).startSketchPoint, lines.item(5))
    constraints.addMidPoint(lines.item(3).endSketchPoint, lines.item(4))
    constraints.addPerpendicular(lines.item(3), lines.item(2))

    # Rotate all sketch elements by bridge pickup angle
    all_items = adsk.core.ObjectCollection.create()
    for curve in sketch.sketchCurves:
        all_items.add(curve)
    for pt in sketch.sketchPoints:
        all_items.add(pt)

    normal = sketch.xDirection.crossProduct(sketch.yDirection)
    normal.transformBy(sketch.transform)
    origin = sketch.origin
    origin.transformBy(sketch.transform)
    matrix = adsk.core.Matrix3D.create()
    matrix.setToRotation(-params.bridge_pickup_angle, normal, origin)
    sketch.move(all_items, matrix)

    sketch.name = 'Bridge Pickup [Single-Coil]'


def _create_bridge_humbucker(
    sketch: adsk.fusion.Sketch,
    bridge_distance: float,
    params: PickupsParams,
) -> None:
    """Create bridge humbucker pickup sketch."""
    center_x = bridge_distance + params.humbucker_width / 2

    width, length, fillet, cavity_hw, cavity_fillet = get_pickup_dimensions(
        'Humbucker',
        params.single_coil_width, params.single_coil_length,
        params.humbucker_width, params.humbucker_length,
        params.humbucker_fillet, params.pickup_cavity_mount_tab_width,
    )

    create_pickup_sketch(
        sketch, center_x, width, length, fillet,
        params.pickup_cavity_mount_length, cavity_hw, cavity_fillet,
    )

    sketch.name = 'Bridge Pickup [Humbucker]'


def _extrude_pickups(
    extrudes: adsk.fusion.ExtrudeFeatures,
    sketch_neck, sketch_middle, sketch_bridge,
    params: PickupsParams,
) -> adsk.fusion.Feature:
    """Extrude pickup cavities into body blank. Returns last feature for timeline."""
    last_feature = None

    if sketch_neck and params.pickup_neck != PickupType.NONE:
        depth = (params.single_coil_depth if params.pickup_neck == PickupType.SINGLE_COIL
                 else params.humbucker_depth)
        profs = _collect_profiles(sketch_neck)
        ext = extrudes.addSimple(
            profs, adsk.core.ValueInput.createByReal(-depth),
            adsk.fusion.FeatureOperations.CutFeatureOperation,
        )
        ext.name = f'Extrusion: Neck Pickup [{params.pickup_neck.value}]'
        last_feature = ext

    if sketch_middle and params.pickup_middle != PickupType.NONE:
        depth = (params.single_coil_depth if params.pickup_middle == PickupType.SINGLE_COIL
                 else params.humbucker_depth)
        profs = _collect_profiles(sketch_middle)
        ext = extrudes.addSimple(
            profs, adsk.core.ValueInput.createByReal(-depth),
            adsk.fusion.FeatureOperations.CutFeatureOperation,
        )
        ext.name = f'Extrusion: Middle Pickup [{params.pickup_middle.value}]'
        last_feature = ext

    if params.pickup_bridge != PickupType.NONE:
        depth = (params.single_coil_depth if params.pickup_bridge == PickupType.SINGLE_COIL
                 else params.humbucker_depth)
        profs = _collect_profiles(sketch_bridge)
        ext = extrudes.addSimple(
            profs, adsk.core.ValueInput.createByReal(-depth),
            adsk.fusion.FeatureOperations.CutFeatureOperation,
        )
        ext.name = f'Extrusion: Bridge Pickup [{params.pickup_bridge.value}]'
        last_feature = ext

    return last_feature


def _collect_profiles(sketch: adsk.fusion.Sketch) -> adsk.core.ObjectCollection:
    """Collect all profiles from a sketch into an ObjectCollection."""
    profs = adsk.core.ObjectCollection.create()
    for prof in sketch.profiles:
        profs.add(prof)
    return profs
