import logging
from fastapi import APIRouter, HTTPException, Form, UploadFile, File
from pathlib import Path

from app.api.api_utils import process_file

get_markdown_router = app = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# POST - /api/get_markdown
@app.post("/api/get_markdown")
async def get_markdown(file: UploadFile = File(...), system_prompt: str | None = Form(None), markdown_model_type: str | None = Form(None)):
    try:
        if file.filename == "":
            logger.warning(f"No file uploaded")
            raise HTTPException(status_code=400, detail="No file uploaded")
         
        file_extension = Path(file.filename).suffix.lower()
        logger.info(f"Uploaded file extension: {file_extension}")

        if file_extension not in [".pdf", ".docx", ".jpg", ".jpeg", ".png"]:
            logger.warning(f"Invalid file type: {file_extension}")
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_extension}")
        
        response = await process_file(file, file_extension, system_prompt, markdown_model_type)

        logger.info("Document converted successfully")
        return {'markdown': response}

    except Exception as e:
        logger.error(f"An error occurred during conversion: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred during conversion: {str(e)}")