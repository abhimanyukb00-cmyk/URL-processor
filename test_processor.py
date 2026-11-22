import respx
from processor import fetch_url, process_urls
import pytest
import httpx

#fetch_url()
@pytest.mark.asyncio
async def test_fetch_url_sucess(respx_mock):
    url = "https://example.com/api"
    respx_mock.get(url).respond(200)

    import asyncio
    semaphore = asyncio.Semaphore(5)

    async with httpx.AsyncClient() as client:
        result = await fetch_url(client, url, semaphore)

    assert result["status_code"] == 200
    assert result["status"] == "success"

@pytest.mark.asyncio
async def test_url_not_found(respx_mock):
    url = "https://example.com/missing"
    respx_mock.get(url).respond(404)

    import asyncio
    semaphore = asyncio.Semaphore(5)

    async with httpx.AsyncClient() as client:
        result = await fetch_url(client, url, semaphore)

    assert result["status_code"] == 404
    assert result["status"] ==  "error"

@pytest.mark.asyncio
async def test_timeout_error(respx_mock):
    url = "https://example.com/timeout"
    respx_mock.get(url).mock(side_effect=httpx.TimeoutException("Request timed out"))

    import asyncio
    semaphore = asyncio.Semaphore(5)

    async with httpx.AsyncClient() as client:
        result = await fetch_url(client, url, semaphore)

    assert result["error_type"] == "TimeoutException"
    assert result["status"] == "error"

@pytest.mark.asyncio
async def test_genaral_exception(respx_mock):
    url = "https://example.com/exception"
    respx_mock.get(url).mock(side_effect=Exception("Unexcepted error"))

    import asyncio
    semaphore = asyncio.Semaphore(5)

    async with httpx.AsyncClient() as client:
        result = await fetch_url(client, url, semaphore)

    assert result["error_type"] == "UnexpectedError"
    assert result["status"] == "error"

#process_url()
@pytest.mark.asyncio
async def test_process_url_output(respx_mock):
    urls = ["httpx://example.com/200", "httpx://example.com/404"]

    respx_mock.get("httpx://example.com/200").mock(return_value=httpx.Response(200))    
    respx_mock.get("httpx://example.com/404").mock(return_value=httpx.Response(404))

    semaphore = 2

    request = {
        "urls":urls,
        "semaphore_limit":semaphore
    }

    res = await process_urls(request)

    assert res["total_processed"] == 2
    assert res["success_count"] == 1
    assert res["error_count"] == 1





