from abc import ABC, abstractmethod
from typing import BinaryIO

class ITranscriptionService(ABC):
    @abstractmethod
    async def transcribe(self, audio_file: BinaryIO) -> str:
        """Transcribes audio file to text."""
        pass
