from typing import List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.modules.inference.service import analyze_code_images

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok", "message": "AI Debugger API is healthy"}


@router.post("/debug")
async def debug_code(
    files: List[UploadFile] = File(...),
    option: str = Form(...),  # Options: 'Hint' or 'Solution'
):
    if not files:
        raise HTTPException(status_code=400, detail="No image files uploaded.")

    if len(files) > 3:
        raise HTTPException(
            status_code=400, detail="Maximum 3 images allowed per request."
        )

    try:
        # Delegate image verification, processing, and Gemini calls to the service layer
        result = analyze_code_images(files, option)
        return result

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Gemini Processing Error: {str(e)}"
        )
