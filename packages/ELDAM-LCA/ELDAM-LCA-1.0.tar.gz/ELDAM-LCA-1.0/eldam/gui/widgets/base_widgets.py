from abc import ABCMeta, abstractmethod
import os
import re

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTreeWidgetItem
from PyQt5.QtGui import QColor

from eldam.gui.dialogs import WarningDialog
from eldam.gui.gui_parameters import *

from eldam.core.parameters import PROCESS_ATTRIBUTES, PRODUCT_FLOW_ATTRIBUTES, TECHNOSPHERE_FLOW_ATTRIBUTES, \
    BIOSPHERE_FLOW_ATTRIBUTES, INPUT_PARAMETERS_ATTRIBUTES, CALCULATED_PARAMETERS_ATTRIBUTES

from eldam.utils.observer import Suscriber
from eldam.utils.gui import name_from_pattern
from eldam.utils.exceptions import ConversionError


class EldamWidget(QWidget):
    """ Base class used by every top level widgets """
    StandardMessage = 1
    SuccessMessage = 2
    ErrorMessage = 3

    def __init__(self, ui_file, *args, **kwargs):
        """
        Args:
            ui_file (str): Path to QtDesigner .ui file
        """
        super().__init__(*args, **kwargs)

        self.ui = uic.loadUi(ui_file, self)

    def show_message(self, message, message_type=StandardMessage, time=STATUS_BAR_MESSAGES_TIME):

        if message_type == self.SuccessMessage:
            self.window().statusBar.setStyleSheet(STATUS_BAR_SUCCESS_STYLESHEET)
        elif message_type == self.ErrorMessage:
            self.window().statusBar.setStyleSheet(STATUS_BAR_ERROR_STYLESHEET)
        else:
            self.window().statusBar.setStyleSheet(STATUS_BAR_DEFAULT_STYLESHEET)

        self.window().statusBar.showMessage(message, time)


class AbcAndPyQtMeta(type(QWidget), ABCMeta):
    """ Class used to solve metaclass conflicts and allow to inherit from ABC classes and PyQt classes """


class EldamWidgetWithProgressBar(EldamWidget, Suscriber, metaclass=AbcAndPyQtMeta):

    def update(self, step, current, total):
        """ Function used by the observer pattern """
        self.update_progressbar(step, current, total)

    def update_progressbar(self, step, current, total):
        """
        Updates the progressbar

        Can be triggered manually or by the overridden method update() of the Suscriber parent class

        Args:
            step (str): Current Step
            current (int): Current value
            total (int): Maximum value
        """
        if current == total:
            self.show_message(message_type=EldamWidget.SuccessMessage, message=step)
        else:
            self.show_message(f"{step}...", time=-1)  # time=-1 keeps the message alive until it is changed

        # Avoiding the "infinite" progressbar display
        if total == 0:
            total = 1

        self.progressBar.setRange(0, total)
        self.progressBar.setValue(current)


class EldamWidgetWithProcessSummary(EldamWidget):
    """ Widgets with a processes_summary QLabel """

    def update_processes_summary(self, message: str, color: str = None):
        """ Update the message in the process summary label """
        if not color:
            color = "black"

        self.processes_summary.setText(message)
        self.processes_summary.setStyleSheet("QLabel{color: " + color + "};}")


