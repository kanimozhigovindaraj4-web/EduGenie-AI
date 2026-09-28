from gemini_client import generate_text


def answer_question(
    question: str,
    level: str = "beginner"
) -> str:

    prompt = f"""
Answer this learner's question:

Question:
{question}

Learner level:
{level}

Requirements:

- Give the direct answer first.
- Explain the reasoning or background clearly.
- Use examples when useful.
- Do not fabricate sources, quotations, statistics, or citations.
- If the question is ambiguous, state the assumption you used.
"""

    return generate_text(
        prompt,
        system_instruction=(
            "You are EduGenie's Q&A tutor. "
            "Prioritize factual accuracy and explain "
            "concepts rather than merely giving an answer."
        ),
        temperature=0.3,
    )