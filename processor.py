import asyncio
import httpx
import time
from pprint import pprint

async def fetch_url(client, url):
    try:
        response = await client.get(url, timeout=5.0)
        response.raise_for_status()
        return {
            "URL":url,
            "Valid":True
        }

    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {str(e)}")
    except httpx.RequestError as e:
        print(f"Request error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

    return {
        "URL":url,
        "Valid":False
        }           


async def process_urls(URLS):
    valid_count = 0
    valid_urls = []

    start_time = time.perf_counter()

    async with httpx.AsyncClient() as client:
        try:
            results = await asyncio.gather(*(fetch_url(client, url) for url in URLS))

            for result in results:
                if result["Valid"]:
                    valid_count += 1
                    valid_urls.append(result["URL"])

        except Exception as e:
            print(f"Asyncio error: {str(e)}")

    end_time = time.perf_counter()
    exe_time = round(end_time - start_time, 2)

    return {
        "Execution_time": exe_time,
        "Valid_URL_count":valid_count,
        "Valid_URLS":valid_urls
    }         
                     

