# -*- coding: utf-8 -*-
# @Author: Selen Calgin
# @Date: 2023-09-25
# @Last Modified by: Selen Calgin

"""Tests of nwb loader for 'nwbmatic' package."""

import nwbmatic as ntm
import pynapple as nap
import numpy as np
import pandas as pd
import pytest
import warnings

@pytest.mark.filterwarnings("ignore")
def test_load_session():
    try:
        data = ntm.load_session("nwbfilestest/allends", "allends")
    except:
        data = ntm.load_session("tests/nwbfilestest/allends", "allends")

    assert isinstance(data.epochs, nap.IntervalSet)
    assert isinstance(data.stimulus_epochs_types, dict)
    assert isinstance(data.stimulus_epochs_blocks, dict)
    assert isinstance(data.stimulus_intervals, dict)
    assert isinstance(data.spikes, nap.TsGroup)
    assert isinstance(data.metadata, dict)
    assert isinstance(data.metadata["stimulus_presentations"], pd.core.frame.DataFrame)
    assert isinstance(data.metadata["stimulus_conditions"], pd.core.frame.DataFrame)
    assert isinstance(data.metadata["stimulus_parameters"], pd.core.frame.DataFrame)
    assert isinstance(data.metadata["channels"], pd.core.frame.DataFrame)
    assert isinstance(data.metadata["probes"], pd.core.frame.DataFrame)
    assert isinstance(data.metadata["units"], pd.core.frame.DataFrame)
    assert isinstance(data.time_support, nap.IntervalSet)
    assert isinstance(data.stimulus_time_support, nap.IntervalSet)

