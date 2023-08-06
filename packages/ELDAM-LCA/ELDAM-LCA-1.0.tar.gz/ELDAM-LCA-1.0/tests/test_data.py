from eldam.core.lci_data import *
from eldam.core.parameters import EldaTemplateParameters

def process_a():
    """
    Process containing only data handled by SimaPro

    Returns:
        Process: Process A
    """
    process = Process(name='Process A',
                      date='13/09/2017',
                      comment='General comment on test process ; with semicolon\n\non 3 lines',
                      allocation_rules='Allocation rules value',
                      author='Generator value',
                      project='ELDAM')

    flows = [ProductFlow(name='Product A',
                         type='Output/Technosphere/Product',
                         unit='kg',
                         amount=2,
                         allocation='A+3',
                         category='_ELDAM',
                         comment='Comment on test product'),
             ProductFlow(name='Coproduct A',
                         type='Output/Technosphere/Product',
                         unit='l',
                         amount=3.2,
                         allocation='100-A-3',
                         category='_ELDAM',
                         comment='Comment on test co-product ; with semicolon'),
             TechnosphereFlow(name='Barley grain, feed, organic {GLO}| market for | APOS, S',
                              type='Output/Technosphere/Avoided product',
                              unit='g',
                              amount=3.5,
                              comment='Rest of the comment',
                              uncertainty='Normal',
                              stdev=0),
             TechnosphereFlow(name='Bentonite quarry infrastructure {RoW}| bentonite quarry construction | APOS, S',
                              comment='rest of the comment\non 2 lines',
                              amount='A',
                              type='Input/Technosphere',
                              unit='p'),
             TechnosphereFlow(name='Heat, from steam, in chemical industry {RoW}| market for heat, '
                                   'from steam, in chemical industry | APOS, U',
                              amount=6,
                              type='Input/Technosphere',
                              unit='MJ'),
             TechnosphereFlow(name='Heat, central or small-scale, natural gas {Europe without Switzerland}| '
                                   'market for heat, central or small-scale, natural gas | Cut-off, U',
                              comment='rest of the comment (lines related to modification and relevance has been '
                                      'skipped because code 0 and A)',
                              amount=2566985,
                              type='Input/Technosphere',
                              unit='kJ'),
             TechnosphereFlow(name='Diesel, burned in building machine {GLO}| market for | APOS, S',
                              comment='Comment',
                              amount=4,
                              type='Input/Technosphere',
                              unit='MJ'),
             BiosphereFlow(name='Occupation, water bodies, artificial',
                           amount=32.36,
                           max_value=50,
                           min_value=0,
                           sub_compartment='in water',
                           type='Input/Nature',
                           uncertainty='Triangle',
                           unit='m2a'),
             BiosphereFlow(name='Xenon-133',
                           comment='Rest of the comment',
                           compartment='Air',
                           amount='NO2',
                           sub_compartment='high. pop.',
                           type='Output/Emission',
                           unit='kBq'),
             BiosphereFlow(name='1-amino-2,4-dibromoanthraquinone',
                           comment='Rest of the comment',
                           compartment='Water',
                           amount='D',
                           type='Output/Emission',
                           unit='kg'),
             BiosphereFlow(name='Methoxyflurane',
                           compartment='Soil',
                           comment='Comment without acv cirad data',
                           sub_compartment='forestry',
                           amount='pi',
                           unit='kg',
                           type='Output/Emission'),
             BiosphereFlow(name='Cathode loss',
                           amount='Project_input_parameter',
                           type='Output/Final waste flows',
                           unit='kg'),
             BiosphereFlow(name='Waste, nuclear, high active/m3',
                           amount='a_plus_no2+6.5',
                           type='Output/Final waste flows',
                           unit='m3'),
             TechnosphereFlow(name='Wastewater from tube collector production {GLO}| market for | Cut-off, U',
                              amount=58,
                              stdev=12,
                              type='Output/Technosphere/Waste',
                              uncertainty='Lognormal',
                              unit='m3')
             ]

    parameters = [InputParameter(comment='Comment on input parameter A',
                                 level='Process',
                                 name='A',
                                 value=5.6,
                                 uncertainty='Normal',
                                 stdev=2),
                  InputParameter(comment='Comment on input parameter NO2 (hidden)',
                                 level='Process',
                                 name='NO2',
                                 value=3,
                                 uncertainty='Triangle',
                                 min_value=2,
                                 max_value=8),
                  InputParameter(comment='Comment on input parameter D',
                                 level='Process',
                                 name='D',
                                 value=8),
                  CalculatedParameter(comment='Comment on calculated parameter A_plus_NO2',
                                      formula='A+NO2',
                                      level='Process',
                                      name='A_plus_NO2'),
                  CalculatedParameter(formula='database_calculated_parameter *65.8 +D',
                                      level='Process',
                                      name='parameter_using_database_param'),
                  InputParameter(name='database_input_parameter',
                                 comment='Comment on database input parameter',
                                 level='Database',
                                 value=5.3,
                                 uncertainty='Triangle',
                                 min_value=5,
                                 max_value=6),
                  CalculatedParameter(comment='comment on database calculated parameter',
                                      formula='database_input_parameter*5',
                                      level='Database',
                                      name='database_calculated_parameter'),
                  InputParameter(comment='comment on project input param',
                                 level='Project',
                                 name='project_input_parameter',
                                 value=8,
                                 uncertainty='Lognormal',
                                 stdev=3.2),
                  CalculatedParameter(comment='comment on project calculated parameter',
                                      formula='project_input_parameter*9',
                                      level='Project',
                                      name='project_calculated_parameter'),
                  CalculatedParameter(formula='project_input_parameter * database_calculated_parameter',
                                      level='Project',
                                      name='other_project_calculated_parameter')
                  ]

    process.add_flows(*flows)
    process.add_parameters(*parameters)

    process.sort_parameters()

    return process


