# Dockerfile 정의
FROM python:3.11-slim

# 작업 디렉토리 생성
WORKDIR /app

# 애플리케이션 코드 복사
COPY . .

# 시스템 패키지 및 Chrome 의존성 설치
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 컨테이너 실행 명령
# --workers 값 공식: CPU Core 개수 * 2 + 1, 일반적인 공식이며 환경에 따라 조절
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "10000", "--workers", "3", "apps.main:app"]