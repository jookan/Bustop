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

def update_score(con,cur, driver_name, deduction_amount):
    cur.execute("SELECT score FROM Driver WHERE driver_name = ?;", (driver_name,))
    result = cur.fetchone()

    if result :
        current_score = result[0]
        new_score = current_score - deduction_amount
        new_score = max(new_score, 0)
        cur.execute("UPDATE Driver SET score = ? WHERE driver_name = ?;", (new_score, driver_name))
        con.commit()

        print(f'{driver_name}의 점수가 {deduction_amount}만큼 차감되어, 새로운 점수는 {new_score}입니다.')

con = sqlite3.connect(DB)
cur = con.cursor()

create_database(con, cur)
con.close()

