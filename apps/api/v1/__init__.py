from fastapi import APIRouter
from .l_fastapi import api_router_l_fastapi
from .l_sql import api_router_l_sql

# APIRouter 정의
api_router:APIRouter = APIRouter()

# 하위 APIRouter 추가
api_router.include_router(api_router_l_fastapi)
api_router.include_router(api_router_l_sql)

# ✅ 디버깅 출력
# print(f"Sub-router (l_fastapi) registered: {[route.path for route in api_router_l_fastapi.routes]}")
# print(f"Sub-router (l_sql) registered: {[route.path for route in api_router_l_sql.routes]}")