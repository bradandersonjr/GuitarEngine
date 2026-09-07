"""Creates dimensioned reference sketches showing all guitar measurements."""

import math
from math import sqrt

import adsk.core
import adsk.fusion

from ..parameters import (
    DimensionsParams, FretboardStyle, HeadstockStyle, PickupType,
)
from ..geometry import (
    fret_position,
    fret_width_at_position,
)
from ..sketch_helpers import (
    create_pickup_sketch,
    get_pickup_dimensions,
    fit_camera,
    create_timeline_group,
)


def build_dimensions(
    app: adsk.core.Application,
    design: adsk.fusion.Design,
    params: DimensionsParams,
) -> adsk.fusion.Component:
    """Create dimension reference sketches for the guitar layout."""
    fb = params.fretboard
    st = params.strings
    pk = params.pickups

    root_comp = design.rootComponent
    dims_occ = root_comp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    dims_comp = adsk.fusion.Component.cast(dims_occ.component)

    nut_distance = fb.guitar_length - fb.headstock_length
    L = fb.fretboard_length
    string_inset = (fb.nut_length - st.nut_string_spacing) / 2

    sketches = dims_comp.sketches
    xy_plane = dims_comp.xYConstructionPlane
    bw = params.body_width

    # ========== Sketch 1: Boundary Dimensions ==========
    sketch1 = sketches.add(xy_plane)
    sketch1.isComputeDeferred = True
    lines = sketch1.sketchCurves.sketchLines
    sketch1.name = 'Boundary Dimensions'
    sketch1.isVisible = True
    sketch1.areDimensionsShown = True
    sketch1.areConstraintsShown = False
    sketch1.arePointsShown = False
    sketch1.areProfilesShown = False

    center_line = lines.addByTwoPoints(
        adsk.core.Point3D.create(0, 0, 0),
        adsk.core.Point3D.create(fb.guitar_length, 0, 0),
    )
    center_line.isConstruction = True
    center_line.isFixed = True

    origin_boundary = lines.addByTwoPoints(
        adsk.core.Point3D.create(0, bw / 2, 0),
        adsk.core.Point3D.create(0, -bw / 2, 0),
    )
    origin_boundary.isConstruction = True

    end_boundary = lines.addByTwoPoints(
        adsk.core.Point3D.create(fb.guitar_length, bw / 2, 0),
        adsk.core.Point3D.create(fb.guitar_length, -bw / 2, 0),
    )
    end_boundary.isConstruction = True

    top_boundary = lines.addByTwoPoints(
        adsk.core.Point3D.create(0, bw / 2, 0),
        adsk.core.Point3D.create(fb.guitar_length, bw / 2, 0),
    )
    top_boundary.isConstruction = True

    bottom_boundary = lines.addByTwoPoints(
        adsk.core.Point3D.create(0, -bw / 2, 0),
        adsk.core.Point3D.create(fb.guitar_length, -bw / 2, 0),
    )
    bottom_boundary.isConstruction = True

    body_boundary = lines.addByTwoPoints(
        adsk.core.Point3D.create(params.body_length, bw / 2, 0),
        adsk.core.Point3D.create(params.body_length, -bw / 2, 0),
    )
    body_boundary.isConstruction = True

    nut_boundary = lines.addByTwoPoints(
        adsk.core.Point3D.create(nut_distance, bw / 4, 0),
        adsk.core.Point3D.create(nut_distance, -bw / 4, 0),
    )
    nut_boundary.isConstruction = True

    bridge_boundary = lines.addByTwoPoints(
        adsk.core.Point3D.create(nut_distance - fb.scale_length, bw / 4, 0),
        adsk.core.Point3D.create(nut_distance - fb.scale_length, -bw / 4, 0),
    )
    bridge_boundary.isConstruction = True

    fret12_boundary = lines.addByTwoPoints(
        adsk.core.Point3D.create(nut_distance - fb.scale_length / 2, bw / 4, 0),
        adsk.core.Point3D.create(nut_distance - fb.scale_length / 2, -bw / 4, 0),
    )
    fret12_boundary.isConstruction = True

    # Add boundary dimension annotations
    dims = sketch1.sketchDimensions
    HORIZ = adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation
    VERT = adsk.fusion.DimensionOrientations.VerticalDimensionOrientation

    # Guitar total length
    dims.addDistanceDimension(
        top_boundary.startSketchPoint, top_boundary.endSketchPoint, HORIZ,
        adsk.core.Point3D.create(top_boundary.length / 2, bw / 2 + 4, 0), False)
    # Body width
    dims.addDistanceDimension(
        origin_boundary.startSketchPoint, origin_boundary.endSketchPoint, VERT,
        adsk.core.Point3D.create(-4, 0, 0), False)
    # Bridge to fret 12
    dims.addDistanceDimension(
        bridge_boundary.startSketchPoint, fret12_boundary.startSketchPoint, HORIZ,
        adsk.core.Point3D.create(nut_distance - fb.scale_length + fb.scale_length / 4, bw / 4 + 2, 0), False)
    # Fret 12 to nut
    dims.addDistanceDimension(
        fret12_boundary.startSketchPoint, nut_boundary.startSketchPoint, HORIZ,
        adsk.core.Point3D.create(nut_distance - fb.scale_length / 4, bw / 4 + 2, 0), False)
    # Body length
    dims.addDistanceDimension(
        top_boundary.startSketchPoint, body_boundary.startSketchPoint, HORIZ,
        adsk.core.Point3D.create(params.body_length / 2, bw / 2 + 2, 0), False)
    # Neck length
    dims.addDistanceDimension(
        body_boundary.startSketchPoint, top_boundary.endSketchPoint, HORIZ,
        adsk.core.Point3D.create((fb.guitar_length + params.body_length) / 2, bw / 2 + 2, 0), False)
    # Half-widths
    dims.addDistanceDimension(
        top_boundary.startSketchPoint, center_line.startSketchPoint, VERT,
        adsk.core.Point3D.create(-2, bw / 4, 0), False)
    dims.addDistanceDimension(
        center_line.startSketchPoint, bottom_boundary.startSketchPoint, VERT,
        adsk.core.Point3D.create(-2, -bw / 4, 0), False)
    # Bridge offset from body end
    dims.addDistanceDimension(
        center_line.startSketchPoint, bridge_boundary.startSketchPoint, HORIZ,
        adsk.core.Point3D.create((fb.guitar_length - fb.headstock_length - fb.scale_length) / 2, bw / 4 + 2, 0), False)
    # Headstock length
    dims.addDistanceDimension(
        nut_boundary.startSketchPoint, center_line.endSketchPoint, HORIZ,
        adsk.core.Point3D.create(fb.guitar_length - fb.headstock_length / 2, bw / 4 + 2, 0), False)

    # ========== Sketch 2: Core Dimensions (frets, machine posts) ==========
    sketch2 = sketches.add(xy_plane)
    sketch2.isComputeDeferred = True
    dim_frets = sketch2.sketchCurves.sketchLines
    dim_circles = sketch2.sketchCurves.sketchCircles
    sketch2.name = 'Core Dimensions'
    sketch2.isVisible = True
    sketch2.areDimensionsShown = True
    sketch2.areConstraintsShown = False
    sketch2.arePointsShown = False
    sketch2.areProfilesShown = False

    # Draw fret dimension lines
    for fret in range(int(fb.fret_number) + 1):
        fret_dist = fret_position(fb.scale_length, fret)
        fret_len = fret_width_at_position(fret_dist, fb.nut_length, fb.end_length, L)
        dim_line = dim_frets.addByTwoPoints(
            adsk.core.Point3D.create(nut_distance - fret_dist, fret_len / 2, 0),
            adsk.core.Point3D.create(nut_distance - fret_dist, -fret_len / 2, 0),
        )
        dim_line.isConstruction = True

    # Fretboard end line
    end_dim = dim_frets.addByTwoPoints(
        adsk.core.Point3D.create(nut_distance - L, fb.end_length / 2, 0),
        adsk.core.Point3D.create(nut_distance - L, -fb.end_length / 2, 0),
    )
    end_dim.isConstruction = True

    # Bridge string spacing line
    bridge_line = dim_frets.addByTwoPoints(
        adsk.core.Point3D.create(nut_distance - fb.scale_length, st.bridge_string_spacing / 2, 0),
        adsk.core.Point3D.create(nut_distance - fb.scale_length, -st.bridge_string_spacing / 2, 0),
    )
    bridge_line.isConstruction = True

    dims2 = sketch2.sketchDimensions

    # Fret-to-fret dimensions
    num_frets = int(fb.fret_number)
    for d in range(num_frets):
        x_pos = nut_distance - fb.scale_length - (fb.scale_length / (-2 ** ((d + 0.5) / 12.0)))
        dims2.addDistanceDimension(
            dim_frets[d].startSketchPoint, dim_frets[d + 1].startSketchPoint, HORIZ,
            adsk.core.Point3D.create(x_pos, 5, 0), False)

    # Cumulative fret distances from nut
    for d in range(1, num_frets + 1):
        x_pos = nut_distance - fb.scale_length - (fb.scale_length / (-2 ** ((d - 0.5) / 12.0)))
        dims2.addDistanceDimension(
            dim_frets[0].endSketchPoint, dim_frets[d].endSketchPoint, HORIZ,
            adsk.core.Point3D.create(x_pos, -5 - d / 4, 0), False)

    # Nut width
    dims2.addDistanceDimension(
        dim_frets[0].startSketchPoint, dim_frets[0].endSketchPoint, VERT,
        adsk.core.Point3D.create(nut_distance + 2, 0, 0), False)
    # End width
    dims2.addDistanceDimension(
        end_dim.startSketchPoint, end_dim.endSketchPoint, VERT,
        adsk.core.Point3D.create(nut_distance - L - 1, 0, 0), False)
    # Fretboard length
    dims2.addDistanceDimension(
        end_dim.endSketchPoint, dim_frets[0].endSketchPoint, HORIZ,
        adsk.core.Point3D.create(nut_distance - L / 2, -12, 0), False)
    # Scale length
    dims2.addDistanceDimension(
        bridge_line.startSketchPoint, dim_frets[0].startSketchPoint, HORIZ,
        adsk.core.Point3D.create(nut_distance - fb.scale_length / 2, 8, 0), False)
    # Bridge string spacing
    dims2.addDistanceDimension(
        bridge_line.startSketchPoint, bridge_line.endSketchPoint, VERT,
        adsk.core.Point3D.create(nut_distance - fb.scale_length - 1, 0, 0), False)

    # Machine post dimensions
    nut_span = fb.nut_length - string_inset * 2

    if st.headstock_style == HeadstockStyle.STRAIGHT_INLINE:
        _dim_straight_inline_posts(
            sketch2, dim_frets, dim_circles, dims2, params,
            nut_distance, nut_span, string_inset, HORIZ, VERT,
        )
    else:
        _dim_symmetrical_posts(
            sketch2, dim_frets, dims2, params,
            nut_distance, HORIZ, VERT,
        )

    # ========== Sketch 3: Pickup Dimensions ==========
    sketch3 = sketches.add(xy_plane)
    sketch3.isComputeDeferred = True
    sketch3.name = 'Pickup Dimensions'
    sketch3.isVisible = True
    sketch3.areDimensionsShown = True
    sketch3.areConstraintsShown = False
    sketch3.arePointsShown = False
    sketch3.areProfilesShown = False

    neck_distance = (fb.guitar_length - fb.headstock_length
                     - fb.fretboard_length - pk.neck_spacing)
    bridge_distance = (fb.guitar_length - fb.headstock_length
                       - fb.scale_length + pk.bridge_spacing)
    middle_distance = bridge_distance + (neck_distance - bridge_distance) / 2

    pickup_data = {}  # Store refs for dimensioning

    # Neck pickup sketch
    if pk.pickup_neck != PickupType.NONE:
        _dim_position_pickup(
            sketch3, pk, pk.pickup_neck, neck_distance,
            is_neck=True, pickup_data=pickup_data, key='neck',
        )

    # Middle pickup sketch
    if pk.pickup_middle != PickupType.NONE:
        _dim_position_pickup(
            sketch3, pk, pk.pickup_middle, middle_distance,
            is_neck=False, pickup_data=pickup_data, key='middle',
        )

    # Bridge pickup sketch
    sketch3_lines = sketch3.sketchCurves.sketchLines
    sketch3_points = sketch3.sketchPoints

    if pk.pickup_bridge == PickupType.SINGLE_COIL:
        center_x = bridge_distance + pk.single_coil_width / 2
    elif pk.pickup_bridge == PickupType.HUMBUCKER:
        center_x = bridge_distance + pk.humbucker_width / 2
    else:
        center_x = bridge_distance

    sk_point = sketch3_points.add(adsk.core.Point3D.create(center_x, 0, 0))
    sk_point.isFixed = True

    if pk.pickup_bridge == PickupType.SINGLE_COIL:
        _dim_bridge_single_coil(sketch3, sk_point, bridge_distance, pk, pickup_data)
    elif pk.pickup_bridge == PickupType.HUMBUCKER:
        _dim_bridge_humbucker(sketch3, sk_point, bridge_distance, pk, pickup_data)

    # Pickup dimension annotations
    dims3 = sketch3.sketchDimensions

    # Neck pickup dims
    if pk.pickup_neck != PickupType.NONE:
        nd = pickup_data['neck']
        x = nd['center_x']
        dims3.addDistanceDimension(
            nd['main_rect'][3].startSketchPoint, nd['main_rect'][1].endSketchPoint, HORIZ,
            adsk.core.Point3D.create(x, -6, 0), False)
        dims3.addDistanceDimension(
            nd['cavity_rect'][3].startSketchPoint, nd['cavity_rect'][1].endSketchPoint, HORIZ,
            adsk.core.Point3D.create(x, -5, 0), False)

    # Middle pickup dims
    if pk.pickup_middle != PickupType.NONE:
        md = pickup_data['middle']
        x = md['center_x']
        dims3.addDistanceDimension(
            md['main_rect'][3].startSketchPoint, md['main_rect'][1].endSketchPoint, HORIZ,
            adsk.core.Point3D.create(x, -6, 0), False)
        dims3.addDistanceDimension(
            md['cavity_rect'][3].startSketchPoint, md['cavity_rect'][1].endSketchPoint, HORIZ,
            adsk.core.Point3D.create(x, -5, 0), False)

    # Bridge pickup dims
    if 'bridge' in pickup_data:
        bd = pickup_data['bridge']
        x = bd['center_x']
        if pk.pickup_bridge == PickupType.SINGLE_COIL:
            dims3.addDistanceDimension(
                bd['main_rect'][3].startSketchPoint, bd['main_rect'][1].endSketchPoint, HORIZ,
                adsk.core.Point3D.create(x, -6, 0), False)
            dims3.addDistanceDimension(
                bd['cavity_rect'][3].startSketchPoint, bd['cavity_rect'][1].endSketchPoint, HORIZ,
                adsk.core.Point3D.create(x, -5, 0), False)
        elif pk.pickup_bridge == PickupType.HUMBUCKER:
            dims3.addDistanceDimension(
                bd['main_rect'][3].startSketchPoint, sk_point, HORIZ,
                adsk.core.Point3D.create(x, -6, 0), False)
            dims3.addDistanceDimension(
                bd['cavity_rect'][3].startSketchPoint, sk_point, HORIZ,
                adsk.core.Point3D.create(x, -5, 0), False)

    # Pickup gap dimensions
    neck_center_line = pickup_data.get('neck', {}).get('center_line')
    middle_center_line = pickup_data.get('middle', {}).get('center_line')

    if neck_center_line:
        dims3.addDistanceDimension(
            neck_center_line.endSketchPoint, sk_point, HORIZ,
            adsk.core.Point3D.create(bridge_distance + (neck_distance - bridge_distance) / 2, 7, 0), False)

        if middle_center_line:
            dims3.addDistanceDimension(
                neck_center_line.endSketchPoint, middle_center_line.endSketchPoint, HORIZ,
                adsk.core.Point3D.create(middle_distance + (neck_distance - middle_distance) / 2, 6, 0), False)
            dims3.addDistanceDimension(
                middle_center_line.endSketchPoint, sk_point, HORIZ,
                adsk.core.Point3D.create(bridge_distance + (middle_distance - bridge_distance) / 2, 6, 0), False)

    # Bridge pickup cavity length
    bridge_center_line = pickup_data.get('bridge', {}).get('center_line')
    if bridge_center_line:
        dims3.addDistanceDimension(
            bridge_center_line.endSketchPoint, bridge_center_line.startSketchPoint, VERT,
            adsk.core.Point3D.create(bridge_distance - 5, 0, 0), False)

    fit_camera(app, smooth=True, orientation=adsk.core.ViewOrientations.TopViewOrientation)

    create_timeline_group(
        design,
        dims_occ.timelineObject.index,
        sketch3.timelineObject.index,
        'Dimensions',
    )
    dims_comp.name = 'Dimensions'

    return dims_comp


