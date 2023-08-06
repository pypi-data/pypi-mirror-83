""" Functions used for SimaPro .xlsx files management """
import re
import json


def extract_data_from_comment(comment):
    r"""
    Extracts data from a comment.

    For example, quality data like process modification code and comment

    Args:
        comment (str): Text containing the data

    Returns:
       dict: Dictionnary containing every parsed data

    Examples:
        >>> extract_data_from_comment('Comment on test co-product\n\n!!! DO NOT EDIT BELOW THIS LINE !!!'
        ...         '\n[[{"review_state": 2, "reviewer_comment":"a reviewer comment",'
        ...         '"comment_for_reviewer": "a comment for reviewer"}]]')
        {'comment': 'Comment on test co-product', 'review_state': 2, 'reviewer_comment': 'a reviewer comment', 'comment_for_reviewer': 'a comment for reviewer'}
        >>> extract_data_from_comment('1BZ:\n1: Information on process modification\nB: Info on relevance'
        ...         '\nZ: Info on confidence\n\nRest of the comment\n\n!!! DO NOT EDIT BELOW THIS LINE !!!\n'
        ...         '[[{"library": "Own process", "review_state": 2, "reviewer_comment": "a reviewer comment",'
        ...         '"comment_for_reviewer": "a comment for reviewer"}]]')
        {'modification_code': '1', 'relevance_code': 'B', 'confidence_code': 'Z', 'modification_comment': 'Information on process modification', 'relevance_comment': 'Info on relevance', 'confidence_comment': 'Info on confidence', 'comment': 'Rest of the comment', 'library': 'Own process', 'review_state': 2, 'reviewer_comment': 'a reviewer comment', 'comment_for_reviewer': 'a comment for reviewer'}
        >>> extract_data_from_comment('0AZ:\nA: info on relevance (the line about modification has been '
        ...         'skipped because code 0)\nZ: info on confidence\n\nrest of the comment\non 2 lines'
        ...         '\n\n!!! DO NOT EDIT BELOW THIS LINE !!!\n[[{"data_source": "Source of the data", '
        ...         '"library": "Own process", "review_state": 2,"reviewer_comment": "a reviewer comment", '
        ...         '"comment_for_reviewer": "a comment for reviewer"}]]')
        {'modification_code': '0', 'relevance_code': 'A', 'confidence_code': 'Z', 'relevance_comment': 'info on relevance (the line about modification has been skipped because code 0)', 'confidence_comment': 'info on confidence', 'comment': 'rest of the comment\non 2 lines', 'data_source': 'Source of the data', 'library': 'Own process', 'review_state': 2, 'reviewer_comment': 'a reviewer comment', 'comment_for_reviewer': 'a comment for reviewer'}
        >>> extract_data_from_comment('Comment without acv cirad data\n\n!!! DO NOT EDIT BELOW THIS LINE !!!\n'
        ...         '[[{"review_state": 2, "reviewer_comment": "a reviewer comment", '
        ...         '"comment_for_reviewer": "a comment for reviewer"}]]')
        {'comment': 'Comment without acv cirad data', 'review_state': 2, 'reviewer_comment': 'a reviewer comment', 'comment_for_reviewer': 'a comment for reviewer'}
        >>> extract_data_from_comment('AY:\nA: info on relevance\nY: info on confidence')
        {'relevance_code': 'A', 'confidence_code': 'Y', 'relevance_comment': 'info on relevance', 'confidence_comment': 'info on confidence'}
        >>> extract_data_from_comment('Just a simple comment')
        {'comment': 'Just a simple comment'}
        >>> extract_data_from_comment('BY')
        {'relevance_code': 'B', 'confidence_code': 'Y'}
        >>> extract_data_from_comment('(3AZ)\n\nComments on quality data are missing')
        {'modification_code': '3', 'relevance_code': 'A', 'confidence_code': 'Z', 'comment': 'Comments on quality data are missing'}
    """

    if comment is None:
        return dict()

    comment = str(comment)

    # If JSON data are presents, isolates it
    if '!!! DO NOT EDIT BELOW THIS LINE !!!' in comment:
        comment, json_data = comment.split('!!! DO NOT EDIT BELOW THIS LINE !!!\n[[')

        # Stripping the strailing ]]
        json_data = json_data[:-2]

        # Unserializing json data
        json_data = json.loads(bytes(json_data, 'utf-8'))
    else:
        json_data = {}

    # Defining regexps
    # Finding if the comment contains a header with quality codes
    find_quality_codes_header = r"^\(?(?! ?:?\n)((?P<modification_code>[0123]) ?[-,;]? ?)?((?P<relevance_code>[AB]) ?[-,;]? ?)?(?P<confidence_code>[YZ])? ?:?\)? ?(\n|$)"

    # Finding quality codes and comments (with header removed)
    find_quality_codes_with_comments = r"^((?P<modification_code>[0123])(?!\w) ?:?-? ?(?P<modification_comment>.*)(\n|$))?((?P<relevance_code>[AB])(?!\w) ?:?-? ?(?P<relevance_comment>.*)(\n|$))?((?P<confidence_code>[YZ])(?!\w) ?:?-? ?(?P<confidence_comment>.*)(\n|$))?"

    # Extracting potential quality data header
    data = re.search(find_quality_codes_header, comment)
    result = data.groupdict() if data is not None else dict()

    # Removing quality data header form comment
    comment = re.sub(find_quality_codes_header, '', comment)

    # Extracting quality data code+comment
    data2 = re.search(find_quality_codes_with_comments, comment)
    data2 = {k: v for k, v in data2.groupdict().items() if v not in (None, '')}

    result.update(data2)
    result = {k: v for k, v in result.items() if v not in (None, '')}

    # Removing quality data form comment
    comment = re.sub(find_quality_codes_with_comments, '', comment)

    result.update({'comment': comment.strip(), **json_data})

    # Removing trailing newlines after the comment
    if 'comment' in result:
        result['comment'] = result['comment'].rstrip()

        if result['comment'] == '':
            del result['comment']

    result = {**result, **json_data}

    return result
