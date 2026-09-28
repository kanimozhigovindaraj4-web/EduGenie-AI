import os

from dotenv import load_dotenv


# Load .env file
load_dotenv()


# Gemini API Key
GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
).strip()


# Gemini model
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
).strip()


# Fallback model used when the primary model is overloaded
GEMINI_FALLBACK_MODEL = os.getenv(
    "GEMINI_FALLBACK_MODEL",
    "gemini-3.5-flash-lite"
).strip()


# Local explanation model
ENABLE_LOCAL_EXPLANATION = (
    os.getenv(
        "ENABLE_LOCAL_EXPLANATION",
        "false"
    ).lower() == "true"
)


LOCAL_MODEL_NAME = os.getenv(
    "LOCAL_MODEL_NAME",
    "MBZUAI/LaMini-Flan-T5-783M"
).strip()


# Maximum input characters sent to Gemini
MAX_INPUT_CHARS = int(
    os.getenv(
        "MAX_INPUT_CHARS",
        "20000"
    )
)


# Maximum Gemini output tokens
MAX_OUTPUT_TOKENS = int(
    os.getenv(
        "MAX_OUTPUT_TOKENS",
        "2048"
    )
)