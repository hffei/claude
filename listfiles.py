from flask import Flask, request, render_template, session, Response, jsonify
import requests
# from werkzeug.utils import secure_filename
import os
from openai import OpenAI
from dotenv import load_dotenv


# 引入环境变量
load_dotenv()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# 列出文件列表
file_list = client.files.list()

# 查看每个文件的信息
for file in file_list.data:
    print(file)