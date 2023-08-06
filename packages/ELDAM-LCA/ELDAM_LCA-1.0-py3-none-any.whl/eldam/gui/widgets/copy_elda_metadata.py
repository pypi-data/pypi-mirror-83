from eldam.gui.widgets import EldamWidgetWithProgressBar
from eldam.gui.dialogs import EldaOpenDialog, ErrorDialog

from eldam.core.elda import Elda
from eldam.core.parameters import ATTRIBUTES_TO_COPY

from eldam.gui.gui_parameters import *

from eldam.utils.exceptions import ExcelFormulaError
from eldam.utils.misc import find_data_file


class CopyEldaMetadataWidget(EldamWidgetWithProgressBar):
    def __init__(self, *args, **kwargs):
        super().__init__(find_data_file("files/user_interfaces/copy_elda_metadata.ui"), *args, **kwargs)

        # Elda widgets bindings
        self.copy_from_dialog = EldaOpenDialog(self, accept_multiple_files=False)
        self.copy_from_browse_button.clicked.connect(self.copy_from_dialog.exec)
        self.copy_from_dialog.filesSelected.connect(
            lambda files: self.copy_from_edit.setText(files[0]))
        self.copy_from_edit.textChanged.connect(self.update_main_button_state)
        self.copy_from_edit.editingFinished.connect(self.check_reference_elda)
        self.copy_from_dialog.filesSelected.connect(self.check_reference_elda)

        self.copy_to_dialog = EldaOpenDialog(self)
        self.copy_to_browse_button.clicked.connect(self.copy_to_dialog.exec)
        self.copy_to_dialog.filesSelected.connect(
            lambda files: self.copy_to_edit.setText(";".join(files)))
        self.copy_to_edit.textChanged.connect(self.update_main_button_state)

        self.main_button.clicked.connect(self.copy_elda_metadata)

    def check_reference_elda(self):
        """ Check if the file provided as the reference Elda is one """
        self.copy_from_edit.setStyleSheet('')  # Resetting the stylesheet

        input_filename = self.copy_from_edit.text()

        # Ending the function if the input is empty
        if not input_filename:
            return

        # Reads process from the file
        try:
            elda = Elda(filepath=input_filename)
        # If a reading error occurs, highlight the path edit border
        except DATA_READING_EXCEPTIONS:
            self.copy_from_edit.setStyleSheet(PATH_ERROR_STYLESHEET)

    def update_main_button_state(self):
        # Check if the main button must be enabled or not

        if self.copy_from_edit.text() and self.copy_to_edit.text():
            self.main_button.setEnabled(True)
        else:
            self.main_button.setEnabled(False)

    def copy_elda_metadata(self):
        # Get the reference elda
        self.show_message(message=READING_ELDA_MESSAGE, time=-1)
        reference_elda = Elda(self.copy_from_edit.text())
        reference_process = reference_elda.read_last_version().to_process()

        # Get the metadata to copy
        attributes_to_copy = []
        for attribute in ATTRIBUTES_TO_COPY:
            # Checkboxes are named by postfixing "_checkbox" to the attribute name
            checkbox = getattr(self, attribute + '_checkbox')
            if checkbox.isChecked() and checkbox.isEnabled():
                attributes_to_copy.append(attribute)

        # Copy metadata from reference elda to every elda to update
        input_filenames = self.copy_to_edit.text().split(';')
        for i, input_filename in enumerate(input_filenames):
            self.update_progressbar(step='Copying metadata', current=i, total=len(input_filenames))

            # Getting the elda
            elda = Elda(filepath=input_filename)

            # Updating its metadata
            elda.update_last_version_metadata(process=reference_process, attributes=attributes_to_copy)

            try:
                elda.save(input_filename)
            except ExcelFormulaError as formula_error:
                ErrorDialog(self, title=EXCEL_FORMULA_ERROR_TITLE,
                            message=EXCEL_FORMULA_ERROR_MESSAGE,
                            additional_info=EXCEL_FORMULA_ADDITIONAL_INFO.format(
                                input_filename, formula_error.formula)).exec()

        self.update_progressbar(step='Metadata copy successful', current=1, total=1)
