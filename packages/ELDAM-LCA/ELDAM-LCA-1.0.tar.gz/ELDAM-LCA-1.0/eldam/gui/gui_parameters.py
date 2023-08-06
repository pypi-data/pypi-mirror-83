from openpyxl.utils.exceptions import InvalidFileException

from eldam.utils.exceptions import NotAnEldaError, NotASimaProExportError

STATUS_BAR_MESSAGES_TIME = 5000  # Default time for status bar messages in milliseconds
STATUS_BAR_DEFAULT_STYLESHEET = "QStatusBar{color:black; font-weight:bold;}"
STATUS_BAR_SUCCESS_STYLESHEET = "QStatusBar{color:green; font-weight:bold;}"
STATUS_BAR_ERROR_STYLESHEET = "QStatusBar{color:red; font-weight:bold;}"
PATH_ERROR_STYLESHEET = "QLineEdit{border: 1px solid #ca0000; border-radius: 3px; height: 1.4em}"
QTREEWIDGET_STYLESHEET = "QTreeWidget::item { border-right: 1px solid lightgrey}" \
                         "QTreeWidget::item:selected{background-color:lightgrey; color:#3c702e;}"

# Data reading exceptions
DATA_READING_EXCEPTIONS = (NotAnEldaError, NotASimaProExportError, InvalidFileException, FileNotFoundError)

# File types and extensions
SIMAPRO_EXPORT_FILE_TYPE = ["SimaPro export files (*.XLSX *.xlsx)"]
SIMAPRO_EXPORT_DEFAULT_EXTENSION = '.xlsx'
SIMAPRO_IMPORT_FILE_TYPE = ["SimaPro import file (*.csv *.CSV)"]
SIMAPRO_IMPORT_DEFAULT_EXTENSION = '.csv'
ELDA_FILE_TYPE = ["Elda file (*.xlsm *.XLSM)"]
ELDA_DEFAULT_EXTENSION = '.xlsm'
ELDA_INDEX_FILE_TYPE = ["Elda index file (*.xlsx *.XLSX)"]
ELDA_INDEX_DEFAULT_EXTENSION = '.xlsx'

DEFAULT_FILE_PATTERN = "PROCESS_PRODUCT_TODAY_NOW"

# Defining file handling constants
SKIP = 'Skip'
RENAME = 'Rename'
OVERWRITE = 'Overwrite'
UPDATE_LAST_VERSION = 'Update last version'
ADD_MINOR_VERSION = 'Add minor version'
ADD_MAJOR_VERSION = 'Add major version'
CANCEL = 'Cancel'

# Dialogs
EXISTING_FILE_TITLE = "File already exists"
EXISTING_FILE_MESSAGE_ELDA = "File \"{}\" already exists.\n\nShould it be overwritten or updated with a new version?"
EXISTING_FILE_CHECKBOX_TEXT = "Apply this choice to every {} remaining files"
EXISTING_FILE_ERROR_TITLE = EXISTING_FILE_TITLE
EXISTING_FILE_ERROR_MESSAGE = """This file already exist and the "Overwrite existing files" option is unchecked.\n
Check this option or rename the file and retry."""
NEW_ELDA_VERSION_AVAILABLE_TITLE = "New ELDAM version available"
NEW_ELDA_VERSION_AVAILABLE_MESSAGE = "A new ELDAM version is available ({}).\nDo you want to download it?"
NEW_ELDA_VERSION_AVAILABLE_MESSAGE_WITH_CHANGELOG = "A new ELDAM version is available: \n\n{}" \
                                                    "\nDo you want to download it?"

# Messages
STATUS_BLANK_ELDA_GENERATED = "Blank Elda generated"
STATUS_PERMISSION_ERROR = "Permission error"
STATUS_WRITING_PERMISSION_ERROR = "Writing permission error"
ELDA_READING_PERMISSION_ERROR = "Elda reading permission error"
STATUS_FILE_ALREADY_EXISTS = "File already exists : {}"
STATUS_MODIFICATION_SUCCESSFUL = "Modification successful"

READING_ELDA_MESSAGE = "Reading Elda ..."
READING_PROCESSES_MESSAGE = "Reading processes ..."
READING_PROCESSES_MESSAGE_WITH_FULL_COUNTER = "Reading processes ({}/{})"
PROCESSES_READ_MESSAGE = "{} process(es) read"
NO_ERRORS_FOUND_MESSAGE = "No errors found in {} read process(es)"
MISSING_QUALITY_DATA_MESSAGE = "{} process(es) with incomplete or missing quality data"
MISSING_QUALITY_DATA_DETAIL_MESSAGE = "{} flow(s) with incomplete or missing quality data."
FILES_UPDATING_MESSAGE = "Updating file {} on {} ..."
FILES_UPDATING_SUCCESS_MESSAGE = "Successfully updated {} file(s)."
MULTIPLE_PRODUCTS_FOR_FILE_NAMING_TITLE = "Process has multiple products"
MULTIPLE_PRODUCTS_FOR_FILE_NAMING_MESSAGE = "The PRODUCT keyword have been used but one or more exported processes have more than one product.\nThe first product will be used."
SUCCESS_MESSAGE = "Conversion successful"
EXCEL_FORMULA_ERROR_TITLE = "Error: unauthorized Excel formula"
EXCEL_FORMULA_ERROR_MESSAGE = "The Elda contains an unauthorized formula.\nReferring to other cells of the Elda is not authorized. Use parameters names instead."
EXCEL_FORMULA_ADDITIONAL_INFO = "\n\nFile: {}" \
                                "\n\nFormula: {}"
MULTIPLE_PROCESSES_IN_XLSX_TITLE = "Error: multiple processes"
MULTIPLE_PROCESSES_IN_XLSX_MESSAGE = "The SimaPro export file contains more than one process." \
                                     "\nPlease select another file."
NO_DIFFERENCES_IN_XLSX_AND_ELDA_MESSAGE = "There are no differences between the .xlsx and the Elda."
EXPRESSIONS_CONVERTED_TO_CONSTANTS_TITLE = "Expressions converted to constants"
EXPRESSIONS_CONVERTED_TO_CONSTANTS_MESSAGE = "{} file(s) have been exported with \"Convert expressions to constants\" " \
                                             "option checked. Parameters and formulas are replaced by their values."
EXPRESSIONS_CONVERTED_TO_CONSTANTS_ADDITIONAL_INFO = "Files:\n{}?"
MISSING_PARAMETER_TITLE = "Missing parameter"
MISSING_PARAMETER_ADDITIONAL_INFO = "This might be because you exported the process" \
                                    " from SimaPro's process edition window.\n\nTry exporting it from LCA Explorer window."

PERMISSION_DENIED_TITLE = "Permission denied"
PERMISSION_DENIED_MESSAGE = "You may not have writing permission on destination folder or the file may already" \
                            " be open."
PERMISSION_DENIED_ADDITIONAL_INFO = "File: {}"
"Please close all Eldas of the directory and retry"
PARAMETER_CONFLICT_TITLE = "Parameter conflict"
PARAMETER_CONFLICT_MESSAGE = "There are {} parameters in conflict.\nPlease select the one to keep."
