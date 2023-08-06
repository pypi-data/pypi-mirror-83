#!/usr/bin/env python
# -*- coding: utf-8 -*-
# test_unique_id.py
"""Tests the unique_id function of mop_tinyDB."""


def test_return_unique_id(db_with_3_mops):
    """Test unique_id() returns correct id."""  # noqa
    db = db_with_3_mops
    new_id = db.unique_id()
    assert new_id == 4  # nosec