def process_a_constants():
    """
    Process containing only data handled by SimaPro

    Returns:
        Process: Process A with expressions converted to constants
    """
    process = process_a()

    process.flows = []
    process.parameters = []

    flows = [ProductFlow(name='Product A',
                         type='Output/Technosphere/Product',
                         unit='kg',
                         amount=2,
                         allocation='8.6',
                         category='_ELDAM',
                         comment='Comment on test product'),
             ProductFlow(name='Coproduct A',
                         type='Output/Technosphere/Product',
                         unit='l',
                         amount=3.2,
                         allocation='91.4',
                         category='_ELDAM',
                         comment='Comment on test co-product ; with semicolon'),
             TechnosphereFlow(name='Barley grain, feed, organic {GLO}| market for | APOS, S',
                              type='Output/Technosphere/Avoided product',
                              unit='g',
                              amount=3.5,
                              comment='Rest of the comment',
                              uncertainty='Normal',
                              stdev=0),
             TechnosphereFlow(name='Bentonite quarry infrastructure {RoW}| bentonite quarry construction | APOS, S',
                              comment='rest of the comment\non 2 lines',
                              amount=5.6,
                              type='Input/Technosphere',
                              unit='p'),
             TechnosphereFlow(name='Heat, from steam, in chemical industry {RoW}| market for heat, '
                                   'from steam, in chemical industry | APOS, U',
                              amount=6,
                              type='Input/Technosphere',
                              unit='MJ'),
             TechnosphereFlow(name='Heat, central or small-scale, natural gas {Europe without Switzerland}| '
                                   'market for heat, central or small-scale, natural gas | Cut-off, U',
                              comment='rest of the comment (lines related to modification and relevance has been '
                                      'skipped because code 0 and A)',
                              amount=2566985,
                              type='Input/Technosphere',
                              unit='kJ'),
             TechnosphereFlow(name='Diesel, burned in building machine {GLO}| market for | APOS, S',
                              comment='Comment',
                              amount=4,
                              type='Input/Technosphere',
                              unit='MJ'),
             BiosphereFlow(name='Occupation, water bodies, artificial',
                           amount=32.36,
                           max_value=50,
                           min_value=0,
                           sub_compartment='in water',
                           type='Input/Nature',
                           uncertainty='Triangle',
                           unit='m2a'),
             BiosphereFlow(name='Xenon-133',
                           comment='Rest of the comment',
                           compartment='Air',
                           amount=3,
                           sub_compartment='high. pop.',
                           type='Output/Emission',
                           unit='kBq'),
             BiosphereFlow(name='1-amino-2,4-dibromoanthraquinone',
                           comment='Rest of the comment',
                           compartment='Water',
                           amount=8,
                           type='Output/Emission',
                           unit='kg'),
             BiosphereFlow(name='Methoxyflurane',
                           compartment='Soil',
                           comment='Comment without acv cirad data',
                           sub_compartment='forestry',
                           amount=3.14,
                           unit='kg',
                           type='Output/Emission'),
             BiosphereFlow(name='Cathode loss',
                           amount=8,
                           type='Output/Final waste flows',
                           unit='kg'),
             BiosphereFlow(name='Waste, nuclear, high active/m3',
                           amount=15.1,
                           type='Output/Final waste flows',
                           unit='m3'),
             TechnosphereFlow(name='Wastewater from tube collector production {GLO}| market for | Cut-off, U',
                              amount=58,
                              stdev=12,
                              type='Output/Technosphere/Waste',
                              uncertainty='Lognormal',
                              unit='m3')
             ]

    process.add_flows(*flows)

    return process


