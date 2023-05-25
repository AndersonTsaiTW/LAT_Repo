from flask import Flask

# 創建 Flask 應用實例
app = Flask(__name__)

# 路由和處理函式
@app.route('/')
def hello():
    return 'Hello, World!'

# 啟動應用
if __name__ == '__main__':
    app.run()
