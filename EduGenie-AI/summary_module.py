import config
from gemini_client import generate_text


def summarize_text(
    text: str,
    length: str = "medium",
    level: str = "beginner"
) -> str:

    text = text[:config.MAX_INPUT_CHARS]

    length_instruction = {

        "short":
            "5 bullet points or fewer",

        "medium":
            "a compact paragraph followed by 5 key points",

        "long":
            "a detailed but concise study summary with headings",

    }.get(
        length.lower(),
        "a compact paragraph followed by 5 key points"
    )

    prompt = f"""
Summarize the educational passage below.

Learner level:
{level}

Requested length:
{length_instruction}

Preserve:

- important facts
- definitions
- relationships
- conclusions

Remove:

- repetition
- minor details

Do not introduce information that is not present
in the passage.

PASSAGE:

{text}
"""

    return generate_text(
        prompt,
        system_instruction=(
            "You are EduGenie's study-summary assistant. "
            "Your job is faithful compression of supplied "
            "educational text."
        ),
        temperature=0.2,
        max_output_tokens=1400,
    )