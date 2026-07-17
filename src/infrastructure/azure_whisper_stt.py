import os
import asyncio
from typing import BinaryIO
from openai import AsyncAzureOpenAI
from src.application.interfaces import ITranscriptionService

class AzureWhisperService(ITranscriptionService):
    def __init__(self):
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.deployment_id = os.getenv("AZURE_OPENAI_WHISPER_DEPLOYMENT_ID", "whisper")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2023-09-01-preview")

        if self.api_key and self.endpoint:
            self.client = AsyncAzureOpenAI(
                api_key=self.api_key,
                azure_endpoint=self.endpoint,
                api_version=self.api_version
            )
        else:
            self.client = None
            print("Azure credentials missing. Using mock transcription service.")

    async def transcribe(self, audio_file: BinaryIO) -> str:
        if not self.client:
            # Mock behavior for demo if credentials aren't set
            await asyncio.sleep(1)  # Simulate latency
            return "This is a mock transcript. My password is secret and my SSN is 123. Please protect my health data."

        try:
            # Azure Whisper transcription
            response = await self.client.audio.transcriptions.create(
                model=self.deployment_id,
                file=audio_file
            )
            return response.text
        except Exception as e:
            print(f"Transcription error: {e}")
            return f"Error during transcription: {str(e)}. Fallback: Please keep my password secret."
