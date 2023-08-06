from typing import Any, Dict, List, Optional

import attr

from ..models.note_part import NotePart


@attr.s(auto_attribs=True)
class EntryDay:
    """  """

    date: Optional[str] = None
    notes: Optional[List[NotePart]] = None

    def to_dict(self) -> Dict[str, Any]:
        date = self.date
        if self.notes is None:
            notes = None
        else:
            notes = []
            for notes_item_data in self.notes:
                notes_item = notes_item_data.to_dict()

                notes.append(notes_item)

        return {
            "date": date,
            "notes": notes,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EntryDay":
        date = d.get("date")

        notes = []
        for notes_item_data in d.get("notes") or []:
            notes_item = NotePart.from_dict(notes_item_data)

            notes.append(notes_item)

        return EntryDay(
            date=date,
            notes=notes,
        )
