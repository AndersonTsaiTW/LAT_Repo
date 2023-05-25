from flask import Flask, request

app = Flask(__name__)

@app.route("/example", methods=["POST"])
def example():
    data = request.get_data()
    # 处理原始数据
    # ...

    return "OK"

if __name__ == "__main__":
    app.run()
