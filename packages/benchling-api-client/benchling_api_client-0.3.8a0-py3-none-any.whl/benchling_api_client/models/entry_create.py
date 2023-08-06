from typing import Any, Dict, Optional

import attr


@attr.s(auto_attribs=True)
class EntryCreate:
    """  """

    name: str
    folder_id: str
    author_ids: Optional[str] = None
    entry_template_id: Optional[str] = None
    schema_id: Optional[str] = None
    custom_fields: Optional[Dict[Any, Any]] = None
    fields: Optional[Dict[Any, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        folder_id = self.folder_id
        author_ids = self.author_ids
        entry_template_id = self.entry_template_id
        schema_id = self.schema_id
        custom_fields = self.custom_fields if self.custom_fields else None

        fields = self.fields if self.fields else None

        return {
            "name": name,
            "folderId": folder_id,
            "authorIds": author_ids,
            "entryTemplateId": entry_template_id,
            "schemaId": schema_id,
            "customFields": custom_fields,
            "fields": fields,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EntryCreate":
        name = d["name"]

        folder_id = d["folderId"]

        author_ids = d.get("authorIds")

        entry_template_id = d.get("entryTemplateId")

        schema_id = d.get("schemaId")

        custom_fields = None
        if d.get("customFields") is not None:
            custom_fields = d.get("customFields")

        fields = None
        if d.get("fields") is not None:
            fields = d.get("fields")

        return EntryCreate(
            name=name,
            folder_id=folder_id,
            author_ids=author_ids,
            entry_template_id=entry_template_id,
            schema_id=schema_id,
            custom_fields=custom_fields,
            fields=fields,
        )
