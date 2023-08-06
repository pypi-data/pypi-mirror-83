from typing import Any, Dict, Optional

import attr


@attr.s(auto_attribs=True)
class EntryExternalFile:
    """The ExternalFile resource stores metadata about the file. The actual original file can be downloaded by using the 'downloadURL' property."""

    id: Optional[str] = None
    download_url: Optional[str] = None
    expires_at: Optional[int] = None
    size: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        download_url = self.download_url
        expires_at = self.expires_at
        size = self.size

        return {
            "id": id,
            "downloadURL": download_url,
            "expiresAt": expires_at,
            "size": size,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EntryExternalFile":
        id = d.get("id")

        download_url = d.get("downloadURL")

        expires_at = d.get("expiresAt")

        size = d.get("size")

        return EntryExternalFile(
            id=id,
            download_url=download_url,
            expires_at=expires_at,
            size=size,
        )
