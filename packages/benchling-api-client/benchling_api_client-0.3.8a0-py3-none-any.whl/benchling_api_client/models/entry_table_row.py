from typing import Any, Dict, List, Optional

import attr

from ..models.entry_table_cell import EntryTableCell


@attr.s(auto_attribs=True)
class EntryTableRow:
    """ Each has property 'cells' that is an array of cell objects """

    cells: Optional[List[EntryTableCell]] = None

    def to_dict(self) -> Dict[str, Any]:
        if self.cells is None:
            cells = None
        else:
            cells = []
            for cells_item_data in self.cells:
                cells_item = cells_item_data.to_dict()

                cells.append(cells_item)

        return {
            "cells": cells,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EntryTableRow":
        cells = []
        for cells_item_data in d.get("cells") or []:
            cells_item = EntryTableCell.from_dict(cells_item_data)

            cells.append(cells_item)

        return EntryTableRow(
            cells=cells,
        )
