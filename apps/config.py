# fastapi 설정 및 환경 변수 정의
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic_settings import BaseSettings, SettingsConfigDict
from .api.v1 import api_router

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

# 환경 변수 설정, 바인딩할 변수 명을 class 내에서 선언해줘야 함.
class Setting(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR)

def create_app() -> FastAPI:
    app: FastAPI = FastAPI()

    # 모든 출처에서의 요청을 허용하기 위한 CORS 설정
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 모든 도메인에서 요청 허용
        allow_credentials=True,
        allow_methods=["*"],  # 모든 HTTP 메서드 허용 (GET, POST, PUT, DELETE 등)
        allow_headers=["*"],  # 모든 헤더 허용
    )

    # 정적 파일 저장소 마운트, css, js 등
    app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')

    # 하위 엔드포인트 APIRouter 추가 
    app.include_router(api_router)

    return app