# AI Code Debugger API

A professional FastAPI backend built for AI-assisted code debugging. This service accepts screenshots of code, analyzes the visual context with Google Gemini, and returns:

- identified issues in the code
- hints for fixing the problem
- a full solution when requested

The API is designed to support frontend integrations, IDE assistant workflows, and debugging tools that need rich, multimodal reasoning from code images.

## Why this project exists

Developers frequently work with screenshots, error captures, and UI or code snippets that are difficult to paste into a prompt cleanly. This backend bridges that gap by letting users upload images of code or error screens and receive structured feedback from an AI model without requiring a local model deployment.

## Core capabilities

- Accepts up to 3 image files per request
- Supports multiple debugging modes:
  - `Hint` mode for guided guidance
  - `Solution` mode for complete fix recommendations
- Validates uploaded image files before processing
- Uses Gemini multimodal analysis to inspect code context across multiple screenshots
- Returns both detected issues and recommended next steps

## Technology stack

- Python 3.10+
- FastAPI
- Google GenAI SDK
- Pillow
- Python-dotenv
- Uvicorn
- Pydantic

## Project structure

```text
Ai-debugger-api/
├── src/
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── core/
│       │   ├── __init__.py
│       │   └── config.py
│       └── modules/
│           └── inference/
│               ├── __init__.py
│               ├── router.py
│               └── service.py
├── .env
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── README.md
└── .venv/
```

## Architecture overview

The application follows a modular FastAPI structure:

- `src/app/main.py` initializes the FastAPI application and global middleware.
- `src/app/core/config.py` loads environment variables and central settings.
- `src/app/modules/inference/router.py` exposes HTTP routes for health checks and debugging requests.
- `src/app/modules/inference/service.py` validates image input, calls Gemini, and combines evaluation results.

This separation keeps the API easy to extend when adding more debugging workflows, model providers, or response formats.

## Prerequisites

Before running the project, make sure you have:

- Python 3.10 or newer
- A valid Google Gemini API key
- Access to a frontend or client that can upload files via multipart form requests

## Environment configuration

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
ALLOWED_ORIGINS=http://localhost:3000
```

The application reads these values from the environment at startup.

## Installation

1. Clone the repository.
2. Create and activate a virtual environment.

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

Optional editable install:

```bash
pip install -e .
```

## Running the application

Because the app uses a `src` layout, set the Python path before launching Uvicorn.

On Windows PowerShell:

```powershell
$env:PYTHONPATH = "src"
uvicorn app.main:app --reload
```

On macOS/Linux:

```bash
export PYTHONPATH=src
uvicorn app.main:app --reload
```

The API will be available at:

- App root: `http://localhost:8000/`
- Health endpoint: `http://localhost:8000/api/v1/health`
- Swagger UI: `http://localhost:8000/docs`
- OpenAPI schema: `http://localhost:8000/api/v1/openapi.json`

## API endpoints

### GET /

Returns a welcome message from the API.

Example response:

```json
{
  "message": "Welcome to AI Code Debugger API"
}
```

### GET /api/v1/health

Checks whether the API is running correctly.

Example response:

```json
{
  "status": "ok",
  "message": "AI Debugger API is healthy"
}
```

### POST /api/v1/debug

Uploads one or more code screenshots and asks the model to analyze them.

Request parameters:

- `files`: one to three uploaded image files
- `option`: either `Hint` or `Solution`

Example using curl:

```bash
curl -X POST "http://localhost:8000/api/v1/debug" \
  -F "option=Hint" \
  -F "files=@screenshot1.png" \
  -F "files=@screenshot2.png"
```

Example response:

```json
{
  "success": true,
  "issues": "The screenshots show a missing import, an undefined variable, and an API call that does not match the expected response shape.",
  "solution": "Consider importing the missing module and checking the response payload before using the field names.",
  "option_selected": "Hint"
}
```

## Request behavior

- Images are validated with Pillow before analysis.
- Invalid files return a `400` error.
- More than 3 uploaded files return a `400` error.
- If Gemini processing fails, the API responds with a `500` error.

## Example usage flow

1. Open a frontend or API client.
2. Upload screenshots of code, UI, or error messages.
3. Choose `Hint` for explanation-only guidance or `Solution` for full remediation.
4. Review the returned analysis and fix instructions.

## Notes

This project currently uses a direct Gemini multimodal workflow and is intentionally lightweight. It is designed to be extended with:

- additional model providers
- custom prompt templates
- saved debug sessions
- user authentication
- database-backed history

## Professional summary

This repository delivers a focused, extensible AI debugging API that turns uploaded code screenshots into actionable developer feedback. It combines FastAPI, multimodal AI, and modular backend design to provide a clean path from raw visual debugging input to clear issue analysis and solution guidance.

```

## Model Loading Behavior

At startup, the app executes `ModelManager.load_all_models()`.

This loads every `.pkl` file in the `models/` directory and stores it in memory under the file name stem. For example:

- `income_salary_classification_model.pkl` -> `income_salary_classification_model`
- `house_price_regression_model.pkl` -> `house_price_regression_model`

If a model file is missing, the corresponding endpoint will return an HTTP 500 error with a message like:

```json
{
  "detail": "income_salary_classification_model not found."
}
```

## How the API Works

The inference service does the following:

1. Retrieves the required model from `ModelManager`
2. Converts the JSON payload into a pandas DataFrame
3. Calls the model's `predict()` method
4. Formats the result into a Pydantic response model
5. Adds confidence values when the model exposes probability or standard deviation data

## Notes

- CORS is enabled for all origins via `CORSMiddleware`
- The app is set up as a minimal ML serving layer, not a full business application
- Model compatibility depends on the structure and feature names expected by the saved `pkl` files

## Development Notes

If you want to extend this project:

- add new prediction routes under `src/app/modules/`
- keep request/response schemas in `schemas.py`
- keep model access logic inside the service layer
- add additional trained models to `models/` and they will be auto-discovered on startup

## License

This repository does not currently include a formal license file.