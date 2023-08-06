#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains helpful utility functions
"""
import os
import json
import pandas as pd
from string import ascii_letters, digits

MITO_FOLDER = os.path.expanduser("~/.mito")


def empty_column_python_code():
    """
    Helper functions for creating an empty entry
    for column_python_code - which can then be filled 
    in later (or left empty for an unedited column)
    """
    return {
        'column_name_change': None,
        'column_type_change': None,
        'column_value_changes': {},
        'column_formula_changes': ''
    }

def code_container(code):
    """
    Returns the code block with
    # MITO CODE START
    and
    # MITO CODE END

    SAME FUNCTION IN PLUGIN.ts
    """

    return f'# MITO CODE START\n\n{code}\n\n# MITO CODE END'

def is_valid_header(column_header):
    """
    A header is valid if:
    1. It is a string
    2. It only contains alphanumber characters, or _
    3. It has at least one non-numeric character.

    Valid examples: A, ABC, 012B, 213_bac, 123_123
    Invalid examples: 123, 123!!!, ABC!, 123-123

    This is a result of not being able to distingush column headers from constants
    otherwise, and would not be necessary if we had a column identifier!
    """

    return isinstance(column_header, str) and ( # Condition (1)
        set(column_header).issubset(set(ascii_letters).union(set(digits)).union(set(['_']))) and # Condition (2)
        not column_header.isdigit() # Condition (3)
    )


def get_invalid_headers(df: pd.DataFrame):
    """
    Given a dataframe, returns a list of all the invalid headers this list has. 
    """
    return [
        header for header in df.columns.tolist()
        if not is_valid_header(header)
    ]


def dfs_to_json(dfs):
    return json.dumps([df_to_json_dumpsable(df) for df in dfs])


def df_to_json_dumpsable(df):
    """
    Returns a dataframe represented in a way that can be turned into a 
    JSON object with json.dumps
    """
    json_obj = json.loads(df.to_json(orient="split"))
    # Then, we go through and find all the null values (which are infinities),
    # and set them to undefined.
    for d in json_obj['data']:
        for idx, e in enumerate(d):
            if e is None:
                d[idx] = 'undefined'
    return json_obj


def read_analysis(analysis_name):
    """
    Given an analysis_name, reads the saved analysis in
    ~/.mito/{analysis_name}.json and returns a JSON object
    representing it.
    """
    analysis_path = f'{MITO_FOLDER}/{analysis_name}.json'

    if not os.path.exists(analysis_path):
        return None

    with open(analysis_path) as f:
        try:
            # We try and read the file as JSON
            return json.load(f)
        except: 
            return None

def make_steps_json_obj(steps):
    """
    Given a steps dictonary from a widget_state_container, puts the steps
    into a format that can be saved and recreated. Necessary for saving an
    analysis to a file!
    """
    steps_json_obj = dict()
    for step_id, step in steps.items():
        step_type = step['step_type']
        if step_type == 'formula':
            steps_json_obj[step_id] = {
                'step_type': step_type,
                'column_spreadsheet_code': step['column_spreadsheet_code']
            }
        if step_type == 'merge':
            steps_json_obj[step_id] = {
                'step_type': step_type,
                'sheet_index_one': step['sheet_index_one'],
                'merge_key_one': step['merge_key_one'],
                'sheet_index_two': step['sheet_index_two'],
                'merge_key_two': step['merge_key_two']
            }
        if step_type == 'column_rename':
            steps_json_obj[step_id] = {
                'step_type': 'column_rename',
                'sheet_index': step['sheet_index'],
                'old_column_header': step['old_column_header'],
                'new_column_header': step['new_column_header']
            }

    return steps_json_obj


def write_analysis(widget_state_container):
    """
    Writes the analysis saved in widget_state_container to
    ~/.mito/{widget_state_container.analysisName}.

    NOTE: as the written analysis is from the widget_state_container,
    we assume that the analysis is valid when written and read back in!
    """

    if not os.path.exists(MITO_FOLDER):
        os.mkdir(MITO_FOLDER)

    analysis_path = f'{MITO_FOLDER}/{widget_state_container.analysis_name}.json'

    with open(analysis_path, 'w+') as f:
        # TODO: replace this with _all_ the steps, rather than just the most recent

        steps_json_obj = make_steps_json_obj(widget_state_container.steps)

        f.write(json.dumps({
            'steps': steps_json_obj,
            'version': 1 # we save the version we can upgrade the format, if we need to!
        }))
        # NOTE: When you change this format, update the string at the bottom of this file!!!

"""
NOTE: update this when you change the format that we write out!

This string will store a history of all the version. We inline it in the code, so it's always close by
and we don't forget to update it. Include an example of the object here!

1:
{"steps": {"0": {"step_type": "formula", "column_spreadsheet_code": [{"A": "", "C": ""}, {"A": "", "B": ""}]}, "1": {"step_type": "merge", "sheet_index_one": 0, "merge_key_one": "A", "sheet_index_two": 1, "merge_key_two": "A"}, "2": {"step_type": "formula", "column_spreadsheet_code": [{"A": "", "C": ""}, {"A": "", "B": ""}, {"A": "", "C": "", "B": "", "D": "=LEFT(B)"}]}}, "version": "0.1.26"}
- We just save all the steps now!
"""