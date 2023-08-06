""" Parameters, values, cell coordinates etc.. used in ELDAM core code """
from collections import OrderedDict

from openpyxl.utils import quote_sheetname

from eldam.utils.misc import find_data_file
from eldam.settings import ELDA_TEMPLATE_VERSION

ELDA_TEMPLATE_FILEPATH = find_data_file('files/EldaTemplate.xlsm')
ELDA_INDEX_FILEPATH = find_data_file('files/EldaIndex.xlsx')
JINJA2_TEMPLATES_FOLDER = find_data_file('files/templates')

# Lists of field names for every flow field
SP_PRODUCT_FIELDS = ['Name', 'Amount', 'Unit', 'Allocation %', 'Waste type', 'Category', 'Comment']
SP_WASTE_TREATMENT_FIELDS = ['Name', 'Amount', 'Unit', 'Waste type', 'Category', 'Comment']
SP_TECHNOSPHERE_FIELDS = ['Name', 'Amount', 'Unit', 'Distribution', 'SD2 or 2SD', 'Min', 'Max', 'Comment']
SP_BIOSPHERE_FIELDS = ['Name', 'Sub-compartment', 'Amount', 'Unit', 'Distribution', 'SD2 or 2SD', 'Min', 'Max',
                       'Comment']
SP_INPUT_PARAMETER_FIELDS = ['Name', 'Value', 'Distribution', 'SD2 or 2SD', 'Min', 'Max', 'Hide', 'Comment']
SP_CALCULATED_PARAMETER_FIELDS = ['Name', 'Expression', 'Comment']

# List of categories used with function SimaProXlsxReader.get_data_by_category()
# for importing data of each category
# Also used by Elda.__init__() to add additional data according to flow category
# List of tuples constituted as:
# (Name of the category in the xlsx file, Field names, {Data to add: Value})
FLOW_CATEGORIES = [('Products', SP_PRODUCT_FIELDS, {'Type': 'Output/Technosphere/Product'}),
                   ('Waste treatment', SP_WASTE_TREATMENT_FIELDS,
                    {'Type': 'Output/Technosphere/Waste treatment product'}),
                   ('Avoided products', SP_TECHNOSPHERE_FIELDS, {'Type': 'Output/Technosphere/Avoided product'}),
                   ('Materials/fuels', SP_TECHNOSPHERE_FIELDS, {'Type': 'Input/Technosphere'}),
                   ('Electricity/heat', SP_TECHNOSPHERE_FIELDS, {'Type': 'Input/Technosphere'}),
                   ('Resources', SP_BIOSPHERE_FIELDS, {'Type': 'Input/Nature'}),
                   ('Emissions to air', SP_BIOSPHERE_FIELDS, {'Type': 'Output/Emission', 'Compartment': 'Air'}),
                   ('Emissions to water', SP_BIOSPHERE_FIELDS, {'Type': 'Output/Emission', 'Compartment': 'Water'}),
                   ('Emissions to soil', SP_BIOSPHERE_FIELDS, {'Type': 'Output/Emission', 'Compartment': 'Soil'}),
                   ('Final waste flows', SP_BIOSPHERE_FIELDS, {'Type': 'Output/Final waste flows'}),
                   ('Waste to treatment', SP_TECHNOSPHERE_FIELDS, {'Type': 'Output/Technosphere/Waste'})]

PARAMETER_CATEGORIES = [('Input parameters', {'Type': 'Input parameter', 'Level': 'Process'}),
                        ('Calculated parameters', {'Type': 'Calculated parameter', 'Level': 'Process'}),
                        ('Database Input parameters', {'Type': 'Input parameter', 'Level': 'Database'}),
                        ('Database Calculated parameters', {'Type': 'Calculated parameter', 'Level': 'Database'}),
                        ('Project Input parameters', {'Type': 'Input parameter', 'Level': 'Project'}),
                        ('Project Calculated parameters', {'Type': 'Calculated parameter', 'Level': 'Project'})]

PROCESS_DATA_CATEGORIES = FLOW_CATEGORIES + [('Non material emissions', SP_BIOSPHERE_FIELDS, {}),
                                             ('Social issues', SP_BIOSPHERE_FIELDS, {}),
                                             ('Economic issues', SP_BIOSPHERE_FIELDS, {})]

PROCESS_PARAMETERS_CATEGORIES = [('Input parameters', SP_INPUT_PARAMETER_FIELDS, {}),
                                 ('Calculated parameters', SP_CALCULATED_PARAMETER_FIELDS, {})]

