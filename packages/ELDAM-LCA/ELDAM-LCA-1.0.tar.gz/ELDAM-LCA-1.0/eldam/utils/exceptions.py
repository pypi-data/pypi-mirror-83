""" Custom exceptions """


class ExcelNameError(Exception):
    pass


class ExcelDuplicateNameError(Exception):
    pass


class CoordinatesFormatError(Exception):
    pass


class SimaProXlsxError(Exception):
    pass


class NotASimaProExportError(Exception):
    pass


class ParameterNumberError(Exception):
    pass


class FlowTypeError(Exception):
    pass


class ParameterConflictError(Exception):
    pass


class NotAnEldaError(Exception):
    pass


class EldaTemplateVersionError(Exception):
    pass


class EldaVersionError(Exception):
    pass


class ExcelFormulaError(Exception):
    def __init__(self, formula=None):
        self.formula = formula


class MissingParameterError(Exception):
    pass


class InputParameterValueError(Exception):
    pass


class ProductTypeError(Exception):
    pass


class ConversionError(Exception):
    pass
