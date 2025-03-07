# FastAPI 프레임워크 기본 정의
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from functools import lru_cache
from .config import Setting, create_app

app: FastAPI = create_app()

# lru_cache decorator: Python 내장 데코레이터, 함수 결과를 캐시, 이미 캐시되어 있다면 함수를 실행하지 않고 캐시 결과 반환
# .env로 환경변수를 주입하는 과정에서 파일을 읽는 비용을 최적화하기 위해 사용
# 환경변수로 한 번 주입된 것은 거의 변화가 없을 것을 가정
@lru_cache
def get_settings() -> Setting:
    return Setting()

# include_in_schema=False 설정 시
# 1. OpenAPI 스키마 생성 시간 단축
# 2. 라우터 정보에 표시되지 않아 보안적 이점
@app.get(
        "/",
        response_class=PlainTextResponse,
        include_in_schema=False,
)
async def health() -> PlainTextResponse:
    return 'ok'

# 라우트 확인 로그
print(f"Registered routes: {[route.path for route in app.routes]}")

# 테스트 시 명령어 사용 예시
# uvicorn --port 20000 --reload apps.main:app