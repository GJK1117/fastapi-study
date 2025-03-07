import random
import string
from datetime import datetime, timedelta

# 임의의 큰 문자열을 생성하는 함수
def random_string(length=50):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# 시작 날짜 설정
base_date = datetime(2025, 1, 1, 12, 0, 0)

# 사용자 데이터 리스트 생성 (예: 1000명의 사용자)
users = []
for i in range(1000):
    user = {
        "id": i,
        "name": f"User{i}",
        "email": f"user{i}@example.com",
        "is_active": i % 2 == 0,
        "balance": round(random.uniform(0, 10000), 2),
        "bio": random_string(200),  # 큰 텍스트 필드
        "friends": [random.randint(0, 999) for _ in range(10)],  # 10명의 친구 id
        "settings": {
            "theme": "dark" if i % 2 == 0 else "light",
            "notifications": random.choice([True, False]),
            "language": random.choice(["en-US", "ko-KR", "es-ES", "fr-FR"]),
            "preferences": {
                "emails": random.choice([True, False]),
                "sms": random.choice([True, False]),
                "push": random.choice([True, False])
            }
        },
        "transactions": [
            {
                "date": (base_date + timedelta(days=random.randint(0, 365))).isoformat() + "Z",
                "amount": round(random.uniform(-500, 500), 2),
                "description": random_string(100)
            }
            for _ in range(5)
        ],
        "metadata": {
            "created_at": base_date.isoformat() + "Z",
            "updated_at": (base_date + timedelta(days=random.randint(1, 365))).isoformat() + "Z",
            "tags": [random_string(5) for _ in range(5)]
        }
    }
    users.append(user)

# 최종 테스트 데이터 dict
test_data = {
    "users": users,
    "summary": {
        "total_users": len(users),
        "active_users": sum(1 for u in users if u["is_active"]),
        "total_balance": sum(u["balance"] for u in users),
        "generated_at": datetime.now().isoformat() + "Z"
    },
    "config": {
        "version": "1.0.0",
        "features": {
            "enable_logging": True,
            "max_connections": 100,
            "supported_languages": ["en", "ko", "es", "fr", "de"]
        }
    }
}

"""
사용자 리스트(1000명의 사용자), 각 사용자의 다양한 속성(큰 문자열, 리스트, 중첩 딕셔너리 등)과 요약 정보를 포함하여, 
직렬화 시 복잡한 구조와 데이터 양으로 인해 orjson과 json 간의 성능 차이를 보다 명확하게 측정할 수 있도록 구성
"""

"""
postman api test 결과(size: 1.38MB)
1. 조건
    - response body size: 1.38MB
    - FastAPI JSONResponse, ORJSONResponse 사용
2. 결과
    - json lib 사용 시 응답 속도 약 23~25ms
    - orjson lib 사용 시 응답 속도 약 12ms

3. 결론
    - 간단한 json 데이터면 거의 차이 없음, json의 구조가 복잡하고 데이터가 많아지면 더 차이가 발생할 수 있음
    - orjson은 낮은 latency를 가지므로 트래픽이 생기면 각 처리 속도에 유리할 수 있음 (참고: https://chaechae.life/blog/fastapi-response-performance)
"""
