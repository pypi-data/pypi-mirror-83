#!/usr/bin/env python
# -*- coding: utf-8 -*-
# test_mop.py
"""Tests for `mop_role` module."""

import pytest
from context import helpers  # noqa
from context import mop_role

# pylint: disable=redefined-outer-name


def test_mop_role():
    # pylint: disable=W0612, W0613

    mop_1 = mop_role.MoP(
        "14",
        "NRW",
        "Grüne",
        "Alfons-Reimund",
        "Hubbeldubbel",
        peer_title="auf der",
        electoral_ward="Rhein-Sieg-Kreis IV",
        minister="JM",
    )

    assert mop_1.legislature == "14"  # nosec
    assert mop_1.first_name == "Alfons-Reimund"  # nosec
    assert mop_1.last_name == "Hubbeldubbel"  # nosec
    assert mop_1.gender == "male"  # nosec
    assert mop_1.peer_preposition == "auf der"  # nosec
    assert mop_1.party_name == "Grüne"  # nosec
    assert mop_1.parties == [  # nosec
        helpers.Party(
            party_name="Grüne", party_entry="unknown", party_exit="unknown"
        )  # noqa  # nosec
    ]  # noqa  # nosec
    assert mop_1.ward_no == 28  # nosec
    assert mop_1.voter_count == 110389  # nosec
    assert mop_1.minister == "JM"  # nosec

    mop_1.add_Party("fraktionslos")
    assert mop_1.party_name == "fraktionslos"  # nosec
    assert mop_1.parties == [  # nosec
        helpers.Party(
            party_name="Grüne", party_entry="unknown", party_exit="unknown"
        ),  # noqa  # nosec
        helpers.Party(
            party_name="fraktionslos",
            party_entry="unknown",
            party_exit="unknown",  # noqa  # nosec
        ),
    ]

    mop_2 = mop_role.MoP(
        "14",
        "NRW",
        "CDU",
        "Regina",
        "Dinther",
        electoral_ward="Landesliste",
    )  # noqa

    assert mop_2.electoral_ward == "ew"  # nosec

    mop_3 = mop_role.MoP(
        "16",
        "NRW",
        "Piraten",
        "Heiner",
        "Wiekeiner",
        electoral_ward="Kreis Aachen I",
    )  # noqa

    assert mop_3.voter_count == 116389  # nosec

    mop_4 = mop_role.MoP(
        "16",
        "NRW",
        "Linke",
        "Heiner",
        "Wiekeiner",
        electoral_ward="Köln I"
    )  # noqa

    assert mop_4.ward_no == 13  # nosec
    assert mop_4.voter_count == 121721  # nosec

    mop_5 = mop_role.MoP("14", "NRW", "Grüne", "Heiner", "Wiekeiner")

    assert mop_5.electoral_ward == "ew"  # nosec
    assert mop_5.ward_no is None  # nosec
    assert mop_5.voter_count is None  # nosec

    mop_5.change_ward("Essen III")

    assert mop_5.electoral_ward == "Essen III"  # nosec
    assert mop_5.ward_no == 67  # nosec
    assert mop_5.voter_count == 104181  # nosec


def test_person_NotInRangeError():
    # pylint: disable=W0612, W0613
    mop = mop_role.MoP

    with pytest.raises(helpers.NotInRange):
        mop("100", "NRW", "SPD", "Alfons-Reimund", "Hubbeldubbel")
