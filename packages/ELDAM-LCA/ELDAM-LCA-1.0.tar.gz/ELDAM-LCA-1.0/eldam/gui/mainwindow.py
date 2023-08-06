import webbrowser

from PyQt5 import QtWidgets, QtGui
from PyQt5 import uic

from eldam.gui.dialogs import AboutDialog
from eldam.gui.gui_parameters import *
from eldam.gui.widgets import BlankEldaWidget, SimaproToEldaWidget, EldaToSimaproWidget, \
    CompareSimaproExportWithEldaWidget, UpdateEldaTemplateWidget, CopyEldaMetadataWidget, GenerateEldaIndexWidget

from eldam.settings import CHANGELOG_URL, DOCUMENTATION_URL, ISSUE_TRACKER_URL, ELDAM_VERSION, DOWNLOAD_URL

from eldam.utils.gui import get_last_eldam_version_number, get_last_changelog
from eldam.utils.misc import find_data_file


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setting icon
        self.setWindowIcon(QtGui.QIcon(find_data_file('files/icons/elsa.ico')))

        # Loading UI
        self.ui = uic.loadUi(find_data_file("files/user_interfaces/mainwindow.ui"), self)

        # Adding a status bar
        self.statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.messageChanged.connect(
            self.set_default_status_bar_stylesheet)  # For resetting default stylesheet

        # Linking toolbar actions with corresponding tabs
        self.actionCreate_blank_Elda.triggered.connect(
            lambda: self.tabWidget.setCurrentWidget(self.tab_blank_elda))
        self.actionConvert_SimaPro_export_to_Elda.triggered.connect(
            lambda: self.tabWidget.setCurrentWidget(self.tab_simapro_to_elda))
        self.actionConvert_Elda_to_SimaPro_import.triggered.connect(
            lambda: self.tabWidget.setCurrentWidget(self.tab_elda_to_simapro))
        self.actionCompare_SimaPro_export_with_Elda.triggered.connect(
            lambda: self.tabWidget.setCurrentWidget(self.tab_compare_simapro_export_with_elda))
        self.actionUpdate_Elda_template.triggered.connect(
            lambda: self.tabWidget.setCurrentWidget(self.tab_update_elda_template))
        self.actionCopy_Elda_metadata.triggered.connect(
            lambda: self.tabWidget.setCurrentWidget(self.tab_copy_elda_metadata))
        self.actionGenerate_Elda_index.triggered.connect(
            lambda: self.tabWidget.setCurrentWidget(self.tab_generate_elda_index))
        self.actionDocumentation.triggered.connect(
            lambda: webbrowser.open_new(DOCUMENTATION_URL))
        self.actionBug_report.triggered.connect(
            lambda: webbrowser.open_new(ISSUE_TRACKER_URL))
        self.actionChangelog.triggered.connect(
            lambda: webbrowser.open_new(CHANGELOG_URL))
        about_dialog = AboutDialog(parent=self)
        self.actionAbout_ELDAM.triggered.connect(about_dialog.exec)

        # Adding corresponding widget to each layout
        self.tab_layout_blank_elda.addWidget(BlankEldaWidget())
        self.tab_layout_simapro_to_elda.addWidget(SimaproToEldaWidget())
        self.tab_layout_elda_to_simapro.addWidget(EldaToSimaproWidget())
        self.tab_layout_compare_simapro_export_with_elda.addWidget(CompareSimaproExportWithEldaWidget())
        self.tab_layout_update_elda_template.addWidget(UpdateEldaTemplateWidget())
        self.tab_layout_copy_elda_metadata.addWidget(CopyEldaMetadataWidget())
        self.tab_layout_generate_elda_index.addWidget(GenerateEldaIndexWidget())

    def show(self):
        super().show()
        self.check_eldam_version()

    def set_default_status_bar_stylesheet(self, args):
        """
        Reset the statusbar stylesheet to black.

        This method is connected to the messageChanged signal of the status bar. If args is empty (ie. if the message is
        removed) then the status bar stylesheet is reset.
        """
        if not args:
            self.statusBar.setStyleSheet(STATUS_BAR_DEFAULT_STYLESHEET)

    def check_eldam_version(self):
        """ Checks if there is a newer ELDAM version than the one running. If yes, prompts the user to download it. """
        last_eldam_version = get_last_eldam_version_number()

        if last_eldam_version not in (ELDAM_VERSION, None):
            last_changelog = get_last_changelog()
            if last_changelog:
                message = NEW_ELDA_VERSION_AVAILABLE_MESSAGE_WITH_CHANGELOG.format(last_changelog)
            else:
                message = NEW_ELDA_VERSION_AVAILABLE_MESSAGE.format(last_eldam_version)
            msg_box = QtWidgets.QMessageBox(parent=self)

            msg_box.setText(message)
            msg_box.setWindowTitle(NEW_ELDA_VERSION_AVAILABLE_TITLE)
            msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            msg_box.accepted.connect(lambda: webbrowser.open_new(DOWNLOAD_URL))

            msg_box.exec()
