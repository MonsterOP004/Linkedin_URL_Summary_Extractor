# server.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from scrapper import html_to_yaml
from memoizer import memoized_scrape, memoized_llm_response
from dotenv import load_dotenv
import os

load_dotenv()

PORT = os.getenv("PORT")

app = FastAPI()

class UrlRequest(BaseModel):
    url: str

class IndexRequest(BaseModel):
    index_name: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the URL Scrapper Content API!"}

@app.post("/url_content_summarizer")
async def analyze_url(request: UrlRequest):
    try:
        # Step 1: Memoized Scraping
        scraped_data = memoized_scrape(request.url)

        if "error" in scraped_data:
            return {
                "status": "error",
                "message": f"Failed to scrape URL: {scraped_data['error']}",
                "url": request.url
            }

        # Step 2: Convert to YAML
        yaml_content = html_to_yaml(scraped_data)

        # Step 3: Memoized LLM Call
        analysis = memoized_llm_response(yaml_content)

        return {
            "status": "success",
            "url": request.url,
            "analysis": analysis
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(PORT)
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
