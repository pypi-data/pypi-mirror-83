import os

from PyQt5 import QtWidgets

from eldam.gui.widgets import EldamConversionWidget, EldamWidgetWithProgressBar
from eldam.gui.dialogs import SimaProExportOpenDialog, EldaSaveDialog, WarningDialog, ErrorDialog, RetryCancelDialog, \
    ExistingEldaFileHandlingDialog
from eldam.gui.gui_parameters import *

from eldam.core.simapro import SimaProXlsxReader
from eldam.core.elda import Elda

from eldam.utils.exceptions import MissingParameterError
from eldam.utils.misc import open_file, find_data_file


class SimaproToEldaWidget(EldamConversionWidget, EldamWidgetWithProgressBar):
    def __init__(self, *args, **kwargs):
        super().__init__(find_data_file("files/user_interfaces/simapro_to_elda.ui"), *args, **kwargs)

        # SimaPro exports widgets bindings
        self.simapro_export_open_dialog = SimaProExportOpenDialog(self)
        self.simapro_export_browse_button.clicked.connect(self.simapro_export_open_dialog.exec)
        self.simapro_export_open_dialog.filesSelected.connect(
            lambda files: self.open_edit.setText(";".join(files)))
        self.simapro_export_open_dialog.filesSelected.connect(self.read_processes)
        self.open_edit.editingFinished.connect(self.read_processes)
        self.open_edit.textChanged.connect(self.update_main_button_state)

        # Eldas to save widgets bindings
        self.elda_save_dialog = EldaSaveDialog(self)

        # On opening the elda_save_dialog, set the default file name to the process name or product name
        # if only one process have been opened, else to the default file name pattern.
        self.elda_save_browse_button.clicked.connect(
            lambda: self.elda_save_dialog.selectFile(self.save_name()))
        self.elda_save_browse_button.clicked.connect(self.elda_save_dialog.exec)
        self.elda_save_dialog.fileSelected.connect(self.save_edit.setText)  # Link EldaSaveDialog -> QLineEdit
        self.save_edit.editingFinished.connect(
            lambda: self.elda_save_dialog.selectFile(self.save_edit.text()))  # Link QLineEdit -> EldaSaveDialog
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
            result = DEFAULT_FILE_PATTERN

        return result + ELDA_DEFAULT_EXTENSION

    def read_processes(self):
        """ Reads the SimaPro exports selected """

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
        files_with_exp_converted_to_const = list()
        for input_filename in input_filenames:
            try:
                xlsx_reader = SimaProXlsxReader(input_filename)
            # If a reading error occurs, highlight the path edit border
            except DATA_READING_EXCEPTIONS:
                self.open_edit.setStyleSheet(PATH_ERROR_STYLESHEET)
                return

            processes = xlsx_reader.to_processes()

            if xlsx_reader.convert_expressions_to_constants:
                files_with_exp_converted_to_const.append(input_filename)

            for process in processes:

                # Removing unused parameters
                process.remove_unused_parameters()

                # Checking for missing parameters on the processes and for parameters with parameters but no formula
                try:
                    process.check_for_missing_parameters()

                except MissingParameterError as error:
                    ErrorDialog(self, title=MISSING_PARAMETER_TITLE,
                                message=f'File: {input_filename}\nProcess: {process.name}\n\n'
                                        f'{str(error)}',
                                additional_info=MISSING_PARAMETER_ADDITIONAL_INFO
                                ).exec()
                    self.open_edit.setText("")
                    return  # Aborting the rest of the function
            self.processes += processes

        if len(files_with_exp_converted_to_const) > 0:
            WarningDialog(self, title=EXPRESSIONS_CONVERTED_TO_CONSTANTS_TITLE,
                          message=EXPRESSIONS_CONVERTED_TO_CONSTANTS_MESSAGE.format(
                              len(files_with_exp_converted_to_const)),
                          additional_info=EXPRESSIONS_CONVERTED_TO_CONSTANTS_ADDITIONAL_INFO.format(
                              "\n\n".join(files_with_exp_converted_to_const))
                          ).exec()

        self.show_detailed_view()

        # Update the "Decide for each" radio button state according to the number of processes
        if len(self.processes) > 1:
            self.decide_for_each_radio.setEnabled(True)
        else:
            self.decide_for_each_radio.setEnabled(False)
            self.decide_for_each_radio.setChecked(False)
            self.overwrite_file_radio.setChecked(True)

    def resolve_export_conflicts(self):
        """ For each export conflict obtain the desired file handling """

        # Gets the file handling specified by the user (if he didn't choose to decide for each process)
        if self.overwrite_file_radio.isChecked():
            file_handling = OVERWRITE
        elif self.update_last_version_radio.isChecked():
            file_handling = UPDATE_LAST_VERSION
        elif self.add_minor_version_radio.isChecked():
            file_handling = ADD_MINOR_VERSION
        elif self.add_major_version_radio.isChecked():
            file_handling = ADD_MAJOR_VERSION
        else:
            file_handling = None

        remaining = len(self.export_conflicts)  # Counting the remaining export conflicts
        for export in self.export_conflicts:
            remaining -= 1

            # If there is a global file handling, attribute it to the current export
            if file_handling is not None:
                export['file_handling'] = file_handling

            else:
                # Else, ask the file handling to the user
                file_handling_dialog = ExistingEldaFileHandlingDialog(self, export['export_filename'])

                # I don't know why but the checkbox cannot be added to the dialog in its init method.
                # Thus, it is added here.
                checkbox = QtWidgets.QCheckBox(EXISTING_FILE_CHECKBOX_TEXT.format(remaining))
                if remaining > 0:
                    file_handling_dialog.setCheckBox(checkbox)
                file_handling_dialog.exec()

                # Get the clicked button
                clicked = file_handling_dialog.clickedButton()
                if clicked.text() == CANCEL:
                    # Stop the function
                    return
                else:
                    current_file_handling = clicked.text()

                # If the user checked the checkbox, apply the choice to every remaining files
                if checkbox.isChecked():
                    file_handling = current_file_handling

                # Save the current file handling
                export['file_handling'] = current_file_handling

    def export_processes(self):
        """ Export the processes from the export parameters list """

        for i, export in enumerate(self.exports_parameters):
            export_filename = export['export_filename']
            process = export['process']
            file_handling = export.get('file_handling', None)

            # Looping to catch PermissionError
            loop = True
            while loop:
                try:
                    # If the file does not exist yet, simply create it else, act according to the file handling
                    if file_handling in (OVERWRITE, None):
                        elda = Elda()
                        elda.add_version(process=process)

                    elif file_handling == RENAME:
                        # Asking the new filename
                        export_filename = EldaSaveDialog(self).getSaveFileName()

                        elda = Elda()
                        elda.add_version(process=process)

                    elif file_handling == UPDATE_LAST_VERSION:
                        elda = Elda(filepath=export_filename)
                        elda.update_last_version(process=process)

                    elif file_handling == ADD_MINOR_VERSION:
                        elda = Elda(filepath=export_filename)
                        elda.add_version(process=process)

                    elif file_handling == ADD_MAJOR_VERSION:
                        elda = Elda(filepath=export_filename)
                        elda.add_version(process=process, major_version=True)

                    elif file_handling == SKIP:
                        continue

                    elda.save(filepath=export_filename)

                    loop = False

                    self.update_progressbar(step="Saving Elda files", current=i + 1, total=len(self.exports_parameters))

                except PermissionError:
                    # Displays a retry/cancel choice in case of permission denied
                    retry_cancel = RetryCancelDialog(self, title=PERMISSION_DENIED_TITLE,
                                                     message=PERMISSION_DENIED_MESSAGE,
                                                     additional_info=PERMISSION_DENIED_ADDITIONAL_INFO.format(
                                                         export_filename))
                    if retry_cancel.exec() == RetryCancelDialog.Cancel:
                        loop = False

        if self.open_elda_or_directory_checkbox.isChecked():
            if len(self.processes) > 1:
                output_path = os.path.dirname(export_filename)
            else:
                output_path = export_filename

            open_file(output_path)

        self.update_progressbar(step="Elda conversion successful", current=1, total=1)
