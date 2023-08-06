from typing import Any, Dict, List, Optional

import attr


@attr.s(auto_attribs=True)
class EntryUnarchivalResponse:
    """IDs of all items that were unarchived, grouped by resource type. This includes the IDs of entries that were unarchived."""

    entry_ids: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        if self.entry_ids is None:
            entry_ids = None
        else:
            entry_ids = self.entry_ids

        return {
            "entryIds": entry_ids,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EntryUnarchivalResponse":
        entry_ids = d.get("entryIds")

        return EntryUnarchivalResponse(
            entry_ids=entry_ids,
        )
