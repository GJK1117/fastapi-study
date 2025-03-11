from fastapi import (
    APIRouter, Request, Path, Query, Body, Cookie, Header, Form
)
from fastapi.responses import (
    PlainTextResponse, JSONResponse, HTMLResponse, ORJSONResponse
)
from fastapi.templating import Jinja2Templates
import os
from typing import (
    Union, Annotated, Literal, List
)
from pydantic import BaseModel, Field
from ...service.test_json_orjson import test_data, test_data_v2

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
async def test_json():
    return JSONResponse(status_code=200, content=test_data_v2)

@api_router_l_fastapi.get(
    '/html',
    response_class=HTMLResponse,
)
async def test_html():
    html_content: str = """
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
# request 필수
async def test_jinja2(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name='item.html', context={"id": id}
    )

@api_router_l_fastapi.get(
    '/orjson',
    response_class=ORJSONResponse,
)
async def test_orjson():
    return ORJSONResponse(status_code=200, content=test_data_v2)

# 경로파라미터 테스트, 경로 파라미터는 값이 필수로 입력됨. ...으로 표시해두면 좋음
# Query 함수에서 alias 인자는 요청을 보낼 때 쿼리파라미터 변수명을 다른 이름으로 사용할 수 있도록
# 설정하는 인자
@api_router_l_fastapi.get('/pathp/{item_id}', response_class=ORJSONResponse)
async def test_path_parameter(
    item_id: int = Path(title="The ID of the item to get"),
    q: Union[str, None] = Query(default=None, alias='item-query')
):
    results: dict = {'item_id': item_id}
    if q:
        results.update({'q': q})
    return ORJSONResponse(content=results, status_code=200)

@api_router_l_fastapi.get('/queryp')
async def test_query_parameter(
    q: Union[str, None] = Query(
        default=None,
        min_length=3,
        max_length=50,
    ), 
):
    results: dict = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({'q': q})
    return results

# *(Asterisk)를 사용하면 Query 함수를 사용해서 쿼리 인자를 정의하지 않아도 쿼리 파라미터로 인식
# 이러한 표현식도 있다 정도 아는 것, 명시적인게 더 좋지 않나?
@api_router_l_fastapi.get("/pathp1/{item_id}")
async def test_path_query_parameter(*, item_id: int = Path(title="The ID of the item to get"), q: str):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# 경로 파라미터의 숫자 검증: gt, le
# gt: 크거나, le: 작거나 같은, lt: 작거나, ge: 크거나 같은
@api_router_l_fastapi.get("/pathp2/{item_id}")
async def test_path_parameter_check_num(
    *,
    item_id: int = Path(title="The ID of the item to get", gt=0, le=1000), # <-- 0보다 크거나 1000보다 작거나
    q: str,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# 경로 파라미터의 숫자 검증, float형
@api_router_l_fastapi.get("/pathp3/{item_id}")
async def test_path_parameter_check_float(
    *,
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    q: str,
    size: float = Query(gt=0, lt=10.5),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if size:
        results.update({"size": size})
    return results

# Pydantic model을 활용하여 쿼리 파라미터를 표현
# FastAPI 0.115.0 부터 제공

class FilterParams(BaseModel):
    # 쿼리 파라미터로 요청할 때 추가적인 데이터 포함을 금지하는 설정
    # 사용은 선택적으로.
    model_config = {"extra": "forbid"}

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

@api_router_l_fastapi.get("/fquery/")
async def test_filter_query(filter_query: Annotated[FilterParams, Query()]):
    return filter_query

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@api_router_l_fastapi.get("/pqparam/{item_id}")
async def test_pqparam(
    *,
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    q: Union[str, None] = None,
    item: Union[Item, None] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

class User(BaseModel):
    username: str
    full_name: Union[str, None] = None

""" FastAPI가 인지하는 body의 구조
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    },
    "importance": 5
}
"""
@api_router_l_fastapi.put("/body/{item_id}")
async def test_body(item_id: int, item: Item, user: User, importance: int = Body(gt=0)):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results

""" FastAPI가 인지하는 body의 구조
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
}

Body 매개변수를 하나만 갖고 있을 때, item을 키 값으로 item class의 값을
가지지 않을 수 있음, embed=True 설정으로 item이라는 키 값 안에 Item class 값이 있도록 설정
"""
@api_router_l_fastapi.put("/bodyembed/{item_id}")
async def test_body_embed(item_id: int, item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results

class Cookies(BaseModel):
    # 추가 쿠키 내용을 금지
    model_config = {"extra": "forbid"}

    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None

@api_router_l_fastapi.get("/cookies/")
async def test_cookies(cookies: Annotated[Cookies, Cookie()]):
    return cookies

class CommonHeaders(BaseModel):
    # 추가 헤더 입력 금지
    # model_config = {"extra": "forbid"}

    # header의 키 값으로 사용할 떄는 _(underscore)를 -(minus)로 변환
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []

@api_router_l_fastapi.get("/header/")
async def test_header(headers: Annotated[CommonHeaders, Header()]):
    return headers

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float = 10.5
    tags: List[str] = []

items_first = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

@api_router_l_fastapi.get("/exc_unset/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def test_res_model_exclude_unset(item_id: str):
    return items_first[item_id]

items_second = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}

@api_router_l_fastapi.get(
    "/include/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
)
async def test_response_model_include(item_id: str):
    return items_second[item_id]

@api_router_l_fastapi.get("/exclude/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def test_response_model_exclude(item_id: str):
    return items_second[item_id]


