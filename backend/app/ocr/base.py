from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class OCRResult:
    text: str
    engine: str
    confidence: float | None = None


class BaseOCREngine(ABC):
    name: str = "base"

    @abstractmethod
    def extract_text(self, file_path: str) -> OCRResult:
        pass