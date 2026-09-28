from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from google.genai.errors import ClientError, ServerError
from pydantic import AliasChoices, BaseModel, Field

from config import GEMINI_API_KEY, GEMINI_MODEL

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0"
)


@app.exception_handler(ServerError)
async def gemini_server_error_handler(
    request: Request,
    error: ServerError,
):

    status_code = error.code if 500 <= error.code < 600 else 502
    detail = (
        "Gemini is temporarily overloaded. Please retry shortly."
        if error.code == 503
        else "Gemini could not complete the request. Please retry shortly."
    )
    headers = {"Retry-After": "30"} if error.code == 503 else {}

    return JSONResponse(
        status_code=status_code,
        content={"detail": detail},
        headers=headers,
    )


@app.exception_handler(ClientError)
async def gemini_client_error_handler(
    request: Request,
    error: ClientError,
):

    if error.code == 429:
        return JSONResponse(
            status_code=429,
            content={
                "detail": (
                    "Gemini API quota exceeded. Wait for the quota to reset "
                    "or use an API key/project with available quota."
                )
            },
            headers={"Retry-After": "60"},
        )

    if error.code == 404:
        return JSONResponse(
            status_code=502,
            content={
                "detail": (
                    "The configured Gemini model is unavailable for this API key "
                    "or project. Check GEMINI_MODEL in the .env file."
                )
            },
        )

    return JSONResponse(
        status_code=error.code if 400 <= error.code < 500 else 502,
        content={
            "detail": "Gemini rejected the request. Check the API key and request settings."
        },
    )


# ---------------------------------------
# Static files
# ---------------------------------------

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# ---------------------------------------
# Templates
# ---------------------------------------

templates = Jinja2Templates(
    directory="templates"
)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():

    return FileResponse("static/favicon.svg", media_type="image/svg+xml")


# ---------------------------------------
# Request Models
# ---------------------------------------

class TextRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=1,
        max_length=20000
    )


class LearnerTextRequest(TextRequest):

    level: str = "beginner"


class QuestionRequest(LearnerTextRequest):

    text: str = Field(
        ...,
        min_length=1,
        max_length=20000,
        validation_alias=AliasChoices("text", "question"),
    )


class QuizRequest(LearnerTextRequest):

    text: str = Field(
        ...,
        min_length=1,
        max_length=10000
    )

    count: int = Field(
        default=3,
        ge=1,
        le=10
    )


class SummaryRequest(LearnerTextRequest):

    length: str = "medium"


class LearningRequest(LearnerTextRequest):

    text: str = Field(
        ...,
        min_length=1,
        max_length=20000,
        validation_alias=AliasChoices("text", "topic"),
    )

    hours_per_week: int = Field(
        default=5,
        ge=1,
        le=60,
        validation_alias=AliasChoices(
            "hours_per_week",
            "hours",
        ),
    )


# ---------------------------------------
# Home
# ---------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


# ---------------------------------------
# Health
# ---------------------------------------

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": "EduGenie",
        "gemini_configured": bool(
            GEMINI_API_KEY
        ),
        "gemini_model": GEMINI_MODEL
    }


# ---------------------------------------
# Question Answering
# ---------------------------------------

@app.post("/qa")
async def qa(
    payload: QuestionRequest
):

    answer = answer_question(
        payload.text,
        payload.level,
    )

    return {
        "answer": answer
    }


# ---------------------------------------
# Explanation
# ---------------------------------------

@app.post("/explain")
async def explain(
    payload: LearnerTextRequest
):

    explanation = explain_topic(
        payload.text,
        payload.level,
    )

    return {
        "explanation": explanation
    }


# ---------------------------------------
# Quiz
# ---------------------------------------

@app.post("/quiz")
async def quiz(
    payload: QuizRequest
):

    quiz_data = generate_quiz(
        payload.text,
        payload.level,
        payload.count,
    )

    return {
        "quiz": quiz_data
    }


# ---------------------------------------
# Summary
# ---------------------------------------

@app.post("/summarize")
async def summarize(
    payload: SummaryRequest
):

    summary = summarize_text(
        payload.text,
        payload.length,
        payload.level,
    )

    return {
        "summary": summary
    }


# ---------------------------------------
# Learning Recommendations
# ---------------------------------------

@app.post("/learn/recommendations")
async def recommendations(
    payload: LearningRequest
):

    recommendations_data = (
        get_learning_recommendations(
            payload.text,
            payload.level,
            payload.hours_per_week,
        )
    )

    return {
        "recommendations":
            recommendations_data
    }