"""Builds body and headstock blank extrusions."""

import adsk.core
import adsk.fusion

from ..parameters import BlanksParams
from ..sketch_helpers import fit_camera, create_timeline_group


def build_blanks(
    app: adsk.core.Application,
    design: adsk.fusion.Design,
    params: BlanksParams,
) -> adsk.fusion.Component:
    """Create rectangular body and headstock blanks."""
    root_comp = design.rootComponent
    blanks_occ = root_comp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    blanks_comp = adsk.fusion.Component.cast(blanks_occ.component)

    sketches = blanks_comp.sketches
    xy_plane = blanks_comp.xYConstructionPlane
    extrudes = blanks_comp.features.extrudeFeatures

    # Body blank sketch
    sketch1 = sketches.add(xy_plane)
    sketch1.isComputeDeferred = False
    sketch1.name = 'Body Blank'
    sketch1.sketchCurves.sketchLines.addTwoPointRectangle(
        adsk.core.Point3D.create(0, -params.body_width / 2, 0),
        adsk.core.Point3D.create(params.body_length, params.body_width / 2, 0),
    )

    # Headstock blank sketch
    sketch2 = sketches.add(xy_plane)
    sketch2.isComputeDeferred = False
    sketch2.name = 'Headstock Blank'
    hs_start_x = params.guitar_length - params.headstock_length
    sketch2.sketchCurves.sketchLines.addTwoPointRectangle(
        adsk.core.Point3D.create(hs_start_x, -params.headstock_width / 2, 0),
        adsk.core.Point3D.create(params.guitar_length, params.headstock_width / 2, 0),
    )

    # Extrude body blank
    body_prof = sketch1.profiles.item(0)
    body_extrude = extrudes.addSimple(
        body_prof,
        adsk.core.ValueInput.createByReal(-params.body_thickness),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
    )
    body_extrude.name = 'Extrusion: Body Blank'
    body_extrude.bodies.item(0).name = 'Body Blank'

    # Extrude headstock blank
    hs_prof = sketch2.profiles.item(0)
    hs_extrude = extrudes.addSimple(
        hs_prof,
        adsk.core.ValueInput.createByReal(-params.headstock_thickness),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
    )
    hs_extrude.name = 'Extrusion: Headstock Blank'
    hs_extrude.bodies.item(0).name = 'Headstock Blank'

    # Apply appearance
    lib = app.materialLibraries.itemByName('Fusion 360 Appearance Library')
    if lib:
        wax_appear = lib.appearances.itemByName('Wax (White)')
        if wax_appear:
            blanks_comp.bRepBodies.item(0).appearance = wax_appear
            blanks_comp.bRepBodies.item(1).appearance = wax_appear

    fit_camera(app)

    # Timeline group
    create_timeline_group(
        design,
        blanks_occ.timelineObject.index,
        hs_extrude.timelineObject.index,
        'Blanks',
    )
    blanks_comp.name = 'Blanks'

    return blanks_comp
