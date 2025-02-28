# Python backend(FastAPI) study

## 설명
- 인턴 과정에서 사용하는 Python Backend 프레임워크에 능숙해지며, 개인적인 능력 향상을 위해 공부 기록을 남기는 repo
- 디렉터리 구조는 FastAPI에서 사용하는 APIRouter 구조를 차용
``` Directory Structure
fastapi-study/
│── apps/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── users.py
│   │   │   ├── items.py
│   │   │   ├── auth.py
│   │   ├── dependencies.py
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
### 25.02.24 ~ 25.02.28
- SQLAlchemy 공식 문서 읽기 및 타이핑
- Flask 기능 추가 업무, Flask context, Flask_APScheduler, crontab 등에 관련한 이슈 경험과 개념 학습
- Git branch, merge, push 명령어를 cli에서 실습

