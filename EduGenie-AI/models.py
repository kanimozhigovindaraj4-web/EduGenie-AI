from typing import List

from pydantic import (
    BaseModel,
    Field,
    field_validator,
)


# ---------------------------------------------------------
# Base request
# ---------------------------------------------------------

class BaseTextRequest(BaseModel):

    level: str = Field(
        default="beginner",
        max_length=30,
    )

    @field_validator("level")
    @classmethod
    def validate_level(
        cls,
        value: str
    ) -> str:

        value = value.strip().lower()

        allowed_levels = {
            "beginner",
            "intermediate",
            "advanced",
        }

        if value not in allowed_levels:
            return "beginner"

        return value


# ---------------------------------------------------------
# Q&A
# ---------------------------------------------------------

class QARequest(BaseTextRequest):

    question: str = Field(
        ...,
        min_length=2,
        max_length=10000,
    )


# ---------------------------------------------------------
# Explanation
# ---------------------------------------------------------

class ExplainRequest(BaseTextRequest):

    topic: str = Field(
        ...,
        min_length=2,
        max_length=5000,
    )

    style: str = Field(
        default="simple",
        max_length=30,
    )


# ---------------------------------------------------------
# Quiz
# ---------------------------------------------------------

class QuizRequest(BaseTextRequest):

    text: str = Field(
        ...,
        min_length=20,
        max_length=20000,
    )


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

class SummaryRequest(BaseTextRequest):

    text: str = Field(
        ...,
        min_length=20,
        max_length=20000,
    )

    length: str = Field(
        default="medium",
        max_length=20,
    )


# ---------------------------------------------------------
# Learning path
# ---------------------------------------------------------

class LearningPathRequest(BaseTextRequest):

    topic: str = Field(
        ...,
        min_length=2,
        max_length=300,
    )

    hours_per_week: int = Field(
        default=5,
        ge=1,
        le=60,
    )


# ---------------------------------------------------------
# Text response
# ---------------------------------------------------------

class TextResponse(BaseModel):

    result: str


# ---------------------------------------------------------
# Quiz question
# ---------------------------------------------------------

class QuizQuestion(BaseModel):

    question: str

    options: List[str] = Field(
        min_length=4,
        max_length=4,
    )

    correct_answer: str

    explanation: str = ""


# ---------------------------------------------------------
# Quiz response
# ---------------------------------------------------------

class QuizResponse(BaseModel):

    questions: List[QuizQuestion] = Field(
        min_length=1,
        max_length=10,
    )


# ---------------------------------------------------------
# Health response
# ---------------------------------------------------------

class HealthResponse(BaseModel):

    status: str

    gemini_configured: bool