""" Functions used for elda management """

import re


def version_from_text(version_text):
    """
    Converts a text to a tuple containing major and minor version number

    Example:
        >>> version_from_text('V1.3')
        (1, 3)

    Args:
        version_text (str): Text formatted version number like 'V2.3'

    Returns:
        (int, int): (major, minor)
    """
    # Asserts the input respects the format
    assert re.match(r"^V\d+\.\d+$", version_text)
    version_text = version_text[1:]

    major, minor = version_text.split(".")

    return int(major), int(minor)


def text_from_version(major, minor):
    """
    Converts major and minor version numbers in a string

    Example:
        >>> text_from_version(1,3)
        'V1.3'

    Args:
        major (int): Major version number
        minor (int): Minor version number

    Returns:
        str: Text formatted version number
    """
    return f"V{major}.{minor}"


def add_major_version_from_text(version_text):
    """
    Returns the next major version from a text formatted version number

    Example:
        >>> add_major_version_from_text('V1.3')
        'V2.0'

    Args:
        version_text (str): Text formatted version number like 'V2.3'

    Returns:
        str: Text formatted version number
    """
    major, minor = version_from_text(version_text)

    major += 1
    minor = 0

    return text_from_version(major, minor)


def add_minor_version_from_text(version_text):
    """
    Returns the next minor version from a text formatted version number

    Example:
        >>> add_minor_version_from_text('V1.3')
        'V1.4'

    Args:
        version_text (str): Text formatted version number like 'V2.3'

    Returns:
        str: Text formatted version number
    """
    major, minor = version_from_text(version_text)

    minor += 1

    return text_from_version(major, minor)
