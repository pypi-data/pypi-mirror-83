from typing import Any, Dict, List

import attr

from ..models.reason import Reason


@attr.s(auto_attribs=True)
class ProjectArchiveRequest:
    """  """

    reason: Reason
    project_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        reason = self.reason.value

        project_ids = self.project_ids

        return {
            "reason": reason,
            "projectIds": project_ids,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ProjectArchiveRequest":
        reason = Reason(d["reason"])

        project_ids = d["projectIds"]

        return ProjectArchiveRequest(
            reason=reason,
            project_ids=project_ids,
        )
