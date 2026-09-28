from typing import List

from pydantic import (
    BaseModel,
    Field,
)

import config
from gemini_client import generate_json


# ---------------------------------------------------------
# Generated question schema
# ---------------------------------------------------------

class GeneratedQuizQuestion(BaseModel):

    question: str

    options: List[str] = Field(
        min_length=4,
        max_length=4,
    )

    correct_answer: str

    explanation: str


# ---------------------------------------------------------
# Compatibility helper
# ---------------------------------------------------------

def clean_json_block(
    value: str
) -> str:

    value = value.strip()

    if value.startswith("```"):

        lines = value.splitlines()

        if (
            lines
            and lines[0].startswith("```")
        ):
            lines = lines[1:]

        if (
            lines
            and lines[-1].strip() == "```"
        ):
            lines = lines[:-1]

        value = "\n".join(lines).strip()

    return value


# ---------------------------------------------------------
# Generate quiz
# ---------------------------------------------------------

def generate_quiz(
    text: str,
    level: str = "beginner",
    count: int = 3,
) -> dict:

    text = text[
        :config.MAX_INPUT_CHARS
    ]

    prompt = f"""
Create exactly {count} multiple-choice questions
from the supplied passage.

Learner level:
{level}

Rules:

- Every question must be answerable from the passage.
- Each question has exactly 4 options.
- correct_answer must exactly match one option.
- Include a short explanation of the correct answer.
- Avoid trick questions.
- Do not use unnecessary outside facts.

PASSAGE:

{text}
"""

    schema = list[
        GeneratedQuizQuestion
    ]

    result = generate_json(
        prompt,
        schema,
        system_instruction=(
            "You generate reliable educational MCQs. "
            "Return only the requested structured quiz."
        ),
    )

    if isinstance(result, str):

        import json

        result = json.loads(
            clean_json_block(result)
        )

    questions = [

        GeneratedQuizQuestion
        .model_validate(item)
        .model_dump()

        for item in result

    ]

    if len(questions) != count:

        raise RuntimeError(
            f"The model did not return exactly {count} quiz questions."
        )

    return {
        "questions": questions
    }