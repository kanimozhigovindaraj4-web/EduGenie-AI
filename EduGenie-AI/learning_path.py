from gemini_client import generate_text


def get_learning_recommendations(
    topic: str,
    level: str = "beginner",
    hours_per_week: int = 5
) -> str:

    prompt = f"""
Design a practical learning path for:

Topic:
{topic}

Starting level:
{level}

Available study time:
{hours_per_week} hours/week

Structure it from beginner to advanced.

Include:

- Stage name and approximate duration
- Concepts to learn
- Practical exercises/projects
- How to check mastery
- Recommended resource TYPES
- Suggested weekly routine
- Prerequisites

Make it realistic for a self-learner.

Do not invent specific URLs.
"""

    return generate_text(
        prompt,
        system_instruction=(
            "You are EduGenie's learning-path planner. "
            "Create structured, realistic study plans "
            "with measurable practice."
        ),
        temperature=0.5,
        max_output_tokens=1800,
    )