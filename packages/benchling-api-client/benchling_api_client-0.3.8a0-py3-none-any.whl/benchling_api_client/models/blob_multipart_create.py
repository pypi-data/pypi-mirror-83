from typing import Any, Dict, Optional

import attr

from ..models.type12345 import Type12345


@attr.s(auto_attribs=True)
class BlobMultipartCreate:
    """  """

    name: str
    type: Type12345
    mime_type: Optional[str] = "application/octet-stream"

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        type = self.type.value

        mime_type = self.mime_type

        return {
            "name": name,
            "type": type,
            "mimeType": mime_type,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BlobMultipartCreate":
        name = d["name"]

        type = Type12345(d["type"])

        mime_type = d.get("mimeType")

        return BlobMultipartCreate(
            name=name,
            type=type,
            mime_type=mime_type,
        )
