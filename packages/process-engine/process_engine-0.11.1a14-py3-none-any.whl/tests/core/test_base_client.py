
import asyncio
import pytest

from process_engine.core.base_client import BaseClient

from tests.helper_aiohttp import http_redirect, CaseControlledTestServer

TIMEOUT = 1

@pytest.mark.asyncio
async def test_server_info(http_redirect):

    sample_response = """
    {"name": "@process-engine/process_engine_runtime", 
    "version": "8.5.0", 
    "description": "Standalone application that provides access to the .TS implementation of the ProcessEngine.", 
    "license": "MIT", 
    "homepage": "https://www.process-engine.io/"}
    """

    async with CaseControlledTestServer() as server:
        http_redirect.add_server('api.process-engine.io', 56100, server.port)
        client = BaseClient('http://api.process-engine.io:56100', http_redirect.session)

        task = asyncio.ensure_future(client.get_serverinfo())
        request = await server.receive_request(timeout=TIMEOUT)

        server.send_response(request,  
            text=sample_response,
            content_type='application/json'
        )

        result = await asyncio.wait_for(task, TIMEOUT)
    
        assert(result['version'] == '8.5.0')
