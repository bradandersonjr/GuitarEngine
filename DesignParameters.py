import os, sys
import adsk.core, adsk.fusion, adsk.cam, traceback
from .Modules import simplejson
from .ParameterValues import ParameterValues
from .UIElements import UIElements

class DesignParameters:

    def __init__(self, app):
        self.app = app
        self.design = app.activeProduct

    def setAndStoreParameterValues(self, values: ParameterValues):

        for key, control in UIElements.floatValueControls.items():
            setattr(values, key, float(control.value))

        for key, control in UIElements.boolValueControls.items():
            setattr(values, key, bool(control.value))

        for key, control in UIElements.intSpinnerControls.items():
            setattr(values, key, float(control.value))

        for key, control in UIElements.floatSpinnerControls.items():
            if (control.unitType == 'deg'):                
                setattr(values, key, self.design.unitsManager.convert(float(control.value), 'rad', 'deg'))
            else:
                setattr(values, key, float(control.value))

        for key, control in UIElements.dropdownControls.items():
            setattr(values, key, control.selectedItem.name)

        paramJson = simplejson.dumps(values.__dict__, use_decimal=True)

        self.design.attributes.add("guitarEngine", "parameterValues", paramJson)

    def getStoredParameters(self):

        valueAttribute = self.design.attributes.itemByName("guitarEngine", "parameterValues")

        if (valueAttribute is not None):
            paramDictionary  = simplejson.loads(valueAttribute.value)

            parameters = ParameterValues()

            for key in paramDictionary:
                setattr(parameters, key, paramDictionary[key])

            return parameters
        else:
            return None
