""" Classes used for simapro files handling """
import os
import re

import openpyxl
import jinja2

from eldam.core.lci_data import *
from eldam.utils.lci_data import encode_simapro_csv_format
from eldam.utils.simapro import extract_data_from_comment
from eldam.utils.exceptions import SimaProXlsxError, ParameterConflictError, NotASimaProExportError
from eldam.utils.misc import x_str, remove_duplicates, n_int, n_str
from eldam.utils.xls import clean_row
from eldam.core.parameters import *


class SimaProXlsxReader:
    """ Class used to read a .xlsx SimaPro file. """

    def __init__(self, filepath):
        """
        Args:
            filepath (str): Complete path to the .xlsx SimaPro export
        """

        # Loading the file:
        self.filepath = filepath
        self.workbook = openpyxl.load_workbook(filename=filepath, read_only=False, data_only=True)
        self.worksheet = self.workbook.active

        # Asserting the file is a SimaPro export file (simply check the first two cells)
        if 'SimaPro' not in self.worksheet['A1'].value:
            raise NotASimaProExportError("This file does not seem to be a SimaPro Export")

        # Cleaning the file rows:
        self.cleaned_rows = self.clean_rows()

        # Checking the export type
        # If the processes have been exported from SimaPro's process edition window, the export won't contain
        # project and database level parameters.
        if 'Database Input parameters' not in [row[0].value for row in self.cleaned_rows if len(row) != 0]:
            self.export_type = 'edition_window'
            self.cleaned_rows.append(list())  # Necessary to have the same format as the file exported from LCA Explorer
        else:
            self.export_type = 'lca_explorer'

        # Checking if expression to constants conversion
        # If the processes have been exported with "Convert expressions to constant",
        # there are no categories for parameters
        if 'Input parameters' in [row[0].value for row in self.cleaned_rows if len(row) != 0]:
            self.convert_expressions_to_constants = False
        else:
            self.convert_expressions_to_constants = True

        # Dividing the rows by process and common parameters
        rows = self.divide_rows_by_process()
        self.processes_rows, self.common_parameters_rows = rows[0], rows[1]

        # Getting common parameters data
        self.common_parameters_data = self.get_common_parameters_data()

        # Getting data by process
        self.processes_data = []
        for process_rows in self.processes_rows:
            process_data = self.get_process_data(process_rows)
            process_data.update(self.common_parameters_data)

            self.processes_data.append(process_data)

    def __repr__(self):
        res = ''
        i = 0
        for row in self.cleaned_rows:
            i += 1
            res += str(i) + ' - ' + '|'.join([str(x.value) for x in row]) + '\n'
        return res

    def clean_rows(self):
        """
        Returns a list of every rows cleaned from trailing empty cells and multi-line comments

        Returns:
            list: Cleaned rows
        """

        cleaned_rows = []

        # Runs among every row from the end and starts to insert these rows from the first non empty one.
        start_inserting = False
        for row in reversed(list(self.worksheet.rows)):

            # If it hasn't started to insert rows yet and the row is not empty, starts to insert
            if not start_inserting and len(row) != 0:
                start_inserting = True

            # If it has started to insert, insert the row
            if start_inserting:
                cleaned_rows.append(clean_row(row))

        cleaned_rows.reverse()

        # Merging rows by flow or parameter
        # Some flows or parameters can be dispatched within several rows due to mutli-line comments.
        # This code merges them into one row with line breaks

        # Loops on cleaned row from the end
        for row_index in range(len(cleaned_rows) - 1, -1, -1):
            row = cleaned_rows[row_index]

            # If a row is not empty and its first cell is empty, this row must be merged with the one above it
            if len(row) != 0:
                if row[0].value is None:

                    # Loops on every cell except the first one
                    for cell_index in range(1, len(row)):

                        # If the row has more cells that cell_index (ie, if the cell exists),
                        # merges it with the above cell
                        if (len(cleaned_rows[row_index - 1]) > cell_index) and \
                                (len(cleaned_rows[row_index]) > cell_index):
                            cleaned_rows[row_index - 1][cell_index].value = \
                                '\n'.join(filter(None, (x_str(cleaned_rows[row_index - 1][cell_index].value),
                                                        x_str(cleaned_rows[row_index][cell_index].value))))

                            # Removing trailing newlines
                            cleaned_rows[row_index - 1][cell_index].value = cleaned_rows[row_index - 1][
                                cell_index].value.rstrip()

                        # Else, it means the above row doesn't have this cell, so it copies it from below
                        else:
                            # If the row is completely empty, needs to create one more cell
                            if len(cleaned_rows[row_index - 1]) == 0:
                                cleaned_rows[row_index - 1].append(cleaned_rows[row_index][0])

                            cleaned_rows[row_index - 1].append(cleaned_rows[row_index][cell_index])

                            if cleaned_rows[row_index - 1][cell_index].value is not None:
                                # Adding a line break
                                cleaned_rows[row_index - 1][cell_index].value = '\n' + \
                                                                                cleaned_rows[row_index - 1][
                                                                                    cell_index].value

        # Removes empty rows
        cleaned_rows = [row for row in cleaned_rows if len(row) == 0 or row[0].value is not None]

        return cleaned_rows

    def divide_rows_by_process(self):
        """
        Divides the rows by process
        
        Returns:
            list: List of list of process data rows
        """

        processes_rows = []
        inserting_data = False
        last_category = False
        common_parameters_rows = []
        common_parameters = False

        for row in self.cleaned_rows:

            # Process header
            if len(row) == 1:
                if row[0].value == 'Process':
                    process_data = []
                    inserting_data = True

            # Process data
            if inserting_data:
                process_data.append(row)

            # Process last category
            if len(row) == 1 and inserting_data:
                last_category_label = 'Waste to treatment' if self.convert_expressions_to_constants else 'Calculated parameters'
                if row[0].value == last_category_label:
                    last_category = True

            # If an empty line is met after the last category header, this is the end of the process data
            if len(row) == 0 and last_category:
                processes_rows.append(process_data)
                inserting_data = False
                last_category = False

            # Common parameters
            if len(row) == 1:
                if row[0].value == 'Database Input parameters':
                    common_parameters = True

            if common_parameters:
                common_parameters_rows.append(row)

        return processes_rows, common_parameters_rows

    def get_process_data(self, process_rows):
        """
        Read the process data from its rows
        
        Args:
            process_rows (list): List of rows corresponding to the process 

        Returns:
            dict: Dictionnary containing the process data
        """

        # Initializing process_data
        process_data = {'SimaPro version': self.worksheet['A1'].value,
                        'Date1': self.worksheet['D1'].value.strftime("%d/%m/%Y"),
                        # Date of the export. Date in D22 is the date of creation of the process.
                        'Time': self.worksheet['F1'].value,
                        'Project': self.worksheet['B2'].value}

        # Collecting metadata:
        for row in process_rows:

            # Filtering only rows with 2 not empty cells
            if len(row) == 2 and row[0].value not in ['', 'External documents', 'Literature references']:
                process_data[row[0].value] = row[1].value  # Adding value to data

            # Getting the comment on system description
            if len(row) > 0 and row[0].value == 'System description':
                process_data['Comment on system description'] = \
                    self.worksheet['B' + str(process_rows.index(row) + 1)].value

            # Ending the loop when it reaches products part
            if len(row) == 1 and row[0].value == ['Products']:
                break

        # Collecting other data
        process_data_categories = PROCESS_DATA_CATEGORIES
        if not self.convert_expressions_to_constants:
            process_data_categories = process_data_categories + PROCESS_PARAMETERS_CATEGORIES

        # Ajusting flow categories according if the process is a waste treatment or not
        if process_data['Category type'] == 'Waste treatment':
            process_data_categories = [x for x in process_data_categories if x[0] != 'Products']
        else:
            process_data_categories = [x for x in process_data_categories if x[0] != 'Waste treatment']

        for category_name, field_names, foo in process_data_categories:
            data = self.get_data_by_category(process_rows, category_name, field_names)
            if len(data) > 0:
                process_data[category_name] = data

        return process_data

    def get_common_parameters_data(self):
        """
        Gets database/project parameters data that are present only once at the end of the file but shared by
        every parameters.

        Returns:
            list: A list of dicts with fields as keys
        """

        common_parameters_data = dict()

        # Check if there are common parameters data (if the process has been exported from the process edition window,
        # database and project level parameters aren't exported)
        # If not, returns an empty dict
        if self.export_type == 'edition_window':
            return common_parameters_data

        else:
            for category_name, field_names, not_used_here_but_necessary in COMMON_PARAMETERS_CATEGORIES:
                data = self.get_data_by_category(self.common_parameters_rows, category_name, field_names)
                if len(data) > 0:
                    common_parameters_data[category_name] = data

            return common_parameters_data

    def get_data_by_category(self, rows, category, fields):
        """
        Reads data of every row for a category (flow or parameter) and returns a list of dicts with fields as keys

        Args:
            rows (list): Rows to extract data from
            category (str): Name of the category
            fields (list): Fields for the data

        Returns:
            list: A list of dicts with fields as keys
        """

        data_list = []
        row_index = None

        # Gets the number of the row containing category header
        for row in rows:

            if len(row) != 0 and row[0].value == category:
                row_index = rows.index(row)  # - 1 is because indexing begins at 0 in Python
                break  # Ends the for loop (no need to go further)

        # If a row seems to correspond to a category header
        if row_index is not None:
            # Skips the category row
            row_index += 1
            next_row = []

            # Loops on every row of the category
            while True:  # Infinite loop, will not stop untill a break statement

                # If the last row have been reached, ends the loop
                if row_index >= len(rows):
                    break

                row_data = {}  # Dict for storing data of the row

                flow_row = next_row or rows[row_index]

                # Defining next_row
                if row_index < (len(rows) - 1):
                    next_row = rows[row_index + 1]

                # If the row is empty and the next row has only the first cell filled (new category flow) or no cell
                # filled, ends the loop
                if len(flow_row) == 0 and len(next_row) <= 1:
                    break

                # Handling cases of UUID like data added to the comment
                if (len(flow_row) == len(fields) + 1) \
                        and (re.match(r'\n*\w{8}-\w{4}-\w{4}-\w{4}-\w{12}', flow_row[-1].value) is not None):
                    flow_row = flow_row[:-1]

                # Raises an error if there is a row longer than the number of fields
                if len(flow_row) > len(fields):
                    raise SimaProXlsxError(
                        f"Function get_data_by_category have been called with category='{category}' and "
                        f"fields={fields}, but there are more data than fields at row {row_index + 1}."
                        f"\nFile: '{self.filepath}'")
                else:
                    # Loops on every cell of the row and inserts its value in row_data
                    for cell_index, field in enumerate(fields):

                        # If the cell index is higher than the number of cells in the row or if the value is an empty
                        # string, attributes None to the field
                        if cell_index < len(flow_row):
                            cell_value = flow_row[cell_index].value
                            if type(cell_value) == str:
                                string_value = cell_value.strip()
                                if string_value != '':
                                    row_data[field] = string_value
                            else:
                                row_data[field] = cell_value
                        else:
                            row_data[field] = None

                    # Inserts row_data in the list to be returned
                    data_list.append(row_data)

                    # Gets to the next row
                    row_index += 1

        else:
            raise SimaProXlsxError(
                f"Function get_data_by_category have been called with category='{category}', but there is no line "
                f"that correspond to this category.\nFile: '{self.filepath}'.")

        return data_list

    def to_processes(self):
        """
        Method used to transform SimaProXlsxReader data into an instance of Process

        Returns:
            list of Process: List of processes described in the SimaProXlsxReader
        """

        processes = []

        for data in self.processes_data:

            # Process metadata
            # Extracting supplementary metadata from the comment
            comment_data = extract_data_from_comment(data.get('Comment', None))
            data = {**data, **comment_data}
            data = {k: v for k, v in data.items() if v != 'None'}

            process = Process(name=data.get('Process name', None),
                              synonym=data.get('synonym', None),
                              category_type=data.get('Category type', None),
                              date=data.get('Date1', None),
                              comment=data.get('comment', None),
                              allocation_rules=data.get('Allocation rules', None),
                              author=data.get('Generator', None),
                              contact=data.get('contact', None),
                              long_term_contact=data.get('long_term_contact', None),
                              step=data.get('step', None),
                              project=data.get('Project', None),
                              step_in_project=data.get('step_in_project', None),
                              reference_period=data.get('reference_period', None),
                              time_validity_limit=data.get('time_validity_limit', None),
                              geographic_representativeness=data.get('geographic_representativeness', None),
                              technology_description=data.get('technology_description', None),
                              technology_scale=data.get('technology_scale', None),
                              technology_level=data.get('technology_level', None),
                              input_mass=data.get('input_mass', None),
                              output_mass=data.get('output_mass', None),
                              version_creator=data.get('version_creator', None),
                              version_contact=data.get('version_contact', None),
                              version_comment=data.get('version_comment', None),
                              inventory_review_state=data.get('inventory_review_state', None),
                              metadata_review=data.get('metadata_review', dict()))

            # Process flows
            for flow_category in FLOW_CATEGORIES:
                # Looping on every flow of this category on data from SimaPro
                if flow_category[0] in data.keys():  # Asserts some data exists for this category
                    flows_data = data[flow_category[0]]

                    for flow_data in flows_data:
                        # Getting non empty data dict that correspond to a process flow data
                        non_empty_flow_data = {x[0]: x[1] for x in flow_data.items() if
                                               x[0] in SIMAPRO_FLOW_FIELDS_NAMES}

                        # Extracting data contained in the comment such as modification code or relevance comment
                        comment_data = extract_data_from_comment(non_empty_flow_data.get('Comment', None))
                        non_empty_flow_data = {**non_empty_flow_data, **comment_data}

                        flow = FlowFactory.create_flow(name=non_empty_flow_data.get('Name', None),
                                                       type=flow_category[2]['Type'],
                                                       unit=non_empty_flow_data.get('Unit', None),
                                                       amount=non_empty_flow_data.get('Amount', None),
                                                       library=non_empty_flow_data.get('library', None),
                                                       data_source=non_empty_flow_data.get('data_source', None),
                                                       comment=non_empty_flow_data.get('comment', None),
                                                       review_state=non_empty_flow_data.get('review_state', 0),
                                                       comment_for_reviewer=non_empty_flow_data.get(
                                                           'comment_for_reviewer',
                                                           None),
                                                       reviewer_comment=non_empty_flow_data.get('reviewer_comment',
                                                                                                None),
                                                       uncertainty=non_empty_flow_data.get('Distribution', 'Undefined'),
                                                       stdev=non_empty_flow_data.get('SD2 or 2SD', None),
                                                       min_value=non_empty_flow_data.get('Min', None),
                                                       max_value=non_empty_flow_data.get('Max', None))

                        if flow.type in PRODUCT_FLOW_TYPES:
                            if non_empty_flow_data.get('Waste type', None) in ('not defined', 'All waste types'):
                                non_empty_flow_data['Waste type'] = None

                            flow.waste_type = non_empty_flow_data.get('Waste type', None)
                            flow.category = non_empty_flow_data.get('Category', 'Materials')
                            flow.allocation = n_str(non_empty_flow_data.get('Allocation %', None))

                        elif flow.type in TECHNOSPHERE_FLOW_TYPES:
                            flow.modification_code = n_int(non_empty_flow_data.get('modification_code', None))
                            flow.modification_comment = non_empty_flow_data.get('modification_comment', None)
                            flow.relevance_code = non_empty_flow_data.get('relevance_code', None)
                            flow.relevance_comment = non_empty_flow_data.get('relevance_comment', None)
                            flow.confidence_code = non_empty_flow_data.get('confidence_code', None)
                            flow.confidence_comment = non_empty_flow_data.get('confidence_comment', None)

                        elif flow.type in BIOSPHERE_FLOW_TYPES:
                            compartment = flow_category[2].get('Compartment')

                            flow.compartment = non_empty_flow_data.get('Compartment', compartment)
                            flow.sub_compartment = non_empty_flow_data.get('Sub-compartment', None)
                            flow.relevance_code = non_empty_flow_data.get('relevance_code', None)
                            flow.relevance_comment = non_empty_flow_data.get('relevance_comment', None)
                            flow.confidence_code = non_empty_flow_data.get('confidence_code', None)
                            flow.confidence_comment = non_empty_flow_data.get('confidence_comment', None)

                        process.add_flow(flow)

            # Process parameters
            # Looping on every parameter type
            for parameter_type in [x[0] for x in PARAMETER_CATEGORIES]:

                # Looping on parameters
                for parameter_data in data.get(parameter_type, []):

                    # Getting parameter level
                    if 'Project' in parameter_type:
                        level = 'Project'
                    elif 'Database' in parameter_type:
                        level = 'Database'
                    else:
                        level = 'Process'

                    comment_data = extract_data_from_comment(parameter_data.get('Comment', None))
                    parameter_data = {**parameter_data, **comment_data}

                    # Adding parameter to the process
                    if 'Input' in parameter_type:

                        # Removing 'Undefined' distributions
                        if parameter_data.get('Distribution') == 'Undefined':
                            parameter_data['Distribution'] = None

                        process.add_parameter(InputParameter(name=parameter_data.get('Name', None),
                                                             comment=parameter_data.get('comment', None),
                                                             value=parameter_data.get('Value', None),
                                                             uncertainty=parameter_data.get('Distribution', None),
                                                             stdev=parameter_data.get('SD2 or 2SD', None),
                                                             min_value=parameter_data.get('Min', None),
                                                             max_value=parameter_data.get('Max', None),
                                                             review_state=parameter_data.get('review_state', 0),
                                                             comment_for_reviewer=parameter_data.get(
                                                                 'comment_for_reviewer',
                                                                 None),
                                                             reviewer_comment=parameter_data.get('reviewer_comment',
                                                                                                 None),
                                                             level=level))
                    elif 'Calculated' in parameter_type:
                        process.add_parameter(CalculatedParameter(name=parameter_data.get('Name', None),
                                                                  comment=parameter_data.get('comment', None),
                                                                  formula=str(
                                                                      parameter_data.get('Expression', None) or ''),
                                                                  review_state=parameter_data.get('review_state', 0),
                                                                  comment_for_reviewer=parameter_data.get(
                                                                      'comment_for_reviewer',
                                                                      None),
                                                                  reviewer_comment=parameter_data.get(
                                                                      'reviewer_comment',
                                                                      None),
                                                                  level=level))

            processes.append(process)

        return processes


