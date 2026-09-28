from functools import lru_cache

from config import (
    ENABLE_LOCAL_EXPLANATION,
    LOCAL_MODEL_NAME
)

from gemini_client import generate_text


# ==========================================
# Optional Local AI Model
# ==========================================

@lru_cache(maxsize=1)
def get_local_pipeline():

    from transformers import pipeline

    return pipeline(
        "text2text-generation",
        model=LOCAL_MODEL_NAME,
        tokenizer=LOCAL_MODEL_NAME
    )


def local_explanation(
    topic: str,
    level: str = "beginner",
) -> str:

    model = get_local_pipeline()

    prompt = f"""
Explain the following topic to a {level} student.

Topic:
{topic}

Give the explanation in this format:

1. Simple Definition
2. Key Points
3. Easy Example
4. Short Recap

Use simple English.
"""

    result = model(
        prompt,
        max_new_tokens=256,
        do_sample=False
    )

    return result[0]["generated_text"].strip()


# ==========================================
# Main Explanation Function
# ==========================================

def explain_topic(
    topic: str,
    level: str = "beginner",
) -> str:

    # Use local model only when enabled
    if ENABLE_LOCAL_EXPLANATION:

        try:

            return local_explanation(
                topic,
                level,
            )

        except Exception as error:

            return (
                "Local explanation model failed.\n\n"
                f"Error: {error}"
            )


    # Otherwise use Gemini
    prompt = f"""
Explain the following topic to a {level} student.

Topic:

{topic}

Use this format:

1. Simple Definition
2. Key Points
3. Easy Example
4. One-Line Recap

Use simple and clear English.
Avoid unnecessary technical language.
"""

    try:

        return generate_text(

            prompt,

            """
You are EduGenie, an educational AI assistant.

Explain difficult concepts in simple,
clear language suitable for college students.

Give accurate and useful explanations.
"""
        )

    except Exception as error:

        return (
            "Unable to generate explanation.\n\n"
            f"Error: {error}"
        )