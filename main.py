from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from processor import process_urls
from typing import Optional

app = FastAPI()

class URLResult(BaseModel):
    url: str
    status: str
    status_code: Optional[int] = None
    error_type: Optional[str] = None
    message: str

class Response(BaseModel):
    execution_time: float
    total_processed: int
    success_count: int
    error_count: int
    results: list[URLResult]

class Request(BaseModel):
    URLS: list[str]    

@app.post("/process/url_batch/", response_model=Response)
async def main(url_batch: Request):
    if not url_batch.URLS:
        raise HTTPException(status_code=400, detail="URL batch request cannot be empty!")

    result = await process_urls(url_batch.URLS)

    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000, host="localhost")