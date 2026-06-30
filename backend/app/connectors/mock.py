from app.connectors.base import BaseConnector, ConnectorHealth


class MockConnector(BaseConnector):
    name = "mock"

    def health(self) -> ConnectorHealth:
        return ConnectorHealth(
            name=self.name,
            enabled=self.enabled,
            status="ok" if self.enabled else "disabled",
            details={"message": "Connector framework ready"},
        )