import os
import torch
from transformers import AutoImageProcessor
from transformers.models.detr import DetrForSegmentation
from PIL import Image

from .base_analyzer import BaseDocumentAnalyzer

class HFDocumentAnalyzer(BaseDocumentAnalyzer):

    def detect_layout(self, file_path: str):
        return self.detect_layout_hf(file_path)

    def detect_layout_hf(self, file_path: str):
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

    