def _dim_position_pickup(sketch, pk, pickup_type, position_x,
                         is_neck, pickup_data, key):
    """Create a dimensioned pickup sketch at position_x."""
    if pickup_type == PickupType.SINGLE_COIL:
        if is_neck:
            cx = position_x - pk.single_coil_width / 2
        else:
            cx = position_x
    else:
        if is_neck:
            cx = position_x - pk.humbucker_width / 2
        else:
            cx = position_x

    width, length, fillet, cavity_hw, cavity_fillet = get_pickup_dimensions(
        pickup_type.value,
        pk.single_coil_width, pk.single_coil_length,
        pk.humbucker_width, pk.humbucker_length,
        pk.humbucker_fillet, pk.pickup_cavity_mount_tab_width,
    )

    main_rect, main_fillets, center_line, cavity_rect, cavity_fillets = create_pickup_sketch(
        sketch, cx, width, length, fillet,
        pk.pickup_cavity_mount_length, cavity_hw, cavity_fillet,
        as_construction=True,
    )

    pickup_data[key] = {
        'main_rect': main_rect,
        'cavity_rect': cavity_rect,
        'center_line': center_line,
        'center_x': cx,
    }


def _dim_bridge_single_coil(sketch, sk_point, bridge_distance, pk, pickup_data):
    """Create dimensioned bridge single-coil pickup with rotation."""
    sc_w = pk.single_coil_width
    center_x = bridge_distance + sc_w / 2
    lines = sketch.sketchCurves.sketchLines

    width, length, fillet, cavity_hw, cavity_fillet = get_pickup_dimensions(
        'Single-Coil',
        pk.single_coil_width, pk.single_coil_length,
        pk.humbucker_width, pk.humbucker_length,
        pk.humbucker_fillet, pk.pickup_cavity_mount_tab_width,
    )

    main_rect, main_fillets, center_line, cavity_rect, cavity_fillets = create_pickup_sketch(
        sketch, center_x, width, length, fillet,
        pk.pickup_cavity_mount_length, cavity_hw, cavity_fillet,
        as_construction=True,
    )

    # Angle line
    angle_line = lines.addByTwoPoints(
        adsk.core.Point3D.create(bridge_distance, 0, 0),
        adsk.core.Point3D.create(bridge_distance + sc_w, 0, 0),
    )
    angle_line.isConstruction = True

    # Constraints (references use relative indices from the pickup sketch items)
    constraints = sketch.geometricConstraints
    # These use indices relative to the current sketch's line collection
    # The pickup sketch creates: main_rect[4 lines] + center_line[1] + cavity_rect[4 lines] + angle_line[1]
    # main_rect lines are at the beginning of this pickup's contribution
    line_count = sketch.sketchCurves.sketchLines.count
    base = line_count - 11  # 4 main + 1 center + 4 cavity + 1 angle + angle_line we just added

    all_lines = sketch.sketchCurves.sketchLines
    constraints.addMidPoint(sk_point, all_lines.item(base + 2))
    constraints.addMidPoint(sk_point, all_lines.item(base + 5))
    constraints.addMidPoint(all_lines.item(base + 5).startSketchPoint, all_lines.item(base + 1))
    constraints.addMidPoint(all_lines.item(base + 5).endSketchPoint, all_lines.item(base + 0))
    constraints.addMidPoint(all_lines.item(base + 5).startSketchPoint, all_lines.item(base + 8))
    constraints.addMidPoint(all_lines.item(base + 5).endSketchPoint, all_lines.item(base + 7))
    constraints.addPerpendicular(all_lines.item(base + 5), all_lines.item(base + 2))

    # Rotate
    items = adsk.core.ObjectCollection.create()
    for i in range(base, base + 10):
        items.add(all_lines.item(i))
    items.add(sk_point)

    normal = sketch.xDirection.crossProduct(sketch.yDirection)
    normal.transformBy(sketch.transform)
    origin = sketch.origin
    origin.transformBy(sketch.transform)
    matrix = adsk.core.Matrix3D.create()
    matrix.setToRotation(-pk.bridge_pickup_angle, normal, origin)
    sketch.move(items, matrix)

    pickup_data['bridge'] = {
        'main_rect': main_rect,
        'cavity_rect': cavity_rect,
        'center_line': center_line,
        'center_x': center_x,
    }


