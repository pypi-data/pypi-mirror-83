import datetime
from typing import Any, Dict, List, Optional, cast

import attr
from dateutil.parser import isoparse

from ..models.archive_record import ArchiveRecord
from ..models.entry_day import EntryDay
from ..models.entry_schema import EntrySchema
from ..models.fields import Fields
from ..models.user_summary import UserSummary


@attr.s(auto_attribs=True)
class Entry:
    """  """

    id: Optional[str] = None
    archive_record: Optional[ArchiveRecord] = None
    authors: Optional[List[UserSummary]] = None
    created_at: Optional[datetime.datetime] = None
    creator: Optional[UserSummary] = None
    custom_fields: Optional[Dict[Any, Any]] = None
    days: Optional[List[EntryDay]] = None
    display_id: Optional[str] = None
    fields: Optional[Fields] = None
    folder_id: Optional[str] = None
    name: Optional[str] = None
    modified_at: Optional[str] = None
    review_record: Optional[Dict[Any, Any]] = None
    schema: Optional[EntrySchema] = None
    web_url: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        archive_record = self.archive_record.to_dict() if self.archive_record else None

        if self.authors is None:
            authors = None
        else:
            authors = []
            for authors_item_data in self.authors:
                authors_item = authors_item_data.to_dict()

                authors.append(authors_item)

        created_at = self.created_at.isoformat() if self.created_at else None

        creator = self.creator.to_dict() if self.creator else None

        custom_fields = self.custom_fields if self.custom_fields else None

        if self.days is None:
            days = None
        else:
            days = []
            for days_item_data in self.days:
                days_item = days_item_data.to_dict()

                days.append(days_item)

        display_id = self.display_id
        fields = self.fields.to_dict() if self.fields else None

        folder_id = self.folder_id
        name = self.name
        modified_at = self.modified_at
        review_record = self.review_record if self.review_record else None

        schema = self.schema.to_dict() if self.schema else None

        web_url = self.web_url

        return {
            "id": id,
            "archiveRecord": archive_record,
            "authors": authors,
            "createdAt": created_at,
            "creator": creator,
            "customFields": custom_fields,
            "days": days,
            "displayId": display_id,
            "fields": fields,
            "folderId": folder_id,
            "name": name,
            "modifiedAt": modified_at,
            "reviewRecord": review_record,
            "schema": schema,
            "webURL": web_url,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Entry":
        id = d.get("id")

        archive_record = None
        if d.get("archiveRecord") is not None:
            archive_record = ArchiveRecord.from_dict(cast(Dict[str, Any], d.get("archiveRecord")))

        authors = []
        for authors_item_data in d.get("authors") or []:
            authors_item = UserSummary.from_dict(authors_item_data)

            authors.append(authors_item)

        created_at = None
        if d.get("createdAt") is not None:
            created_at = isoparse(cast(str, d.get("createdAt")))

        creator = None
        if d.get("creator") is not None:
            creator = UserSummary.from_dict(cast(Dict[str, Any], d.get("creator")))

        custom_fields = None
        if d.get("customFields") is not None:
            custom_fields = d.get("customFields")

        days = []
        for days_item_data in d.get("days") or []:
            days_item = EntryDay.from_dict(days_item_data)

            days.append(days_item)

        display_id = d.get("displayId")

        fields = None
        if d.get("fields") is not None:
            fields = Fields.from_dict(cast(Dict[str, Any], d.get("fields")))

        folder_id = d.get("folderId")

        name = d.get("name")

        modified_at = d.get("modifiedAt")

        review_record = None
        if d.get("reviewRecord") is not None:
            review_record = d.get("reviewRecord")

        schema = None
        if d.get("schema") is not None:
            schema = EntrySchema.from_dict(cast(Dict[str, Any], d.get("schema")))

        web_url = d.get("webURL")

        return Entry(
            id=id,
            archive_record=archive_record,
            authors=authors,
            created_at=created_at,
            creator=creator,
            custom_fields=custom_fields,
            days=days,
            display_id=display_id,
            fields=fields,
            folder_id=folder_id,
            name=name,
            modified_at=modified_at,
            review_record=review_record,
            schema=schema,
            web_url=web_url,
        )
