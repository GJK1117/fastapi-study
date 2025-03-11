# Python backend(FastAPI) study

## 설명
- 인턴 과정에서 사용하는 Python Backend 프레임워크 및 인프라 요소에 능숙해지며, 개인적인 능력 향상을 위해 공부 기록을 남기는 repo
- 디렉터리 구조는 FastAPI에서 사용하는 APIRouter 구조를 차용
``` Directory Structure
fastapi-study/
│── apps/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   ├── api/
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── dependencies.py
│   │   │   ├── l_fastapi.py
│   │   │   ├── l_sql.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── item.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── item.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── item_service.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py
│   ├── tests/
│   │   ├── test_users.py
│   │   ├── test_items.py
│── .gitignore
│── Dockerfile
│── README.md
│── requirements.txt

```

## 기간
### 1주차: 25.02.24. ~ 25.02.28.
- SQLAlchemy 공식 문서 읽기 및 타이핑, [SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/20/tutorial/index.html)
- Flask 기능 추가 업무, Flask context, Flask_APScheduler, crontab 등에 관련한 이슈 경험과 개념 학습
- Git branch, merge, push 명령어를 cli에서 실습

### 2주차 25.03.03. ~ 25.03.07.
- SQLite 관련 이슈를 적절히 대응하기 위해 SQLite에 대한 학습(+ SQLAlchemy 이어서 학습), [SQLite Documentation](https://www.sqlite.org/docs.html)
- Git Action WorkFlow 작성 방법에 대해 학습(SSH, Docker, Test)
- FastAPI 시작(uvicorn) 및 환경변수 주입 학습(pydantic_settings, lru_cache)

### 3주차 25.03.10. ~ 25.03.14.
- AI서비스 인수인계
- 

### 4주차 25.03.17. ~ 25.03.21.

### 5주차 25.03.24. ~ 25.03.28.

### 6주차 25.03.31. ~ 25.04.04.

### 7주차 25.04.07. ~ 25.04.11.

### 8주차 25.04.14. ~ 25.04.18.

### 9주차 25.04.21. ~ 25.04.25.

### 10주차 25.04.28. ~ 25.05.02.

### 11주차 25.05.05. ~ 25.05.09.

### 12주차 25.05.12. ~ 25.05.16.

### 13주차 25.05.19. ~ 25.05.23.

### 14주차 25.05.26. ~ 25.05.30.

### 15주차 25.06.02. ~ 25.06.06.

### 16주차 25.06.09. ~ 25.06.13.

### 17주차 25.06.16. ~ 25.06.20.

### 18주차 25.06.23. ~ 25.06.27.

### 19주차 25.06.30. ~ 25.07.04.

### 20주차 25.07.07. ~ 25.07.11.

### 21주차 25.07.14. ~ 25.07.18.

### 22주차 25.07.21. ~ 25.07.25.

### 23주차 25.07.28. ~ 25.08.01.

### 24주차 25.08.04. ~ 25.08.08.

### 25주차 25.08.11. ~ 25.08.15.

### 26주차 25.08.18. ~ 25.08.22.

