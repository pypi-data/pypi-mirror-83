#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import
import re
import string

__author__ = "Paul Morel"
__copyright__ = "© Copyright 2009-2020, Tartan Solutions, Inc"
__credits__ = ["Paul Morel"]
__license__ = "Proprietary"
__maintainer__ = "Paul Morel"
__email__ = "paul.morel@tartansolutions.com"


def replaceTags(value, data_record):
    """
    As efficiently as possible, replace tags in input string with corresponding values in
    data_record dictionary.

    The idea is to iterate through all of the elements of the data_record, and replace each
    instance of a bracketed key in the input string with the associated value indicated by
    the data record.

    This function will be used a lot, so it's important to make it as efficient as possible.

    Args:
        value (str): The string with tags to replace
        data_record (dict): A dict containing the tags to replace, and what to replace them with

    Returns:
        str: `value` with the tags replaced

    Examples:
        >>> data_record = {"a": "AAA", "b": "BBB"}
        >>> input_value = "aye [a] and bee [b]"
        >>> replaceTags(input_value, data_record)
        'aye AAA and bee BBB'
    """

    prog = re.compile(r"\[([a-zA-Z_][a-zA-Z0-9_\(\)]*)\]")
    matches = prog.finditer(value)

    for match in matches:
        if match.group(1) in data_record:
            value = value.replace(match.group(0), data_record[match.group(1)])

    return value


def apply_variables(message, sub_dict, strict=True, nonstrict_error_handler=None):
    """
    Apply our variable substitution logic, used everywhere throughout analyze.
    It basically works like str.format(), but it raises specific errors

    Args:
        message (str): message with variables to be inserted.
        sub_dict (dict): variables to use for replacement
        strict (bool): If true, error on missing keys. If false, replace missing keys with empty string.
        nonstrict_error_handler (function): function to handle a warning in the case of missing keys. Should take an error_message as an argument.

    Returns:
        (str): the message with the values of variables inserted.
    """
    if message is None:
        return None

    # No position tokens allowed
    message = message.replace('{}', '')

    if not message:
        return message

    if message:
        text_keys = set([
            col[1]
            for col in string.Formatter().parse(message)
            if col[1] is not None
        ])

        bad_keys = [k for k in text_keys if k not in sub_dict]
        if bad_keys:
            bad_string = ", ".join(sorted(bad_keys))
            error_message = (
                'The following variables are invalid '
                'or undefined: {}.'.format(bad_string)
            )
            if strict:
                raise Exception(error_message)
            else:
                # Remove any .format tokens that are missing from the
                # substitution dict
                for key in bad_keys:
                    token = ''.join(('{', str(key), '}'))
                    message = message.replace(token, '')

                if nonstrict_error_handler:
                    nonstrict_error_handler(error_message)

        return message.format(**sub_dict)
