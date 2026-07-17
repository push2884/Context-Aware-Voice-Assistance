from typing import BinaryIO
from src.application.interfaces import ITranscriptionService
from src.domain.privacy_models import PrivacyEvaluator, PrivacyAssessment

class PrivacyService:
    def __init__(self, transcription_service: ITranscriptionService):
        self.transcription_service = transcription_service

    async def analyze_audio_privacy(self, audio_data: BinaryIO) -> PrivacyAssessment:
        # 1. Transcribe audio
        transcript = await self.transcription_service.transcribe(audio_data)
        
        # 2. Evaluate privacy risks
        assessment = PrivacyEvaluator.evaluate(transcript)
        
        return assessment