def _dim_bridge_humbucker(sketch, sk_point, bridge_distance, pk, pickup_data):
    """Create dimensioned bridge humbucker pickup."""
    center_x = bridge_distance + pk.humbucker_width / 2

    width, length, fillet, cavity_hw, cavity_fillet = get_pickup_dimensions(
        'Humbucker',
        pk.single_coil_width, pk.single_coil_length,
        pk.humbucker_width, pk.humbucker_length,
        pk.humbucker_fillet, pk.pickup_cavity_mount_tab_width,
    )

    main_rect, main_fillets, center_line, cavity_rect, cavity_fillets = create_pickup_sketch(
        sketch, center_x, width, length, fillet,
        pk.pickup_cavity_mount_length, cavity_hw, cavity_fillet,
        as_construction=True,
    )

    pickup_data['bridge'] = {
        'main_rect': main_rect,
        'cavity_rect': cavity_rect,
        'center_line': center_line,
        'center_x': center_x,
    }


def _dim_straight_inline_posts(sketch2, dim_frets, dim_circles, dims2, params,
                               nut_distance, nut_span, string_inset, HORIZ, VERT):
    """Add straight in-line machine post dimensions."""
    st = params.strings
    string_count = int(st.string_count)

    for s in range(string_count):
        nut_y = nut_span / 2 - (nut_span / (string_count - 1)) * s
        hole_x = nut_distance + st.nut_to_post + s * st.machine_post_hole_spacing
        post = dim_circles.addByTwoPoints(
            adsk.core.Point3D.create(hole_x, nut_y, 0),
            adsk.core.Point3D.create(hole_x, nut_y + st.machine_post_diameter, 0),
        )
        post.isConstruction = True

    for d in range(string_count - 1):
        dims2.addDistanceDimension(
            dim_circles[d].centerSketchPoint, dim_circles[d + 1].centerSketchPoint, HORIZ,
            adsk.core.Point3D.create(
                nut_distance + st.nut_to_post + st.machine_post_hole_spacing * d + st.machine_post_hole_spacing / 2,
                4, 0), False)
        dims2.addDistanceDimension(
            dim_circles[d].centerSketchPoint, dim_circles[d + 1].centerSketchPoint, VERT,
            adsk.core.Point3D.create(
                params.fretboard.guitar_length + 2,
                nut_span / 2 - (nut_span / (string_count - 1)) * d,
                0), False)

    dims2.addDistanceDimension(
        dim_frets.item(0).startSketchPoint, dim_circles.item(0).centerSketchPoint, HORIZ,
        adsk.core.Point3D.create(nut_distance + st.nut_to_post / 2, 4, 0), False)


