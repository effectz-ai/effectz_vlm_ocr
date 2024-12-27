import logging
from fastapi import APIRouter, HTTPException, Form
import json

from app.api.api_utils import process_url

url_to_markdown_router = app = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# POST - /api/url_to_markdown
@app.post("")
async def url_to_markdown(url: str = Form(...), options: str = Form(...)):
    try:
        if url == "":
            logger.warning(f"No url provided")
            raise HTTPException(status_code=400, detail="No url provided")
         
        logger.info(f"Provided URL: {url}")

        options_dict = json.loads(options)
        
        response = await process_url(url, options_dict)

        logger.info("Document converted successfully")
        return {'markdown': response}

    except Exception as e:
        logger.error(f"An error occurred during conversion: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred during conversion: {str(e)}")