COMMON_PARAMETERS_CATEGORIES = [('Database Input parameters', SP_INPUT_PARAMETER_FIELDS, {}),
                                ('Database Calculated parameters', SP_CALCULATED_PARAMETER_FIELDS, {}),
                                ('Project Input parameters', SP_INPUT_PARAMETER_FIELDS, {}),
                                ('Project Calculated parameters', SP_CALCULATED_PARAMETER_FIELDS, {})]

# Dictionary mapping flow field names to Elda column
SIMAPRO_FLOW_FIELDS_NAMES = ['Type',
                             'Name',
                             'Amount',
                             'Unit',
                             'Allocation %',
                             'Waste type',
                             'Comment',
                             'Distribution',
                             'SD2 or 2SD',
                             'Min',
                             'Max',
                             'Sub-compartment',
                             'Compartment',
                             'Category']

PRODUCT_FLOW_TYPES = ['Output/Technosphere/Product', 'Output/Technosphere/Waste treatment product']
TECHNOSPHERE_FLOW_TYPES = ['Output/Technosphere/Avoided product', 'Output/Technosphere/Waste',
                           'Input/Technosphere']
BIOSPHERE_FLOW_TYPES = ['Input/Nature', 'Output/Emission', 'Output/Final waste flows']

# Used to show data in the GUI
PROCESS_ATTRIBUTES = OrderedDict(name='Name', date='Date', category_type="Category type", project='Project',
                                 author='Author', allocation_rules='Allocation rules', comment='Comment')
PRODUCT_FLOW_ATTRIBUTES = OrderedDict(name='Name', type='Type', unit='Unit', amount='Amount', category='Category',
                                      waste_type='Waste type', allocation='Allocation', data_source='Data source',
                                      library='Library', comment='Comment', review_state='Review state',
                                      comment_for_reviewer='Comment for reviewer',
                                      reviewer_comment='Reviewer comment', uncertainty='Uncertainty', stdev='StDev',
                                      min_value='Min', max_value='Max')
TECHNOSPHERE_FLOW_ATTRIBUTES = OrderedDict(name='Name', type='Type', unit='Unit', amount='Amount',
                                           data_source='Data source', library='Library', comment='Comment',
                                           review_state='Review state', comment_for_reviewer='Comment for reviewer',
                                           reviewer_comment='Reviewer comment', uncertainty='Uncertainty',
                                           stdev='StDev', min_value='Min', max_value='Max',
                                           modification_code='Modification code',
                                           modification_comment='Modification comment', relevance_code='Relevance code',
                                           relevance_comment='Relevance comment', confidence_code='Confidence code',
                                           confidence_comment='Confidence comment')
BIOSPHERE_FLOW_ATTRIBUTES = OrderedDict(name='Name', type='Type', compartment='Compartment',
                                        sub_compartment='Sub-compartment', unit='Unit', amount='Amount',
                                        data_source='Data source', library='Library', comment='Comment',
                                        review_state='Review state', comment_for_reviewer='Comment for reviewer',
                                        reviewer_comment='Reviewer comment', uncertainty='Uncertainty', stdev='StDev',
                                        min_value='Min', max_value='Max', relevance_code='Relevance code',
                                        relevance_comment='Relevance comment', confidence_code='Confidence code',
                                        confidence_comment='Confidence comment')
INPUT_PARAMETERS_ATTRIBUTES = OrderedDict(name='Name', value_or_formula='Value', uncertainty='Uncertainty',
                                          stdev='StDev', min_value='Min', max_value='Max', comment='Comment',
                                          review_state='Review state', comment_for_reviewer='Comment for reviewer',
                                          reviewer_comment='Reviewer comment', level='Level')
CALCULATED_PARAMETERS_ATTRIBUTES = OrderedDict(name='Name', value_or_formula='Value', comment='Comment',
                                               review_state='Review state', comment_for_reviewer='Comment for reviewer',
                                               reviewer_comment='Reviewer comment', level='Level')

# Review attributes names
REVIEW_ATTRIBUTES = ['value', 'comment', 'comment_for_reviewer', 'review_state', 'reviewer_comment']

# SimaPro built-in variables, lowercase only
# Seems that Pi is the only SimaPro built-in variable.
SIMAPRO_BUILT_IN_VARIABLES = {'pi': '3.1415926535',
                              'Pi': '3.1415926535',
                              'PI': '3.1415926535'}

