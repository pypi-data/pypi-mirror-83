#!/usr/bin/env python
# -*- coding: utf-8 -*-
# test_update.py
"""Tests the update function of mop_tinyDB."""


def test_update_party_entry(db_with_3_mops):
    """Test update_mop(field="party_entry", value="2010") updates mop's data."""  # noqa
    db = db_with_3_mops
    field = "party_entry"
    value = "2010"
    mop_id = 2
    mop = db.get_mop(mop_id=mop_id)
    db.update_mop(mop_id, field=field, value=value)
    mop = db.get_mop(mop_id)
    assert mop["party_entry"] == "2010"  # nosec
    assert mop["parties"][0]["party_entry"] == "2010"  # nosec


def test_update_party_exit(db_with_3_mops):
    """Test update_mop(field="party_exit", value="2010") updates mop's data."""  # noqa
    db = db_with_3_mops
    field = "party_exit"
    value = "2011"
    mop_id = 1
    mop = db.get_mop(mop_id=mop_id)
    db.update_mop(mop_id, field=field, value=value)
    mop = db.get_mop(mop_id)
    assert mop["party_exit"] == "2011"  # nosec
    assert mop["parties"][0]["party_exit"] == "2011"  # nosec


def test_update_non_party_entry(db_with_3_mops):
    """Test update_mop(field="academic_title", value="Dr.") updates mop's data."""  # noqa
    db = db_with_3_mops
    field = "academic_title"
    value = "MBA"
    mop_id = 1
    db.update_mop(mop_id, field=field, value=value)
    mop = db.get_mop(mop_id=mop_id)
    assert mop["academic_title"] == "MBA"  # nosec
