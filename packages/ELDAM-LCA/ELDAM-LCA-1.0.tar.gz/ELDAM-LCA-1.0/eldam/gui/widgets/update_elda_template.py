from eldam.gui.widgets import EldamWidget
from eldam.gui.dialogs import EldaOpenDialog, RetryCancelDialog
from eldam.gui.gui_parameters import *

from eldam.core.elda import Elda

from eldam.utils.misc import find_data_file


class UpdateEldaTemplateWidget(EldamWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(find_data_file("files/user_interfaces/update_elda_template.ui"), *args, **kwargs)

        self.elda_open_dialog = EldaOpenDialog(self)

        self.browse_button.clicked.connect(self.elda_open_dialog.exec)
        self.elda_open_dialog.filesSelected.connect(lambda files: self.open_edit.setText(";".join(files)))
        self.main_button.clicked.connect(self.update_elda_template)
        self.open_edit.textChanged.connect(self.update_main_button_state)

    def update_main_button_state(self):
        # Check if the main button must be enabled or not

        if self.open_edit.text():
            self.main_button.setEnabled(True)
        else:
            self.main_button.setEnabled(False)

    def update_elda_template(self):
        """ Updates Elda template of every selected Eldas """

        filenames = self.open_edit.text().split(";")
        updated_files = 0

        # Reads processes from the files
        for i, input_filename in enumerate(filenames):
            self.show_message(FILES_UPDATING_MESSAGE.format(i + 1, len(filenames)))
            elda = Elda(filepath=input_filename)

            # Looping to catch PermissionError
            loop = True
            while loop:
                try:
                    elda.save(input_filename)
                    loop = False
                    updated_files += 1
                except PermissionError:
                    # Displays a retry/cancel choice in case of permission denied
                    retry_cancel = RetryCancelDialog(self, title=PERMISSION_DENIED_TITLE,
                                                     message=PERMISSION_DENIED_MESSAGE,
                                                     additional_info=PERMISSION_DENIED_ADDITIONAL_INFO.format(
                                                         input_filename))
                    if retry_cancel.exec() == RetryCancelDialog.Cancel:
                        loop = False

        if updated_files:
            self.show_message(FILES_UPDATING_SUCCESS_MESSAGE.format(updated_files),
                              message_type=EldamWidget.SuccessMessage)
