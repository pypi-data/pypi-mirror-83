from typing import Any, Dict, List, Optional

import attr


@attr.s(auto_attribs=True)
class RequestsTasksBulkCreateRequest:
    """  """

    tasks: Optional[List[Dict[Any, Any]]] = None

    def to_dict(self) -> Dict[str, Any]:
        if self.tasks is None:
            tasks = None
        else:
            tasks = []
            for tasks_item_data in self.tasks:
                tasks_item = tasks_item_data

                tasks.append(tasks_item)

        return {
            "tasks": tasks,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "RequestsTasksBulkCreateRequest":
        tasks = []
        for tasks_item_data in d.get("tasks") or []:
            tasks_item = tasks_item_data

            tasks.append(tasks_item)

        return RequestsTasksBulkCreateRequest(
            tasks=tasks,
        )
