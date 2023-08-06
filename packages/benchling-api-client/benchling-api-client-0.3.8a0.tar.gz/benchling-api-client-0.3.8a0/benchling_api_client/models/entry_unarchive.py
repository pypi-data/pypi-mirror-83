from typing import Any, Dict, List

import attr


@attr.s(auto_attribs=True)
class EntryUnarchive:
    """  """

    entry_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        entry_ids = self.entry_ids

        return {
            "entryIds": entry_ids,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EntryUnarchive":
        entry_ids = d["entryIds"]

        return EntryUnarchive(
            entry_ids=entry_ids,
        )
