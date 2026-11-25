# URL-processor

An asynchronous batch URL checker built with FastAPI and `httpx`, using `asyncio.Semaphore` to bound concurrent outgoing requests and return structured success/error summaries.

## Features

- Concurrent URL fetching controlled by a configurable `semaphore_limit`
- Handles HTTP status codes (`200`, `404`, etc.), `httpx.TimeoutException`, and unexpected exceptions cleanly without crashing the batch
- Async unit test suite powered by `pytest`, `pytest-asyncio`, and `respx`

## Setup

```bash
git clone [https://github.com/abhimanyukb00-cmyk/URL-processor.git](https://github.com/abhimanyukb00-cmyk/URL-processor.git)
cd URL-processor
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt