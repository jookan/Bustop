import sqlite3

DB = "bus_database.db"

def create_database(con, cur):
    # 테이블 생성 (테이블이 이미 존재하면 오류 발생 방지)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Driver (
        idx INTEGER PRIMARY KEY,
        driver_name TEXT,
        score INTEGER,
        vc_num TEXT
    );
    """)

    # 샘플 데이터 삽입
    data = [
        (1, '이주환', 100, '12가3456'),
        (2, '천명호', 100, '34나5678'),
        (3, '김상우', 100, '56다7890'),
        (4, '최정우', 100, '78라9012')  # 쉼표 제거
    ]

    # 데이터 삽입 (이미 존재하는 경우 중복 방지)
    cur.executemany("INSERT OR IGNORE INTO Driver VALUES (?, ?, ?, ?);", data)
    # 변경사항 저장 및 연결 닫기
    con.commit()

con = sqlite3.connect(DB)
cur = con.cursor()

create_database(con, cur)
con.close()

