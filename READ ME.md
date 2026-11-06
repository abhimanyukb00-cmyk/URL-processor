#URL processor

#A simple python script that is able to recive a batch of logs and process when while keeping track of the execution time and returning a clean, structured json consisting of the valid url count and the urls themselves.

#Makes use of FastAPI, pydantic BaseModel, uvicorn, asyncio...

#Requirements

#python 3.13.7 or higher.

#Make sure the following are installed.
```bash
pip install fastapi pydantic "uvicorn[standard]"