def process_b():
    """
    Process containing the same informations as the process A but with review, data quality and other elda info.

    Returns:
        Process: Process B
    """
    # Getting a copy of process_a
    process = process_a()

    # Changing the process name and comment
    process.name = 'Process B'
    process.comment = 'General comment on test process\n\non 3 lines'

    # Adding metadata
    process.synonym = 'process_b'
    process.category_type = 'Material'
    process.contact = 'contact@mail.com'
    process.long_term_contact = 'longterm@mail.com'
    process.step = 'Materials'
    process.step_in_project = 'step in the project'
    process.reference_period = '2018'
    process.time_validity_limit = '2030'
    process.geographic_representativeness = 'France'
    process.technology_description = 'Description of the technology'
    process.technology_scale = 'Pilot scale'
    process.technology_level = 'Modern'
    process.input_mass = '=H39'
    process.output_mass = '=H36+H37+H38'
    process.version_creator = 'creator'
    process.version_contact = 'contact@mail.com'
    process.version_comment = 'comment on version'
    process.inventory_review_state = 'Valid'

    # Adding review info on metadata
    for attribute in EldaTemplateParameters().METADATA_CELLS.keys():
        process.metadata_review[attribute] = {'comment': 'a comment',
                                              'review_state': 1,
                                              'comment_for_reviewer': 'a comment for reviewer',
                                              'reviewer_comment': 'a reviewer comment'}

    # Removing comment on the comment
    process.metadata_review['comment'].pop('comment')

    # Creating a modified versions of the flows with additional data
    flows = [ProductFlow(name='Product B',
                         type='Output/Technosphere/Product',
                         waste_type='Biopolymers',
                         unit='kg',
                         amount=2,
                         allocation='A+3',
                         category='_ELDAM',
                         data_source='Source of the data',
                         comment='Comment on test product'),
             ProductFlow(name='Coproduct B',
                         type='Output/Technosphere/Product',
                         unit='l',
                         amount=3.2,
                         allocation='100-A-3',
                         category='_ELDAM',
                         comment='Comment on test co-product'),
             TechnosphereFlow(name='Barley grain, feed, organic {GLO}| market for | APOS, S',
                              type='Output/Technosphere/Avoided product',
                              unit='g',
                              library='Own process',
                              amount=3.5,
                              comment='Rest of the comment',
                              uncertainty='Normal',
                              stdev=0,
                              modification_code=1,
                              modification_comment='Information on process modification',
                              relevance_code='B',
                              relevance_comment='Info on relevance',
                              confidence_code='Z',
                              confidence_comment='Info on confidence'),
             TechnosphereFlow(name='Bentonite quarry infrastructure {RoW}| bentonite quarry construction | APOS, S',
                              comment='rest of the comment\non 2 lines',
                              amount='A',
                              type='Input/Technosphere',
                              unit='p',
                              data_source='Source of the data',
                              modification_code=0,
                              relevance_code='A',
                              library='Own process',
                              relevance_comment='info on relevance (the line about modification has been skipped '
                                                'because code 0)',
                              confidence_code='Z',
                              confidence_comment='info on confidence'),
             TechnosphereFlow(name='Heat, from steam, in chemical industry {RoW}| market for heat, '
                                   'from steam, in chemical industry | APOS, U',
                              amount=6,
                              type='Input/Technosphere',
                              unit='MJ',
                              modification_code=3,
                              modification_comment='info on modification',
                              relevance_code='A',
                              confidence_code='Y',
                              confidence_comment='info on confidence ( info on relevance is empty because code was A)'),
             TechnosphereFlow(name='Heat, central or small-scale, natural gas {Europe without Switzerland}| '
                                   'market for heat, central or small-scale, natural gas | Cut-off, U',
                              comment='rest of the comment (lines related to modification and relevance has been '
                                      'skipped because code 0 and A)',
                              amount=2566985,
                              type='Input/Technosphere',
                              unit='kJ',
                              library='Ecoinvent v3',
                              data_source='Source of the data',
                              modification_code=0,
                              relevance_code='A',
                              confidence_code='Z',
                              confidence_comment='info on confidence'),
             TechnosphereFlow(name='Diesel, burned in building machine {GLO}| market for | APOS, S',
                              comment='Comment',
                              amount=4,
                              type='Input/Technosphere',
                              unit='MJ',
                              library='Ecoinvent v3',
                              data_source='Source of the data',
                              modification_code=0,
                              relevance_code='A',
                              confidence_code='Z',
                              confidence_comment='info on confidence'),
             BiosphereFlow(name='Occupation, water bodies, artificial',
                           amount=32.36,
                           max_value=50,
                           min_value=0,
                           sub_compartment='in water',
                           type='Input/Nature',
                           uncertainty='Triangle',
                           unit='m2a',
                           relevance_code='B',
                           relevance_comment='info on relevance',
                           confidence_code='Z',
                           confidence_comment='info on confidence'),
             BiosphereFlow(name='Xenon-133',
                           comment='Rest of the comment',
                           compartment='Air',
                           amount='NO2',
                           sub_compartment='high. pop.',
                           type='Output/Emission',
                           unit='kBq',
                           relevance_code='B',
                           relevance_comment='info on relevance',
                           confidence_code='Y',
                           confidence_comment='info on confidence'),
             BiosphereFlow(name='1-amino-2,4-dibromoanthraquinone',
                           comment='Rest of the comment',
                           compartment='Water',
                           amount='D',
                           type='Output/Emission',
                           unit='kg',
                           relevance_code='A',
                           confidence_code='Y',
                           confidence_comment='info on confidence'),
             BiosphereFlow(name='Methoxyflurane',
                           compartment='Soil',
                           comment='Comment without acv cirad data',
                           sub_compartment='forestry',
                           amount='pi',
                           unit='kg',
                           type='Output/Emission', ),
             BiosphereFlow(name='Cathode loss',
                           amount='project_input_parameter',
                           type='Output/Final waste flows',
                           unit='kg',
                           relevance_code='B',
                           relevance_comment='info on relevance',
                           confidence_code='Z'),
             BiosphereFlow(name='Waste, nuclear, high active/m3',
                           amount='A_plus_NO2+6.5',
                           type='Output/Final waste flows',
                           unit='m3',
                           relevance_code='A',
                           relevance_comment='info on relevance',
                           confidence_code='Y',
                           confidence_comment='info on confidence'),
             TechnosphereFlow(name='Wastewater from tube collector production {GLO}| market for | Cut-off, U',
                              amount=58,
                              stdev=12,
                              type='Output/Technosphere/Waste',
                              uncertainty='Lognormal',
                              unit='m3',
                              relevance_code='B',
                              relevance_comment='info on relevance',
                              confidence_code='Z')
             ]

    process.flows = flows

    # Adding review data to its flows
    for flow in process.flows:
        flow.review_state = 2
        flow.comment_for_reviewer = "a comment for reviewer"
        flow.reviewer_comment = "a reviewer comment"

    # Adding review data to its input parameters (process level only)
    for param in process.input_parameters:
        if param.level == 'Process':
            param.review_state = 0
            param.comment_for_reviewer = "a comment for reviewer"
            param.reviewer_comment = "a reviewer comment"

    # Adding review data to its calculated parameters (process level only)
    for param in process.calculated_parameters:
        if param.level == 'Process':
            param.review_state = 1
            param.comment_for_reviewer = "a comment for reviewer"
            param.reviewer_comment = "a reviewer comment"

    process.sort_parameters()

    return process


