from fastapi import APIRouter
from .l_fastapi import api_router_l_fastapi
from .l_sql import api_router_l_sql

# APIRouter 정의
api_router:APIRouter = APIRouter()

# 하위 APIRouter 추가
api_router.include_router(api_router_l_fastapi)
api_router.include_router(api_router_l_sql)