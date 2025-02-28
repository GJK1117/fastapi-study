from sqlalchemy import (
    create_engine, text, Table, Column, Integer, String, MetaData, ForeignKey
)

'''
create_engine의 첫 인자에 대한 정보
1. 어떤 DB와 연결하는지(sqlite)
2. 연결하는 DB API, 드라이버가 무엇인지(pysqlite)
3. DB의 위치를 어떻게 정의할 것인지, 이 경우 로컬에서 테스트하므로 memory로 작성
    -> local에서 docker나 SQL program 실행 없이 in-memory로 데이터를 저장하고 휘발

Lazy Conneting으로 연결 요청이 있을 때 실제로 DB와 연결되어 통신

echo 인자를 True로 설정하여 SQL 요청에 대한 결과를 콘솔에 출력하도록 함

future 인자를 True로 설정하여 sqlalchemy 2.0에 대한 설명으로 진행됨
future 인자는 버전 2.0의 코드 스타일을 활성화 여부 옵션
'''
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)

# 버전 1.4 스타일 / 버전 2.0 스타일 차이
# 1. Connection API
# 1.4
'''
conn = engine.connect()
conn.execute("SELECT 1")  # 실행
conn.commit()
conn.close()
'''

# 2.0
'''
with engine.begin() as conn:
    conn.execute("SELECT 1")  # 실행
'''

# 2. Session
# 1.4
'''
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()
'''

# 2.0
'''
from sqlalchemy.orm import Session

with Session(engine) as session:
    # 세션이 자동으로 닫힘
    ...
'''

# 3. Result 객체 사용 방식
# 1.4
'''
result = conn.execute("SELECT 1")
row = result.fetchone()
print(row[0])  # 인덱싱 방식
'''

# 2.0
'''
result = conn.execute("SELECT 1")
row = result.one()
print(row)  # 네임드 튜플 방식

네임드 튜플 방식: Collections.namedtuple type, tuple + dict의 데이터 구조, immutable하면서 필드 값에 접근할 수 있는 기능
'''

# Connection Example
''' code
with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())'''

''' console
2025-02-26 10:09:14,462 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-02-26 10:09:14,462 INFO sqlalchemy.engine.Engine select 'hello world'      
2025-02-26 10:09:14,462 INFO sqlalchemy.engine.Engine [generated in 0.00036s] ()
[('hello world',)]
2025-02-26 10:09:14,463 INFO sqlalchemy.engine.Engine ROLLBACK
'''

''' script
DB와 연결 후(BEGIN) text로 작성했던 쿼리가 실행, 이후 연결이 끊어진 다음 ROLLBACK이 수행

이 경우 쿼리가 DB에 적용되지 않음, 쿼리를 적용하기 위해 Connection.commit()을 수행해야 함
'''

# Committing Changes
''' code
with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
    )
    conn.commit()
'''

''' console
2025-02-26 10:20:33,793 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-02-26 10:20:33,793 INFO sqlalchemy.engine.Engine CREATE TABLE some_table (x int, y int)     
2025-02-26 10:20:33,793 INFO sqlalchemy.engine.Engine [generated in 0.00049s] ()
2025-02-26 10:20:33,795 INFO sqlalchemy.engine.Engine INSERT INTO some_table (x, y) VALUES (?, ?)
2025-02-26 10:20:33,795 INFO sqlalchemy.engine.Engine [generated in 0.00040s] [(1, 1), (2, 4)]
2025-02-26 10:20:33,795 INFO sqlalchemy.engine.Engine COMMIT
'''

''' script
conn.commit()를 사용하여 쿼리를 통한 데이터 변경 사항을 DB에 적용
현 예시는 두 쿼리 문을 하나의 conmmit()으로 적용했지만, 그 사이 혹은 그 이후에
쿼리를 추가하고 쿼리에 대한 commit()을 수행할 수 있음
'''

# begin once
''' code
with engine.begin() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 6, "y": 8}, {"x": 9, "y": 10}]
    )
'''

