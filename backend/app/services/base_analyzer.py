class BaseDocumentAnalyzer:
    """Base class for document analysis tools."""

    # check layout overlapping
    def is_overlapping(box1, box2):
        return not (
            box1[2] < box2[0] or  
            box1[0] > box2[2] or  
            box1[3] < box2[1] or  
            box1[1] > box2[3]    
        )

    def remove_overlapping(paragraphs, tables):
        """
        Remove paragraphs that overlap with tables.
        
        Args:
            paragraphs (list): List of bounding boxes for paragraphs.
            tables (list): List of bounding boxes for tables.
        
        Returns:
            list: Filtered list of paragraph bounding boxes.
        """
        filtered_paragraphs = []
        for paragraph in paragraphs:
            if not any(is_overlapping(paragraph, table) for table in tables):
                filtered_paragraphs.append(paragraph)
        return filtered_paragraphs
    
    def detect_layout(file_path: str):
    
        raise NotImplementedError("Subclasses must implement this method.")
    
