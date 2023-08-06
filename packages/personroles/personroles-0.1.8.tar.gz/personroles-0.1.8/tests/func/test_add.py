#!/usr/bin/env python
# -*- coding: utf-8 -*-
# test_add.py
"""Tests the add function of mop_tinyDB."""
from dataclasses import asdict

from context import mop_role

new_mop = mop_role.MoP("17", "NRW", "Grüne", "Gudrun B.", "Heinz")


def test_add_returns_valid_id(mops_db_fixture):
    """Test mop_db.add_mop(<valid mop>) should return an integer."""
    db = mops_db_fixture
    mop_id = db.add_mop(asdict(new_mop))
    assert isinstance(mop_id, int)  # nosec


def test_add_increases_count(db_with_3_mops):
    """Test add_mop() affect on mop_db.count()."""
    db = db_with_3_mops
    mop_id = db.add_mop(asdict(new_mop))
    assert db.count() == mop_id  # nosec


def test_add_returns_correct_id(db_with_3_mops):
    """Test add_mop() affect on mop_db.count()."""
    db = db_with_3_mops
    mop_id = db.add_mop(asdict(new_mop))
    assert mop_id == 4  # nosec
