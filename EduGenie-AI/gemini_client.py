from functools import lru_cache
from typing import Any

from google import genai
from google.genai.errors import ClientError, ServerError
from google.genai import types

from config import (
    GEMINI_FALLBACK_MODEL,
    GEMINI_API_KEY,
    GEMINI_MODEL,
    MAX_OUTPUT_TOKENS
)


@lru_cache(maxsize=1)
def get_client():

    if not GEMINI_API_KEY:

        raise RuntimeError(
            "GEMINI_API_KEY is missing."
            " Please add your Gemini API key"
            " to the .env file."
        )

    return genai.Client(
        api_key=GEMINI_API_KEY
    )


def _generate_content(
    prompt: str,
    generation_config: types.GenerateContentConfig,
):

    client = get_client()

    try:
        return client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=generation_config,
        )
    except (ClientError, ServerError) as error:
        should_try_fallback = (
            isinstance(error, ServerError)
            and 500 <= error.code < 600
        ) or (
            isinstance(error, ClientError)
            and error.code in (404, 429)
        )

        if (
            not should_try_fallback
            or not GEMINI_FALLBACK_MODEL
            or GEMINI_FALLBACK_MODEL == GEMINI_MODEL
        ):
            raise

        return client.models.generate_content(
            model=GEMINI_FALLBACK_MODEL,
            contents=prompt,
            config=generation_config,
        )


def generate_text(
    prompt: str,
    system_instruction: str | None = None,
    temperature: float = 0.3,
    max_output_tokens: int = MAX_OUTPUT_TOKENS,
) -> str:

    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        system_instruction=system_instruction,
    )


    response = _generate_content(prompt, config)


    text = getattr(
        response,
        "text",
        None
    )


    if not text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )


    return text.strip()


def generate_json(
    prompt: str,
    response_schema: object,
    system_instruction: str | None = None,
    temperature: float = 0.3,
    max_output_tokens: int = MAX_OUTPUT_TOKENS,
) -> Any:

    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        system_instruction=system_instruction,
        response_mime_type="application/json",
        response_schema=response_schema,
    )

    response = _generate_content(prompt, config)

    parsed = getattr(response, "parsed", None)

    if parsed is not None:
        return parsed

    text = getattr(response, "text", None)

    if not text:
        raise RuntimeError(
            "Gemini returned an empty JSON response."
        )

    return text.strip()