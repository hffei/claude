from flask import Flask, request, render_template, jsonify
import os
from openai import OpenAI
from dotenv import load_dotenv

app = Flask(__name__)

# 引入环境变量
load_dotenv()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

@app.route('/uploads', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        # 保存上传的文件到本地
        file_path = os.path.join('uploads', uploaded_file.filename)
        uploaded_file.save(file_path)
        
        # 上传文件到 OpenAI API
        with open(file_path, 'rb') as f:
            file_object = client.files.create(file=f, purpose="file-extract")
            # 通过 OpenAI 处理文件，获取结果
            # 这里可以根据需要处理 file_object 或者直接返回它
        
        # 返回处理结果
        return jsonify({'success': True, 'message': '文件上传成功并处理完成'})
    else:
        return jsonify({'success': False, 'message': '未选择文件'})

if __name__ == '__main__':
    app.run(debug=True)
