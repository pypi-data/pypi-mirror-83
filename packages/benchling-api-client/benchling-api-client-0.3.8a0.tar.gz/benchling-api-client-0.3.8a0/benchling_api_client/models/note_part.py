from typing import Any, Dict, List, Optional, cast

import attr

from ..models.entry_link import EntryLink
from ..models.entry_table import EntryTable
from ..models.type123 import Type123


@attr.s(auto_attribs=True)
class NotePart:
    """Notes are the main building blocks of entries. Each note corresponds roughly to a paragraph and has one of these types: - 'text': plain text - 'code': preformatted code block - 'table': a table with rows and columns of text - 'list_bullet': one "line" of a bulleted list - 'list_number': one "line" of a numbered list - 'list_checkbox': one "line" of a checklist - 'external_file': an attached user-uploaded file"""

    type: Optional[Type123] = None
    indentation: Optional[int] = 0
    text: Optional[str] = None
    links: Optional[List[EntryLink]] = None
    checked: Optional[bool] = None
    table: Optional[EntryTable] = None
    external_file_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value if self.type else None

        indentation = self.indentation
        text = self.text
        if self.links is None:
            links = None
        else:
            links = []
            for links_item_data in self.links:
                links_item = links_item_data.to_dict()

                links.append(links_item)

        checked = self.checked
        table = self.table.to_dict() if self.table else None

        external_file_id = self.external_file_id

        return {
            "type": type,
            "indentation": indentation,
            "text": text,
            "links": links,
            "checked": checked,
            "table": table,
            "externalFileId": external_file_id,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NotePart":
        type = None
        if d.get("type") is not None:
            type = Type123(d.get("type"))

        indentation = d.get("indentation")

        text = d.get("text")

        links = []
        for links_item_data in d.get("links") or []:
            links_item = EntryLink.from_dict(links_item_data)

            links.append(links_item)

        checked = d.get("checked")

        table = None
        if d.get("table") is not None:
            table = EntryTable.from_dict(cast(Dict[str, Any], d.get("table")))

        external_file_id = d.get("externalFileId")

        return NotePart(
            type=type,
            indentation=indentation,
            text=text,
            links=links,
            checked=checked,
            table=table,
            external_file_id=external_file_id,
        )
