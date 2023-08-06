from PyQt5 import QtWidgets, QtCore, uic

from eldam.gui.gui_parameters import *

from eldam.core.parameters import CALCULATED_PARAMETERS_ATTRIBUTES, INPUT_PARAMETERS_ATTRIBUTES

from eldam.utils.gui import remove_path_from_error_message
from eldam.utils.misc import find_data_file

from eldam.settings import ELDAM_VERSION


class ResizableMessageBox(QtWidgets.QMessageBox):
    """
     Resizable message box

     Source:
        https://stackoverflow.com/a/2664019
    """

    def __init__(self):
        QtWidgets.QMessageBox.__init__(self)
        self.setSizeGripEnabled(True)

    def event(self, e):
        result = QtWidgets.QMessageBox.event(self, e)

        self.setMinimumHeight(0)
        self.setMaximumHeight(16777215)
        self.setMinimumWidth(0)
        self.setMaximumWidth(16777215)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        text_edit = self.findChild(QtWidgets.QTextEdit)
        if text_edit is not None:
            text_edit.setMinimumHeight(0)
            text_edit.setMaximumHeight(16777215)
            text_edit.setMinimumWidth(0)
            text_edit.setMaximumWidth(16777215)
            text_edit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        return result


class SimaProExportOpenDialog(QtWidgets.QFileDialog):
    def __init__(self, parent, accept_multiple_files=True):
        super().__init__(parent=parent)

        self.setNameFilters(SIMAPRO_EXPORT_FILE_TYPE)
        self.setDefaultSuffix(SIMAPRO_EXPORT_DEFAULT_EXTENSION)
        self.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        if accept_multiple_files:
            self.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        else:
            self.setFileMode(QtWidgets.QFileDialog.ExistingFile)


class SimaProImportSaveDialog(QtWidgets.QFileDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setNameFilters(SIMAPRO_IMPORT_FILE_TYPE)
        self.setDefaultSuffix(SIMAPRO_IMPORT_DEFAULT_EXTENSION)
        self.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)


class EldaOpenDialog(QtWidgets.QFileDialog):
    def __init__(self, parent, accept_multiple_files=True):
        super().__init__(parent=parent)

        self.setNameFilters(ELDA_FILE_TYPE)
        self.setDefaultSuffix(ELDA_DEFAULT_EXTENSION)
        self.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        if accept_multiple_files:
            self.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        else:
            self.setFileMode(QtWidgets.QFileDialog.ExistingFile)


class EldaSaveDialog(QtWidgets.QFileDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.setNameFilters(ELDA_FILE_TYPE)
        self.setDefaultSuffix(ELDA_DEFAULT_EXTENSION)
        self.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)


class EldaIndexSaveDialog(QtWidgets.QFileDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.setNameFilters(ELDA_INDEX_FILE_TYPE)
        self.setDefaultSuffix(ELDA_INDEX_DEFAULT_EXTENSION)
        self.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)


class ExistingEldaFileHandlingDialog(QtWidgets.QMessageBox):
    """ Class used to ask the file handling method for existing elda files """

    def __init__(self, parent, filename):
        super().__init__(parent=parent)

        self.setWindowTitle(EXISTING_FILE_TITLE)
        self.setText(EXISTING_FILE_MESSAGE_ELDA.format(filename))

        # Adding buttons (right to left)
        self.addButton(CANCEL, QtWidgets.QMessageBox.NoRole)
        self.addButton(ADD_MAJOR_VERSION, QtWidgets.QMessageBox.NoRole)
        self.addButton(ADD_MINOR_VERSION, QtWidgets.QMessageBox.NoRole)
        self.addButton(UPDATE_LAST_VERSION, QtWidgets.QMessageBox.NoRole)
        self.addButton(OVERWRITE, QtWidgets.QMessageBox.NoRole)
        self.addButton(RENAME, QtWidgets.QMessageBox.NoRole)
        self.addButton(SKIP, QtWidgets.QMessageBox.NoRole)