class SimaProCsvWriter:
    """ Class used to write a SimaPro .csv import file from a process """

    def __init__(self, *args, chosen_parameters=list(), elda_only_data=True):
        """
        Args:
            *args (Process): Processe(s) to export in the csv file
            chosen_parameters (list of InputParameter or CalculatedParameter): Parameters chosen by the user in case of conflict on conflict on database/project parameters
            elda_only_data (bool): Should data that are used by ELDAM but not by SimaPro be embeded in the comment


        Raises:
            ParameterConflictError:
                Exception raised if several database/project level parameters have the same name but not the same
                values. The exception arguments contains the conflictual parameters.
        """

        self.processes = args
        self.elda_only_data = elda_only_data

        # Getting a list of the names of the chosen parameters
        chosen_parameters_names = [param.name for param in chosen_parameters]

        # Gathering database/project parameters from every processes
        database_input_parameters = []
        database_calculated_parameters = []
        project_input_parameters = []
        project_calculated_parameters = []

        for process in self.processes:
            database_input_parameters += [param for param
                                          in process.input_parameters
                                          if param.level == 'Database'
                                          and param not in database_input_parameters
                                          and param.name not in chosen_parameters_names]
            database_calculated_parameters += [param for param
                                               in process.calculated_parameters
                                               if param.level == 'Database'
                                               and param not in database_calculated_parameters
                                               and param.name not in chosen_parameters_names]
            project_input_parameters += [param for param
                                         in process.input_parameters
                                         if param.level == 'Project'
                                         and param not in project_input_parameters
                                         and param.name not in chosen_parameters_names]
            project_calculated_parameters += [param for param
                                              in process.calculated_parameters
                                              if param.level == 'Project'
                                              and param not in project_calculated_parameters
                                              and param.name not in chosen_parameters_names]

        # Checking database/project parameters conflict
        all_parameters = database_input_parameters + database_calculated_parameters + \
                         project_input_parameters + project_calculated_parameters
        all_parameters_names = set([param.name for param in all_parameters])

        conflicts = []
        for name in all_parameters_names:

            # Getting every conflictual parameters of this name
            conflict_parameters = remove_duplicates([param for param in all_parameters if param.name == name])

            if len(conflict_parameters) > 1:
                conflicts.append(conflict_parameters)

        # If there are parameters in conflict, raises an exception passing conflictual parameters
        if conflicts:
            raise ParameterConflictError(conflicts)

        # Adding chosen parameters
        database_input_parameters += [param for param in chosen_parameters
                                      if param.type == 'Input parameter' and param.level == 'Database']
        database_calculated_parameters += [param for param in chosen_parameters
                                           if param.type == 'Calculated parameter' and param.level == 'Database']
        project_input_parameters += [param for param in chosen_parameters
                                     if param.type == 'Input parameter' and param.level == 'Project']

        project_calculated_parameters += [param for param in chosen_parameters
                                          if param.type == 'Calculated parameter' and param.level == 'Project']

        # Creating the strings to integrate in the csv for each parameter category
        self.database_input_parameters = '\n'.join([param.simapro_csv_format(elda_only_data=self.elda_only_data)
                                                    for param in database_input_parameters])
        self.database_calculated_parameters = '\n'.join([param.simapro_csv_format(elda_only_data=self.elda_only_data)
                                                         for param in database_calculated_parameters])
        self.project_input_parameters = '\n'.join([param.simapro_csv_format(elda_only_data=self.elda_only_data)
                                                   for param in project_input_parameters])
        self.project_calculated_parameters = '\n'.join([param.simapro_csv_format(elda_only_data=self.elda_only_data)
                                                        for param in project_calculated_parameters])

    def to_csv(self, filepath):
        """
        Exports the SimaProCsvWriter process to a SimaPro .csv import file

        Args:
            filepath (str): Path to the export file
        """

        # Replacing data in the file template using jinja2
        env = jinja2.Environment(trim_blocks=True,
                                 lstrip_blocks=True)

        template_path = os.path.join(JINJA2_TEMPLATES_FOLDER, 'simapro_csv_template.jinja2')
        with open(template_path, 'r') as file:
            template_string = file.read()
        template = env.from_string(template_string)

        # OLD: Use of get_template was abandonned as it let to compilation issues:
        # https://github.com/pyinstaller/pyinstaller/issues/1898
        # env = jinja2.Environment(
        #     loader=jinja2.PackageLoader('eldam.core', 'templates'),
        #     trim_blocks=True,
        #     lstrip_blocks=True
        # )
        #
        # template = env.get_template('simapro_csv_template.jinja2')

        result = template.render(processes=self.processes,
                                 database_input_parameters=self.database_input_parameters,
                                 database_calculated_parameters=self.database_calculated_parameters,
                                 project_input_parameters=self.project_input_parameters,
                                 project_calculated_parameters=self.project_calculated_parameters,
                                 elda_only_data=self.elda_only_data,
                                 encode_simapro_csv_format=encode_simapro_csv_format)

        # Writing the file
        with open(filepath, 'w', encoding='cp1252') as export_file:
            export_file.write(result)