''' console
2025-02-26 10:29:39,887 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-02-26 10:29:39,888 INFO sqlalchemy.engine.Engine CREATE TABLE some_table (x int, y int)
2025-02-26 10:29:39,888 INFO sqlalchemy.engine.Engine [generated in 0.00022s] ()
2025-02-26 10:29:39,889 INFO sqlalchemy.engine.Engine INSERT INTO some_table (x, y) VALUES (?, ?)
2025-02-26 10:29:39,889 INFO sqlalchemy.engine.Engine [generated in 0.00019s] [(6, 8), (9, 10)]
2025-02-26 10:29:39,889 INFO sqlalchemy.engine.Engine COMMIT
'''

''' script
with 절을 engine.begin()로 사용

별도의 commit, rollback 명시 없이 예외 없이 적용되서 블록이 끝나면 commit,
예외 발생 시 ROLLBACK을 해주는 코드 스타일
'''

# 쿼리 실행 시 console 처음에 뜨는 BEGIN(implicit)
''' script
DB에 실제로 BEGIN이라는 명령을 보내진 않지만 명시적으로 트랜잭션을 시작했다는 표시
보통 트랜잭션은 "BEGIN -> SQL 실행 -> COMMIT or ROLLBACK" 의 과정
'''

# Basics of Statement Execution
# 1. Fetching Rows
''' code
with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    result = conn.execute(text("SELECT x, y FROM some_table"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 6, "y": 8}, {"x": 9, "y": 10}]
    )
    for row in result:
        print(f"x: {row.x} y: {row.y}")
        
'''

''' console
2025-02-26 10:45:20,962 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-02-26 10:45:20,962 INFO sqlalchemy.engine.Engine CREATE TABLE some_table (x int, y int)
2025-02-26 10:45:20,963 INFO sqlalchemy.engine.Engine [generated in 0.00088s] ()
2025-02-26 10:45:20,963 INFO sqlalchemy.engine.Engine SELECT x, y FROM some_table
2025-02-26 10:45:20,964 INFO sqlalchemy.engine.Engine [generated in 0.00024s] ()
2025-02-26 10:45:20,964 INFO sqlalchemy.engine.Engine INSERT INTO some_table (x, y) VALUES (?, ?)
2025-02-26 10:45:20,964 INFO sqlalchemy.engine.Engine [generated in 0.00032s] [(6, 8), (9, 10)]
2025-02-26 10:45:20,965 INFO sqlalchemy.engine.Engine ROLLBACK
'''

''' script
쿼리의 결과를 result 객체에 저장, result는 namedtuple type으로 for문으로
조회할 수 있게 구현되어있음

이외에 result 객체를 읽는 여러 방법도 있음 ex) result.all()
'''

# 2. Sending Parameters
''' code
with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": i*2, "y": i*3}for i in range(1, 4)]  # 3행 데이터 삽입
    )
    result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2})
    for row in result:
        print(f"x: {row.x} y: {row.y}")
'''

''' console
2025-02-26 10:53:59,689 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-02-26 10:53:59,689 INFO sqlalchemy.engine.Engine CREATE TABLE some_table (x int, y int)
2025-02-26 10:53:59,689 INFO sqlalchemy.engine.Engine [generated in 0.00081s] ()
2025-02-26 10:53:59,690 INFO sqlalchemy.engine.Engine INSERT INTO some_table (x, y) VALUES (?, ?)
2025-02-26 10:53:59,691 INFO sqlalchemy.engine.Engine [generated in 0.00038s] [(2, 3), (4, 6), (6, 9)]
2025-02-26 10:53:59,691 INFO sqlalchemy.engine.Engine SELECT x, y FROM some_table WHERE y > ?
2025-02-26 10:53:59,691 INFO sqlalchemy.engine.Engine [generated in 0.00026s] (2,)
x: 2 y: 3
x: 4 y: 6
x: 6 y: 9
2025-02-26 10:53:59,692 INFO sqlalchemy.engine.Engine ROLLBACK
'''

# qmark 매개 변수 스타일
''' script

'''

# 3. Sending Multiple Parameters
''' code
with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 11, "y": 12}, {"x": 13, "y": 14}],
    )
    conn.commit()
'''

''' console
2025-02-26 11:00:46,226 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-02-26 11:00:46,227 INFO sqlalchemy.engine.Engine CREATE TABLE some_table (x int, y int)
2025-02-26 11:00:46,227 INFO sqlalchemy.engine.Engine [generated in 0.00104s] ()
2025-02-26 11:00:46,228 INFO sqlalchemy.engine.Engine INSERT INTO some_table (x, y) VALUES (?, ?)
2025-02-26 11:00:46,229 INFO sqlalchemy.engine.Engine [generated in 0.00054s] [(11, 12), (13, 14)]
2025-02-26 11:00:46,229 INFO sqlalchemy.engine.Engine COMMIT
'''