class DirectoryOpenDialog(QtWidgets.QFileDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        self.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)


class RetryCancelDialog(QtWidgets.QMessageBox):
    def __init__(self, parent, title, message, additional_info=None):
        super().__init__(parent=parent)

        self.setIcon(QtWidgets.QMessageBox.Critical)

        self.setText(message)
        self.setInformativeText(additional_info)
        self.setWindowTitle(title)
        self.setStandardButtons(QtWidgets.QMessageBox.Retry | QtWidgets.QMessageBox.Cancel)


class WarningDialog(QtWidgets.QMessageBox):
    def __init__(self, parent, title, message, additional_info=None):
        super().__init__(parent=parent)

        self.setIcon(QtWidgets.QMessageBox.Warning)

        self.setText(message)
        self.setInformativeText(additional_info)
        self.setWindowTitle(title)
        self.setStandardButtons(QtWidgets.QMessageBox.Ok)


class ErrorDialog(QtWidgets.QMessageBox):
    def __init__(self, parent, title, message, additional_info=None):
        super().__init__(parent=parent)

        self.setIcon(QtWidgets.QMessageBox.Critical)

        self.setText(message)
        self.setInformativeText(additional_info)
        self.setWindowTitle(title)
        self.setStandardButtons(QtWidgets.QMessageBox.Ok)


class ParameterConflictDialog(QtWidgets.QDialog):
    def __init__(self, conflict, parent=None):
        """
        Args:
            conflict (list): List of parameter conflicts
            parent (QtWidgets.QWidget): Parent widget
        """
        super().__init__(parent=parent)

        self.ui = uic.loadUi(find_data_file("files/user_interfaces/parameter_conflict_dialog.ui"), self)

        self.setWindowTitle(PARAMETER_CONFLICT_TITLE)
        self.label.setText(PARAMETER_CONFLICT_MESSAGE.format(len(conflict)))

        # Getting the type of the parameters
        param_type = None
        param_types = set([param.type for param in conflict])
        if len(param_types) == 1:  # Only one type of parameters
            param_type = param_types.pop()

        # Adding columns according to parameter type
        if param_type == 'Input parameter':
            attributes = INPUT_PARAMETERS_ATTRIBUTES
        elif param_type == 'Calculated parameter':
            attributes = CALCULATED_PARAMETERS_ATTRIBUTES
        else:  # Comparing input parameters and calculated parameters
            attributes = INPUT_PARAMETERS_ATTRIBUTES

        # Setting columns
        self.treeWidget.setColumnCount(len(attributes))
        self.treeWidget.setHeaderLabels(attributes.values())
        self.treeWidget.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        # Alternating row colors
        self.treeWidget.setAlternatingRowColors(True)

        # Setting stylesheet
        self.treeWidget.setStyleSheet(QTREEWIDGET_STYLESHEET)

        # Inserting a tree item per parameter and selecting the first one by default
        first = True
        for parameter in conflict:
            values = [str(getattr(parameter, attr) or '') for attr in attributes]
            item = QtWidgets.QTreeWidgetItem(self.treeWidget, values)

            if first:
                self.treeWidget.setCurrentItem(item)
                first = False


class AboutDialog(QtWidgets.QDialog):
    """ About ELDAM dialog """

    def __init__(self, parent):
        super().__init__(parent=parent)

        self.ui = uic.loadUi(find_data_file("files/user_interfaces/about.ui"), self)

        self.eldam_version_label.setText(ELDAM_VERSION)


class RuntimeErrorDialog(QtWidgets.QMessageBox):
    """ Dialog used show unexpected runtime error to the user. """

    def __init__(self, message):
        """
        Args:
            message (str): Runtime exception message
        """
        super().__init__()

        self.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.setDetailedText(remove_path_from_error_message(message))
