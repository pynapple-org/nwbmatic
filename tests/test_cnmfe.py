# -*- coding: utf-8 -*-
# @Author: gviejo
# @Date:   2022-04-04 22:40:51
# @Last Modified by:   Guillaume Viejo
# @Last Modified time: 2023-06-08 17:04:39

"""Tests of CNMFE loaders for `nwbmatic` package."""

import nwbmatic as ntm
import pynapple as nap
import numpy as np
import pandas as pd
import pytest
import warnings


@pytest.mark.filterwarnings("ignore")
def test_inscopix_cnmfe():
    try:
        data = ntm.load_session("nwbfilestest/inscopix-cnmfe", "inscopix-cnmfe")
    except:
        data = ntm.load_session("tests/nwbfilestest/inscopix-cnmfe", "inscopix-cnmfe")
    assert isinstance(data.C, nap.TsdFrame)
    assert len(data.C.columns) == 10
    assert len(data.C) > 0
    assert isinstance(data.A, np.ndarray)
    assert len(data.A) == len(data.C.columns)


@pytest.mark.filterwarnings("ignore")
def test_minian():
    try:
        data = ntm.load_session("nwbfilestest/minian", "minian")
    except:
        data = ntm.load_session("tests/nwbfilestest/minian", "minian")
    assert isinstance(data.C, nap.TsdFrame)
    assert len(data.C.columns) == 10
    assert len(data.C) > 0
    assert isinstance(data.A, np.ndarray)
    assert len(data.A) == len(data.C.columns)


@pytest.mark.filterwarnings("ignore")
def test_cnmfe_matlab():
    try:
        data = ntm.load_session("nwbfilestest/matlab-cnmfe", "cnmfe-matlab")
    except:
        data = ntm.load_session("tests/nwbfilestest/matlab-cnmfe", "cnmfe-matlab")
    assert isinstance(data.C, nap.TsdFrame)
    assert len(data.C.columns) == 10
    assert len(data.C) > 0
    assert isinstance(data.A, np.ndarray)
    assert len(data.A) == len(data.C.columns)
