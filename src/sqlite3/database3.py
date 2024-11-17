import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox

DATABASE_FILE = "your_database.db"

def initialize_database():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS driver (
            idx INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            score INTEGER DEFAULT 100,
            vc_num TEXT DEFAULT NULL
        )
    ''')
    data = [
        (1, '이주환', 100, '62라1234'),
        (2, '김상우', 90, '11가5678'),
        (3, '박철수', 85, '33다9999')
    ]
    for record in data:
        cursor.execute('''
            INSERT OR IGNORE INTO driver (idx, name, score, vc_num)
            VALUES (?, ?, ?, ?)
        ''', record)
    conn.commit()
    conn.close()

def show_current_data():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM driver")
    rows = cursor.fetchall()
    print("Current data in the database:")
    for row in rows:
        print(row)
    conn.close()

def update_driver_table_with_opencv(conn, data_to_update, opencv_signal):
    try:
        cursor = conn.cursor()
        if opencv_signal == 1:
            for row in data_to_update:
                idx, name = row
                cursor.execute("SELECT score FROM driver WHERE idx = ? AND name = ?", (idx, name))
                result = cursor.fetchone()
                if result is None:
                    continue
                current_score = result[0]
                new_score = current_score - 1
                cursor.execute("UPDATE driver SET score = ? WHERE idx = ? AND name = ?", (new_score, idx, name))
                print(f"Updated idx={idx}, name={name}, score={new_score}")
            conn.commit()
    except sqlite3.Error as e:
        print("데이터베이스 오류:", e)
    finally:
        conn.close()

def handle_login():
    global data_to_update
    idx = idx_var.get().strip()
    name = name_var.get().strip()
    if not idx.isdigit():
        messagebox.showerror("Error", "idx는 숫자여야 합니다.")
        return
    idx = int(idx)
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM driver WHERE idx = ? AND name = ?", (idx, name))
    user = cursor.fetchone()
    if user:
        messagebox.showinfo("Success", f"로그인 성공: {name}")
        data_to_update = [(idx, name)]
        root.quit()
    else:
        messagebox.showerror("Error", "로그인 실패")
    conn.close()

def create_login_gui():
    global root, idx_var, name_var
    root = Tk()
    root.title("Driver Login")
    Label(root, text="기사님 번호 (idx):").grid(row=0, column=0, padx=10, pady=5)
    idx_var = StringVar()
    Entry(root, textvariable=idx_var).grid(row=0, column=1, padx=10, pady=5)
    Label(root, text="기사님 이름 (name):").grid(row=1, column=0, padx=10, pady=5)
    name_var = StringVar()
    Entry(root, textvariable=name_var).grid(row=1, column=1, padx=10, pady=5)
    Button(root, text="로그인", command=handle_login).grid(row=2, column=0, columnspan=2, pady=10)
    root.mainloop()

if __name__ == "__main__":
    data_to_update = []
    initialize_database()
    show_current_data()
    create_login_gui()
    if data_to_update:
        conn = sqlite3.connect(DATABASE_FILE)
        opencv_signal = 1
        update_driver_table_with_opencv(conn, data_to_update, opencv_signal)
