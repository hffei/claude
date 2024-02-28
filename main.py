from flask import Flask, request, render_template, session, Response, jsonify
import os
from openai import OpenAI
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# 引入环境变量
load_dotenv()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# 创建 Flask 应用
app = Flask(__name__)
# 设置上传目录
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def home():
    return render_template('chat.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['message']
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        # 保存上传的文件到本地
        file_path = os.path.join(UPLOAD_FOLDER, secure_filename(uploaded_file.filename))
        uploaded_file.save(file_path)
        
        # 上传文件到 OpenAI API
        with open(file_path, 'rb') as f:
            file_object = client.files.create(file=f, purpose="file-extract")
        
        # 将文件内容添加到消息列表中
        file_content = client.files.content(file_id=file_object.id).text
        messages = [
            {"role": "system", "content": "文件上传成功并处理完成"},
            {"role": "system", "content": file_content},
            {"role": "user", "content": user_input},
        ]
        
        # 调用 OpenAI API
        completion = client.chat.completions.create(
            model="moonshot-v1-128k",
            messages=messages,
            temperature=0.3,
        )

        # 获取 AI 回复的内容
        ai_response_text = completion.choices[0].message.content

        return jsonify({'text': ai_response_text})
    else:
        return jsonify({'success': False, 'message': '未选择文件'})

# 启动应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