ELDA_INDEX_COLUMNS = {'file_name': 'A',
                      'location': 'B',
                      'process_name': 'C',
                      'project': 'D',
                      'comment': 'E',
                      'author': 'F',
                      'contact': 'G',
                      'long_term_contact': 'H',
                      'last_version': 'I',
                      'last_version_date': 'J',
                      'status': 'K',
                      'product_flows': 'L',
                      'technosphere_flows_nb': 'M',
                      'biosphere_flows_nb': 'N',
                      'input_parameters_nb': 'O',
                      'calculated_parameters_nb': 'P'
                      }

ELDA_INDEX_COLUMNS_TO_CENTER = ['last_version', 'technosphere_flows_nb', 'biosphere_flows_nb',
                                'input_parameters_nb',
                                'calculated_parameters_nb']

# Process attributes that can be copied by the "Copy Elda metadata" feature
ATTRIBUTES_TO_COPY = [
    'name',
    'synonym',
    'category_type',
    'comment',
    'allocation_rules',
    'author',
    'contact',
    'long_term_contact',
    'step',
    'project',
    'step_in_project',
    'reference_period',
    'time_validity_limit',
    'geographic_representativeness',
    'technology_description',
    'technology_scale',
    'technology_level']

EXCEL_EXTERNAL_LINK_PATTERN = r"""'.*\[.*\].*'\!\$?[A-Z]+\$?\d+"""

# This is the only Elda cell address that is defined outside EldaTemplateParameters. It is used for determining the
# elda template version and thus cannot be changed from version to version
ELDA_TEMPLATE_VERSION_CELL = 'B22'


