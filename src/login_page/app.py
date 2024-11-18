from flask import Flask, request, render_template
import threading

app = Flask(__name__)

# 전역 변수 및 이벤트 객체
_driver_name = None
driver_name_event = threading.Event()

def set_driver_name(name):
    """driver_name을 설정하는 함수"""
    global _driver_name
    _driver_name = name
    driver_name_event.set()  # 이벤트 플래그 설정

def get_driver_name():
    """driver_name을 가져오는 함수"""
    return _driver_name

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["driver_name"]
        print(f"Received driver name: {name}")
        set_driver_name(name)
        return "Driver name received. You can close this page."
    return render_template("index.html")

def run_flask():
    app.run(host="0.0.0.0", port=5000)
