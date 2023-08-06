from typing import Any, Dict, List, Optional

import attr

from ..models.entry_table_row import EntryTableRow


@attr.s(auto_attribs=True)
class EntryTable:
    """Actual tabular data with rows and columns of text on the note."""

    name: Optional[str] = None
    column_labels: Optional[List[Optional[str]]] = None
    rows: Optional[List[EntryTableRow]] = None

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        if self.column_labels is None:
            column_labels = None
        else:
            column_labels = self.column_labels

        if self.rows is None:
            rows = None
        else:
            rows = []
            for rows_item_data in self.rows:
                rows_item = rows_item_data.to_dict()

                rows.append(rows_item)

        return {
            "name": name,
            "columnLabels": column_labels,
            "rows": rows,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EntryTable":
        name = d.get("name")

        column_labels = d.get("columnLabels")

        rows = []
        for rows_item_data in d.get("rows") or []:
            rows_item = EntryTableRow.from_dict(rows_item_data)

            rows.append(rows_item)

        return EntryTable(
            name=name,
            column_labels=column_labels,
            rows=rows,
        )
