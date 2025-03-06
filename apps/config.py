# fastapi 설정 및 환경 변수 정의
import os
from functools import lru_cache
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')

class Setting(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR)

@lru_cache
def get_settings() -> Setting:
    return Setting()

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

    return app