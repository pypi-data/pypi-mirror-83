from typing import Any, Dict, Optional

import attr


@attr.s(auto_attribs=True)
class EntryPatch:
    """  """

    author_ids: Optional[str] = None
    name: Optional[str] = None
    folder_id: Optional[str] = None
    fields: Optional[Dict[Any, Any]] = None
    schema_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        author_ids = self.author_ids
        name = self.name
        folder_id = self.folder_id
        fields = self.fields if self.fields else None

        schema_id = self.schema_id

        return {
            "authorIds": author_ids,
            "name": name,
            "folderId": folder_id,
            "fields": fields,
            "schemaId": schema_id,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EntryPatch":
        author_ids = d.get("authorIds")

        name = d.get("name")

        folder_id = d.get("folderId")

        fields = None
        if d.get("fields") is not None:
            fields = d.get("fields")

        schema_id = d.get("schemaId")

        return EntryPatch(
            author_ids=author_ids,
            name=name,
            folder_id=folder_id,
            fields=fields,
            schema_id=schema_id,
        )
