import uvicorn
from fastapi import FastAPI, UploadFile, File, Depends
from src.domain.privacy_models import PrivacyAssessment
from src.application.privacy_service import PrivacyService
from src.infrastructure.azure_whisper_stt import AzureWhisperService
from src.infrastructure.security import validate_api_token

app = FastAPI(title="WhisperShield AI - Backend")

# Dependency Injection
def get_privacy_service() -> PrivacyService:
    transcription_service = AzureWhisperService()
    return PrivacyService(transcription_service)

@app.post("/analyze-privacy", response_model=PrivacyAssessment)
async def analyze_privacy(
    file: UploadFile = File(...),
    token: str = Depends(validate_api_token),
    service: PrivacyService = Depends(get_privacy_service)
):
    """
    Upload an audio file to transcribe it and analyze privacy risks.
    """
    # Read file content into memory
    content = await file.read()
    from io import BytesIO
    audio_buffer = BytesIO(content)
    audio_buffer.name = file.filename # Required by some SDKs
    
    assessment = await service.analyze_audio_privacy(audio_buffer)
    return assessment

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
