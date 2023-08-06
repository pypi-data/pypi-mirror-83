import os

from eldam.gui.widgets import EldamConversionWidget
from eldam.gui.dialogs import EldaOpenDialog, SimaProImportSaveDialog, ErrorDialog, RetryCancelDialog, \
    ParameterConflictDialog
from eldam.gui.gui_parameters import *

from eldam.core.simapro import SimaProCsvWriter
from eldam.core.elda import Elda

from eldam.utils.exceptions import ExcelFormulaError, ConversionError, ParameterConflictError
from eldam.utils.misc import open_file, find_data_file


class EldaToSimaproWidget(EldamConversionWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(find_data_file("files/user_interfaces/elda_to_simapro.ui"), *args, **kwargs)

        # Elda widgets bindings
        self.elda_open_dialog = EldaOpenDialog(self)
        self.elda_open_browse_button.clicked.connect(self.elda_open_dialog.exec)
        self.elda_open_dialog.filesSelected.connect(
            lambda files: self.open_edit.setText(";".join(files)))
        self.elda_open_dialog.filesSelected.connect(self.read_processes)
        self.open_edit.editingFinished.connect(self.read_processes)
        self.open_edit.textChanged.connect(self.update_main_button_state)

        # Simapro imports to save widgets bindings
        self.simapro_import_save_dialog = SimaProImportSaveDialog(self)

        # On opening the simapro_import_save_dialog, set the default file name to the process name or product name
        # if only one process have been opened, else to the default file name pattern.
        self.simapro_import_browse_button.clicked.connect(
            lambda: self.simapro_import_save_dialog.selectFile(self.save_name()))
        self.simapro_import_browse_button.clicked.connect(self.simapro_import_save_dialog.exec)
        self.simapro_import_save_dialog.fileSelected.connect(self.save_edit.setText)
        self.save_edit.editingFinished.connect(
            lambda: self.simapro_import_save_dialog.selectFile(self.save_edit.text()))
        self.save_edit.textChanged.connect(self.update_main_button_state)

    def update_main_button_state(self):
        # Check if the main button must be enabled or not

        if self.save_edit.text() and self.open_edit.text():
            self.main_button.setEnabled(True)
        else:
            self.main_button.setEnabled(False)

    def save_name(self):
        """ Return the save name proposed to the user according to the parameters and number of processes """
        if len(self.processes) == 1:
            if self.processes[0].product is not None:
                result = self.processes[0].product.name
            else:
                result = self.processes[0].name or ''
        else:
            result = ''

        return result + SIMAPRO_IMPORT_DEFAULT_EXTENSION

    def read_processes(self):
        """ Reads the Eldas selected """
        self.open_edit.setStyleSheet('')  # Resetting the stylesheet

        self.processes = list()  # Removing previous processes
        self.treeWidget.clear()  # Clearing widget
        self.update_processes_summary('')
        input_filenames = self.open_edit.text().split(';')

        # Ending the function if the input is empty
        if input_filenames == ['']:
            return

        # Reads processes from the files
        self.show_message(message=READING_PROCESSES_MESSAGE)
        for i, input_filename in enumerate(input_filenames):
            self.show_message(message=READING_PROCESSES_MESSAGE_WITH_FULL_COUNTER.format(i, len(input_filenames)))

            try:
                elda = Elda(filepath=input_filename)
            # If a reading error occurs, highlight the path edit border
            except DATA_READING_EXCEPTIONS:
                self.open_edit.setStyleSheet(PATH_ERROR_STYLESHEET)
                return

            try:
                self.processes.append(elda.read_last_version().to_process())
            except ExcelFormulaError as formula_error:
                ErrorDialog(self, title=EXCEL_FORMULA_ERROR_TITLE,
                            message=EXCEL_FORMULA_ERROR_MESSAGE,
                            additional_info=EXCEL_FORMULA_ADDITIONAL_INFO.format(
                                input_filename, formula_error.formula)).exec()

        self.show_detailed_view()

    def resolve_export_conflicts(self):
        """ Raise an error if there are export conflicts and the user haven't checked
        the "Overwrite existing files" option"""

        if (len(self.export_conflicts) > 0) and not self.overwrite_file_checkbox.isChecked():
            ErrorDialog(self, title=EXISTING_FILE_ERROR_TITLE, message=EXISTING_FILE_ERROR_MESSAGE).exec()
            raise ConversionError

    def resolve_parameter_conflicts(self, conflict):
        """
        Shows the user the parameters in conflict (same name but different values) and lets him choose the one to keep

        Args:
            conflict (list of parameters):
                List of project/database parameters in conflict

        Returns:
            int: index of the parameter chosen by the user in conflict
        """

        parameter_conflict_dialog = ParameterConflictDialog(conflict=conflict, parent=self)

        if parameter_conflict_dialog.exec():  # Exec return 0 if the dialog is cancelled and 1 if ok is clicked
            # Return the index of the selected row
            return parameter_conflict_dialog.treeWidget \
                .indexFromItem(parameter_conflict_dialog.treeWidget.currentItem()) \
                .row()
        else:
            raise ConversionError

    def export_processes(self):
        """ Export the processes from the export parameters list """
        export_filename = self.save_edit.text()

        # Looping to catch PermissionError
        loop = True
        while loop:
            try:

                # Trying to catch ParameterConflictError
                try:
                    csv_writer = SimaProCsvWriter(*self.processes,
                                                  elda_only_data=not self.simapro_data_only_checkbox.isChecked())

                except ParameterConflictError as conflicts:
                    chosen_parameters = []
                    for conflict in conflicts.args[0]:
                        index = self.resolve_parameter_conflicts(conflict)
                        chosen_parameters.append(conflict[index])

                    csv_writer = SimaProCsvWriter(*self.processes, chosen_parameters=chosen_parameters)

                csv_writer.to_csv(filepath=export_filename)
                loop = False

            except PermissionError:
                # Displays a retry/cancel choice in case of permission denied
                retry_cancel = RetryCancelDialog(self, title=PERMISSION_DENIED_TITLE,
                                                 message=PERMISSION_DENIED_MESSAGE,
                                                 additional_info=PERMISSION_DENIED_ADDITIONAL_INFO.format(
                                                     export_filename))
                if retry_cancel.exec() == RetryCancelDialog.Cancel:
                    loop = False

            if self.open_directory_checkbox.isChecked():
                output_path = os.path.dirname(export_filename)

                open_file(output_path)

        self.show_message(SUCCESS_MESSAGE, message_type=self.SuccessMessage)
