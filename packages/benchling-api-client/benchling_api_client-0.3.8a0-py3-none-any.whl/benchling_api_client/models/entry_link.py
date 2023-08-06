from typing import Any, Dict, Optional

import attr

from ..models.type1234 import Type1234


@attr.s(auto_attribs=True)
class EntryLink:
    """Links are contained within notes to reference resources that live outside of the entry. A link can target an external resource via an http(s):// hyperlink or a Benchling resource via @-mentions and drag-n-drop."""

    id: Optional[str] = None
    type: Optional[Type1234] = None
    web_url: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        type = self.type.value if self.type else None

        web_url = self.web_url

        return {
            "id": id,
            "type": type,
            "webURL": web_url,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EntryLink":
        id = d.get("id")

        type = None
        if d.get("type") is not None:
            type = Type1234(d.get("type"))

        web_url = d.get("webURL")

        return EntryLink(
            id=id,
            type=type,
            web_url=web_url,
        )
