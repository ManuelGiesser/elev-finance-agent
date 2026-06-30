from app.connectors.base import BaseConnector, ConnectorHealth


class GoogleDriveConnector(BaseConnector):
    name = "google_drive"

    def __init__(
        self,
        enabled: bool,
        ff_folder_id: str = "",
        belege_folder_id: str = "",
    ):
        super().__init__(enabled=enabled)
        self.ff_folder_id = ff_folder_id
        self.belege_folder_id = belege_folder_id

    def health(self) -> ConnectorHealth:
        configured = bool(self.ff_folder_id and self.belege_folder_id)

        if not self.enabled:
            status = "disabled"
        elif configured:
            status = "configured"
        else:
            status = "missing_configuration"

        return ConnectorHealth(
            name=self.name,
            enabled=self.enabled,
            status=status,
            details={
                "ff_folder_configured": bool(self.ff_folder_id),
                "belege_folder_configured": bool(self.belege_folder_id),
            },
        )