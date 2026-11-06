from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from processor import process_urls

app = FastAPI()

class Response(BaseModel):
    Execution_time: float
    Valid_URL_count: int
    Valid_URLS: list[str]

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