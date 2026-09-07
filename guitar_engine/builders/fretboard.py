"""Builds the guitar fretboard with optional fret slots, markers, and nut slot."""

import math
from math import sqrt

import adsk.core
import adsk.fusion

from ..parameters import FretboardParams, FretboardStyle
from ..geometry import (
    fret_position,
    all_fret_positions,
    fret_width_at_position,
    radius_sagitta,
    inlay_midpoints,
    single_dot_positions,
    small_dot_positions,
    double_dot_positions,
)
from ..sketch_helpers import fit_camera, create_timeline_group


def build_fretboard(
    app: adsk.core.Application,
    design: adsk.fusion.Design,
    params: FretboardParams,
) -> adsk.fusion.Component:
    """Create the fretboard component with surfaces, fret cuts, and markers."""
    root_comp = design.rootComponent
    new_occ = root_comp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    fb_comp = adsk.fusion.Component.cast(new_occ.component)
    fb_comp.description = 'Fretboard'

    nut_distance = params.guitar_length - params.headstock_length
    L = params.fretboard_length

    # Resolve effective radii based on fretboard style
    if params.fretboard_style == FretboardStyle.STRAIGHT_RADIUS:
        nut_radius = params.radius
        end_radius = params.radius
    else:
        nut_radius = params.nut_radius
        end_radius = params.end_radius

    is_flat = params.fretboard_style == FretboardStyle.FLAT

    # Sagitta calculations for end and nut arcs
    end_r = 0 if is_flat else radius_sagitta(end_radius, params.end_length / 2)
    nut_r = 0 if is_flat else radius_sagitta(nut_radius, params.nut_length / 2)
    end_c = radius_sagitta(params.end_curve, params.end_length / 2)

    h = params.fretboard_height

    # --- Key points for fretboard surface ---
    if is_flat:
        end_top_l = adsk.core.Point3D.create(nut_distance + end_c - L, -params.end_length / 2, h)
        end_top_c = adsk.core.Point3D.create(nut_distance - L, 0, h)
        end_top_r = adsk.core.Point3D.create(nut_distance + end_c - L, params.end_length / 2, h)
    else:
        end_top_l = adsk.core.Point3D.create(nut_distance + end_c - L, -params.end_length / 2, h - end_r)
        end_top_c = adsk.core.Point3D.create(nut_distance - L, 0, h)
        end_top_r = adsk.core.Point3D.create(nut_distance + end_c - L, params.end_length / 2, h - end_r)

    end_bot_l = adsk.core.Point3D.create(nut_distance + end_c - L, -params.end_length / 2, 0)
    end_bot_c = adsk.core.Point3D.create(nut_distance - L, 0, 0)
    end_bot_r = adsk.core.Point3D.create(nut_distance + end_c - L, params.end_length / 2, 0)

    if is_flat:
        nut_top_l = adsk.core.Point3D.create(nut_distance, -params.nut_length / 2, h)
    else:
        nut_top_l = adsk.core.Point3D.create(nut_distance, -params.nut_length / 2, h - nut_r)
    nut_top_c = adsk.core.Point3D.create(nut_distance, 0, h)
    if is_flat:
        nut_top_r = adsk.core.Point3D.create(nut_distance, params.nut_length / 2, h)
    else:
        nut_top_r = adsk.core.Point3D.create(nut_distance, params.nut_length / 2, h - nut_r)

    # --- Sketches ---
    sketches = fb_comp.sketches
    xy_plane = fb_comp.xYConstructionPlane

    # Sketch 1: Fretboard curves (main surface paths)
    sketch_curves = sketches.add(xy_plane)
    sketch_curves.isComputeDeferred = True
    arcs = sketch_curves.sketchCurves.sketchArcs
    lines = sketch_curves.sketchCurves.sketchLines

    # Path 1: End top arc (bridge end)
    if params.create_end_curve and is_flat:
        path1 = arcs.addByThreePoints(
            adsk.core.Point3D.create(nut_distance + end_c - L, params.end_length / 2, h),
            adsk.core.Point3D.create(nut_distance - L, 0, h),
            adsk.core.Point3D.create(nut_distance + end_c - L, -params.end_length / 2, h),
        )
    elif params.create_end_curve:
        path1 = arcs.addByThreePoints(end_top_l, end_top_c, end_top_r)
    else:
        path1 = arcs.addByThreePoints(
            adsk.core.Point3D.create(nut_distance - L, params.end_length / 2, h - end_r),
            adsk.core.Point3D.create(nut_distance - L, 0, h),
            adsk.core.Point3D.create(nut_distance - L, -params.end_length / 2, h - end_r),
        )

    open_profile1 = adsk.fusion.Path.create(
        path1.createForAssemblyContext(new_occ),
        adsk.fusion.ChainedCurveOptions.noChainedCurves,
    )

    # Path 2: End bottom
    if params.create_end_curve:
        path2 = arcs.addByThreePoints(end_bot_l, end_bot_c, end_bot_r)
    else:
        path2 = lines.addByTwoPoints(
            adsk.core.Point3D.create(nut_distance - L, params.end_length / 2, 0),
            adsk.core.Point3D.create(nut_distance - L, -params.end_length / 2, 0),
        )

    open_profile2 = adsk.fusion.Path.create(
        path2.createForAssemblyContext(new_occ),
        adsk.fusion.ChainedCurveOptions.noChainedCurves,
    )

    # Path 3: Nut top
    if is_flat:
        path3 = lines.addByTwoPoints(
            adsk.core.Point3D.create(nut_distance, -params.nut_length / 2, h),
            adsk.core.Point3D.create(nut_distance, params.nut_length / 2, h),
        )
    else:
        path3 = arcs.addByThreePoints(nut_top_l, nut_top_c, nut_top_r)

    open_profile3 = adsk.fusion.Path.create(
        path3.createForAssemblyContext(new_occ),
        adsk.fusion.ChainedCurveOptions.noChainedCurves,
    )

    # Path 4: Nut bottom
    path4 = lines.addByTwoPoints(
        adsk.core.Point3D.create(nut_distance, -params.nut_length / 2, 0),
        adsk.core.Point3D.create(nut_distance, params.nut_length / 2, 0),
    )
    open_profile4 = adsk.fusion.Path.create(
        path4.createForAssemblyContext(new_occ),
        adsk.fusion.ChainedCurveOptions.noChainedCurves,
    )

    # Connecting lines
    lines.addByTwoPoints(path1.startSketchPoint, path3.startSketchPoint)
    lines.addByTwoPoints(path2.startSketchPoint, path4.endSketchPoint)
    lines.addByTwoPoints(path1.endSketchPoint, path3.endSketchPoint)
    lines.addByTwoPoints(path2.endSketchPoint, path4.startSketchPoint)

    sketch_curves.name = 'Fretboard curves'
    sketch_curves.arePointsShown = False
    sketch_curves.isVisible = False

    # Sketch: Fret reference lines
    sketch_fret_ref = sketches.add(xy_plane)
    sketch_fret_ref.isComputeDeferred = True
    fret_ref_lines = sketch_fret_ref.sketchCurves.sketchLines
    sketch_fret_ref.name = 'Fret Lines (Reference)'
    sketch_fret_ref.isVisible = False

    # Sketch: Fret slot cuts
    sketch_fret_cuts = sketches.add(xy_plane)
    sketch_fret_cuts.isComputeDeferred = False
    cut_lines = sketch_fret_cuts.sketchCurves.sketchLines
    sketch_fret_cuts.name = f'Fret slots [ {params.fret_number} frets ]'
    sketch_fret_cuts.isVisible = False

    # Sketch: Nut slot
    sketch_nut = sketches.add(xy_plane)
    sketch_nut.isComputeDeferred = False
    nut_lines = sketch_nut.sketchCurves.sketchLines
    nut_lines.addTwoPointRectangle(
        adsk.core.Point3D.create(nut_distance, params.nut_length, h),
        adsk.core.Point3D.create(nut_distance + params.nut_slot_width, -params.nut_length, h),
    )
    nut_profile = sketch_nut.profiles.item(0)
    sketch_nut.name = 'Nut slot profile'
    sketch_nut.isVisible = False

    # Sketch: Inlay markers
    sketch_inlays = sketches.add(xy_plane)
    sketch_inlays.isComputeDeferred = False
    marker_circles = sketch_inlays.sketchCurves.sketchCircles
    sketch_inlays.name = 'Inlays'
    sketch_inlays.isVisible = False

    # Sketch: Marker reference points
    sketch_marker_pts = sketches.add(xy_plane)
    sketch_marker_pts.isComputeDeferred = True
    marker_points = sketch_marker_pts.sketchPoints
    sketch_marker_pts.name = 'Default Marker Positions'
    sketch_marker_pts.isVisible = False

    # --- Surface loft operations ---
    loft_feats = fb_comp.features.loftFeatures

    # Loft 1: Bridge end surface
    loft_input1 = loft_feats.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    loft_input1.loftSections.add(open_profile2)
    loft_input1.loftSections.add(open_profile1)
    loft_input1.isSolid = False
    loft1 = loft_feats.add(loft_input1)
    loft1.name = 'Loft: Fretboard End'

    # Loft 2: Nut end surface
    loft_input2 = loft_feats.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    loft_input2.loftSections.add(open_profile3)
    loft_input2.loftSections.add(open_profile4)
    loft_input2.isSolid = False
    loft2 = loft_feats.add(loft_input2)
    loft2.name = 'Loft: Fretboard Start'

    # Loft 3: Full fretboard surface
    loft_input3 = loft_feats.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    loft_input3.loftSections.add(loft1.faces[0])
    loft_input3.loftSections.add(loft2.faces[0])
    loft_input3.isSolid = False
    loft3 = loft_feats.add(loft_input3)
    loft3.name = 'Loft: Fretboard'

    # Stitch surfaces together
    surfaces = adsk.core.ObjectCollection.create()
    surfaces.add(loft1.bodies.item(0))
    surfaces.add(loft2.bodies.item(0))
    surfaces.add(loft3.bodies.item(0))

    tolerance = adsk.core.ValueInput.createByString('0.001 in')
    stitches = fb_comp.features.stitchFeatures
    stitch_input = stitches.createInput(
        surfaces, tolerance,
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
    )
    stitch = stitches.add(stitch_input)
    stitch.name = 'Stitch: Fretboard'

    # --- Fillet corners ---
    fb_body = stitch.bodies.item(0)
    end_edges = adsk.core.ObjectCollection.create()
    end_edges.add(fb_body.edges.item(1))
    end_edges.add(fb_body.edges.item(3))

    if params.create_fillet_radius:
        fillets = fb_comp.features.filletFeatures
        fillet_input = fillets.createInput()
        fillet_input.addConstantRadiusEdgeSet(
            end_edges,
            adsk.core.ValueInput.createByReal(params.fillet_radius),
            True,
        )
        fillet_input.isG2 = False
        fillet_input.isRollingBallCorner = True
        fillet = fillets.add(fillet_input)
        fillet.name = 'Rounded Corners'

    # --- Offset surface for fret projections ---
    face = stitch.bodies.item(0)
    top_face_idx = 6 if params.create_fillet_radius else 4
    top_face = face.faces.item(top_face_idx)

    input_entities = adsk.core.ObjectCollection.create()
    input_entities.add(top_face)

    offset_feats = fb_comp.features.offsetFeatures
    offset_input = offset_feats.createInput(
        input_entities,
        adsk.core.ValueInput.createByReal(-params.tang_depth),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
    )
    offset_feat = offset_feats.add(offset_input)
    offset_feat.name = 'Offset: Fret Projections'
    off_surf = offset_feat.faces.item(0)
    off_surf.body.name = 'Reference for fret cuts'
    off_surf.body.isVisible = False

    # Extend offset surface edges
    input_edges = adsk.core.ObjectCollection.create()
    for edge in off_surf.edges:
        input_edges.add(edge)

    distance = adsk.core.ValueInput.createByString('0.5 in')
    extend_feats = fb_comp.features.extendFeatures
    extend_input = extend_feats.createInput(
        input_edges, distance,
        adsk.fusion.SurfaceExtendTypes.NaturalSurfaceExtendType,
    )
    extend_feat = extend_feats.add(extend_input)
    extend_feat.name = 'Extend: Fret Projections'

    # --- Create fret slots and reference lines ---
    fret_positions = all_fret_positions(params.scale_length, params.fret_number)

    for fret_dist in fret_positions:
        fret_len = fret_width_at_position(
            fret_dist, params.nut_length, params.end_length, L,
        )
        x = nut_distance - fret_dist

        if params.create_blind_frets:
            inset = params.blind_frets / 2
            # Fret reference line
            fret_ref_lines.addByTwoPoints(
                adsk.core.Point3D.create(x, fret_len / 2 - inset, h),
                adsk.core.Point3D.create(x, -fret_len / 2 + inset, h),
            )
            # Fret slot rectangle
            cut_lines.addTwoPointRectangle(
                adsk.core.Point3D.create(x - params.tang_width / 2, -fret_len / 2 + inset, h),
                adsk.core.Point3D.create(x + params.tang_width / 2, fret_len / 2 - inset, h),
            )
        else:
            # Fret reference line (extended beyond fretboard)
            fret_ref_lines.addByTwoPoints(
                adsk.core.Point3D.create(x, fret_len / 2 + 1, h),
                adsk.core.Point3D.create(x, -fret_len / 2 - 1, h),
            )
            # Fret slot rectangle (extended beyond fretboard)
            cut_lines.addTwoPointRectangle(
                adsk.core.Point3D.create(x - params.tang_width / 2, -fret_len / 2 - 1, h),
                adsk.core.Point3D.create(x + params.tang_width / 2, fret_len / 2 + 1, h),
            )

    # --- Inlay markers ---
    inlays = inlay_midpoints(fret_positions)

    for pos in single_dot_positions(inlays):
        marker_circles.addByCenterRadius(
            adsk.core.Point3D.create(nut_distance - pos, 0, h),
            params.marker_diameter,
        )
        marker_points.add(adsk.core.Point3D.create(nut_distance - pos, 0, h))

    for pos in small_dot_positions(inlays):
        marker_circles.addByCenterRadius(
            adsk.core.Point3D.create(nut_distance - pos, 0, h),
            params.marker_diameter / 2,
        )
        marker_points.add(adsk.core.Point3D.create(nut_distance - pos, 0, h))

    for pos in double_dot_positions(inlays):
        marker_circles.addByCenterRadius(
            adsk.core.Point3D.create(nut_distance - pos, params.marker_spacing / 2, h),
            params.marker_diameter,
        )
        marker_circles.addByCenterRadius(
            adsk.core.Point3D.create(nut_distance - pos, -params.marker_spacing / 2, h),
            params.marker_diameter,
        )
        marker_points.add(adsk.core.Point3D.create(nut_distance - pos, 0, h))

    # Collect marker profiles
    fret_markers = adsk.core.ObjectCollection.create()
    for prof in sketch_inlays.profiles:
        fret_markers.add(prof)

    # --- Name the fretboard body ---
    fretboard = stitch.bodies.item(0)
    fretboard.name = f'Fretboard [ {params.fret_number} frets ]'

    # --- Project fret lines onto surface ---
    fb_faces = [f for f in fretboard.faces]
    fb_surf = fb_faces[top_face_idx::2]
    fret_curves_list = [c for c in sketch_fret_ref.sketchCurves]

    sketch_proj = sketches.add(xy_plane)
    sketch_proj.isComputeDeferred = True
    sketch_proj.projectToSurface(
        fb_surf, fret_curves_list,
        adsk.fusion.SurfaceProjectTypes.AlongVectorSurfaceProjectType,
        fb_comp.zConstructionAxis,
    )
    sketch_proj.name = f'Fret Lines [ {params.fret_number} frets ]'
    sketch_proj.isVisible = False

    # --- Extrusions ---
    extrudes = fb_comp.features.extrudeFeatures

    # Extrude markers
    if params.create_fret_markers:
        marker_extrude = extrudes.addSimple(
            fret_markers,
            adsk.core.ValueInput.createByReal(-params.marker_depth),
            adsk.fusion.FeatureOperations.CutFeatureOperation,
        )
        marker_extrude.name = 'Extrusion: Fret Markers'

    # Collect fret cut profiles
    cut_profs = adsk.core.ObjectCollection.create()
    for prof in sketch_fret_cuts.profiles:
        cut_profs.add(prof)

    # Fret cut extrusion (to entity)
    extrude_input = extrudes.createInput(
        cut_profs, adsk.fusion.FeatureOperations.CutFeatureOperation,
    )
    extent_to = adsk.fusion.ToEntityExtentDefinition.create(extend_feat.faces.item(0), True)
    extrude_input.setOneSideExtent(
        extent_to, adsk.fusion.ExtentDirections.PositiveExtentDirection,
    )

    # Extension extrusion at nut end
    nut_face_idx = 4 if params.create_fillet_radius else 1
    nut_extend = extrudes.addSimple(
        fb_faces[nut_face_idx], distance,
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
    )
    nut_ext_body = nut_extend.bodies.item(0)
    nut_ext_body.name = 'Extension'
    nut_extend.name = 'Extrusion: Extension'

    # Nut slot extrusion
    nut_slot = extrudes.addSimple(
        nut_profile,
        adsk.core.ValueInput.createByReal(-params.nut_slot_depth),
        adsk.fusion.FeatureOperations.CutFeatureOperation,
    )
    nut_slot.name = 'Extrusion: Nut Slot'

    # Fret cuts extrusion
    last_feature = nut_slot
    if params.create_fret_cuts:
        fret_extrude = extrudes.add(extrude_input)
        fret_extrude.name = 'Extrusion: Cutting Frets'
        last_feature = fret_extrude

    # Extension visibility
    nut_ext_body.isVisible = params.extension_visible

    # --- Appearance ---
    lib = app.materialLibraries.itemByName('Fusion 360 Appearance Library')
    if lib:
        yellow_appear = lib.appearances.itemByName('Paint - Enamel Glossy (Yellow)')
        wax_appear = lib.appearances.itemByName('Wax (White)')

        if yellow_appear:
            fb_comp.bRepBodies.item(0).appearance = yellow_appear
            fb_comp.bRepBodies.item(1).appearance = yellow_appear
        if wax_appear:
            off_surf.appearance = wax_appear

    fit_camera(app)

    # --- Timeline group ---
    create_timeline_group(
        design,
        new_occ.timelineObject.index,
        last_feature.timelineObject.index,
        f'Fretboard [ {params.fret_number} Frets ]',
    )
    fb_comp.name = f'Fretboard [ {params.fret_number} Frets ]'

    return fb_comp
