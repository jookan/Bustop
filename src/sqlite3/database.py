import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('your_database.db')
c = conn.cursor()

#기존 테이블이 있다면 삭제하기!
c.execute("DROP TABLE IF EXISTS driver")

# 테이블 생성
c.execute('''
    CREATE TABLE driver (
        idx INTEGER PRIMARY KEY AUTOINCREMENT,       -- 인덱스, 자동 증가 필드
        name VARCHAR(10) DEFAULT NULL,               -- 사용자 이름, NULL 허용
        score FLOAT DEFAULT 100,                     -- 운행 점수, 기본값 100
        vc_num VARCHAR(10) DEFAULT NULL              -- 차량 번호, NULL 허용
    )
''')

data_to_insert = [
    (1, '이주환', 100, '62라1234'),
    (2, '김상우', 90, '11가5678'),
    (3, '박철수', 85, '33다9999')
]

# 여러 행을 한 번에 삽입
c.executemany("INSERT INTO driver (idx, name, score, vc_num) VALUES (?, ?, ?, ?)", data_to_insert)

# 변경사항 저장
conn.commit()
c.execute("SELECT * FROM driver")
rows = c.fetchall()  # 모든 데이터를 가져옴

# 데이터 출력
for row in rows:
    print("모든 기사님들의 데이터 출력",row)
    

c.execute("SELECT * FROM driver WHERE score >= ?", (90,))
rows = c.fetchall()
for row in rows:
    print("점수가 90점 이상인 기사님",row)

    

# 변경사항 저장 및 연결 종료
conn.commit()
conn.close()


