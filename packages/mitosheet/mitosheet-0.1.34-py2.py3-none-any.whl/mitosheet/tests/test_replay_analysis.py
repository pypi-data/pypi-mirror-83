#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains tests for edit events.
"""
import pytest
import pandas as pd
import json

from mitosheet.example import sheet
from mitosheet.tests.test_utils import create_mito_wrapper

from mitosheet.utils import write_analysis, read_analysis

# We assume only column A exists
PERSIST_ANALYSIS_TESTS = [
    (0, '=0'),
    (1, '=1'),
    (2, '=A + 1'),
    ('APPLE', '=UPPER(\'apple\')'),
    (2, '=LEFT((A + 1) * 100)'),
    ('APPLE', '=UPPER(LOWER(UPPER(\'apple\')))')
]
@pytest.mark.parametrize("b_value,b_formula", PERSIST_ANALYSIS_TESTS)
def test_recover_analysis(b_value, b_formula):
    mito = create_mito_wrapper([1])
    mito.set_formula(b_formula, 0, 'B', add_column=True)
    # We first write out the analysis
    analysis_name = mito.mito_widget.analysis_name
    write_analysis(mito.mito_widget.widget_state_container)

    df = pd.DataFrame(data={'A': [1]})
    new_mito = sheet(df)
    new_mito.receive_message(new_mito, {
        'event': 'update_event',
        'type': 'use_existing_analysis_update',
        'analysis_name': analysis_name
    })

    curr_step = new_mito.widget_state_container.curr_step

    assert curr_step['column_metatype'][0]['B'] == 'formula'
    assert curr_step['column_spreadsheet_code'][0]['B'] == b_formula
    assert new_mito.widget_state_container.dfs[0]['B'].tolist() == [b_value]
    assert new_mito.column_spreadsheet_code_json == json.dumps(curr_step['column_spreadsheet_code'])


# We assume only column A exists
PERSIST_ANALYSIS_TESTS = [
    (0, '=0'),
    (1, '=1'),
    (2, '=A + 1'),
    ('APPLE', '=UPPER(\'apple\')'),
    (2, '=LEFT((A + 1) * 100)'),
    ('APPLE', '=UPPER(LOWER(UPPER(\'apple\')))')
]
@pytest.mark.parametrize("b_value,b_formula", PERSIST_ANALYSIS_TESTS)
def test_persist_analysis_multi_sheet(b_value, b_formula):
    mito = create_mito_wrapper([1], sheet_two_A_data=[1])
    mito.set_formula(b_formula, 0, 'B', add_column=True)
    mito.set_formula(b_formula, 1, 'B', add_column=True)
    # We first write out the analysis
    analysis_name = mito.mito_widget.analysis_name
    write_analysis(mito.mito_widget.widget_state_container)

    df1 = pd.DataFrame(data={'A': [1]})
    df2 = pd.DataFrame(data={'A': [1]})

    new_mito = sheet(df1, df2)
    new_mito.receive_message(mito, {
        'event': 'update_event',
        'type': 'use_existing_analysis_update',
        'analysis_name': analysis_name
    })

    curr_step = new_mito.widget_state_container.curr_step

    assert curr_step['column_metatype'][0]['B'] == 'formula'
    assert curr_step['column_spreadsheet_code'][0]['B'] == b_formula
    assert new_mito.widget_state_container.dfs[0]['B'].tolist() == [b_value]

    assert curr_step['column_metatype'][1]['B'] == 'formula'
    assert curr_step['column_spreadsheet_code'][1]['B'] == b_formula
    assert new_mito.widget_state_container.dfs[1]['B'].tolist() == [b_value]
    
    assert new_mito.column_spreadsheet_code_json == json.dumps(curr_step['column_spreadsheet_code'])


def test_persisit_rename_column():
    mito = create_mito_wrapper([1])
    mito.rename_column(0, 'A', 'NEW_COLUMN')

    analysis_name = mito.mito_widget.analysis_name
    write_analysis(mito.mito_widget.widget_state_container)

    df1 = pd.DataFrame(data={'A': [1]})

    new_mito = sheet(df1)
    new_mito.receive_message(mito, {
        'event': 'update_event',
        'type': 'use_existing_analysis_update',
        'analysis_name': analysis_name
    })

    curr_step = new_mito.widget_state_container.curr_step

    assert curr_step['dfs'][0].equals(pd.DataFrame(data={'NEW_COLUMN': [1]}))