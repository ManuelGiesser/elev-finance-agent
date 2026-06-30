from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class ConnectorHealth:
    name: str
    enabled: bool
    status: str
    details: dict[str, Any] | None = None


class BaseConnector(ABC):
    name: str = "base"

    def __init__(self, enabled: bool = False):
        self.enabled = enabled

    @abstractmethod
    def health(self) -> ConnectorHealth:
        pass