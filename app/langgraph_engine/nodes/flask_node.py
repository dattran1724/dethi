import json
from flask import Flask, request
import threading

app = Flask(__name__)
storage = {"result": None}

@app.route('/result', methods=['GET'])
def show_result():
    result = storage.get("result")
    if not result:
        return "Chưa có dữ liệu", 200
    return f"""
        <html>
        <body>
            <h1>Kết quả từ MongoDB:</h1>
            <pre>{json.dumps(result, indent=2, ensure_ascii=False)}</pre>
        </body>
        </html>
    """

def run_flask():
    app.run(port=5001, debug=False)

# Chạy Flask ở thread riêng
threading.Thread(target=run_flask, daemon=True).start()

def flask_node(state):
    storage["result"] = state.get("result", {})
    return {"result": storage["result"]}
