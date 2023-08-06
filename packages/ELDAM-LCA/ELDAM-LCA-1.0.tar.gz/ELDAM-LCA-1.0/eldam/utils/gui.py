""" Functions used in ELDAM GUI """

import re
from datetime import datetime

import requests


def name_from_pattern(pattern, process='process', product='product'):
    """
    Creates a file name from a pattern

    Pattern replaceable items are PROCESS and DATE

    Args:
        pattern (str): Pattern to use
        process (str): Process name for replacing PROCESS in the pattern
        product (str): Product name for replacing PRODUCT in the pattern

    Returns:
        str: filename

    Examples:
        >>> name_from_pattern('PROCESS_date', process='process_name')
        'process_name_date'
        >>> name_from_pattern('PROCESS_foo', process='process/name/with/slash')
        'process_name_with_slash_foo'
        >>> name_from_pattern('PRODUCT_bar', product='Prod')
        'Prod_bar'
    """

    result = pattern.replace('PROCESS', process)  # Changing process name
    result = result.replace('PRODUCT', product)  # Changing product name
    result = result.replace('TODAY', datetime.now().strftime('%y-%m-%d'))  # Changing date
    result = result.replace('NOW', datetime.now().strftime('%H-%M-%S'))  # Changing time
    result = result.replace('/', '_')  # Removing slashes
    return result


def remove_path_from_error_message(message):
    """
    The error message displayed when ELDAM crashes contains path to the Python files on the computer on which ELDAM
    as been compilated. This function simply hides the first part of the path.

    Args:
        message (str): Error message

    Returns:
        str: Error message with first part of paths hidden

    Examples:
        >>> remove_path_from_error_message('''Traceback (most recent call last):  File "C:/Users/user/AppData/Local/Programs/Python/Python37/lib/tkinter/__init__.py", line 1702, in __call__   return self.func(*args)  File "C:/Path/to/ELDAM/eldam/gui_tk.py", line 453, in convert_elda_to_csv    self.read_elda()  File "C:/Path/to/ELDAM/eldam/gui_tk.py", line 665, in read_elda    self.processes.append(elda.read_last_version().to_process())  File "C:/Path/to/ELDAM/eldam/core/elda.py", line 870, in to_process    level=input_parameter_data['level'] or 'Process')  File "C:/Path/to/ELDAM/eldam/core/lci_data.py", line 474, in __init__    self.value_or_formula = self.valueAttributeError: 'InputParameter' object has no attribute 'value' ''')
        'Traceback (most recent call last):  File "... \\x02/lib/tkinter/__init__.py", line 1702, in __call__   return self.func(*args)  File "... \\x02/eldam/gui_tk.py", line 453, in convert_elda_to_csv    self.read_elda()  File "... \\x02/eldam/gui_tk.py", line 665, in read_elda    self.processes.append(elda.read_last_version().to_process())  File "... \\x02/eldam/core/elda.py", line 870, in to_process    level=input_parameter_data[\\'level\\'] or \\'Process\\')  File "... \\x02/eldam/core/lci_data.py", line 474, in __init__    self.value_or_formula = self.valueAttributeError: \\'InputParameter\\' object has no attribute \\'value\\' '
    """
    return re.sub('File "(.(?!(lib|eldam)))*', 'File "... \2', message)


def get_last_eldam_version_number(offset=0):
    """
    Gets last ELDAM version number from the gitlab repository tags

    Args:
        offset (int): Offset of 1 will give the penultimate version number

    Returns:
        str: Last ELDAM version number
    """
    try:
        resp = requests.get('https://framagit.org/api/v4/projects/20233/repository/tags')
    except (requests.exceptions.SSLError, requests.exceptions.ConnectionError):
        return None

    counter = -1
    for tag in resp.json():
        version = re.search(r"(?P<version>\d+(.\d+)*)", tag['name'])
        if version:
            counter += 1
            if counter == offset:
                return version.group('version')


def get_last_changelog():
    """
    Gets ELDAM's last changelog.

    Returns:
        str: Last ELDAM changelog
    """
    changelog_url = 'https://framagit.org/GustaveCoste/eldam/raw/master/CHANGELOG.rst'
    try:
        resp = requests.get(changelog_url)
    except (requests.exceptions.SSLError, requests.exceptions.ConnectionError):
        return None
    full_changelog = resp.text

    last_version_number = get_last_eldam_version_number()
    penultimate_version_number = get_last_eldam_version_number(offset=1)
    penultimate_major_version_number = '.'.join(
        penultimate_version_number.split('.')[0:2])  # Getting only major version number
    last_changelog = str()
    record = False
    for line in full_changelog.splitlines():
        if line == last_version_number:
            record = True
        elif (line == penultimate_version_number) or (line == penultimate_major_version_number):
            record = False

        if record:
            last_changelog += '\n' + line

    return last_changelog
