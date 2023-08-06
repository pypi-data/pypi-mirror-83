from typing import Any, Dict, List

import attr


@attr.s(auto_attribs=True)
class ProjectUnarchiveRequest:
    """  """

    project_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        project_ids = self.project_ids

        return {
            "projectIds": project_ids,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ProjectUnarchiveRequest":
        project_ids = d["projectIds"]

        return ProjectUnarchiveRequest(
            project_ids=project_ids,
        )
