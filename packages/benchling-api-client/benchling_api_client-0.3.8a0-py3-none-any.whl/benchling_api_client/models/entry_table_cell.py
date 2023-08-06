from typing import Any, Dict, Optional, cast

import attr

from ..models.entry_link import EntryLink


@attr.s(auto_attribs=True)
class EntryTableCell:
    """  """

    text: Optional[str] = None
    link: Optional[EntryLink] = None

    def to_dict(self) -> Dict[str, Any]:
        text = self.text
        link = self.link.to_dict() if self.link else None

        return {
            "text": text,
            "link": link,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EntryTableCell":
        text = d.get("text")

        link = None
        if d.get("link") is not None:
            link = EntryLink.from_dict(cast(Dict[str, Any], d.get("link")))

        return EntryTableCell(
            text=text,
            link=link,
        )
