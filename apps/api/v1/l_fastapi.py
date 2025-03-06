from fastapi import APIRouter, Request
from fastapi.responses import (
    PlainTextResponse, JSONResponse, HTMLResponse
)
from fastapi.templating import Jinja2Templates
import os

TEMPLATES_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'templates')
templates: Jinja2Templates = Jinja2Templates(directory=TEMPLATES_DIR)

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
async def test_json():\
    return {'content': 'hello'}

@api_router_l_fastapi.get(
    '/html',
    response_class=HTMLResponse,
)
async def test_html():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    # 동일한 방법
    # return HTMLResponse(content=html_content, status_code=200)
    return html_content

@api_router_l_fastapi.get(
    '/jinja2/{id}',
    response_class=HTMLResponse,
)
async def test_jinja2(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name='item.html', context={"id": id}
    )