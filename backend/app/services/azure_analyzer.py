import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from .base_analyzer import BaseDocumentAnalyzer

class AzureDocumentAnalyzer(BaseDocumentAnalyzer):

    def __init__(self, endpoint: str = None, key: str = None):
        self.endpoint = endpoint or os.getenv("AZURE_ENDPOINT")
        self.key = key or os.getenv("AZURE_KEY")
        self.client = DocumentAnalysisClient(
            endpoint=self.endpoint, credential=AzureKeyCredential(self.key)
        )

    
    # layout detection using Azure
    def detect_layout_azure(file_path: str):
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

        filtered_paragraphs = self.remove_overlapping(bbox_paragraphs, bbox_tables)
        return filtered_paragraphs + bbox_tables
    
    def detect_layout(file_path: str):
        return detect_layout_azure(file_path)
    

# layout detection using Azure
