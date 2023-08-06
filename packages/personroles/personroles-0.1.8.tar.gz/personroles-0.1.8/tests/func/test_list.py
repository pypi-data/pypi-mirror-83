#!/usr/bin/env python
# -*- coding: utf-8 -*-
# test_list.py
"""Tests the list function of mop_tinyDB."""


def test_list_returns_list(db_with_3_mops):
    """Test mop_db.list_mops() should return a list."""
    db = db_with_3_mops
    mops = db.list_mops()
    assert isinstance(mops, list)  # nosec


def test_list_returns_list_of_dicts(db_with_3_mops):
    """Test list_mops() returns a list of dicts."""
    db = db_with_3_mops
    mops = db.list_mops()
    for mop in mops:
        assert isinstance(mop, dict)  # nosec


def test_list_returns_list_with_valid_field(db_with_6_mops):
    """Test list_mops(field="party_name", value="SPD") returns correct entries."""  # noqa
    db = db_with_6_mops
    field = "party_name"
    value = "SPD"
    mops = db.list_mops(field=field, value=value)
    for mop in mops:
        assert mop["party_name"] == "SPD"  # nosec
