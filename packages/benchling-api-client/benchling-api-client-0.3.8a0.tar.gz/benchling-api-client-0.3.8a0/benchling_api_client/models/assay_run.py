from typing import Any, Dict, Optional, cast

import attr

from ..models.schema_summary import SchemaSummary
from ..models.user_summary import UserSummary


@attr.s(auto_attribs=True)
class AssayRun:
    """  """

    id: Optional[str] = None
    project_id: Optional[str] = None
    created_at: Optional[str] = None
    creator: Optional[UserSummary] = None
    schema: Optional[SchemaSummary] = None
    fields: Optional[Dict[Any, Any]] = None
    entry_id: Optional[str] = None
    is_reviewed: Optional[bool] = None
    validation_schema: Optional[str] = None
    validation_comment: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        project_id = self.project_id
        created_at = self.created_at
        creator = self.creator.to_dict() if self.creator else None

        schema = self.schema.to_dict() if self.schema else None

        fields = self.fields if self.fields else None

        entry_id = self.entry_id
        is_reviewed = self.is_reviewed
        validation_schema = self.validation_schema
        validation_comment = self.validation_comment

        return {
            "id": id,
            "projectId": project_id,
            "createdAt": created_at,
            "creator": creator,
            "schema": schema,
            "fields": fields,
            "entryId": entry_id,
            "isReviewed": is_reviewed,
            "validationSchema": validation_schema,
            "validationComment": validation_comment,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AssayRun":
        id = d.get("id")

        project_id = d.get("projectId")

        created_at = d.get("createdAt")

        creator = None
        if d.get("creator") is not None:
            creator = UserSummary.from_dict(cast(Dict[str, Any], d.get("creator")))

        schema = None
        if d.get("schema") is not None:
            schema = SchemaSummary.from_dict(cast(Dict[str, Any], d.get("schema")))

        fields = None
        if d.get("fields") is not None:
            fields = d.get("fields")

        entry_id = d.get("entryId")

        is_reviewed = d.get("isReviewed")

        validation_schema = d.get("validationSchema")

        validation_comment = d.get("validationComment")

        return AssayRun(
            id=id,
            project_id=project_id,
            created_at=created_at,
            creator=creator,
            schema=schema,
            fields=fields,
            entry_id=entry_id,
            is_reviewed=is_reviewed,
            validation_schema=validation_schema,
            validation_comment=validation_comment,
        )
