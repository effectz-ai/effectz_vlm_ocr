# import libraries
from dotenv import load_dotenv

# load environment variables
load_dotenv()

import logging
import os
from pathlib import Path
import glob
import uvicorn
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
import ollama
import fitz 
from spire.doc import *
from spire.doc.common import *

# initialize app
app = FastAPI()

# temporary storage for pdfs and images
TEMP_STORAGE_DIR = os.getenv("TEMP_STORAGE_DIR", "temp_storage")

# storage for .md files
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")

if not os.path.exists(TEMP_STORAGE_DIR):
    os.makedirs(TEMP_STORAGE_DIR)

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# POST
@app.post("/api/get_markdown")
async def get_markdown(file: UploadFile = File(...), vlm: str | None = Form(None), system_prompt: str | None = Form(None)):
    try:
        file_extension = Path(file.filename).suffix.lower()
        logging.info(f"Uploaded file extension: {file_extension}")

        if file_extension not in [".pdf", ".docx"]:
            logging.warning(f"Invalid file type: {file_extension}")
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_extension}")
        
        await process_file(file, file_extension, vlm, system_prompt)

        logging.info("Document converted successfully")
        return {'message': 'Document conversion completed!'}

    except Exception as e:
        logging.error(f"HTTPException: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# process the input file (.pdf)
async def process_file(file: UploadFile, file_extension: str, vlm: str, system_prompt: str):
    vlm_name = vlm if vlm is not None else os.getenv("VLM")
    sys_prompt = system_prompt if system_prompt is not None else os.getenv("SYSTEM_PROMPT")

    if vlm_name is None:
        raise ValueError(
            "Please set the VLM"
        )
    
    if sys_prompt is None:
        raise ValueError(
            "Please set the system prompt"
        )
    
    file_storage_path = f"{TEMP_STORAGE_DIR}/{file.filename}"
    with open(file_storage_path, "wb") as f:
            f.write(await file.read())

    if file_extension == ".docx":
        image_paths = docx_to_images(file_storage_path)

    else:
        image_paths = pdf_to_images(file_storage_path)
    
    markdown_content = get_vlm_response(vlm_name, sys_prompt, image_paths)

    save_md_file(markdown_content)

    clean_temp_storage(TEMP_STORAGE_DIR)

# convert the docx into images and temporarily store them
def docx_to_images(file_path: str):
    document = Document()
    document.LoadFromFile(file_path)

    image_paths = []

    image_streams = document.SaveImageToStreams(ImageType.Bitmap)

    for image in image_streams:
        image_name = f"img.png"
        image_path = os.path.join(TEMP_STORAGE_DIR, image_name)
        with open(image_path,'wb') as image_file:
            image_file.write(image.ToArray())
        image_paths.append(image_path)
        break

    document.Close()
    
    return image_paths

# convert the pdf into images and temporarily store them
def pdf_to_images(file_path: str):
    pdf_document = fitz.open(file_path)

    image_paths = []

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap(dpi=300) 
        image_name = f"img.png"
        image_path = os.path.join(TEMP_STORAGE_DIR, image_name)
        pix.save(image_path)
        image_paths.append(image_path)
        break

    pdf_document.close()

    return image_paths

# get response from the VLM
def get_vlm_response(vlm: str, system_prompt: str, image_path_list: list[str]):
    response = ollama.chat(
        model=vlm, 
        messages=[
            {
                'role': 'system',
                'content': (system_prompt)
            },
            {
                'role': 'user',
                'images': image_path_list
            }
        ]
    )

    return response["message"]["content"]

# save the .md file
def save_md_file(markdown_content: str):
    with open(f"{OUTPUT_DIR}/output.md", "w") as file:
        file.write(markdown_content)

# clean the temporary storage
def clean_temp_storage(folder_path: str):
    for file_path in glob.glob(os.path.join(folder_path, "*")):
        os.remove(file_path)

# run app
if __name__ == "__main__":
    # set app host and app port
    app_host = os.getenv("APP_HOST", "0.0.0.0")
    app_port = int(os.getenv("APP_PORT", "5001"))

    uvicorn.run(app="main:app", host=app_host, port=app_port)
