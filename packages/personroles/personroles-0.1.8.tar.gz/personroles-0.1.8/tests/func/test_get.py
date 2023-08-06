#!/usr/bin/env python
# -*- coding: utf-8 -*-
# test_get.py
"""Tests the get function of mop_tinyDB."""
from context import mop_role

new_mop = mop_role.MoP("17", "NRW", "Grüne", "Gudrun B.", "Heinz")


def test_get_returns_valid_mop(db_with_3_mops, three_mops_fixture):
    """Test mop_db.get_mop(<valid mop_id>) should return the right mop."""
    db = db_with_3_mops

    mop_1 = three_mops_fixture[0]
    mop_1.mop_id = 1
    mop_dict = db.get_mop(1)
    mop = mop_role.MoP(**mop_dict)
    assert mop == mop_1  # nosec

    mop_2 = three_mops_fixture[1]
    mop_2.mop_id = 2
    mop_dict = db.get_mop(2)
    mop = mop_role.MoP(**mop_dict)
    assert mop == mop_2  # nosec


def test_get_returns_None(db_with_3_mops):
    db = db_with_3_mops
    mop_dict = db.get_mop(100)
    assert mop_dict is None  # nosec
