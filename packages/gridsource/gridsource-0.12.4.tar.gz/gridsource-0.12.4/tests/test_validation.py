#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `gridsource` package."""

import os
import shutil
from pprint import pprint as pp

import numpy as np
import pandas as pd
import pytest

from gridsource import Data as IVData
from gridsource import ValidData as VData


def test_00():
    data = VData()
    # ------------------------------------------------------------------------
    # Create a schema for "test" tab
    # This example show a YAML schema syntax,
    # but json or plain dict is also OK:
    data._set_schema(
        "test",
        "---"
        "\nid:"
        "\n  types: integer"
        "\n  unique: true"
        "\n  mandatory: true"
        "\nname:"
        "\n  types: string"
        "\n  mandatory: true"
        "\nfirstname:"
        "\n  types: string"
        "\nage:"
        "\n  types: integer"
        "\n  minimum: 0"
        "\nlife_nb:"
        "\n  types: integer"
        "\n  mandatory: true"
        "\n  maximum: 4",
    )
    # ------------------------------------------------------------------------
    # create dummy data
    data._data["test"] = pd.DataFrame(
        {
            "id": {7: 0, 1: 1, 2: 5},
            "name": {7: "Doe", 1: "Fante", 2: "Mercury"},
            "firstname": {7: "John", 2: "Freddy", 1: "Richard"},
            "age": {7: "42", 1: 22},
            "life_nb": {7: 5, 1: "hg", 2: 15},
        }
    )
    expected_report = {
        ("age", 0): [
            "'42' is not valid under any of the given schemas",
            "'42' is not of type 'integer'",
            "'42' is not of type 'null'",
        ],
        ("life_nb", 0): ["5 is greater than the maximum of 4"],
        ("life_nb", 1): ["'hg' is not of type 'integer'"],
        ("life_nb", 2): ["15 is greater than the maximum of 4"],
    }
    is_valid, errors = data.validate_tab("test")
    assert is_valid is False
    assert errors == expected_report


@pytest.fixture
def datadir():
    """
    Basic IO Structure
    """
    test_dir = os.path.dirname(os.path.realpath(__file__))
    indir = os.path.join(test_dir, "data")
    outdir = os.path.join(test_dir, "_out")
    # ensure outdir exists and is empty
    if os.path.isdir(outdir):
        shutil.rmtree(outdir)
    os.makedirs(outdir)
    return indir, outdir


def test_01(datadir):
    indir, outdir = datadir
    data = IVData()
    data.read_excel(os.path.join(indir, "test_00.xlsx"))
    data.read_schema(os.path.join(indir, "test_00.schema.yaml"))
    for tab in ("names", "cars", "empty"):
        print('checking "%s"' % tab, end="... ")
        is_ok, errors = data.validate_tab(tab)
        try:
            assert is_ok is True
        except:
            print("OUPS!")
            __import__("pdb").set_trace()
        else:
            print("OK")
        assert errors == {}
    # ------------------------------------------------------------------------
    # export and reimport to/from various formats
    for extension in (".cfg", ".xlsx", ".ini"):
        target = os.path.join(outdir, "test_00" + extension)
        print("test '%s' extension" % target)
        assert not os.path.isfile(target)
        data.to(target)
        assert os.path.isfile(target)
        # --------------------------------------------------------------------
        # read the newly created file
        data_new = IVData()
        data_new.read(target)
        data_new.read_schema(os.path.join(indir, "test_00.schema.yaml"))
        for tab in data._data.keys():
            print('checking "%s"' % tab, end="... ")
            is_ok, errors = data_new.validate_tab(tab)
            try:
                assert is_ok is True
            except:
                print("OUPS!")
                __import__("pdb").set_trace()
            else:
                print("OK")
            assert errors == {}


def test_02(datadir):
    indir, outdir = datadir
    data = IVData()
    data.read_excel(os.path.join(indir, "test_00.xlsx"))
    data.read_schema(os.path.join(indir, "test_00.schema.yaml"))
    ret = data.validate()
    assert len(ret) == 0
    for tabname, (is_ok, retvals) in ret.items():
        assert is_ok
        assert len(retvals) == 0


def test_03(datadir):
    indir, outdir = datadir
    data = IVData()
    data.read_excel(os.path.join(indir, "test_00.xlsx"))
    data.read_schema(os.path.join(indir, "test_00.schema2.yaml"))
    ret = data.validate()
    assert ret == {"cars": {("Year", 2): ["None is not of type 'integer'"]}}
