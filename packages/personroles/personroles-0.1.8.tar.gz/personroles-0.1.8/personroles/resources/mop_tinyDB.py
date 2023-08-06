#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Database wrapper for mops instances."""
import os
import sys
from typing import Optional

import tinydb  # type: ignore # isort: skip # noqa # pylint: disable=wrong-import-position


PACKAGE_PARENT = ".."
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)  # isort:skip # noqa # pylint: disable=wrong-import-position
sys.path.append(
    os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT))
)  # isort: skip # noqa # pylint: disable=wrong-import-position


class Mops_TinyDB():
    """Wrapper class for TinyDB."""

    def __init__(self, db_path):
        """Connect to DB."""
        self._db = tinydb.TinyDB(db_path + "mops_db.json")

    def add_mop(self, mop: dict) -> int:
        """Add a mop dict to DB."""
        mop_id = self._db.insert(mop)
        mop["mop_id"] = mop_id
        self._db.update(mop, doc_ids=[mop_id])
        return mop_id

    def get_mop(self, mop_id: int) -> Optional[dict]:
        """Return a mop dict with matching id."""
        if self._db.contains(doc_id=mop_id):
            return self._db.get(doc_id=mop_id)
        else:
            return None

    def list_mops(self, field=None, value=None):  # type (str) -> list[dict]
        """Return list of mops."""
        if field is None:
            return self._db.all()
        else:
            return self._db.search(tinydb.where(field) == value)

    def count(self) -> int:
        """Return number of mops in DB."""
        return len(self._db)

    def update_mop(self, mop_id: int, field=None, value=None) -> None:
        """Modify mop in DB with given mop_id."""
        self._db.update({field: value}, doc_ids=[mop_id])
        if field in ["party_entry", "party_exit"]:
            self._update_parties(mop_id, field, value)

    def _update_parties(self, mop_id: int, field, value) -> None:
        mop = self._db.get(doc_id=mop_id)
        party_name = mop["party_name"]
        index = None
        for i, party in enumerate(mop["parties"]):
            if party["party_name"] == party_name:
                index = i
        if index is not None:
            party_entry, party_exit = self._assign_party_details(mop, party, field, value)  # noqa
            mop["parties"][index] = {"party_name": party_name,
                                     "party_entry": party_entry,
                                     "party_exit": party_exit}
            self.delete(mop_id)
            self.add_mop(mop)

    def _assign_party_details(self, mop, party, field, value):
        if field == "party_entry":
            party_entry = value
            party_exit = party["party_exit"]
        elif field == "party_exit":
            party_entry = party["party_entry"]
            party_exit = value

        return party_entry, party_exit

    def delete(self, mop_id: int) -> None:
        """Remove a mop from DB with given mop_id."""
        self._db.remove(doc_ids=[mop_id])

    def delete_all(self):
        """Remove all mops from DB."""
        self._db.truncate()

    def unique_id(self):  # type () -> int
        """Return an integer that does not exist in the db."""
        i = 1
        while self._db.contains(doc_id=i):
            i += 1
        return i


def stop_mops_db(db_path: str) -> None:
    """Disconnect from DB."""
    pass


def start_mops_db(db_path: str) -> Mops_TinyDB:
    """Connect to DB."""
    return Mops_TinyDB(db_path)