def process_a_with_process_b_metadata():
    """
    Process containing name, synonym, flows and paramaters from the process A and metadata from the process B

    Returns:
        Process: Process A with process B metadata

    """
    process = process_b()

    process_a_temp = process_a()

    process.input_mass = process_a_temp.input_mass
    process.output_mass = process_a_temp.output_mass

    process.metadata_review.pop('input_mass')
    process.metadata_review.pop('output_mass')

    process.flows = process_a_temp.flows
    process.parameters = process_a_temp.parameters

    return process


def process_c():
    """
    Process derived from process A but with some modifications

    Returns:
        Process: Process C
    """
    # Getting a copy of the reference process
    process = process_a()

    # Changing metadata
    process.name = 'Process C'
    process.comment = 'General comment on test process\n\non 3 lines'

    # Subseting flows
    process.flows = process.flows[0:4]
    process.flows[
        3].amount = 'A + NO2 + D + project_input_parameter + database_input_parameter + New_input_parameter + ' \
                    'New_input_parameter2 + New_input_parameter3 + New_input_parameter4 + ' \
                    'New_calculated_parameter5 + New_calculated_parameter6 + New_calculated_parameter7 + ' \
                    'New_calculated_parameter8 - A_plus_NO2 - parameter_using_database_param * ' \
                    'project_calculated_parameter / other_project_calculated_parameter'

    # Renaming product flows
    process.flows[0].name = 'Product C'
    process.flows[1].name = 'Coproduct C'

    # Adding new parameters
    new_parameter = InputParameter(name='New_input_parameter', value=5, level='Process')
    new_parameter2 = InputParameter(name='New_input_parameter2', value=5, level='Process')
    new_parameter3 = InputParameter(name='New_input_parameter3', value=5, level='Process')
    new_parameter4 = InputParameter(name='New_input_parameter4', value=5, level='Process')
    new_parameter5 = CalculatedParameter(name='New_calculated_parameter5', formula='3+4', level='Process')
    new_parameter6 = CalculatedParameter(name='New_calculated_parameter6', formula='3+4', level='Process')
    new_parameter7 = CalculatedParameter(name='New_calculated_parameter7', formula='3+4', level='Process')
    new_parameter8 = CalculatedParameter(name='New_calculated_parameter8', formula='3+4', level='Process')
    process.add_parameters(new_parameter, new_parameter2, new_parameter3, new_parameter4, new_parameter5,
                           new_parameter6, new_parameter7, new_parameter8)

    process.sort_parameters()

    return process


