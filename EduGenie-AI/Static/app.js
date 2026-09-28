const taskTabs = document.querySelectorAll(".task-tab");
const taskForm = document.getElementById("task-form");

const inputLabel = document.getElementById("input-label");
const userInput = document.getElementById("user-input");

const levelSelect = document.getElementById("level");
const summaryLength = document.getElementById("summary-length");
const hoursInput = document.getElementById("hours");

const lengthWrap = document.getElementById("length-wrap");
const hoursWrap = document.getElementById("hours-wrap");

const submitButton = document.getElementById("submit-button");

const resultSection = document.getElementById("result-section");
const resultTitle = document.getElementById("result-title");
const resultContainer = document.getElementById("result");

const copyButton = document.getElementById("copy-button");

const statusDot = document.getElementById("status-dot");
const statusText = document.getElementById("status-text");

let currentTask = "qa";


// ---------------------------------------------------------
// Task configuration
// ---------------------------------------------------------

const taskConfig = {
    qa: {
        label: "Ask your question",
        placeholder: "Example: Why does the sky look blue?",
        button: "Run EduGenie",
        title: "Q&A Result"
    },

    explain: {
        label: "Enter a topic to explain",
        placeholder: "Example: Explain Python loops simply.",
        button: "Explain",
        title: "Explanation"
    },

    quiz: {
        label: "Enter text for quiz generation",
        placeholder: "Paste at least 20 characters of study material.",
        button: "Generate Quiz",
        title: "Practice Quiz"
    },

    summarize: {
        label: "Enter text to summarize",
        placeholder: "Paste at least 20 characters of study material.",
        button: "Summarize",
        title: "Summary"
    },

    learn: {
        label: "Enter a learning topic",
        placeholder: "Example: Python programming",
        button: "Build Learning Path",
        title: "Learning Path"
    }
};


// ---------------------------------------------------------
// Task switching
// ---------------------------------------------------------

taskTabs.forEach((tab) => {

    tab.addEventListener("click", () => {

        currentTask = tab.dataset.task;

        taskTabs.forEach((item) => {
            item.classList.remove("active");
        });

        tab.classList.add("active");

        updateTaskUI();

    });

});


function updateTaskUI() {

    const config = taskConfig[currentTask];

    inputLabel.textContent = config.label;

    userInput.placeholder = config.placeholder;

    submitButton.textContent = config.button;

    lengthWrap.classList.toggle(
        "hidden",
        currentTask !== "summarize"
    );

    hoursWrap.classList.toggle(
        "hidden",
        currentTask !== "learn"
    );

    resultSection.classList.add("hidden");

    userInput.focus();

}


// ---------------------------------------------------------
// Backend health check
// ---------------------------------------------------------

async function checkBackend() {

    try {

        const response = await fetch("/health");

        if (!response.ok) {
            throw new Error("Backend health check failed");
        }

        const data = await response.json();

        if (data.status === "ok") {

            statusText.textContent = "Backend connected";

            statusDot.classList.add("online");

        } else {

            statusText.textContent = "Backend unavailable";

        }

    } catch (error) {

        statusText.textContent = "Backend unavailable";

        statusDot.classList.remove("online");

        console.error(error);

    }

}


// ---------------------------------------------------------
// API helper
// ---------------------------------------------------------

async function callAPI(endpoint, payload) {

    const response = await fetch(endpoint, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(payload)

    });

    const data = await response.json();

    if (!response.ok) {

        const message = Array.isArray(data.detail)
            ? data.detail.map((item) => {
                const field = Array.isArray(item.loc)
                    ? item.loc.slice(1).join(".")
                    : "";

                return field
                    ? `${field}: ${item.msg}`
                    : item.msg;
            }).join("; ")
            : data.detail || "Something went wrong.";

        throw new Error(message);

    }

    return data;

}


// ---------------------------------------------------------
// Request payloads
// ---------------------------------------------------------

