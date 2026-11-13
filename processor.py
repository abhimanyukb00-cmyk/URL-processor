import asyncio
import httpx
import time
from pprint import pprint

async def fetch_url(client, url, limit):
    async with limit:
        try:
            response = await client.get(url, timeout=5.0)
            response.raise_for_status()
            return {
                "url":url,
                "status":"success",
                "status_code":200,
                "error_type":None,
                "message":"OK"
            }

        except httpx.TimeoutException as e:
            return {
                "url":url,
                "status":"error",
                "status_code":None,
                "error_type":"TimeoutException",
                "message":f"Request timeout: {str(e)}"
            }

        except httpx.HTTPStatusError as e:
                    return {
                "url":url,
                "status":"error",
                "status_code":e.response.status_code,
                "error_type":"HTTPStatusError",
                "message":f"Client error: {str(e)}"
            }

        except httpx.RequestError as e:
                    return {
                "url":url,
                "status":"error",
                "status_code":None,
                "error_type":"RequestError",
                "message":f"Connection failed: {str(e)}"
            }

        except Exception as e:
                    return {
                "url":url,
                "status":"error",
                "status_code":None,
                "error_type":"UnexpectedError",
                "message":f"Unexpected error: {str(e)}"
            }

async def process_urls(request):
    URLS = request["urls"]
    semaphore_limit = request["semaphore_limit"]

    valid_count = 0

    semaphore = asyncio.Semaphore(semaphore_limit)

    start_time = time.perf_counter()

    async with httpx.AsyncClient() as client:
        try:
            results = await asyncio.gather(*(fetch_url(client, url, semaphore) for url in URLS))

            for result in results:
                if result["status_code"] == 200:
                    valid_count += 1

        except Exception as e:
            print(f"Asyncio error: {str(e)}")

    end_time = time.perf_counter()
    exe_time = round(end_time - start_time, 2)

    return {
        "execution_time": exe_time,
        "total_processed":len(URLS),
        "success_count":valid_count,
        "error_count":len(URLS) - valid_count,
        "results":results
    }         
                     

