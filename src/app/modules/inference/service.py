import io
from typing import List
from PIL import Image
from fastapi import UploadFile, HTTPException
from google import genai
from app.core.config import settings

# Initialize Gemini Client
client = genai.Client(api_key=settings.API_KEY)


def verify_and_process_images(files: List[UploadFile]) -> List[Image.Image]:
    pil_images = []
    for file in files:
        try:
            content = file.file.read()
            image = Image.open(io.BytesIO(content))
            pil_images.append(image)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid image file '{file.filename}': {str(e)}",
            )
    return pil_images


def generate_response_issues(pil_images: List[Image.Image]) -> str:
    prompt = (
        "Analyze all the provided code screenshots together as a complete context. "
        "Describe all the issues across these images clearly. "
        "Do not provide any fixes, solutions, or code."
    )
    response = client.models.generate_content(
        model="gemini-3.8-flash", contents=[*pil_images, prompt]
    )
    return response.text


def generate_response_solution(pil_images: List[Image.Image], option: str) -> str:
    if option == "Hint":
        prompt = (
            "Analyze all the provided code screenshots together. "
            "Provide hints and explanations to help fix the issues shown across these images. "
            "Do not give the full solution or complete code."
        )
    else:
        prompt = (
            "Analyze all the provided code screenshots together. "
            "Provide the complete solution code along with a clear explanation "
            "to fix the issues shown across all these images."
        )

    response = client.models.generate_content(
        model="gemini-3.8-flash", contents=[*pil_images, prompt]
    )
    return response.text


def analyze_code_images(files: List[UploadFile], option: str) -> dict:
   
    pil_images = verify_and_process_images(files)

    issues_text = generate_response_issues(pil_images)
    solution_text = generate_response_solution(pil_images, option)

    return {
        "success": True,
        "issues": issues_text,
        "solution": solution_text,
        "option_selected": option,
    }
