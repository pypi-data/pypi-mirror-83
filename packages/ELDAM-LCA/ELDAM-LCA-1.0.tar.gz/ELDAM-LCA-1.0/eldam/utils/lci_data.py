""" Functions for lci data management """
import os
import re
import json

import jinja2

from eldam.settings import CSV_DELIMITER
from eldam.core.parameters import REVIEW_ATTRIBUTES, JINJA2_TEMPLATES_FOLDER
from eldam.utils.misc import space_prefix


def encode_comment(template_name, **kwargs):
    """
    Function to encode a flow or parameter comment with its data and a given template

    Args:
        template_name (str): Name of the template to use
        **kwargs: data to use for templating

    Returns:
        str: String containing the comment, quality data, and json encoded data

    Examples:

        >>> print(encode_comment('technosphere_flow_comment.jinja2',
        ...                      modification_code=2,
        ...                      modification_comment='modification comment',
        ...                      relevance_code='A',
        ...                      relevance_comment='relevance comment',
        ...                      confidence_code='Y',
        ...                      confidence_comment='confidence comment',
        ...                      comment='Some comment',
        ...                      json_data='{json: data}'))
        2AY:
        2: modification comment
        A: relevance comment
        Y: confidence comment
        <BLANKLINE>
        Some comment
        <BLANKLINE>
        !!! DO NOT EDIT BELOW THIS LINE !!!
        [[{json: data}]]
    """

    # Removing empty values from kwargs to avoid 'None' strings in the result
    kwargs = {x: kwargs[x] for x in kwargs if kwargs[x] is not None}

    env = jinja2.Environment(trim_blocks=True,
                             lstrip_blocks=True)

    env.filters['space_prefix'] = space_prefix

    template_path = os.path.join(JINJA2_TEMPLATES_FOLDER, template_name)
    with open(template_path, 'r') as file:
        template_string = file.read()
    template = env.from_string(template_string)

    # OLD: Use of get_template was abandonned as it let to compilation issues:
    # https://github.com/pyinstaller/pyinstaller/issues/1898
    # env = jinja2.Environment(loader=jinja2.PackageLoader('eldam.core', 'templates'),
    #                          trim_blocks=True,
    #                          lstrip_blocks=True)
    #
    # env.filters['space_prefix'] = space_prefix
    #
    # template = env.get_template(template_name)

    encoded_comment = template.render(**kwargs)

    # Removing trailing newlines
    encoded_comment = encoded_comment.strip()

    # Removing duplicates empty lines
    encoded_comment = re.sub('\n{3,}', '\n\n', encoded_comment)

    return encoded_comment


def encode_json_data(**kwargs):
    """
    Encodes flow or parameter data into a json string

    Args:
        **kwargs: Data to encode

    Returns:
        str: Json encoded string

    Examples:
        >>> encode_json_data(something='this', nothing=None, something_else='that')
        '{"something": "this", "something_else": "that"}'
    """

    # Removing empty values
    data = {x: kwargs[x] for x in kwargs if kwargs[x] is not None and (x != 'review_state' or kwargs[x] != 0)}

    if len(data) == 0:
        return None

    return json.dumps(data, ensure_ascii=False)


def encode_simapro_csv_format(*args):
    """
    Encodes flow or parameter data for insertion in a SimaPro csv import file.

    Args:
        *args: Data to encode

    Returns:
        str: string formatted for insertion in a SimaPro csv import file.

    Examples:
        >>> encode_simapro_csv_format(5.6, '3,7', 'text with double quotes " and ; semicolon')
        '5.6;"3,7";"text with double quotes "" and ; semicolon"'
    """
    # Doubling double quotes in strings to protect them in the csv
    args = [x.replace('"', '""') if (type(x) == str) else x for x in args]

    args = [f'"{x}"' if (type(x) == str) and (x != '') else str(x) for x in args]

    result = CSV_DELIMITER.join(args)

    # Replacing newlines by special character used by SimaPro
    result = result.replace('\n', '\x7f')

    return result


def compare_element(element1, element2):
    """
    Returns a dictionnary containing every differences between two objects

    Args:
        element1:
        element2:

    Returns:
        dict: Differences between the two objects
    """
    if element1 == element2:
        return dict()

    result = dict()

    for attribute in vars(element1).keys():
        if getattr(element1, attribute) != getattr(element2, attribute):
            result[attribute] = (getattr(element1, attribute), getattr(element2, attribute))

    return result


def compare_input_parameters(parameter1, parameter2):
    """
    Returns a dictionnary containing every differences between two input parameters

    Args:
        parameter1 (InputParameter):
        parameter2 (InputParameter):

    Returns:
        dict: Differences between the two parameters
    """

    return compare_element(parameter1, parameter2)


def compare_calculated_parameters(parameter1, parameter2):
    """
    Returns a dictionnary containing every differences between two calculated parameters

    Args:
        parameter1 (CalculatedParameter):
        parameter2 (CalculatedParameter):

    Returns:
        dict: Differences between the two parameters
    """

    return compare_element(parameter1, parameter2)


def compare_parameters(parameter1, parameter2):
    """
    Returns a dictionnary containing every differences between two parameters of the same type

    Args:
        parameter1 (InputParameter or CalculatedParameter):
        parameter2 (InputParameter or CalculatedParameter):

    Returns:
        dict: Differences between the two parameters
    """

    if parameter1.type != parameter2.type:
        return {'type': (parameter1.type, parameter2.type)}

    else:
        return compare_element(parameter1, parameter2)


