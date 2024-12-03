from fastapi import UploadFile
import os

from app.services.azure_analyzer import AzureDocumentAnalyzer
from app.services.hf_analyzer import HFDocumentAnalyzer
from app.services.ollama_markdown_converter import OllamaMarkdownConverter
from app.services.openai_markdown_converter import OpenAIMarkdownConverter
from app.utils import save_md_file, clean_temp_storage, docx_to_images, pdf_to_images, crop_images

TEMP_STORAGE_DIR = os.getenv("TEMP_STORAGE_DIR", "temp_storage")

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