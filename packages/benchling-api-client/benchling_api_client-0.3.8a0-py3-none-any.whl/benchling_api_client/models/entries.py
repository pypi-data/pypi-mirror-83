from typing import Any, Dict, List, Optional

import attr

from ..models.entry import Entry


@attr.s(auto_attribs=True)
class Entries:
    """  """

    entries: Optional[List[Entry]] = None

    def to_dict(self) -> Dict[str, Any]:
        if self.entries is None:
            entries = None
        else:
            entries = []
            for entries_item_data in self.entries:
                entries_item = entries_item_data.to_dict()

                entries.append(entries_item)

        return {
            "entries": entries,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Entries":
        entries = []
        for entries_item_data in d.get("entries") or []:
            entries_item = Entry.from_dict(entries_item_data)

            entries.append(entries_item)

        return Entries(
            entries=entries,
        )
