# Dockerfile 정의
FROM python:3.8.10-slim

# 작업 디렉토리 생성
WORKDIR /app

# 애플리케이션 코드 복사
COPY . .

# 시스템 패키지 및 Chrome 의존성 설치
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 컨테이너 실행 명령
CMD ["python", "main.py"]