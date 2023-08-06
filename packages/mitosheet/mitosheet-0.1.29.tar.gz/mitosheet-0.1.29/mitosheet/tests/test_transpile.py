#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

import pytest

from ..transpile import transpile
from mitosheet.tests.test_utils import create_mito_wrapper


def test_transpile_single_column():
    mito = create_mito_wrapper(['abc'])
    mito.set_formula('=A', 0, 'B', add_column=True)
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == ['# Step 1', 'df1[\'B\'] = df1[\'A\']']


def test_transpile_multiple_columns_no_relationship():
    mito = create_mito_wrapper(['abc'])
    mito.add_column(0, 'B')
    mito.add_column(0, 'C')
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert 'df1[\'B\'] = 0' in code_container['code']
    assert 'df1[\'C\'] = 0' in code_container['code']

def test_transpile_columns_in_each_sheet():
    mito = create_mito_wrapper(['abc'], sheet_two_A_data=['abc'])
    mito.add_column(0, 'B')
    mito.add_column(1, 'B')
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert 'df1[\'B\'] = 0' in code_container['code']
    assert 'df2[\'B\'] = 0' in code_container['code']

def test_transpile_multiple_columns_linear():
    mito = create_mito_wrapper(['abc'])
    mito.set_formula('=A', 0, 'B', add_column=True)
    mito.set_formula('=B', 0, 'C', add_column=True)
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == ['# Step 1', 'df1[\'B\'] = df1[\'A\']', 'df1[\'C\'] = df1[\'B\']']

COLUMN_HEADERS = [
    ('ABC'),
    ('ABC_D'),
    ('ABC_DEF'),
    ('ABC_123'),
    ('ABC_HAHA_123'),
    ('ABC_HAHA-123'),
    ('---data---'),
    ('---da____ta---'),
    ('--'),
]
@pytest.mark.parametrize("column_header", COLUMN_HEADERS)
def test_transpile_column_headers_non_alphabet(column_header):
    mito = create_mito_wrapper(['abc'])
    mito.set_formula('=A', 0, column_header, add_column=True)
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == ['# Step 1', f'df1[\'{column_header}\'] = df1[\'A\']']


COLUMN_HEADERS = [
    ('ABC'),
    ('ABC_D'),
    ('ABC_DEF'),
    ('ABC_123'),
    ('ABC_HAHA_123'),
    ('ABC_HAHA-123'),
    ('---data---'),
    ('---da____ta---'),
    ('--'),
]
@pytest.mark.parametrize("column_header", COLUMN_HEADERS)
def test_transpile_column_headers_non_alphabet_multi_sheet(column_header):
    mito = create_mito_wrapper(['abc'], sheet_two_A_data=['abc'])
    mito.set_formula('=A', 0, column_header, add_column=True)
    mito.set_formula('=A', 1, column_header, add_column=True)
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == ['# Step 1', f'df1[\'{column_header}\'] = df1[\'A\']', f'df2[\'{column_header}\'] = df2[\'A\']']