class EldamConversionWidget(EldamWidgetWithProcessSummary, metaclass=AbcAndPyQtMeta):
    """ Special class for ELDAM widgets with a tree widget to display processes and methods to convert processes """

    # Constants used to set the state of the TreeWidget
    DETAILED_VIEW = 1
    QUALITY_CHECK = 2

    def __init__(self, ui_file, *args, **kwargs):
        super().__init__(ui_file, *args, **kwargs)

        self.processes = list()
        self.exports_parameters = list()

        # Setting TreeWidget first column width
        self.treeWidget.setColumnWidth(0, 250)

        # Alternating row colors
        self.treeWidget.setAlternatingRowColors(True)

        # Adding a separator between columns
        self.treeWidget.setStyleSheet(QTREEWIDGET_STYLESHEET)

        self.display_mode = self.DETAILED_VIEW  # Setting the default tree widget display mode
        self.toggle_display_button.clicked.connect(self.toggle_display_mode)

        self.main_button.clicked.connect(self.convert)

    def toggle_display_mode(self):
        """ Changes the display mode from detailed view to quality check and inversely """
        if self.display_mode == self.DETAILED_VIEW:
            self.show_quality_check_view()

        elif self.display_mode == self.QUALITY_CHECK:
            self.show_detailed_view()

    @abstractmethod
    def read_processes(self):
        """ Read the input files """

    def show_detailed_view(self):
        """ Display the read processes in the tree widget """

        # Setting the display mode
        if self.display_mode == self.QUALITY_CHECK:
            self.toggle_display_button.setText("Quality check")  # Changing the button text
            self.display_mode = self.DETAILED_VIEW

        # Updating the process summary
        if len(self.processes) > 0:
            self.update_processes_summary(message=PROCESSES_READ_MESSAGE.format(len(self.processes)))

        # Removing previous data
        self.treeWidget.clear()

        # Building the tree widget
        for process in self.processes:
            process_item = QTreeWidgetItem(self.treeWidget, [process.name or 'Process with no name'])
            process_item.setExpanded(True)

            for attr in PROCESS_ATTRIBUTES.items():
                QTreeWidgetItem(process_item, [attr[1], str(getattr(process, attr[0]) or '')])

            # Inserting flows
            # Product flows
            product_flows_item = QTreeWidgetItem(process_item, ['Product flows',
                                                                f"{len(process.product_flows)} product flow(s)"])

            for flow in process.product_flows:
                flow_item = QTreeWidgetItem(product_flows_item, [flow.type, flow.name])

                for attr in PRODUCT_FLOW_ATTRIBUTES.items():
                    QTreeWidgetItem(flow_item, [attr[1], str(getattr(flow, attr[0]) or '')])

            # Technosphere flows
            technosphere_flows_item = QTreeWidgetItem(process_item, ['Technosphere flows',
                                                                     f"{len(process.technosphere_flows)} "
                                                                     f"technosphere flow(s)"])

            for flow in process.technosphere_flows:
                flow_item = QTreeWidgetItem(technosphere_flows_item, [flow.type, flow.name])

                for attr in TECHNOSPHERE_FLOW_ATTRIBUTES.items():
                    QTreeWidgetItem(flow_item, [attr[1], str(getattr(flow, attr[0]) or '')])

            # Biosphere flows
            biosphere_flows_item = QTreeWidgetItem(process_item, ['Biosphere flows',
                                                                  f"{len(process.biosphere_flows)} biosphere flow(s)"])
            for flow in process.biosphere_flows:
                flow_item = QTreeWidgetItem(biosphere_flows_item, [flow.type, flow.name])

                for attr in BIOSPHERE_FLOW_ATTRIBUTES.items():
                    QTreeWidgetItem(flow_item, [attr[1], str(getattr(flow, attr[0]) or '')])

            # Parameters
            # Input parameters
            input_parameters_item = QTreeWidgetItem(process_item, ['Input parameters',
                                                                   f"{len(process.input_parameters)} "
                                                                   f"input parameter(s)"])

            for parameter in process.input_parameters:
                parameter_item = QTreeWidgetItem(input_parameters_item, [parameter.type, parameter.name])

                for attr in INPUT_PARAMETERS_ATTRIBUTES.items():
                    QTreeWidgetItem(parameter_item, [attr[1], str(getattr(parameter, attr[0]) or '')])

            # Calculated parameters
            calculated_parameters_item = QTreeWidgetItem(process_item, ['Calculated parameters',
                                                                        f"{len(process.calculated_parameters)} "
                                                                        f"calculated parameter(s)"])

            for parameter in process.calculated_parameters:
                parameter_item = QTreeWidgetItem(calculated_parameters_item, [parameter.type, parameter.name])

                for attr in CALCULATED_PARAMETERS_ATTRIBUTES.items():
                    QTreeWidgetItem(parameter_item, [attr[1], str(getattr(parameter, attr[0]) or '')])

    def show_quality_check_view(self):
        """ Shows a quality data check of the read processes in the tree widget """

        # Setting the display mode
        if self.display_mode == self.DETAILED_VIEW:
            self.toggle_display_button.setText("Detailed view")  # Changing the button text
            self.display_mode = self.QUALITY_CHECK

        # Removing previous data
        self.treeWidget.clear()

        # Building the tree widget
        # Getting processes and flows missing quality data
        incomplete_processes = []
        for process in self.processes:
            incomplete_flows = []

            for flow in process.technosphere_flows + process.biosphere_flows:
                if len(flow.missing_quality_data) > 0:
                    incomplete_flows.append(flow)

            if len(incomplete_flows) > 0:
                process_item = QTreeWidgetItem(self.treeWidget, [process.name or 'Process with no name',
                                                                 MISSING_QUALITY_DATA_DETAIL_MESSAGE.format(
                                                                     len(incomplete_flows))])
                process_item.setExpanded(True)

                incomplete_processes.append(process)

                # Technosphere flows
                incomplete_technosphere_flows = [flow for flow in incomplete_flows if
                                                 flow in process.technosphere_flows]

                technosphere_flows_item = QTreeWidgetItem(process_item, ['Technosphere flows',
                                                                         MISSING_QUALITY_DATA_DETAIL_MESSAGE.format(
                                                                             len(incomplete_technosphere_flows))])

                for flow in incomplete_technosphere_flows:
                    flow_item = QTreeWidgetItem(technosphere_flows_item, [flow.type, flow.name])

                    for attr in TECHNOSPHERE_FLOW_ATTRIBUTES.items():
                        # Inserting attributes with a different background color for missing quality data attributes
                        attr_item = QTreeWidgetItem(flow_item, [attr[1], str(getattr(flow, attr[0]) or '')])

                        if attr[0] in flow.missing_quality_data:
                            attr_item.setBackground(1, QColor('lightcoral'))

                # Biosphere flows
                incomplete_biosphere_flows = [flow for flow in incomplete_flows if flow in process.biosphere_flows]

                biosphere_flows_item = QTreeWidgetItem(process_item, ['Biosphere flows',
                                                                      MISSING_QUALITY_DATA_DETAIL_MESSAGE.format(
                                                                          len(incomplete_technosphere_flows))])

                for flow in incomplete_biosphere_flows:
                    flow_item = QTreeWidgetItem(biosphere_flows_item, [flow.type, flow.name])

                    for attr in BIOSPHERE_FLOW_ATTRIBUTES.items():
                        # Inserting attributes with a different background color for missing quality data attributes
                        attr_item = QTreeWidgetItem(flow_item, [attr[1], str(getattr(flow, attr[0]) or '')])

                        if attr[0] in flow.missing_quality_data:
                            attr_item.setBackground(1, QColor('lightcoral'))

        # Updating the message
        if len(self.processes) > 0:
            if len(incomplete_processes) == 0:
                message = NO_ERRORS_FOUND_MESSAGE.format(len(self.processes))
                color = 'green'
            else:
                message = MISSING_QUALITY_DATA_MESSAGE.format(len(incomplete_processes))
                color = 'darkorange'

            self.update_processes_summary(message=message, color=color)

    def build_export_list(self):
        """ Building a list of items containing the process to export and the filename of the export  """

        self.exports_parameters = []  # Resetting the list
        multiple_products_for_file_naming_warning = False
        exported_filenames = []  # Storing the saved filenames for comparison

        for process in self.processes:
            # If multiple processes, generate filename from pattern
            if len(self.processes) == 1:
                export_filename = self.save_edit.text()
            else:
                directory, pattern = os.path.split(self.save_edit.text())

                if 'PRODUCT' in pattern and process.product is None:
                    multiple_products_for_file_naming_warning = True

                export_filename = name_from_pattern(pattern, process.name or 'process',
                                                    process.product.name if process.product is not None
                                                    else process.product_flows[0].name)

                # Replacing forbidden symbols from filename by "_"
                export_filename = re.sub(r'[^\w\-_\. ]', '_', export_filename)

                # Looping on already existing filenames to add a number after the file name in case of duplicates
                # Removing extension
                filename, extension = os.path.splitext(export_filename)
                while filename in exported_filenames:
                    parse = re.search("(?P<filename>.*)_\((?P<number>\d+)\)", filename)

                    if parse is not None:
                        number = str(int(parse['number']) + 1)
                        filename = parse['filename'] + '_(' + number + ')'
                    else:
                        filename = filename + '_(2)'
                filename = filename + extension

                export_filename = os.path.join(directory, filename)

            # Adding the export filename to the list
            exported_filenames.append(export_filename)

            # Adding the export parameters to the list
            self.exports_parameters.append({'process': process, 'export_filename': export_filename})

        # If a filename have been computed from a pattern using the PRODUCT tag and the corresponding process has
        # multiple products, warn the user
        if multiple_products_for_file_naming_warning:
            WarningDialog(self, title=MULTIPLE_PRODUCTS_FOR_FILE_NAMING_TITLE,
                          message=MULTIPLE_PRODUCTS_FOR_FILE_NAMING_MESSAGE).exec()

    @property
    def export_conflicts(self):
        """ For each export, check if the file already exists """
        return [export for export in self.exports_parameters if os.path.isfile(export['export_filename'])]

    @abstractmethod
    def resolve_export_conflicts(self):
        """ For each export, check if the filename doesn't already exists. If yes, obtain the desired file handling """

    @abstractmethod
    def export_processes(self):
        """ Export the processes from the export parameters list """

    def convert(self):
        """
        Export the read processes to files of the corresponding output

        This function operates in three steps:
        1. Building the export list:
        2. Resolving export conflicts:
        3. Exporting the processes
        """

        try:
            self.build_export_list()
            self.resolve_export_conflicts()
            self.export_processes()
        except ConversionError:
            pass