def compare_flows(flow1, flow2):
    """
    Returns a dictionnary containing every differences between two flows

    Args:
        flow1 (Flow):
        flow2 (Flow):

    Returns:
        dict: Differences between the two flows
    """

    return compare_element(flow1, flow2)


def compare_processes(process1, process2):
    """
    Returns a dictionnary containing every differences between two processes

    Args:
        process1 (Process):
        process2 (Process):

    Returns:
        dict: Differences between the two processes
    """

    if process1 == process2:
        return dict()

    result = dict()
    parameters_result = list()
    flows_results = list()

    for attribute in vars(process1).keys():

        # Skipping some attributes
        if attribute in ('metadata_review', 'date'):
            continue

        elif attribute == 'parameters':

            # Getting every parameters
            parameters1 = list(process1.parameters)
            parameters1_copy = list(process1.parameters)
            parameters2 = list(process2.parameters)

            # Looping on every parameter and removing it from both lists if it is redundant.
            # This way, only non redundant parameters are kept.
            for parameter in parameters1_copy:
                if parameter in parameters2:
                    parameters1.remove(parameter)
                    parameters2.remove(parameter)

            if (len(parameters1) > 0) or (len(parameters2) > 0):
                # Looping on every parameters to compare it to the others
                for parameter1 in parameters1:

                    # If there is a parameter of the same name in the compared process, compares parameters
                    # and removes it from parameters2
                    try:
                        parameter2 = [param for param in parameters2 if param.name == parameter1.name][0]

                        parameters_differences = compare_parameters(parameter1, parameter2)
                        parameters_differences['name'] = (parameter1.name, parameter1.name)

                        parameters_result.append(parameters_differences)

                        parameters2.remove(parameter2)

                    # Otherwise, inserts the parameters data manually
                    except IndexError:
                        parameter1_data = dict()
                        for parameter1_attribute in vars(parameter1).keys():
                            if getattr(parameter1, parameter1_attribute) is not None:
                                parameter1_data[parameter1_attribute] = (getattr(parameter1, parameter1_attribute),
                                                                         None)
                        parameters_result.append(parameter1_data)

                # Looping on remaining parameters in parameters2 (ie the parameters that are only in process2)
                for parameter2 in parameters2:
                    parameter2_data = dict()
                    for parameter2_attribute in vars(parameter2).keys():
                        if getattr(parameter2, parameter2_attribute) is not None:
                            parameter2_data[parameter2_attribute] = (None, getattr(parameter2, parameter2_attribute))

                    parameters_result.append(parameter2_data)

                result[attribute] = parameters_result

        # Doing the same as above with flows
        elif attribute == 'flows':

            flows1 = list(process1.flows)
            flows1_copy = list(process1.flows)
            flows2 = list(process2.flows)

            for flow in flows1_copy:
                if flow in flows2:
                    flows1.remove(flow)
                    flows2.remove(flow)

            if (len(flows1) > 0) or (len(flows2) > 0):
                # Looping on every flow to compare it to the others
                for flow1 in flows1:

                    # If there is a flow of the same name in the compared process, compares flows
                    # and removes it from flows2
                    try:
                        flow2 = [fl for fl in flows2 if fl.name == flow1.name][0]

                        flows_differences = compare_flows(flow1, flow2)
                        flows_differences['name'] = (flow1.name, flow2.name)

                        flows_results.append(flows_differences)

                        flows2.remove(flow2)

                    except IndexError:
                        flow1_data = dict()
                        for flow1_attribute in vars(flow1).keys():
                            if getattr(flow1, flow1_attribute) is not None:
                                flow1_data[flow1_attribute] = (getattr(flow1, flow1_attribute),
                                                               None)
                        flows_results.append(flow1_data)

                # Looping on remaining flows in flows2 (ie. the flows that are only in process2)
                for flow2 in flows2:
                    flow2_data = dict()
                    for flow2_attribute in vars(flow2).keys():
                        if getattr(flow2, flow2_attribute) is not None:
                            flow2_data[flow2_attribute] = (None, getattr(flow2, flow2_attribute))

                    flows_results.append(flow2_data)

                result[attribute] = flows_results

        elif getattr(process1, attribute) != getattr(process2, attribute):

            value1 = getattr(process1, attribute)
            try:
                metadata1 = process1.metadata_review[attribute]
            except KeyError:
                metadata1 = dict()

            value2 = getattr(process2, attribute)
            try:
                metadata2 = process2.metadata_review[attribute]
            except KeyError:
                metadata2 = dict()

            metadata1.update({'value': value1})
            metadata2.update({'value': value2})

            result[attribute] = compare_metadata(metadata1, metadata2)

    return result


def compare_metadata(metadata1, metadata2):
    """
    Compares two metadata review dicts

    Args:
        metadata1 (dict):
        metadata2 (dict):

    Returns:
        dict: Differences between the two metadata
    """

    result = dict()

    for attribute in REVIEW_ATTRIBUTES:

        try:
            attribute1 = metadata1[attribute]
        except KeyError:
            attribute1 = None

        try:
            attribute2 = metadata2[attribute]
        except KeyError:
            attribute2 = None

        if attribute1 != attribute2:
            result[attribute] = (attribute1, attribute2)

    return result
