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
from PIL import Image
import torch
from transformers import AutoImageProcessor
from transformers.models.detr import DetrForSegmentation
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

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
async def get_markdown(file: UploadFile = File(...), vlm: str | None = Form(None), system_prompt: str | None = Form(None)):
    try:
        if file.filename == "":
            logger.warning(f"No file uploaded")
            raise HTTPException(status_code=400, detail="No file uploaded")
         
        file_extension = Path(file.filename).suffix.lower()
        logger.info(f"Uploaded file extension: {file_extension}")

        if file_extension not in [".pdf", ".docx", ".jpg", ".jpeg", ".png"]:
            logger.warning(f"Invalid file type: {file_extension}")
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_extension}")
        
        response = await process_file(file, file_extension, vlm, system_prompt)

        logger.info("Document converted successfully")
        return {'markdown': response}

    except Exception as e:
        logger.error(f"An error occurred during conversion: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred during conversion: {str(e)}")
    
# POST - /api/layout_entity_markdown
@app.post("/api/layout_entity_markdown")
async def layout_entity_markdown(file: UploadFile = File(...), vlm: str | None = Form(None), system_prompt: str | None = Form(None), layout_model_type: str | None = Form(None)):
    try:
        if file.filename == "":
            logger.warning(f"No file uploaded")
            raise HTTPException(status_code=400, detail="No file uploaded")
         
        file_extension = Path(file.filename).suffix.lower()
        logger.info(f"Uploaded file extension: {file_extension}")

        if file_extension not in [".pdf", ".docx", ".jpg", ".jpeg", ".png"]:
            logger.warning(f"Invalid file type: {file_extension}")
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_extension}")
        
        response = await process_file(file, file_extension, vlm, system_prompt, layout_model_type, layout=True)

        logger.info("Document converted successfully")
        return {'markdown': response}

    except Exception as e:
        logger.error(f"An error occurred during conversion: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred during conversion: {str(e)}")

# process the input file (.pdf)
async def process_file(file: UploadFile, file_extension: str, vlm: str, system_prompt: str, layout_model_type=None, layout=False):
    vlm_name = vlm if vlm is not None else os.getenv("VLM")
    sys_prompt = system_prompt if system_prompt is not None else os.getenv("SYSTEM_PROMPT")
    layout_detection_model_type = layout_model_type if layout_model_type is not None else os.getenv("LAYOUT_DETECTION_MODEL_TYPE")

    if vlm_name is None:
        raise ValueError(
            "Please set the VLM"
        )
    
    if sys_prompt is None:
        raise ValueError(
            "Please set the system prompt"
        )
    
    if layout_detection_model_type is None:
        raise ValueError(
            "Please set the layout detection model type"
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
        if layout_detection_model_type == "azure":
            bbox = layout_detection_azure(image_paths[0])
        
        elif layout_detection_model_type == "hugging_face":
            bbox = layout_detection_hf(image_paths[0])

        image_paths = [crop_images(image_paths[0], bbox)[0]]

    markdown_content = get_vlm_response(vlm_name, sys_prompt, image_paths)

    save_md_file(markdown_content)

    clean_temp_storage(TEMP_STORAGE_DIR)

    return markdown_content

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

# crop images according to bbox
def crop_images(file_path: str, bbox: list[list]):
    image_paths = []
    img = Image.open(file_path).convert("RGB")

    for idx, box in enumerate(bbox):
        x_min, y_min, x_max, y_max = map(int, box)
        cropped_img = img.crop((x_min, y_min, x_max, y_max))  
        final_image = Image.new("RGB", img.size, (255, 255, 255))
        final_image.paste(cropped_img, (x_min, y_min))
        final_image_name = f"entity_{idx}.png"
        final_image_path = os.path.join(TEMP_STORAGE_DIR, final_image_name)
        final_image.save(final_image_path)
        image_paths.append(final_image_path)

    return image_paths

# check layout overlapping
def is_overlapping(box1, box2):
    return not (
        box1[2] < box2[0] or  
        box1[0] > box2[2] or  
        box1[3] < box2[1] or  
        box1[1] > box2[3]    
    )

# remove overlapping layouts between paragraphs and tables
def remove_overlapping(paragraphs, tables):
    filtered_paragraphs = []
    for paragraph in paragraphs:
        if not any(is_overlapping(paragraph, table) for table in tables):
            filtered_paragraphs.append(paragraph)
    return filtered_paragraphs

# layout detection using Azure
def layout_detection_azure(file_path: str):
    azure_endpoint = os.getenv("AZURE_ENDPOINT")
    azure_key = os.getenv("AZURE_KEY")

    document_analysis_client = DocumentAnalysisClient(
        endpoint=azure_endpoint, credential=AzureKeyCredential(azure_key)
    )

    with open(file_path, "rb") as file:
        poller = document_analysis_client.begin_analyze_document("prebuilt-layout", file)
        result = poller.result()
    
    bbox_paragraphs = []
    bbox_tables = []

    for paragraph in result.paragraphs:
        for region in paragraph.bounding_regions:
            polygon = region.polygon
            bounding_box = [
                    min(point.x for point in polygon),
                    min(point.y for point in polygon),
                    max(point.x for point in polygon),
                    max(point.y for point in polygon)
                ]      
            bbox_paragraphs.append(bounding_box)

    for table in result.tables:
        for region in table.bounding_regions:
            polygon = region.polygon
            bounding_box = [
                    min(point.x for point in polygon),
                    min(point.y for point in polygon),
                    max(point.x for point in polygon),
                    max(point.y for point in polygon)
                ] 
            bbox_tables.append(bounding_box)

    filtered_paragraphs = remove_overlapping(bbox_paragraphs, bbox_tables)
    return filtered_paragraphs + bbox_tables
    
# layout detection using Hugging Face model
def layout_detection_hf(file_path: str):
    layout_detection_img_proc = AutoImageProcessor.from_pretrained(os.getenv("HF_IMG_PROC_NAME"))
    layout_detection_hf_model = DetrForSegmentation.from_pretrained(os.getenv("HF_MODEL_NAME"))

    if layout_detection_img_proc is None:
        raise ValueError(
            "Please set the Hugging Face layout detection image processor"
        )
    
    if layout_detection_hf_model is None:
        raise ValueError(
            "Please set the Hugging Face layout detection model name"
        )

    img = Image.open(file_path).convert("RGB")

    with torch.inference_mode():
        input_ids = layout_detection_img_proc(img, return_tensors='pt')
        output = layout_detection_hf_model(**input_ids)
    
    threshold=0.75

    bbox_pred = layout_detection_img_proc.post_process_object_detection(
        output,
        threshold=threshold,
        target_sizes=[img.size[::-1]]
    )

    detected_entities = bbox_pred[0]

    return detected_entities['boxes']

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
