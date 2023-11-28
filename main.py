from flask import Flask, request, render_template
import requests
from werkzeug.utils import secure_filename
import os

# 创建 Flask 应用
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.secret_key = 'your_secret_key'  # 在生产环境中应该从环境变量或配置文件中获取

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 初始化全局变量
global_id = ''
global_conversation_id = ''

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    global global_id, global_conversation_id

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
        "key": "claude-asfkljfvoe",  # 应从环境变量或配置文件中获取
    }
    if global_id:
        data['id'] = global_id
    if global_conversation_id:
        data['conversation_id'] = global_conversation_id

    url = "http://23.224.232.204/claude_api"

    # 发送请求到 API
    resp = requests.post(url, data=data, files=files)
    response_data = resp.json()
    global_id = response_data.get('id', global_id)  # 更新全局 id
    global_conversation_id = response_data.get('conversation_id', global_conversation_id)  # 更新全局 conversation_id

    # 输出会话 ID 用于调试
    print(global_id)
    print(global_conversation_id)

    return response_data

# 启动应用
if __name__ == '__main__':
    app.run(debug=True)  # 注意：在生产环境中应设置 debug=False
