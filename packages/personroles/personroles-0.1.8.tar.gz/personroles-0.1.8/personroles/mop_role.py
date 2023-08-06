#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A set of dataclasses concerning roles of persons and their particulars."""

import os
import sys
from dataclasses import asdict, dataclass, field
from typing import List, Optional

PACKAGE_PARENT = ".."
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)  # isort:skip # noqa # pylint: disable=wrong-import-position
sys.path.append(
    os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT))
)  # isort: skip # noqa # pylint: disable=wrong-import-position

from personroles.politician_role import Politician  # type: ignore  # noqa
from personroles.resources.helpers import AttrDisplay  # type: ignore # noqa
from personroles.resources.helpers import NotInRange  # type: ignore # noqa
from personroles.resources.mop_tinyDB import Mops_TinyDB  # type: ignore # noqa


@dataclass
class _MoP_default:
    mop_id: int = field(default=0)
    electoral_ward: str = field(default="ew")
    ward_no: Optional[int] = field(default=None)
    voter_count: Optional[int] = field(default=None)
    parl_pres: bool = field(default=False)
    parl_vicePres: bool = field(default=False)
    parliament_entry: str = field(default="unknown")  # date string: "11.3.2015"  # noqa
    parliament_exit: str = field(default="unknown")  # dto.
    speeches: List[str] = field(
        default_factory=lambda: []
    )  # identifiers for speeches  # noqa
    reactions: List[str] = field(
        default_factory=lambda: []
    )  # identifiers for reactions

    def renamed_wards(self):
        """Some electoral wards have been renamed in the Wikipedia."""
        wards = {
            "Kreis Aachen I": "Aachen III",
            "Hochsauerlandkreis II – Soest III": "Hochsauerlandkreis II",
            "Kreis Aachen II": "Aachen IV"
            if self.last_name in ["Wirtz", "Weidenhaupt"]
            else "Kreis Aachen I",
        }
        if self.electoral_ward in wards.keys():
            self.electoral_ward = wards[self.electoral_ward]

    def scrape_wiki_for_ward(self) -> None:
        """Find tables in Wikipedia containing informations about electoral wards."""  # noqa
        import requests
        from bs4 import BeautifulSoup  # type: ignore

        URL_base = "https://de.wikipedia.org/wiki/Landtagswahlkreis_{}"
        URL = URL_base.format(self.electoral_ward)
        req = requests.get(URL)
        bsObj = BeautifulSoup(req.text, "lxml")
        table = bsObj.find(class_="infobox float-right toptextcells")
        self.scrape_wiki_table_for_ward(table)

    def scrape_wiki_table_for_ward(self, table) -> None:
        for td in table.find_all("td"):
            if "Wahlkreisnummer" in td.text:
                ward_no = td.find_next().text.strip()
                ward_no = ward_no.split(" ")[0]
                self.ward_no = int(ward_no)
            elif "Wahlberechtigte" in td.text:
                voter_count = td.find_next().text.strip()
                voter_count = self.fix_voter_count(voter_count)
                self.voter_count = int(voter_count)

    def fix_voter_count(self, voter_count):
        if voter_count[-1] == "]":
            voter_count = voter_count[:-3]
        if " " in voter_count:
            voter_count = "".join(voter_count.split(" "))
        else:
            voter_count = "".join(voter_count.split("."))
        return voter_count


@dataclass
class _MoP_base:
    legislature: str
    state: str


@dataclass
class MoP(_MoP_default, Politician, _MoP_base, AttrDisplay):
    """
    Module mop_role.py covers the role as member of parliament.

    The role integrates the role of politician and adds a federal state (like
    "NRW" or "BY") and legislature (legislative term) as obligatory
    informations to define the role. More informations like speeches held or
    offices (like president) filled can be added. Call politician's
    __post_init__ to initialize wards and voters.
    """

    def __post_init__(self):
        """
        Check if legislature is correct for NRW and add legislature into the
        mop's list of memberships (in case more than one term is spent in
        parliament.
        """
        if int(self.legislature) not in range(14, 18):
            raise NotInRange("Number for legislature not in range")
        Politician.__post_init__(self)
        self.change_ward()

    def change_ward(self, ward=None):
        if ward:
            self.electoral_ward = ward
        if self.electoral_ward not in ["ew", "Landesliste"]:
            self.renamed_wards()
            self.scrape_wiki_for_ward()
        else:
            self.electoral_ward = "ew"


if __name__ == "__main__":

    mop_1 = MoP("14", "NRW", "SPD", "Tom", "Schwadronius", party_entry="1990",
                peer_title="Junker von", date_of_birth="1950")
    mop_2 = MoP("15", "NRW", "Grüne", "Sabine", "Dingenskirchen",
                electoral_ward="Essen II", peer_preposition="von")
    mop_3 = MoP("15", "NRW", "Grüne", "Sammy", "Goodwill",
                electoral_ward="Duisburg II", academic_title="Dr")
    mop_4 = MoP("15", "NRW", "FDP", "Ralf", "Witzel",
                electoral_ward="Essen III")
    mop_5 = MoP("16", "NRW", "SPD", "Horst", "Schmitt",
                electoral_ward="Düsseldorf III")

    print(mop_1)

    mop_1.add_Party("Grüne", party_entry="30.11.1999")
    mop_1.change_ward("Düsseldorf II")
    print(mop_1)
    print()

    print(mop_1.__dict__)
    print()

    # Dataclasses come with an asdict module:
    # https://stackoverflow.com/a/35282286/6597765
    print(asdict(mop_1))

    db = Mops_TinyDB(".")
    db.delete_all()
    db.add_mop(asdict(mop_1))
    print(mop_2)

    db.add_mop(asdict(mop_2))
    field = "last_name"  # type: ignore
    value = "Schwadronius"  # type: ignore
    print(f"print(db.all(field={field}, value={value})):")
    print(db.list_mops(field=field, value=value))
    print()
    print("-" * 50)
    print("for item in db.list_mops()")
    for item in db.list_mops():
        # convert dict back to dataclass:
        # https://www.reddit.com/r/learnpython/comments/9h74no/convert_dict_to_dataclass/e69p8m8?utm_source=share&utm_medium=web2x&context=3  # noqa
        mop = MoP(**item)
        print(mop)

    db.add_mop(asdict(mop_3))
    db.add_mop(asdict(mop_4))
    db.add_mop(asdict(mop_5))

    field = "party_name"  # type: ignore
    value = "Grüne"

    print("-" * 50)
    print("for item in db.list_mops(field=party_name, value=Grüne):")
    for item in db.list_mops(field=field, value=value):
        # convert dict back to dataclass:
        # https://www.reddit.com/r/learnpython/comments/9h74no/convert_dict_to_dataclass/e69p8m8?utm_source=share&utm_medium=web2x&context=3  # noqa
        mop = MoP(**item)
        print(mop)

    field = "party_name"  # type: ignore
    value = "SPD"

    print("-" * 50)
    print("for item in db.list_mops(field=party_name, value=SPD):")
    for item in db.list_mops(field=field, value=value):
        # convert dict back to dataclass:
        # https://www.reddit.com/r/learnpython/comments/9h74no/convert_dict_to_dataclass/e69p8m8?utm_source=share&utm_medium=web2x&context=3  # noqa
        mop = MoP(**item)
        print(mop)

    print("-" * 50)
    print("db.get_mop(mop_id=2):")
    item = db.get_mop(mop_id=2)
    mop = MoP(**item)
    print(mop)

    os.remove("./.mops_db.json")