''' script
한 쿼리에 여러 행을 추가할 수 있는 로직
list comprehension를 활용하여 규칙이 있는 값들을 입력 가능
'''

# connection 객체
''' script
connection 객체는 내부적으로 cursor.executemany()를 사용
'''

# 4. Executing with an ORM Session
''' code
from sqlalchemy.orm import Session

stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")
with Session(engine) as session:
    result = session.execute(stmt, {"y": 6})
    for row in result:
        print(f"x: {row.x}  y: {row.y}")

with Session(engine) as session:
    result = session.execute(
        text("UPDATE some_table SET y=:y WHERE x=:x"),
        [{"x": 9, "y": 11}, {"x": 13, "y": 15}],
    )
    session.commit()
'''

''' console
2025-02-26 11:15:04,308 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-02-26 11:15:04,309 INFO sqlalchemy.engine.Engine SELECT x, y FROM some_table WHERE y > ? ORDER BY x, y
2025-02-26 11:15:04,309 INFO sqlalchemy.engine.Engine [generated in 0.00034s] (6,)
x: 11  y: 12
x: 13  y: 14
2025-02-26 11:15:04,310 INFO sqlalchemy.engine.Engine ROLLBACK
2025-02-26 11:15:04,310 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-02-26 11:15:04,310 INFO sqlalchemy.engine.Engine UPDATE some_table SET y=? WHERE x=?
2025-02-26 11:15:04,311 INFO sqlalchemy.engine.Engine [generated in 0.00021s] [(11, 9), (15, 13)]
2025-02-26 11:15:04,311 INFO sqlalchemy.engine.Engine COMMIT
'''

''' script
이전까지 사용했던 connect는 비ORM 형식
ORM을 사용하기 위해 session을 사용하고,
connect()로 구현한 것도 session을 사용한 방식으로 코드를 변경하여 
쉽게 변환이 가능
'''

# session
''' script
session은 트랜잭션이 종료된 후 DB와 연결을 유지하지 않음.
새로운 요청이 있을 때 새로운 연결을 요청함

Session은 with 블록 내에서 여러 개의 SQL을 실행할 때, 동일한 트랜잭션 내에서는 같은 Connection을 재사용하려고 한다. 
하지만, commit()이나 rollback()이 호출되면 트랜잭션이 종료되며, 이후 새로운 SQL 실행 시 새로운 Connection을 받을 수도 있다.

commit 함수 하나로 여러 쿼리를 하나의 트랜잭션으로 통합 -> 트랜잭션 자동 관리
'''

# Working with Database Metadata
# 1. Setting up MetaData with Table objects
# 여기서 말하는 Metadata는 DB의 구조를 Python 객체로 표현한 것, 와닿게 말하면 클래스로 표현한 것

''' code
from sqlalchemy import MetaData
metadata_obj = MetaData()

from sqlalchemy import Table, Column, Integer, String
user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)

print(user_table.c.name)
print(user_table.c.keys())
'''

''' console
user_account.name
['id', 'name', 'fullname']
'''

''' script
하나의 DB에 보통 한 개의 metadata를 선언하고, DB안에 여러 테이블을 정의
-> 코드 관리와 마이그레이션 상황에 유리

다만 다중 DB(MySQL, SQLite, PostgreSQL...)의 사용 시 분리하여 구현하는 것이 용이

metadata에 table을 정의하고 table 내에 column을 정의함. column은 Table.c 로 접근이 가능

Integer, String 객체는 SQL의 정수형과 문자열을 의미, 
code의 name column은 문자열 길이도 지정하여 column 전달 나머지 id, fullname은 객체 자체로 전달이 가능
'''

# 2. Declaring Simple Constraints
''' code
from sqlalchemy import MetaData
metadata_obj = MetaData()

from sqlalchemy import Table, Column, Integer, String
user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)

print(user_table.primary_key)

from sqlalchemy import ForeignKey
address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String, nullable=False),
)
'''

''' console
PrimaryKeyConstraint(Column('id', Integer(), table=<user_account>, primary_key=True, nullable=False))
'''

