#Default Parameter values, all values in cm (fusion's internal unit of measurement)
class ParameterValues:

    units: str

    # General Tab
    stringCount: int = 6
    fretNumber: int = 22
    scaleLength: float = 64.77
    guitarLength: float = 100.3
    neckPocketLength: float = 8
    bodyWidth: float = 31.75
    bodyThickness: float = 4.5
    bodyLength: float = 42.545
    firstFretThickness: float = 2
    twelfthfretThickness: float = 2.2
    neckThickness: float = 2.54
    generateOnlyFretboard: bool = False
    generateBlanks: bool = True
    generateDimensions: bool = False

    #Fretboard Tab
    radius: float = 18.415
    fretboardLength: float = 46.83
    nutRadius: float = 30.48
    endRadius: float = 40.64
    fretboardHeight: float = 0.64
    bridgeStringSpacing: float = 5.25
    nutStringSpacing: float = 3.5
    nutLength: float = 4.3
    endLength: float = 5.25
    nutSlotWidth: float = 0.32
    nutSlotDepth: float = 0.2
    createFilletRadius: bool = True
    filletRadius: float = 0.508
    createEndCurve: bool = True
    endCurve: float = 25.4
    extensionVisible: bool = True
    fretboardStyle: str = 'Straight Radius'
    createFretCuts: bool = True
    tangWidth: float =  0.06
    tangDepth: float = 0.16
    createBlindFrets: bool = True
    blindFretInset: float = 0.2
    createFretMarkers:  bool = True
    markerDiameter: float = 0.3
    markerDepth: float = 0.18
    markerSpacing: float = 2.14

    # Headstock Tab
    headstockStyle: str = 'Straight In-line'
    headstockLength: float = 18.8
    headstockWidth: float = 8.89
    headstockThickness: float = 1.25
    nutToPost: float = 3.8
    machinePostHoleDiameter: float = 1.0
    machinePostDiameter: float = 0.5
    machinePostHoleSpacing: float = 2.46

    #Pickup Tab
    pickupNeck: str = "Single-Coil"
    pickupMiddle: str = "Single-Coil"
    pickupBridge: str = "Single-Coil"

    bridgePickupAngle: float = 10
    neckSpacing: float = 0.7
    bridgeSpacing: float = 1.05

    singleCoilLength: float = 6.985
    singleCoilWidth: float = 1.778
    singleCoilDepth: float = 2.54

    humbuckerLength: float = 6.985
    humbuckerWidth: float = 3.81
    humbuckerDepth: float = 2.54
    humbuckerFillet: float = 0.3
    pickupCavityMountLength: float = 8.3312
    pickupCavityMountTabWidth: float =  1.27