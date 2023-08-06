import os

from PyQt5.QtCore import QUrl

from eldam.gui.widgets import EldamWidget, EldamWidgetWithProgressBar
from eldam.gui.dialogs import DirectoryOpenDialog, EldaIndexSaveDialog
from eldam.gui.gui_parameters import STATUS_FILE_ALREADY_EXISTS, STATUS_WRITING_PERMISSION_ERROR, \
    ELDA_READING_PERMISSION_ERROR

from eldam.core.elda_index import EldaIndexer
from eldam.utils.misc import open_file, find_data_file


class GenerateEldaIndexWidget(EldamWidgetWithProgressBar):
    def __init__(self, *args, **kwargs):
        super().__init__(find_data_file("files/user_interfaces/generate_elda_index.ui"), *args, **kwargs)

        # Elda directory widgets bindings
        self.directory_open_dialog = DirectoryOpenDialog(self)

        self.directory_browse_button.clicked.connect(self.directory_open_dialog.exec)
        self.directory_open_dialog.urlSelected.connect(lambda x: self.open_edit.setText(x.url(QUrl.PreferLocalFile)))
        self.open_edit.editingFinished.connect(
            lambda: self.directory_open_dialog.selectUrl(QUrl(self.open_edit.text())))
        self.open_edit.textChanged.connect(self.update_main_button_state)

        # Setting the Elda index filename from the entered directory
        self.directory_open_dialog.urlSelected.connect(
            lambda x: self.save_edit.setText(x.url(QUrl.PreferLocalFile) + "/elda_index.xlsx"))
        self.directory_open_dialog.urlSelected.connect(
            lambda x: self.elda_index_save_dialog.selectFile(x.url(QUrl.PreferLocalFile) + "/elda_index.xlsx"))

        # Elda index widgets bindings
        self.elda_index_save_dialog = EldaIndexSaveDialog(self)
        self.elda_index_browse_button.clicked.connect(self.elda_index_save_dialog.exec)
        self.elda_index_save_dialog.fileSelected.connect(self.save_edit.setText)
        self.save_edit.editingFinished.connect(
            lambda: self.elda_index_save_dialog.selectFile(self.save_edit.text()))
        self.save_edit.textChanged.connect(self.update_main_button_state)

        self.main_button.clicked.connect(self.generate_elda_index)

    def update_main_button_state(self):
        # Check if the main button must be enabled or not

        if self.save_edit.text() and self.open_edit.text():
            self.main_button.setEnabled(True)
        else:
            self.main_button.setEnabled(False)

    def generate_elda_index(self):

        directory = self.open_edit.text()
        output = self.save_edit.text()

        # Check if the Elda Index file already exists

        if os.path.isfile(output):
            if self.overwrite_elda_index_checkbox.isChecked():
                os.remove(output)
            else:
                self.show_message(message_type=EldamWidget.ErrorMessage,
                                  message=STATUS_FILE_ALREADY_EXISTS.format(output))
                return

        # Adding a progressbar suscriber to update the progress bar with the progress of the indexer
        indexer = EldaIndexer(directory)
        indexer.add_suscriber(self)

        # Looping to catch reading PermissionError
        try:
            indexer.build_index()
        except PermissionError:
            self.show_message(ELDA_READING_PERMISSION_ERROR, message_type=EldamWidget.ErrorMessage)

        # Looping to catch writing PermissionError
        try:
            indexer.save_index(output)
        except PermissionError:
            # Displays a retry/cancel choice in case of permission denied
            self.show_message(STATUS_WRITING_PERMISSION_ERROR, message_type=EldamWidget.ErrorMessage)

        if self.open_elda_index_checkbox.isChecked():
            open_file(output)