''' script
테이블 column에 기본키(Primary Key)나 외래키(Foreign Key)를 설정 가능
외래키의 경우 참조하고자 하는 테이블의 속성 이름을 지정 ex) table.id
외래키의 경우 null은 허용되나 예시에는 null을 허용하지 않았고 이를 nullable=False로 설정
또한 타입의 경우 참조한 속성의 설정을 따라감, 별도의 타입 표시가 없음
'''

# 3. Emitting DDL to the Database
''' code
metadata_obj = MetaData()

user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String, nullable=False),
)

metadata_obj.create_all(engine)
'''

''' console
2025-02-26 13:37:24,630 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-02-26 13:37:24,630 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("user_account")
2025-02-26 13:37:24,630 INFO sqlalchemy.engine.Engine [raw sql] ()
2025-02-26 13:37:24,631 INFO sqlalchemy.engine.Engine PRAGMA temp.table_info("user_account")
2025-02-26 13:37:24,631 INFO sqlalchemy.engine.Engine [raw sql] ()
2025-02-26 13:37:24,632 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("address")
2025-02-26 13:37:24,632 INFO sqlalchemy.engine.Engine [raw sql] ()
2025-02-26 13:37:24,632 INFO sqlalchemy.engine.Engine PRAGMA temp.table_info("address")
2025-02-26 13:37:24,632 INFO sqlalchemy.engine.Engine [raw sql] ()
2025-02-26 13:37:24,633 INFO sqlalchemy.engine.Engine
CREATE TABLE user_account (
        id INTEGER NOT NULL,
        name VARCHAR(30),
        fullname VARCHAR,
        PRIMARY KEY (id)
)


2025-02-26 13:37:24,634 INFO sqlalchemy.engine.Engine [no key 0.00058s] ()
2025-02-26 13:37:24,634 INFO sqlalchemy.engine.Engine
CREATE TABLE address (
        id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        email_address VARCHAR NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES user_account (id)
)


2025-02-26 13:37:24,635 INFO sqlalchemy.engine.Engine [no key 0.00068s] ()
2025-02-26 13:37:24,635 INFO sqlalchemy.engine.Engine COMMIT
'''

''' script
SQLite은 DDL 생성 프로세스에서 테이블의 현재 상태를 확인 후 DDL을 수행
테이블의 현재 상태를 확인하거나 변경하는 기능을 PRAGMA라고 함, 다른 SQLite 전용 기능

SQLite는 MySQL과 다르게 DDL을 트랜잭션 내에서 수행이 가능
MySQL의 경우 별도의 설정 이후 DDL을 트랜잭션 내에서 수행할 수 있는 옵션이 있긴 하나 기본적으로
DDL시 즉시 자동 커밋이 발생하여 트랜잭션이 종료
'''

# 4. Defining Table Metadata with the ORM
''' code
from sqlalchemy.orm import registry
mapper_registry = registry()

print(mapper_registry.metadata)

Base = mapper_registry.generate_base()

from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)
    addresses = relationship("Address", back_populates="user")
    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"))
    user = relationship("User", back_populates="addresses")
    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
'''

''' console
MetaData()
'''

''' script
3번 항목과 똑같은 결과를 다른 방식으로 구현, 4번 항목에서는 registry를 사용하여 선언적으로 
태이블을 정의하고 생성
'''

# registry tip
from sqlalchemy.orm import declarative_base

Base = declarative_base()

''' script
registry 선언 -> generate_base() 선언 과정을
declarative_base로 한 번에 동작 가능하게 하는 기존 방법도 사용이 가능

다만 registry를 사용하는 편이 확장과 다중 DB 관리에 용이, mapper_registry에 등록되어 명확한 ORM 관리 가능

간단한 프로젝트에 단일 ORM만 사용한다면 declarative_base, 그게 아니라면 registry를 사용하는 것이 합리적(?)

* SQLAlchemy 1.4+에서는 registry()를 사용하는 것이 공식적으로 더 권장되는 방식
'''

# 4-1. Declaring Mapped Classes
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)
    addresses = relationship("Address", back_populates="user")
    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"))
    user = relationship("User", back_populates="addresses")
    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

print(User.__table__)

sandy = User(name="sandy", fullname="Sandy Cheeks")
print(sandy)

sandy = User(name="sandy", fullname="Sandy Cheeks")
print(sandy)