def _dim_symmetrical_posts(sketch2, dim_frets, dims2, params,
                           nut_distance, HORIZ, VERT):
    """Add symmetrical (3+3) machine post dimensions."""
    st = params.strings
    nss = st.nut_string_spacing
    ntp = st.nut_to_post
    mphs = st.machine_post_hole_spacing
    mpd = st.machine_post_diameter

    posts = sketch2.sketchCurves.sketchCircles
    r = mpd / 2

    h1 = posts.addByCenterRadius(adsk.core.Point3D.create(nut_distance + ntp, nss / 2 + mpd / 2, 0), r)
    h1.isConstruction = True
    h2 = posts.addByCenterRadius(adsk.core.Point3D.create(nut_distance + ntp + mphs, nss / 2 + mpd / 2, 0), r)
    h2.isConstruction = True
    h3 = posts.addByCenterRadius(adsk.core.Point3D.create(nut_distance + ntp + mphs * 2, nss / 2 + mpd / 2, 0), r)
    h3.isConstruction = True
    h4 = posts.addByCenterRadius(adsk.core.Point3D.create(nut_distance + ntp + mphs * 2, -nss / 2 - mpd / 2, 0), r)
    h4.isConstruction = True
    h5 = posts.addByCenterRadius(adsk.core.Point3D.create(nut_distance + ntp + mphs, -nss / 2 - mpd / 2, 0), r)
    h5.isConstruction = True
    h6 = posts.addByCenterRadius(adsk.core.Point3D.create(nut_distance + ntp, -nss / 2 - mpd / 2, 0), r)
    h6.isConstruction = True

    dims2.addDistanceDimension(
        dim_frets.item(0).startSketchPoint, h1.centerSketchPoint, HORIZ,
        adsk.core.Point3D.create(nut_distance + ntp / 2, 4, 0), False)
    dims2.addDistanceDimension(
        h1.centerSketchPoint, h2.centerSketchPoint, HORIZ,
        adsk.core.Point3D.create(nut_distance + ntp + mphs / 2, 4, 0), False)
    dims2.addDistanceDimension(
        h2.centerSketchPoint, h3.centerSketchPoint, HORIZ,
        adsk.core.Point3D.create(nut_distance + ntp + mphs * 1.5, 4, 0), False)
    dims2.addDistanceDimension(
        h3.centerSketchPoint, h4.centerSketchPoint, VERT,
        adsk.core.Point3D.create(nut_distance + mphs * 3 + 2, 0, 0), False)
