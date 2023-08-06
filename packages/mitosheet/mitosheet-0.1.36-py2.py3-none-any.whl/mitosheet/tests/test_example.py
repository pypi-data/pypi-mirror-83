#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.
import pandas as pd
import pytest

from ..example import MitoWidget, sheet
from ..utils import get_invalid_headers
from mitosheet.errors import EditError

def test_example_creation_blank():
    df = pd.DataFrame()
    w = MitoWidget(df)

VALID_DATAFRAMES = [
    (pd.DataFrame()),
    (pd.DataFrame(data={'A': [1, 2, 3]})),
    (pd.DataFrame(data={'A0123': [1, 2, 3]})),
]
@pytest.mark.parametrize("df", VALID_DATAFRAMES)
def test_sheet_creates_valid_dataframe(df):
    mito = sheet(df)
    assert mito is not None

NON_VALID_HEADER_DATAFRAMES = [
    (pd.DataFrame(data={0: [1, 2, 3]})),
    (pd.DataFrame(data=[1, 2, 3])),
    (pd.DataFrame(data={'A': [1, 2, 3], 0: [1, 2, 3]})),
    (pd.DataFrame(data={'A': [1, 2, 3], '000': [1, 2, 3]})),
    (pd.DataFrame(data={'A': [1, 2, 3], 'abc-123': [1, 2, 3]})),
    (pd.DataFrame(data={'A': [1, 2, 3], '-123': [1, 2, 3]})),
    (pd.DataFrame(data={'A': [1, 2, 3], '-123_': [1, 2, 3]})),
    (pd.DataFrame(data={'A': [1, 2, 3], '-abc_': [1, 2, 3]})),
]
@pytest.mark.parametrize("df", NON_VALID_HEADER_DATAFRAMES)
def test_sheet_errors_during_non_string_headers(df):
    assert len(get_invalid_headers(df)) != 0
    with pytest.raises(Exception) as e_info:
        sheet(df)

def test_create_with_multiple_dataframes():
    mito = sheet(pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(data={'A': [1, 2, 3]}))
    assert mito is not None

def test_create_with_multiple_dataframes_single_invalid_header():
    with pytest.raises(EditError):
        mito = sheet(pd.DataFrame(data={'A': [1, 2, 3]}), pd.DataFrame(data={'B': [1, 2, 3]}), pd.DataFrame(data={'0': [1, 2, 3]}))