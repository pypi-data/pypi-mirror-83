""" Miscellaneous functions used by ELDAM """

import os
import sys
import subprocess
import difflib

import jinja2


def x_str(arg):
    """
    A function that returns an empty string if the input is None, else str(arg)

    Example:
        >>> x_str(None)
        ''
        >>> x_str(5)
        '5'

    Args:
        arg: Object

    Returns:
        str or NoneType: str(arg) or None
    """
    return '' if arg is None else str(arg)


def n_str(arg):
    """
    A function that returns None if the input is None, else str(arg)

    Example:
        >>> n_str(None)

        >>> n_str(5)
        '5'

    Args:
        arg: Object

    Returns:
        str or NoneType: str(arg) or None
    """

    return None if arg is None else str(arg)


def n_float(arg):
    """
    A function returning a float or None if arg is None

    Example:
        >>> n_float(None)

        >>> n_float(6)
        6.0

    Args:
        arg: Object

    Returns:
        float or NoneType: float(arg) or None
    """

    if arg is None:
        return None

    return float(arg)


def n_int(arg):
    """
    A function returning a int or None if arg is None

    Example:
        >>> n_int(None)

        >>> n_int(6)
        6

    Args:
        arg: Object

    Returns:
        int or NoneType: int(arg) or None
    """

    if arg is None:
        return None

    return int(arg)


def find_data_file(filename):
    """
    Function used to find data files when compiling with cs_freeze

    Args:
        filename (str): The name of the file from the program (.py or .exe)

    Returns:
        str: Path to the file
    """
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    return os.path.join(datadir, filename)


def compare_file(file_1, file_2):
    """
    Returns the differences between two files.

    Args:
        file_1 (str): Path to file 1
        file_2 (str): Path to file 2

    Returns:
        str: Differences between the files
    """

    with open(file_1, 'r') as f1, open(file_2) as f2:
        diff = difflib.ndiff(f1.readlines(), f2.readlines())

        result = ''

        for line in diff:
            if line.startswith('-'):
                result += line
            elif line.startswith('+'):
                result += '\t\t' + line

    return result


def remove_duplicates(iterable):
    """
    Returns a list without its duplicates preserving the order of the elements

    Notes:
        Works on list of unhashable and unsortable objects

    Args:
        iterable (list): List to remove duplicates from

    Returns:
        list: List without its duplicates

    Examples:
        >>> remove_duplicates([1, 2, 3, 4, 4])
        [1, 2, 3, 4]
    """

    # order preserving
    checked = []
    for e in iterable:
        if e not in checked:
            checked.append(e)
    return checked


def is_number(s):
    """
    Checks if a string is a number or not.

    Args:
        s (str): String to check

    Returns:
        bool: Answer

    Examples:
        >>> is_number('0')
        True
        >>> is_number('Input')
        False
        >>> is_number('0,5')
        False
        >>> is_number('0.3')
        True
        >>> is_number('5')
        True

    """
    try:
        float(s)
        return True
    except ValueError:
        return False


def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])


def space_prefix(string):
    """
    Returns a string prefixed with a space.

    For use as a filter in Jinja2 templates

    Args:
        string (str): String to prefix

    Returns:
        str: Prefixed string

    Examples:
        >>> space_prefix('aaa')
        ' aaa'
        >>> space_prefix(None)
        ''
    """
    try:
        if string is None:
            return ''

        return ' ' + string

    except jinja2.exceptions.UndefinedError:
        return ''
