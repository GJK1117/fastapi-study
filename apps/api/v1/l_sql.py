from fastapi import APIRouter

api_router_l_sql: APIRouter = APIRouter(
    prefix='/l_sql',
    tags=['sql', 'db', 'sqlite', 'sqlalchemy'],
)