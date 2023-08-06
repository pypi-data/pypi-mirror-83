import shutil

from eldam.gui.widgets import EldamWidget
from eldam.gui.dialogs import EldaSaveDialog
from eldam.gui.gui_parameters import STATUS_BLANK_ELDA_GENERATED, STATUS_PERMISSION_ERROR

from eldam.core.parameters import ELDA_TEMPLATE_FILEPATH
from eldam.utils.misc import find_data_file, open_file


class BlankEldaWidget(EldamWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(ui_file=find_data_file("files/user_interfaces/blank_elda.ui"), *args, **kwargs)

        self.elda_save_dialog = EldaSaveDialog(self)

        self.browse_button.clicked.connect(self.elda_save_dialog.exec)
        self.elda_save_dialog.fileSelected.connect(self.save_edit.setText)  # Link EldaSaveDialog -> QLineEdit
        self.save_edit.editingFinished.connect(
            lambda: self.elda_save_dialog.selectFile(self.save_edit.text()))  # Link QLineEdit -> EldaSaveDialog
        self.save_edit.textChanged.connect(self.update_main_button_state)

        self.main_button.clicked.connect(self.save_blank_elda)

    def update_main_button_state(self):
        # Check if the main button must be enabled or not

        if self.save_edit.text():
            self.main_button.setEnabled(True)
        else:
            self.main_button.setEnabled(False)

    def save_blank_elda(self):
        """ Saves a blank Elda file """

        output = self.save_edit.text()

        try:
            shutil.copyfile(find_data_file(ELDA_TEMPLATE_FILEPATH), output)

            self.show_message(STATUS_BLANK_ELDA_GENERATED, message_type=EldamWidget.SuccessMessage)

            if self.open_saved_elda_checkbox.isChecked():
                open_file(output)

        except PermissionError:
            self.show_message(STATUS_PERMISSION_ERROR, message_type=EldamWidget.ErrorMessage)