function buildPayload() {

    const text = userInput.value.trim();

    const level = levelSelect.value;

    if (currentTask === "qa") {

        return {
            text: text,
            level: level
        };

    }

    if (currentTask === "explain") {

        return {
            text: text,
            level: level
        };

    }

    if (currentTask === "quiz") {

        return {
            text: text,
            level: level
        };

    }

    if (currentTask === "summarize") {

        return {
            text: text,
            level: level,
            length: summaryLength.value
        };

    }

    if (currentTask === "learn") {

        return {
            text: text,
            level: level,
            hours_per_week: Number(hoursInput.value)
        };

    }

}


// ---------------------------------------------------------
// Endpoint selection
// ---------------------------------------------------------

function getEndpoint() {

    const endpoints = {

        qa: "/qa",

        explain: "/explain",

        quiz: "/quiz",

        summarize: "/summarize",

        learn: "/learn/recommendations"

    };

    return endpoints[currentTask];

}


// ---------------------------------------------------------
// Result rendering
// ---------------------------------------------------------

function renderTextResult(data) {

    resultContainer.textContent =
        data.result ||
        data.answer ||
        data.explanation ||
        data.summary ||
        data.recommendations ||
        "No result returned.";

}


function renderQuizResult(data) {

    resultContainer.replaceChildren();

    const questions = data.questions || data.quiz?.questions;

    if (!Array.isArray(questions)) {

        resultContainer.textContent = "No quiz questions returned.";

        return;

    }

    questions.forEach((question, index) => {

        const card = document.createElement("div");

        card.className = "quiz-question";

        const heading = document.createElement("h3");

        heading.textContent = `${index + 1}. ${question.question}`;

        card.appendChild(heading);

        const optionsList = document.createElement("ol");

        question.options.forEach((option) => {

            const item = document.createElement("li");

            item.textContent = option;

            optionsList.appendChild(item);

        });

        card.appendChild(optionsList);

        const answer = document.createElement("p");

        answer.textContent =
            `Correct answer: ${question.correct_answer}`;

        card.appendChild(answer);

        if (question.explanation) {

            const explanation = document.createElement("p");

            explanation.textContent =
                `Explanation: ${question.explanation}`;

            card.appendChild(explanation);

        }

        resultContainer.appendChild(card);

    });

}


// ---------------------------------------------------------
// Form submission
// ---------------------------------------------------------

taskForm.addEventListener("submit", async (event) => {

    event.preventDefault();

    const text = userInput.value.trim();

    if (text.length === 0) {

        alert("Please enter some text.");

        return;

    }

    if (
        (currentTask === "quiz" ||
        currentTask === "summarize") &&
        text.length < 20
    ) {

        alert("Please enter at least 20 characters.");

        return;

    }

    if (
        currentTask === "learn" &&
        (
            Number(hoursInput.value) < 1 ||
            Number(hoursInput.value) > 60
        )
    ) {

        alert("Hours/week must be between 1 and 60.");

        return;

    }

    submitButton.disabled = true;

    submitButton.textContent = "Working...";

    resultSection.classList.remove("hidden");

    resultTitle.textContent = taskConfig[currentTask].title;

    resultContainer.textContent = "Generating response...";

    try {

        const data = await callAPI(
            getEndpoint(),
            buildPayload()
        );

        if (currentTask === "quiz") {

            renderQuizResult(data);

        } else {

            renderTextResult(data);

        }

    } catch (error) {

        resultContainer.textContent =
            `Error: ${error.message}`;

        console.error(error);

    } finally {

        submitButton.disabled = false;

        submitButton.textContent =
            taskConfig[currentTask].button;

    }

});


// ---------------------------------------------------------
// Copy result
// ---------------------------------------------------------

copyButton.addEventListener("click", async () => {

    const text = resultContainer.innerText;

    if (!text.trim()) {

        return;

    }

    try {

        await navigator.clipboard.writeText(text);

        copyButton.textContent = "Copied!";

        setTimeout(() => {

            copyButton.textContent = "Copy";

        }, 1500);

    } catch (error) {

        console.error("Copy failed:", error);

        alert("Unable to copy the result.");

    }

});


// ---------------------------------------------------------
// Initialize
// ---------------------------------------------------------

updateTaskUI();

checkBackend();