def process_d():
    """
    A waste treatment process with a precise waste typem

    Returns:
        Process: Process d
    """

    process = Process(name='Process D', project='ELDAM', date='02/07/2019', category_type='Waste treatment')

    process.add_flows(ProductFlow(name='Waste treatment D',
                                  type='Output/Technosphere/Waste treatment product',
                                  waste_type='Polypropylene, granulate {RoW}| production | APOS, S',
                                  amount=15,
                                  unit='kg',
                                  category='_ELDAM',
                                  comment='Comment on waste treatment'),
                      BiosphereFlow(name='Transformation, from permanent crop, vine',
                                    type='Input/Nature',
                                    sub_compartment='land',
                                    amount='9+5',
                                    unit='m2')
                      )

    return process


def process_e():
    """
    A waste treatment process with undefined waste type (All waste types)

    Returns:
        Process: Process E
    """

    process = Process(name='Process E', project='ELDAM', date='11/07/2019', category_type='Waste treatment')

    process.add_flows(ProductFlow(name='Waste treatment E',
                                  type='Output/Technosphere/Waste treatment product',
                                  waste_type=None,
                                  amount=20,
                                  unit='m3',
                                  category='_ELDAM',
                                  comment='This waste treatment has no waste type'),
                      TechnosphereFlow(name='Basalt {GLO}| market for | APOS, U',
                                       type='Input/Technosphere',
                                       amount=9,
                                       unit='kg')
                      )

    return process
