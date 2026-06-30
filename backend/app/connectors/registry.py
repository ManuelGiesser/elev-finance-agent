from app.connectors.base import ConnectorHealth


class ConnectorRegistry:
    def __init__(self):
        self._connectors = []

    def register(self, connector):
        self._connectors.append(connector)

    def health(self) -> list[ConnectorHealth]:
        return [connector.health() for connector in self._connectors]


registry = ConnectorRegistry()