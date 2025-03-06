from fastapi import APIRouter
from fastapi.responses import (
    PlainTextResponse, JSONResponse
)

api_router_l_fastapi: APIRouter = APIRouter(
    prefix='/l_fastapi', 
    tags=['fastapi'],
)

@api_router_l_fastapi.get(
        '/plaintext', 
        response_class=PlainTextResponse,
)
async def test_plaintext():
    return 'hello test'

@api_router_l_fastapi.get(
    '/json',
    response_class=JSONResponse,
)
async def test_json():
    return {'content': 'hello'}