from PyQt5.QtWidgets import QTreeWidgetItem

from eldam.gui.widgets import EldamWidgetWithProcessSummary
from eldam.gui.dialogs import EldaOpenDialog, SimaProExportOpenDialog, ErrorDialog, RetryCancelDialog
from eldam.gui.gui_parameters import *

from eldam.core.simapro import SimaProXlsxReader
from eldam.core.elda import Elda

from eldam.utils.exceptions import MissingParameterError, ExcelFormulaError
from eldam.utils.lci_data import compare_processes
from eldam.utils.misc import x_str, find_data_file


class CompareSimaproExportWithEldaWidget(EldamWidgetWithProcessSummary):
    def __init__(self, *args, **kwargs):
        super().__init__(find_data_file("files/user_interfaces/compare_simapro_export_with_elda.ui"), *args, **kwargs)

        self.simapro_export_process = None
        self.elda_process = None

        # Setting TreeWidget columns width
        self.treeWidget.setColumnWidth(0, 250)
        self.treeWidget.setColumnWidth(1, 250)

        # Adding a separator between columns
        self.treeWidget.setStyleSheet(QTREEWIDGET_STYLESHEET)

        # Alternating row colors
        self.treeWidget.setAlternatingRowColors(True)

        # SimaPro exports widgets bindings
        self.simapro_export_open_dialog = SimaProExportOpenDialog(self, accept_multiple_files=False)
        self.simapro_export_browse_button.clicked.connect(self.simapro_export_open_dialog.exec)
        self.simapro_export_open_dialog.filesSelected.connect(
            lambda files: self.simapro_export_edit.setText(files[0]))
        self.simapro_export_open_dialog.filesSelected.connect(self.read_simapro_export)
        self.simapro_export_edit.editingFinished.connect(self.read_simapro_export)

        # Elda widgets bindings
        self.elda_open_dialog = EldaOpenDialog(self, accept_multiple_files=False)
        self.elda_browse_button.clicked.connect(self.elda_open_dialog.exec)
        self.elda_open_dialog.filesSelected.connect(
            lambda files: self.elda_edit.setText(files[0]))
        self.elda_open_dialog.filesSelected.connect(self.read_elda)
        self.elda_edit.editingFinished.connect(self.read_elda)

        # Binding buttons
        self.overwrite_elda_button.clicked.connect(self.overwrite_elda)
        self.update_last_version_button.clicked.connect(self.update_last_version)
        self.add_minor_version_button.clicked.connect(self.add_minor_version)
        self.add_major_version_button.clicked.connect(self.add_major_version)

    def read_simapro_export(self):
        self.simapro_export_edit.setStyleSheet('')  # Resetting the stylesheet

        input_filename = self.simapro_export_edit.text()

        # Ending the function if the input is empty
        if not input_filename:
            return

        # Reading the data
        try:
            xlsx_reader = SimaProXlsxReader(input_filename)
        # If a reading error occurs, highlight the path edit border
        except DATA_READING_EXCEPTIONS:
            self.simapro_export_edit.setStyleSheet(PATH_ERROR_STYLESHEET)
            return

        processes = xlsx_reader.to_processes()

        # Checking that there are only one process in the SimaPro export
        if len(processes) > 1:
            ErrorDialog(self, title=MULTIPLE_PROCESSES_IN_XLSX_TITLE,
                        message=MULTIPLE_PROCESSES_IN_XLSX_MESSAGE).exec()
            self.simapro_export_edit.setText("")
            return  # Aborting the rest of the function
        else:
            process = processes[0]

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
            self.simapro_export_edit.setText("")
            return  # Aborting the rest of the function

        # Saving the process as attribute
        self.simapro_export_process = process

        # Displaying the process view
        self.show_comparison()

    def read_elda(self):
        self.elda_edit.setStyleSheet('')  # Resetting the stylesheet

        input_filename = self.elda_edit.text()

        # Ending the function if the input is empty
        if not input_filename:
            return

        # Reads process from the file
        try:
            elda = Elda(filepath=input_filename)

        # If a reading error occurs, highlight the path edit border
        except DATA_READING_EXCEPTIONS:
            self.elda_edit.setStyleSheet(PATH_ERROR_STYLESHEET)
            return

        try:
            self.elda_process = elda.read_last_version().to_process()
            self.elda_process.remove_unused_parameters()

            # Displaying the process view
            self.show_comparison()

        except ExcelFormulaError as formula_error:
            ErrorDialog(self, title=EXCEL_FORMULA_ERROR_TITLE,
                        message=EXCEL_FORMULA_ERROR_MESSAGE,
                        additional_info=EXCEL_FORMULA_ADDITIONAL_INFO.format(
                            input_filename, formula_error.formula)).exec()

    def show_comparison(self):
        """ Show the comparison between the Elda process and the SimaPro export process in the tree widget """

        # Removing previous data
        self.treeWidget.clear()

        # Only continue if the SimaPro export process and the Elda process are defined
        if (self.simapro_export_process is None) or (self.elda_process is None):
            return

        # Getting process differences
        differences = compare_processes(self.simapro_export_process, self.elda_process)

        # If there are no differences, show a message and stop and stop the function
        if not differences:
            self.update_processes_summary(message=NO_DIFFERENCES_IN_XLSX_AND_ELDA_MESSAGE, color="green")
            return

        # Enable buttons
        self.overwrite_elda_button.setEnabled(True)
        self.update_last_version_button.setEnabled(True)
        self.add_minor_version_button.setEnabled(True)
        self.add_major_version_button.setEnabled(True)

        # Getting number of differences by category
        nb_metadata_differences = len([x for x in differences.keys() if x not in ('flows', 'parameters')])
        nb_flows_differences = len(differences.get('flows', []))
        nb_params_differences = len(differences.get('parameters', []))

        # Building a message from number of differences of each kind
        delimiter1 = ", " if nb_metadata_differences > 0 and nb_flows_differences > 0 and nb_params_differences > 0 else \
            'and ' if nb_metadata_differences > 0 and nb_flows_differences > 0 and nb_params_differences == 0 else ''
        delimiter2 = 'and ' if nb_params_differences > 0 and (
                nb_flows_differences > 0 or nb_metadata_differences > 0) else ''

        message = "{nb_metadata_diff}{metadata_diff_label}{delimiter1}" \
                  "{nb_flows_diff}{flows_diff_label}{delimiter2}" \
                  "{nb_params_diff}{params_diff_label}".format(nb_metadata_diff=nb_metadata_differences or '',
                                                               metadata_diff_label=" metadata differences "
                                                               if nb_metadata_differences > 0 else '',
                                                               delimiter1=delimiter1,
                                                               nb_flows_diff=nb_flows_differences or '',
                                                               flows_diff_label=" flows differences "
                                                               if nb_flows_differences > 0 else '',
                                                               delimiter2=delimiter2,
                                                               nb_params_diff=nb_params_differences or '',
                                                               params_diff_label=" parameters differences"
                                                               if nb_params_differences > 0 else '', )
        self.update_processes_summary(message=message)

        for attribute, values in differences.items():
            if attribute == 'flows':
                flows_item = QTreeWidgetItem(self.treeWidget, ['Flows'])

                # Looping on each flow differences
                for flow in values:
                    flow_item = QTreeWidgetItem(flows_item, [flow['name'][0] or flow['name'][1]])

                    for flow_attribute, flow_values in flow.items():
                        if flow_attribute != 'name':
                            QTreeWidgetItem(flow_item, [flow_attribute] + [x_str(val) for val in flow_values])

            elif attribute == 'parameters':
                parameters_item = QTreeWidgetItem(self.treeWidget, ['Parameters'])

                # Looping on each parameter differences
                for parameter in values:
                    parameter_item = QTreeWidgetItem(parameters_item, [parameter['name'][0] or parameter['name'][1]])

                    for parameter_attribute, parameter_values in parameter.items():
                        if parameter_attribute != 'name':
                            QTreeWidgetItem(parameter_item,
                                            [parameter_attribute] + [x_str(val) for val in parameter_values])

            else:
                attribute_item = QTreeWidgetItem(self.treeWidget, [attribute] + [x_str(val) for val in values['value']])

                for review_attribute, review_values in values.items():
                    if review_attribute != 'value':
                        QTreeWidgetItem(attribute_item,
                                        [review_attribute] + [x_str(val) for val in review_values])

    def overwrite_elda(self):
        elda = Elda()
        elda.add_version(process=self.simapro_export_process)

        self.save_elda(elda)

    def update_last_version(self):
        elda = Elda(self.elda_edit.text())
        elda.update_last_version(process=self.simapro_export_process)

        self.save_elda(elda)

    def add_minor_version(self):
        elda = Elda(self.elda_edit.text())
        elda.add_version(process=self.simapro_export_process)

        self.save_elda(elda)

    def add_major_version(self):
        elda = Elda(self.elda_edit.text())
        elda.add_version(process=self.simapro_export_process, major_version=True)

        self.save_elda(elda)

    def save_elda(self, elda):
        """ Try to save an Elda on the given filename and handle permission error """
        export_filename = self.elda_edit.text()

        loop = True
        while loop:
            try:
                elda.save(export_filename)
                loop = False
            except PermissionError:
                # Displays a retry/cancel choice in case of permission denied
                retry_cancel = RetryCancelDialog(self, title=PERMISSION_DENIED_TITLE,
                                                 message=PERMISSION_DENIED_MESSAGE,
                                                 additional_info=PERMISSION_DENIED_ADDITIONAL_INFO.format(
                                                     export_filename))
                if retry_cancel.exec() == RetryCancelDialog.Cancel:
                    loop = False

        # Resetting the widgets and displaying a success message
        self.elda_edit.setText('')
        self.simapro_export_edit.setText('')
        self.treeWidget.clear()
        self.update_processes_summary('')
        self.show_message(message=STATUS_MODIFICATION_SUCCESSFUL, message_type=self.SuccessMessage)
