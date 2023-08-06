#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A set of dataclasses concerning roles of persons and their particulars."""

import os
import sys
from dataclasses import dataclass, field
from typing import List, Optional

PACKAGE_PARENT = ".."
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)  # isort:skip # noqa # pylint: disable=wrong-import-position
sys.path.append(
    os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT))
)  # isort: skip # noqa # pylint: disable=wrong-import-position

from personroles.person import Person  # type: ignore  # noqa
from personroles.resources import helpers  # type: ignore  # noqa
from personroles.resources.constants import (  # type: ignore # noqa
    GERMAN_PARTIES,
)
from personroles.resources.helpers import AttrDisplay  # type: ignore # noqa
from personroles.resources.helpers import NotGermanParty  # type: ignore # noqa
from personroles.resources.helpers import Party  # type: ignore # noqa


@dataclass
class _Politician_default:
    """Data about a politician's party and office(s)."""
    parties: List[Party] = field(default_factory=lambda: [])
    minister: Optional[str] = field(default=None)
    offices: List[str] = field(default_factory=lambda: [])


@dataclass
class Politician(
    _Politician_default,
    helpers._Party_default,
    Person,
    helpers._Party_base,
    AttrDisplay,
):
    """
    A politician's basic data.

    Module politician_role.py is collecting party affiliation, minister (like
    "JM": Justizminister), offices (in case more than one ministry position is
    filled (i.e. ["JM", "FM"]), and personal data like name, age, gender ...
    """

    def __post_init__(self):
        Party.__post_init__(self)
        Person.__post_init__(self)
        Person.get_sex(self)
        Person.get_age(self)
        self.add_Party(
            self.party_name, self.party_entry, self.party_exit
        )
        if self.minister is not None and self.minister not in self.offices:
            self.offices.append(self.minister)

    def add_Party(self, party_name, party_entry="unknown", party_exit="unknown") -> None:  # noqa
        if party_name in GERMAN_PARTIES:
            self._change_dict_to_Party()
            if self._party_in_parties(party_name, party_entry, party_exit):
                self._update_parties(party_name, party_entry, party_exit)
            else:
                self.party_name = party_name
                self.party_entry = party_entry
                self.party_exit = party_exit
                party = Party(self.party_name, self.party_entry, self.party_exit)  # noqa
                self.parties.append(party)
        else:
            raise NotGermanParty()

    def _update_party(self, party, party_name, party_entry, party_exit) -> Party:  # noqa
        if party_entry != "unknown" and party.party_entry == "unknown":
            party.party_entry = party_entry
        if party_exit != "unknown" and party.party_exit == "unknown":
            party.party_exit = party_exit
        return party

    def _update_parties(self, party_name, party_entry="unknown", party_exit="unknown") -> None:  # noqa
        if self._party_in_parties(party_name, party_entry, party_exit):
            parties_tmp = self.parties[:]
            for prty in parties_tmp:
                if prty.party_name == party_name:
                    updated_party = self._update_party(prty, party_name, party_entry, party_exit)  # noqa
                    self.parties.remove(prty)
                    self.parties.append(updated_party)
                    self.party_entry = updated_party.party_entry
                    self.party_exit = updated_party.party_exit
                    break

    def _change_dict_to_Party(self) -> None:  # noqa
        parties_tmp = self.parties[:]
        for party in parties_tmp:
            if isinstance(party, dict):
                prty = Party(**party)
                self.parties.remove(party)
                self.parties.append(prty)

    def _party_in_parties(self, party_name, party_entry, party_exit) -> bool:
        parties_tmp = self.parties[:]
        for party in parties_tmp:
            if party_name == party.party_name:
                return True
        return False


if __name__ == "__main__":

    politician = Politician(
        "SPD",
        "Bärbel",
        "Gutherz",
        academic_title="Dr.",
        date_of_birth="1980",
    )
    print(politician)
    print()

    politician.add_Party("Linke", party_entry="2016")
    print(politician)
    print(politician.first_name)
    print(politician.party_name)
    for party in politician.parties:
        print(party)
        print(party.party_name)
        print()
