# import libraries
from dotenv import load_dotenv

# load environment variables
load_dotenv()

import logging
import os
from pathlib import Path
import uvicorn
from fastapi import FastAPI, File, Form, UploadFile, HTTPException

from app.services.azure_analyzer import AzureDocumentAnalyzer
from app.services.hf_analyzer import HFDocumentAnalyzer
from app.services.ollama_markdown_converter import OllamaMarkdownConverter
from app.services.openai_markdown_converter import OpenAIMarkdownConverter
from app.utils import save_md_file, clean_temp_storage, docx_to_images, pdf_to_images, crop_images

# initialize app
app = FastAPI()

# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# temporary storage for pdfs and images
TEMP_STORAGE_DIR = os.getenv("TEMP_STORAGE_DIR", "temp_storage")

# storage for .md files
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")

if not os.path.exists(TEMP_STORAGE_DIR):
    os.makedirs(TEMP_STORAGE_DIR)

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

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
    
# POST - /api/layout_entity_markdown
@app.post("/api/layout_entity_markdown")
async def layout_entity_markdown(file: UploadFile = File(...), system_prompt: str | None = Form(None), markdown_model_type: str | None = Form(None), layout_model_type: str | None = Form(None)):
    try:
        if file.filename == "":
            logger.warning(f"No file uploaded")
            raise HTTPException(status_code=400, detail="No file uploaded")
         
        file_extension = Path(file.filename).suffix.lower()
        logger.info(f"Uploaded file extension: {file_extension}")

        if file_extension not in [".pdf", ".docx", ".jpg", ".jpeg", ".png"]:
            logger.warning(f"Invalid file type: {file_extension}")
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_extension}")
        
        response = await process_file(file, file_extension, system_prompt, markdown_model_type, layout_model_type, layout=True)

        logger.info("Document converted successfully")
        return {'markdown': response}

    except Exception as e:
        logger.error(f"An error occurred during conversion: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred during conversion: {str(e)}")

# process the input file (.pdf)
async def process_file(file: UploadFile, file_extension: str, system_prompt: str, markdown_model_type: str, layout_model_type=None, layout=False):
    sys_prompt = system_prompt if system_prompt is not None else os.getenv("SYSTEM_PROMPT")
    markdown_generation_model_type = markdown_model_type if markdown_model_type is not None else os.getenv("MARKDOWN_GENERATION_MODEL_TYPE")
    
    if sys_prompt is None:
        raise ValueError(
            "Please set the system prompt"
        )
    
    if markdown_generation_model_type is None:
        raise ValueError(
            "Please set the markdown generation model type"
        )

    file_storage_path = f"{TEMP_STORAGE_DIR}/{file.filename}"
    with open(file_storage_path, "wb") as f:
            f.write(await file.read())

    if file_extension == ".docx":
        image_paths = docx_to_images(file_storage_path)

    elif file_extension == ".pdf":
        image_paths = pdf_to_images(file_storage_path)
    
    else:
        image_paths = [file_storage_path]
    
    if layout:
        layout_detection_model_type = layout_model_type if layout_model_type is not None else os.getenv("LAYOUT_DETECTION_MODEL_TYPE")

        if layout_detection_model_type is None:
            raise ValueError(
                "Please set the layout detection model type"
            )

        if layout_detection_model_type == "azure":
            bbox = AzureDocumentAnalyzer().detect_layout(image_paths[0])
        
        elif layout_detection_model_type == "hugging_face":
            bbox = HFDocumentAnalyzer().detect_layout(image_paths[0])

        image_paths = [crop_images(image_paths[0], bbox)[0]]
    
    if markdown_generation_model_type == "ollama":
            markdown_content = OllamaMarkdownConverter().convert_to_markdown(sys_prompt, image_paths)
        
    elif markdown_generation_model_type == "openai":
            markdown_content = OpenAIMarkdownConverter().convert_to_markdown(sys_prompt, image_paths)

    save_md_file(markdown_content)

    clean_temp_storage(TEMP_STORAGE_DIR)

    return markdown_content

# run app
if __name__ == "__main__":
    # set app host and app port
    app_host = os.getenv("APP_HOST", "0.0.0.0")
    app_port = int(os.getenv("APP_PORT", "5001"))

    uvicorn.run(app="main:app", host=app_host, port=app_port)
