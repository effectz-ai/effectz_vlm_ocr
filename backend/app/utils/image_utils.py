import os
from spire.doc import *
from spire.doc.common import *
import fitz
from PIL import Image

TEMP_STORAGE_DIR = os.getenv("TEMP_STORAGE_DIR", "temp_storage")

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
        image_name = f"img{page_num}.png"
        image_path = os.path.join(TEMP_STORAGE_DIR, image_name)
        pix.save(image_path)
        image_paths.append(image_path)

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