import datetime
from typing import Any, Dict, List, Optional, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.request_status import RequestStatus


@attr.s(auto_attribs=True)
class Request:
    """  """

    id: str
    created_at: datetime.datetime
    fields: Dict[Any, Any]
    display_id: str
    assignees: List[Union[Dict[Any, Any], Dict[Any, Any]]]
    request_status: RequestStatus
    web_url: str
    scheduled_on: Optional[datetime.date] = None
    project_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        created_at = self.created_at.isoformat()

        fields = self.fields

        display_id = self.display_id
        assignees = []
        for assignees_item_data in self.assignees:
            if isinstance(assignees_item_data, Dict[Any, Any]):
                assignees_item = assignees_item_data

            else:
                assignees_item = assignees_item_data

            assignees.append(assignees_item)

        request_status = self.request_status.value

        web_url = self.web_url
        scheduled_on = self.scheduled_on.isoformat() if self.scheduled_on else None

        project_id = self.project_id

        return {
            "id": id,
            "createdAt": created_at,
            "fields": fields,
            "displayId": display_id,
            "assignees": assignees,
            "requestStatus": request_status,
            "webURL": web_url,
            "scheduledOn": scheduled_on,
            "projectId": project_id,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Request":
        id = d["id"]

        created_at = isoparse(d["createdAt"])

        fields = d["fields"]

        display_id = d["displayId"]

        assignees = []
        for assignees_item_data in d["assignees"]:

            def _parse_assignees_item(data: Dict[str, Any]) -> Union[Dict[Any, Any], Dict[Any, Any]]:
                assignees_item: Union[Dict[Any, Any], Dict[Any, Any]]
                try:
                    assignees_item = assignees_item_data

                    return assignees_item
                except:  # noqa: E722
                    pass
                assignees_item = assignees_item_data

                return assignees_item

            assignees_item = _parse_assignees_item(assignees_item_data)

            assignees.append(assignees_item)

        request_status = RequestStatus(d["requestStatus"])

        web_url = d["webURL"]

        scheduled_on = None
        if d.get("scheduledOn") is not None:
            scheduled_on = isoparse(cast(str, d.get("scheduledOn"))).date()

        project_id = d.get("projectId")

        return Request(
            id=id,
            created_at=created_at,
            fields=fields,
            display_id=display_id,
            assignees=assignees,
            request_status=request_status,
            web_url=web_url,
            scheduled_on=scheduled_on,
            project_id=project_id,
        )
