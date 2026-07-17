from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class PrivacyEntity(BaseModel):
    text: str
    entity_type: str
    risk_score: float

class PrivacyAssessment(BaseModel):
    transcript: str
    risk_level: RiskLevel
    score: float
    detected_entities: List[PrivacyEntity] = []
    recommendation: str

class PrivacyEvaluator:
    """Core domain logic for privacy risk calculation."""
    
    SENSITIVE_KEYWORDS = {
        "password": 0.9,
        "ssn": 1.0,
        "credit card": 1.0,
        "address": 0.5,
        "phone number": 0.4,
        "email": 0.4,
        "secret": 0.7,
        "health": 0.6
    }

    @staticmethod
    def evaluate(text: str) -> PrivacyAssessment:
        detected = []
        total_score = 0.0
        text_lower = text.lower()

        for keyword, weight in PrivacyEvaluator.SENSITIVE_KEYWORDS.items():
            if keyword in text_lower:
                detected.append(PrivacyEntity(
                    text=keyword,
                    entity_type="PII",
                    risk_score=weight
                ))
                total_score += weight

        # Normalize score and determine level
        normalized_score = min(total_score, 1.0)
        
        if normalized_score >= 0.8:
            level = RiskLevel.CRITICAL
            rec = "DO NOT UPLOAD. Contains highly sensitive information."
        elif normalized_score >= 0.5:
            level = RiskLevel.HIGH
            rec = "Caution: Contains personal data. Redaction recommended."
        elif normalized_score >= 0.2:
            level = RiskLevel.MEDIUM
            rec = "Minor privacy risks detected."
        else:
            level = RiskLevel.LOW
            rec = "Safe to process."

        return PrivacyAssessment(
            transcript=text,
            risk_level=level,
            score=normalized_score,
            detected_entities=detected,
            recommendation=rec
        )