class EldaTemplateParameters:
    """ Class used to store parameters related to the Elda template and to handle changes between versions """

    def __init__(self, elda_template_version=ELDA_TEMPLATE_VERSION):
        """
        Here are defined the parameters used by the current version of ELDAM

        Args:
            elda_template_version (str): Version of Eldam for which to get the parameters. Default is current version.
        """

        # Column of every flow fields
        self.FLOW_FIELDS_COLUMNS = {'type': 'B',
                                    'name': 'C',
                                    'library': 'D',
                                    'compartment': 'E',
                                    'waste_type': 'F',
                                    'sub_compartment': 'F',
                                    'unit': 'G',
                                    'amount': 'H',
                                    'formula': 'I',
                                    'allocation': 'J',
                                    'allocation_formula': 'K',
                                    'category': 'L',
                                    'data_source': 'M',
                                    'comment': 'O',
                                    'comment_for_reviewer': 'P',
                                    'review_state': 'Q',
                                    'reviewer_comment': 'S',
                                    'uncertainty': 'T',
                                    'stdev': 'U',
                                    'min_value': 'V',
                                    'max_value': 'W',
                                    'modification_code': 'X',
                                    'modification_comment': 'Y',
                                    'relevance_code': 'Z',
                                    'relevance_comment': 'AA',
                                    'confidence_code': 'AB',
                                    'confidence_comment': 'AC'}

        # Parameters fields order in the elda
        self.INPUT_PARAMETER_FIELDS_ORDER = ['name', 'value', 'merged_column', 'comment', 'comment_for_reviewer',
                                             'review_state', 'review_state_litteral', 'reviewer_comment', 'uncertainty',
                                             'stdev', 'min_value', 'max_value', 'level']
        self.CALCULATED_PARAMETER_FIELDS_ORDER = ['name', 'value', 'formula', 'comment', 'comment_for_reviewer',
                                                  'review_state', 'review_state_litteral', 'reviewer_comment', 'level']

        # Row number of the first flow on the elda
        self.FIRST_FLOW_ROW_NUMBER = 36

        # Row number of the first flow on the elda
        self.LAST_FLOW_ROW_NUMBER = 185

        # Default last input/calculated parameter cell coords
        self.DEFAULT_LAST_INPUT_PARAMETER_CELL_COORDS = '$L$23'
        self.DEFAULT_LAST_CALCULATED_PARAMETER_CELL_COORDS = '$L$33'

        # Cell in which the last input/calculated parameter cell coords are stored
        self.LAST_INPUT_PARAMETER_CELL_COORDS_CELL = "Q1"
        self.LAST_CALCULATED_PARAMETER_CELL_COORDS_CELL = "Q2"

        # Parameters blocs dimensions
        self.INPUT_PARAMETERS_BLOCK_HEIGHT = 9  # number of rows
        self.INPUT_PARAMETERS_BLOCK_WIDTH = 13  # number of columns
        self.CALCULATED_PARAMETERS_BLOCK_HEIGHT = 8  # number of rows
        self.CALCULATED_PARAMETERS_BLOCK_WIDTH = 9  # number of columns

        # Parameters name column
        self.PARAMETERS_NAME_COLUMN = 'L'

        # Process metadata cells
        self.METADATA_CELLS = {'name': 'D10',
                               'synonym': 'D11',
                               'category_type': 'D12',
                               'comment': 'D27',
                               'allocation_rules': 'D13',
                               'author': 'D5',
                               'contact': 'D6',
                               'long_term_contact': 'D7',
                               'step': 'D14',
                               'project': 'D15',
                               'step_in_project': 'D16',
                               'reference_period': 'D18',
                               'time_validity_limit': 'D19',
                               'geographic_representativeness': 'D21',
                               'technology_description': 'D23',
                               'technology_scale': 'D24',
                               'technology_level': 'D25',
                               'input_mass': 'D31',
                               'output_mass': 'D32'}

        self.VERSION_INFO_CELLS = {'version_creator': 'M6',
                                   'version_contact': 'M7',
                                   'version_comment': 'M9',
                                   'inventory_review_state': 'M12'}

        self.VERSION_DATE_CELL = 'M8'

        # Row numbers for parameters blocks
        self.PARAMETERS_FIRST_ROW = {'Input parameter': 16, 'Calculated parameter': 27}
        self.PARAMETERS_LAST_ROW = {'Input parameter': 23, 'Calculated parameter': 33}

        # Ranges of cells to be cleaned by EldaVersionWriter.clean_data() to remove parameters and flows from the sheet.
        self.CELLS_TO_CLEAN = [
            # First parameter block
            'L16:P23',
            'L27:M33',
            'O27:P33',
            'S16:X23',
            'S27:X33',

            # Flow data
            'C36:H185',
            'J36:J185',
            'L36:p185',
            'S36:AD185',
        ]

        # Range of cells to be deletes (value, style, conditional formatting and data validation)
        # by EldaVersionWriter.clean_data() to remove parameters and flows from the sheet.
        self.CELLS_TO_DELETE = [
            # Other parameter blocks
            'Z15:{}33',
        ]

        # Ranges of cells to be replaced by EldaVersionWriter.clean_data().
        # Item key is the replacement string and item value is the list of ranges of cells to be replaced
        self.CELLS_TO_REPLACE = {"Select a type": ['B36:B185'],
                                 # Review state
                                 0: [  # Flows
                                     'Q36:Q185',

                                     # Parameters
                                     'Q16:Q23',
                                     'Q27:Q33'
                                 ]
                                 }

        # Formula used for changed values conditional formatting
        self.CHANGED_VALUE_CF_FORMULA = \
            '($M$2<>0)*(B5<>INDIRECT(ADDRESS(ROW(B5),COLUMN(B5),4,,CONCATENATE("V",$M$1,".",$M$2-1))))'

        # Cells coordinates used in various places
        self.GENERAL_COMMENT_CELL = 'D27'
        self.MAJOR_VERSION_NUMBER_CELL = 'M1'
        self.MAJOR_VERSION_NUMBER_FIXED_CELL = 'M1'
        self.MINOR_VERSION_NUMBER_CELL = 'M2'
        self.MINOR_VERSION_NUMBER_FIXED_CELL = '$M$2'
        self.NEXT_MINOR_VERSION_NUMBER_CELL = 'M3'
        self.REVIEW_STATE_CELL = 'M4'
        self.FIRST_INPUT_PARAMETER_VALUE_CELL = 'M16'
        self.FIRST_CALCULATED_PARAMETER_VALUE_CELL = 'M27'
        self.PROCESS_NAME_CELL = 'D10'

        # Comments size handling
        # On reading a workbook, openpyxl looses comments positions and size.
        # If they do not fit the default size, they must be reset manually
        # Width, Height
        self.COMMENT_DIMENSIONS = {'medium': (200, 100),
                                   'big': (200, 150),
                                   'huge': (500, 220),
                                   }

        self.ELDA_COMMENTS = {
            'L12': 'medium',
            'B12': 'medium',
            'B14': 'huge',
            'B23': 'medium',
            'B25': 'huge',
            'C33': 'medium',
            'F35': 'medium',
            'H35': 'medium',
            'L35': 'medium',
            'M35': 'medium',
            'U15': 'medium',
            'U35': 'medium',
            'X35': 'big',
            'Z35': 'big',
            'AB35': 'big'
        }

        self.SIMAPRO_UNITS_DEFINITION_CELLS = f"{quote_sheetname('Simapro units')}!$A$1:$A$196"

        if elda_template_version != ELDA_TEMPLATE_VERSION:
            self.load_version_parameters(elda_template_version)

    def load_version_parameters(self, elda_template_version):
        """
        Updates the parameters for a defined anterior version of the Elda template.

        If there are multiple versions between the current one and the demanded one, the changes are accumulated to go
        back one version at a time.

        Args:
            elda_template_version (str): Version of the Elda template for which to get the parameters.
        """

        major, minor = elda_template_version.split(".")
        major = int(major)
        minor = int(minor)

        # If the version to go back to is anterior or equal to 0.18
        if (major <= 0) or (minor <= 18):
            # # # Here are the differences from template 0.18 to 0.19 # # #

            self.FLOW_FIELDS_COLUMNS = {'type': 'B',
                                        'name': 'C',
                                        'library': 'D',
                                        'compartment': 'E',
                                        'waste_type': 'F',
                                        'sub_compartment': 'F',
                                        'unit': 'G',
                                        'amount': 'H',
                                        'formula': 'I',
                                        'allocation': 'J',
                                        'category': 'K',
                                        'data_source': 'L',
                                        'comment': 'N',
                                        'review_state': 'P',
                                        'comment_for_reviewer': 'O',
                                        'reviewer_comment': 'R',
                                        'modification_code': 'W',
                                        'modification_comment': 'X',
                                        'relevance_code': 'Y',
                                        'relevance_comment': 'Z',
                                        'confidence_code': 'AA',
                                        'confidence_comment': 'AB',
                                        'uncertainty': 'S',
                                        'stdev': 'T',
                                        'min_value': 'U',
                                        'max_value': 'V'}

            self.DEFAULT_LAST_INPUT_PARAMETER_CELL_COORDS = '$K$23'
            self.DEFAULT_LAST_CALCULATED_PARAMETER_CELL_COORDS = '$K$33'
            self.LAST_INPUT_PARAMETER_CELL_COORDS_CELL = "O1"
            self.LAST_CALCULATED_PARAMETER_CELL_COORDS_CELL = "O2"

            self.PARAMETERS_NAME_COLUMN = 'K'

            self.VERSION_INFO_CELLS = {'version_creator': 'L6',
                                       'version_contact': 'L7',
                                       'version_comment': 'L9',
                                       'inventory_review_state': 'L12'}

            self.VERSION_DATE_CELL = 'L8'

            self.CELLS_TO_CLEAN = [
                'K16:O23',
                'K27:L33',
                'N27:O33',
                'R16:W23',
                'R27:W33',
                'C36:H185',
                'J36:O185',
                'R36:AC185',
            ]

            self.CELLS_TO_DELETE = [
                # Other parameter blocks
                'Y15:{}33',
            ]

            self.CELLS_TO_REPLACE = {"Select a type": ['B36:B185'],
                                     0: [
                                         'P36:P185',
                                         'P16:P23',
                                         'P27:P33'
                                     ]
                                     }

            self.CHANGED_VALUE_CF_FORMULA = \
                '($L$2<>0)*(B5<>INDIRECT(ADDRESS(ROW(B5),COLUMN(B5),4,,CONCATENATE("V",$L$1,".",$L$2-1))))'

            self.GENERAL_COMMENT_CELL = 'D27'
            self.MAJOR_VERSION_NUMBER_CELL = 'L1'
            self.MINOR_VERSION_NUMBER_CELL = 'L2'
            self.MINOR_VERSION_NUMBER_FIXED_CELL = '$L$2'
            self.NEXT_MINOR_VERSION_NUMBER_CELL = 'L3'
            self.REVIEW_STATE_CELL = 'L4'
            self.FIRST_INPUT_PARAMETER_VALUE_CELL = 'L16'
            self.FIRST_CALCULATED_PARAMETER_VALUE_CELL = 'L27'
            self.PROCESS_NAME_CELL = 'D10'

            self.ELDA_COMMENTS = {
                'K12': 'medium',
                'B12': 'medium',
                'B14': 'huge',
                'B23': 'medium',
                'B25': 'huge',
                'C33': 'medium',
                'F35': 'medium',
                'H35': 'medium',
                'L35': 'medium',
                'T15': 'medium',
                'T35': 'medium',
                'W35': 'big',
                'Y35': 'big',
                'AA35': 'big'
            }
