from flask import Flask, request, render_template, session
import requests
from werkzeug.utils import secure_filename
import os

# 创建 Flask 应用
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.secret_key = 'your_secret_key'

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['message']

    # 检查并保存上传的文件
    file = request.files.get('file')
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        files = {'file': (filename, open(file_path, 'rb'))}
    else:
        files = {}

    # 设置 API 请求的数据
    data = {
        "q": user_input,
        "key": "claude-asfkljfvoe",
    }
    url = "http://23.224.232.204/claude_api"

    # 发送请求到 API
    resp = requests.post(url, data=data, files=files)
    
    response = resp.json()
    return response

# 启动应用
if __name__ == '__main__':
    app.run(debug=True)
