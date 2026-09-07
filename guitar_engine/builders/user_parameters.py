"""Adds named user parameters to the Fusion 360 design for further modeling."""

import adsk.core
import adsk.fusion

from ..parameters import UserParams


def build_user_parameters(
    app: adsk.core.Application,
    design: adsk.fusion.Design,
    params: UserParams,
) -> None:
    """Create Fusion 360 user parameters from the guitar configuration."""
    default_units = design.unitsManager.defaultLengthUnits
    user_params = design.userParameters

    length_params = [
        ('BodyLength', params.body_length),
        ('BodyWidth', params.body_width),
        ('BodyThickness', params.body_thickness),
        ('FretboardHeight', params.fretboard_height),
        ('NeckThickness', params.neck_thickness),
        ('FirstFretThickness', params.first_fret_thickness),
        ('TwelfthFretThickness', params.twelfth_fret_thickness),
        ('HeadstockLength', params.headstock_length),
        ('HeadstockWidth', params.headstock_width),
        ('HeadstockThickness', params.headstock_thickness),
        ('NutToPost', params.nut_to_post),
        ('MachinePostHoleSpacing', params.machine_post_hole_spacing),
        ('MachinePostHoleDiameter', params.machine_post_hole_diameter),
        ('MachinePostDiameter', params.machine_post_diameter),
    ]

    for name, value in length_params:
        user_params.add(
            name,
            adsk.core.ValueInput.createByReal(float(value)),
            default_units,
            '',
        )

    # Angle parameters
    user_params.add('HeadstockAngle',
                    adsk.core.ValueInput.createByString('10'), 'deg', '')
    user_params.add('HyoidDistance',
                    adsk.core.ValueInput.createByReal(1.5 * 2.54), default_units, '')
    user_params.add('HyoidAngle',
                    adsk.core.ValueInput.createByString('90'), 'deg', '')
