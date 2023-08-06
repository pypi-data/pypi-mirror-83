from typing import Any, Dict, Optional

import attr


@attr.s(auto_attribs=True)
class BadRequestErrorBulk:
    """  """

    error: Optional[Dict[Any, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        error = self.error if self.error else None

        return {
            "error": error,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BadRequestErrorBulk":
        error = None
        if d.get("error") is not None:
            error = d.get("error")

        return BadRequestErrorBulk(
            error=error,
        )
