from flask import Flask, request, render_template
import requests
from werkzeug.utils import secure_filename
import os

# 创建 Flask 应用
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'  # 设置文件上传的目标文件夹

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 定义路由，用于渲染对话页面
@app.route('/')
def home():
    return render_template('chat.html')  # 使用一个 HTML 模板

# 定义路由，处理来自对话页面的请求
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['message']  # 获取用户输入

    # 设置 API 请求的数据
    data = {
        "q": user_input,
        "key": "claude-asfkljfvoe",  # 密钥
    }
    files = {
        # 'file': ('case.txt', open('case.txt', 'rb'))  # 如果需要上传文件
    }
    url = "http://23.224.232.204/claude_api"

    # 发送请求到 API
    resp = requests.post(url, data=data, files=files)
    
    # 获取响应
    response = resp.json()
    print(resp.json()) 
    # 可以选择将响应直接返回给前端，或进行进一步处理
    return response

# 定义路由，处理文件上传
@app.route('/upload', methods=['POST'])
def file_upload():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File uploaded successfully'

# 启动应用
if __name__ == '__main__':
    app.run(debug=True)
